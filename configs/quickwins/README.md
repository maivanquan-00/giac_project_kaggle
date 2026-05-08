# Quick Wins — Config Variants cho [Issue 07](../../docs/issues/07-quick-wins-config.md)

Mỗi file ở đây là 1 variant của config gốc, chỉ thay 1-2 hyperparameter để test 1 quick win độc lập.

## Quy ước naming

```
configs/quickwins/<dataset>_<exp_id>_<short_desc>.yaml

Ví dụ:
  gi_07a_focal12.yaml      = GI + Quick win 07.A (focal_alpha[3]=12)
  ucec_07cd_emqtl.yaml     = UCEC + 07.C + 07.D (max_edges=50, pval=0.20)
```

## Cách chạy

```bash
# Chạy 1 quick win với multi-seed:
python run_multi_seed.py --config configs/quickwins/gi_07a_focal12.yaml

# Hoặc chạy single seed (debug nhanh):
python train.py --config configs/quickwins/gi_07a_focal12.yaml --seed 42

# Compare với baseline:
python run_multi_seed.py --config configs/config.yaml          # baseline
python run_multi_seed.py --config configs/quickwins/gi_07a_focal12.yaml  # +07.A
```

## Bảng quick wins hiện có

| File | Dataset | Thay đổi vs base config | Lý do | Risk |
|------|---------|-------------------------|-------|------|
| `gi_07a_focal12.yaml` | GI | `focal_alpha=[1,4.5,1.5,12,2]` + `use_manual_focal_alpha=true` | Push HM-SNV recall lên (n=19) | Có thể hại class khác |
| `gi_07b_smoothing.yaml` | GI | `label_smoothing: 0.10` | Giảm overconfidence → minority recall ↑ | Thấp |
| `gi_08a_light_regularization.yaml` | GI | dropout/weight decay/Frobenius giảm đồng thời | Test hypothesis GIAC đang underfit vì over-regularized | Trung bình |
| `gi_08b_light_reg_focal_smoothing.yaml` | GI | 08.A + manual alpha mean≈1 + smoothing=0.10 | Conservative minority push sau khi giảm regularization | Trung bình |
| `gi_08c_balanced_sampler_ce.yaml` | GI | balanced sampler + CE + no class weights | Test alternative không dùng focal/class-weight để tránh minority decision quá nhiễu | Trung bình |
| `brca_07b_smoothing.yaml` | BRCA | `label_smoothing: 0.10` | Stability cho LumA/Normal | Thấp |
| `brca_07f_valsize.yaml` | BRCA | `val_size: 0.20` | Val less noisy → best_epoch chính xác → fix Fold-4 | Thấp (mất 5% train data) |
| `ucec_07c_max_edges.yaml` | UCEC | `max_edges_per_node: 50` | UCEC có hub CpG có thể bị cap=20 | Rất thấp |
| `ucec_07d_pval.yaml` | UCEC | `emqtl_pval_threshold: 0.20` | Tăng từ ~3K lên ~6-8K edges | Có thể tăng noise |
| `ucec_07cd_combo.yaml` | UCEC | 07.C + 07.D | Combined emQTL boost | — |
| `ucec_07b_smoothing.yaml` | UCEC | `label_smoothing: 0.10` | POLE stability | Thấp |
| `kipan_07b_smoothing.yaml` | KIPAN | `label_smoothing: 0.10` | KICH stability | Thấp |
| `kipan_07e_minority02.yaml` | KIPAN | `minority_classes: [0, 2]` | Boost cả KIRP cùng KICH | Trung tính |
| `kipan_07g_topk48.yaml` | KIPAN | `topk_seq: 48` | OPUS_PROMPT evidence: cải thiện KICH F1 floor 0.75→0.81 | Thấp |

## Quy tắc test

1. **Mỗi exp chạy multi-seed** (3 seeds × 5 folds = 15 runs). Single-seed không đủ tin cậy.
2. **Compare với baseline cùng 3 seeds** — chứ không so với số "best run cũ".
3. **Quy tắc keep:** ΔF1 macro > +0.005 với std không tăng → KEEP.
4. **Quy tắc reject:** ΔF1 macro < +0.000 hoặc std tăng > 0.02 → REJECT.
5. Với GI, đọc thêm bảng **Per-class F1** trong output mới. Một config chỉ đáng giữ nếu macro F1 tăng hoặc nếu HM-SNV/GS tăng rõ mà CIN/MSI không sụp mạnh.

## GI screening đã chạy — không chạy lại

Các config dưới đây đã chạy **seed 42 × 5-fold** ngày 2026-05-08. Baseline GIAC seed 42 trước đó là **macro F1 ≈ 0.6933**.

| Config | Macro F1 | Weighted F1 | Per-fold macro F1 | Per-class F1 mean `[CIN, GS, MSI, HM, EBV]` | Quyết định |
|--------|----------|-------------|-------------------|---------------------------------------------|------------|
| `gi_08b_light_reg_focal_smoothing.yaml` | **0.7199** | **0.8626** | `[0.7783, 0.6986, 0.7254, 0.6835, 0.7136]` | `[0.9137, 0.6669, 0.8508, 0.1833, 0.9846]` | **KEEP — chạy full 3 seeds** |
| `gi_08a_light_regularization.yaml` | 0.6849 | 0.8501 | `[0.7576, 0.7142, 0.6498, 0.6549, 0.6479]` | `[0.9047, 0.6276, 0.8650, 0.1308, 0.8965]` | REJECT riêng lẻ; 08B giữ phần light-reg |
| `gi_08c_balanced_sampler_ce.yaml` | 0.6648 | 0.8447 | `[0.6491, 0.6633, 0.6552, 0.6516, 0.7050]` | `[0.8992, 0.6403, 0.8574, 0.0267, 0.9007]` | REJECT — HM-SNV collapse, macro giảm |
| `gi_07a_focal12.yaml` | 0.6320 | 0.8097 | `[0.5130, 0.8515, 0.5770, 0.6257, 0.5928]` | `[0.8858, 0.5954, 0.7258, 0.1864, 0.7664]` | **REJECT mạnh** — rất unstable, hại MSI/EBV |

Kết luận screening:

- `gi_08b_light_reg_focal_smoothing.yaml` là config duy nhất vượt baseline seed 42 rõ ràng: `+0.0266 macro F1`.
- `gi_08a` xác nhận giảm regularization có ích một phần, nhưng một mình chưa đủ.
- `gi_08c` cho thấy balanced sampler + CE không hợp với GIAC trên GI.
- `gi_07a` chứng minh focal alpha scale lớn `[1,4.5,1.5,12,2]` làm loss mất cân bằng; tránh lặp lại hướng tăng alpha tuyệt đối quá mạnh.
- Các file output đã lưu ở `configs/quickwins/gi_*_output.md`; không cần chạy lại 4 config này trừ khi code training thay đổi lớn.

## Thứ tự chạy tiếp cho GI

Chạy full multi-seed cho config tốt nhất:

```bash
python run_multi_seed.py --config configs/quickwins/gi_08b_light_reg_focal_smoothing.yaml --seeds 42 123 2024
```

Nếu 08B full vẫn tốt, bước sau mới tạo biến thể rất hẹp quanh 08B, ví dụ:

- `gi_08b_gamma15`: giữ 08B, đổi `focal_gamma: 2.0 -> 1.5`.
- `gi_08b_no_smoothing`: giữ 08B, đổi `label_smoothing: 0.10 -> 0.05`.
- `gi_08b_alpha_hm25`: giữ 08B, giảm HM alpha `3.20 -> 2.50` để xem HM-SNV noise có giảm không.

Không ưu tiên chạy `gi_07b_smoothing.yaml` một mình nữa, vì screening cho thấy tổ hợp light-reg + manual alpha scale nhỏ + smoothing mới là phần có tín hiệu.

## Combined config

Sau khi sàng lọc các quick win work, tạo file `<dataset>_combined_final.yaml` áp dụng tất cả wins → run 1 lần cuối.

| Dataset | Combined config | Best multi-seed F1 |
|---------|-----------------|---------------------|
| GI | `gi_combined_final.yaml` (TBD) | TBD |
| BRCA | `brca_combined_final.yaml` (TBD) | TBD |
| UCEC | `ucec_combined_final.yaml` (TBD) | TBD |
| KIPAN | `kipan_combined_final.yaml` (TBD) | TBD |
