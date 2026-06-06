"""
model_v2.py
-----------
GIACModelV2 — GAT cá thể hoá (patient-conditioned), GIỮ NGUYÊN GAT (đúng tên đề tài).

Mục đích: inject dữ liệu sinh học thực tế của bệnh nhân vào node features TRƯỚC GAT
(xem gat_encoder_v2.py) → embedding cá thể hoá, không phí dữ liệu sinh học.

Khác v2 cũ: dùng LẠI ModalityCrossAttention của v1 (fusion modality GLOBAL) thay vì
fusion per-patient — vì fusion per-patient từng làm SỤP nhánh miRNA (w→0.025). Ở đây
chỉ thay ENCODER (cá thể hoá), giữ phần cross-attention/fusion như v1 đã chạy tốt →
cô lập đúng thứ cần test + giữ multi-omic cân bằng.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from src.model import ModalityCrossAttention   # tái dùng cross-attention v1
from src.models.gat_encoder_v2 import MultiOmicGATModuleV2
from src.models.classifier import FocalLoss, SubtypeClassifier, SupConLoss, frobenius_regularization_loss


class GIACModelV2(nn.Module):

    def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
        super().__init__()
        H           = cfg_model["hidden_dim"]
        num_classes = cfg_model["num_classes"]
        topk        = cfg_model.get("topk_seq", 32)

        self.gat = MultiOmicGATModuleV2(
            dims       = dims,
            hidden_dim = H,
            n_heads    = cfg_model["gat_heads"],
            n_layers   = cfg_model["gat_layers"],
            dropout    = cfg_model.get("gat_dropout", 0.3),
            topk_seq   = topk,
            gat_chunk  = cfg_model.get("gat_chunk", 4),
        )
        self.cross_attn = ModalityCrossAttention(
            hidden_dim = H,
            n_heads    = cfg_model.get("ca_heads", 4),
            dropout    = cfg_model.get("ca_dropout", 0.2),
            alpha      = cfg_model.get("sparsemax_alpha", 1.5),
        )
        self.classifier = SubtypeClassifier(
            hidden_dim  = H,
            final_dim   = cfg_model["final_dim"],
            num_classes = num_classes,
            dropout     = cfg_model.get("classifier_dropout", 0.5),
        )

        self.loss_name = cfg_train.get("loss_name", "focal").lower()
        self.register_buffer("class_weights", torch.ones(num_classes, dtype=torch.float32))
        self.focal_loss = FocalLoss(
            gamma           = cfg_train["focal_gamma"],
            alpha           = cfg_train["focal_alpha"],
            num_classes     = num_classes,
            label_smoothing = cfg_train.get("label_smoothing", 0.0),
        )
        self.lambda_frob   = cfg_train.get("lambda_frobenius", 0.01)
        self.lambda_supcon = cfg_train.get("lambda_supcon", 0.0)
        if self.lambda_supcon > 0.0:
            self.supcon_loss = SupConLoss(
                temperature=cfg_train.get("supcon_temperature", 0.07)
            )

    def set_class_weights(self, w):
        norm = w / w.mean().clamp_min(1e-8)
        self.class_weights.copy_(norm.to(self.class_weights.device))
        self.focal_loss.set_alpha(self.class_weights)

    def forward(self, batch, graph, return_interpretability=False, return_embeddings=False):
        z_gene, z_cpg_seq, z_mirna_seq = self.gat(batch, graph)
        fused, attn_info = self.cross_attn(z_gene, z_cpg_seq, z_mirna_seq, return_attn=True)
        logits = self.classifier(fused)

        if return_interpretability:
            return logits, None, attn_info
        if return_embeddings:
            return logits, fused, attn_info
        return logits, attn_info

    def compute_loss(self, logits, labels, attn_info=None, embeddings=None):
        if self.loss_name == "cross_entropy":
            loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
        else:
            loss_cls = self.focal_loss(logits, labels)
        loss_frob = frobenius_regularization_loss(
            self.cross_attn, self.lambda_frob, param_prefix="W_"
        )
        loss = loss_cls + loss_frob
        if embeddings is not None and self.lambda_supcon > 0.0:
            loss = loss + self.lambda_supcon * self.supcon_loss(embeddings, labels)
        return loss
