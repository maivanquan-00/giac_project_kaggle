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
[Train] Acc=0.3399  P=0.3429  R=0.5043  F1=0.2954
[Val  ] Acc=0.3919  P=0.3740  R=0.5903  F1=0.3705
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.5341  P=0.4403  R=0.6629  F1=0.4563
[Val  ] Acc=0.5135  P=0.5412  R=0.5587  F1=0.4750
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.7238  P=0.5732  R=0.8253  F1=0.6306
[Val  ] Acc=0.6351  P=0.5837  R=0.7049  F1=0.6048
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.8376  P=0.7253  R=0.9207  F1=0.7767
[Val  ] Acc=0.7568  P=0.6740  R=0.7409  F1=0.6981
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.8816  P=0.8019  R=0.9427  F1=0.8537
[Val  ] Acc=0.7703  P=0.5965  R=0.6489  F1=0.6171
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.9241  P=0.8371  R=0.9713  F1=0.8914
[Val  ] Acc=0.8378  P=0.8350  R=0.7831  F1=0.7885
Fold 1 | Epoch  40/150
[Train] Acc=0.9363  P=0.8870  R=0.9791  F1=0.9249
[Val  ] Acc=0.8378  P=0.8336  R=0.7831  F1=0.7870
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  45/150
[Train] Acc=0.9575  P=0.8918  R=0.9838  F1=0.9322
[Val  ] Acc=0.8378  P=0.8336  R=0.7831  F1=0.7870
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  50/150
[Train] Acc=0.9666  P=0.9106  R=0.9880  F1=0.9455
[Val  ] Acc=0.8649  P=0.8592  R=0.7911  F1=0.8039
Fold 1 | Epoch  55/150
[Train] Acc=0.9742  P=0.9236  R=0.9903  F1=0.9545
[Val  ] Acc=0.8649  P=0.8592  R=0.7911  F1=0.8039
Fold 1 | Epoch  60/150
[Train] Acc=0.9833  P=0.9577  R=0.9935  F1=0.9748
[Val  ] Acc=0.9189  P=0.9456  R=0.8071  F1=0.8443
⏹️  Early stopping tại epoch 64 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8370  P=0.7388  R=0.7962  F1=0.7569
✅ Best val F1: 0.8443
✅ Test F1:     0.7569

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9381    0.8480    0.8908       125
          GS     0.5806    0.8182    0.6792        22
         MSI     0.7586    0.8148    0.7857        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.8370       184
   macro avg     0.7388    0.7962    0.7569       184
weighted avg     0.8570    0.8370    0.8420       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.3959  std=0.0826  min=0.3087  max=0.5449
   meth : mean=0.2924  std=0.0473  min=0.2091  max=0.3434
   mirna: mean=0.3117  std=0.0353  min=0.2461  max=0.3479

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
[Train] Acc=0.3551  P=0.3444  R=0.4627  F1=0.3050
[Val  ] Acc=0.3108  P=0.3328  R=0.4238  F1=0.2649
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.5524  P=0.4424  R=0.6866  F1=0.4711
[Val  ] Acc=0.4189  P=0.4281  R=0.5023  F1=0.3869
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.6813  P=0.5379  R=0.7979  F1=0.5926
[Val  ] Acc=0.7568  P=0.5250  R=0.6530  F1=0.5599
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.7800  P=0.6677  R=0.8979  F1=0.7317
[Val  ] Acc=0.8108  P=0.6458  R=0.7650  F1=0.6867
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.8604  P=0.7484  R=0.9076  F1=0.8021
[Val  ] Acc=0.8378  P=0.6911  R=0.7912  F1=0.7309
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.9241  P=0.8481  R=0.9648  F1=0.8983
[Val  ] Acc=0.8514  P=0.8009  R=0.7952  F1=0.7717
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  40/150
[Train] Acc=0.9347  P=0.8711  R=0.9744  F1=0.9145
[Val  ] Acc=0.8649  P=0.8143  R=0.7810  F1=0.7743
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  45/150
[Train] Acc=0.9605  P=0.9144  R=0.9820  F1=0.9452
[Val  ] Acc=0.8649  P=0.8047  R=0.7810  F1=0.7691
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  50/150
[Train] Acc=0.9697  P=0.9338  R=0.9889  F1=0.9592
[Val  ] Acc=0.8649  P=0.8143  R=0.7810  F1=0.7743
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  55/150
[Train] Acc=0.9818  P=0.9378  R=0.9947  F1=0.9644
[Val  ] Acc=0.8784  P=0.8211  R=0.7992  F1=0.7864
Fold 2 | Epoch  60/150
[Train] Acc=0.9818  P=0.9327  R=0.9947  F1=0.9615
[Val  ] Acc=0.8784  P=0.8122  R=0.7992  F1=0.7811
Fold 2 | Epoch  65/150
[Train] Acc=0.9863  P=0.9585  R=0.9938  F1=0.9751
[Val  ] Acc=0.8784  P=0.8211  R=0.7992  F1=0.7864
⏹️  Early stopping tại epoch 68 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.9022  P=0.7526  R=0.8069  F1=0.7634
✅ Best val F1: 0.8304
✅ Test F1:     0.7634

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     1.0000    0.9040    0.9496       125
          GS     0.7778    0.9545    0.8571        22
         MSI     0.7353    0.9259    0.8197        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.9022       184
   macro avg     0.7526    0.8069    0.7634       184
weighted avg     0.9156    0.9022    0.9031       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.3548  std=0.0369  min=0.3095  max=0.4285
   meth : mean=0.3207  std=0.0224  min=0.2768  max=0.3486
   mirna: mean=0.3245  std=0.0145  min=0.2946  max=0.3419

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
[Train] Acc=0.2636  P=0.2138  R=0.2114  F1=0.1660
[Val  ] Acc=0.2703  P=0.2684  R=0.2975  F1=0.2123
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.3000  P=0.2898  R=0.3654  F1=0.2384
[Val  ] Acc=0.2703  P=0.3965  R=0.4522  F1=0.3018
Fold 3 | Epoch  10/150
[Train] Acc=0.3848  P=0.3540  R=0.5329  F1=0.3319
[Val  ] Acc=0.3784  P=0.4352  R=0.5478  F1=0.3392
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.5545  P=0.4607  R=0.6696  F1=0.4874
[Val  ] Acc=0.4459  P=0.4997  R=0.7611  F1=0.4878
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.6909  P=0.5737  R=0.7839  F1=0.6138
[Val  ] Acc=0.7297  P=0.5772  R=0.7815  F1=0.6228
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.8167  P=0.7198  R=0.9009  F1=0.7703
[Val  ] Acc=0.7568  P=0.5859  R=0.7895  F1=0.6383
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.8379  P=0.7465  R=0.9299  F1=0.8060
[Val  ] Acc=0.7568  P=0.6344  R=0.8036  F1=0.6835
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9076  P=0.8401  R=0.9644  F1=0.8903
[Val  ] Acc=0.8108  P=0.6378  R=0.8196  F1=0.6943
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  40/150
[Train] Acc=0.9409  P=0.8971  R=0.9763  F1=0.9311
[Val  ] Acc=0.8108  P=0.6674  R=0.8338  F1=0.7165
Fold 3 | Epoch  45/150
[Train] Acc=0.9621  P=0.9387  R=0.9846  F1=0.9593
[Val  ] Acc=0.8108  P=0.7571  R=0.8480  F1=0.7461
Fold 3 | Epoch  50/150
[Train] Acc=0.9773  P=0.9677  R=0.9933  F1=0.9791
[Val  ] Acc=0.8243  P=0.6742  R=0.8378  F1=0.7246
⏹️  Early stopping tại epoch 54 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8306  P=0.6899  R=0.7299  F1=0.7077
✅ Best val F1: 0.7515
✅ Test F1:     0.7077

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9076    0.8640    0.8852       125
          GS     0.4231    0.5238    0.4681        21
         MSI     0.9286    0.9286    0.9286        28
      HM-SNV     0.3333    0.3333    0.3333         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8306       183
   macro avg     0.6899    0.7299    0.7077       183
weighted avg     0.8441    0.8306    0.8362       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.3718  std=0.1169  min=0.2690  max=0.5984
   meth : mean=0.3054  std=0.0726  min=0.1702  max=0.3716
   mirna: mean=0.3228  std=0.0444  min=0.2314  max=0.3594

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
[Train] Acc=0.2212  P=0.2006  R=0.2450  F1=0.1620
[Val  ] Acc=0.2703  P=0.2242  R=0.2096  F1=0.1878
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.3439  P=0.2979  R=0.4347  F1=0.2618
[Val  ] Acc=0.2703  P=0.2661  R=0.2874  F1=0.2200
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.4121  P=0.3256  R=0.4709  F1=0.3096
[Val  ] Acc=0.4054  P=0.3123  R=0.4194  F1=0.2835
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.5424  P=0.4190  R=0.6357  F1=0.4490
[Val  ] Acc=0.5946  P=0.3749  R=0.4624  F1=0.3905
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.7045  P=0.5648  R=0.8293  F1=0.6294
[Val  ] Acc=0.7297  P=0.4547  R=0.6126  F1=0.4961
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.8288  P=0.7647  R=0.9124  F1=0.8173
[Val  ] Acc=0.8243  P=0.5551  R=0.6689  F1=0.5924
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.8864  P=0.7820  R=0.9502  F1=0.8465
[Val  ] Acc=0.8514  P=0.5837  R=0.6952  F1=0.6224
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.9439  P=0.8597  R=0.9814  F1=0.9116
[Val  ] Acc=0.8784  P=0.6301  R=0.7356  F1=0.6744
Fold 4 | Epoch  40/150
[Train] Acc=0.9515  P=0.9027  R=0.9820  F1=0.9379
[Val  ] Acc=0.8649  P=0.6168  R=0.7498  F1=0.6698
Fold 4 | Epoch  45/150
[Train] Acc=0.9697  P=0.9278  R=0.9890  F1=0.9548
[Val  ] Acc=0.8649  P=0.6171  R=0.7316  F1=0.6648
⏹️  Early stopping tại epoch 49 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.7923  P=0.6576  R=0.7644  F1=0.6912
✅ Best val F1: 0.6744
✅ Test F1:     0.6912

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9307    0.7520    0.8319       125
          GS     0.4615    0.8571    0.6000        21
         MSI     0.8125    0.9630    0.8814        27
      HM-SNV     0.3333    0.2500    0.2857         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.7923       183
   macro avg     0.6576    0.7644    0.6912       183
weighted avg     0.8404    0.7923    0.8014       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.3463  std=0.0338  min=0.3055  max=0.4243
   meth : mean=0.3425  std=0.0321  min=0.2727  max=0.3821
   mirna: mean=0.3111  std=0.0027  min=0.3030  max=0.3154

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
[Train] Acc=0.3636  P=0.2404  R=0.2805  F1=0.1898
[Val  ] Acc=0.4054  P=0.2332  R=0.2707  F1=0.2074
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.4606  P=0.3303  R=0.3681  F1=0.2739
[Val  ] Acc=0.4730  P=0.2725  R=0.3502  F1=0.2021
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.4258  P=0.3410  R=0.4796  F1=0.3154
[Val  ] Acc=0.5135  P=0.3471  R=0.4736  F1=0.3478
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.5697  P=0.4695  R=0.6582  F1=0.4883
[Val  ] Acc=0.5135  P=0.4150  R=0.5486  F1=0.4331
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.7091  P=0.5969  R=0.8156  F1=0.6411
[Val  ] Acc=0.7027  P=0.5054  R=0.6046  F1=0.5416
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.8258  P=0.6935  R=0.9285  F1=0.7691
[Val  ] Acc=0.7703  P=0.5742  R=0.6712  F1=0.6104
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  30/150
[Train] Acc=0.8576  P=0.7717  R=0.9330  F1=0.8295
[Val  ] Acc=0.7838  P=0.5985  R=0.7116  F1=0.6300
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  35/150
[Train] Acc=0.9242  P=0.8585  R=0.9687  F1=0.9060
[Val  ] Acc=0.7973  P=0.6968  R=0.7752  F1=0.7232
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  40/150
[Train] Acc=0.9348  P=0.9039  R=0.9728  F1=0.9338
[Val  ] Acc=0.8243  P=0.8089  R=0.8014  F1=0.7731
Fold 5 | Epoch  45/150
[Train] Acc=0.9621  P=0.9232  R=0.9873  F1=0.9525
[Val  ] Acc=0.8378  P=0.8125  R=0.7872  F1=0.7736
Fold 5 | Epoch  50/150
[Train] Acc=0.9803  P=0.9723  R=0.9921  F1=0.9816
[Val  ] Acc=0.8514  P=0.8220  R=0.7912  F1=0.7816
⏹️  Early stopping tại epoch 51 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8197  P=0.7283  R=0.7285  F1=0.7154
✅ Best val F1: 0.7940
✅ Test F1:     0.7154

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9286    0.8387    0.8814       124
          GS     0.4483    0.5909    0.5098        22
         MSI     0.7647    0.9630    0.8525        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8197       183
   macro avg     0.7283    0.7285    0.7154       183
weighted avg     0.8396    0.8197    0.8243       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.4336  std=0.1580  min=0.2871  max=0.7228
   meth : mean=0.2724  std=0.0960  min=0.1070  max=0.3665
   mirna: mean=0.2940  std=0.0623  min=0.1702  max=0.3472

📈 5-fold CV summary
  ACCURACY : mean=0.8364  std=0.0363
  PRECISION: mean=0.7135  std=0.0348
  RECALL   : mean=0.7652  std=0.0325
  F1       : mean=0.7269  std=0.0283

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

         CIN     0.8682    0.8960    0.8819       125
          GS     0.6875    0.5000    0.5789        22
         MSI     0.8421    0.5926    0.6957        27
      HM-SNV     0.5000    0.5000    0.5000         4
         EBV     0.3750    1.0000    0.5455         6

    accuracy                         0.7989       184
   macro avg     0.6546    0.6977    0.6404       184
weighted avg     0.8187    0.7989    0.7991       184

[Test] Acc=0.7989  P=0.6546  R=0.6977  F1=0.6404

🔍 Patient Modality Gate Statistics (N=184)
   Gene expression     : mean=0.3892  std=0.0793
   DNA methylation     : mean=0.2963  std=0.0456
   miRNA               : mean=0.3146  std=0.0336

✔️  Accuracy: 0.7989
   Correct: 147 / 184