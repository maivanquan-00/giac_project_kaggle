"""
model_v2.py
-----------
GIACModelV2 — phiên bản nâng cấp, giữ nguyên model.py (v1) để A/B.

Khác biệt so với v1:
  1. Encoder = MultiOmicGATModuleV2 (patient-conditioned GAT — xem gat_encoder_v2.py).
     → inject giá trị bệnh nhân vào node features TRƯỚC GAT, tất cả CpG/miRNA value
       đều lan truyền qua đồ thị (sửa tận gốc #1/#6).
  2. ModalityCrossAttentionV2: trọng số fusion cpg/mirna CÁ THỂ HOÁ theo từng bệnh
     nhân (gate sinh từ z_gene), thay cho 1 tham số global của v1 (sửa #5).

Cross-attention giữ kiến trúc asymmetric như v1 (gene=Q, cpg/mirna=K/V, entmax15)
nên tên param Q/K/V không đổi → frobenius_regularization_loss vẫn hoạt động.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from entmax import entmax15

from src.models.gat_encoder_v2 import MultiOmicGATModuleV2
from src.models.classifier import FocalLoss, SubtypeClassifier, SupConLoss, frobenius_regularization_loss


class ModalityCrossAttentionV2(nn.Module):
    """Asymmetric cross-attention + per-patient modality fusion.

    Gene (B,H) là Query, CpG/miRNA (B,K,H) là Key/Value. Khác v1: trọng số trộn
    ctx_cpg vs ctx_mirna do một gate nhỏ sinh ra TỪNG BỆNH NHÂN (điều kiện trên
    z_gene), thay vì 1 tham số global dùng chung.
    """

    def __init__(self, hidden_dim: int, n_heads: int, dropout: float, alpha: float = 1.5):
        super().__init__()
        assert hidden_dim % n_heads == 0
        self.H        = hidden_dim
        self.n_heads  = n_heads
        self.head_dim = hidden_dim // n_heads
        self.scale    = self.head_dim ** -0.5
        self.alpha    = alpha

        self.W_q = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_k_cpg   = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_v_cpg   = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_k_mirna = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_v_mirna = nn.Linear(hidden_dim, hidden_dim, bias=False)

        self.W_out   = nn.Linear(hidden_dim * 2, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.norm    = nn.LayerNorm(hidden_dim)

        # Per-patient modality gate: z_gene → 2 logits (cpg, mirna).
        # Init lớp cuối = 0 → softmax = [0.5, 0.5] (giống init global logits=0 của v1).
        self.modality_gate = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 2),
        )
        nn.init.zeros_(self.modality_gate[-1].weight)
        nn.init.zeros_(self.modality_gate[-1].bias)

        # Learnable log-temperature cho attention sharpening (init temp ≈ 2)
        self.log_temp = nn.Parameter(torch.tensor(0.69))

    def _attend(self, q, W_k, W_v, kv_seq):
        B, K, _ = kv_seq.shape
        Q = self.W_q(q).view(B, self.n_heads, 1, self.head_dim)
        K_ = W_k(kv_seq).view(B, K, self.n_heads, self.head_dim).transpose(1, 2)
        V_ = W_v(kv_seq).view(B, K, self.n_heads, self.head_dim).transpose(1, 2)

        scores = torch.matmul(Q, K_.transpose(-2, -1)) * self.scale * self.log_temp.exp()
        if self.alpha == 1.0:
            attn = F.softmax(scores, dim=-1)
        else:
            attn = entmax15(scores, dim=-1)
        ctx = torch.matmul(attn, V_)
        ctx = self.dropout(ctx)
        ctx = ctx.squeeze(2).transpose(1, 2).contiguous().view(B, self.H)

        attn_w = attn.mean(dim=1).squeeze(1)              # (B, K)
        return ctx, attn_w

    def forward(self, z_gene, z_cpg_seq, z_mirna_seq, return_attn=False):
        ctx_cpg,   attn_cpg   = self._attend(z_gene, self.W_k_cpg,   self.W_v_cpg,   z_cpg_seq)
        ctx_mirna, attn_mirna = self._attend(z_gene, self.W_k_mirna, self.W_v_mirna, z_mirna_seq)

        w = F.softmax(self.modality_gate(z_gene), dim=-1)            # (B, 2) per-patient
        combined = torch.cat([w[:, 0:1] * ctx_cpg, w[:, 1:2] * ctx_mirna], dim=-1)  # (B, 2H)
        fused = self.norm(self.W_out(combined) + z_gene)

        if return_attn:
            return fused, {
                "cpg_attn":         attn_cpg,        # (B, K)
                "mirna_attn":       attn_mirna,      # (B, K)
                "modality_weights": w.mean(dim=0),   # (2,) mean batch — tương thích pipeline cũ
                "modality_weights_per_patient": w,   # (B, 2) — tín hiệu cá thể hoá
            }
        return fused, None


class GIACModelV2(nn.Module):

    def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
        super().__init__()
        H           = cfg_model["hidden_dim"]
        num_classes = cfg_model["num_classes"]
        topk        = cfg_model.get("topk_seq", 32)

        self.gat = MultiOmicGATModuleV2(
            dims       = dims,
            hidden_dim = H,
            n_heads    = cfg_model["gat_heads"],
            n_layers   = cfg_model["gat_layers"],
            dropout    = cfg_model.get("gat_dropout", 0.3),
            topk_seq   = topk,
            gat_chunk  = cfg_model.get("gat_chunk", 4),
        )
        self.cross_attn = ModalityCrossAttentionV2(
            hidden_dim = H,
            n_heads    = cfg_model.get("ca_heads", 4),
            dropout    = cfg_model.get("ca_dropout", 0.2),
            alpha      = cfg_model.get("sparsemax_alpha", 1.5),
        )
        self.classifier = SubtypeClassifier(
            hidden_dim  = H,
            final_dim   = cfg_model["final_dim"],
            num_classes = num_classes,
            dropout     = cfg_model.get("classifier_dropout", 0.5),
        )

        self.loss_name = cfg_train.get("loss_name", "focal").lower()
        self.register_buffer("class_weights", torch.ones(num_classes, dtype=torch.float32))
        self.focal_loss = FocalLoss(
            gamma           = cfg_train["focal_gamma"],
            alpha           = cfg_train["focal_alpha"],
            num_classes     = num_classes,
            label_smoothing = cfg_train.get("label_smoothing", 0.0),
        )
        self.lambda_frob   = cfg_train.get("lambda_frobenius", 0.01)
        self.lambda_supcon = cfg_train.get("lambda_supcon", 0.0)
        if self.lambda_supcon > 0.0:
            self.supcon_loss = SupConLoss(
                temperature=cfg_train.get("supcon_temperature", 0.07)
            )

    def set_class_weights(self, w):
        norm = w / w.mean().clamp_min(1e-8)
        self.class_weights.copy_(norm.to(self.class_weights.device))
        self.focal_loss.set_alpha(self.class_weights)

    def forward(self, batch, graph, return_interpretability=False, return_embeddings=False):
        z_gene, z_cpg_seq, z_mirna_seq = self.gat(batch, graph)
        fused, attn_info = self.cross_attn(z_gene, z_cpg_seq, z_mirna_seq, return_attn=True)
        logits = self.classifier(fused)

        if return_interpretability:
            return logits, None, attn_info
        if return_embeddings:
            return logits, fused, attn_info
        return logits, attn_info

    def compute_loss(self, logits, labels, attn_info=None, embeddings=None):
        if self.loss_name == "cross_entropy":
            loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
        else:
            loss_cls = self.focal_loss(logits, labels)
        loss_frob = frobenius_regularization_loss(
            self.cross_attn, self.lambda_frob, param_prefix="W_"
        )
        loss = loss_cls + loss_frob
        if embeddings is not None and self.lambda_supcon > 0.0:
            loss = loss + self.lambda_supcon * self.supcon_loss(embeddings, labels)
        return loss
