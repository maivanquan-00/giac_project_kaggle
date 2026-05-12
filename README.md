# Phân loại bệnh nhân ung thư dựa trên đồ thị dị thể đa omics kết hợp Graph Attention Network và Cross-Attention

**Đồ án tốt nghiệp HUST 2025.2** — Trường Công nghệ Thông tin và Truyền thông.

| Mục                 | Thông tin                                |
| ------------------- | ---------------------------------------- |
| Sinh viên           | NULL                                     |
| Giáo viên hướng dẫn | NULL                                     |
| Lĩnh vực            | Trí tuệ nhân tạo ứng dụng — Tin sinh học |
| Thời gian thực hiện | 23/02/2026 – 12/07/2026                  |

> Đồ án đề xuất kiến trúc **GIAC** (Graph-Informed Asymmetric Cross-attention) — kế thừa và cải tiến mô hình baseline **MoXGATE** ([arXiv:2506.06980](https://arxiv.org/abs/2506.06980)) cho bài toán phân loại phân nhóm phân tử ung thư từ ba loại dữ liệu omics: gene expression, DNA methylation và miRNA expression của TCGA.

---

## 1. Mục tiêu của đồ án (theo Phiếu giao nhiệm vụ)

### 1.1 Vấn đề thực tiễn

- **Phân loại phân tử ung thư** là nền tảng của *y học chính xác* — mỗi phân nhóm phân tử có tiên lượng và phác đồ điều trị khác nhau, phân loại đúng ảnh hưởng trực tiếp đến kết quả điều trị.
- Dữ liệu **đa omics** (gene/methylation/miRNA) bổ sung cho nhau nhưng có **chiều rất cao** (~46K features tổng) và **số mẫu hạn chế** (vài trăm bệnh nhân/cohort) → cần phương pháp fusion thông minh.
- Các quan hệ điều tiết sinh học đã biết (emQTL, PPI, pathway, miRNA target) là **prior knowledge quý giá** chưa được khai thác đầy đủ trong các mô hình deep learning thông thường.
- Mô hình cần **interpretable** — chỉ ra gene/CpG/miRNA nào quyết định phân loại — để có giá trị ứng dụng nghiên cứu lâm sàng.

### 1.2 Sản phẩm đề xuất

1. **Kiến trúc tổng quát** áp dụng được cho nhiều bộ dữ liệu đa omics, không bị giới hạn loại ung thư hay số subtype cụ thể (đã thử nghiệm trên 4 dataset TCGA: GI/BRCA/UCEC/KIPAN).
2. **Đồ thị dị thể đa omics** tích hợp **8 loại quan hệ sinh học** từ 7 cơ sở dữ liệu chuẩn (emQTL, STRING PPI, Reactome, miRTarBase, TargetScan miR family, Illumina 450K CpG island, co-regulation suy diễn).
3. **Cross-Attention bất đối xứng**: gene đóng vai trò *Query*, CpG/miRNA đóng vai trò *Key/Value* — phản ánh đúng *central dogma* (methylation/miRNA điều khiển ngược lên biểu hiện gene).
4. **Source code module hoá**, dễ mở rộng sang dataset mới (chỉ cần thêm 1 file `config_*.yaml` và file `clean_labels_*.csv`).
5. **Kết quả thực nghiệm** kiểm chứng bằng **3 seeds × 5-fold Stratified CV = 15 runs/dataset** thay vì single split như MoXGATE — đảm bảo độ tin cậy thống kê.

---

## 2. So sánh với MoXGATE (baseline)

| Khía cạnh           | **MoXGATE** ([arXiv 2506.06980](https://arxiv.org/abs/2506.06980)) | **GIAC (đề xuất)**                                                         |
| ------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Đồ thị              | ❌ Không dùng — 3 modalities xử lý độc lập                          | ✅ **Heterogeneous Graph 8 loại quan hệ**                                   |
| Encoder             | 3 nhánh **Self-Attention** (8 heads, 256d) độc lập                 | **HeteroGAT** (GATv2 × 13 relation types) chia sẻ qua đồ thị               |
| Cross-Attention     | **Đối xứng** — stack 3 modalities, attention xếp đều               | **Bất đối xứng** — gene = Q, CpG/miRNA = K/V                               |
| Kích hoạt attention | softmax (dày đặc)                                                  | **Entmax 1.5** (sparse → interpretable per-patient)                        |
| Số tham số          | ~12.6M                                                             | **~830K (1/15)** — lightweight                                             |
| Loss                | Focal (γ=2, α=1)                                                   | Focal **per-class α từ class frequency** + label smoothing + Frobenius reg |
| Đánh giá            | Single 90/10 split (COAD+READ+STAD train, ESCA test)               | **5-fold Stratified CV × 3 seeds = 15 runs**                               |
| Dataset             | GI + BRCA                                                          | GI + BRCA + UCEC + KIPAN (mở rộng 2 dataset)                               |

---

## 3. Pipeline tiền xử lý dữ liệu

> **Pipeline gọn:** `raw TCGA TSV → 4 file processed_*.csv → 4 file final_*.csv (đã align sample)`. Chạy 1 lệnh duy nhất: `python preprocessed_data/main_preprocess_omics.py --base <thư_mục_gốc>`.

### 3.1 Sơ đồ tổng quát

```
data_original/<dataset>/                      ← Input
  ├── gene/    *.tsv (Xena STAR, log2(TPM+1))
  ├── mirna/   *.tsv (Xena, log2(RPM+1))
  └── methyl/
      ├── 27k/  *.tsv  (beta values [0,1])
      └── 450k/ *.tsv  (beta values [0,1])
data_original/subtype_<dataset>/  *.tsv  ← Clinical labels
data_original/annotation/                 ← File phụ trợ
  ├── gencode.v36.annotation.gtf            (lọc protein-coding genes)
  ├── cross_reactive_probes.txt             (Chen et al. 2013)
  └── HumanMethylation450_manifest.csv     (lọc chrX/Y probes)
Heterogeneous_Graph/hgnc_complete_set.txt   (Ensembl→symbol mapping)

         │
         │ preprocess_Gene.py
         │ preprocess_miRNA.py
         │ preprocess_CpG.py
         │ preprocess_labels[_brca/_ucec/_kipan/_lgg].py
         ▼
data_processed_<dataset>/
  ├── processed_gene.csv         (patients × ~19K gene symbols)
  ├── processed_mirna.csv        (patients × ~600 miRNA expressed)
  ├── processed_methylation.csv  (patients × ~27K CpG probes)
  └── clean_labels_<dataset>.csv (Patient ID, Cancer_Type, Subtype, Target_Label)

         │ final_process_omics.py  (lấy giao 4 nguồn theo Patient ID)
         ▼
data_final_<dataset>/                     ← Input cho train.py
  ├── final_gene.csv
  ├── final_mirna.csv
  ├── final_methylation.csv
  └── final_labels.csv
```

### 3.2 Chuẩn hoá Patient ID — quy tắc chung 3 modalities

Mọi script `preprocess_{Gene,miRNA,CpG}.py` đều áp 4 bước **giống nhau** trên từng file TSV cohort:

| Bước | Hành động                                    | Lý do                                                                                |
| ---- | -------------------------------------------- | ------------------------------------------------------------------------------------ |
| (a)  | Lọc cột `barcode[13:15] == '01'`             | Chỉ giữ **Primary Solid Tumor**, loại normal `11`, recurrence `02`, metastatic `06`. |
| (b)  | Cắt barcode về 12 ký tự đầu (`TCGA-XX-XXXX`) | Patient ID chuẩn — cho phép merge cross-modality.                                    |
| (c)  | Loại bệnh nhân trùng (giữ Vial A = first)    | Một bệnh nhân có thể có nhiều aliquot.                                               |
| (d)  | Transpose → `(patients × features)`          | Convention chung của framework downstream.                                           |

### 3.3 Gene Expression (`preprocess_Gene.py`)

```
GENCODE v36 GTF  →  19.962 protein-coding gene_id (có version, ENSG…X)
                         │
TCGA STAR TPM TSV  ──────┤  lọc protein-coding
                         │  chuẩn hoá Patient ID (a-d)
                         ▼
            concat(join='inner')   ← chỉ giữ gene xuất hiện ở mọi cohort
                         │
            Quality Control:
              - Drop gene thiếu >40% bệnh nhân
              - Median imputation cho phần còn lại
                         │
            Map ENSG.version → gene SYMBOL  ← qua hgnc_complete_set.txt
              (~19.000 → ~17.500 sau drop unmapped, dedup symbol)
                         │
                         ▼
            processed_gene.csv  (patients × gene symbols)
```

**Lưu ý quan trọng:**
- Dữ liệu Xena/STAR đã ở dạng `log2(TPM+1)` — **KHÔNG log thêm** lần nữa (bug double-log đã fix 2026-05-09: range gene từ [0, 4] → [0, 15]).
- Cột phải là **gene symbol**, không phải Ensembl ID — graph PPI/Reactome dùng symbol làm key.
- Sanity check: `max ≈ 15-20`, `median ≈ 5-8`. Nếu max < 6 → có double-log bug.

### 3.4 miRNA Expression (`preprocess_miRNA.py`)

Đầu vào là `log2(RPM+1)` từ Xena (~1.881 stem-loop precursors theo miRBase v22).

| Bước                   | Chi tiết                                                                                 |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| Chuẩn hoá Patient ID   | (a)-(d) như trên                                                                         |
| QC                     | Drop miRNA thiếu >40% bệnh nhân + median imputation                                      |
| **Lọc low-expression** | Giữ miRNA có `log2(RPM+1) > 0.5` ở **≥20% bệnh nhân** → còn ~600 miRNA biểu hiện ổn định |

Output: `processed_mirna.csv` (patients × ~600 miRNA, tên dạng `hsa-mir-21-1`).

### 3.5 DNA Methylation (`preprocess_CpG.py`)

Đầu vào là **2 platform** Illumina: 27k (~27.578 probes) và 450k (~485.512 probes). Bước xử lý đặc thù:

```
27k + 450k file  →  chuẩn hoá Patient ID (a-d)
                         │
                concat(join='inner')   ← tự động thu về ~27k sites chung
                                          (vì 27k là tập con của 450k)
                         │
                Loại bệnh nhân vừa có 27k vừa 450k  → giữ bản 450k
                         │
                Lọc probes không đáng tin cậy:
                  - Cross-reactive (Chen et al. 2013, AlleleA/B_Hits > 1)
                  - chrX/Y (Illumina 450k manifest → bias giới tính)
                         │
                QC: drop probe thiếu >40% + median imputation
                         │
                         ▼
            processed_methylation.csv  (patients × ~25K-26K CpG sites)
```

Beta value ∈ [0, 1] (0 = unmethylated, 1 = fully methylated).

### 3.6 Labels — 5 dataset, 5 logic riêng

| Dataset   | File                                                                       | Subtypes                             | Logic chính                                            |
| --------- | -------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------ |
| **GI**    | [preprocess_labels.py](preprocessed_data/preprocess_labels.py)             | 5: CIN/GS/MSI/HM-SNV/EBV             | Cắt prefix `ESCA_`/`COAD_`/...; merge `POLE → HM-SNV`. |
| **BRCA**  | [preprocess_labels_brca.py](preprocessed_data/preprocess_labels_brca.py)   | 5 PAM50: LumA/LumB/Her2/Basal/Normal | Tách hậu tố sau `BRCA_`, normalize case.               |
| **UCEC**  | [preprocess_labels_ucec.py](preprocessed_data/preprocess_labels_ucec.py)   | 4: CN_LOW/CN_HIGH/MSI/POLE           | Detect substring trong subtype string.                 |
| **KIPAN** | [preprocess_labels_kipan.py](preprocessed_data/preprocess_labels_kipan.py) | 3: KICH/KIRC/KIRP                    | Tách từ `project_id` (`TCGA-KIRC` → `KIRC`).           |
| **LGG**   | [preprocess_labels_lgg.py](preprocessed_data/preprocess_labels_lgg.py)     | 3: Codel/IDHmut-non-codel/IDHwt      | Match keyword `CODEL`, `NON.*CODEL`, `IDH.*WT`.        |

Output thống nhất: `Patient ID, Cancer_Type, Subtype, Target_Label` — `Target_Label` là integer 0..(num_classes−1).

### 3.7 `final_process_omics.py` — bước căn chỉnh cuối

```
load clean_labels_<ds>.csv  →  bệnh nhân có nhãn hợp lệ
load 3 file processed_*.csv  →  lọc theo nhãn
                              →  inner-join 4 nguồn theo Patient ID
                              →  align thứ tự dòng
                              →  ghi 4 file final_*.csv (input cho train.py)
```

Sanity check tự động phát hiện:
- Double-log gene (`max < 6.0`)
- Cột vẫn Ensembl thay vì symbol (graph sẽ rỗng)
- Beta methylation ngoài [0, 1]
- NaN sót sau imputation
- Phân bố `Target_Label` cuối + thống kê per-cancer-type

### 3.8 Tiền xử lý "online" trong `src/data/dataset.py` (không leakage)

Khi train, mỗi fold **fit lại preprocessing CHỈ trên training subset của fold đó** rồi áp lên val/test:

```
StratifiedKFold(n=5)  →  5 fold × (train, val, test)
                          │
                          │  fit_preprocessor(train only):
                          │    1. Pre-filter cột std < 1e-10 (constant)
                          │    2. ANOVA F-test (f_classif) → top-K theo F-score
                          │       gene_top_k = 3500
                          │       meth_top_k = 3500
                          │       mirna_top_k = 1881 (giữ tất cả)
                          │    3. Minority-class boost: với mỗi class hiếm c
                          │       chạy ANOVA binary (c vs rest), lấy top-N
                          │       feature, MERGE (union, dedup) vào tập chính
                          │       → đảm bảo feature đặc trưng cho minority
                          │         không bị ANOVA tổng đè bẹp
                          │    4. Compute mean/std trên train subset
                          │
                          │  apply_preprocessor(val/test):
                          │    select features theo `indices` đã chọn
                          │    z-score = (x - train_mean) / train_std
                          ▼
                ANOVA-selected, z-scored arrays
                (gene ≈ 3500-3800, meth ≈ 3500-3800, mirna = 1881)
```

`minority_classes` cho từng dataset (config-level):
- **GI**: `[1, 3]` (GS=49, HM-SNV=19 — 2 lớp hiếm nhất)
- **BRCA**: `[1, 2, 4]` (Her2, LumA chú ý nhỏ, Normal=36)
- **UCEC**: `[3]` (POLE ~7%)
- **KIPAN**: không cần boost (3 lớp tương đối cân)

---

## 4. Đồ thị dị thể đa omics

### 4.1 3 loại node

| Node    | Số lượng                                  | Embedding                                               |
| ------- | ----------------------------------------- | ------------------------------------------------------- |
| `gene`  | ~3.500-3.800 (sau ANOVA + minority boost) | `nn.Parameter(N_g, 64)` learnable, share giữa bệnh nhân |
| `cpg`   | ~3.500-3.800 (CpG site đã chọn)           | `nn.Parameter(N_c, 64)` learnable                       |
| `mirna` | ~500 (giữ toàn bộ)                        | `nn.Parameter(N_m, 64)` learnable                       |

Các node embedding **chỉ encode "feature identity"** (TP53 luôn là TP53), không phải patient-specific. Tổng ~568K params (68% tổng số params toàn model).

### 4.2 8 loại cạnh sinh học (13 relation types khi tính cả chiều ngược)

| #   | Quan hệ                                  | Nguồn                                                          | Ý nghĩa sinh học                                        | # edges (GI) |
| --- | ---------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------- | ------------ |
| 1   | `cpg → regulates → gene` (+ chiều ngược) | TCGA emQTL `TCGA_emQTL_<cohort>.txt`, `p < 0.05`               | Methylation điều tiết biểu hiện gene                    | ~24K         |
| 2   | `gene ↔ ppi ↔ gene`                      | STRING v12 `combined_score ≥ 700`                              | Tương tác protein-protein                               | ~30K         |
| 3   | `mirna → targets → gene` (+ chiều ngược) | miRTarBase `hsa_MTI.csv`                                       | miRNA ức chế biểu hiện gene                             | ~145K        |
| 4   | `gene ↔ copathway ↔ gene`                | Reactome `Ensembl2Reactome_All_Levels.txt`, pathway ≤ 50 genes | Cùng pathway → co-regulated                             | ~15K         |
| 5   | `mirna ↔ samefamily ↔ mirna`             | TargetScan `miR_Family_Info.txt`                               | Cùng seed family → cơ chế tương tự                      | ~1.4K        |
| 6   | `cpg ↔ coregulates ↔ mirna`              | **Suy diễn** từ #1 ∩ #3 (cùng regulate gene chung)             | Đóng vòng CpG–Gene–miRNA                                | ~18K         |
| 7   | `cpg ↔ sameisland ↔ cpg`                 | Illumina 450K manifest `HumanMethylation450_manifest.csv`      | Cùng CpG island → co-methylated, cùng regulatory region | TBD          |
| 8   | Self-loops (3 cho mỗi node type)         | identity                                                       | Bảo toàn thông tin gốc qua GATv2                        | = số nodes   |

**Capping** để tránh đồ thị quá dày (config `graph.max_edges_per_node = 20`, `max_targets_per_mirna = 100`, `max_coregulation_edges = 10`, `max_pathway_size = 50`, `MAX_FAMILY_SIZE = 20`).

### 4.3 Quy tắc matching tên (quan trọng cho lookup nhất quán)

| Modality | Normalization key                                                                                                                    |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Gene     | UPPERCASE (`TP53`) — cho cả `gene_idx`, alias STRING, HGNC mapping                                                                   |
| CpG      | giữ nguyên (`cg00000029`)                                                                                                            |
| miRNA    | lowercase (`hsa-mir-21-1`); thêm regex strip suffix `-1/-2/-3` (precursor) và `-3p/-5p` (mature) khi cần match TargetScan/miRTarBase |

```
gene_idx  : { "TP53": 0, "BRCA1": 1, ... }              # UPPER
cpg_idx   : { "cg00000029": 0, "cg00000108": 1, ... }   # raw
mirna_idx : { "hsa-mir-21-1": 0, "hsa-let-7a-1": 1, …}  # lower
```

Một bug đã được fix: regex chuẩn hoá miRNA cũ `r'-\d+$'` quá tham (sẽ biến `hsa-mir-100` → `hsa-mir`); regex mới `r'^(hsa-(?:mir|let)-\S+?)-([1-9])$'` phân biệt đúng "100 là số gốc" vs "-1/-2/-3 là precursor isoform suffix".

---

## 5. Kiến trúc model GIAC

```
Input batch:                    Heterogeneous Graph (shared, build 1 lần per fold)
 gene  (B, F_g≈3500)              ┌─ gene  nodes (N_g, 64)
 meth  (B, F_m≈3500)              ├─ cpg   nodes (N_c, 64)
 mirna (B, F_mi=1881)             └─ mirna nodes (N_m, 64) + 7 edge types
        │                                              │
        └──────────────────────┬───────────────────────┘
                               ▼
       ┌──────────────────── MODULE 1 ────────────────────┐
       │     MultiOmicGATModule (gat_encoder.py)          │
       │                                                  │
       │  Layer 1: HeteroConv(GATv2 × 12 relations)       │
       │           + Residual + ELU + LayerNorm           │
       │  Layer 2: HeteroConv(GATv2 × 12 relations)       │
       │           + Residual + ELU + LayerNorm           │
       │                                                  │
       │  Outputs (per patient):                          │
       │    z_gene      (B, 64)    weighted-mean over     │
       │                            gene embeddings       │
       │                            theo expression value │
       │    z_cpg_seq   (B, 32, 64) top-32 CpG by |β|,   │
       │                             modulated theo β,    │
       │                             + rank pos-encoding  │
       │    z_mirna_seq (B, 32, 64) top-32 miRNA tương tự │
       └─────────────────────┬────────────────────────────┘
                             ▼
       ┌──────────────────── MODULE 2 ────────────────────┐
       │   ModalityCrossAttention (model.py) — Asymmetric │
       │                                                  │
       │     z_gene  ── W_q ──────────────► Q (B, 64)     │
       │                                                  │
       │     z_cpg_seq ── W_k_cpg, W_v_cpg ► K, V         │
       │     z_mirna_seq ── W_k_mirna, W_v_mirna ► K, V   │
       │                                                  │
       │   scores_m = (Q · K_m^T)/√d_h · exp(log_temp)   │
       │   attn_m   = entmax15(scores_m)  ← sparse        │
       │   ctx_m    = attn_m · V_m                        │
       │                                                  │
       │   w = softmax(modality_logits)  (2,)             │
       │   fused = LN( W_o[w₀·ctx_cpg ‖ w₁·ctx_mirna]    │
       │              + z_gene )                          │
       └─────────────────────┬────────────────────────────┘
                             ▼
       ┌──────────────────── MODULE 3 ────────────────────┐
       │   SubtypeClassifier (classifier.py)              │
       │                                                  │
       │   Linear(64 → 32) → ReLU → Dropout(0.5)          │
       │   → Linear(32 → C)                               │
       └─────────────────────┬────────────────────────────┘
                             ▼
                   logits (B, C)
                             │
              Loss = FocalLoss(γ=2, α per-class)
                     + label_smoothing 0.05
                     + λ_F · ‖W_q,W_k,W_v,W_o‖²_F
```

### 5.1 Module 1 — `MultiOmicGATModule` (HeteroGAT encoder)

**File:** [src/models/gat_encoder.py](src/models/gat_encoder.py)

- **`HeteroConv` × 2 layers**, mỗi layer ánh xạ qua 12 `GATv2Conv` (1 per relation type), aggregator `sum`, multi-head 4 heads × head_dim 16 = 64.
- **Residual + LayerNorm + ELU + Dropout** sau mỗi layer:
  ```
  x_t = LayerNorm( x_t + ELU(Dropout(out_t)) )    ∀ t ∈ {gene, cpg, mirna}
  ```
- **3 đầu ra cho từng bệnh nhân:**
  - `z_gene = LayerNorm( batch[gene] @ E_gene / √F_g )` — weighted sum gene embeddings, weight là expression z-scored, chia `√F_g` chống nổ scale.
  - `z_cpg_seq` / `z_mirna_seq`: chọn `K=32` token có `|value|` lớn nhất, modulate `E_topk + E_topk * value` (multiplicative+additive), thêm **rank-based positional embedding** (rank 0 = most active).

### 5.2 Module 2 — `ModalityCrossAttention` (asymmetric, sparse)

**File:** [src/model.py](src/model.py)

**Tại sao bất đối xứng?** Theo *central dogma*: methylation/miRNA → điều khiển → gene expression → phenotype (subtype). Vì vậy gene nên **truy vấn** epigenetic + post-transcriptional context, không ngược lại. Khác với MoXGATE (xếp 3 modality đối xứng).

**Forward:**

$$
\text{ctx}_m = \text{entmax}_{1.5}\!\left(\frac{Q K_m^T}{\sqrt{d_h}} e^{\tau}\right) V_m, \quad m \in \{\text{cpg, mirna}\}
$$

$$
w = \text{softmax}(l)\in\mathbb{R}^2, \qquad \text{fused} = \text{LN}\big(W_o\,[w_c\cdot \text{ctx}_c \,\|\, w_m\cdot \text{ctx}_m] + z_{\text{gene}}\big)
$$

**Trong đó:**
- $\tau$ (`log_temp`) — học được, sharpen/flatten attention distribution.
- $l$ (`modality_logits`) — học được, đo tầm quan trọng *toàn cục* của CpG vs miRNA.
- **Entmax 1.5** thay softmax → output **sparse** (nhiều weight = 0 hard) → **interpretable**: trả về `cpg_attn (B, K)`, `mirna_attn (B, K)`, `modality_weights (2,)` cho từng bệnh nhân.

**Khác MoXGATE:**

|                      | MoXGATE                                     | GIAC                                         |
| -------------------- | ------------------------------------------- | -------------------------------------------- |
| Vai trò 3 modalities | Đối xứng (stack & cross-attention 32 heads) | **Bất đối xứng** (gene = Q, CpG/miRNA = K/V) |
| Sparsity             | softmax (dense)                             | **entmax15** (sparse)                        |
| Interpretability     | Chỉ modality weights (3,)                   | Per-patient per-token + modality             |

### 5.3 Module 3 — `SubtypeClassifier` + Focal Loss

**File:** [src/models/classifier.py](src/models/classifier.py)

```python
fc = Linear(hidden=64 → final_dim=32) → ReLU → Dropout(0.5) → Linear(32 → C)
```

**Focal loss** với label smoothing:

$$
\mathcal{L}_{\text{focal}} = -\frac{1}{B}\sum_i \alpha_{y_i}(1-p_{i,y_i})^{\gamma}\,\text{ce}_i, \quad \text{ce}_i = (1-\epsilon)(-\log p_{i,y_i}) + \epsilon\,\overline{(-\log p_i)}
$$

- $\gamma = 2.0$, $\epsilon = 0.05$.
- $\alpha_c$ tính **động** từ class frequency của train set qua `compute_class_weights`, normalize mean = 1 (trừ khi bật `use_manual_focal_alpha=true` để giữ giá trị config).
- **Frobenius regularization** $\lambda_F = 0.001$ trên mọi `W_*` của cross-attention để tránh weight collapse khi entmax15 đẩy gradient về biên.

### 5.4 Tổng tham số (~830K) — phân bố

| Component                                   | Params    | %    |
| ------------------------------------------- | --------- | ---- |
| 3 node embedding tables (3 × N × 64)        | ~568K     | 68%  |
| HeteroConv 2 layers × 12 GATv2 relations    | ~98K      | 12%  |
| Cross-attention (W_q, 2×W_k, 2×W_v, W_o)    | ~25K      | 3%   |
| Position embeddings (2 × 32 × 64)           | ~4K       | 0.5% |
| LayerNorms + classifier head                | ~7K       | 0.7% |
| Misc (log_temp, modality_logits, alpha buf) | <1K       | —    |
| **Total**                                   | **~830K** | 100% |

→ **MoXGATE ~12.6M params** → GIAC chỉ bằng **1/15**, nhưng đạt độ ổn định cao hơn 2-5 lần qua multi-seed (xem §7).

---

## 6. Training pipeline

**File:** [train.py](train.py), [run_multi_seed.py](run_multi_seed.py)

| Thành phần            | Cấu hình mặc định                                                                                                                                                                                                                                                                   |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Đánh giá**          | 5-fold Stratified CV (`StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)`); val set = 15% of train-fold qua `train_test_split` riêng                                                                                                                                     |
| **Multi-seed**        | 3 seeds (42, 123, 2024) × 5 folds = **15 runs/dataset**                                                                                                                                                                                                                             |
| **Optimizer**         | AdamW, 2 param groups: base (lr=1e-4, wd=3e-3), `node_emb` (lr=1e-4, wd=1.5e-2)                                                                                                                                                                                                     |
| **Scheduler**         | OneCycleLR (max_lr=5e-4, pct_start=0.1, div_factor=10, final_div_factor=100) — step per batch                                                                                                                                                                                       |
| **Loss**              | Focal + Frobenius reg                                                                                                                                                                                                                                                               |
| **Class imbalance**   | (a) Per-class `α` từ inverse frequency  (b) Optional `WeightedRandomSampler` (đã thử nghiệm — gây collapse trên hầu hết dataset, mặc định OFF)  (c) **Minority augmentation**: thêm Gaussian noise σ=0.10 vào sample minority class trong mỗi batch — chống memorize bệnh nhân hiếm |
| **Gradient clipping** | `max_norm = 1.0`                                                                                                                                                                                                                                                                    |
| **Early stopping**    | Patience = 20 epochs trên `val_f1` macro                                                                                                                                                                                                                                            |
| **Epochs**            | 150                                                                                                                                                                                                                                                                                 |
| **Model selection**   | best `val_f1` macro (có thể đổi `model_selection_metric: val_loss`)                                                                                                                                                                                                                 |

**Metrics báo cáo (`src/utils.py:compute_metrics`):**
- **Primary: Macro F1** — conservative cho imbalanced multi-class (đối xử mọi class như nhau).
- **Secondary: Weighted F1** — báo song song để đối chiếu với MoXGATE paper (paper dùng weighted F1, đã verify bằng reproduction 2026-05-07).
- Per-class F1, per-cancer-type F1 (cho dataset multi-cohort như GI).

**Workflow chuẩn:**

```bash
# 1 dataset, 3 seeds × 5 folds
python run_multi_seed.py --config configs/config.yaml          # GI
python run_multi_seed.py --config configs/config_brca.yaml     # BRCA
python run_multi_seed.py --config configs/config_ucec.yaml     # UCEC
python run_multi_seed.py --config configs/config_kipan.yaml    # KIPAN

# Single-seed debug
python train.py --config configs/config.yaml --seed 42
```

`run_multi_seed.py` parse stdout từng seed, aggregate mean ± std, in **block markdown sẵn sàng paste vào [docs/RESULTS.md](docs/RESULTS.md)**.

---

## 7. Kết quả thực nghiệm

> **Đánh giá apples-to-apples**: MoXGATE đã được **re-run** với cùng `StratifiedKFold(5)` và cùng 3 seeds để so sánh công bằng (paper gốc dùng single 90/10 split). Số liệu authoritative: [docs/RESULTS.md](docs/RESULTS.md).

### 7.1 So sánh GIAC vs MoXGATE (Macro F1, 3 seeds × 5 folds = 15 runs)

| Dataset                  | n   | # subtypes                      | **GIAC macro F1**  | MoXGATE 5-fold macro F1 | Δ            | Verdict      |
| ------------------------ | --- | ------------------------------- | ------------------ | ----------------------- | ------------ | ------------ |
| GI (COAD+ESCA+READ+STAD) | 917 | 5 (CIN/GS/MSI/HM-SNV/EBV)       | 0.6626 ± 0.035     | 0.7132 ± 0.063          | −0.051       | MoXGATE      |
| BRCA                     | 965 | 5 (Basal/Her2/LumA/LumB/Normal) | 0.8077 ± 0.009     | 0.8184 ± 0.029          | −0.011       | gần tie      |
| **UCEC**                 | 499 | 4 (CN_high/CN_low/MSI/POLE)     | **0.7447 ± 0.009** | 0.7193 ± 0.041          | **+0.025** ✓ | **GIAC win** |
| KIPAN                    | 685 | 3 (KICH/KIRC/KIRP)              | 0.8918 ± 0.008     | 0.9526 ± 0.017          | −0.061       | MoXGATE      |

### 7.2 Weighted F1 (đối chiếu paper MoXGATE)

| Dataset  | GIAC               | MoXGATE        | Δ            |
| -------- | ------------------ | -------------- | ------------ |
| GI       | 0.8226 ± 0.022     | 0.8626 ± 0.020 | −0.040       |
| BRCA     | 0.8690 ± 0.011     | 0.8717 ± 0.021 | −0.003 (tie) |
| **UCEC** | **0.7919 ± 0.006** | 0.7765 ± 0.027 | +0.015 ✓     |
| KIPAN    | 0.9160 ± 0.008     | 0.9593 ± 0.013 | −0.043       |

### 7.3 Phát hiện quan trọng — GIAC ổn định hơn MoXGATE 2-5 lần

| Dataset | GIAC std | MoXGATE std | Ratio           |
| ------- | -------- | ----------- | --------------- |
| GI      | 0.035    | 0.063       | **1.8×** stable |
| BRCA    | 0.009    | 0.029       | **3.2×** stable |
| UCEC    | 0.009    | 0.041       | **4.6×** stable |
| KIPAN   | 0.008    | 0.017       | **2.1×** stable |

→ Đây là điểm mạnh có thể nhấn mạnh: **lightweight + parameter efficient + training stability** — phù hợp triển khai lâm sàng (kết quả dự đoán được, ít phụ thuộc seed).

### 7.4 Quan sát interpretability

Cross-attention `modality_weights` (học được) cho thấy **CpG luôn chiếm tỷ trọng cao hơn miRNA**:
- BRCA: cpg ≈ 0.60–0.63, mirna ≈ 0.37–0.40
- KIPAN: cpg ≈ 0.57–0.62, mirna ≈ 0.38–0.43

Phù hợp sinh học: DNA methylation là **hallmark** quan trọng trong phân loại phân tử ung thư vú (BRCA) và thận (KIPAN). `nnz` của entmax15 ~0.3-0.5 → mỗi bệnh nhân chỉ "chú ý" 10-15 trong 32 token CpG/miRNA — sparse và có thể giải thích.

---

## 8. Cấu trúc thư mục

```
giac_project_kaggle/
├── README.md                       ← tài liệu bạn đang đọc
├── CLAUDE.md                       ← quy ước project + assistant guide
├── Phiếu_giao_nhiệm_vụ.xlsx        ← PGNV (FROZEN architecture sau khi nộp)
├── requirements.txt
├── config.py                       ← path config cho preprocess scripts standalone
│
├── train.py                        ← training loop + 5-fold CV
├── run_multi_seed.py               ← wrapper 3 seeds, aggregate mean ± std
│
├── configs/                        ← 1 YAML per dataset
│   ├── config.yaml                 (GI: COAD+ESCA+READ+STAD)
│   ├── config_brca.yaml
│   ├── config_ucec.yaml
│   ├── config_kipan.yaml
│   └── config_gi_stad_only.yaml    (STAD-only, 5 subtypes đầy đủ)
│
├── src/
│   ├── model.py                    GIACModel + ModalityCrossAttention
│   ├── models/
│   │   ├── gat_encoder.py          MultiOmicGATModule (HeteroGAT)
│   │   └── classifier.py           SubtypeClassifier + FocalLoss
│   ├── data/
│   │   ├── dataset.py              load + ANOVA + StratifiedKFold + z-score
│   │   └── graph_builder.py        build HeteroData từ 7 nguồn prior knowledge
│   └── utils.py                    metrics, plotting, checkpoint
│
├── preprocessed_data/              ← pipeline TCGA raw → final_*.csv
│   ├── main_preprocess_omics.py    orchestrator (1 lệnh chạy hết 5 datasets)
│   ├── preprocess_Gene.py
│   ├── preprocess_miRNA.py
│   ├── preprocess_CpG.py
│   ├── preprocess_labels.py        (GI)
│   ├── preprocess_labels_brca.py
│   ├── preprocess_labels_ucec.py
│   ├── preprocess_labels_kipan.py
│   ├── preprocess_labels_lgg.py
│   └── final_process_omics.py      align + filter
│
└── docs/
    ├── PIVOT_PLAN.md               strategy chính (FROZEN + audit + LGG)
    ├── MODEL_ARCHITECTURE.md       chi tiết module (slide-friendly)
    ├── RESULTS.md                  single source of truth — multi-seed log
    └── issues/
        ├── README.md
        ├── 09-model-audit.md       (model audit checklist)
        ├── 10-stad-evaluation.md
        └── 11-lgg-mofnet-comparison.md
```

---

## 9. Cài đặt và chạy

### 9.1 Môi trường

```bash
pip install -r requirements.txt
# hoặc:
pip install torch torch_geometric entmax scikit-learn pandas numpy seaborn pyyaml openpyxl
```

### 9.2 Chuẩn bị dữ liệu (1 lệnh duy nhất)

```bash
# Build cả 5 datasets từ raw TCGA → final_*.csv
python preprocessed_data/main_preprocess_omics.py --base /path/to/data_root

# Hoặc chỉ 1 dataset
python preprocessed_data/main_preprocess_omics.py --base /path/to/data_root --dataset brca

# Rebuild labels GI (4 cohort GI có pipeline label tự động)
python preprocessed_data/main_preprocess_omics.py --base /path/to/data_root \
    --dataset gi --rebuild_labels_gi
```

Đối với BRCA/UCEC/KIPAN/LGG, file `clean_labels_<ds>.csv` cần được tạo trước qua các script `preprocess_labels_*.py` riêng (đầu vào là TSV clinical từ TCGA/cBioPortal).

### 9.3 Train

```bash
# Multi-seed (recommended, 3 × 5 = 15 runs)
python run_multi_seed.py --config configs/config.yaml          # GI
python run_multi_seed.py --config configs/config_brca.yaml     # BRCA
python run_multi_seed.py --config configs/config_ucec.yaml     # UCEC
python run_multi_seed.py --config configs/config_kipan.yaml    # KIPAN

# Single-seed (debug)
python train.py --config configs/config.yaml --seed 42
```

### 9.4 Cấu trúc 1 file config

```yaml
data:
  data_dir:  "/path/data_final_<dataset>"
  graph_dir: "/path/Heterogeneous_Graph"
  emqtl_dir: "/path/Heterogeneous_Graph/<DS>_extend"   # optional, default = graph_dir/GIAC_main
  cancer_types: ["BRCA"]                                 # filter Cancer_Type column

preprocessing:
  gene_top_k:  3500
  meth_top_k:  3500
  mirna_top_k: 1881
  feature_selection_method: "anova"
  val_size:    0.15
  cv_folds:    5
  minority_boost_gene: 200
  minority_boost_meth: 150
  minority_boost_mirna: 0
  minority_classes: [1, 2, 4]

graph:
  emqtl_pval_threshold: 0.05
  max_edges_per_node:   20
  max_coregulation_edges: 10
  ppi_score_threshold:  700
  use_ppi: true
  use_reactome: true
  use_mirna: true
  use_mirna_family: true

model:
  hidden_dim: 64
  gat_heads:  4
  gat_layers: 2
  gat_dropout: 0.5
  topk_seq:    32
  ca_heads:    4
  ca_dropout:  0.4
  sparsemax_alpha: 1.5     # 1.0 = softmax, 1.5 = entmax15
  num_classes: 5
  classifier_dropout: 0.5
  final_dim:   32

training:
  epochs: 150
  batch_size: 32
  learning_rate:     1.0e-4
  max_learning_rate: 5.0e-4
  scheduler: "onecycle"
  weight_decay:          3.0e-3
  node_emb_weight_decay: 1.5e-2
  focal_gamma: 2.0
  focal_alpha: [1.0, 4.5, 1.5, 8.0, 2.0]   # overridden if use_manual_focal_alpha=false
  label_smoothing: 0.05
  balanced_sampler: false
  lambda_frobenius: 0.001
  patience: 20
  model_selection_metric: "val_f1"
  seed: 42
  loss_name: "focal"
  subtype_names: ["CIN", "GS", "MSI", "HM-SNV", "EBV"]

logging:
  save_dir: "checkpoints/"
  log_interval: 5
```

---

## 10. Nguồn dữ liệu & prior knowledge

### 10.1 Dữ liệu TCGA multi-omics

| Modality         | Nguồn                                     | Định dạng                           | Đơn vị           |
| ---------------- | ----------------------------------------- | ----------------------------------- | ---------------- |
| Gene expression  | TCGA RNA-Seq (UCSC Xena STAR pipeline)    | TSV matrix (gene × sample)          | log2(TPM+1)      |
| DNA methylation  | TCGA Illumina HumanMethylation 27k + 450k | TSV matrix (CpG × sample)           | beta value [0,1] |
| miRNA expression | TCGA miRNA-Seq (UCSC Xena, stem-loop)     | TSV matrix (miRNA × sample)         | log2(RPM+1)      |
| Clinical labels  | cBioPortal / TCGA PanCanAtlas TSV         | TSV với cột `Patient ID`, `Subtype` | text             |

### 10.2 Prior knowledge databases

| Nguồn                      | Dùng cho cạnh                                                | File                                                             |
| -------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------- |
| **emQTL (TCGA)**           | CpG → Gene                                                   | `TCGA_emQTL_<COHORT>.txt` (cohort-specific)                      |
| **STRING v12**             | Gene ↔ Gene PPI                                              | `9606.protein.links.v12.0.txt`, `9606.protein.aliases.v12.0.txt` |
| **Reactome**               | Gene ↔ Gene co-pathway                                       | `Ensembl2Reactome_All_Levels.txt`                                |
| **miRTarBase**             | miRNA → Gene                                                 | `hsa_MTI.csv`                                                    |
| **TargetScan**             | miRNA ↔ miRNA family                                         | `miR_Family_Info.txt`                                            |
| **HGNC**                   | Ensembl → gene symbol                                        | `hgnc_complete_set.txt`                                          |
| **GENCODE v36**            | Lọc protein-coding genes                                     | `gencode.v36.annotation.gtf`                                     |
| **Chen et al. 2013**       | Loại CpG cross-reactive                                      | `cross_reactive_probes.txt`                                      |
| **Illumina 450K manifest** | Loại CpG trên chrX/Y (tiền xử lý) + CpG island edges (graph) | `HumanMethylation450_manifest.csv`                               |

---

## 11. Tài liệu tham khảo chính

- **MoXGATE** (baseline được cải tiến): Modality-Aware Cross-Attention for Multi-Omic Gastrointestinal Cancer Subtype Classification — [arXiv:2506.06980](https://arxiv.org/abs/2506.06980).
- **GATv2Conv**: Brody et al., *How Attentive are Graph Attention Networks?*, ICLR 2022.
- **Entmax 1.5**: Peters et al., *Sparse Sequence-to-Sequence Models*, ACL 2019.
- **Focal Loss**: Lin et al., *Focal Loss for Dense Object Detection*, CVPR 2017.
- **STRING v12**: Szklarczyk et al., NAR 2023.
- **Reactome**: Jassal et al., NAR 2020.
- **miRTarBase 2022**: Huang et al., NAR 2022.
- **TargetScan v8**: McGeary et al., Science 2019.
- **TCGA emQTL**: methylation–expression QTL pre-computed cho từng cohort TCGA.

---

## 12. Tài liệu chi tiết

| File                                                     | Nội dung                                                                                     |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| [docs/PIVOT_PLAN.md](docs/PIVOT_PLAN.md)                 | Strategy chính: FROZEN architecture sau khi nộp PGNV; lộ trình audit + data expansion + LGG. |
| [docs/MODEL_ARCHITECTURE.md](docs/MODEL_ARCHITECTURE.md) | Chi tiết module + công thức + dimension annotation (slide-friendly).                         |
| [docs/RESULTS.md](docs/RESULTS.md)                       | Single source of truth — paste output từ `run_multi_seed.py` ở đây.                          |
| [docs/issues/](docs/issues/)                             | Issue tracker: 09 (model audit), 10 (STAD-only), 11 (LGG vs MOFNet).                         |
| [CLAUDE.md](CLAUDE.md)                                   | Quy ước project + assistant guidelines.                                                      |
