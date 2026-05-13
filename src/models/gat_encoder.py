import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from torch_geometric.nn import GATv2Conv, HeteroConv


def _make_hetero_conv(hidden_dim: int, n_heads: int, dropout: float) -> HeteroConv:
    head_dim = hidden_dim // n_heads

    def bip():
        # edge_dim=1 → GATv2 sẽ nhận edge_attr (-log10(p) cho emQTL,
        # uniform 1.0 cho relations khác) và đưa vào attention.
        return GATv2Conv((hidden_dim, hidden_dim), head_dim,
                         heads=n_heads, add_self_loops=False,
                         dropout=dropout, edge_dim=1)

    def hom():
        return GATv2Conv(hidden_dim, head_dim,
                         heads=n_heads, add_self_loops=False,
                         dropout=dropout, edge_dim=1)

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
        ("cpg",   "sameisland",   "cpg"):   hom(),
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

        # Rank-based positional encodings for top-K CpG and miRNA sequences.
        # Each of the K slots (rank-0 = most active … rank K-1 = least active)
        # receives a unique learned offset so that cross-attention can distinguish
        # tokens even when their GAT embeddings are nearly identical.
        self.cpg_pos_emb   = nn.Embedding(topk_seq, hidden_dim)
        self.mirna_pos_emb = nn.Embedding(topk_seq, hidden_dim)
        nn.init.normal_(self.cpg_pos_emb.weight,   std=0.02)
        nn.init.normal_(self.mirna_pos_emb.weight, std=0.02)

        # Summary vector norm for gene query only
        self.gene_norm = nn.LayerNorm(hidden_dim)

    def forward(self, batch: dict, graph: HeteroData):
        x_dict = {k: self.node_emb[k] for k in ["gene", "cpg", "mirna"]}

        present = {k: v for k, v in graph.edge_index_dict.items() if v.shape[1] > 0}
        # Edge attributes (-log10(p) for emQTL, score/1000 for PPI, uniform 1.0 elsewhere).
        # HeteroConv splits this dict by edge_type and passes `edge_attr=<tensor>` to each conv.
        # GATv2Conv was built with edge_dim=1, so every present relation MUST have edge_attr;
        # fall back to uniform 1.0 if missing to keep training robust.
        edge_attr_dict = {}
        for k, ei in present.items():
            attr = getattr(graph[k], "edge_attr", None)
            if attr is None:
                attr = torch.ones((ei.shape[1], 1), dtype=torch.float32, device=ei.device)
            edge_attr_dict[k] = attr
        for i in range(self.n_layers):
            out = self.convs[i](x_dict, present, edge_attr=edge_attr_dict)
            x_dict = {
                t: self.layer_norms[i][t](h + F.elu(self.dropout(out.get(t, h))))
                for t, h in x_dict.items()
            }

        # ── Gene: single summary vector (B, H) used as Query ──────────
        z_gene = self.gene_norm(
            torch.matmul(batch["gene"], x_dict["gene"])
            / math.sqrt(batch["gene"].shape[1])
        )

        # ── CpG: top-K sequence (B, K, H) used as Key/Value ───────────
        z_cpg_seq   = self._topk_seq(batch["meth"],  x_dict["cpg"],  self.topk_seq, self.cpg_pos_emb)
        z_mirna_seq = self._topk_seq(batch["mirna"], x_dict["mirna"], self.topk_seq, self.mirna_pos_emb)

        return z_gene, z_cpg_seq, z_mirna_seq

    def _topk_seq(self, X: torch.Tensor, E: torch.Tensor, K: int,
                  pos_emb: nn.Embedding = None) -> torch.Tensor:
        B, n_feat = X.shape
        K = min(K, n_feat)

        topk_idx = X.abs().topk(K, dim=1).indices       # (B, K)
        E_topk   = E[topk_idx]                          # (B, K, H)

        # Modulate each node embedding by patient's feature value (signed, standardised)
        weights = X.gather(1, topk_idx).unsqueeze(-1)   # (B, K, 1)
        z_seq   = E_topk + E_topk * weights             # (B, K, H)

        if pos_emb is not None:
            rank_ids = torch.arange(K, device=X.device).unsqueeze(0).expand(B, -1)
            z_seq    = z_seq + pos_emb(rank_ids)

        return z_seq
