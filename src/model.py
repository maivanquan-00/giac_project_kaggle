"""
model.py
--------
Full model: ghép 3 module lại thành một nn.Module hoàn chỉnh.

Flow tóm tắt:
  [Gene, Meth, miRNA features]
        ↓  Module 1
  [GAT Encoders] → z_gene, z_cpg, z_mirna  (B, D)
        ↓  Module 2
  [Sparse Cross-Attention] → fused  (B, D)
     + [Patient Sparse Attention] → sparse_weights per patient
        ↓  Module 3
  [Classifier] → logits  (B, 5)
"""

import torch
import torch.nn as nn
from torch_geometric.data import HeteroData

from src.models.gat_encoder      import MultiOmicGATModule
from src.models.sparse_attention  import SparseMultiheadCrossAttention, PatientSparseAttention
from src.models.classifier        import SubtypeClassifier, FocalLoss
from src.models.classifier        import modality_regularization_loss, frobenius_regularization_loss


class GIACModel(nn.Module):
    """
    Mô hình đề xuất cải tiến MoXGATE:
      Module 1: Heterogeneous GAT Encoder
      Module 2: Sparse Cross-Attention Fusion
      Module 3: Focal Loss Classifier
    """

    def __init__(self, dims: dict, cfg_model: dict, cfg_train: dict):
        """
        dims       : {'gene': F_g, 'meth': F_m, 'mirna': F_mi}
        cfg_model  : config.yaml['model']
        cfg_train  : config.yaml['training']
        """
        super().__init__()

        D = cfg_model["hidden_dim"]

        # ── Module 1: GAT Encoder ────────────────────────────────────
        self.gat_module = MultiOmicGATModule(
            dims       = dims,
            hidden_dim = D,
            n_heads    = cfg_model["gat_heads"],
            n_layers   = cfg_model["gat_layers"],
            dropout    = cfg_model["gat_dropout"],
        )

        # ── Module 2a: Sparse Cross-Attention (modality-level) ───────
        self.sparse_cross_attn = SparseMultiheadCrossAttention(
            hidden_dim      = D,
            n_heads         = cfg_model["cross_attn_heads"],
            dropout         = cfg_model["cross_attn_dropout"],
            sparsemax_alpha = cfg_model["sparsemax_alpha"],
        )

        # ── Module 2b: Patient-level sparse feature attention ─────────
        self.patient_attn = PatientSparseAttention(
            dims       = dims,
            hidden_dim = D,
            alpha      = cfg_model["sparsemax_alpha"],
        )

        # ── Module 3: Classifier ─────────────────────────────────────
        self.classifier = SubtypeClassifier(
            hidden_dim  = D,
            final_dim   = cfg_model["final_dim"],
            num_classes = cfg_model["num_classes"],
            dropout     = cfg_model["classifier_dropout"],
        )

        # ── Loss & regularization config ─────────────────────────────
        self.focal_loss = FocalLoss(
            gamma       = cfg_train["focal_gamma"],
            alpha       = cfg_train["focal_alpha"],
            num_classes = cfg_model["num_classes"],
        )
        self.lambda1 = cfg_train["lambda_modality"]
        self.lambda2 = cfg_train["lambda_frobenius"]

    def forward(
        self,
        batch: dict,
        graph: HeteroData,
        return_interpretability: bool = False,
    ):
        """
        Parameters
        ----------
        batch  : dict {'gene': (B,Fg), 'meth': (B,Fm), 'mirna': (B,Fmi), 'label': (B,)}
        graph  : HeteroData — heterogeneous graph (topology cố định)
        return_interpretability : nếu True, trả về thêm sparse weights

        Returns
        -------
        logits : (B, num_classes)
        [optional] sparse_weights: dict per modality per patient
        [optional] modality_weights: (3,) tầm quan trọng tương đối của 3 omics
        """
        # ── Module 1 ─────────────────────────────────────────────────
        z_gene, z_cpg, z_mirna = self.gat_module(batch, graph)
        # mỗi cái: (B, D)

        # ── Module 2a: modality-level sparse fusion ──────────────────
        if return_interpretability:
            fused, attn_weights, mod_weights = self.sparse_cross_attn(
                z_gene, z_cpg, z_mirna, return_sparse_weights=True
            )
        else:
            fused = self.sparse_cross_attn(z_gene, z_cpg, z_mirna)

        # ── Module 2b: feature-level sparse attention ────────────────
        patient_sparse = self.patient_attn(batch)
        # patient_sparse: dict {'gene': (B,Fg), 'meth': (B,Fm), 'mirna': (B,Fmi)}

        # Weighted gate: scale fused với average sparse weight magnitude
        # (optional enhancement — có thể bỏ nếu muốn đơn giản hơn)
        gene_gate  = patient_sparse["gene"].mean(dim=1, keepdim=True)    # (B, 1)
        cpg_gate   = patient_sparse["meth"].mean(dim=1, keepdim=True)
        mirna_gate = patient_sparse["mirna"].mean(dim=1, keepdim=True)

        # Tăng cường fused bằng patient-specific importance
        gate_sum = gene_gate + cpg_gate + mirna_gate + 1e-8
        fused = fused * (
            gene_gate * z_gene + cpg_gate * z_cpg + mirna_gate * z_mirna
        ).sigmoid() / gate_sum

        # ── Module 3: Classification ──────────────────────────────────
        logits = self.classifier(fused)  # (B, num_classes)

        if return_interpretability:
            return logits, patient_sparse, mod_weights
        return logits

    def compute_loss(
        self,
        logits: torch.Tensor,   # (B, C)
        labels: torch.Tensor,   # (B,)
    ) -> torch.Tensor:
        """
        Tổng loss = Focal Loss + modality regularization + Frobenius regularization
        (Equation 14 trong MoXGATE paper)
        """
        loss_focal = self.focal_loss(logits, labels)

        mod_w = self.sparse_cross_attn.modality_weights
        loss_mod = modality_regularization_loss(mod_w, self.lambda1)

        loss_frob = frobenius_regularization_loss(
            self.sparse_cross_attn, self.lambda2, param_prefix="W_"
        )

        return loss_focal + loss_mod + loss_frob
