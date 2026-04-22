"""
model.py — GIACModel: HeteroGAT + 3-token Self-Attention Fusion + Classifier

Architecture
============
  [Gene(B,Fg)]  [Meth(B,Fm)]  [miRNA(B,Fr)]
       |              |              |
       └──── MultiOmicGATModule ─────┘
             (HeteroGraph + GATv2)
                     |
       z_gene(B,H)  z_cpg(B,H)  z_mirna(B,H)
                     |
          ModalityFusionAttention
          ┌──────────────────────┐
          │ Stack → (B, 3, H)    │  3-token sequence
          │ Multi-head attention  │  gene ↔ cpg ↔ mirna
          │ Entmax15 (sparse)     │  interpretable weights
          │ gene token as output  │  gene = anchor
          └──────────────────────┘
                     |
               fused (B, H)
                     |
          SubtypeClassifier → logits (B,5)

Fix vs previous version
-----------------------
Previous ModalityCrossAttention used 1-token K/V → softmax(1 score) = 1.0 always
→ attention was mathematically degenerate (no learning possible).

This version stacks all 3 modalities as a 3-token sequence and runs full
multi-head self-attention, so attention scores are computed over 3 keys and
softmax produces meaningful non-trivial weights.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from entmax import entmax15

from src.models.gat_encoder import MultiOmicGATModule
from src.models.classifier import FocalLoss, SubtypeClassifier, frobenius_regularization_loss


# ─────────────────────────────────────────────────────────────────────────────
#  3-token Self-Attention Fusion
# ─────────────────────────────────────────────────────────────────────────────

class ModalityFusionAttention(nn.Module):
    """
    Multi-head attention over a 3-token sequence [z_gene, z_cpg, z_mirna].

    Each modality is treated as one token. Full self-attention is computed
    so every modality can attend to every other. The gene token output is
    used as the fused representation (gene as anchor — biology-motivated:
    methylation and miRNA regulate gene expression, not the reverse).

    Entmax15 replaces softmax → sparse attention, some modalities get
    exactly 0 weight per patient → interpretable & prevents noisy modalities
    from diluting the signal.

    Parameters
    ----------
    hidden_dim : H  (must be divisible by n_heads)
    n_heads    : attention heads
    dropout    : dropout on attention weights
    alpha      : entmax alpha (1.0=softmax, 1.5=entmax15, 2.0=sparsemax)
    """

    def __init__(self, hidden_dim: int, n_heads: int, dropout: float, alpha: float = 1.5):
        super().__init__()
        assert hidden_dim % n_heads == 0
        self.H        = hidden_dim
        self.n_heads  = n_heads
        self.head_dim = hidden_dim // n_heads
        self.scale    = self.head_dim ** -0.5
        self.alpha    = alpha

        # Shared Q, K, V projections (same weights for all 3 tokens)
        self.W_q = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_k = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_v = nn.Linear(hidden_dim, hidden_dim, bias=False)

        self.W_out  = nn.Linear(hidden_dim, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.norm    = nn.LayerNorm(hidden_dim)

        # Learnable modality importance (3 logits → softmax → interpretable weights)
        self.modality_logits = nn.Parameter(torch.zeros(3))

    @property
    def modality_weights(self) -> torch.Tensor:
        """Global modality weights (3,): [gene, cpg, mirna]."""
        return F.softmax(self.modality_logits, dim=0)

    def forward(
        self,
        z_gene:  torch.Tensor,  # (B, H)
        z_cpg:   torch.Tensor,  # (B, H)
        z_mirna: torch.Tensor,  # (B, H)
        return_attn: bool = False,
    ):
        B = z_gene.shape[0]

        # ── Stack into sequence (B, 3, H) ──────────────────────────────
        C = torch.stack([z_gene, z_cpg, z_mirna], dim=1)  # (B, 3, H)

        # ── Multi-head projections → (B, n_heads, 3, head_dim) ─────────
        def proj(x, W):
            return W(x).view(B, 3, self.n_heads, self.head_dim).transpose(1, 2)

        Q = proj(C, self.W_q)   # (B, n_heads, 3, head_dim)
        K = proj(C, self.W_k)
        V = proj(C, self.W_v)

        # ── Attention scores (B, n_heads, 3, 3) ────────────────────────
        scores = torch.matmul(Q, K.transpose(-2, -1)) * self.scale

        # Entmax15: sparse attention — some keys get exactly 0 weight
        if self.alpha == 1.0:
            attn = F.softmax(scores, dim=-1)
        else:
            attn = entmax15(scores, dim=-1)  # (B, n_heads, 3, 3)
        attn = self.dropout(attn)

        # ── Weighted sum → (B, 3, H) ────────────────────────────────────
        context = torch.matmul(attn, V)                          # (B, n_heads, 3, head_dim)
        context = context.transpose(1, 2).contiguous().view(B, 3, self.H)

        # ── Apply global modality weights ────────────────────────────────
        w = self.modality_weights  # (3,)  [gene_w, cpg_w, mirna_w]
        context = context * w.view(1, 3, 1)  # scale each modality's output

        # ── Use gene token as output anchor ──────────────────────────────
        # Gene token at index 0 has attended over cpg and mirna info
        fused = context[:, 0, :]             # (B, H) — gene token output

        # ── Output projection + residual ─────────────────────────────────
        fused = self.W_out(fused)
        fused = self.norm(fused + z_gene)    # residual: gene is the anchor

        if return_attn:
            # attn averaged over heads: (B, 3, 3) — gene row = gene's attention over all 3
            attn_avg = attn.mean(dim=1)  # (B, 3, 3)
            return fused, {
                "attn_matrix":      attn_avg,           # (B, 3, 3)
                "gene_over_cpg":    attn_avg[:, 0, 1],  # (B,) gene→cpg
                "gene_over_mirna":  attn_avg[:, 0, 2],  # (B,) gene→mirna
                "modality_weights": w,                   # (3,) global
            }
        return fused, None


# ─────────────────────────────────────────────────────────────────────────────
#  Main model
# ─────────────────────────────────────────────────────────────────────────────

class GIACModel(nn.Module):

    def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
        super().__init__()

        H           = cfg_model["hidden_dim"]
        num_classes = cfg_model["num_classes"]

        # Module 1: Heterogeneous GAT
        self.gat = MultiOmicGATModule(
            dims       = dims,
            hidden_dim = H,
            n_heads    = cfg_model["gat_heads"],
            n_layers   = cfg_model["gat_layers"],
            dropout    = cfg_model.get("gat_dropout", 0.3),
        )

        # Module 2: 3-token Self-Attention Fusion
        self.cross_attn = ModalityFusionAttention(
            hidden_dim = H,
            n_heads    = cfg_model.get("ca_heads", cfg_model.get("cross_attn_heads", 4)),
            dropout    = cfg_model.get("ca_dropout", cfg_model.get("cross_attn_dropout", 0.2)),
            alpha      = cfg_model.get("sparsemax_alpha", 1.5),
        )

        # Module 3: Classifier
        self.classifier = SubtypeClassifier(
            hidden_dim  = H,
            final_dim   = cfg_model["final_dim"],
            num_classes = num_classes,
            dropout     = cfg_model.get("classifier_dropout", 0.5),
        )

        # Loss
        self.loss_name = cfg_train.get("loss_name", "focal").lower()
        self.register_buffer("class_weights", torch.ones(num_classes, dtype=torch.float32))
        self.focal_loss = FocalLoss(
            gamma           = cfg_train["focal_gamma"],
            alpha           = cfg_train["focal_alpha"],
            num_classes     = num_classes,
            label_smoothing = cfg_train.get("label_smoothing", 0.0),
        )
        self.lambda_frob = cfg_train.get("lambda_frobenius", 0.01)

    def set_class_weights(self, w: torch.Tensor):
        norm = w / w.mean().clamp_min(1e-8)
        self.class_weights.copy_(norm.to(self.class_weights.device))
        self.focal_loss.set_alpha(self.class_weights)

    def forward(self, batch: dict, graph: HeteroData, return_interpretability: bool = False):
        # Step 1: GAT encoding
        z_gene, z_cpg, z_mirna = self.gat(batch, graph)

        # Step 2: Fusion attention
        fused, attn_info = self.cross_attn(
            z_gene, z_cpg, z_mirna, return_attn=True
        )

        # Step 3: Classify
        logits = self.classifier(fused)

        if return_interpretability:
            return logits, None, attn_info
        return logits, attn_info

    def compute_loss(self, logits, labels, attn_info=None):
        if self.loss_name == "cross_entropy":
            loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
        else:
            loss_cls = self.focal_loss(logits, labels)

        loss_frob = frobenius_regularization_loss(
            self.cross_attn, self.lambda_frob, param_prefix="W_"
        )
        return loss_cls + loss_frob