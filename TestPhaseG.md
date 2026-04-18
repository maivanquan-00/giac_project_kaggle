/kaggle/working/giac_project_kaggle
🖥️  Device: cuda
📂 Loading data từ: /kaggle/input/datasets/maivanquan/datn-2025-2/data_final
  Labels : (917, 3)
  Gene   : (917, 19930)
  Meth   : (917, 23111)
  miRNA  : (917, 1881)

  Samples sau align : 917
  Phân bố subtype   : {np.int64(0): np.int64(624), np.int64(1): np.int64(108), np.int64(2): np.int64(136), np.int64(3): np.int64(19), np.int64(4): np.int64(30)}

📐 Fold 1: gene=3000, meth=3000, mirna=1000

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3000
   CpG   nodes : 3000
   miRNA nodes : 1000
   Parsing emQTL COAD... 62,017 edges
   Parsing emQTL ESCA... 22,578 edges
   Parsing emQTL READ... 77 edges
   Parsing emQTL STAD... 23,403 edges
   CpG→Gene edges  : 108,075
   Building ENSP→symbol map từ alias file... 3,106 proteins mapped
   Parsing STRING links... 7,933 unique edges
   Gene↔Gene edges : 15,866
   Parsing hsa_MTI.csv... 41,402 edges
   miRNA→Gene edges: 41,402

🧠 Fold 1 model parameters: 1,489,800
🚀 Bắt đầu training fold 1...

🗓️  Scheduler: onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.0971  P=0.1722  R=0.1695  F1=0.0801
[Val  ] Acc=0.0946  P=0.1747  R=0.2484  F1=0.0839
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.1715  P=0.3004  R=0.3332  F1=0.1832
[Val  ] Acc=0.1757  P=0.2876  R=0.4372  F1=0.1862
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.3460  P=0.3464  R=0.5060  F1=0.3001
[Val  ] Acc=0.3919  P=0.3767  R=0.5903  F1=0.3721
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.5372  P=0.4359  R=0.6446  F1=0.4496
[Val  ] Acc=0.5000  P=0.5386  R=0.5547  F1=0.4693
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.7329  P=0.5788  R=0.8317  F1=0.6396
[Val  ] Acc=0.6757  P=0.6022  R=0.7169  F1=0.6290
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.8316  P=0.7177  R=0.9291  F1=0.7712
[Val  ] Acc=0.7703  P=0.7078  R=0.7449  F1=0.7206
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.8771  P=0.7822  R=0.9333  F1=0.8382
[Val  ] Acc=0.7568  P=0.5916  R=0.6449  F1=0.6115
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.9272  P=0.8398  R=0.9684  F1=0.8924
[Val  ] Acc=0.8514  P=0.8444  R=0.7871  F1=0.7960
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  40/150
[Train] Acc=0.9332  P=0.8696  R=0.9761  F1=0.9138
[Val  ] Acc=0.8243  P=0.8133  R=0.7609  F1=0.7644
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  45/150
[Train] Acc=0.9545  P=0.8889  R=0.9829  F1=0.9297
[Val  ] Acc=0.8243  P=0.8242  R=0.7791  F1=0.7794
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  50/150
[Train] Acc=0.9666  P=0.9041  R=0.9902  F1=0.9427
[Val  ] Acc=0.8514  P=0.8450  R=0.7871  F1=0.7951
Fold 1 | Epoch  55/150
[Train] Acc=0.9757  P=0.9243  R=0.9929  F1=0.9560
[Val  ] Acc=0.8514  P=0.8450  R=0.7871  F1=0.7951
Fold 1 | Epoch  60/150
[Train] Acc=0.9788  P=0.9513  R=0.9900  F1=0.9697
[Val  ] Acc=0.9054  P=0.9120  R=0.8031  F1=0.8328
⏹️  Early stopping tại epoch 64 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8424  P=0.8071  R=0.8036  F1=0.7802
✅ Best val F1: 0.8328
✅ Test F1:     0.7802

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9381    0.8480    0.8908       125
          GS     0.5806    0.8182    0.6792        22
         MSI     0.7667    0.8519    0.8070        27
      HM-SNV     1.0000    0.5000    0.6667         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.8424       184
   macro avg     0.8071    0.8036    0.7802       184
weighted avg     0.8654    0.8424    0.8472       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.3899  std=0.0762  min=0.3092  max=0.5273
   meth : mean=0.2950  std=0.0443  min=0.2169  max=0.3429
   mirna: mean=0.3151  std=0.0319  min=0.2558  max=0.3478

📐 Fold 2: gene=3000, meth=3000, mirna=1000

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3000
   CpG   nodes : 3000
   miRNA nodes : 1000
   Parsing emQTL COAD... 60,494 edges
   Parsing emQTL ESCA... 22,789 edges
   Parsing emQTL READ... 77 edges
   Parsing emQTL STAD... 23,759 edges
   CpG→Gene edges  : 107,119
   Building ENSP→symbol map từ alias file... 3,107 proteins mapped
   Parsing STRING links... 7,824 unique edges
   Gene↔Gene edges : 15,648
   Parsing hsa_MTI.csv... 41,033 edges
   miRNA→Gene edges: 41,033

🧠 Fold 2 model parameters: 1,489,800
🚀 Bắt đầu training fold 2...

🗓️  Scheduler: onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.1684  P=0.1831  R=0.2478  F1=0.1161
[Val  ] Acc=0.1486  P=0.2194  R=0.1764  F1=0.0883
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.2322  P=0.2835  R=0.3802  F1=0.2055
[Val  ] Acc=0.1351  P=0.3029  R=0.2928  F1=0.1391
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.3536  P=0.3435  R=0.4623  F1=0.3031
[Val  ] Acc=0.3108  P=0.3414  R=0.4379  F1=0.2750
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.5539  P=0.4521  R=0.7074  F1=0.4829
[Val  ] Acc=0.3784  P=0.3828  R=0.4438  F1=0.3288
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.6904  P=0.5541  R=0.8273  F1=0.6102
[Val  ] Acc=0.7297  P=0.5113  R=0.6267  F1=0.5414
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.7845  P=0.6797  R=0.8970  F1=0.7395
[Val  ] Acc=0.8108  P=0.6526  R=0.7650  F1=0.6912
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.8528  P=0.7391  R=0.9166  F1=0.7980
[Val  ] Acc=0.8378  P=0.6009  R=0.6952  F1=0.6384
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.9181  P=0.8482  R=0.9609  F1=0.8963
[Val  ] Acc=0.8378  P=0.7894  R=0.7730  F1=0.7566
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  40/150
[Train] Acc=0.9347  P=0.8890  R=0.9744  F1=0.9252
[Val  ] Acc=0.8649  P=0.8143  R=0.7810  F1=0.7743
Fold 2 | Epoch  45/150
[Train] Acc=0.9560  P=0.8867  R=0.9806  F1=0.9281
[Val  ] Acc=0.8649  P=0.8143  R=0.7810  F1=0.7743
Fold 2 | Epoch  50/150
[Train] Acc=0.9651  P=0.9286  R=0.9876  F1=0.9554
[Val  ] Acc=0.8649  P=0.8143  R=0.7810  F1=0.7743
⏹️  Early stopping tại epoch 52 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.8696  P=0.7485  R=0.8283  F1=0.7739
✅ Best val F1: 0.8125
✅ Test F1:     0.7739

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9732    0.8720    0.9198       125
          GS     0.6774    0.9545    0.7925        22
         MSI     0.7586    0.8148    0.7857        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     0.6667    1.0000    0.8000         6

    accuracy                         0.8696       184
   macro avg     0.7485    0.8283    0.7739       184
weighted avg     0.8897    0.8696    0.8734       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.3765  std=0.1362  min=0.2493  max=0.6286
   meth : mean=0.3117  std=0.0743  min=0.1793  max=0.3873
   mirna: mean=0.3118  std=0.0621  min=0.1913  max=0.3714

📐 Fold 3: gene=3000, meth=3000, mirna=1000

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3000
   CpG   nodes : 3000
   miRNA nodes : 1000
   Parsing emQTL COAD... 60,602 edges
   Parsing emQTL ESCA... 22,748 edges
   Parsing emQTL READ... 76 edges
   Parsing emQTL STAD... 23,388 edges
   CpG→Gene edges  : 106,814
   Building ENSP→symbol map từ alias file... 3,101 proteins mapped
   Parsing STRING links... 7,922 unique edges
   Gene↔Gene edges : 15,844
   Parsing hsa_MTI.csv... 42,224 edges
   miRNA→Gene edges: 42,224

🧠 Fold 3 model parameters: 1,489,800
🚀 Bắt đầu training fold 3...

🗓️  Scheduler: onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.3955  P=0.2234  R=0.2301  F1=0.1980
[Val  ] Acc=0.5541  P=0.2132  R=0.4520  F1=0.2446
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.4864  P=0.2898  R=0.3560  F1=0.2738
[Val  ] Acc=0.5946  P=0.3439  R=0.4470  F1=0.3328
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.3909  P=0.3373  R=0.4796  F1=0.3049
[Val  ] Acc=0.3919  P=0.4848  R=0.5417  F1=0.3229
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.5697  P=0.4588  R=0.6749  F1=0.4958
[Val  ] Acc=0.6351  P=0.5200  R=0.7535  F1=0.5553
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.7121  P=0.6087  R=0.8228  F1=0.6553
[Val  ] Acc=0.6486  P=0.5754  R=0.7716  F1=0.6095
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.8394  P=0.7338  R=0.9341  F1=0.7910
[Val  ] Acc=0.8514  P=0.6857  R=0.8600  F1=0.7436
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.9045  P=0.8122  R=0.9613  F1=0.8678
[Val  ] Acc=0.8649  P=0.7005  R=0.8498  F1=0.7515
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9439  P=0.8754  R=0.9772  F1=0.9182
[Val  ] Acc=0.8649  P=0.7057  R=0.8498  F1=0.7523
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  40/150
[Train] Acc=0.9667  P=0.9376  R=0.9881  F1=0.9607
[Val  ] Acc=0.8649  P=0.7960  R=0.8316  F1=0.7750
Fold 3 | Epoch  45/150
[Train] Acc=0.9667  P=0.9205  R=0.9806  F1=0.9472
[Val  ] Acc=0.8514  P=0.7896  R=0.8458  F1=0.7707
Fold 3 | Epoch  50/150
[Train] Acc=0.9788  P=0.9356  R=0.9938  F1=0.9628
[Val  ] Acc=0.8784  P=0.8058  R=0.8538  F1=0.7880
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  55/150
[Train] Acc=0.9848  P=0.9608  R=0.9897  F1=0.9748
[Val  ] Acc=0.8514  P=0.7807  R=0.8276  F1=0.7648
Fold 3 | Epoch  60/150
[Train] Acc=0.9909  P=0.9857  R=0.9973  F1=0.9912
[Val  ] Acc=0.8649  P=0.7960  R=0.8316  F1=0.7750
Fold 3 | Epoch  65/150
[Train] Acc=0.9788  P=0.9429  R=0.9916  F1=0.9657
[Val  ] Acc=0.8514  P=0.7788  R=0.8418  F1=0.7674
⏹️  Early stopping tại epoch 65 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8525  P=0.7052  R=0.7443  F1=0.7233
✅ Best val F1: 0.7880
✅ Test F1:     0.7233

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9174    0.8880    0.9024       125
          GS     0.5217    0.5714    0.5455        21
         MSI     0.8966    0.9286    0.9123        28
      HM-SNV     0.3333    0.3333    0.3333         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8525       183
   macro avg     0.7052    0.7443    0.7233       183
weighted avg     0.8572    0.8525    0.8543       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.3711  std=0.0601  min=0.3123  max=0.4926
   meth : mean=0.3239  std=0.0438  min=0.2379  max=0.3680
   mirna: mean=0.3050  std=0.0163  min=0.2695  max=0.3197

📐 Fold 4: gene=3000, meth=3000, mirna=1000

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3000
   CpG   nodes : 3000
   miRNA nodes : 1000
   Parsing emQTL COAD... 60,577 edges
   Parsing emQTL ESCA... 23,154 edges
   Parsing emQTL READ... 73 edges
   Parsing emQTL STAD... 23,374 edges
   CpG→Gene edges  : 107,178
   Building ENSP→symbol map từ alias file... 3,104 proteins mapped
   Parsing STRING links... 8,055 unique edges
   Gene↔Gene edges : 16,110
   Parsing hsa_MTI.csv... 41,880 edges
   miRNA→Gene edges: 41,880

🧠 Fold 4 model parameters: 1,489,800
🚀 Bắt đầu training fold 4...

🗓️  Scheduler: onecycle
Fold 4 | Epoch   1/150
[Train] Acc=0.1697  P=0.2184  R=0.2541  F1=0.1395
[Val  ] Acc=0.1622  P=0.2002  R=0.2724  F1=0.1115
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.3076  P=0.2786  R=0.3973  F1=0.2199
[Val  ] Acc=0.3784  P=0.3184  R=0.3688  F1=0.2426
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.4379  P=0.3356  R=0.5022  F1=0.3206
[Val  ] Acc=0.5135  P=0.3454  R=0.4878  F1=0.3419
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.5955  P=0.4595  R=0.6940  F1=0.4975
[Val  ] Acc=0.5811  P=0.3966  R=0.5544  F1=0.4268
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.7288  P=0.5805  R=0.8406  F1=0.6530
[Val  ] Acc=0.6892  P=0.5187  R=0.6147  F1=0.5511
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.8242  P=0.7475  R=0.9176  F1=0.8079
[Val  ] Acc=0.8108  P=0.5733  R=0.6832  F1=0.6170
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.8985  P=0.8271  R=0.9532  F1=0.8769
[Val  ] Acc=0.8378  P=0.6003  R=0.7053  F1=0.6417
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.9212  P=0.8410  R=0.9524  F1=0.8862
[Val  ] Acc=0.8514  P=0.6110  R=0.7093  F1=0.6508
Fold 4 | Epoch  40/150
[Train] Acc=0.9606  P=0.8844  R=0.9826  F1=0.9272
[Val  ] Acc=0.8649  P=0.6113  R=0.7133  F1=0.6530
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  45/150
[Train] Acc=0.9682  P=0.9204  R=0.9906  F1=0.9527
[Val  ] Acc=0.8649  P=0.6113  R=0.7133  F1=0.6530
Fold 4 | Epoch  50/150
[Train] Acc=0.9894  P=0.9596  R=0.9969  F1=0.9775
[Val  ] Acc=0.8649  P=0.6113  R=0.7133  F1=0.6530
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  55/150
[Train] Acc=0.9864  P=0.9672  R=0.9944  F1=0.9802
[Val  ] Acc=0.8649  P=0.6113  R=0.7133  F1=0.6530
Fold 4 | Epoch  60/150
[Train] Acc=0.9924  P=0.9763  R=0.9962  F1=0.9859
[Val  ] Acc=0.8784  P=0.6282  R=0.7173  F1=0.6630
Fold 4 | Epoch  65/150
[Train] Acc=0.9955  P=0.9713  R=0.9987  F1=0.9840
[Val  ] Acc=0.8649  P=0.6113  R=0.7133  F1=0.6530
⏹️  Early stopping tại epoch 68 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.8470  P=0.6657  R=0.7241  F1=0.6897
✅ Best val F1: 0.6630
✅ Test F1:     0.6897

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9298    0.8480    0.8870       125
          GS     0.5862    0.8095    0.6800        21
         MSI     0.8125    0.9630    0.8814        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8470       183
   macro avg     0.6657    0.7241    0.6897       183
weighted avg     0.8551    0.8470    0.8468       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.3754  std=0.0242  min=0.3464  max=0.4222
   meth : mean=0.3348  std=0.0202  min=0.2964  max=0.3594
   mirna: mean=0.2898  std=0.0040  min=0.2814  max=0.2941

📐 Fold 5: gene=3000, meth=3000, mirna=1000

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3000
   CpG   nodes : 3000
   miRNA nodes : 1000
   Parsing emQTL COAD... 60,396 edges
   Parsing emQTL ESCA... 22,795 edges
   Parsing emQTL READ... 75 edges
   Parsing emQTL STAD... 23,738 edges
   CpG→Gene edges  : 107,004
   Building ENSP→symbol map từ alias file... 3,098 proteins mapped
   Parsing STRING links... 7,873 unique edges
   Gene↔Gene edges : 15,746
   Parsing hsa_MTI.csv... 41,403 edges
   miRNA→Gene edges: 41,403

🧠 Fold 5 model parameters: 1,489,800
🚀 Bắt đầu training fold 5...

🗓️  Scheduler: onecycle
Fold 5 | Epoch   1/150
[Train] Acc=0.0970  P=0.1999  R=0.2496  F1=0.1310
[Val  ] Acc=0.0541  P=0.0709  R=0.1667  F1=0.0748
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.1864  P=0.2727  R=0.3746  F1=0.1829
[Val  ] Acc=0.1622  P=0.1793  R=0.3907  F1=0.1385
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.4091  P=0.3469  R=0.4781  F1=0.3259
[Val  ] Acc=0.3108  P=0.2961  R=0.3914  F1=0.2615
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.5470  P=0.4990  R=0.6985  F1=0.5190
[Val  ] Acc=0.5541  P=0.4572  R=0.6707  F1=0.5023
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.6439  P=0.5655  R=0.8248  F1=0.6022
[Val  ] Acc=0.7162  P=0.6045  R=0.7734  F1=0.6486
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.8167  P=0.7148  R=0.9072  F1=0.7617
[Val  ] Acc=0.7973  P=0.5955  R=0.6832  F1=0.6278
Fold 5 | Epoch  30/150
[Train] Acc=0.8682  P=0.7593  R=0.9373  F1=0.8177
[Val  ] Acc=0.7568  P=0.5667  R=0.6530  F1=0.5956
Fold 5 | Epoch  35/150
[Train] Acc=0.9182  P=0.8484  R=0.9744  F1=0.8996
[Val  ] Acc=0.8108  P=0.6083  R=0.6832  F1=0.6362
⏹️  Early stopping tại epoch 35 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.6776  P=0.5549  R=0.7701  F1=0.6098
✅ Best val F1: 0.6486
✅ Test F1:     0.6098

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9070    0.6290    0.7429       124
          GS     0.3429    0.5455    0.4211        22
         MSI     0.6579    0.9259    0.7692        27
      HM-SNV     0.2000    0.7500    0.3158         4
         EBV     0.6667    1.0000    0.8000         6

    accuracy                         0.6776       183
   macro avg     0.5549    0.7701    0.6098       183
weighted avg     0.7791    0.6776    0.7006       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.4193  std=0.2287  min=0.1795  max=0.7947
   meth : mean=0.3014  std=0.1594  min=0.0689  max=0.5042
   mirna: mean=0.2794  std=0.0733  min=0.1364  max=0.3674

📈 5-fold CV summary
  ACCURACY : mean=0.8178  std=0.0707
  PRECISION: mean=0.6963  std=0.0849
  RECALL   : mean=0.7741  std=0.0380
  F1       : mean=0.7154  std=0.0624


  📂 Loading data từ: /kaggle/input/datasets/maivanquan/datn-2025-2/data_final
  Labels : (917, 3)
  Gene   : (917, 19930)
  Meth   : (917, 23111)
  miRNA  : (917, 1881)

  Samples sau align : 917
  Phân bố subtype   : {np.int64(0): np.int64(624), np.int64(1): np.int64(108), np.int64(2): np.int64(136), np.int64(3): np.int64(19), np.int64(4): np.int64(30)}

📊 Split: train=659, val=74, test=184

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3000
   CpG   nodes : 3000
   miRNA nodes : 1000
   Parsing emQTL COAD... 60,476 edges
   Parsing emQTL ESCA... 22,642 edges
   Parsing emQTL READ... 77 edges
   Parsing emQTL STAD... 23,252 edges
   CpG→Gene edges  : 106,447
   Building ENSP→symbol map từ alias file... 3,104 proteins mapped
   Parsing STRING links... 8,013 unique edges
   Gene↔Gene edges : 16,026
   Parsing hsa_MTI.csv... 41,088 edges
   miRNA→Gene edges: 41,088
✅ Loaded: /kaggle/working/checkpoints/best_model_fold_1.pt

📋 Classification Report:
              precision    recall  f1-score   support

         CIN     0.8712    0.9200    0.8949       125
          GS     0.6667    0.4545    0.5405        22
         MSI     0.8421    0.5926    0.6957        27
      HM-SNV     0.6000    0.7500    0.6667         4
         EBV     0.4615    1.0000    0.6316         6

    accuracy                         0.8152       184
   macro avg     0.6883    0.7434    0.6859       184
weighted avg     0.8232    0.8152    0.8098       184

[Test] Acc=0.8152  P=0.6883  R=0.7434  F1=0.6859

🔍 Patient Modality Gate Statistics (N=184)
   Gene expression     : mean=0.3837  std=0.0724
   DNA methylation     : mean=0.2985  std=0.0424
   miRNA               : mean=0.3178  std=0.0301

✔️  Accuracy: 0.8152
   Correct: 150 / 184