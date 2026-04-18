# 📋 GIAC Multi-Omics Experiment Log

> **Purpose**: Tài liệu hóa toàn bộ quá trình thử nghiệm để AI khác (hoặc bản thân sau này) có thể tiếp tục mà không bị mất context.
> 
> **Dataset**: GIAC cancer subtype classification — 917 patients, 5 classes (CIN=624, MSI=136, GS=108, EBV=30, HM-SNV=19)
>
> **Target**: Accuracy ≥ 85%, Macro F1 ≥ 85%
>
> **Current Best**: Acc=0.846, Macro F1=0.738 (Phase F)

---

## 🗂️ Tóm tắt kiến trúc hiện tại (Phase F)

```
Multi-omics input (gene: 19930, meth: 23111, mirna: 1881)
        │
        ▼ ANOVA Feature Selection (supervised, on train only)
    gene: top 3000, meth: top 3000, mirna: top 1000
        │
        ▼ Heterogeneous Graph (PPI + emQTL + miRTarBase)
        │
        ▼ MultiOmicGATModule (4 heads, 2 layers, hidden=128)
        │
    z_gene (B,128) | z_meth (B,128) | z_mirna (B,128)
        │
        ▼ Gated Modality Fusion MLP
    concat → LayerNorm → Linear(384,128) → GELU → Dropout(0.5) → Linear(128,3) → Softmax
    = patient_gate (B, 3)  ← per-patient weight
        │
        ▼ Weighted Sum: fused = Σ gate_i * z_i
        │
        ▼ SubtypeClassifier: Linear(128,64) → ReLU → Dropout → Linear(64,5)
        │
        ▼ 5-class logits
```

**Key files**:
- `src/model.py` — GIACModel (Gated Fusion)
- `src/models/gat_encoder.py` — MultiOmicGATModule
- `src/data/dataset.py` — ANOVA feature selection + CV folds
- `train.py` — main training loop, 5-fold CV
- `ablation.py` — 5-fold modality ablation study
- `configs/config.yaml` — all hyperparameters

---

## 📅 Lịch sử thay đổi (Experiment Timeline)

### Phase A — Baseline (Old cross-attention model)
**Model params**: 1,583,723

**Architecture**: GAT Encoder → SparseMultiheadCrossAttention + PatientSparseAttention (Sparsemax) → hybrid blend → Classifier

**Config (Phase A)**:
```yaml
feature_selection_method: "variance"
scheduler: cosine
weight_decay: 5e-3
patience: 20
focal_gamma: 2.0
label_smoothing: 0.0
```

**Results (5-fold CV)**:
| Metric | Mean | Std |
|---|---|---|
| Accuracy | 0.830 | 0.018 |
| Macro F1 | 0.698 | 0.052 |

**Per-class issues**: HM-SNV F1 = 0.00 ở 2/5 folds (chỉ 19 samples toàn dataset)

**Findings từ ablation**:
- `meth_only`: F1=0.643 (mạnh nhất)
- `gene_only`: F1=0.605
- `mirna_only`: F1=0.391 (nhiễu)
- `all`: F1=0.531 (tệ nhất!) → **Destructive Fusion**: cross-attention phá hoại signal

---

### Phase B — Old model + New config (ANOVA + OneCycleLR)
**Model params**: 1,583,724 (VẪN LÀ OLD MODEL — user chạy cached code trên Kaggle)

**Changes từ Phase A**:
- `feature_selection_method`: variance → **anova** (supervised, fit on train only)
- `scheduler`: cosine → **onecycle** (LR = 1e-4 to 5e-4)
- `weight_decay`: 5e-3 → **5e-2**
- `patience`: 20 (giữ)
- `focal_gamma`: 2.0 (giữ)
- `label_smoothing`: 0.0 → **0.05**

**Results**:
| Metric | Mean | Std |
|---|---|---|
| Accuracy | **0.852** | 0.022 |
| Macro F1 | **0.732** | 0.020 |

**Gate stats (PatientSparseAttention)**:
- meth: 0.48–0.57 ✅ (đúng thứ tự ablation)
- gene: 0.36–0.42
- mirna: 0.06–0.20 ✅ (bị suppress đúng)

**Insight**: Cải thiện đến từ ANOVA + OneCycleLR, KHÔNG phải từ architecture change.

---

### B1 — Architecture: Gated Modality Fusion
**[CODE CHANGE] src/model.py**

**Lý do**: Ablation chứng minh cross-attention phá hoại (all < meth_only). Thay bằng Gated Fusion đơn giản hơn.

**Thay đổi**:
- XÓA: `SparseMultiheadCrossAttention`, `PatientSparseAttention`
- THÊM: `modality_gate` MLP (LayerNorm → Linear → GELU → Dropout → Linear → Softmax)
- XÓA: `fusion_mode`, `learnable_blend`, `fixed_blend_alpha` config

**Note**: Model params giảm từ 1,583,723 → **1,489,800** (bỏ cross-attention heads)

---

### Phase C — New model + tighter regularization (FAILED)
**Model params**: 1,489,800 (first real run with new gated model)

**Changes**:
- `patience`: 20 → **10** (too short)
- `label_smoothing`: 0.05 → **0.10** (too high)
- `focal_gamma`: 2.0 → **3.0**
- `weight_decay`: giữ **5e-2** (ĐÂY LÀ VẤN ĐỀ CHÍNH)

**Results**:
| Metric | Mean | Std |
|---|---|---|
| Accuracy | 0.822 | 0.042 |
| Macro F1 | 0.711 | 0.042 |

**Root cause thất bại**: `weight_decay=5e-2` + `frobenius=0.01` kéo gate MLP weights về 0 → softmax của zeros = 1/3, 1/3, 1/3 → gate uniform → model tương đương trung bình 3 modalities → tệ hơn dùng meth alone.

**Gate stats**: gene≈0.35, meth≈0.32, mirna≈0.32 (ALL UNIFORM, std=0.02–0.07) ❌

---

### Phase D — New model + WD fix
**Changes từ Phase C**:
- `weight_decay`: 5e-2 → **1e-2** (KEY FIX)
- `patience`: 10 → **15** (compromise)
- `label_smoothing`: 0.10 → **0.05** (revert)
- `focal_gamma`: **3.0** (giữ)

**Results**:
| Metric | Mean | Std |
|---|---|---|
| Accuracy | 0.841 | 0.040 |
| Macro F1 | 0.725 | 0.028 |

**Gate stats**: gene≈0.37, meth≈0.30–0.32, mirna≈0.30–0.32 (vẫn còn khá uniform, std=0.04–0.15)

**Nhận xét**: Tốt hơn Phase C nhưng gate vẫn chưa học đúng thứ tự (meth nên cao hơn gene theo ablation).

---

### Phase E — Gate bias init + Frobenius=0 (CATASTROPHIC FAILURE)
**[CODE CHANGE] src/model.py** + config

**Lý do (SAI)**: Thử init gate bias để encode ablation prior (meth > gene > mirna). Đồng thời tắt Frobenius reg vì nghĩ nó cản gate học extreme weights.

**Changes**:
```python
# Thêm vào model.py (SAI — đã bị revert)
with torch.no_grad():
    self.modality_gate[-1].bias.data = torch.tensor([-0.5, 0.5, -1.5])
```
```yaml
lambda_frobenius: 0.01 → 0.00  # SAI — đã bị revert
```

**Results**:
| Metric | Mean | Std |
|---|---|---|
| Accuracy | **0.786** | 0.023 |
| Macro F1 | **0.647** | 0.037 |

**Root cause thất bại**: Bỏ Frobenius → gate weights không bị penalize → gate collapse về extreme values (std=0.38–0.44) → highly volatile, inconsistent selection → training instability → test F1 drop mạnh.

**Gate stats**: gene≈0.19–0.50, meth≈0.33–0.46, mirna≈0.14–0.35 (high variance, unstable) ❌

---

### Phase F — Phase D config (= revert Phase E, BEST RESULT)
**Model params**: 1,489,800

**Config hiện tại** (đây là config ĐANG DÙNG):
```yaml
preprocessing:
  gene_top_k: 3000
  meth_top_k: 3000
  mirna_top_k: 1000
  feature_selection_method: "anova"

model:
  hidden_dim: 128
  gat_heads: 4
  gat_layers: 2
  gat_dropout: 0.5
  gate_dropout: 0.5
  classifier_dropout: 0.5
  num_classes: 5
  final_dim: 64

training:
  epochs: 150
  batch_size: 32
  learning_rate: 1e-4
  max_learning_rate: 5e-4
  scheduler: "onecycle"
  weight_decay: 1e-2
  focal_gamma: 3.0
  focal_alpha: 1.0
  label_smoothing: 0.05
  lambda_modality: 0.00
  lambda_frobenius: 0.01
  patience: 15
  seed: 42
  loss_name: "focal"
```

**Results (BEST)**:
| Metric | Mean | Std |
|---|---|---|
| Accuracy | **0.846** | 0.031 |
| Macro F1 | **0.738** | 0.038 |

**Per-fold**:
| Fold | Acc | Macro F1 | HM-SNV F1 | GS F1 |
|---|---|---|---|---|
| 1 | 0.859 | **0.806** 🏆 | 0.667 | 0.692 |
| 2 | 0.891 | 0.745 | 0.333 | 0.816 |
| 3 | 0.831 | 0.692 | 0.286 | 0.522 |
| 4 | 0.798 | 0.716 | 0.250 | 0.613 |
| 5 | 0.853 | 0.730 | 0.333 | 0.512 |

---

## 🧠 Bài học / Key Insights

### 1. Destructive Fusion không phải lý do đơn giản
Ablation 5-fold chứng minh `all < meth_only`, nhưng trong full training, cross-attention + Sparsemax (PatientSparseAttention) lại tạo ra gate ổn định và đúng hướng (meth=0.48–0.57). Gated MLP mới thì gate uniform hơn (std=0.04–0.15 vs 0.41–0.45 của Sparsemax).

### 2. Weight Decay ảnh hưởng gate mạnh hơn tưởng
WD=5e-2 làm gate MLP weights → 0 → softmax của zeros = uniform (1/3, 1/3, 1/3) → mất hoàn toàn khả năng phân biệt modality. WD=1e-2 ổn hơn nhưng vẫn chưa đủ để gate học meth > gene.

### 3. Frobenius regularization là cần thiết cho stability
Tắt Frobenius → gate volatile (std=0.38–0.44 extreme) → training instability. Frobenius=0.01 là balance tốt.

### 4. HM-SNV là bottleneck không thể vượt qua với dataset này
- 19 samples HM-SNV tổng cộng → 3–4 per test fold
- Macro F1 chia đều cho 5 classes → HM-SNV tác động 20% macro F1
- Với 4 test samples: 1 misclassification = F1 giảm 0.25
- **Không thể đạt 85% Macro F1 ổn định mà không có thêm HM-SNV data**

### 5. Variance giữa folds là do data composition, không phải training instability
Fold 3, 4 luôn yếu nhất vì các HM-SNV samples khó nhất rơi vào đó (phân phối bởi StratifiedKFold với seed=42).

---

## 🚧 Khoảng cách còn lại

**Target**: Acc=85%, F1=85%  
**Current**: Acc=84.6% ✅ (gần đạt), F1=73.8% ❌ (gap 11.2%)

**Gap chủ yếu do**:
1. **HM-SNV**: F1=0.25–0.67 (rất noisy do ít samples)
2. **GS class**: F1=0.51–0.82 (inconsistent)

---

## 🔮 Hướng tiếp cận chưa thử

### Ưu tiên cao (không cần thêm data)
1. **Test-time ensemble**: Voter kết quả 5 fold models (majority vote hoặc soft vote trên probabilities). Không cần train thêm. Fold 1 (F1=0.806) + Fold 2 (0.745) nếu ensemble tốt có thể push F1 lên.

2. **Replace Softmax bằng Sparsemax trong gate**: Phase B old model dùng Sparsemax cho PatientSparseAttention và đạt gate std=0.41–0.45 (bimodal, quyết định rõ ràng). Thay `F.softmax` bằng `sparsemax` (module đã exists trong `src/models/sparse_attention.py`) có thể giúp gate phân biệt modality tốt hơn.

3. **Meth-only model cuối cùng**: Nếu gated model không thể vượt meth_only (F1=0.643 ablation trên 1-fold), thì có thể chạy meth_only với full pipeline (5-fold CV, ANOVA, OneCycleLR) để so sánh.

### Ưu tiên thấp (rủi ro cao)
4. **Mixup augmentation cho GS class**: GS (108 samples, F1=0.51–0.82) là class thứ hai yếu nhất. Mixup không tạo ngoài distribution.

5. **SMOTE trên feature space**: Đã thất bại trước đó với raw features. Có thể thử trên GAT embeddings (z_gene, z_meth) sau khi train.

---

## 📁 Files quan trọng

| File | Mô tả |
|---|---|
| `src/model.py` | GIACModel — Gated Fusion architecture |
| `src/models/gat_encoder.py` | MultiOmicGATModule |
| `src/models/sparse_attention.py` | SparseMultiheadCrossAttention, PatientSparseAttention (không dùng nữa nhưng GIỮ LẠI để không cần xóa) |
| `src/models/classifier.py` | FocalLoss, SubtypeClassifier |
| `src/data/dataset.py` | ANOVA feature selection, StratifiedKFold CV |
| `src/data/graph_builder.py` | HeteroGraph builder (PPI + emQTL + miRTarBase) |
| `train.py` | Main training loop + 5-fold CV |
| `ablation.py` | Modality ablation study |
| `evaluate.py` | Evaluation + patient gate statistics |
| `configs/config.yaml` | All hyperparameters |
| `TestPhaseA.md` | Phase A output (old model baseline) |
| `TestPhaseB.md` | Phase B–E outputs |
| `TestPhaseD.md` | Phase D output |
| `TestPhaseE.md` | Phase E output (catastrophic failure) |
| `TestPhaseNew.md` | Phase F output (current best) |

---

## ⚙️ Cách chạy

```bash
# Full 5-fold CV training
python train.py --config configs/config.yaml

# Ablation study (xác nhận fusion đúng hướng)
python ablation.py --config configs/config.yaml

# Evaluate checkpoint cụ thể
python evaluate.py --config configs/config.yaml \
    --checkpoint /kaggle/working/checkpoints/best_model_fold_1.pt
```

**Verification sau mỗi run**:
1. `meth gate mean > 0.35` → gate đang học đúng (meth được ưu tiên)
2. `all > meth_only` trong ablation → fusion đang có lợi
3. Fold 3, 4 F1 < Fold 1, 2, 5 → bình thường (data composition effect)
