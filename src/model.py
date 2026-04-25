import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from entmax import entmax15

from src.models.gat_encoder import MultiOmicGATModule
from src.models.classifier import FocalLoss, SubtypeClassifier, frobenius_regularization_loss


class ModalityCrossAttention(nn.Module):
    """
    Asymmetric cross-attention: gene (B,H) as Query, CpG/miRNA (B,K,H) as Key/Value.

    Gene attends over K most-active CpG nodes and K most-active miRNA nodes.
    Entmax15 produces sparse weights → interpretable (which nodes matter per patient).
    Output: gene enriched with epigenetic + post-transcriptional context.
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

        # Combine both modality contexts → H
        self.W_out   = nn.Linear(hidden_dim * 2, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.norm    = nn.LayerNorm(hidden_dim)

        # Global modality importance (2: cpg, mirna)
        self.modality_logits = nn.Parameter(torch.zeros(2))

        # Learnable log-temperature for attention sharpening.
        # Initialized to 0.0 → temp = 1.0 (standard scale).
        # Positional encoding already differentiates the K tokens; starting
        # at temp=1.0 lets the model learn the right sharpness from data
        # rather than forcing aggressive sparsity from epoch 1.
        self.log_temp = nn.Parameter(torch.tensor(0.0))

    @property
    def modality_weights(self):
        return F.softmax(self.modality_logits, dim=0)

    def _attend(self, q, W_k, W_v, kv_seq):
        """
        q      : (B, H)
        kv_seq : (B, K, H)
        Returns context (B, H) and attn_weights (B, K) averaged over heads.
        """
        B, K, _ = kv_seq.shape

        # Q: (B, n_heads, 1, head_dim)
        Q = self.W_q(q).view(B, self.n_heads, 1, self.head_dim)

        # K, V: (B, n_heads, K, head_dim)
        K_ = W_k(kv_seq).view(B, K, self.n_heads, self.head_dim).transpose(1, 2)
        V_ = W_v(kv_seq).view(B, K, self.n_heads, self.head_dim).transpose(1, 2)

        # Attention scores (B, n_heads, 1, K) → sparse weights over K nodes
        # Multiply by exp(log_temp) to sharpen/flatten the distribution;
        # initialized to ~2.0 so entmax15 receives amplified score differences.
        scores = torch.matmul(Q, K_.transpose(-2, -1)) * self.scale * self.log_temp.exp()
        if self.alpha == 1.0:
            attn = F.softmax(scores, dim=-1)
        else:
            attn = entmax15(scores, dim=-1)
        # NOTE: dropout applied to context output, not to attention weights.
        # Dropping attention weights after entmax15 destroys sparsity patterns and
        # creates train/eval mismatch (model sees zeroed weights in train but full
        # sparse distribution at eval time).
        ctx = torch.matmul(attn, V_)                      # (B, n_heads, 1, head_dim)
        ctx = self.dropout(ctx)                           # regularize context, not weights
        ctx = ctx.squeeze(2).transpose(1, 2).contiguous().view(B, self.H)

        # Average attention over heads for interpretability: (B, K)
        attn_w = attn.mean(dim=1).squeeze(1)

        return ctx, attn_w

    def forward(self, z_gene, z_cpg_seq, z_mirna_seq, return_attn=False):
        ctx_cpg,   attn_cpg   = self._attend(z_gene, self.W_k_cpg,   self.W_v_cpg,   z_cpg_seq)
        ctx_mirna, attn_mirna = self._attend(z_gene, self.W_k_mirna, self.W_v_mirna, z_mirna_seq)

        w = self.modality_weights                         # (2,)
        combined = torch.cat([w[0] * ctx_cpg, w[1] * ctx_mirna], dim=-1)  # (B, 2H)
        fused = self.norm(self.W_out(combined) + z_gene)  # residual

        if return_attn:
            return fused, {
                "cpg_attn":        attn_cpg,              # (B, K)
                "mirna_attn":      attn_mirna,            # (B, K)
                "modality_weights": w,                    # (2,)
            }
        return fused, None


class GIACModel(nn.Module):

    def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
        super().__init__()
        H           = cfg_model["hidden_dim"]
        num_classes = cfg_model["num_classes"]
        topk        = cfg_model.get("topk_seq", 32)

        self.gat = MultiOmicGATModule(
            dims       = dims,
            hidden_dim = H,
            n_heads    = cfg_model["gat_heads"],
            n_layers   = cfg_model["gat_layers"],
            dropout    = cfg_model.get("gat_dropout", 0.3),
            topk_seq   = topk,
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
        self.lambda_frob = cfg_train.get("lambda_frobenius", 0.01)

    def set_class_weights(self, w):
        norm = w / w.mean().clamp_min(1e-8)
        self.class_weights.copy_(norm.to(self.class_weights.device))
        self.focal_loss.set_alpha(self.class_weights)

    def forward(self, batch, graph, return_interpretability=False):
        z_gene, z_cpg_seq, z_mirna_seq = self.gat(batch, graph)
        fused, attn_info = self.cross_attn(
            z_gene, z_cpg_seq, z_mirna_seq, return_attn=True
        )
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
