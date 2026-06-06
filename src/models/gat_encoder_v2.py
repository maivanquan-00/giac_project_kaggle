"""
gat_encoder_v2.py
-----------------
MultiOmicGATModuleV2 — GIỮ NGUYÊN GAT, nhưng inject giá trị thật của bệnh nhân
vào node features TRƯỚC khi chạy GAT → message passing trở thành cá thể hoá.

Khác v1 (gat_encoder.py):
  - v1: GAT chạy trên node_emb GLOBAL → embedding giống mọi bệnh nhân; giá trị
        bệnh nhân chỉ vào SAU GAT.
  - v2: x[b,i] = E[i] + value[b,i]·scale + value[b,i]·E[i]·gamma  (inject TRƯỚC GAT)
        → embedding của 1 gene phụ thuộc methylation/expression THỰC TẾ của hàng
          xóm ở chính bệnh nhân đó. Dùng hết dữ liệu sinh học, không phí.

GAT vẫn là GATv2 (đúng tên đề tài). Vì node features giờ khác nhau theo bệnh nhân,
GAT phải chạy per-patient → batch-hoá + gradient checkpointing để khỏi OOM.
Nên chạy trên đồ thị THƯA (minimal graph) để nhẹ.

Inject = per-channel FiLM: scale/gamma là vector (H,) học được per-modality.
  value_scale init 0 (additive tắt); value_gamma init 0.5 (multiplicative bật vừa)
  → tín hiệu bệnh nhân có tiếng nói từ epoch 0. 2 param này loại khỏi weight_decay
  trong train.py (tránh bị dìm về 0).
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint
from torch_geometric.data import HeteroData
from torch_geometric.nn import GATv2Conv, HeteroConv

_NODE_TYPES = ["gene", "cpg", "mirna"]
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
                 n_layers: int, dropout: float, topk_seq: int = 32,
                 gat_chunk: int = 4):
        super().__init__()
        assert hidden_dim % n_heads == 0
        self.n_layers   = n_layers
        self.hidden_dim = hidden_dim
        self.topk_seq   = topk_seq
        # Số bệnh nhân/lần qua GAT. GAT per-patient nhân đồ thị B lần → OOM nếu
        # batch hết. Chunk nhỏ + gradient checkpointing giới hạn peak ≈ gat_chunk
        # × đồ-thị (đổi lại chậm hơn ~1.5-2×). Tăng nếu còn VRAM.
        self.gat_chunk  = max(1, int(gat_chunk))

        self.n_nodes = {"gene": dims["gene"], "cpg": dims["meth"], "mirna": dims["mirna"]}

        self.node_emb = nn.ParameterDict({
            "gene":  nn.Parameter(torch.empty(dims["gene"],  hidden_dim)),
            "cpg":   nn.Parameter(torch.empty(dims["meth"],  hidden_dim)),
            "mirna": nn.Parameter(torch.empty(dims["mirna"], hidden_dim)),
        })
        for p in self.node_emb.values():
            nn.init.xavier_uniform_(p)

        # ── Patient value injection (per-channel FiLM) ──
        self.value_scale = nn.ParameterDict({
            t: nn.Parameter(torch.zeros(hidden_dim)) for t in _NODE_TYPES
        })
        self.value_gamma = nn.ParameterDict({
            t: nn.Parameter(torch.full((hidden_dim,), 0.5)) for t in _NODE_TYPES
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

        self.cpg_pos_emb   = nn.Embedding(topk_seq, hidden_dim)
        self.mirna_pos_emb = nn.Embedding(topk_seq, hidden_dim)
        nn.init.normal_(self.cpg_pos_emb.weight,   std=0.02)
        nn.init.normal_(self.mirna_pos_emb.weight, std=0.02)

        self.gene_norm = nn.LayerNorm(hidden_dim)

        self._edge_cache = {}

    def film_summary(self):
        return {
            "cpg_gamma":   self.value_gamma["cpg"].mean().item(),
            "cpg_beta":    self.value_scale["cpg"].mean().item(),
            "mirna_gamma": self.value_gamma["mirna"].mean().item(),
            "mirna_beta":  self.value_scale["mirna"].mean().item(),
        }

    def _inject(self, t: str, value: torch.Tensor) -> torch.Tensor:
        """node features cá thể hoá (B, n_t, H): x = E + value·scale + value·E·gamma."""
        E = self.node_emb[t]
        val = value.unsqueeze(-1)
        return E.unsqueeze(0) + val * self.value_scale[t] + val * E.unsqueeze(0) * self.value_gamma[t]

    def _batched_edges(self, present: dict, B: int, device, graph_id: int):
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

    def _encode_chunk(self, vg, vc, vm, present, graph_id):
        bc = vg.shape[0]
        device = vg.device
        vals = {"gene": vg, "cpg": vc, "mirna": vm}
        h_dict = {
            t: self._inject(t, vals[t]).reshape(bc * self.n_nodes[t], self.hidden_dim)
            for t in _NODE_TYPES
        }
        batched_edges = self._batched_edges(present, bc, device, graph_id)
        for i in range(self.n_layers):
            out = self.convs[i](h_dict, batched_edges)
            h_dict = {
                t: self.layer_norms[i][t](h + F.elu(self.dropout(out.get(t, h))))
                for t, h in h_dict.items()
            }
        return tuple(h_dict[t].view(bc, self.n_nodes[t], self.hidden_dim) for t in _NODE_TYPES)

    def forward(self, batch: dict, graph: HeteroData):
        B = batch["gene"].shape[0]
        present = {k: v for k, v in graph.edge_index_dict.items() if v.shape[1] > 0}
        gid = id(graph)

        parts = {t: [] for t in _NODE_TYPES}
        for s in range(0, B, self.gat_chunk):
            vg = batch["gene"][s:s + self.gat_chunk]
            vc = batch["meth"][s:s + self.gat_chunk]
            vm = batch["mirna"][s:s + self.gat_chunk]
            if self.training and self.gat_chunk < B:
                eg, ec, em = checkpoint(
                    lambda a, b, c: self._encode_chunk(a, b, c, present, gid),
                    vg, vc, vm, use_reentrant=False,
                )
            else:
                eg, ec, em = self._encode_chunk(vg, vc, vm, present, gid)
            parts["gene"].append(eg)
            parts["cpg"].append(ec)
            parts["mirna"].append(em)

        emb = {t: torch.cat(parts[t], dim=0) for t in _NODE_TYPES}  # (B, n_t, H) cá thể hoá

        # Gene query: value-weighted pool toàn bộ gene
        z_gene = self.gene_norm(
            torch.einsum("bn,bnh->bh", batch["gene"], emb["gene"])
            / math.sqrt(batch["gene"].shape[1])
        )
        z_cpg_seq   = self._topk_seq(batch["meth"],  emb["cpg"],   self.topk_seq, self.cpg_pos_emb)
        z_mirna_seq = self._topk_seq(batch["mirna"], emb["mirna"], self.topk_seq, self.mirna_pos_emb)
        return z_gene, z_cpg_seq, z_mirna_seq

    def _topk_seq(self, X: torch.Tensor, E: torch.Tensor, K: int,
                  pos_emb: nn.Embedding) -> torch.Tensor:
        """Top-K token cho cross-attention. E là (B, n, H) đã cá thể hoá qua GAT."""
        B, n_feat = X.shape
        K = min(K, n_feat)
        topk_idx = X.abs().topk(K, dim=1).indices
        idx = topk_idx.unsqueeze(-1).expand(B, K, self.hidden_dim)
        E_topk = torch.gather(E, 1, idx)
        rank_ids = torch.arange(K, device=X.device).unsqueeze(0).expand(B, -1)
        return E_topk + pos_emb(rank_ids)
