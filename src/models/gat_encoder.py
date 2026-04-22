import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from torch_geometric.nn import GATv2Conv, HeteroConv


def _make_hetero_conv(hidden_dim: int, n_heads: int, dropout: float) -> HeteroConv:
    head_dim = hidden_dim // n_heads

    def bip():
        return GATv2Conv((hidden_dim, hidden_dim), head_dim,
                         heads=n_heads, add_self_loops=False, dropout=dropout)

    def hom():
        return GATv2Conv(hidden_dim, head_dim,
                         heads=n_heads, add_self_loops=False, dropout=dropout)

    return HeteroConv({
        ("cpg",   "regulates",    "gene"):  bip(),
        ("gene",  "regulated_by", "cpg"):   bip(),
        ("mirna", "targets",      "gene"):  bip(),
        ("gene",  "targeted_by",  "mirna"): bip(),
        ("cpg",   "coregulates",  "mirna"): bip(),
        ("mirna", "coregulates",  "cpg"):   bip(),
        ("gene",  "ppi",          "gene"):  hom(),
        ("gene",  "copathway",    "gene"):  hom(),
        ("mirna", "samefamily",   "mirna"): hom(),
        ("gene",  "self_loop",    "gene"):  hom(),
        ("cpg",   "self_loop",    "cpg"):   hom(),
        ("mirna", "self_loop",    "mirna"): hom(),
    }, aggr="sum")


class MultiOmicGATModule(nn.Module):
    def __init__(self, dims: dict, hidden_dim: int, n_heads: int,
                 n_layers: int, dropout: float, topk_seq: int = 32):
        super().__init__()
        assert hidden_dim % n_heads == 0
        self.n_layers  = n_layers
        self.hidden_dim = hidden_dim
        self.topk_seq  = topk_seq  # K tokens per modality for cross-attention

        self.node_emb = nn.ParameterDict({
            "gene":  nn.Parameter(torch.empty(dims["gene"],  hidden_dim)),
            "cpg":   nn.Parameter(torch.empty(dims["meth"],  hidden_dim)),
            "mirna": nn.Parameter(torch.empty(dims["mirna"], hidden_dim)),
        })
        for p in self.node_emb.values():
            nn.init.xavier_uniform_(p)

        self.convs = nn.ModuleList(
            [_make_hetero_conv(hidden_dim, n_heads, dropout) for _ in range(n_layers)]
        )
        self.layer_norms = nn.ModuleList([
            nn.ModuleDict({
                "gene":  nn.LayerNorm(hidden_dim),
                "cpg":   nn.LayerNorm(hidden_dim),
                "mirna": nn.LayerNorm(hidden_dim),
            }) for _ in range(n_layers)
        ])
        self.dropout = nn.Dropout(dropout)

        # For the single summary vector (used as gene query)
        self.output_norm = nn.ModuleDict({
            "gene":  nn.LayerNorm(hidden_dim),
            "cpg":   nn.LayerNorm(hidden_dim),
            "mirna": nn.LayerNorm(hidden_dim),
        })

    def forward(self, batch: dict, graph: HeteroData):
        x_dict = {k: self.node_emb[k] for k in ["gene", "cpg", "mirna"]}

        present = {k: v for k, v in graph.edge_index_dict.items() if v.shape[1] > 0}
        for i in range(self.n_layers):
            out = self.convs[i](x_dict, present)
            x_dict = {
                t: self.layer_norms[i][t](h + F.elu(self.dropout(out.get(t, h))))
                for t, h in x_dict.items()
            }

        # ── Gene: single summary vector (B, H) used as Query ──────────
        z_gene = self.output_norm["gene"](
            torch.matmul(batch["gene"], x_dict["gene"])
            / math.sqrt(batch["gene"].shape[1])
        )

        # ── CpG: top-K sequence (B, K, H) used as Key/Value ───────────
        # Select top-K CpG nodes per patient by their feature value (abs)
        # → captures the most active methylation sites per patient
        z_cpg_seq   = self._topk_seq(batch["meth"],  x_dict["cpg"],  self.topk_seq, "cpg")
        z_mirna_seq = self._topk_seq(batch["mirna"], x_dict["mirna"], self.topk_seq, "mirna")

        return z_gene, z_cpg_seq, z_mirna_seq

    def _topk_seq(self, X: torch.Tensor, E: torch.Tensor,
                  K: int, modality: str) -> torch.Tensor:
        """
        X : (B, F)   patient feature values (standardised)
        E : (F, H)   node embeddings after GAT
        Returns (B, K, H) — top-K node embeddings weighted by patient values
        """
        B, F = X.shape
        K = min(K, F)

        # Use absolute value to capture both hyper- and hypo-methylation
        scores = X.abs()                              # (B, F)
        topk_idx = scores.topk(K, dim=1).indices      # (B, K)

        # Gather embeddings for selected nodes
        E_topk = E[topk_idx]                          # (B, K, H)

        # Weight each embedding by the patient's actual feature value
        weights = X.gather(1, topk_idx).unsqueeze(-1) # (B, K, 1)
        z_seq = self.output_norm[modality](
            (E_topk * weights).view(B * K, -1)
        ).view(B, K, -1)                              # (B, K, H)

        return z_seq