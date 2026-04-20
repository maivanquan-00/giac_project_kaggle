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
[Train] Acc=0.2246  P=0.2594  R=0.3039  F1=0.1793
[Val  ] Acc=0.4459  P=0.5004  R=0.5711  F1=0.4565
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.6829  P=0.5603  R=0.7058  F1=0.5915
[Val  ] Acc=0.7162  P=0.5676  R=0.6511  F1=0.5900
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.9014  P=0.8130  R=0.9443  F1=0.8646
[Val  ] Acc=0.8649  P=0.6729  R=0.7133  F1=0.6915
       fusion_alpha=0.261  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.9530  P=0.9098  R=0.9616  F1=0.9330
[Val  ] Acc=0.8784  P=0.8767  R=0.8133  F1=0.8267
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.9651  P=0.9542  R=0.9876  F1=0.9685
[Val  ] Acc=0.9189  P=0.9289  R=0.8253  F1=0.8568
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  25/150
[Train] Acc=0.9727  P=0.9342  R=0.9861  F1=0.9586
[Val  ] Acc=0.8649  P=0.8656  R=0.8093  F1=0.8181
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  30/150
[Train] Acc=0.9742  P=0.9532  R=0.9881  F1=0.9696
[Val  ] Acc=0.8649  P=0.8656  R=0.8093  F1=0.8181
       fusion_alpha=0.249  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 33 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.9022  P=0.8424  R=0.8212  F1=0.8291
✅ Best val F1: 0.8568
✅ Test F1:     0.8291

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9435    0.9360    0.9398       125
          GS     0.7500    0.8182    0.7826        22
         MSI     0.8519    0.8519    0.8519        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.9022       184
   macro avg     0.8424    0.8212    0.8291       184
weighted avg     0.9028    0.9022    0.9020       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.2577  std=0.0041  min=0.2524  max=0.2630
   meth : mean=0.4740  std=0.0055  min=0.4666  max=0.4814
   mirna: mean=0.2683  std=0.0014  min=0.2662  max=0.2704

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
[Train] Acc=0.4552  P=0.2662  R=0.2973  F1=0.2361
[Val  ] Acc=0.7162  P=0.4942  R=0.5640  F1=0.4807
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.6935  P=0.5014  R=0.6395  F1=0.5409
[Val  ] Acc=0.7838  P=0.5006  R=0.6610  F1=0.5445
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.8513  P=0.7429  R=0.9359  F1=0.8022
[Val  ] Acc=0.8784  P=0.8217  R=0.8032  F1=0.7859
       fusion_alpha=0.261  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.9378  P=0.8695  R=0.9566  F1=0.9078
[Val  ] Acc=0.8919  P=0.8283  R=0.7707  F1=0.7741
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.9439  P=0.8751  R=0.9771  F1=0.9153
[Val  ] Acc=0.8784  P=0.8304  R=0.7850  F1=0.7813
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.9757  P=0.9541  R=0.9907  F1=0.9710
[Val  ] Acc=0.8514  P=0.8008  R=0.7770  F1=0.7627
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  30/150
[Train] Acc=0.9757  P=0.9050  R=0.9929  F1=0.9394
[Val  ] Acc=0.8919  P=0.8346  R=0.7890  F1=0.7761
       fusion_alpha=0.248  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  35/150
[Train] Acc=0.9833  P=0.9628  R=0.9951  F1=0.9781
[Val  ] Acc=0.8649  P=0.7288  R=0.7627  F1=0.7372
       fusion_alpha=0.247  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 38 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.9293  P=0.7890  R=0.8149  F1=0.7874
✅ Best val F1: 0.8250
✅ Test F1:     0.7874

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9833    0.9440    0.9633       125
          GS     0.7500    0.9545    0.8400        22
         MSI     0.9615    0.9259    0.9434        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.9293       184
   macro avg     0.7890    0.8149    0.7874       184
weighted avg     0.9341    0.9293    0.9285       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.1936  std=0.0010  min=0.1920  max=0.1953
   meth : mean=0.4758  std=0.0091  min=0.4620  max=0.4937
   mirna: mean=0.3306  std=0.0101  min=0.3110  max=0.3460

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
[Train] Acc=0.4030  P=0.2599  R=0.2776  F1=0.2450
[Val  ] Acc=0.5676  P=0.3627  R=0.5322  F1=0.4010
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.7424  P=0.5857  R=0.6991  F1=0.6209
[Val  ] Acc=0.7703  P=0.6511  R=0.7935  F1=0.6948
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.9061  P=0.8539  R=0.9249  F1=0.8835
[Val  ] Acc=0.8378  P=0.7125  R=0.8236  F1=0.7515
       fusion_alpha=0.261  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.9545  P=0.9200  R=0.9813  F1=0.9474
[Val  ] Acc=0.8784  P=0.8921  R=0.8356  F1=0.8420
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.9591  P=0.9354  R=0.9821  F1=0.9569
[Val  ] Acc=0.8919  P=0.8400  R=0.8396  F1=0.8131
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  25/150
[Train] Acc=0.9803  P=0.9431  R=0.9900  F1=0.9644
[Val  ] Acc=0.8784  P=0.8970  R=0.8214  F1=0.8390
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.9712  P=0.9520  R=0.9852  F1=0.9674
[Val  ] Acc=0.8649  P=0.8831  R=0.8316  F1=0.8334
       fusion_alpha=0.249  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  35/150
[Train] Acc=0.9909  P=0.9689  R=0.9957  F1=0.9819
[Val  ] Acc=0.9189  P=0.9191  R=0.8476  F1=0.8651
       fusion_alpha=0.247  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  40/150
[Train] Acc=0.9909  P=0.9634  R=0.9957  F1=0.9789
[Val  ] Acc=0.9189  P=0.9185  R=0.8476  F1=0.8656
       fusion_alpha=0.246  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 42 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8743  P=0.7426  R=0.7348  F1=0.7343
✅ Best val F1: 0.8756
✅ Test F1:     0.7343

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.8931    0.9360    0.9141       125
          GS     0.6667    0.4762    0.5556        21
         MSI     0.9630    0.9286    0.9455        28
      HM-SNV     0.3333    0.3333    0.3333         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8743       183
   macro avg     0.7426    0.7348    0.7343       183
weighted avg     0.8675    0.8743    0.8685       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.2324  std=0.0001  min=0.2321  max=0.2326
   meth : mean=0.4777  std=0.0003  min=0.4773  max=0.4783
   mirna: mean=0.2899  std=0.0002  min=0.2896  max=0.2901

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
[Train] Acc=0.3409  P=0.2969  R=0.3110  F1=0.2248
[Val  ] Acc=0.6081  P=0.3967  R=0.5259  F1=0.3839
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.7364  P=0.5484  R=0.6874  F1=0.5811
[Val  ] Acc=0.8649  P=0.6298  R=0.7133  F1=0.6566
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.9288  P=0.8357  R=0.9498  F1=0.8853
[Val  ] Acc=0.8514  P=0.6059  R=0.7093  F1=0.6492
       fusion_alpha=0.261  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.9121  P=0.8690  R=0.9407  F1=0.8996
[Val  ] Acc=0.8784  P=0.6340  R=0.7173  F1=0.6686
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  20/150
[Train] Acc=0.9515  P=0.8692  R=0.9799  F1=0.9153
[Val  ] Acc=0.9054  P=0.7113  R=0.7436  F1=0.7267
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.9773  P=0.9579  R=0.9710  F1=0.9640
[Val  ] Acc=0.8649  P=0.6862  R=0.7133  F1=0.6985
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.9939  P=0.9704  R=0.9966  F1=0.9825
[Val  ] Acc=0.9189  P=0.7325  R=0.7476  F1=0.7381
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  35/150
[Train] Acc=0.9879  P=0.9710  R=0.9927  F1=0.9815
[Val  ] Acc=0.9054  P=0.7128  R=0.7436  F1=0.7269
       fusion_alpha=0.248  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  40/150
[Train] Acc=0.9712  P=0.9354  R=0.9857  F1=0.9590
[Val  ] Acc=0.9324  P=0.7468  R=0.7516  F1=0.7482
       fusion_alpha=0.248  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 44 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.8689  P=0.8811  R=0.7493  F1=0.7699
✅ Best val F1: 0.7482
✅ Test F1:     0.7699

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9040    0.9040    0.9040       125
          GS     0.6087    0.6667    0.6364        21
         MSI     0.8929    0.9259    0.9091        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8689       183
   macro avg     0.8811    0.7493    0.7699       183
weighted avg     0.8737    0.8689    0.8662       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.2593  std=0.0002  min=0.2589  max=0.2596
   meth : mean=0.4325  std=0.0001  min=0.4323  max=0.4327
   mirna: mean=0.3082  std=0.0001  min=0.3081  max=0.3083

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
[Train] Acc=0.2939  P=0.3151  R=0.3904  F1=0.2544
[Val  ] Acc=0.4324  P=0.3711  R=0.5509  F1=0.3472
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.6864  P=0.5413  R=0.7010  F1=0.5822
[Val  ] Acc=0.7973  P=0.5452  R=0.6974  F1=0.5917
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.9076  P=0.7973  R=0.9353  F1=0.8501
[Val  ] Acc=0.8649  P=0.6955  R=0.6992  F1=0.6973
       fusion_alpha=0.261  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  15/150
[Train] Acc=0.9394  P=0.8492  R=0.9720  F1=0.8974
[Val  ] Acc=0.8784  P=0.6573  R=0.7214  F1=0.6818
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  20/150
[Train] Acc=0.9652  P=0.9323  R=0.9833  F1=0.9559
[Val  ] Acc=0.9054  P=0.6772  R=0.7476  F1=0.7057
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 22 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8033  P=0.7583  R=0.8014  F1=0.7752
✅ Best val F1: 0.7963
✅ Test F1:     0.7752

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9273    0.8226    0.8718       124
          GS     0.4286    0.5455    0.4800        22
         MSI     0.6857    0.8889    0.7742        27
      HM-SNV     0.7500    0.7500    0.7500         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8033       183
   macro avg     0.7583    0.8014    0.7752       183
weighted avg     0.8302    0.8033    0.8118       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.2071  std=0.1235  min=0.0587  max=0.4646
   meth : mean=0.4140  std=0.1455  min=0.2010  max=0.6953
   mirna: mean=0.3789  std=0.1560  min=0.1343  max=0.6882

📈 5-fold CV summary
  ACCURACY : mean=0.8756  std=0.0421
  PRECISION: mean=0.8027  std=0.0519
  RECALL   : mean=0.7843  std=0.0354
  F1       : mean=0.7792  std=0.0306