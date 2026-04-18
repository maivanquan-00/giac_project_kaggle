"""
model.py
--------
Full GIAC model with graph encoder, sparse fusion, lightweight feature
interpretability, and imbalance-aware classification loss.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import HeteroData

from src.models.gat_encoder import MultiOmicGATModule
from src.models.sparse_attention import (
    PatientSparseAttention,
    SparseMultiheadCrossAttention,
)
from src.models.classifier import (
    FocalLoss,
    SubtypeClassifier,
    frobenius_regularization_loss,
    modality_regularization_loss,
)


class GIACModel(nn.Module):
    def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
        super().__init__()

        hidden_dim = cfg_model["hidden_dim"]
        num_classes = cfg_model["num_classes"]

        self.gat_module = MultiOmicGATModule(
            dims=dims,
            hidden_dim=hidden_dim,
            n_heads=cfg_model["gat_heads"],
            n_layers=cfg_model["gat_layers"],
            dropout=cfg_model["gat_dropout"],
        )

        self.sparse_cross_attn = SparseMultiheadCrossAttention(
            hidden_dim=hidden_dim,
            n_heads=cfg_model["cross_attn_heads"],
            dropout=cfg_model["cross_attn_dropout"],
            sparsemax_alpha=cfg_model["sparsemax_alpha"],
            modality_temperature=cfg_model.get("modality_temperature", 1.0),
        )

        self.patient_attn = PatientSparseAttention(
            dims=dims,
            hidden_dim=hidden_dim,
            alpha=cfg_model["sparsemax_alpha"],
        )

        self.classifier = SubtypeClassifier(
            hidden_dim=hidden_dim,
            final_dim=cfg_model["final_dim"],
            num_classes=num_classes,
            dropout=cfg_model["classifier_dropout"],
        )

        self.modality_gate = nn.Sequential(
            nn.LayerNorm(hidden_dim * 3),
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.GELU(),
            nn.Dropout(cfg_model["classifier_dropout"]),
            nn.Linear(hidden_dim, 3),
        )

        self.fusion_mode = cfg_model.get("fusion_mode", "hybrid")
        self.learnable_blend = bool(cfg_model.get("learnable_blend", False))
        fixed_blend_alpha = float(cfg_model.get("fixed_blend_alpha", 0.5))
        fixed_blend_alpha = min(max(fixed_blend_alpha, 0.0), 1.0)
        if self.learnable_blend:
            init_logit = torch.logit(torch.tensor(fixed_blend_alpha).clamp(1e-4, 1 - 1e-4))
            self.fusion_logit = nn.Parameter(init_logit)
        else:
            self.register_buffer("fixed_blend_alpha", torch.tensor(fixed_blend_alpha))

        self.loss_name = cfg_train.get("loss_name", "focal").lower()
        self.register_buffer("class_weights", torch.ones(num_classes, dtype=torch.float32))
        self.focal_loss = FocalLoss(
            gamma=cfg_train["focal_gamma"],
            alpha=cfg_train["focal_alpha"],
            num_classes=num_classes,
            label_smoothing=cfg_train.get("label_smoothing", 0.0),
        )
        self.lambda1 = cfg_train["lambda_modality"]
        self.lambda2 = cfg_train["lambda_frobenius"]

    def set_class_weights(self, class_weights: torch.Tensor):
        normalized = class_weights / class_weights.mean().clamp_min(1e-8)
        self.class_weights.copy_(normalized.to(self.class_weights.device))
        self.focal_loss.set_alpha(self.class_weights)

    def forward(self, batch: dict, graph: HeteroData, return_interpretability: bool = False):
        z_gene, z_cpg, z_mirna = self.gat_module(batch, graph)

        if return_interpretability:
            cross_fused, _, global_modality_weights = self.sparse_cross_attn(
                z_gene, z_cpg, z_mirna, return_sparse_weights=True
            )
        else:
            cross_fused = self.sparse_cross_attn(z_gene, z_cpg, z_mirna)
            global_modality_weights = None

        patient_sparse = self.patient_attn(batch)

        stacked_modalities = torch.stack([z_gene, z_cpg, z_mirna], dim=1)
        patient_gate = F.softmax(
            self.modality_gate(torch.cat([z_gene, z_cpg, z_mirna], dim=-1)),
            dim=-1,
        )
        patient_fused = (stacked_modalities * patient_gate.unsqueeze(-1)).sum(dim=1)

        if self.fusion_mode == "patient_only":
            fused = patient_fused
        elif self.fusion_mode == "cross_only":
            fused = cross_fused
        else:
            if self.learnable_blend:
                blend_alpha = torch.sigmoid(self.fusion_logit)
            else:
                blend_alpha = self.fixed_blend_alpha
            fused = blend_alpha * cross_fused + (1.0 - blend_alpha) * patient_fused

        logits = self.classifier(fused)

        if return_interpretability:
            return logits, patient_sparse, {
                "global": global_modality_weights,
                "patient": patient_gate,
            }
        return logits

    def compute_loss(self, logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        if self.loss_name == "cross_entropy":
            loss_cls = F.cross_entropy(logits, labels, weight=self.class_weights)
        else:
            loss_cls = self.focal_loss(logits, labels)

        mod_w = self.sparse_cross_attn.modality_weights
        loss_mod = modality_regularization_loss(mod_w, self.lambda1)
        loss_frob = frobenius_regularization_loss(
            self.sparse_cross_attn, self.lambda2, param_prefix="W_"
        )
        return loss_cls + loss_mod + loss_frob
