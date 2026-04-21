# """
# model.py
# --------
# GIAC model: Graph encoder + Gated Modality Fusion + Focal Loss classifier.

# Phase B1 change: Cross-attention fusion replaced by a single patient-specific
# Gated Fusion MLP. Ablation showed cross-attention was destroying signal
# (all < meth_only). Patient gate already learned to suppress miRNA correctly.
# """

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torch_geometric.data import HeteroData

# from src.models.gat_encoder import MultiOmicGATModule
# from src.models.classifier import (
#     FocalLoss,
#     SubtypeClassifier,
#     frobenius_regularization_loss,
# )


# class GIACModel(nn.Module):
#     """GIAC model with Gated Modality Fusion.

#     Architecture:
#         1. GAT Encoder  → z_gene, z_cpg, z_mirna  (B, hidden_dim each)
#         2. Modality Gate → per-patient softmax weights over 3 modalities
#         3. Weighted Sum  → fused = sum_m(gate_m * z_m)  (B, hidden_dim)
#         4. Classifier   → logits  (B, num_classes)
#     """

#     def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
#         super().__init__()

#         hidden_dim = cfg_model["hidden_dim"]
#         num_classes = cfg_model["num_classes"]
#         gate_dropout = cfg_model.get("gate_dropout", cfg_model["classifier_dropout"])

#         self.gat_module = MultiOmicGATModule(
#             dims=dims,
#             hidden_dim=hidden_dim,
#             n_heads=cfg_model["gat_heads"],
#             n_layers=cfg_model["gat_layers"],
#             dropout=cfg_model["gat_dropout"],
#         )

#         # ── Gated Modality Fusion ─────────────────────────────────────
#         # Input: concat of 3 modality vectors  (B, hidden_dim*3)
#         # Output: softmax weights over 3 modalities  (B, 3)
#         self.modality_gate = nn.Sequential(
#             nn.LayerNorm(hidden_dim * 3),
#             nn.Linear(hidden_dim * 3, hidden_dim),
#             nn.GELU(),
#             nn.Dropout(gate_dropout),
#             nn.Linear(hidden_dim, 3),
#         )

#         self.classifier = SubtypeClassifier(
#             hidden_dim=hidden_dim,
#             final_dim=cfg_model["final_dim"],
#             num_classes=num_classes,
#             dropout=cfg_model["classifier_dropout"],
#         )

#         self.loss_name = cfg_train.get("loss_name", "focal").lower()
#         self.register_buffer("class_weights", torch.ones(num_classes, dtype=torch.float32))
#         self.focal_loss = FocalLoss(
#             gamma=cfg_train["focal_gamma"],
#             alpha=cfg_train["focal_alpha"],
#             num_classes=num_classes,
#             label_smoothing=cfg_train.get("label_smoothing", 0.0),
#         )
#         self.lambda2 = cfg_train["lambda_frobenius"]

#     def set_class_weights(self, class_weights: torch.Tensor):
#         normalized = class_weights / class_weights.mean().clamp_min(1e-8)
#         self.class_weights.copy_(normalized.to(self.class_weights.device))
#         self.focal_loss.set_alpha(self.class_weights)

#     def forward(self, batch: dict, graph: HeteroData, return_interpretability: bool = False):
#         # 1. Graph-based encoding per modality
#         z_gene, z_cpg, z_mirna = self.gat_module(batch, graph)  # each: (B, hidden_dim)

#         # 2. Patient-specific modality gate
#         gate_input = torch.cat([z_gene, z_cpg, z_mirna], dim=-1)  # (B, hidden_dim*3)
#         patient_gate = F.softmax(self.modality_gate(gate_input), dim=-1)  # (B, 3)

#         # 3. Gated weighted sum fusion
#         stacked = torch.stack([z_gene, z_cpg, z_mirna], dim=1)   # (B, 3, hidden_dim)
#         fused = (stacked * patient_gate.unsqueeze(-1)).sum(dim=1) # (B, hidden_dim)

#         # 4. Classification
#         logits = self.classifier(fused)

#         if return_interpretability:
#             return logits, None, {"patient": patient_gate}
#         return logits

#     def compute_loss(self, logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
#         if self.loss_name == "cross_entropy":
#             loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
#         else:
#             loss_cls = self.focal_loss(logits, labels)

#         # Frobenius regularization on gate MLP weights
#         loss_frob = frobenius_regularization_loss(
#             self.modality_gate, self.lambda2, param_prefix="weight"
#         )
#         return loss_cls + loss_frob


# """
# model.py
# --------
# GIAC model: Graph encoder + Gated Modality Fusion + Shortcut path + Focal Loss.

# Architecture:
#     1. GAT Encoder    → z_gene, z_cpg, z_mirna  (B, hidden_dim each)
#     2. Modality Gate  → per-patient softmax weights → fused_gat  (B, hidden_dim)
#     3. Shortcut       → Linear(raw concat) → fused_shortcut  (B, hidden_dim)
#     4. Residual Mix   → fused = alpha*fused_gat + (1-alpha)*fused_shortcut
#                         alpha là learnable scalar, học tự động trong training
#     5. Classifier     → logits  (B, num_classes)

# Lý do thêm shortcut:
#     - Softmax baseline (shortcut only) đạt F1=0.83 vì gradient trực tiếp
#     - GAT alone đạt F1=0.72 vì gradient loãng qua nhiều bước trung gian
#     - Shortcut đảm bảo minority classes (HM-SNV, EBV) vẫn nhận gradient mạnh
#     - fusion_alpha tự học: nếu GAT không giúp ích thì alpha → 0 tự động
# """

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torch_geometric.data import HeteroData

# from src.models.gat_encoder import MultiOmicGATModule
# from src.models.classifier import (
#     FocalLoss,
#     SubtypeClassifier,
#     frobenius_regularization_loss,
# )


# class GIACModel(nn.Module):

#     def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
#         super().__init__()

#         hidden_dim   = cfg_model["hidden_dim"]
#         num_classes  = cfg_model["num_classes"]
#         gate_dropout = cfg_model.get("gate_dropout", cfg_model["classifier_dropout"])

#         # ── Module 1: GAT Encoder ─────────────────────────────────────
#         self.gat_module = MultiOmicGATModule(
#             dims       = dims,
#             hidden_dim = hidden_dim,
#             n_heads    = cfg_model["gat_heads"],
#             n_layers   = cfg_model["gat_layers"],
#             dropout    = cfg_model["gat_dropout"],
#         )

#         # ── Module 2: Gated Modality Fusion (GAT path) ────────────────
#         # Input : concat [z_gene, z_cpg, z_mirna]  (B, hidden_dim*3)
#         # Output: softmax weights over 3 modalities (B, 3)
#         self.modality_gate = nn.Sequential(
#             nn.LayerNorm(hidden_dim * 3),
#             nn.Linear(hidden_dim * 3, hidden_dim),
#             nn.GELU(),
#             nn.Dropout(gate_dropout),
#             nn.Linear(hidden_dim, 3),
#         )

#         # ── Module 3: Shortcut path (raw → hidden) ────────────────────
#         # Concat raw features của 3 omics → project về hidden_dim
#         # Đảm bảo gradient flow trực tiếp từ loss đến raw features
#         # → minority classes như HM-SNV, EBV vẫn nhận gradient mạnh
#         raw_dim = dims["gene"] + dims["meth"] + dims["mirna"]
#         self.shortcut = nn.Sequential(
#             nn.Linear(raw_dim, hidden_dim * 2),
#             nn.GELU(),
#             nn.Dropout(gate_dropout),
#             nn.Linear(hidden_dim * 2, hidden_dim),
#             nn.LayerNorm(hidden_dim),
#         )

#         # ── fusion_alpha: tỷ lệ pha trộn GAT vs Shortcut ─────────────
#         # sigmoid(0.0) = 0.5 → khởi đầu blend đều 2 path
#         # Sau training model tự quyết định cần bao nhiêu GAT
#         self.fusion_alpha = nn.Parameter(torch.tensor(0.0))

#         # ── Module 4: Classifier ──────────────────────────────────────
#         self.classifier = SubtypeClassifier(
#             hidden_dim  = hidden_dim,
#             final_dim   = cfg_model["final_dim"],
#             num_classes = num_classes,
#             dropout     = cfg_model["classifier_dropout"],
#         )

#         # ── Loss ──────────────────────────────────────────────────────
#         self.loss_name = cfg_train.get("loss_name", "focal").lower()
#         self.register_buffer(
#             "class_weights", torch.ones(num_classes, dtype=torch.float32)
#         )
#         self.focal_loss = FocalLoss(
#             gamma           = cfg_train["focal_gamma"],
#             alpha           = cfg_train["focal_alpha"],
#             num_classes     = num_classes,
#             label_smoothing = cfg_train.get("label_smoothing", 0.0),
#         )
#         self.lambda2 = cfg_train["lambda_frobenius"]

#     def set_class_weights(self, class_weights: torch.Tensor):
#         normalized = class_weights / class_weights.mean().clamp_min(1e-8)
#         self.class_weights.copy_(normalized.to(self.class_weights.device))
#         self.focal_loss.set_alpha(self.class_weights)

#     def forward(
#         self,
#         batch: dict,
#         graph: HeteroData,
#         return_interpretability: bool = False,
#     ):
#         # ── GAT path ──────────────────────────────────────────────────
#         z_gene, z_cpg, z_mirna = self.gat_module(batch, graph)  # (B, H) each

#         gate_input   = torch.cat([z_gene, z_cpg, z_mirna], dim=-1)   # (B, H*3)
#         patient_gate = F.softmax(self.modality_gate(gate_input), dim=-1)  # (B, 3)

#         stacked   = torch.stack([z_gene, z_cpg, z_mirna], dim=1)      # (B, 3, H)
#         fused_gat = (stacked * patient_gate.unsqueeze(-1)).sum(dim=1)  # (B, H)

#         # ── Shortcut path ─────────────────────────────────────────────
#         x_raw          = torch.cat(
#             [batch["gene"], batch["meth"], batch["mirna"]], dim=-1
#         )                                          # (B, F_gene+F_meth+F_mirna)
#         fused_shortcut = self.shortcut(x_raw)      # (B, H)

#         # ── Residual mix ──────────────────────────────────────────────
#         alpha = torch.sigmoid(self.fusion_alpha)   # scalar trong (0, 1)
#         fused = alpha * fused_gat + (1.0 - alpha) * fused_shortcut  # (B, H)

#         # ── Classification ────────────────────────────────────────────
#         logits = self.classifier(fused)

#         if return_interpretability:
#             return logits, None, {
#                 "patient":      patient_gate,       # (B, 3) — per-patient gate
#                 "fusion_alpha": alpha.item(),        # scalar — GAT vs shortcut ratio
#             }
#         return logits

#     def compute_loss(
#         self, logits: torch.Tensor, labels: torch.Tensor
#     ) -> torch.Tensor:
#         if self.loss_name == "cross_entropy":
#             loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
#         else:
#             loss_cls = self.focal_loss(logits, labels)

#         loss_frob = frobenius_regularization_loss(
#             self.modality_gate, self.lambda2, param_prefix="weight"
#         )
#         return loss_cls + loss_frob

# """
# model.py — GIAC model với Gated Fusion + Shortcut + Entropy Reg.

# Fix:
#   1. forward() trả về patient_gate để compute_loss dùng entropy penalty
#   2. compute_loss() thêm entropy regularization chống gate collapse
#   3. fusion_alpha init = -1.0 → sigmoid(-1)≈0.27, ưu tiên shortcut ban đầu
#      (shortcut đã proven tốt hơn GAT đơn độc)
# """

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torch_geometric.data import HeteroData
# from entmax import entmax15, sparsemax

# from src.models.gat_encoder import MultiOmicGATModule
# from src.models.classifier import (
#     FocalLoss,
#     SubtypeClassifier,
#     frobenius_regularization_loss,
# )


# class GIACModel(nn.Module):

#     def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
#         super().__init__()

#         hidden_dim   = cfg_model["hidden_dim"]
#         num_classes  = cfg_model["num_classes"]
#         gate_dropout = cfg_model.get("gate_dropout", cfg_model["classifier_dropout"])

#         # Module 1: GAT Encoder
#         self.gat_module = MultiOmicGATModule(
#             dims       = dims,
#             hidden_dim = hidden_dim,
#             n_heads    = cfg_model["gat_heads"],
#             n_layers   = cfg_model["gat_layers"],
#             dropout    = cfg_model["gat_dropout"],
#         )

#         # Module 2: Gated Modality Fusion
#         self.modality_gate = nn.Sequential(
#             nn.LayerNorm(hidden_dim * 3),
#             nn.Linear(hidden_dim * 3, hidden_dim),
#             nn.GELU(),
#             nn.Dropout(gate_dropout),
#             nn.Linear(hidden_dim, 3),
#         )

#         with torch.no_grad():
#             self.modality_gate[-1].bias[0] += 0.0  # gene giữ nguyên
#             self.modality_gate[-1].bias[1] += 0.3  # meth nhỉnh hơn chút
#             self.modality_gate[-1].bias[2] += 0.1  # mirna nhỉnh hơn xỉu

#         # Module 3: Shortcut path
#         raw_dim = dims["gene"] + dims["meth"] + dims["mirna"]
#         self.shortcut = nn.Sequential(
#             nn.Linear(raw_dim, hidden_dim * 2),
#             nn.GELU(),
#             nn.Dropout(gate_dropout),
#             nn.Linear(hidden_dim * 2, hidden_dim),
#             nn.LayerNorm(hidden_dim),
#         )

#         # fusion_alpha: init=-1.0 → sigmoid≈0.27, ưu tiên shortcut ban đầu
#         # Lý do: shortcut proven F1=0.83, GAT cần thêm epoch để "earn" trust
#         self.fusion_alpha = nn.Parameter(torch.tensor(-1.0))

#         # Module 4: Classifier
#         self.classifier = SubtypeClassifier(
#             hidden_dim  = hidden_dim,
#             final_dim   = cfg_model["final_dim"],
#             num_classes = num_classes,
#             dropout     = cfg_model["classifier_dropout"],
#         )

#         # Loss config
#         self.loss_name = cfg_train.get("loss_name", "focal").lower()
#         self.register_buffer(
#             "class_weights", torch.ones(num_classes, dtype=torch.float32)
#         )
#         self.focal_loss = FocalLoss(
#             gamma           = cfg_train["focal_gamma"],
#             alpha           = cfg_train["focal_alpha"],
#             num_classes     = num_classes,
#             label_smoothing = cfg_train.get("label_smoothing", 0.0),
#         )
#         self.lambda2        = cfg_train["lambda_frobenius"]
#         # Entropy penalty weight — lÃ¢Ìy tÆ°Ì€ config hoÄƒÌ£c default 0.01
#         self.lambda_entropy = cfg_train.get("lambda_entropy", 0.0)
#         self.sparsemax_alpha = cfg_model.get("sparsemax_alpha", 1.5)

#     def set_class_weights(self, class_weights: torch.Tensor):
#         normalized = class_weights / class_weights.mean().clamp_min(1e-8)
#         self.class_weights.copy_(normalized.to(self.class_weights.device))
#         self.focal_loss.set_alpha(self.class_weights)

#     def forward(self, batch: dict, graph: HeteroData, return_interpretability: bool = False):
#         # GAT path
#         z_gene, z_cpg, z_mirna = self.gat_module(batch, graph)

#         gate_input   = torch.cat([z_gene, z_cpg, z_mirna], dim=-1)
#         gate_logits  = self.modality_gate(gate_input)
        
#         if self.sparsemax_alpha == 1.0:
#             patient_gate = F.softmax(gate_logits, dim=-1)
#         elif self.sparsemax_alpha == 1.5:
#             patient_gate = entmax15(gate_logits, dim=-1)
#         else:
#             patient_gate = sparsemax(gate_logits, dim=-1)  # (B, 3)

#         stacked   = torch.stack([z_gene, z_cpg, z_mirna], dim=1)
#         fused_gat = (stacked * patient_gate.unsqueeze(-1)).sum(dim=1)

#         # Shortcut path
#         x_raw          = torch.cat([batch["gene"], batch["meth"], batch["mirna"]], dim=-1)
#         fused_shortcut = self.shortcut(x_raw)

#         # Residual mix
#         alpha = torch.sigmoid(self.fusion_alpha)
#         fused = alpha * fused_gat + (1.0 - alpha) * fused_shortcut

#         logits = self.classifier(fused)

#         if return_interpretability:
#             return logits, None, {
#                 "patient":      patient_gate,
#                 "fusion_alpha": alpha.item(),
#             }

#         # Training: trả thêm patient_gate để compute_loss tính entropy penalty
#         return logits, patient_gate

#     def compute_loss(self, logits: torch.Tensor, labels: torch.Tensor,
#                      patient_gate: torch.Tensor = None) -> torch.Tensor:
#         # Classification loss
#         if self.loss_name == "cross_entropy":
#             loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
#         else:
#             loss_cls = self.focal_loss(logits, labels)

#         # Frobenius regularization
#         loss_frob = frobenius_regularization_loss(
#             self.modality_gate, self.lambda2, param_prefix="weight"
#         )

#         # Entropy penalty — phạt nếu gate quá uniform (collapse)
#         # H(gate) = -sum(p*log(p)), cao = uniform
#         # Ta muốn gate phân biệt → minimize H → thêm +lambda*H vào loss
#         if patient_gate is not None and self.lambda_entropy > 0:
#             entropy = -(patient_gate * (patient_gate + 1e-8).log()).sum(dim=-1).mean()
#             loss_entropy = self.lambda_entropy * entropy
#         else:
#             loss_entropy = 0.0

#         return loss_cls + loss_frob + loss_entropy

# """
# model.py
# --------
# GIAC model: Graph encoder + Gated Modality Fusion + Focal Loss classifier.

# Phase B1 change: Cross-attention fusion replaced by a single patient-specific
# Gated Fusion MLP. Ablation showed cross-attention was destroying signal
# (all < meth_only). Patient gate already learned to suppress miRNA correctly.
# """

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torch_geometric.data import HeteroData

# from src.models.gat_encoder import MultiOmicGATModule
# from src.models.classifier import (
#     FocalLoss,
#     SubtypeClassifier,
#     frobenius_regularization_loss,
# )


# class GIACModel(nn.Module):
#     """GIAC model with Gated Modality Fusion.

#     Architecture:
#         1. GAT Encoder  → z_gene, z_cpg, z_mirna  (B, hidden_dim each)
#         2. Modality Gate → per-patient softmax weights over 3 modalities
#         3. Weighted Sum  → fused = sum_m(gate_m * z_m)  (B, hidden_dim)
#         4. Classifier   → logits  (B, num_classes)
#     """

#     def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
#         super().__init__()

#         hidden_dim = cfg_model["hidden_dim"]
#         num_classes = cfg_model["num_classes"]
#         gate_dropout = cfg_model.get("gate_dropout", cfg_model["classifier_dropout"])

#         self.gat_module = MultiOmicGATModule(
#             dims=dims,
#             hidden_dim=hidden_dim,
#             n_heads=cfg_model["gat_heads"],
#             n_layers=cfg_model["gat_layers"],
#             dropout=cfg_model["gat_dropout"],
#         )

#         # ── Gated Modality Fusion ─────────────────────────────────────
#         # Input: concat of 3 modality vectors  (B, hidden_dim*3)
#         # Output: softmax weights over 3 modalities  (B, 3)
#         self.modality_gate = nn.Sequential(
#             nn.LayerNorm(hidden_dim * 3),
#             nn.Linear(hidden_dim * 3, hidden_dim),
#             nn.GELU(),
#             nn.Dropout(gate_dropout),
#             nn.Linear(hidden_dim, 3),
#         )

#         self.classifier = SubtypeClassifier(
#             hidden_dim=hidden_dim,
#             final_dim=cfg_model["final_dim"],
#             num_classes=num_classes,
#             dropout=cfg_model["classifier_dropout"],
#         )

#         self.loss_name = cfg_train.get("loss_name", "focal").lower()
#         self.register_buffer("class_weights", torch.ones(num_classes, dtype=torch.float32))
#         self.focal_loss = FocalLoss(
#             gamma=cfg_train["focal_gamma"],
#             alpha=cfg_train["focal_alpha"],
#             num_classes=num_classes,
#             label_smoothing=cfg_train.get("label_smoothing", 0.0),
#         )
#         self.lambda2 = cfg_train["lambda_frobenius"]

#     def set_class_weights(self, class_weights: torch.Tensor):
#         normalized = class_weights / class_weights.mean().clamp_min(1e-8)
#         self.class_weights.copy_(normalized.to(self.class_weights.device))
#         self.focal_loss.set_alpha(self.class_weights)

#     def forward(self, batch: dict, graph: HeteroData, return_interpretability: bool = False):
#         # 1. Graph-based encoding per modality
#         z_gene, z_cpg, z_mirna = self.gat_module(batch, graph)  # each: (B, hidden_dim)

#         # 2. Patient-specific modality gate
#         gate_input = torch.cat([z_gene, z_cpg, z_mirna], dim=-1)  # (B, hidden_dim*3)
#         patient_gate = F.softmax(self.modality_gate(gate_input), dim=-1)  # (B, 3)

#         # 3. Gated weighted sum fusion
#         stacked = torch.stack([z_gene, z_cpg, z_mirna], dim=1)   # (B, 3, hidden_dim)
#         fused = (stacked * patient_gate.unsqueeze(-1)).sum(dim=1) # (B, hidden_dim)

#         # 4. Classification
#         logits = self.classifier(fused)

#         if return_interpretability:
#             return logits, None, {"patient": patient_gate}
#         return logits

#     def compute_loss(self, logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
#         if self.loss_name == "cross_entropy":
#             loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
#         else:
#             loss_cls = self.focal_loss(logits, labels)

#         # Frobenius regularization on gate MLP weights
#         loss_frob = frobenius_regularization_loss(
#             self.modality_gate, self.lambda2, param_prefix="weight"
#         )
#         return loss_cls + loss_frob


# """
# model.py
# --------
# GIAC model: Graph encoder + Gated Modality Fusion + Shortcut path + Focal Loss.

# Architecture:
#     1. GAT Encoder    → z_gene, z_cpg, z_mirna  (B, hidden_dim each)
#     2. Modality Gate  → per-patient softmax weights → fused_gat  (B, hidden_dim)
#     3. Shortcut       → Linear(raw concat) → fused_shortcut  (B, hidden_dim)
#     4. Residual Mix   → fused = alpha*fused_gat + (1-alpha)*fused_shortcut
#                         alpha là learnable scalar, học tự động trong training
#     5. Classifier     → logits  (B, num_classes)

# Lý do thêm shortcut:
#     - Softmax baseline (shortcut only) đạt F1=0.83 vì gradient trực tiếp
#     - GAT alone đạt F1=0.72 vì gradient loãng qua nhiều bước trung gian
#     - Shortcut đảm bảo minority classes (HM-SNV, EBV) vẫn nhận gradient mạnh
#     - fusion_alpha tự học: nếu GAT không giúp ích thì alpha → 0 tự động
# """

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torch_geometric.data import HeteroData

# from src.models.gat_encoder import MultiOmicGATModule
# from src.models.classifier import (
#     FocalLoss,
#     SubtypeClassifier,
#     frobenius_regularization_loss,
# )


# class GIACModel(nn.Module):

#     def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
#         super().__init__()

#         hidden_dim   = cfg_model["hidden_dim"]
#         num_classes  = cfg_model["num_classes"]
#         gate_dropout = cfg_model.get("gate_dropout", cfg_model["classifier_dropout"])

#         # ── Module 1: GAT Encoder ─────────────────────────────────────
#         self.gat_module = MultiOmicGATModule(
#             dims       = dims,
#             hidden_dim = hidden_dim,
#             n_heads    = cfg_model["gat_heads"],
#             n_layers   = cfg_model["gat_layers"],
#             dropout    = cfg_model["gat_dropout"],
#         )

#         # ── Module 2: Gated Modality Fusion (GAT path) ────────────────
#         # Input : concat [z_gene, z_cpg, z_mirna]  (B, hidden_dim*3)
#         # Output: softmax weights over 3 modalities (B, 3)
#         self.modality_gate = nn.Sequential(
#             nn.LayerNorm(hidden_dim * 3),
#             nn.Linear(hidden_dim * 3, hidden_dim),
#             nn.GELU(),
#             nn.Dropout(gate_dropout),
#             nn.Linear(hidden_dim, 3),
#         )

#         # ── Module 3: Shortcut path (raw → hidden) ────────────────────
#         # Concat raw features của 3 omics → project về hidden_dim
#         # Đảm bảo gradient flow trực tiếp từ loss đến raw features
#         # → minority classes như HM-SNV, EBV vẫn nhận gradient mạnh
#         raw_dim = dims["gene"] + dims["meth"] + dims["mirna"]
#         self.shortcut = nn.Sequential(
#             nn.Linear(raw_dim, hidden_dim * 2),
#             nn.GELU(),
#             nn.Dropout(gate_dropout),
#             nn.Linear(hidden_dim * 2, hidden_dim),
#             nn.LayerNorm(hidden_dim),
#         )

#         # ── fusion_alpha: tỷ lệ pha trộn GAT vs Shortcut ─────────────
#         # sigmoid(0.0) = 0.5 → khởi đầu blend đều 2 path
#         # Sau training model tự quyết định cần bao nhiêu GAT
#         self.fusion_alpha = nn.Parameter(torch.tensor(0.0))

#         # ── Module 4: Classifier ──────────────────────────────────────
#         self.classifier = SubtypeClassifier(
#             hidden_dim  = hidden_dim,
#             final_dim   = cfg_model["final_dim"],
#             num_classes = num_classes,
#             dropout     = cfg_model["classifier_dropout"],
#         )

#         # ── Loss ──────────────────────────────────────────────────────
#         self.loss_name = cfg_train.get("loss_name", "focal").lower()
#         self.register_buffer(
#             "class_weights", torch.ones(num_classes, dtype=torch.float32)
#         )
#         self.focal_loss = FocalLoss(
#             gamma           = cfg_train["focal_gamma"],
#             alpha           = cfg_train["focal_alpha"],
#             num_classes     = num_classes,
#             label_smoothing = cfg_train.get("label_smoothing", 0.0),
#         )
#         self.lambda2 = cfg_train["lambda_frobenius"]

#     def set_class_weights(self, class_weights: torch.Tensor):
#         normalized = class_weights / class_weights.mean().clamp_min(1e-8)
#         self.class_weights.copy_(normalized.to(self.class_weights.device))
#         self.focal_loss.set_alpha(self.class_weights)

#     def forward(
#         self,
#         batch: dict,
#         graph: HeteroData,
#         return_interpretability: bool = False,
#     ):
#         # ── GAT path ──────────────────────────────────────────────────
#         z_gene, z_cpg, z_mirna = self.gat_module(batch, graph)  # (B, H) each

#         gate_input   = torch.cat([z_gene, z_cpg, z_mirna], dim=-1)   # (B, H*3)
#         patient_gate = F.softmax(self.modality_gate(gate_input), dim=-1)  # (B, 3)

#         stacked   = torch.stack([z_gene, z_cpg, z_mirna], dim=1)      # (B, 3, H)
#         fused_gat = (stacked * patient_gate.unsqueeze(-1)).sum(dim=1)  # (B, H)

#         # ── Shortcut path ─────────────────────────────────────────────
#         x_raw          = torch.cat(
#             [batch["gene"], batch["meth"], batch["mirna"]], dim=-1
#         )                                          # (B, F_gene+F_meth+F_mirna)
#         fused_shortcut = self.shortcut(x_raw)      # (B, H)

#         # ── Residual mix ──────────────────────────────────────────────
#         alpha = torch.sigmoid(self.fusion_alpha)   # scalar trong (0, 1)
#         fused = alpha * fused_gat + (1.0 - alpha) * fused_shortcut  # (B, H)

#         # ── Classification ────────────────────────────────────────────
#         logits = self.classifier(fused)

#         if return_interpretability:
#             return logits, None, {
#                 "patient":      patient_gate,       # (B, 3) — per-patient gate
#                 "fusion_alpha": alpha.item(),        # scalar — GAT vs shortcut ratio
#             }
#         return logits

#     def compute_loss(
#         self, logits: torch.Tensor, labels: torch.Tensor
#     ) -> torch.Tensor:
#         if self.loss_name == "cross_entropy":
#             loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
#         else:
#             loss_cls = self.focal_loss(logits, labels)

#         loss_frob = frobenius_regularization_loss(
#             self.modality_gate, self.lambda2, param_prefix="weight"
#         )
#         return loss_cls + loss_frob

"""
model.py -- GIAC model: Gated Fusion + Shortcut path.

Phase 20 change -- Fix gate collapse detected in Phase 19:
  Problem: LayerNorm(z_gene, z_cpg, z_mirna) normalizes all 3 embeddings to
  the same mean/scale, so the gate MLP cannot distinguish modalities by
  magnitude => gate std = 0.000 in 3/5 folds (Phase 19 log).

  Fix: Add a second gate branch (gate_raw_proj) fed by raw modality summary
  statistics [mean, std, l2norm] computed BEFORE the GAT encoder and without
  LayerNorm. These stats retain real per-patient variance across modalities.

  Combined gate logits = gate_from_gat + gate_from_raw
  gate_from_gat: existing path (LayerNorm -> Linear -> GELU -> Dropout -> Linear)
  gate_from_raw: new path (Linear(9,16) -> GELU -> Linear(16,3)), no LayerNorm
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from entmax import entmax15, sparsemax

from src.models.gat_encoder import MultiOmicGATModule
from src.models.classifier import (
    FocalLoss,
    SubtypeClassifier,
    frobenius_regularization_loss,
)


def _raw_modality_stats(x: torch.Tensor) -> torch.Tensor:
    """Compute [mean, std, l2norm/sqrt(F)] for one modality batch.

    Bypasses LayerNorm entirely, preserving per-patient variance that
    LayerNorm erases in the GAT embedding path.

    Args:
        x: (B, F) standardized feature tensor for one modality.
    Returns:
        (B, 3) tensor.
    """
    mean = x.mean(dim=1, keepdim=True)
    std  = x.std(dim=1, keepdim=True)
    l2   = x.norm(dim=1, keepdim=True) / (x.shape[1] ** 0.5)
    return torch.cat([mean, std, l2], dim=1)


class GIACModel(nn.Module):

    def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
        super().__init__()

        hidden_dim   = cfg_model["hidden_dim"]
        num_classes  = cfg_model["num_classes"]
        gate_dropout = cfg_model.get("gate_dropout", cfg_model["classifier_dropout"])

        # Module 1: GAT Encoder
        self.gat_module = MultiOmicGATModule(
            dims       = dims,
            hidden_dim = hidden_dim,
            n_heads    = cfg_model["gat_heads"],
            n_layers   = cfg_model["gat_layers"],
            dropout    = cfg_model["gat_dropout"],
        )

        # Module 2a: Gate from GAT embeddings (with LayerNorm)
        self.modality_gate = nn.Sequential(
            nn.LayerNorm(hidden_dim * 3),
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.GELU(),
            nn.Dropout(gate_dropout),
            nn.Linear(hidden_dim, 3),
        )
        with torch.no_grad():
            self.modality_gate[-1].bias[0] += 0.0   # gene
            self.modality_gate[-1].bias[1] += 0.3   # meth (ablation prior)
            self.modality_gate[-1].bias[2] += 0.1   # mirna

        # Module 2b: Gate from raw modality stats (NEW - no LayerNorm)
        # 9 = 3 modalities x 3 stats (mean, std, l2norm)
        self.gate_raw_proj = nn.Sequential(
            nn.Linear(9, 16),
            nn.GELU(),
            nn.Linear(16, 3),
        )

        # Module 3: Shortcut path
        raw_dim = dims["gene"] + dims["meth"] + dims["mirna"]
        self.shortcut = nn.Sequential(
            nn.Linear(raw_dim, hidden_dim * 2),
            nn.GELU(),
            nn.Dropout(gate_dropout),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LayerNorm(hidden_dim),
        )

        # fusion_alpha: init=-1.0 -> sigmoid~0.27, shortcut-first
        self.fusion_alpha = nn.Parameter(torch.tensor(-1.0))

        # Module 4: Classifier
        self.classifier = SubtypeClassifier(
            hidden_dim  = hidden_dim,
            final_dim   = cfg_model["final_dim"],
            num_classes = num_classes,
            dropout     = cfg_model["classifier_dropout"],
        )

        # Loss config
        self.loss_name = cfg_train.get("loss_name", "focal").lower()
        self.register_buffer(
            "class_weights", torch.ones(num_classes, dtype=torch.float32)
        )
        self.focal_loss = FocalLoss(
            gamma           = cfg_train["focal_gamma"],
            alpha           = cfg_train["focal_alpha"],
            num_classes     = num_classes,
            label_smoothing = cfg_train.get("label_smoothing", 0.0),
        )
        self.lambda2         = cfg_train["lambda_frobenius"]
        self.lambda_entropy  = cfg_train.get("lambda_entropy", 0.0)
        self.sparsemax_alpha = cfg_model.get("sparsemax_alpha", 1.5)

    def set_class_weights(self, class_weights: torch.Tensor):
        normalized = class_weights / class_weights.mean().clamp_min(1e-8)
        self.class_weights.copy_(normalized.to(self.class_weights.device))
        self.focal_loss.set_alpha(self.class_weights)

    def forward(self, batch: dict, graph: HeteroData, return_interpretability: bool = False):
        # GAT path
        z_gene, z_cpg, z_mirna = self.gat_module(batch, graph)

        # Gate path A: from GAT embeddings (subject to LayerNorm collapse)
        gate_from_gat = self.modality_gate(
            torch.cat([z_gene, z_cpg, z_mirna], dim=-1)
        )  # (B, 3)

        # Gate path B: from raw modality statistics (bypasses LayerNorm)
        raw_stats = torch.cat([
            _raw_modality_stats(batch["gene"]),
            _raw_modality_stats(batch["meth"]),
            _raw_modality_stats(batch["mirna"]),
        ], dim=1)  # (B, 9)
        gate_from_raw = self.gate_raw_proj(raw_stats)  # (B, 3)

        # Combined gate logits - additive, both paths contribute
        gate_logits = gate_from_gat + gate_from_raw  # (B, 3)

        if self.sparsemax_alpha == 1.0:
            patient_gate = F.softmax(gate_logits, dim=-1)
        elif self.sparsemax_alpha == 1.5:
            patient_gate = entmax15(gate_logits, dim=-1)
        else:
            patient_gate = sparsemax(gate_logits, dim=-1)

        stacked   = torch.stack([z_gene, z_cpg, z_mirna], dim=1)       # (B, 3, H)
        fused_gat = (stacked * patient_gate.unsqueeze(-1)).sum(dim=1)   # (B, H)

        # Shortcut path
        x_raw          = torch.cat([batch["gene"], batch["meth"], batch["mirna"]], dim=-1)
        fused_shortcut = self.shortcut(x_raw)

        # Residual mix
        alpha = torch.sigmoid(self.fusion_alpha)
        fused = alpha * fused_gat + (1.0 - alpha) * fused_shortcut

        logits = self.classifier(fused)

        if return_interpretability:
            return logits, None, {
                "patient":      patient_gate,
                "fusion_alpha": alpha.item(),
            }

        return logits, patient_gate

    def compute_loss(self, logits: torch.Tensor, labels: torch.Tensor,
                     patient_gate: torch.Tensor = None) -> torch.Tensor:
        if self.loss_name == "cross_entropy":
            loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
        else:
            loss_cls = self.focal_loss(logits, labels)

        loss_frob = frobenius_regularization_loss(
            self.modality_gate, self.lambda2, param_prefix="weight"
        )

        if patient_gate is not None and self.lambda_entropy > 0:
            entropy = -(patient_gate * (patient_gate + 1e-8).log()).sum(dim=-1).mean()
            loss_entropy = self.lambda_entropy * entropy
        else:
            loss_entropy = 0.0

        return loss_cls + loss_frob + loss_entropy