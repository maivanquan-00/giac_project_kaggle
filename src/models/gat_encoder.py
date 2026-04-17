"""
gat_encoder.py
--------------
Graph encoder for the heterogeneous GIAC graph.

The graph encoder learns static node embeddings and propagates information across:
  - cpg -> gene and gene -> cpg
  - mirna -> gene and gene -> mirna
  - self loops for each modality
  - gene-gene interactions

Patient-specific embeddings are then computed by projecting each patient's omics
profile onto the graph-aware node embeddings.
"""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from torch_geometric.nn import GATv2Conv, HeteroConv


class MultiOmicGATModule(nn.Module):
    def __init__(self, dims: dict, hidden_dim: int, n_heads: int, n_layers: int, dropout: float):
        super().__init__()
        self.n_layers = n_layers
        self.hidden_dim = hidden_dim

        self.node_emb = nn.ParameterDict(
            {
                "gene": nn.Parameter(torch.empty(dims["gene"], hidden_dim)),
                "cpg": nn.Parameter(torch.empty(dims["meth"], hidden_dim)),
                "mirna": nn.Parameter(torch.empty(dims["mirna"], hidden_dim)),
            }
        )
        for emb in self.node_emb.values():
            nn.init.xavier_uniform_(emb)

        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        for _ in range(n_layers):
            self.convs.append(
                HeteroConv(
                    {
                        ("cpg", "regulates", "gene"): GATv2Conv(
                            (hidden_dim, hidden_dim),
                            hidden_dim // n_heads,
                            heads=n_heads,
                            add_self_loops=False,
                            dropout=dropout,
                        ),
                        ("gene", "regulated_by", "cpg"): GATv2Conv(
                            (hidden_dim, hidden_dim),
                            hidden_dim // n_heads,
                            heads=n_heads,
                            add_self_loops=False,
                            dropout=dropout,
                        ),
                        ("mirna", "targets", "gene"): GATv2Conv(
                            (hidden_dim, hidden_dim),
                            hidden_dim // n_heads,
                            heads=n_heads,
                            add_self_loops=False,
                            dropout=dropout,
                        ),
                        ("gene", "targeted_by", "mirna"): GATv2Conv(
                            (hidden_dim, hidden_dim),
                            hidden_dim // n_heads,
                            heads=n_heads,
                            add_self_loops=False,
                            dropout=dropout,
                        ),
                        ("gene", "interacts", "gene"): GATv2Conv(
                            hidden_dim,
                            hidden_dim // n_heads,
                            heads=n_heads,
                            add_self_loops=False,
                            dropout=dropout,
                        ),
                        ("gene", "self_loop", "gene"): GATv2Conv(
                            hidden_dim,
                            hidden_dim // n_heads,
                            heads=n_heads,
                            add_self_loops=False,
                            dropout=dropout,
                        ),
                        ("cpg", "self_loop", "cpg"): GATv2Conv(
                            hidden_dim,
                            hidden_dim // n_heads,
                            heads=n_heads,
                            add_self_loops=False,
                            dropout=dropout,
                        ),
                        ("mirna", "self_loop", "mirna"): GATv2Conv(
                            hidden_dim,
                            hidden_dim // n_heads,
                            heads=n_heads,
                            add_self_loops=False,
                            dropout=dropout,
                        ),
                    },
                    aggr="sum",
                )
            )
            self.norms.append(
                nn.ModuleDict(
                    {
                        "gene": nn.LayerNorm(hidden_dim),
                        "cpg": nn.LayerNorm(hidden_dim),
                        "mirna": nn.LayerNorm(hidden_dim),
                    }
                )
            )

        self.dropout = nn.Dropout(dropout)
        self.output_norm = nn.ModuleDict(
            {
                "gene": nn.LayerNorm(hidden_dim),
                "cpg": nn.LayerNorm(hidden_dim),
                "mirna": nn.LayerNorm(hidden_dim),
            }
        )

    def forward(self, batch: dict, graph: HeteroData, return_attention: bool = False):
        x_dict = {
            "gene": self.node_emb["gene"],
            "cpg": self.node_emb["cpg"],
            "mirna": self.node_emb["mirna"],
        }

        for layer_idx in range(self.n_layers):
            out_dict = self.convs[layer_idx](x_dict, graph.edge_index_dict)
            next_dict = {}
            for node_type, h_prev in x_dict.items():
                h_new = out_dict.get(node_type, h_prev)
                h_new = F.elu(h_new)
                h_new = self.dropout(h_new)
                next_dict[node_type] = self.norms[layer_idx][node_type](h_prev + h_new)
            x_dict = next_dict

        z_gene = self.output_norm["gene"](
            torch.matmul(batch["gene"], x_dict["gene"]) / math.sqrt(batch["gene"].shape[1])
        )
        z_cpg = self.output_norm["cpg"](
            torch.matmul(batch["meth"], x_dict["cpg"]) / math.sqrt(batch["meth"].shape[1])
        )
        z_mirna = self.output_norm["mirna"](
            torch.matmul(batch["mirna"], x_dict["mirna"]) / math.sqrt(batch["mirna"].shape[1])
        )

        if return_attention:
            return z_gene, z_cpg, z_mirna, None
        return z_gene, z_cpg, z_mirna
