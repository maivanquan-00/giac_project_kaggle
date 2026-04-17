"""
classifier.py
-------------
Module 3 — Focal Loss Classifier + Interpretability output

Giữ nguyên ý tưởng từ MoXGATE (Focal Loss để xử lý class imbalance)
nhưng thêm:
  - Label smoothing
  - Modality weight regularization loss (như paper gốc)
  - Frobenius norm regularization
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


# ─────────────────────────────────────────────
#  Focal Loss
# ─────────────────────────────────────────────
class FocalLoss(nn.Module):
    """
    Focal Loss cho class imbalance.
    
    L = -sum_i [ alpha_i * (1 - p_i)^gamma * y_i * log(p_i) ]
    
    gamma=2 (paper MoXGATE): tập trung vào hard examples (minority subtypes)
    alpha: class-specific weights; dùng 1.0 uniform hoặc list per class
    
    Reference: Lin et al., "Focal Loss for Dense Object Detection", CVPR 2017
    """

    def __init__(self, gamma: float = 2.0, alpha=1.0, num_classes: int = 5):
        super().__init__()
        self.gamma = gamma

        if isinstance(alpha, (int, float)):
            alpha_tensor = torch.ones(num_classes, dtype=torch.float32) * alpha
        else:
            alpha_tensor = torch.tensor(alpha, dtype=torch.float32)
        self.register_buffer("alpha", alpha_tensor)

    def set_alpha(self, alpha: torch.Tensor):
        self.alpha.copy_(alpha.to(self.alpha.device, dtype=self.alpha.dtype))

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        logits  : (B, num_classes) — raw output từ classifier
        targets : (B,) — class indices 0..4
        """
        # Tính cross-entropy per sample
        log_probs = F.log_softmax(logits, dim=-1)   # (B, C)
        probs     = log_probs.exp()                  # (B, C)

        # Lấy log_prob và prob của class đúng
        log_pt = log_probs.gather(1, targets.unsqueeze(1)).squeeze(1)  # (B,)
        pt     = probs.gather(1, targets.unsqueeze(1)).squeeze(1)      # (B,)

        # Alpha per sample
        alpha_t = self.alpha[targets]  # (B,)

        # Focal weight
        focal_weight = (1.0 - pt) ** self.gamma  # (B,)

        loss = -alpha_t * focal_weight * log_pt   # (B,)
        return loss.mean()


# ─────────────────────────────────────────────
#  Classifier head
# ─────────────────────────────────────────────
class SubtypeClassifier(nn.Module):
    """
    Classifier đơn giản sau khi đã có fused representation.
    
    Input:  (B, hidden_dim)
    Output: (B, num_classes) logits
    """

    def __init__(
        self,
        hidden_dim:  int,
        final_dim:   int,       # 128 như MoXGATE
        num_classes: int,       # 5
        dropout:     float,
    ):
        super().__init__()

        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, final_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(final_dim, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc(x)  # (B, num_classes)


# ─────────────────────────────────────────────
#  Regularization losses (như MoXGATE eq. 14)
# ─────────────────────────────────────────────
def modality_regularization_loss(
    modality_weights: torch.Tensor,  # (3,) — output từ SparseAttention.modality_weights
    lambda1: float,
) -> torch.Tensor:
    """
    L_reg1 = lambda1 * ||w - 1/3||^2
    Khuyến khích modality weights không lệch quá xa nhau.
    """
    uniform = torch.ones_like(modality_weights) / 3.0
    return lambda1 * ((modality_weights - uniform) ** 2).sum()


def frobenius_regularization_loss(
    model: nn.Module,
    lambda2: float,
    param_prefix: str = "W_",  # chỉ regularize các weight matrix
) -> torch.Tensor:
    """
    L_reg2 = lambda2 * ||W_c||_F^2
    Frobenius norm regularization trên weight matrices của cross-attention.
    """
    reg = None
    for name, param in model.named_parameters():
        if param_prefix in name and param.requires_grad:
            term = param.norm("fro") ** 2
            reg = term if reg is None else reg + term
    if reg is None:
        first_param = next(model.parameters(), None)
        if first_param is None:
            return torch.tensor(0.0)
        return first_param.new_tensor(0.0)
    return lambda2 * reg
