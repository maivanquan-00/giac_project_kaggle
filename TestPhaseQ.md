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
   Building ENSP→symbol map từ alias file... 3,126 proteins mapped
   Parsing STRING links... 7,937 unique edges
   Gene↔Gene edges : 15,874
   Parsing hsa_MTI.csv... 41,459 edges
   miRNA→Gene edges: 41,459
   Building CpG↔miRNA co-regulation edges... 6,440 edges
   CpG↔miRNA edges : 6,440

🧠 Fold 1 model parameters: 3,448,329
🚀 Bắt đầu training fold 1...

🗓️  Scheduler: onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.2246  P=0.2561  R=0.3023  F1=0.1782
[Val  ] Acc=0.4324  P=0.4997  R=0.5671  F1=0.4516
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.6935  P=0.5350  R=0.7046  F1=0.5826
[Val  ] Acc=0.7432  P=0.5807  R=0.6591  F1=0.6019
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.8816  P=0.7887  R=0.9524  F1=0.8451
[Val  ] Acc=0.8514  P=0.6519  R=0.6911  F1=0.6689
       fusion_alpha=0.261  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.9347  P=0.8864  R=0.9610  F1=0.9188
[Val  ] Acc=0.8784  P=0.8699  R=0.7951  F1=0.8128
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 1 | Epoch  20/150
[Train] Acc=0.9439  P=0.9201  R=0.9771  F1=0.9445
[Val  ] Acc=0.8784  P=0.6866  R=0.7173  F1=0.7007
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  25/150
[Train] Acc=0.9712  P=0.9627  R=0.9835  F1=0.9724
[Val  ] Acc=0.8514  P=0.6519  R=0.6911  F1=0.6689
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 27 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8152  P=0.7253  R=0.7881  F1=0.7423
✅ Best val F1: 0.8359
✅ Test F1:     0.7423

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9444    0.8160    0.8755       125
          GS     0.4722    0.7727    0.5862        22
         MSI     0.7931    0.8519    0.8214        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.8152       184
   macro avg     0.7253    0.7881    0.7423       184
weighted avg     0.8534    0.8152    0.8258       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.2591  std=0.0154  min=0.2316  max=0.2848
   meth : mean=0.4749  std=0.0413  min=0.4022  max=0.5555
   mirna: mean=0.2660  std=0.0285  min=0.2128  max=0.3131

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
   Building ENSP→symbol map từ alias file... 3,126 proteins mapped
   Parsing STRING links... 7,828 unique edges
   Gene↔Gene edges : 15,656
   Parsing hsa_MTI.csv... 41,092 edges
   miRNA→Gene edges: 41,092
   Building CpG↔miRNA co-regulation edges... 6,400 edges
   CpG↔miRNA edges : 6,400

🧠 Fold 2 model parameters: 3,448,329
🚀 Bắt đầu training fold 2...

🗓️  Scheduler: onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.4173  P=0.3126  R=0.3877  F1=0.2881
[Val  ] Acc=0.6892  P=0.3982  R=0.5419  F1=0.3934
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.6737  P=0.5220  R=0.7257  F1=0.5726
[Val  ] Acc=0.7568  P=0.4999  R=0.6530  F1=0.5463
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.8634  P=0.7634  R=0.9091  F1=0.8132
[Val  ] Acc=0.8243  P=0.6879  R=0.7872  F1=0.7241
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.9196  P=0.8549  R=0.9448  F1=0.8936
[Val  ] Acc=0.8784  P=0.7484  R=0.8032  F1=0.7659
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 2 | Epoch  20/150
[Train] Acc=0.9347  P=0.8310  R=0.9573  F1=0.8789
[Val  ] Acc=0.8919  P=0.7318  R=0.8072  F1=0.7573
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.9575  P=0.8923  R=0.9816  F1=0.9305
[Val  ] Acc=0.9189  P=0.8655  R=0.8152  F1=0.8148
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.9803  P=0.9600  R=0.9921  F1=0.9750
[Val  ] Acc=0.9324  P=0.8812  R=0.8192  F1=0.8250
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  35/150
[Train] Acc=0.9863  P=0.9700  R=0.9917  F1=0.9805
[Val  ] Acc=0.8919  P=0.8418  R=0.8072  F1=0.7966
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  40/150
[Train] Acc=0.9879  P=0.9812  R=0.9964  F1=0.9883
[Val  ] Acc=0.9189  P=0.8610  R=0.8152  F1=0.8144
       fusion_alpha=0.249  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 44 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.9185  P=0.8831  R=0.9010  F1=0.8852
✅ Best val F1: 0.8250
✅ Test F1:     0.8852

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9829    0.9200    0.9504       125
          GS     0.7692    0.9091    0.8333        22
         MSI     0.8065    0.9259    0.8621        27
      HM-SNV     1.0000    0.7500    0.8571         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.9185       184
   macro avg     0.8831    0.9010    0.8852       184
weighted avg     0.9277    0.9185    0.9205       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.2419  std=0.0000  min=0.2418  max=0.2420
   meth : mean=0.4649  std=0.0000  min=0.4649  max=0.4650
   mirna: mean=0.2932  std=0.0000  min=0.2931  max=0.2932

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
   Building ENSP→symbol map từ alias file... 3,121 proteins mapped
   Parsing STRING links... 7,926 unique edges
   Gene↔Gene edges : 15,852
   Parsing hsa_MTI.csv... 42,285 edges
   miRNA→Gene edges: 42,285
   Building CpG↔miRNA co-regulation edges... 6,500 edges
   CpG↔miRNA edges : 6,500

🧠 Fold 3 model parameters: 3,448,329
🚀 Bắt đầu training fold 3...

🗓️  Scheduler: onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.3985  P=0.2603  R=0.2784  F1=0.2444
[Val  ] Acc=0.5811  P=0.3737  R=0.5503  F1=0.4127
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.7500  P=0.6136  R=0.7365  F1=0.6535
[Val  ] Acc=0.7703  P=0.6511  R=0.7935  F1=0.6948
       fusion_alpha=0.268  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.8970  P=0.8290  R=0.9142  F1=0.8648
[Val  ] Acc=0.8378  P=0.7125  R=0.8236  F1=0.7515
       fusion_alpha=0.261  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.9364  P=0.8902  R=0.9670  F1=0.9237
[Val  ] Acc=0.8514  P=0.8752  R=0.8276  F1=0.8253
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 3 | Epoch  20/150
[Train] Acc=0.9727  P=0.9537  R=0.9856  F1=0.9687
[Val  ] Acc=0.8514  P=0.8752  R=0.8276  F1=0.8253
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.9742  P=0.9407  R=0.9786  F1=0.9583
[Val  ] Acc=0.9054  P=0.9150  R=0.8436  F1=0.8610
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  30/150
[Train] Acc=0.9652  P=0.9251  R=0.9898  F1=0.9542
[Val  ] Acc=0.8784  P=0.8921  R=0.8356  F1=0.8420
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9712  P=0.9079  R=0.9702  F1=0.9358
[Val  ] Acc=0.9054  P=0.8217  R=0.8476  F1=0.8306
       fusion_alpha=0.249  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  40/150
[Train] Acc=0.9894  P=0.9743  R=0.9948  F1=0.9842
[Val  ] Acc=0.9054  P=0.9118  R=0.8618  F1=0.8644
       fusion_alpha=0.248  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  45/150
[Train] Acc=0.9848  P=0.9705  R=0.9892  F1=0.9795
[Val  ] Acc=0.9324  P=0.8746  R=0.8698  F1=0.8470
       fusion_alpha=0.247  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 49 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8798  P=0.7716  R=0.7523  F1=0.7571
✅ Best val F1: 0.8830
✅ Test F1:     0.7571

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9062    0.9280    0.9170       125
          GS     0.6316    0.5714    0.6000        21
         MSI     0.9630    0.9286    0.9455        28
      HM-SNV     0.5000    0.3333    0.4000         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8798       183
   macro avg     0.7716    0.7523    0.7571       183
weighted avg     0.8751    0.8798    0.8767       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.2342  std=0.0000  min=0.2342  max=0.2342
   meth : mean=0.4775  std=0.0000  min=0.4775  max=0.4775
   mirna: mean=0.2882  std=0.0000  min=0.2882  max=0.2882

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
   Building ENSP→symbol map từ alias file... 3,124 proteins mapped
   Parsing STRING links... 8,059 unique edges
   Gene↔Gene edges : 16,118
   Parsing hsa_MTI.csv... 41,940 edges
   miRNA→Gene edges: 41,940
   Building CpG↔miRNA co-regulation edges... 6,480 edges
   CpG↔miRNA edges : 6,480

🧠 Fold 4 model parameters: 3,448,329
🚀 Bắt đầu training fold 4...

🗓️  Scheduler: onecycle
Fold 4 | Epoch   1/150
[Train] Acc=0.1970  P=0.2612  R=0.2750  F1=0.1775
[Val  ] Acc=0.5000  P=0.3829  R=0.5316  F1=0.3670
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.6742  P=0.5449  R=0.8084  F1=0.5986
[Val  ] Acc=0.7703  P=0.5272  R=0.7036  F1=0.5778
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.8848  P=0.7626  R=0.9289  F1=0.8263
[Val  ] Acc=0.8919  P=0.6459  R=0.7396  F1=0.6847
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  15/150
[Train] Acc=0.9182  P=0.8539  R=0.9472  F1=0.8912
[Val  ] Acc=0.9054  P=0.6602  R=0.7436  F1=0.6949
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  20/150
[Train] Acc=0.9727  P=0.9323  R=0.9861  F1=0.9566
[Val  ] Acc=0.8919  P=0.6444  R=0.7396  F1=0.6845
       fusion_alpha=0.255  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.9758  P=0.9551  R=0.9817  F1=0.9676
[Val  ] Acc=0.9054  P=0.6602  R=0.7436  F1=0.6949
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  30/150
[Train] Acc=0.9727  P=0.9317  R=0.9808  F1=0.9544
[Val  ] Acc=0.8649  P=0.6196  R=0.7133  F1=0.6585
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  35/150
[Train] Acc=0.9818  P=0.9775  R=0.9872  F1=0.9820
[Val  ] Acc=0.9054  P=0.6602  R=0.7436  F1=0.6949
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 39 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.8798  P=0.8875  R=0.7842  F1=0.7875
✅ Best val F1: 0.7349
✅ Test F1:     0.7875

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9328    0.8880    0.9098       125
          GS     0.6429    0.8571    0.7347        21
         MSI     0.8621    0.9259    0.8929        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8798       183
   macro avg     0.8875    0.7842    0.7875       183
weighted avg     0.8927    0.8798    0.8790       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.2208  std=0.0002  min=0.2204  max=0.2212
   meth : mean=0.4734  std=0.0001  min=0.4732  max=0.4735
   mirna: mean=0.3058  std=0.0002  min=0.3055  max=0.3061

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
   Building ENSP→symbol map từ alias file... 3,119 proteins mapped
   Parsing STRING links... 7,877 unique edges
   Gene↔Gene edges : 15,754
   Parsing hsa_MTI.csv... 41,465 edges
   miRNA→Gene edges: 41,465
   Building CpG↔miRNA co-regulation edges... 6,420 edges
   CpG↔miRNA edges : 6,420

🧠 Fold 5 model parameters: 3,448,329
🚀 Bắt đầu training fold 5...

🗓️  Scheduler: onecycle
Fold 5 | Epoch   1/150
[Train] Acc=0.3879  P=0.2643  R=0.2428  F1=0.2206
[Val  ] Acc=0.7027  P=0.5264  R=0.7188  F1=0.5738
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.6970  P=0.5297  R=0.7098  F1=0.5726
[Val  ] Acc=0.8243  P=0.6758  R=0.8196  F1=0.7247
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.8924  P=0.7918  R=0.9513  F1=0.8477
[Val  ] Acc=0.9054  P=0.9243  R=0.8254  F1=0.8573
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  15/150
[Train] Acc=0.9136  P=0.8137  R=0.9602  F1=0.8632
[Val  ] Acc=0.9054  P=0.7119  R=0.7658  F1=0.7332
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  20/150
[Train] Acc=0.9606  P=0.8906  R=0.9804  F1=0.9296
[Val  ] Acc=0.8919  P=0.7161  R=0.7618  F1=0.7307
       fusion_alpha=0.255  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 23 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8525  P=0.8575  R=0.7941  F1=0.8055
✅ Best val F1: 0.8851
✅ Test F1:     0.8055

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9391    0.8710    0.9038       124
          GS     0.4516    0.6364    0.5283        22
         MSI     0.8966    0.9630    0.9286        27
      HM-SNV     1.0000    0.5000    0.6667         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8525       183
   macro avg     0.8575    0.7941    0.8055       183
weighted avg     0.8776    0.8525    0.8603       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.2901  std=0.0985  min=0.1457  max=0.4709
   meth : mean=0.4001  std=0.0705  min=0.2923  max=0.5354
   mirna: mean=0.3098  std=0.0431  min=0.2303  max=0.3839

📈 5-fold CV summary
  ACCURACY : mean=0.8691  std=0.0342
  PRECISION: mean=0.8250  std=0.0650
  RECALL   : mean=0.8039  std=0.0507
  F1       : mean=0.7955  std=0.0500