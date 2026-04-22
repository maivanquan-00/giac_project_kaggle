"""
model.py
--------
GIACModel: Heterogeneous Graph + GAT + Cross-Attention pipeline.

Architecture
============

  [Gene (B,F_g)]  [Meth (B,F_m)]  [miRNA (B,F_r)]
        |               |                |
        └───────── MultiOmicGATModule ───┘
                  (HeteroGraph + GATv2)
                        |
          z_gene (B,H)  z_cpg (B,H)  z_mirna (B,H)
                        |
              ModalityCrossAttention
              ┌─────────────────────┐
              │ Q=z_gene            │  gene attends over cpg & mirna
              │ K,V=[z_cpg,z_mirna] │  (biologically: cpg/mirna regulate genes)
              └─────────────────────┘
                        |
                  fused (B,H)
                        |
              SubtypeClassifier  →  logits (B,5)

Cross-Attention design
----------------------
Asymmetric: gene is always the Query. CpG and miRNA are Keys/Values.
This matches biology: methylation and miRNA *regulate* gene expression,
not the reverse. The fusion output is a gene-centric representation
enriched with epigenetic (CpG) and post-transcriptional (miRNA) context.

Each head independently computes:
    Attn(Q_gene, K_mod, V_mod) for mod in {cpg, mirna}
Output is concatenated across modalities then projected.

Phase history notes
-------------------
Phase A: cross-attention was symmetric (all attend to all) → destructive,
         all < meth_only in ablation.
Phase B-Q: replaced with gated MLP fusion → better but gate collapsed.
Phase 20+: return to asymmetric cross-attention with proper Q=gene design.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData

from src.models.gat_encoder import MultiOmicGATModule
from src.models.classifier import FocalLoss, SubtypeClassifier, frobenius_regularization_loss


# ─────────────────────────────────────────────────────────────────────────────
#  Asymmetric Cross-Attention Fusion
# ─────────────────────────────────────────────────────────────────────────────

class ModalityCrossAttention(nn.Module):
    """
    Asymmetric multi-head cross-attention: gene queries, {cpg, mirna} as keys/values.

    For each regulatory modality m in {cpg, mirna}:
        head_i = softmax( Q_i K_m_i^T / sqrt(d) ) V_m_i
    All heads and modalities are concatenated then projected back to H.

    Parameters
    ----------
    hidden_dim   : H
    n_heads      : number of attention heads
    dropout      : dropout on attention weights
    modality_temperature : temperature for modality weight softmax (interpretability)
    """

    # def __init__(
    #     self,
    #     hidden_dim: int,
    #     n_heads:    int,
    #     dropout:    float,
    #     modality_temperature: float = 1.0,
    # ):
    #     super().__init__()
    #     assert hidden_dim % n_heads == 0
    #     self.hidden_dim = hidden_dim
    #     self.n_heads    = n_heads
    #     self.head_dim   = hidden_dim // n_heads
    #     self.scale      = self.head_dim ** -0.5
    #     self.temperature = max(float(modality_temperature), 1e-3)

    #     # Query projection: gene
    #     self.W_q = nn.Linear(hidden_dim, hidden_dim, bias=False)

    #     # Key/Value projections: one pair per regulatory modality
    #     self.W_k_cpg   = nn.Linear(hidden_dim, hidden_dim, bias=False)
    #     self.W_v_cpg   = nn.Linear(hidden_dim, hidden_dim, bias=False)
    #     self.W_k_mirna = nn.Linear(hidden_dim, hidden_dim, bias=False)
    #     self.W_v_mirna = nn.Linear(hidden_dim, hidden_dim, bias=False)

    #     # Output projection  (2 modalities × H -> H)
    #     self.W_out = nn.Linear(hidden_dim * 2, hidden_dim)

    #     self.dropout = nn.Dropout(dropout)
    #     self.norm    = nn.LayerNorm(hidden_dim)

    #     # Learnable global modality importance weights (interpretability)
    #     # logits[0] = cpg importance, logits[1] = mirna importance
    #     self.modality_logits = nn.Parameter(torch.zeros(2))

    # @property
    # def modality_weights(self) -> torch.Tensor:
    #     """Softmax-normalised global modality weights (2,)."""
    #     return F.softmax(self.modality_logits / self.temperature, dim=0)

    # def _attend(
    #     self,
    #     q: torch.Tensor,   # (B, H)  gene query
    #     k: torch.Tensor,   # (B, H)  modality key
    #     v: torch.Tensor,   # (B, H)  modality value
    # ) -> tuple[torch.Tensor, torch.Tensor]:
    #     """
    #     Single-modality multi-head cross-attention.
    #     q, k, v are each (B, H).
    #     Returns:
    #         context : (B, H)
    #         attn_w  : (B, n_heads, 1, 1) — averaged attention weight for interpretability
    #     """
    #     B = q.shape[0]

    #     # Project and reshape to (B, n_heads, 1, head_dim)
    #     def proj_reshape(x, W):
    #         return W(x).view(B, self.n_heads, 1, self.head_dim)

    #     Q = proj_reshape(q, self.W_q)    # gene query
    #     # k and v are (B, H) -> treat as single token: (B, n_heads, 1, head_dim)
    #     # We reshape K/V as sequence of 1 token (each patient, each modality = 1 vec)
    #     K = k.view(B, self.n_heads, 1, self.head_dim)
    #     V = v.view(B, self.n_heads, 1, self.head_dim)

    #     # Attention: (B, n_heads, 1, 1)
    #     scores  = torch.matmul(Q, K.transpose(-2, -1)) * self.scale
    #     attn_w  = F.softmax(scores, dim=-1)                # softmax over 1 key → always 1.0
    #     attn_w  = self.dropout(attn_w)

    #     # Context: (B, n_heads, 1, head_dim) -> (B, H)
    #     context = torch.matmul(attn_w, V)
    #     context = context.view(B, self.hidden_dim)

    #     return context, attn_w

    # def forward(
    #     self,
    #     z_gene:  torch.Tensor,   # (B, H)
    #     z_cpg:   torch.Tensor,   # (B, H)
    #     z_mirna: torch.Tensor,   # (B, H)
    #     return_attn: bool = False,
    # ):
    #     """
    #     Returns
    #     -------
    #     fused   : (B, H)
    #     attn    : dict with keys "cpg_attn", "mirna_attn", "modality_weights"
    #               (only when return_attn=True)
    #     """
    #     # ── Cross-attention: gene -> cpg ────────────────────────────────
    #     ctx_cpg,   attn_cpg   = self._attend(
    #         z_gene, self.W_k_cpg(z_cpg),   self.W_v_cpg(z_cpg)
    #     )
    #     # ── Cross-attention: gene -> mirna ──────────────────────────────
    #     ctx_mirna, attn_mirna = self._attend(
    #         z_gene, self.W_k_mirna(z_mirna), self.W_v_mirna(z_mirna)
    #     )

    #     # ── Modality-weighted combination ───────────────────────────────
    #     w = self.modality_weights  # (2,)
    #     # Weight each modality's context before concatenation
    #     weighted = torch.cat([w[0] * ctx_cpg, w[1] * ctx_mirna], dim=-1)  # (B, 2H)

    #     # ── Output projection + residual (gene as anchor) ───────────────
    #     fused = self.W_out(weighted)              # (B, H)
    #     fused = self.norm(fused + z_gene)         # residual: gene is the anchor

    #     if return_attn:
    #         return fused, {
    #             "cpg_attn":        attn_cpg.mean(dim=1).squeeze(-1).squeeze(-1),   # (B,)
    #             "mirna_attn":      attn_mirna.mean(dim=1).squeeze(-1).squeeze(-1), # (B,)
    #             "modality_weights": w,   # (2,) — global
    #         }
    #     return fused

    def __init__(
        self,
        hidden_dim: int,
        n_heads: int,
        dropout: float,
        modality_temperature: float = 1.0, # Giữ lại để tương thích signature cũ
    ):
        super().__init__()
        self.hidden_dim = hidden_dim
        
        # Dùng MultiheadAttention chuẩn của PyTorch
        self.self_attn = nn.MultiheadAttention(
            embed_dim=hidden_dim, 
            num_heads=n_heads, 
            dropout=dropout, 
            batch_first=True
        )
        
        self.norm = nn.LayerNorm(hidden_dim)
        
        # Project từ 3 tokens đã được attention về lại hidden_dim
        self.W_out = nn.Linear(hidden_dim * 3, hidden_dim)

    def forward(
        self,
        z_gene:  torch.Tensor,   # (B, H)
        z_cpg:   torch.Tensor,   # (B, H)
        z_mirna: torch.Tensor,   # (B, H)
        return_attn: bool = False,
    ):
        B = z_gene.shape[0]
        
        # Stack thành sequence 3 tokens: (B, 3, H)
        # Index: 0=gene, 1=cpg, 2=mirna
        seq = torch.stack([z_gene, z_cpg, z_mirna], dim=1)

        # Chạy full self-attention
        # attn_out: (B, 3, H), attn_weights: (B, 3, 3)
        attn_out, attn_weights = self.self_attn(seq, seq, seq)

        # Flatten 3 tokens thành 1 vector duy nhất rồi project về lại H
        flat = attn_out.reshape(B, -1)      # (B, 3 * H)
        fused = self.W_out(flat)            # (B, H)

        # Residual connection: gene vẫn đóng vai trò là anchor
        fused = self.norm(fused + z_gene)

        if return_attn:
            # Lấy attention weights của gene (query 0) chú ý vào cpg (key 1) và mirna (key 2)
            cpg_attn = attn_weights[:, 0, 1]
            mirna_attn = attn_weights[:, 0, 2]
            
            # Tính weight trung bình toàn cục cho interpretability
            return fused, {
                "cpg_attn": cpg_attn,
                "mirna_attn": mirna_attn,
                "modality_weights": torch.tensor([cpg_attn.mean(), mirna_attn.mean()], device=z_gene.device)
            }
            
        return fused


# ─────────────────────────────────────────────────────────────────────────────
#  Main model
# ─────────────────────────────────────────────────────────────────────────────

class GIACModel(nn.Module):
    """
    Full pipeline: GAT encoder -> Cross-Attention fusion -> Classifier.

    Parameters
    ----------
    dims      : {"gene": F_g, "meth": F_m, "mirna": F_r}  (post-ANOVA dims)
    cfg_model : model section of config.yaml
    cfg_train : training section of config.yaml
    """

    def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
        super().__init__()

        H           = cfg_model["hidden_dim"]
        num_classes = cfg_model["num_classes"]
        gat_drop    = cfg_model.get("gat_dropout", 0.3)
        attn_drop   = cfg_model.get("cross_attn_dropout", 0.3)
        cls_drop    = cfg_model.get("classifier_dropout", 0.5)

        # ── Module 1: Heterogeneous GAT ───────────────────────────────────
        self.gat = MultiOmicGATModule(
            dims       = dims,
            hidden_dim = H,
            n_heads    = cfg_model["gat_heads"],
            n_layers   = cfg_model["gat_layers"],
            dropout    = gat_drop,
        )

        # ── Module 2: Asymmetric Cross-Attention Fusion ───────────────────
        self.cross_attn = ModalityCrossAttention(
            hidden_dim           = H,
            n_heads              = cfg_model.get("cross_attn_heads", 4),
            dropout              = attn_drop,
            modality_temperature = cfg_model.get("modality_temperature", 1.0),
        )

        # ── Module 3: Classifier head ─────────────────────────────────────
        self.classifier = SubtypeClassifier(
            hidden_dim  = H,
            final_dim   = cfg_model["final_dim"],
            num_classes = num_classes,
            dropout     = cls_drop,
        )

        # ── Loss ──────────────────────────────────────────────────────────
        self.loss_name = cfg_train.get("loss_name", "focal").lower()
        self.register_buffer(
            "class_weights", torch.ones(num_classes, dtype=torch.float32)
        )
        self.focal_loss = FocalLoss(
            gamma           = cfg_train["focal_gamma"],
            alpha           = cfg_train["focal_alpha"],
            num_classes     = num_classes,
            label_smoothing = cfg_train.get("label_smoothing", 0.0),
        )
        self.lambda_frob = cfg_train.get("lambda_frobenius", 0.01)

    # ── Convenience ───────────────────────────────────────────────────────────

    def set_class_weights(self, w: torch.Tensor):
        norm = w / w.mean().clamp_min(1e-8)
        self.class_weights.copy_(norm.to(self.class_weights.device))
        self.focal_loss.set_alpha(self.class_weights)

    # ── Forward ───────────────────────────────────────────────────────────────

    def forward(
        self,
        batch: dict,
        graph: HeteroData,
        return_interpretability: bool = False,
    ):
        """
        Parameters
        ----------
        batch  : {"gene": (B,F_g), "meth": (B,F_m), "mirna": (B,F_r), "label": (B,)}
        graph  : HeteroData (built once per fold by build_hetero_graph)
        return_interpretability : if True, return attention weights dict

        Returns (training)
        ------------------
        logits      : (B, num_classes)
        attn_info   : dict  — cross-attention weights for monitoring/logging

        Returns (interpretability)
        --------------------------
        logits, None, {
            "cpg_attn"        : (B,)   — per-patient cpg attention
            "mirna_attn"      : (B,)   — per-patient mirna attention
            "modality_weights": (2,)   — global [cpg_weight, mirna_weight]
        }
        """
        # Step 1: GAT encoding
        z_gene, z_cpg, z_mirna = self.gat(batch, graph)

        # Step 2: Cross-attention fusion
        if return_interpretability:
            fused, attn_info = self.cross_attn(
                z_gene, z_cpg, z_mirna, return_attn=True
            )
            logits = self.classifier(fused)
            return logits, None, attn_info

        fused, attn_info = self.cross_attn(
            z_gene, z_cpg, z_mirna, return_attn=True
        )

        # Step 3: Classification
        logits = self.classifier(fused)

        return logits, attn_info

    # ── Loss ──────────────────────────────────────────────────────────────────

    def compute_loss(
        self,
        logits:    torch.Tensor,
        labels:    torch.Tensor,
        attn_info: dict | None = None,
    ) -> torch.Tensor:
        if self.loss_name == "cross_entropy":
            loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
        else:
            loss_cls = self.focal_loss(logits, labels)

        # Frobenius regularisation on cross-attention weight matrices
        loss_frob = frobenius_regularization_loss(
            self.cross_attn, self.lambda_frob, param_prefix="W_"
        )

        return loss_cls + loss_frob