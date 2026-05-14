import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from entmax import entmax15

from src.models.gat_encoder import MultiOmicGATModule
from src.models.classifier import FocalLoss, SubtypeClassifier, SupConLoss, frobenius_regularization_loss


class ModalityCrossAttention(nn.Module):
    """
    Asymmetric cross-attention: gene as Query (sequence, Phase 3.1), CpG/miRNA (B,K,H) as Key/Value.

    Phase 3.1 changes from 2.1a:
      - Q is now (B, K_g, H) gene sequence instead of (B, H) summary
      - Multi-token Q → each gene token gets its own ctx_cpg, ctx_mirna
      - After cross-attention, mean-pool gene sequence to (B, H)
      - Cách C: concat[pooled, z_gene_summary] → W_combine → final (preserves baseline strength)

    Entmax15 produces sparse weights → interpretable.
    """

    def __init__(self, hidden_dim: int, n_heads: int, dropout: float, alpha: float = 1.5):
        super().__init__()
        assert hidden_dim % n_heads == 0
        self.H        = hidden_dim
        self.n_heads  = n_heads
        self.head_dim = hidden_dim // n_heads
        self.scale    = self.head_dim ** -0.5
        self.alpha    = alpha

        # Gene query projection
        self.W_q = nn.Linear(hidden_dim, hidden_dim, bias=False)

        # Separate K/V projections per regulatory modality
        self.W_k_cpg   = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_v_cpg   = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_k_mirna = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_v_mirna = nn.Linear(hidden_dim, hidden_dim, bias=False)

        # Combine both modality contexts (B, K_g, 2H) → (B, K_g, H)
        self.W_out   = nn.Linear(hidden_dim * 2, hidden_dim)
        # Phase 3.1 Cách C: combine [pooled gene seq | gene summary] → H
        self.W_combine = nn.Linear(hidden_dim * 2, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.norm    = nn.LayerNorm(hidden_dim)

        # Global modality importance (2: cpg, mirna)
        self.modality_logits = nn.Parameter(torch.zeros(2))

        # Learnable log-temperature for attention sharpening.
        self.log_temp = nn.Parameter(torch.tensor(0.69))

    @property
    def modality_weights(self):
        return F.softmax(self.modality_logits, dim=0)

    def _attend_seq(self, q_seq, W_k, W_v, kv_seq):
        """
        Phase 3.1: sequence Q cross-attention.
        q_seq  : (B, K_g, H) — gene sequence query
        kv_seq : (B, K, H)   — cpg or mirna sequence
        Returns ctx (B, K_g, H) and attn (B, K_g, K) averaged over heads.
        """
        B, K_g, _ = q_seq.shape
        _, K, _   = kv_seq.shape

        # Q: (B, n_heads, K_g, head_dim)
        Q = self.W_q(q_seq).view(B, K_g, self.n_heads, self.head_dim).transpose(1, 2)
        # K, V: (B, n_heads, K, head_dim)
        K_ = W_k(kv_seq).view(B, K, self.n_heads, self.head_dim).transpose(1, 2)
        V_ = W_v(kv_seq).view(B, K, self.n_heads, self.head_dim).transpose(1, 2)

        # Attention scores: (B, n_heads, K_g, K)
        scores = torch.matmul(Q, K_.transpose(-2, -1)) * self.scale * self.log_temp.exp()
        if self.alpha == 1.0:
            attn = F.softmax(scores, dim=-1)
        else:
            attn = entmax15(scores, dim=-1)
        ctx = torch.matmul(attn, V_)                        # (B, n_heads, K_g, head_dim)
        ctx = self.dropout(ctx)
        ctx = ctx.transpose(1, 2).contiguous().view(B, K_g, self.H)  # (B, K_g, H)

        # Average attention over heads: (B, K_g, K)
        attn_w = attn.mean(dim=1)
        return ctx, attn_w

    def forward(self, z_gene_summary, z_gene_seq, z_cpg_seq, z_mirna_seq, return_attn=False):
        # Multi-Q cross-attention (Phase 3.1)
        ctx_cpg,   attn_cpg   = self._attend_seq(z_gene_seq, self.W_k_cpg,   self.W_v_cpg,   z_cpg_seq)
        ctx_mirna, attn_mirna = self._attend_seq(z_gene_seq, self.W_k_mirna, self.W_v_mirna, z_mirna_seq)
        # ctx_*: (B, K_g, H)

        w = self.modality_weights                                            # (2,)
        combined = torch.cat([w[0] * ctx_cpg, w[1] * ctx_mirna], dim=-1)     # (B, K_g, 2H)
        seq_fused = self.norm(self.W_out(combined) + z_gene_seq)             # (B, K_g, H) — residual w/ seq

        # Pool gene sequence to single vector (mean over K_g tokens)
        seq_pooled = seq_fused.mean(dim=1)                                   # (B, H)

        # Phase 3.1 Cách C: combine pooled sequence + summary (residual w/ summary)
        final = self.norm(self.W_combine(torch.cat([seq_pooled, z_gene_summary], dim=-1)) + z_gene_summary)
        # (B, H)

        if return_attn:
            # Aggregate attention over gene tokens for interpretability: (B, K)
            return final, {
                "cpg_attn":        attn_cpg.mean(dim=1),     # (B, K_c)
                "mirna_attn":      attn_mirna.mean(dim=1),   # (B, K_m)
                "modality_weights": w,                       # (2,)
            }
        return final, None


class GIACModel(nn.Module):

    def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
        super().__init__()
        H           = cfg_model["hidden_dim"]
        num_classes = cfg_model["num_classes"]
        topk        = cfg_model.get("topk_seq", 32)
        topk_gene   = cfg_model.get("topk_seq_gene", topk)   # Phase 3.1: default = topk

        self.gat = MultiOmicGATModule(
            dims          = dims,
            hidden_dim    = H,
            n_heads       = cfg_model["gat_heads"],
            n_layers      = cfg_model["gat_layers"],
            dropout       = cfg_model.get("gat_dropout", 0.3),
            topk_seq      = topk,
            topk_seq_gene = topk_gene,
        )
        self.cross_attn = ModalityCrossAttention(
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
        z_gene_summary, z_gene_seq, z_cpg_seq, z_mirna_seq = self.gat(batch, graph)
        fused, attn_info = self.cross_attn(
            z_gene_summary, z_gene_seq, z_cpg_seq, z_mirna_seq, return_attn=True
        )
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
