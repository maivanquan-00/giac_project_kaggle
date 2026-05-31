"""
gat_encoder_v2.py
-----------------
MultiOmicGATModuleV2 — phiên bản patient-conditioned của MultiOmicGATModule.

Khác biệt cốt lõi so với v1 ([gat_encoder.py]):
  - v1: node_emb là embedding GLOBAL, GAT chạy 1 lần → embedding giống mọi bệnh nhân.
        Giá trị bệnh nhân chỉ vào SAU GAT (qua z_gene full + top-K CpG/miRNA).
  - v2: inject giá trị thật của bệnh nhân vào node features TRƯỚC GAT, rồi chạy
        GAT theo từng bệnh nhân (batch-hoá B đồ thị). Message passing trở thành
        cá thể hoá: embedding của 1 gene phụ thuộc methylation/expression thực tế
        của hàng xóm Ở CHÍNH BỆNH NHÂN ĐÓ. → giải quyết tận gốc việc "feature ngoài
        top-K bị bỏ giá trị" (tất cả value đều lan truyền qua đồ thị).

Patient value injection (per-channel FiLM, cũng thay scalar γ/β của v1):
    x[b, i] = E[i] + value[b, i] * scale + value[b, i] * E[i] * gamma
  với scale, gamma là vector (H,) học được per-modality. Init = 0 → x = E
  (GAT input ban đầu giống hệt v1, học dần tín hiệu bệnh nhân).

Chi phí: GAT chạy per-patient → ~B× chi phí GAT của v1. Nếu OOM, giảm batch_size.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from torch_geometric.nn import GATv2Conv, HeteroConv

_NODE_TYPES = ["gene", "cpg", "mirna"]
# Ánh xạ node type → key trong batch dict của bệnh nhân
_BATCH_KEY = {"gene": "gene", "cpg": "meth", "mirna": "mirna"}


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
        ("cpg",   "sameisland",   "cpg"):   hom(),
        ("gene",  "self_loop",    "gene"):  hom(),
        ("cpg",   "self_loop",    "cpg"):   hom(),
        ("mirna", "self_loop",    "mirna"): hom(),
    }, aggr="sum")


class MultiOmicGATModuleV2(nn.Module):
    def __init__(self, dims: dict, hidden_dim: int, n_heads: int,
                 n_layers: int, dropout: float, topk_seq: int = 32):
        super().__init__()
        assert hidden_dim % n_heads == 0
        self.n_layers   = n_layers
        self.hidden_dim = hidden_dim
        self.topk_seq   = topk_seq

        self.n_nodes = {"gene": dims["gene"], "cpg": dims["meth"], "mirna": dims["mirna"]}

        self.node_emb = nn.ParameterDict({
            "gene":  nn.Parameter(torch.empty(dims["gene"],  hidden_dim)),
            "cpg":   nn.Parameter(torch.empty(dims["meth"],  hidden_dim)),
            "mirna": nn.Parameter(torch.empty(dims["mirna"], hidden_dim)),
        })
        for p in self.node_emb.values():
            nn.init.xavier_uniform_(p)

        # ── Patient value injection (per-channel FiLM), init 0 → x = node_emb ──
        self.value_scale = nn.ParameterDict({
            t: nn.Parameter(torch.zeros(hidden_dim)) for t in _NODE_TYPES
        })
        self.value_gamma = nn.ParameterDict({
            t: nn.Parameter(torch.zeros(hidden_dim)) for t in _NODE_TYPES
        })

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

        # Rank-based positional encodings cho top-K sequence
        self.cpg_pos_emb   = nn.Embedding(topk_seq, hidden_dim)
        self.mirna_pos_emb = nn.Embedding(topk_seq, hidden_dim)
        nn.init.normal_(self.cpg_pos_emb.weight,   std=0.02)
        nn.init.normal_(self.mirna_pos_emb.weight, std=0.02)

        self.gene_norm = nn.LayerNorm(hidden_dim)

        # Cache batched edge_index theo (B, id(graph)) để không rebuild mỗi step
        self._edge_cache = {}

    # ── FiLM summary (per-channel → trả scalar mean cho reporting, tương thích v1) ──
    def film_summary(self):
        return {
            "cpg_gamma":   self.value_gamma["cpg"].mean().item(),
            "cpg_beta":    self.value_scale["cpg"].mean().item(),
            "mirna_gamma": self.value_gamma["mirna"].mean().item(),
            "mirna_beta":  self.value_scale["mirna"].mean().item(),
        }

    def _inject(self, t: str, value: torch.Tensor) -> torch.Tensor:
        """node features cá thể hoá: (B, n_t, H).

        x[b, i] = E[i] + value[b,i] * scale + value[b,i] * E[i] * gamma
        """
        E = self.node_emb[t]                      # (n_t, H)
        val = value.unsqueeze(-1)                 # (B, n_t, 1)
        scale = self.value_scale[t]               # (H,)
        gamma = self.value_gamma[t]               # (H,)
        x = E.unsqueeze(0) + val * scale + val * E.unsqueeze(0) * gamma
        return x                                  # (B, n_t, H)

    def _batched_edges(self, present: dict, B: int, device, graph_id: int):
        """Nhân bản edge_index của B đồ thị (disconnected), offset theo node count."""
        cache_key = (graph_id, B)
        if cache_key in self._edge_cache:
            return self._edge_cache[cache_key]
        ar = torch.arange(B, device=device)
        batched = {}
        for (s, r, d), ei in present.items():
            E_edges = ei.shape[1]
            src_off = (ar * self.n_nodes[s]).repeat_interleave(E_edges)
            dst_off = (ar * self.n_nodes[d]).repeat_interleave(E_edges)
            src = ei[0].repeat(B) + src_off
            dst = ei[1].repeat(B) + dst_off
            batched[(s, r, d)] = torch.stack([src, dst], dim=0)
        self._edge_cache[cache_key] = batched
        return batched

    def forward(self, batch: dict, graph: HeteroData):
        device = batch["gene"].device
        B = batch["gene"].shape[0]

        # 1) node features cá thể hoá rồi flatten (B*n_t, H) cho batched GAT
        h_dict = {}
        for t in _NODE_TYPES:
            x = self._inject(t, batch[_BATCH_KEY[t]])         # (B, n_t, H)
            h_dict[t] = x.reshape(B * self.n_nodes[t], self.hidden_dim)

        present = {k: v for k, v in graph.edge_index_dict.items() if v.shape[1] > 0}
        batched_edges = self._batched_edges(present, B, device, id(graph))

        # 2) GAT message passing (per-patient nhờ batched graph)
        for i in range(self.n_layers):
            out = self.convs[i](h_dict, batched_edges)
            h_dict = {
                t: self.layer_norms[i][t](h + F.elu(self.dropout(out.get(t, h))))
                for t, h in h_dict.items()
            }

        # 3) reshape về (B, n_t, H) — embedding giờ đã cá thể hoá theo bệnh nhân
        emb = {t: h_dict[t].view(B, self.n_nodes[t], self.hidden_dim) for t in _NODE_TYPES}

        # ── Gene query: value-weighted pooling toàn bộ gene (giống tinh thần v1) ──
        z_gene = self.gene_norm(
            torch.einsum("bn,bnh->bh", batch["gene"], emb["gene"])
            / math.sqrt(batch["gene"].shape[1])
        )

        # ── CpG/miRNA: top-K sequence (theo abs value) từ embedding đã cá thể hoá ──
        z_cpg_seq   = self._topk_seq(batch["meth"],  emb["cpg"],   self.topk_seq, self.cpg_pos_emb)
        z_mirna_seq = self._topk_seq(batch["mirna"], emb["mirna"], self.topk_seq, self.mirna_pos_emb)

        return z_gene, z_cpg_seq, z_mirna_seq

    def _topk_seq(self, X: torch.Tensor, E: torch.Tensor, K: int,
                  pos_emb: nn.Embedding) -> torch.Tensor:
        """Top-K token cho cross-attention. E giờ là (B, n, H) đã cá thể hoá nên
        KHÔNG cần FiLM lại ở đây (giá trị bệnh nhân đã nằm trong embedding qua GAT).
        """
        B, n_feat = X.shape
        K = min(K, n_feat)

        topk_idx = X.abs().topk(K, dim=1).indices                  # (B, K)
        idx = topk_idx.unsqueeze(-1).expand(B, K, self.hidden_dim)  # (B, K, H)
        E_topk = torch.gather(E, 1, idx)                           # (B, K, H)

        rank_ids = torch.arange(K, device=X.device).unsqueeze(0).expand(B, -1)
        return E_topk + pos_emb(rank_ids)
