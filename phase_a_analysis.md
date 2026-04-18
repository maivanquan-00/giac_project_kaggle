# 🔬 Phase A Final Analysis — 5-Fold Ablation

## 1. Kết quả chính

### Ablation 5-fold cross-validated (mean ± std)

| Config        | Val F1          | Test Acc        | Test F1         | Std F1       |
| ------------- | --------------- | --------------- | --------------- | ------------ |
| **meth_only** | **0.693±0.060** | **0.737±0.022** | **0.643±0.045** | thấp nhất    |
| gene_only     | 0.663±0.040     | 0.730±0.035     | 0.605±0.059     |              |
| gene+meth     | 0.640±0.046     | 0.727±0.030     | 0.601±0.067     |              |
| gene+mirna    | 0.639±0.048     | 0.705±0.032     | 0.598±0.073     |              |
| all           | 0.593±0.128     | 0.669±0.146     | 0.531±0.162     | **cao nhất** |
| mirna_only    | 0.403±0.098     | 0.501±0.150     | 0.391±0.135     |              |

### So sánh với full training (150 epochs):
|                         | Test Acc    | Macro F1    |
| ----------------------- | ----------- | ----------- |
| Full train (all, 150ep) | 0.830±0.018 | 0.698±0.052 |
| Ablation (all, 80ep)    | 0.669±0.146 | 0.531±0.162 |

> [!NOTE]
> Ablation dùng 80 epochs / patience 15 nên absolute numbers thấp hơn full training. Nhưng **thứ tự xếp hạng** giữa các config cùng budget là thông tin quan trọng nhất.

---

## 2. Bốn kết luận từ dữ liệu

### ① Methylation là modality mạnh nhất và ổn định nhất
- Test F1 = **0.643±0.045** (std thấp nhất trong tất cả configs)
- Test Acc = 0.737±0.022 (variance thấp nhất)
- Là modality duy nhất consistently > 0.55 F1 ở mọi fold

### ② Gene là modality mạnh thứ hai
- Test F1 = 0.605±0.059
- Có complementary signal so với meth (nhìn từ per-class: gene tốt hơn meth ở một số classes nhất định)

### ③ miRNA gần như không có tín hiệu discriminative
- Test F1 = 0.391±0.135 (variance cao, đôi khi `<` 0.14)
- Thêm miRNA vào gene **không cải thiện**: gene+mirna (0.598) ≈ gene_only (0.605)
- Patient gate đã tự học suppress miRNA (mean weight 0.06-0.20)

### ④ Fusion cơ chế hiện tại PHÁ HỦY tín hiệu
- `all` (0.531) **tệ hơn** mọi single-modality config (trừ mirna_only)
- `gene+meth` (0.601) **tệ hơn** cả `meth_only` (0.643) và `gene_only` (0.605)
- Variance của `all` là cao nhất (0.162) → fusion không ổn định
- cross-attention + patient gate + 0.5/0.5 blending đang tạo conflict thay vì synergy

---

## 3. Nguyên nhân gốc rễ

```
1. Cross-attention giữa 3 modalities → noise interference
   (đặc biệt miRNA, modality yếu, gây nhiễu cho gene/meth)

2. Dual-path fusion (cross-attn 50% + patient gate 50%) → 
   hai nhánh "tranh nhau" thay vì bổ sung

3. Global modality weights frozen (temperature=0.1) →
   model không thể tự loại bỏ miRNA ở cross-attention level

4. Feature selection chỉ dùng variance → 
   không lọc được features có discriminative power thấp
```

---

## 4. Đề xuất Phase B — 3 thay đổi cốt lõi

### B1: Đơn giản hóa Fusion (Impact lớn nhất)

**Hiện tại:**
```
cross_attn(gene, meth, mirna) → fused_1
patient_gate(gene, meth, mirna) → fused_2
final = 0.5 * fused_1 + 0.5 * fused_2  ← 2 nhánh xung đột
```

**Đề xuất — Gated Concatenation:**
```
gate = softmax(MLP(concat[gene, meth, mirna]))  # (B, 3)
stacked = stack([gene, meth, mirna])             # (B, 3, D)
fused = sum(stacked * gate)                      # (B, D)
logits = classifier(fused)
```

- Bỏ cross-attention hoàn toàn (nó đang gây hại)
- Giữ patient gate (nó đang hoạt động, std cao)  
- Bỏ dual-path blending 50/50

### B2: Supervised Feature Selection (Impact trung bình)

Thay variance-only → ANOVA F-test trên train set.
Meth (modality mạnh nhất) sẽ được chọn features có discriminative power cao hơn.

### B3: Tăng Regularization (Impact nhỏ nhưng cần thiết)

- Tăng dropout: 0.3 → 0.4
- Label smoothing: 0.05-0.1 trong focal loss
- Weight decay: 1e-4 → 5e-4

---

## 5. Về miRNA — Giữ hay bỏ?

> [!IMPORTANT]
> **Đề xuất: Giữ miRNA nhưng để model tự downweight.**
> 
> Lý do:
> - Đây là bài toán multi-omics 5 loại. Bỏ hoàn toàn 1 modality không tốt cho thesis.  
> - Patient gate đã chứng minh nó CÓ THỂ suppress miRNA khi cần (mean weight 0.06 ở fold 5).
> - Nếu fix fusion đúng cách (B1), model sẽ tự gán trọng số thấp cho miRNA.
> - Fold 4 cho thấy mirna_only F1=0.54, nghĩa là ở một số data splits miRNA VẪN có tín hiệu.

---

## 6. Kỳ vọng sau Phase B

| Metric               | Hiện tại | Dự kiến sau B1-B3 |
| -------------------- | -------- | ----------------- |
| Test Accuracy        | 0.830    | 0.85-0.87         |
| Macro F1 (5 classes) | 0.698    | 0.75-0.80         |
| Weighted F1          | ~0.84    | 0.87-0.90         |

> [!NOTE]
> Macro F1 = 0.85 với 5 classes (HM-SNV có 19 samples) là cực kỳ khó.
> Mục tiêu thực tế: **Macro F1 ≥ 0.78, Accuracy ≥ 0.85**.
