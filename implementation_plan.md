# Implementation Plan — GIAC Diagnostic-First Improvement

## Mục tiêu
Xác định chính xác bottleneck của mô hình trước khi tối ưu. Chia thành 2 phase rõ ràng:
- **Phase A**: Diagnostic — thu thập dữ liệu để ra quyết định
- **Phase B**: Optimization — áp dụng cải tiến dựa trên kết quả Phase A

---

## Phase A: Diagnostic (không thay đổi model)

### A1. Classification Report + Confusion Matrix per Fold

#### [MODIFY] [train.py](file:///d:/ĐATN/giac_project_kaggle/train.py)
- Sau khi evaluate test set mỗi fold, in `sklearn.metrics.classification_report` đầy đủ (precision/recall/f1 **per class**).
- Lưu confusion matrix dạng số tuyệt đối (không normalize) ra file `.csv` + heatmap `.png`.
- Mục tiêu: xác định class 3 & 4 đang bị misclassify sang đâu.

#### [MODIFY] [utils.py](file:///d:/ĐATN/giac_project_kaggle/src/utils.py)
- Thêm hàm `print_classification_report()` wrapper.
- Thêm hàm `save_confusion_matrix_csv()`.

---

### A2. Modality Ablation Study

#### [NEW] [ablation.py](file:///d:/ĐATN/giac_project_kaggle/ablation.py)
Script chạy 6 cấu hình trên **1 fold duy nhất** (fold 1) để so sánh nhanh:

| Config | Gene | Meth | miRNA |
|---|---|---|---|
| gene_only | ✅ | ❌ | ❌ |
| meth_only | ❌ | ✅ | ❌ |
| mirna_only | ❌ | ❌ | ✅ |
| gene+meth | ✅ | ✅ | ❌ |
| gene+mirna | ✅ | ❌ | ✅ |
| all (baseline) | ✅ | ✅ | ✅ |

Cách implement: mask modality bằng cách zero-out input features tại batch level (không cần thay đổi model architecture). Output: bảng so sánh Acc/F1 per config.

---

### A3. Inspect Patient Gate Distribution

#### [MODIFY] [train.py](file:///d:/ĐATN/giac_project_kaggle/train.py)
- Trong `eval_epoch`, khi evaluate test set, bật `return_interpretability=True`.
- Thu thập patient gate weights `(B, 3)` cho toàn bộ test set.
- Log thống kê: mean, std, min, max của mỗi cột (gene/meth/mirna gate).
- Nếu std < 0.05 cho tất cả cột → patient gate đang "chết", fusion cần viết lại.

---

## Phase B: Optimization (áp dụng sau khi có kết quả Phase A)

> [!IMPORTANT]
> Các bước dưới đây sẽ được thực hiện **tuần tự**, mỗi bước chạy 1 fold để đo impact trước khi chuyển sang bước tiếp.

### B1. Supervised Feature Selection

#### [MODIFY] [dataset.py](file:///d:/ĐATN/giac_project_kaggle/src/data/dataset.py)
- Thêm `_select_top_discriminative_features(train_X, train_y, top_k)` dùng ANOVA F-test (nhanh, ổn định) hoặc mutual information.
- Thay `_select_top_variance_features` bằng hàm mới trong `_fit_modality_preprocessor`.
- Fit trên train-only, áp dụng cho val/test — giữ nguyên pipeline đang có.

#### [MODIFY] [config.yaml](file:///d:/ĐATN/giac_project_kaggle/configs/config.yaml)
- Thêm option `feature_selection_method: "anova"` (hoặc `"variance"` để fallback).

### B2. Fix Modality Fusion

#### [MODIFY] [sparse_attention.py](file:///d:/ĐATN/giac_project_kaggle/src/models/sparse_attention.py)
- Loại bỏ `temperature = 0.1` trong property `modality_weights` → dùng `temperature = 1.0`.
- Tuỳ kết quả A3: nếu patient gate cũng "chết" → đơn giản hoá toàn bộ fusion thành **1 nhánh duy nhất** (hoặc patient-only gate hoặc cross-attention-only, bỏ cái kia).

#### [MODIFY] [model.py](file:///d:/ĐATN/giac_project_kaggle/src/model.py)
- Tùy kết quả A2 (ablation): nếu 1 modality không đóng góp → bỏ modality đó hoặc giảm weight xuống.
- Tùy kết quả A3: thay đổi tỉ lệ `0.5 * fused + 0.5 * patient_fused` → có thể chuyển sang learnable alpha hoặc bỏ 1 nhánh.

### B3. Regularization & Training

#### [MODIFY] [config.yaml](file:///d:/ĐATN/giac_project_kaggle/configs/config.yaml)
```yaml
model:
  gat_dropout: 0.5          # tăng từ 0.4
  cross_attn_dropout: 0.5   # tăng từ 0.4
  classifier_dropout: 0.6   # tăng từ 0.5

training:
  weight_decay: 5.0e-2      # tăng từ 1e-2
  lambda_modality: 0.00     # giữ 0 hoặc bỏ hẳn
```

#### [MODIFY] [classifier.py](file:///d:/ĐATN/giac_project_kaggle/src/models/classifier.py)
- Thêm label smoothing (0.1) vào FocalLoss.

#### [MODIFY] [train.py](file:///d:/ĐATN/giac_project_kaggle/train.py)
- Thay `CosineAnnealingLR` bằng `OneCycleLR` với warm-up.

---

## Thứ tự thực hiện

```
A1 (report/confusion) → A2 (ablation) → A3 (patient gate)
         ↓                    ↓                ↓
    Biết class nào yếu   Biết modality    Biết fusion
                          nào hữu ích     có hoạt động
         └────────────────────┴──────────────────┘
                              ↓
                    B1 (feature selection)
                              ↓
                    B2 (fix fusion)
                              ↓
                    B3 (regularization)
                              ↓
                    Full 5-fold CV → đánh giá
```

---

## Verification Plan

### Phase A
- Classification report phải hiển thị per-class P/R/F1 cho tất cả 5 classes.
- Ablation table phải có 6 dòng với Acc/F1 comparable.
- Patient gate stats phải có mean/std/min/max cho 3 gates.

### Phase B
- Mỗi cải tiến chạy fold 1, so sánh Val F1 với baseline (0.7933).
- Sau khi kết hợp tất cả, chạy full 5-fold CV, so sánh với baseline mean F1 (0.6812).
- Target: **F1 ≥ 0.82, Acc ≥ 0.85** trên 5-fold CV.
