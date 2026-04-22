"""
gat_encoder.py
--------------
Heterogeneous GAT encoder for the GIAC multi-omics graph.

Architecture
------------
1. Static learnable node embeddings (gene/cpg/mirna), shape (N_type, H).
2. L layers of HeteroConv(GATv2Conv) — one attention kernel per edge type.
   All 7 edge types are covered:
     inter-omic : cpg->gene, gene->cpg, mirna->gene, gene->mirna,
                  cpg<->mirna (coregulation)
     intra-omic : gene<->gene (ppi), gene<->gene (copathway),
                  mirna<->mirna (samefamily)
     self-loops : gene, cpg, mirna
3. Patient projection:
   z_modality = LayerNorm( X_patient @ E_modality / sqrt(F) )
   where X_patient is the (B, F) feature matrix after ANOVA selection and
   E_modality is the (F, H) node-embedding matrix after L GAT layers.
   This is a differentiable linear read-out: each patient gets a weighted
   sum of node embeddings, weighted by their omics values.
"""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from torch_geometric.nn import GATv2Conv, HeteroConv


# ─────────────────────────────────────────────────────────────────────────────
#  Helper: build one HeteroConv layer covering all present edge types
# ─────────────────────────────────────────────────────────────────────────────

def _make_hetero_conv(hidden_dim: int, n_heads: int, dropout: float) -> HeteroConv:
    head_dim = hidden_dim // n_heads

    def bipartite(in_src=hidden_dim, in_dst=hidden_dim):
        return GATv2Conv(
            (in_src, in_dst), head_dim,
            heads=n_heads, add_self_loops=False, dropout=dropout,
        )

    def homogeneous():
        return GATv2Conv(
            hidden_dim, head_dim,
            heads=n_heads, add_self_loops=False, dropout=dropout,
        )

    conv_dict = {
        # ── inter-omic ──────────────────────────────────────────────────────
        ("cpg",   "regulates",    "gene"):  bipartite(),
        ("gene",  "regulated_by", "cpg"):   bipartite(),
        ("mirna", "targets",      "gene"):  bipartite(),
        ("gene",  "targeted_by",  "mirna"): bipartite(),
        ("cpg",   "coregulates",  "mirna"): bipartite(),
        ("mirna", "coregulates",  "cpg"):   bipartite(),
        # ── intra-omic ──────────────────────────────────────────────────────
        ("gene",  "ppi",          "gene"):  homogeneous(),
        ("gene",  "copathway",    "gene"):  homogeneous(),
        ("mirna", "samefamily",   "mirna"): homogeneous(),
        # ── self-loops ──────────────────────────────────────────────────────
        ("gene",  "self_loop",    "gene"):  homogeneous(),
        ("cpg",   "self_loop",    "cpg"):   homogeneous(),
        ("mirna", "self_loop",    "mirna"): homogeneous(),
    }
    return HeteroConv(conv_dict, aggr="sum")


# ─────────────────────────────────────────────────────────────────────────────
#  Main module
# ─────────────────────────────────────────────────────────────────────────────

class MultiOmicGATModule(nn.Module):
    """
    Multi-layer Heterogeneous GAT encoder.

    Parameters
    ----------
    dims      : {"gene": F_g, "meth": F_m, "mirna": F_r}
    hidden_dim: embedding dimension H (same for all node types)
    n_heads   : GAT attention heads (hidden_dim must be divisible)
    n_layers  : number of message-passing layers (1 or 2 recommended)
    dropout   : dropout on attention coefficients and activations
    """

    def __init__(
        self,
        dims:       dict,
        hidden_dim: int,
        n_heads:    int,
        n_layers:   int,
        dropout:    float,
    ):
        super().__init__()
        assert hidden_dim % n_heads == 0, (
            f"hidden_dim={hidden_dim} must be divisible by n_heads={n_heads}"
        )
        self.n_layers   = n_layers
        self.hidden_dim = hidden_dim

        # ── Static learnable node embeddings ──────────────────────────────
        # Shape (N_nodes_of_type, H) — shared across all patients in a fold.
        # These are updated via back-prop through the patient projection.
        self.node_emb = nn.ParameterDict({
            "gene":  nn.Parameter(torch.empty(dims["gene"],  hidden_dim)),
            "cpg":   nn.Parameter(torch.empty(dims["meth"],  hidden_dim)),
            "mirna": nn.Parameter(torch.empty(dims["mirna"], hidden_dim)),
        })
        for p in self.node_emb.values():
            nn.init.xavier_uniform_(p)

        # ── GAT layers ────────────────────────────────────────────────────
        self.convs = nn.ModuleList(
            [_make_hetero_conv(hidden_dim, n_heads, dropout)
             for _ in range(n_layers)]
        )

        # Per-layer, per-node-type LayerNorm (for residual + norm)
        self.layer_norms = nn.ModuleList([
            nn.ModuleDict({
                "gene":  nn.LayerNorm(hidden_dim),
                "cpg":   nn.LayerNorm(hidden_dim),
                "mirna": nn.LayerNorm(hidden_dim),
            })
            for _ in range(n_layers)
        ])

        self.dropout = nn.Dropout(dropout)

        # Final output norm after patient projection
        self.output_norm = nn.ModuleDict({
            "gene":  nn.LayerNorm(hidden_dim),
            "cpg":   nn.LayerNorm(hidden_dim),
            "mirna": nn.LayerNorm(hidden_dim),
        })

    def forward(
        self,
        batch: dict,
        graph: HeteroData,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Parameters
        ----------
        batch : {"gene": (B, F_g), "meth": (B, F_m), "mirna": (B, F_r)}
        graph : HeteroData with edge_index_dict

        Returns
        -------
        z_gene  : (B, H)
        z_cpg   : (B, H)
        z_mirna : (B, H)
        """
        # ── Step 1: graph message passing on node embeddings ──────────────
        x_dict = {
            "gene":  self.node_emb["gene"],    # (N_g, H)
            "cpg":   self.node_emb["cpg"],     # (N_c, H)
            "mirna": self.node_emb["mirna"],   # (N_r, H)
        }

        # Only pass edge types that actually exist in the graph
        present_edge_dict = {
            k: v for k, v in graph.edge_index_dict.items()
            if v.shape[1] > 0
        }

        for layer_idx in range(self.n_layers):
            out_dict = self.convs[layer_idx](x_dict, present_edge_dict)
            next_dict = {}
            for node_type, h_prev in x_dict.items():
                h_new = out_dict.get(node_type, h_prev)
                h_new = F.elu(h_new)
                h_new = self.dropout(h_new)
                # Residual + LayerNorm
                next_dict[node_type] = self.layer_norms[layer_idx][node_type](
                    h_prev + h_new
                )
            x_dict = next_dict

        # ── Step 2: patient projection ────────────────────────────────────
        # z = LayerNorm( X @ E / sqrt(F) )
        # X: (B, F)  -- patient feature values (standardised)
        # E: (F, H)  -- learned node embeddings
        # Result: (B, H) -- patient-specific graph-aware representation
        z_gene  = self.output_norm["gene"](
            torch.matmul(batch["gene"],  x_dict["gene"])
            / math.sqrt(batch["gene"].shape[1])
        )
        z_cpg   = self.output_norm["cpg"](
            torch.matmul(batch["meth"],  x_dict["cpg"])
            / math.sqrt(batch["meth"].shape[1])
        )
        z_mirna = self.output_norm["mirna"](
            torch.matmul(batch["mirna"], x_dict["mirna"])
            / math.sqrt(batch["mirna"].shape[1])
        )

        return z_gene, z_cpg, z_mirna