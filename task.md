# Task Tracker — GIAC Phase A Diagnostics

## Phase A: Diagnostic

- `[x]` **A1**: Classification Report + Confusion Matrix per Fold
  - `[x]` utils.py: thêm `print_classification_report()` + `save_confusion_matrix_csv()`
  - `[x]` train.py: gọi diagnostic functions sau test evaluation
- `[x]` **A2**: Modality Ablation Study
  - `[x]` Tạo `ablation.py` — chạy 6 modality configs trên fold 1
- `[x]` **A3**: Inspect Patient Gate Distribution
  - `[x]` train.py: thêm `collect_gate_stats()` + log stats sau test eval

## Phase B: Optimization (chờ kết quả Phase A)

- `[ ]` B1: Supervised Feature Selection (ANOVA/MI)
- `[ ]` B2: Fix Modality Fusion
- `[ ]` B3: Regularization & Training
