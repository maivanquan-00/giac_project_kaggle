# """
# gat_encoder.py
# --------------
# Module 1 — Heterogeneous GAT Encoder

# Thay thế Self-Attention phẳng của MoXGATE bằng Graph Attention Network (GAT)
# chạy trên đồ thị sinh học.

# Kiến trúc:
#   Input: node features (sample vector) + heterogeneous graph structure
#   Output: node embeddings đã nhận thông tin từ hàng xóm sinh học

# Reference: Veličković et al., "Graph Attention Networks", ICLR 2018
#            Brody et al., "How Attentive are Graph Attention Networks?", ICLR 2022 (GATv2)
# """

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torch_geometric.nn import GATv2Conv, HeteroConv, Linear
# from torch_geometric.data import HeteroData


# class OmicGATEncoder(nn.Module):
#     """
#     GAT encoder cho MỘT modality (gene / cpg / mirna).
    
#     Mỗi modality có encoder riêng, KHÔNG chia sẻ tham số.
    
#     Flow:
#       raw_features (N_nodes, F_in)
#         → Linear projection → (N_nodes, hidden_dim)
#         → GATv2Conv layer 1  → (N_nodes, hidden_dim)
#         → GATv2Conv layer 2  → (N_nodes, hidden_dim)
#         → [mean pooling over nodes] → (hidden_dim,)  [per sample]
#     """

#     def __init__(
#         self,
#         in_dim: int,         # số features đầu vào (sau variance filtering)
#         hidden_dim: int,     # chiều embedding
#         n_heads: int,        # số attention heads
#         n_layers: int,       # số GAT layers (thường 2)
#         dropout: float,
#         node_type: str,      # 'gene', 'cpg', hoặc 'mirna' — chỉ để log
#     ):
#         super().__init__()
#         self.node_type  = node_type
#         self.hidden_dim = hidden_dim
#         self.n_layers   = n_layers

#         # Linear projection: F_in → hidden_dim
#         self.input_proj = nn.Sequential(
#             nn.Linear(in_dim, hidden_dim),
#             nn.LayerNorm(hidden_dim),
#             nn.ReLU(),
#             nn.Dropout(dropout),
#         )

#         # Stack GATv2 layers
#         # GATv2 tốt hơn GATv1 vì attention score phụ thuộc cả query lẫn key
#         # (Brody et al., 2022)
#         self.gat_layers = nn.ModuleList()
#         for i in range(n_layers):
#             # hidden_dim phải chia hết cho n_heads
#             assert hidden_dim % n_heads == 0, \
#                 f"hidden_dim={hidden_dim} phải chia hết cho n_heads={n_heads}"

#             self.gat_layers.append(
#                 GATv2Conv(
#                     in_channels  = hidden_dim,
#                     out_channels = hidden_dim // n_heads,  # mỗi head có out = hidden/heads
#                     heads        = n_heads,
#                     concat       = True,    # concat output của các heads → hidden_dim
#                     dropout      = dropout,
#                     add_self_loops = True,  # tự kết nối: node học từ chính nó
#                 )
#             )

#         self.norm_layers = nn.ModuleList([
#             nn.LayerNorm(hidden_dim) for _ in range(n_layers)
#         ])
#         self.dropout = nn.Dropout(dropout)

#     def forward(
#         self,
#         x: torch.Tensor,          # (N_nodes, F_in) — features của TẤT CẢ nodes
#         edge_index: torch.Tensor,  # (2, E) — cạnh trong đồ thị
#         return_attention: bool = False,
#     ):
#         """
#         Nếu return_attention=True, trả về thêm attention weights
#         (dùng trong interpretability).
#         """
#         # Project vào hidden space
#         h = self.input_proj(x)  # (N_nodes, hidden_dim)

#         attn_weights_list = []

#         # Chạy qua các GAT layers với residual connection
#         for i, (gat, norm) in enumerate(zip(self.gat_layers, self.norm_layers)):
#             if return_attention:
#                 h_new, (edge_idx, alpha) = gat(h, edge_index, return_attention_weights=True)
#                 attn_weights_list.append((edge_idx, alpha))
#             else:
#                 h_new = gat(h, edge_index)

#             h_new = F.elu(h_new)          # ELU thường tốt hơn ReLU cho GAT
#             h_new = self.dropout(h_new)
#             h     = norm(h_new + h)        # residual + layer norm

#         if return_attention:
#             return h, attn_weights_list
#         return h  # (N_nodes, hidden_dim)


# # ─────────────────────────────────────────────
# #  Wrapper: 3 encoders cho 3 omics + graph handling
# # ─────────────────────────────────────────────
# class MultiOmicGATModule(nn.Module):
#     """
#     Gọi 3 OmicGATEncoder riêng biệt, mỗi encoder cho một modality.
    
#     Đầu vào mỗi sample: vector đặc trưng của sample đó được broadcast
#     lên tất cả nodes (tức là node i nhận feature[i] của sample đó).
    
#     Sau GAT, ta lấy MEAN POOLING qua tất cả nodes để ra 1 vector
#     per-sample cho mỗi modality.
    
#     Shape flow:
#       gene_x  : (batch, F_gene)  → broadcast → (F_gene, F_gene) ... → (batch, hidden)
      
#     Lưu ý: Đây là "sample-wise graph" — mỗi sample được xử lý như
#     một đồ thị riêng nhưng chia sẻ cùng topology (edge_index).
#     """

#     def __init__(self, dims: dict, hidden_dim: int, n_heads: int, n_layers: int, dropout: float):
#         """
#         dims: {'gene': F_gene, 'meth': F_cpg, 'mirna': F_mirna}
#         """
#         super().__init__()

#         self.gene_encoder = OmicGATEncoder(
#             in_dim=dims["gene"], hidden_dim=hidden_dim,
#             n_heads=n_heads, n_layers=n_layers, dropout=dropout, node_type="gene"
#         )
#         self.cpg_encoder = OmicGATEncoder(
#             in_dim=dims["meth"], hidden_dim=hidden_dim,
#             n_heads=n_heads, n_layers=n_layers, dropout=dropout, node_type="cpg"
#         )
#         self.mirna_encoder = OmicGATEncoder(
#             in_dim=dims["mirna"], hidden_dim=hidden_dim,
#             n_heads=n_heads, n_layers=n_layers, dropout=dropout, node_type="mirna"
#         )

#     def forward(self, batch: dict, graph: HeteroData, return_attention: bool = False):
#         """
#         batch  : dict từ DataLoader {'gene': (B,F_g), 'meth': (B,F_m), 'mirna': (B,F_mi)}
#         graph  : HeteroData (topology cố định, không thay đổi theo batch)
        
#         Trả về:
#             z_gene  : (B, hidden_dim)
#             z_cpg   : (B, hidden_dim)
#             z_mirna : (B, hidden_dim)
#         """
#         B = batch["gene"].shape[0]  # batch size
#         device = batch["gene"].device

#         # ── Cách xử lý: mỗi feature vector của sample là node features ──
#         # Gene: (B, F_gene) → transpose → (F_gene, B) →
#         #       dùng F_gene nodes, mỗi node có B-dim feature
#         # Sau đó mean pool theo nodes → (B, hidden)
#         #
#         # Trực giác: mỗi "node" là một gene, feature của nó là
#         # giá trị biểu hiện của gene đó trên tất cả samples trong batch.

#         # Lấy edge_index cho từng loại cạnh
#         cpg_gene_edge = graph["cpg", "regulates", "gene"].edge_index.to(device) \
#                         if ("cpg", "regulates", "gene") in graph.edge_types \
#                         else _self_loop_edges(batch["meth"].shape[1], device)

#         gene_gene_edge = graph["gene", "interacts", "gene"].edge_index.to(device) \
#                          if ("gene", "interacts", "gene") in graph.edge_types \
#                          else _self_loop_edges(batch["gene"].shape[1], device)

#         mirna_gene_edge = graph["mirna", "targets", "gene"].edge_index.to(device) \
#                           if ("mirna", "targets", "gene") in graph.edge_types \
#                           else _self_loop_edges(batch["mirna"].shape[1], device)

#         # ── Encode từng modality ──────────────────────────────────────
#         # gene: dùng gene-gene PPI edges
#         if return_attention:
#             h_gene,  attn_gene  = self.gene_encoder(
#                 batch["gene"].T,  gene_gene_edge,  return_attention=True)
#             h_cpg,   attn_cpg   = self.cpg_encoder(
#                 batch["meth"].T,  cpg_gene_edge,   return_attention=True)
#             h_mirna, attn_mirna = self.mirna_encoder(
#                 batch["mirna"].T, mirna_gene_edge, return_attention=True)
#         else:
#             h_gene  = self.gene_encoder(batch["gene"].T,  gene_gene_edge)
#             h_cpg   = self.cpg_encoder(batch["meth"].T,   cpg_gene_edge)
#             h_mirna = self.mirna_encoder(batch["mirna"].T, mirna_gene_edge)

#         # h_gene : (F_gene, hidden_dim) → mean over nodes → (hidden_dim,)
#         # Nhưng ta cần (B, hidden_dim) — xử lý: encode per-feature, lấy mean
#         # Đây là "feature-level" representation
#         z_gene  = h_gene.mean(dim=0).unsqueeze(0).expand(B, -1)   # (B, hidden)
#         z_cpg   = h_cpg.mean(dim=0).unsqueeze(0).expand(B, -1)
#         z_mirna = h_mirna.mean(dim=0).unsqueeze(0).expand(B, -1)

#         if return_attention:
#             attn = {"gene": attn_gene, "cpg": attn_cpg, "mirna": attn_mirna}
#             return z_gene, z_cpg, z_mirna, attn

#         return z_gene, z_cpg, z_mirna  # mỗi cái shape (B, hidden_dim)


# # ─────────────────────────────────────────────
# #  Helper
# # ─────────────────────────────────────────────
# def _self_loop_edges(n_nodes: int, device) -> torch.Tensor:
#     """Tạo self-loop edges khi không có edge_index thực."""
#     idx = torch.arange(n_nodes, device=device)
#     return torch.stack([idx, idx], dim=0)



"""
Gemini
3 Lỗi Sai Chí Mạng Trong Kiến Trúc Cũ
1. Lỗi Crash PyTorch (mat1 and mat2 shapes cannot be multiplied)
Bạn đang truyền dữ liệu bệnh nhân batch["gene"].T có kích thước $19930 \times 32$ (với 32 là Batch Size) vào lớp nn.Linear(in_dim=19930, hidden_dim=256).
Lớp Linear sẽ cố gắng lấy chiều cuối cùng làm feature đầu vào. Nó kỳ vọng nhìn thấy số 19930, nhưng lại nhận được 32. 
PyTorch không thể nhân ma trận $19930 \times 32$ với trọng số $19930 \times 256$. 
Hơn nữa, Batch Size là một con số động (batch cuối cùng có thể chỉ có 16 bệnh nhân), bạn không bao giờ được phép dùng Batch Size làm Feature Dimension.
2. Lỗi Đồ thị Dị thể (Heterogeneous Mismatch)
Bạn đang truyền một tập cạnh hai chiều (Bipartite Edges) như cpg_gene_edge (từ 23111 node CpG trỏ sang 19930 node Gene) vào một mạng GATv2Conv thông thường. 
Mạng GAT cơ bản chỉ xử lý đồ thị đồng nhất (Homogeneous) — tức là Node nguồn và Node đích phải cùng chung một tập hợp. 
Việc bạn "ép" nó chạy chung sẽ khiến quá trình truyền tin (message passing) bị trỏ sai ID và làm hỏng hoàn toàn cấu trúc sinh học.
3. Lỗi Xóa Sạch Dữ Liệu Bệnh Nhân (Clone Bug)
Hãy nhìn vào dòng này trong code của bạn:z_gene = h_gene.mean(dim=0).unsqueeze(0).expand(B, -1)
Đoạn code này tính ra 1 vector duy nhất cho toàn bộ batch, sau đó nhân bản (copy-paste) nó ra 32 lần cho 32 bệnh nhân. 
Kết quả là cả 32 bệnh nhân đều có embedding y hệt nhau. Mô hình Subtyping của bạn bị tước bỏ hoàn toàn thông tin đặc trưng của từng người, Accuracy sẽ chỉ dừng ở mức random đoán mò.

Giải pháp chuẩn: PyG HeteroConv + Static Node Embeddings
Để mô hình vừa học được từ đồ thị sinh học khổng lồ, vừa giữ được tính cá nhân hóa của bệnh nhân (Patient-Specific), ta dùng công thức Toán học sau:
GNN học một tập hợp Node Embedding mang cấu trúc sinh học: $E_{gene} \in \mathbb{R}^{F_{gene} \times H_{dim}}$
Nhân chéo biểu diễn đó với dữ liệu hồ sơ bệnh án của từng người $X_{patient} \in \mathbb{R}^{B \times F_{gene}}$.
Áp dụng Dot Product: $Z = X_{patient} E_{gene} \in \mathbb{R}^{B \times H_{dim}}$.
Kết quả là mỗi bệnh nhân có một đại diện riêng lẻ, và bạn không bao giờ bị lỗi shape ma trận!

"""

"""
gat_encoder.py
--------------
Module 1 — Heterogeneous GAT Encoder (Fixed Architecture)

Sử dụng Static Node Embeddings kết hợp HeteroConv để lan truyền
thông tin sinh học. Sau đó, dùng phép chiếu (Projection) để tạo ra
Patient-Specific Embeddings từ hồ sơ Multi-omics của từng bệnh nhân.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATv2Conv, HeteroConv
from torch_geometric.data import HeteroData

class MultiOmicGATModule(nn.Module):
    def __init__(self, dims: dict, hidden_dim: int, n_heads: int, n_layers: int, dropout: float):
        """
        dims: {'gene': F_gene, 'meth': F_cpg, 'mirna': F_mirna}
        """
        super().__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        # 1. Khởi tạo Static Node Embeddings (Tính chất sinh học cốt lõi)
        self.node_emb = nn.ParameterDict({
            "gene": nn.Parameter(torch.randn(dims["gene"], hidden_dim)),
            "cpg": nn.Parameter(torch.randn(dims["meth"], hidden_dim)),
            "mirna": nn.Parameter(torch.randn(dims["mirna"], hidden_dim))
        })

        # Khởi tạo tham số bằng Xavier để hội tụ nhanh
        for emb in self.node_emb.values():
            nn.init.xavier_uniform_(emb)

        # 2. Xây dựng các lớp HeteroConv
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        
        for _ in range(n_layers):
            # HeteroConv tự động điều hướng message passing an toàn
            conv = HeteroConv({
                # Bipartite Edges: Nguồn -> Đích (cần truyền kích thước Tuple cho GATv2Conv)
                ("cpg", "regulates", "gene"): GATv2Conv((hidden_dim, hidden_dim), hidden_dim // n_heads, heads=n_heads, add_self_loops=False, dropout=dropout),
                ("mirna", "targets", "gene"): GATv2Conv((hidden_dim, hidden_dim), hidden_dim // n_heads, heads=n_heads, add_self_loops=False, dropout=dropout),
                # Homogeneous Edges: Gene <-> Gene
                ("gene", "interacts", "gene"): GATv2Conv(hidden_dim, hidden_dim // n_heads, heads=n_heads, add_self_loops=True, dropout=dropout),
            }, aggr="sum") # "sum" thường ưu việt hơn "mean" trong đồ thị sinh học
            self.convs.append(conv)
            
            # Layer Norm riêng cho từng loại node
            self.norms.append(nn.ModuleDict({
                "gene": nn.LayerNorm(hidden_dim),
                "cpg": nn.LayerNorm(hidden_dim),
                "mirna": nn.LayerNorm(hidden_dim)
            }))
            
        self.dropout = nn.Dropout(dropout)
        
        # THÊM 3 LỚP NORMALIZATION NÀY VÀO CUỐI HÀM __init__
        self.out_norm_gene = nn.LayerNorm(hidden_dim)
        self.out_norm_cpg = nn.LayerNorm(hidden_dim)
        self.out_norm_mirna = nn.LayerNorm(hidden_dim)

    def forward(self, batch: dict, graph: HeteroData, return_attention: bool = False):
        """
        Input: 
           batch: {'gene': (B, F_gene), 'meth': (B, F_cpg), 'mirna': (B, F_mirna)}
           graph: HeteroData chứa cấu trúc mạng
        """
        # ── BƯỚC 1: Lan truyền thông tin trên đồ thị tĩnh (Graph Embedding) ──
        x_dict = {
            "gene": self.node_emb["gene"],
            "cpg": self.node_emb["cpg"],
            "mirna": self.node_emb["mirna"]
        }

        for i in range(self.n_layers):
            # HeteroConv sẽ chỉ trả về các node nhận được message (như Gene)
            out_dict = self.convs[i](x_dict, graph.edge_index_dict)
            
            for key in x_dict.keys():
                if key in out_dict:
                    h = F.elu(out_dict[key])
                    h = self.dropout(h)
                    # Residual Connection + LayerNorm
                    x_dict[key] = self.norms[i][key](h + x_dict[key])
                # Note: Các node CpG, miRNA không có cạnh nhận vào nên không cập nhật qua GNN
                # Chúng sẽ được tối ưu hóa trực tiếp thông qua Backpropagation từ Loss cuối.

        # ── BƯỚC 2: Tích hợp với hồ sơ bệnh nhân (Patient-Specific Projection) ──
        # x_dict hiện chứa các vector thể hiện tính chất sinh học (Node, Hidden)
        # Ta dùng phép nhân ma trận (B, Node) x (Node, Hidden) -> (B, Hidden)
        
        # Lấy số lượng features của từng omics
        d_gene = batch["gene"].shape[1]
        d_cpg = batch["meth"].shape[1]
        d_mirna = batch["mirna"].shape[1]

        # Áp dụng Scaled Dot-Product (chia cho căn bậc 2 của số chiều)
        z_gene = self.out_norm_gene(torch.matmul(batch["gene"], x_dict["gene"]) / math.sqrt(d_gene))
        z_cpg = self.out_norm_cpg(torch.matmul(batch["meth"], x_dict["cpg"]) / math.sqrt(d_cpg))
        z_mirna = self.out_norm_mirna(torch.matmul(batch["mirna"], x_dict["mirna"]) / math.sqrt(d_mirna))

        # Bạn có thể phát triển thêm return_attention sau (hiện tại HeteroConv k hỗ trợ trả attention dict tự động)
        if return_attention:
            return z_gene, z_cpg, z_mirna, None

        return z_gene, z_cpg, z_mirna