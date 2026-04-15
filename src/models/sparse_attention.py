"""
sparse_attention.py
-------------------
Module 2 — Patient-Specific Sparse Cross-Attention

Thay thế softmax bằng Sparsemax trong cross-attention:
  - Softmax  : tất cả features đều có trọng số > 0 (dù rất nhỏ)
  - Sparsemax: nhiều features nhận đúng bằng 0 → sparse, diễn giải được

Kết quả: mỗi bệnh nhân có "bản đồ feature" riêng — chỉ những
gene/CpG/miRNA thực sự quan trọng mới có trọng số khác 0.

Reference:
  - Martins & Astudillo, "From Softmax to Sparsemax", ICML 2016
  - Peters et al., "Sparse Sequence-to-Sequence Models", ACL 2019
  - Library: pip install entmax
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from entmax import sparsemax, entmax15   # pip install entmax


class SparseMultiheadCrossAttention(nn.Module):
    """
    Multi-head Cross-Attention với Sparsemax thay softmax.
    
    Input: 3 vectors từ GAT encoder [z_gene, z_cpg, z_mirna], mỗi cái (B, D)
    Output: fused vector (B, D) + per-sample sparse attention weights
    
    Cơ chế:
      1. Stack 3 modalities: C = [z_gene, z_cpg, z_mirna] → (B, 3, D)
      2. Tính Q, K, V projections
      3. Attention scores với Sparsemax (không phải softmax)
      4. Modality-weighted sum (learnable weights w1, w2, w3 như MoXGATE)
      5. Output: fused representation (B, D)
    """

    def __init__(
        self,
        hidden_dim: int,       # D
        n_heads: int,          # số attention heads (32 như MoXGATE)
        dropout: float,
        sparsemax_alpha: float = 1.5,  # 1.0=softmax, 1.5=sparsemax, 2.0=harder sparse
    ):
        super().__init__()
        assert hidden_dim % n_heads == 0, \
            f"hidden_dim={hidden_dim} phải chia hết cho n_heads={n_heads}"

        self.hidden_dim = hidden_dim
        self.n_heads    = n_heads
        self.head_dim   = hidden_dim // n_heads
        self.alpha      = sparsemax_alpha
        self.scale      = self.head_dim ** -0.5

        # Projection matrices cho Q, K, V
        self.W_q = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_k = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_v = nn.Linear(hidden_dim, hidden_dim, bias=False)

        # Output projection
        self.out_proj = nn.Linear(hidden_dim, hidden_dim)
        self.dropout  = nn.Dropout(dropout)
        self.norm     = nn.LayerNorm(hidden_dim)

        # Learnable modality weights (như MoXGATE gốc)
        # Khởi tạo đều = 1/3, học trong quá trình training
        self.modality_logits = nn.Parameter(torch.zeros(3))

    @property
    def modality_weights(self) -> torch.Tensor:
        """Trả về w = softmax(logits) để đảm bảo sum=1."""
        return F.softmax(self.modality_logits, dim=0)  # (3,)

    def forward(
        self,
        z_gene:  torch.Tensor,   # (B, D)
        z_cpg:   torch.Tensor,   # (B, D)
        z_mirna: torch.Tensor,   # (B, D)
        return_sparse_weights: bool = False,
    ):
        """
        return_sparse_weights=True: trả về attention weights per sample
            → dùng trong interpretability để biết modality nào quan trọng
        """
        B, D = z_gene.shape

        # ── 1. Stack modalities ──────────────────────────────────────
        # C: (B, 3, D) — 3 modalities như 3 "tokens"
        C = torch.stack([z_gene, z_cpg, z_mirna], dim=1)  # (B, 3, D)

        # ── 2. Multi-head Q, K, V ────────────────────────────────────
        # (B, 3, D) → (B, 3, n_heads, head_dim) → (B, n_heads, 3, head_dim)
        def project_and_reshape(x, W):
            return W(x).view(B, 3, self.n_heads, self.head_dim).transpose(1, 2)

        Q = project_and_reshape(C, self.W_q)  # (B, H, 3, d_h)
        K = project_and_reshape(C, self.W_k)  # (B, H, 3, d_h)
        V = project_and_reshape(C, self.W_v)  # (B, H, 3, d_h)

        # ── 3. Attention scores ──────────────────────────────────────
        # scores: (B, H, 3, 3) — attention của mỗi modality với mỗi modality khác
        scores = torch.matmul(Q, K.transpose(-2, -1)) * self.scale  # (B, H, 3, 3)

        # ── 4. Sparsemax thay softmax ────────────────────────────────
        # sparsemax hoạt động trên dim=-1
        # Kết quả: nhiều entries = 0 (không phải gần 0 như softmax)
        if self.alpha == 1.0:
            # softmax thông thường (baseline comparison)
            attn_weights = F.softmax(scores, dim=-1)
        elif self.alpha == 1.5:
            # entmax1.5 = sparsemax
            attn_weights = entmax15(scores, dim=-1)
        else:
            # sparsemax cứng hơn
            attn_weights = sparsemax(scores, dim=-1)

        attn_weights = self.dropout(attn_weights)

        # ── 5. Weighted sum ──────────────────────────────────────────
        context = torch.matmul(attn_weights, V)  # (B, H, 3, d_h)
        # Reshape: (B, H, 3, d_h) → (B, 3, H*d_h) = (B, 3, D)
        context = context.transpose(1, 2).contiguous().view(B, 3, D)

        # ── 6. Modality-weighted fusion ──────────────────────────────
        # w: (3,) → broadcast với context (B, 3, D)
        w = self.modality_weights  # (3,)
        # Weighted sum qua 3 modalities
        fused = (context * w.view(1, 3, 1)).sum(dim=1)  # (B, D)

        # ── 7. Output projection + residual ──────────────────────────
        fused = self.out_proj(fused)
        # Residual: cộng với mean của 3 inputs (skip connection)
        residual = (z_gene + z_cpg + z_mirna) / 3.0
        fused = self.norm(fused + residual)

        if return_sparse_weights:
            # Trả về attention weights averaged qua heads: (B, 3, 3)
            attn_avg = attn_weights.mean(dim=1)  # (B, 3, 3)
            return fused, attn_avg, w

        return fused  # (B, D)


# ─────────────────────────────────────────────
#  Patient-level sparse feature importance
# ─────────────────────────────────────────────
class PatientSparseAttention(nn.Module):
    """
    Tầng bổ sung: tính sparse attention weights ở mức FEATURE (không phải modality).
    
    Mục đích: xác định feature nào (gene/CpG/miRNA cụ thể) quan trọng
    nhất cho TỪNG bệnh nhân.
    
    Input: raw feature vectors trước GAT encoding
    Output: sparse weight vector per patient per modality
    
    Đây là nguồn dữ liệu cho top-K gene per patient.
    """

    def __init__(self, dims: dict, hidden_dim: int, alpha: float = 1.5):
        """
        dims: {'gene': F_g, 'meth': F_m, 'mirna': F_mi}
        """
        super().__init__()
        self.alpha = alpha

        # Scoring function: feature → scalar score
        # Dùng 2-layer MLP để tính importance score cho mỗi feature
        self.gene_scorer  = self._make_scorer(dims["gene"],  hidden_dim)
        self.cpg_scorer   = self._make_scorer(dims["meth"],  hidden_dim)
        self.mirna_scorer = self._make_scorer(dims["mirna"], hidden_dim)

    def _make_scorer(self, in_dim: int, hidden: int) -> nn.Module:
        """
        MLP: (in_dim,) → (in_dim,) scalar scores per feature
        """
        return nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, in_dim),  # output: 1 score per feature
        )

    def forward(self, batch: dict) -> dict:
        """
        Trả về dict sparse_weights với keys 'gene', 'meth', 'mirna'
        Mỗi value: (B, F) với nhiều entries = 0
        """
        sparse_weights = {}

        for name, scorer, key in [
            ("gene",  self.gene_scorer,  "gene"),
            ("meth",  self.cpg_scorer,   "meth"),
            ("mirna", self.mirna_scorer, "mirna"),
        ]:
            x = batch[key]          # (B, F)
            scores = scorer(x)      # (B, F) — unnormalized importance scores

            # Áp dụng sparsemax trên dim=-1 (qua features)
            if self.alpha == 1.5:
                w = entmax15(scores, dim=-1)   # (B, F), nhiều entries = 0
            else:
                w = sparsemax(scores, dim=-1)  # (B, F)

            sparse_weights[name] = w

        return sparse_weights


def get_top_k_features(
    sparse_weights: dict,
    feature_names: dict,
    k: int = 50,
) -> dict:
    """
    Trích xuất top-K features có sparse weight cao nhất cho từng bệnh nhân.
    
    Parameters
    ----------
    sparse_weights : output từ PatientSparseAttention.forward()
    feature_names  : dict {'gene': [...], 'meth': [...], 'mirna': [...]}
    k              : số features lấy per modality per patient
    
    Returns
    -------
    dict: {
        'gene':  list of list (mỗi patient một list tên gene),
        'meth':  list of list,
        'mirna': list of list,
    }
    """
    results = {}
    for mod in ["gene", "meth", "mirna"]:
        w = sparse_weights[mod]        # (B, F)
        names = feature_names[mod]
        patient_features = []

        for i in range(w.shape[0]):
            # Lấy top-K indices có weight cao nhất và khác 0
            w_i = w[i].detach().cpu()
            nonzero_mask = w_i > 0
            if nonzero_mask.sum() == 0:
                patient_features.append([])
                continue

            # Sắp xếp giảm dần, lấy top-K
            top_k_actual = min(k, nonzero_mask.sum().item())
            top_idx = torch.topk(w_i, k=top_k_actual).indices.tolist()
            top_features = [(names[j], w_i[j].item()) for j in top_idx if w_i[j] > 0]
            patient_features.append(top_features)

        results[mod] = patient_features

    return results
