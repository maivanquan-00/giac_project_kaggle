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
        ("cpg",   "sameisland",   "cpg"):   hom(),
        ("gene",  "self_loop",    "gene"):  hom(),
        ("cpg",   "self_loop",    "cpg"):   hom(),
        ("mirna", "self_loop",    "mirna"): hom(),
    }, aggr="sum")


class MultiOmicGATModule(nn.Module):
    def __init__(self, dims: dict, hidden_dim: int, n_heads: int,
                 n_layers: int, dropout: float, topk_seq: int = 32,
                 film_per_channel: bool = False,
                 use_modality_summary: bool = False,
                 summary_condition_topk: bool = False,
                 topk_selection: str = "zscore",
                 use_gat: bool = True,
                 use_film: bool = True,
                 use_pos_emb: bool = True,
                 gat_init_residual: float = 0.0):
        super().__init__()
        assert hidden_dim % n_heads == 0
        self.n_layers  = n_layers
        self.hidden_dim = hidden_dim
        # Ablation các thành phần "thêm thắt" (giữ cái nào chứng minh được giá trị):
        #   use_gat=False     → bỏ message passing, dùng thẳng node_emb.
        #   use_film=False    → bỏ γ/β học được, dùng z = E + E·value (baseline đơn giản).
        #   use_pos_emb=False → bỏ rank positional encoding (top-K thành tập bất biến hoán vị).
        self.use_gat     = use_gat
        self.use_film    = use_film
        self.use_pos_emb = use_pos_emb
        # Initial residual (GCNII): mỗi lớp giữ α phần embedding GỐC → GAT tinh chỉnh
        # nhẹ thay vì over-smooth. α=0 = behavior cũ; α~0.1-0.3 chống smoothing.
        self.gat_init_residual = gat_init_residual
        self.topk_seq  = topk_seq  # K tokens per modality for cross-attention
        # Tiêu chí chọn K token: "zscore" (mặc định, |value| lớn nhất = bất thường
        # nhất của bệnh nhân) | "random" (ablation: chọn K ngẫu nhiên/bệnh nhân để
        # kiểm chứng tiêu chí |z-score| có mang tín hiệu hay không).
        self.topk_selection = topk_selection
        # 2 cải tiến opt-in (default False = behavior v1 gốc):
        #   film_per_channel: γ/β FiLM thành vector (H,) thay scalar → điều biến
        #     từng channel theo value bệnh nhân (#2).
        #   use_modality_summary: thêm 1 token "tóm tắt full-signal" (pool TOÀN BỘ
        #     CpG/miRNA, như nhánh gene) vào đầu chuỗi K/V → tận dụng cả 3500
        #     feature thay vì chỉ top-32, không cần per-patient GAT.
        #   summary_condition_topk: trộn summary full-signal vào từng token TopK qua
        #     gate học được; gate init=0 nên ban đầu không phá baseline.
        self.film_per_channel     = film_per_channel
        self.use_modality_summary = use_modality_summary
        self.summary_condition_topk = summary_condition_topk

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
        self.cpg_pos_emb   = nn.Embedding(topk_seq, hidden_dim)
        self.mirna_pos_emb = nn.Embedding(topk_seq, hidden_dim)
        nn.init.normal_(self.cpg_pos_emb.weight,   std=0.02)
        nn.init.normal_(self.mirna_pos_emb.weight, std=0.02)

        # Phase 2.1a — Patient-aware FiLM params for top-K modulation.
        # z = E_topk + γ * E_topk * weights + β * weights; init γ=1, β=0 matches baseline.
        # film_per_channel=True → γ/β là vector (H,) (broadcast per channel); False → scalar.
        film_shape = (hidden_dim,) if film_per_channel else (1,)
        self.film_cpg_gamma   = nn.Parameter(torch.ones(film_shape))
        self.film_cpg_beta    = nn.Parameter(torch.zeros(film_shape))
        self.film_mirna_gamma = nn.Parameter(torch.ones(film_shape))
        self.film_mirna_beta  = nn.Parameter(torch.zeros(film_shape))

        # Summary vector norm for gene query only
        self.gene_norm = nn.LayerNorm(hidden_dim)

        # Full-signal summary norms (dùng cho summary token hoặc condition TopK)
        if use_modality_summary or summary_condition_topk:
            self.cpg_sum_norm   = nn.LayerNorm(hidden_dim)
            self.mirna_sum_norm = nn.LayerNorm(hidden_dim)
        if summary_condition_topk:
            self.cpg_summary_gate   = nn.Parameter(torch.tensor(0.0))
            self.mirna_summary_gate = nn.Parameter(torch.tensor(0.0))

    def film_summary(self):
        """Trả scalar mean của γ/β (tương thích reporting cho cả scalar lẫn vector)."""
        return {
            "cpg_gamma":   self.film_cpg_gamma.mean().item(),
            "cpg_beta":    self.film_cpg_beta.mean().item(),
            "mirna_gamma": self.film_mirna_gamma.mean().item(),
            "mirna_beta":  self.film_mirna_beta.mean().item(),
        }

    def forward(self, batch: dict, graph: HeteroData):
        x_dict = {k: self.node_emb[k] for k in ["gene", "cpg", "mirna"]}

        # Ablation use_gat=False: bỏ qua message passing → x_dict = node_emb thô.
        if self.use_gat:
            x0 = dict(x_dict)                            # embedding gốc cho initial residual
            a  = self.gat_init_residual
            present = {k: v for k, v in graph.edge_index_dict.items() if v.shape[1] > 0}
            for i in range(self.n_layers):
                out = self.convs[i](x_dict, present)
                upd = {t: h + F.elu(self.dropout(out.get(t, h))) for t, h in x_dict.items()}
                if a > 0.0:                              # GCNII: pha lại embedding gốc
                    upd = {t: (1.0 - a) * v + a * x0[t] for t, v in upd.items()}
                x_dict = {t: self.layer_norms[i][t](v) for t, v in upd.items()}

        # ── Gene: single summary vector (B, H) used as Query (Phase 2.1a baseline) ──
        z_gene = self.gene_norm(
            torch.matmul(batch["gene"], x_dict["gene"])
            / math.sqrt(batch["gene"].shape[1])
        )

        # ── CpG/miRNA: top-K sequence as Key/Value ──
        cpg_pos   = self.cpg_pos_emb   if self.use_pos_emb else None
        mirna_pos = self.mirna_pos_emb if self.use_pos_emb else None
        cpg_g, cpg_b     = (self.film_cpg_gamma,   self.film_cpg_beta)   if self.use_film else (None, None)
        mirna_g, mirna_b = (self.film_mirna_gamma, self.film_mirna_beta) if self.use_film else (None, None)
        z_cpg_seq   = self._topk_seq(batch["meth"],  x_dict["cpg"],  self.topk_seq, cpg_pos,   cpg_g,   cpg_b)
        z_mirna_seq = self._topk_seq(batch["mirna"], x_dict["mirna"], self.topk_seq, mirna_pos, mirna_g, mirna_b)

        # ── Full-signal summary: pool TOÀN BỘ feature (như gene). Summary này có
        #    thể là token riêng, hoặc được trộn vào từng TopK token qua gate. ──
        if self.use_modality_summary or self.summary_condition_topk:
            z_cpg_full = self.cpg_sum_norm(
                torch.matmul(batch["meth"], x_dict["cpg"]) / math.sqrt(batch["meth"].shape[1])
            ).unsqueeze(1)                                  # (B, 1, H)
            z_mirna_full = self.mirna_sum_norm(
                torch.matmul(batch["mirna"], x_dict["mirna"]) / math.sqrt(batch["mirna"].shape[1])
            ).unsqueeze(1)

            if self.summary_condition_topk:
                z_cpg_seq = z_cpg_seq + torch.tanh(self.cpg_summary_gate) * z_cpg_full
                z_mirna_seq = z_mirna_seq + torch.tanh(self.mirna_summary_gate) * z_mirna_full

        # ── Full-signal summary token: ghép vào đầu chuỗi K/V để cross-attention
        #    thấy [tóm-tắt-toàn-cục, top-K] ──
        if self.use_modality_summary:
            z_cpg_seq   = torch.cat([z_cpg_full,   z_cpg_seq],   dim=1)   # (B, K+1, H)
            z_mirna_seq = torch.cat([z_mirna_full, z_mirna_seq], dim=1)

        return z_gene, z_cpg_seq, z_mirna_seq

    def _topk_seq(self, X: torch.Tensor, E: torch.Tensor, K: int,
                  pos_emb: nn.Embedding = None,
                  film_gamma: torch.Tensor = None,
                  film_beta: torch.Tensor = None) -> torch.Tensor:
        """Top-K patient-aware sequence with learnable FiLM modulation.

        z = E_topk + γ * E_topk * weights + β * weights
        Init γ=1, β=0 → equivalent to baseline `E_topk + E_topk * weights`.
        Model learns to adjust γ (scale of multiplicative patient signal) and β
        (additive patient signal bias).
        """
        B, n_feat = X.shape
        K = min(K, n_feat)

        if self.topk_selection == "random":
            # Ablation: chọn K feature NGẪU NHIÊN/bệnh nhân (không theo |z-score|).
            # rand + topk = K chỉ số phân biệt ngẫu nhiên mỗi hàng.
            scores   = torch.rand(B, n_feat, device=X.device)
            topk_idx = scores.topk(K, dim=1).indices     # (B, K) ngẫu nhiên
        else:                                            # "zscore" (mặc định)
            topk_idx = X.abs().topk(K, dim=1).indices    # (B, K) bất thường nhất
        E_topk   = E[topk_idx]                          # (B, K, H)

        weights = X.gather(1, topk_idx).unsqueeze(-1)   # (B, K, 1)
        if film_gamma is not None and film_beta is not None:
            z_seq = E_topk + film_gamma * E_topk * weights + film_beta * weights
        else:
            z_seq = E_topk + E_topk * weights           # baseline fallback

        if pos_emb is not None:
            rank_ids = torch.arange(K, device=X.device).unsqueeze(0).expand(B, -1)
            z_seq    = z_seq + pos_emb(rank_ids)

        return z_seq
