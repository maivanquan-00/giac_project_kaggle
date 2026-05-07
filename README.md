# Phân loại bệnh nhân ung thư dựa trên đồ thị dị thể đa omics kết hợp GAT và Cross-Attention


---

## Tổng quan

Đồ án đề xuất kiến trúc **GIAC** (Graph-Informed Asymmetric Cross-attention) cho bài toán phân loại phân nhóm phân tử ung thư từ dữ liệu đa omics (gene expression, DNA methylation, miRNA expression). Mô hình kết hợp:

1. **Đồ thị dị thể đa omics** — mã hoá 7 loại quan hệ sinh học đã biết vào cấu trúc đồ thị;
2. **HeteroGAT encoder** — dùng GATv2Conv học embedding cho từng node trên đồ thị;
3. **Asymmetric Cross-Attention** — gene là Query, top-K CpG và miRNA là Key/Value, cho phép tích hợp tín hiệu điều tiết vào biểu diễn gene của từng bệnh nhân;
4. **Focal Loss** với class weights — xử lý mất cân bằng lớp vốn nghiêm trọng trong dữ liệu ung thư.

Khác với MoXGATE (baseline) dùng đánh giá single random split, mô hình được kiểm chứng bằng **5-fold Stratified Cross-Validation** để đảm bảo tính tin cậy thống kê.

---

## Kiến trúc mô hình

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INPUT (một bệnh nhân)                           │
│   Gene: (F_g,)    CpG/Meth: (F_m,)    miRNA: (F_mi,)                  │
│   F_g ≈ 3500      F_m ≈ 3500          F_mi = 1881                      │
└────────────────┬──────────────────────────────┬────────────────────────┘
                 │                              │
       ┌─────────▼──────────┐        ┌──────────▼──────────────┐
       │   ANOVA Top-K      │        │  Heterogeneous Graph     │
       │  Feature Selection │        │  (shared across batch)   │
       │  (per modality,    │        │  3 node types, 7 edges   │
       │   fitted on train) │        └──────────┬───────────────┘
       └─────────┬──────────┘                   │
                 │                              │
       ┌─────────▼──────────────────────────────▼───────────────┐
       │              MultiOmicGATModule (gat_encoder.py)        │
       │                                                          │
       │  node_emb: ParameterDict {gene, cpg, mirna}             │
       │         ↓  modulate by patient feature values           │
       │  Layer 1: HeteroConv (GATv2Conv × 12 edge types)        │
       │         + Residual + ELU + LayerNorm                    │
       │  Layer 2: HeteroConv (GATv2Conv × 12 edge types)        │
       │         + Residual + ELU + LayerNorm                    │
       │                                                          │
       │  Output:                                                 │
       │    z_gene:      (B, H)    — weighted mean over genes    │
       │    z_cpg_seq:   (B, K, H) — top-K CpG + pos encoding   │
       │    z_mirna_seq: (B, K, H) — top-K miRNA + pos encoding  │
       └─────────────────────────┬──────────────────────────────┘
                                 │
       ┌─────────────────────────▼──────────────────────────────┐
       │       ModalityCrossAttention (model.py)                 │
       │                                                          │
       │  Gene z_gene ──────────────────────► Query (B, H)       │
       │                                                          │
       │  z_cpg_seq ─── W_k_cpg / W_v_cpg ─► K/V (B, K, H)     │
       │    Gene attends over K=32 CpG nodes                     │
       │    Entmax15 sparse weights → interpretable               │
       │    ctx_cpg: (B, H)                                       │
       │                                                          │
       │  z_mirna_seq ── W_k_mirna / W_v_mirna ► K/V (B, K, H)  │
       │    Gene attends over K=32 miRNA nodes                   │
       │    ctx_mirna: (B, H)                                     │
       │                                                          │
       │  w = softmax(modality_logits)  — học được {cpg, mirna}  │
       │  fused = LayerNorm(W_out([w0·ctx_cpg, w1·ctx_mirna])    │
       │                + z_gene)  — residual connection         │
       │  Output: fused (B, H)                                    │
       └─────────────────────────┬──────────────────────────────┘
                                 │
       ┌─────────────────────────▼──────────────────────────────┐
       │          SubtypeClassifier (classifier.py)              │
       │                                                          │
       │  Linear(H → final_dim=32) → ReLU → Dropout             │
       │  Linear(32 → num_classes)                               │
       │  Output: logits (B, num_classes)                        │
       └─────────────────────────┬──────────────────────────────┘
                                 │
                    Focal Loss + Label Smoothing
```

---

## Schema đồ thị dị thể

### Node types

| Node type | Số nodes (sau feature selection) | Nguồn dữ liệu                       |
| --------- | -------------------------------- | ----------------------------------- |
| `gene`    | ~3,500 (top-K theo ANOVA)        | TCGA gene expression (ENSG symbols) |
| `cpg`     | ~3,500 (top-K theo ANOVA)        | TCGA DNA methylation (cg... probes) |
| `mirna`   | 1,881 (toàn bộ)                  | TCGA miRNA expression               |

### Edge types (7 loại)

| Edge type                    | Quan hệ sinh học                      | Nguồn                          | Số lượng (BRCA) |
| ---------------------------- | ------------------------------------- | ------------------------------ | --------------- |
| `cpg → gene` (regulates)     | Biểu hiện甲基 hoá điều tiết gene      | emQTL (TCGA, p-value ≤ 0.05)   | ~52,000         |
| `gene ↔ gene` (ppi)          | Protein-protein interaction           | STRING v12, score ≥ 700        | ~22,000         |
| `mirna → gene` (targets)     | miRNA ức chế/điều tiết biểu hiện gene | miRTarBase (hsa_MTI.csv)       | ~147,000        |
| `gene ↔ gene` (copathway)    | Tham gia cùng pathway sinh học        | Reactome (pathway size ≤ 50)   | ~15,000         |
| `mirna ↔ mirna` (samefamily) | Cùng seed family (cơ chế tương tự)    | TargetScan / miR Family Info   | ~1,400          |
| `cpg ↔ mirna` (coregulates)  | CpG và miRNA cùng điều tiết 1 gene    | Suy diễn từ emQTL + miRTarBase | ~18,000         |
| Self-loops                   | Giữ thông tin ban đầu qua GATv2       | —                              | = số nodes      |

### Ghi chú về emQTL theo dataset

| Dataset                  | emQTL edges | Ghi chú                                            |
| ------------------------ | ----------- | -------------------------------------------------- |
| BRCA                     | ~52,000     | Phong phú — CpG kết nối tốt vào gene graph         |
| KIPAN                    | ~50,000+    | Phong phú                                          |
| GI (STAD/COAD/ESCA/READ) | ~40,000+    | Phong phú                                          |
| UCEC                     | ~3,000      | Thưa — giới hạn chính của mô hình trên dataset này |

---

## Chi tiết các module

### Module 1: MultiOmicGATModule (`src/models/gat_encoder.py`)

**Đầu vào:**
- `batch`: dict với keys `gene (B, F_g)`, `meth (B, F_m)`, `mirna (B, F_mi)` — feature vectors đã chuẩn hoá
- `graph`: `HeteroData` — đồ thị chia sẻ (không phụ thuộc bệnh nhân)

**Bước xử lý:**

1. **Node embedding**: mỗi node type có learnable embedding matrix `(num_nodes, H)` — một shared embedding bank, không phải per-patient
2. **GATv2Conv** (2 layers): `HeteroConv` với 12 relation types (bao gồm self-loops); mỗi layer có residual connection + ELU + LayerNorm
3. **Gene summary vector**: `z_gene = softmax-weighted mean` của tất cả gene node embeddings, trọng số từ patient feature values, chia `sqrt(F_g)` — cho `(B, H)`
4. **Top-K sequence**: chọn K=32 CpG/miRNA có giá trị feature lớn nhất (theo |x|), lấy embedding tương ứng, cộng positional encoding theo rank, modulate bởi feature value — cho `(B, K, H)`

**Hyperparameters:**
- `hidden_dim = 64`, `gat_heads = 4`, `gat_layers = 2`, `gat_dropout = 0.5`, `topk_seq = 32`

---

### Module 2: ModalityCrossAttention (`src/model.py`)

**Cơ chế asymmetric cross-attention:**

- Gene `z_gene` là **Query** — đặt câu hỏi: "CpG/miRNA nào điều tiết tôi?"
- `z_cpg_seq (B, 32, H)` là **Key/Value** cho nhánh epigenetic
- `z_mirna_seq (B, 32, H)` là **Key/Value** cho nhánh post-transcriptional

**Attention:**
```
scores = Q · K^T · scale · exp(log_temp)
attn   = Entmax15(scores)  # sparse, per-patient, per-node
ctx    = attn · V
```

**Fusion:**
```
w = softmax(modality_logits)   # học được: {w_cpg, w_mirna}
fused = LayerNorm(W_out([w_cpg·ctx_cpg ‖ w_mirna·ctx_mirna]) + z_gene)
```

**Interpretability output:**
- `cpg_attn (B, 32)` — mức độ mỗi CpG site quan trọng với từng bệnh nhân
- `mirna_attn (B, 32)` — mức độ mỗi miRNA quan trọng
- `modality_weights (2,)` — tầm quan trọng toàn cục của CpG vs miRNA

**Hyperparameters:**
- `ca_heads = 4`, `ca_dropout = 0.4`, `sparsemax_alpha = 1.5` (entmax15, hoặc 1.0 = softmax)

---

### Module 3: SubtypeClassifier + FocalLoss (`src/models/classifier.py`)

**Classifier:**
```
Linear(H=64 → final_dim=32) → ReLU → Dropout → Linear(32 → num_classes)
```

**Focal Loss:**
```
L = -Σ α_i · (1 - p_i)^γ · log(p_i)
```
- `γ = 2.0`: tập trung vào hard examples (minority subtypes)
- `α_i`: tính động từ `compute_class_weights` trên mỗi fold train set
- Label smoothing `ε = 0.05` để tránh overconfidence

**Frobenius regularization** trên weight matrices của cross-attention (`λ = 0.001`).

---

## Pipeline tiền xử lý

```
Raw TCGA data (gene: ~20K, meth: ~23K, mirna: 1881)
        ↓
1. Align samples (intersection qua 3 modality + labels)
        ↓
2. Stratified K-Fold split (5 folds, seed=42)
        ↓  [fitting CHỈ trên train set của mỗi fold]
3. ANOVA F-test feature selection
   - Top gene_top_k=3500 genes theo F-statistic (gene vs subtype labels)
   - Top meth_top_k=3500 CpG probes tương tự
   - Toàn bộ 1881 miRNA
   - Minority boost: thêm top-K features đặc trưng cho minority classes
        ↓
4. StandardScaler (fit trên train, transform val/test)
        ↓
5. Synthetic oversampling cho minority classes (trong train set)
        ↓
6. Build HeteroGraph từ feature names đã chọn
        ↓
7. Train / Validate / Test
```

---

## Training pipeline (`train.py`)

| Thành phần            | Chi tiết                                                           |
| --------------------- | ------------------------------------------------------------------ |
| **Đánh giá**          | 5-fold Stratified Cross-Validation (metric: val_f1)                |
| **Optimizer**         | AdamW, `weight_decay=3e-3`, `node_emb_weight_decay=1.5e-2`         |
| **Scheduler**         | OneCycleLR (`max_lr=5e-4`, `pct_start=0.1`)                        |
| **Loss**              | Focal Loss + Frobenius regularization                              |
| **Imbalance**         | `WeightedRandomSampler` (optional) + `minority_boost` oversampling |
| **Early stopping**    | Patience=20 epochs trên `val_f1`                                   |
| **Gradient clipping** | max_norm=1.0                                                       |
| **Epochs**            | 150                                                                |

---

## Cấu trúc thư mục

```
giac_project_kaggle/
├── README.md
├── train.py                        # Script huấn luyện chính (5-fold CV)
├── configs/
│   ├── config.yaml                 # GI cancer (STAD/COAD/ESCA/READ, 5 subtypes)
│   ├── config_brca.yaml            # BRCA (5 subtypes: Basal/Her2/LumA/LumB/Normal)
│   ├── config_ucec.yaml            # UCEC (4 subtypes: CN_high/CN_low/MSI/POLE)
│   └── config_kipan.yaml           # KIPAN (3 subtypes: KICH/KIRC/KIRP)
├── src/
│   ├── model.py                    # GIACModel: ghép encoder + cross-attn + classifier
│   ├── models/
│   │   ├── gat_encoder.py          # MultiOmicGATModule (HeteroGAT 2 layers)
│   │   ├── classifier.py           # SubtypeClassifier + FocalLoss
│   │   └── sparse_attention.py     # (Legacy) SparseMultiheadCrossAttention
│   ├── data/
│   │   ├── dataset.py              # Load, feature selection, split, normalize
│   │   └── graph_builder.py        # Build HeteroData từ 6 nguồn dữ liệu sinh học
│   └── utils.py                    # Metrics, seed, checkpoint, confusion matrix
├── Phiếu_giao_nhiệm_vụ 1.xlsx
└── Test_*/                         # Log kết quả thực nghiệm
    ├── 1.md  (Exp1)
    ├── 2.md  (Exp2)
    └── 3.md  (Exp3)
```

---

## Kết quả thực nghiệm

Đánh giá bằng **Macro F1** trên test set, tổng hợp qua 5-fold CV.

### So sánh với MoXGATE (baseline)

> ⚠️ MoXGATE dùng **single random split** — không phải 5-fold CV. Hai phương pháp đánh giá không hoàn toàn so sánh được trực tiếp. 5-fold CV tin cậy thống kê hơn nhưng thường cho con số thấp hơn do trung bình qua nhiều fold khó hơn.

| Dataset | Subtypes                        | Mô hình đề xuất (5-fold CV) | MoXGATE (single split) | Nhận xét               |
| ------- | ------------------------------- | --------------------------- | ---------------------- | ---------------------- |
| UCEC    | 4 (CN_high/CN_low/MSI/POLE)     | **0.7609** ± —              | 0.7487                 | **Vượt baseline**      |
| BRCA    | 5 (Basal/Her2/LumA/LumB/Normal) | 0.8333 ± 0.0478             | 0.8723                 | Cạnh tranh (gap ~0.04) |
| KIPAN   | 3 (KICH/KIRC/KIRP)              | 0.9210 ± 0.0142             | 0.9561                 | Cạnh tranh (gap ~0.04) |
| GI      | 5 (CIN/GS/MSI/HM-SNV/EBV)       | —                           | 0.8333                 | Dataset gốc            |

### Tiến trình thực nghiệm BRCA

| Exp      | Thay đổi chính                             | F1 (5-fold) |
| -------- | ------------------------------------------ | ----------- |
| Exp1     | Config mặc định                            | 0.7704      |
| Exp2     | Tăng patience, dropout cao hơn             | 0.7536      |
| **Exp3** | **Revert dropout, balanced_sampler=false** | **0.8333**  |

### Tiến trình thực nghiệm KIPAN

| Exp      | Thay đổi chính                          | F1 (5-fold) |
| -------- | --------------------------------------- | ----------- |
| Exp1     | Config mặc định                         | 0.8999      |
| **Exp2** | **minority_boost tăng, ca_dropout=0.4** | **0.9210**  |
| Exp3     | balanced_sampler=true (backfired)       | 0.9009      |

### Quan sát về interpretability

Cross-attention weights cho thấy modality CpG luôn chiếm tỷ trọng cao hơn miRNA:
- BRCA: cpg ≈ 0.60–0.63, mirna ≈ 0.37–0.40
- KIPAN: cpg ≈ 0.57–0.62, mirna ≈ 0.38–0.43

Điều này phù hợp sinh học: DNA methylation là hallmark quan trọng trong phân loại phân tử ung thư vú và thận.

---

## Cài đặt và chạy

### Môi trường

```bash
pip install torch torch_geometric entmax scikit-learn pandas numpy seaborn pyyaml
```

### Chạy huấn luyện

```bash
# GI cancer (config mặc định)
python train.py --config configs/config.yaml

# BRCA
python train.py --config configs/config_brca.yaml

# UCEC
python train.py --config configs/config_ucec.yaml

# KIPAN
python train.py --config configs/config_kipan.yaml
```

### Cấu trúc config

```yaml
data:
  data_dir: "/path/to/data"     # thư mục chứa labels.csv, gene.csv, meth.csv, mirna.csv
  graph_dir: "/path/to/graph"   # thư mục chứa file STRING, Reactome, miRTarBase, ...
  emqtl_dir: "/path/to/emqtl"  # thư mục chứa TCGA_emQTL_{CANCER}.txt
  cancer_types: ["BRCA"]

preprocessing:
  gene_top_k: 3500
  meth_top_k: 3500
  mirna_top_k: 1881
  feature_selection_method: "anova"
  minority_boost_gene: 200      # số features bổ sung cho minority classes
  minority_classes: [1, 2, 4]   # index của minority classes

model:
  hidden_dim: 64
  gat_heads: 4
  gat_layers: 2
  sparsemax_alpha: 1.0          # 1.0=softmax, 1.5=entmax15 (sparse)
  num_classes: 5

training:
  epochs: 150
  learning_rate: 1.0e-4
  scheduler: "onecycle"
  loss_name: "focal"
  focal_gamma: 2.0
  patience: 20
  subtype_names: ["Basal", "Her2", "LumA", "LumB", "Normal"]
```

---

## Dữ liệu đầu vào

Mỗi dataset cần 4 file CSV:

| File         | Nội dung                                                     |
| ------------ | ------------------------------------------------------------ |
| `labels.csv` | `sample_id, subtype_label`                                   |
| `gene.csv`   | `sample_id, ENSG00000...` (gene expression, log2-normalized) |
| `meth.csv`   | `sample_id, cg12345678...` (beta values 0–1)                 |
| `mirna.csv`  | `sample_id, hsa-mir-21...` (miRNA expression)                |

Dữ liệu lấy từ TCGA qua GDC Data Portal, preprocessing theo pipeline của TCGA multi-omics.

---

## Nguồn prior knowledge sinh học

| Nguồn        | Dùng cho                      | File                              |
| ------------ | ----------------------------- | --------------------------------- |
| emQTL (TCGA) | CpG → Gene edges              | `TCGA_emQTL_{CANCER}.txt`         |
| STRING v12   | Gene ↔ Gene PPI edges         | `9606.protein.links.v12.0.txt`    |
| Reactome     | Gene ↔ Gene co-pathway        | `Ensembl2Reactome_All_Levels.txt` |
| miRTarBase   | miRNA → Gene edges            | `hsa_MTI.csv`                     |
| TargetScan   | miRNA ↔ miRNA family          | `miR_Family_Info.txt`             |
| HGNC         | Ensembl → gene symbol mapping | `hgnc_complete_set.txt`           |
| STRING alias | ENSP → gene symbol mapping    | `9606.protein.aliases.v12.0.txt`  |

---

## Tài liệu tham khảo chính

- **MoXGATE**: Multi-Omics Graph Attention Network — baseline paper được cải tiến
- **GATv2Conv**: Brody et al., "How Attentive are Graph Attention Networks?", ICLR 2022
- **Entmax15**: Peters et al., "Sparse Sequence-to-Sequence Models", ACL 2019
- **Focal Loss**: Lin et al., "Focal Loss for Dense Object Detection", CVPR 2017
- **emQTL**: TCGA methylation-expression quantitative trait loci
