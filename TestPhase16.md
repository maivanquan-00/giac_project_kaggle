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
[Train] Acc=0.2974  P=0.2864  R=0.3674  F1=0.2320
[Val  ] Acc=0.4595  P=0.4065  R=0.5569  F1=0.4000
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.7967  P=0.7634  R=0.8275  F1=0.7700
[Val  ] Acc=0.7568  P=0.5899  R=0.6631  F1=0.6151
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.9712  P=0.9538  R=0.9894  F1=0.9703
[Val  ] Acc=0.9054  P=0.9003  R=0.8031  F1=0.8318
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.9666  P=0.9337  R=0.9784  F1=0.9544
[Val  ] Acc=0.8243  P=0.8272  R=0.7791  F1=0.7784
       fusion_alpha=0.259  (GAT=0.26, Shortcut=0.74)
Fold 1 | Epoch  20/150
[Train] Acc=0.9924  P=0.9896  R=0.9956  F1=0.9925
[Val  ] Acc=0.8378  P=0.8294  R=0.7649  F1=0.7778
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 1 | Epoch  25/150
[Train] Acc=0.9939  P=0.9901  R=0.9982  F1=0.9940
[Val  ] Acc=0.8649  P=0.6643  R=0.6951  F1=0.6784
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
⏹️  Early stopping tại epoch 25 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8478  P=0.7741  R=0.7977  F1=0.7777
✅ Best val F1: 0.8318
✅ Test F1:     0.7777

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9310    0.8640    0.8963       125
          GS     0.5312    0.7727    0.6296        22
         MSI     0.8846    0.8519    0.8679        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8478       184
   macro avg     0.7741    0.7977    0.7777       184
weighted avg     0.8683    0.8478    0.8540       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.2652  std=0.0772  min=0.1381  max=0.3874
   meth : mean=0.4677  std=0.0532  min=0.3753  max=0.5689
   mirna: mean=0.2671  std=0.0444  min=0.1939  max=0.3452

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
[Train] Acc=0.3505  P=0.3383  R=0.3217  F1=0.2937
[Val  ] Acc=0.5811  P=0.4053  R=0.5544  F1=0.4102
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.8058  P=0.6830  R=0.8489  F1=0.7357
[Val  ] Acc=0.8514  P=0.5962  R=0.6992  F1=0.6365
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.9605  P=0.9292  R=0.9766  F1=0.9508
[Val  ] Acc=0.8649  P=0.8125  R=0.7992  F1=0.7776
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.9378  P=0.9300  R=0.9603  F1=0.9436
[Val  ] Acc=0.8649  P=0.8047  R=0.7810  F1=0.7691
       fusion_alpha=0.259  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.9833  P=0.9777  R=0.9908  F1=0.9839
[Val  ] Acc=0.8243  P=0.7963  R=0.7507  F1=0.7463
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 2 | Epoch  25/150
[Train] Acc=0.9985  P=0.9974  R=0.9996  F1=0.9985
[Val  ] Acc=0.9054  P=0.8682  R=0.7930  F1=0.8048
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.9985  P=0.9974  R=0.9996  F1=0.9985
[Val  ] Acc=0.9189  P=0.8720  R=0.7970  F1=0.8087
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
Fold 2 | Epoch  35/150
[Train] Acc=0.9985  P=0.9974  R=0.9996  F1=0.9985
[Val  ] Acc=0.8784  P=0.8395  R=0.7667  F1=0.7774
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  40/150
[Train] Acc=0.9985  P=0.9974  R=0.9996  F1=0.9985
[Val  ] Acc=0.8649  P=0.8244  R=0.7445  F1=0.7560
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 41 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.9076  P=0.8798  R=0.8344  F1=0.8385
✅ Best val F1: 0.8087
✅ Test F1:     0.8385

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9587    0.9280    0.9431       125
          GS     0.7500    0.8182    0.7826        22
         MSI     0.8333    0.9259    0.8772        27
      HM-SNV     1.0000    0.5000    0.6667         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.9076       184
   macro avg     0.8798    0.8344    0.8385       184
weighted avg     0.9129    0.9076    0.9076       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.2614  std=0.0000  min=0.2614  max=0.2614
   meth : mean=0.4370  std=0.0000  min=0.4370  max=0.4370
   mirna: mean=0.3016  std=0.0000  min=0.3016  max=0.3017

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
[Train] Acc=0.5318  P=0.3219  R=0.3982  F1=0.3052
[Val  ] Acc=0.6757  P=0.4222  R=0.5682  F1=0.4534
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.8394  P=0.7326  R=0.7835  F1=0.7386
[Val  ] Acc=0.7973  P=0.7480  R=0.7974  F1=0.7248
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.9561  P=0.9162  R=0.9770  F1=0.9440
[Val  ] Acc=0.8919  P=0.8148  R=0.8396  F1=0.8255
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.9848  P=0.9803  R=0.9902  F1=0.9849
[Val  ] Acc=0.9189  P=0.9298  R=0.8476  F1=0.8716
       fusion_alpha=0.259  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.9939  P=0.9902  R=0.9982  F1=0.9941
[Val  ] Acc=0.8919  P=0.8477  R=0.8538  F1=0.8221
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 3 | Epoch  25/150
[Train] Acc=0.9985  P=0.9975  R=0.9996  F1=0.9985
[Val  ] Acc=0.8649  P=0.7924  R=0.8134  F1=0.8014
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
Fold 3 | Epoch  30/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.9324  P=0.9482  R=0.8516  F1=0.8823
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 34 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8852  P=0.7243  R=0.6809  F1=0.6986
✅ Best val F1: 0.8937
✅ Test F1:     0.6986

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.8881    0.9520    0.9189       125
          GS     0.7333    0.5238    0.6111        21
         MSI     1.0000    0.9286    0.9630        28
      HM-SNV     0.0000    0.0000    0.0000         3
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8852       183
   macro avg     0.7243    0.6809    0.6986       183
weighted avg     0.8765    0.8852    0.8779       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.2171  std=0.0005  min=0.2165  max=0.2179
   meth : mean=0.4699  std=0.0022  min=0.4664  max=0.4741
   mirna: mean=0.3129  std=0.0021  min=0.3091  max=0.3160

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
[Train] Acc=0.2939  P=0.2830  R=0.3858  F1=0.2298
[Val  ] Acc=0.3649  P=0.3699  R=0.5167  F1=0.2893
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.8030  P=0.6994  R=0.8138  F1=0.7318
[Val  ] Acc=0.8108  P=0.6339  R=0.7338  F1=0.6677
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.9621  P=0.9306  R=0.9846  F1=0.9554
[Val  ] Acc=0.8649  P=0.6862  R=0.7133  F1=0.6985
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.9054  P=0.7322  R=0.7436  F1=0.7360
       fusion_alpha=0.259  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  20/150
[Train] Acc=0.9212  P=0.8914  R=0.9636  F1=0.9199
[Val  ] Acc=0.8784  P=0.6846  R=0.7356  F1=0.7070
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  25/150
[Train] Acc=0.9924  P=0.9900  R=0.9957  F1=0.9928
[Val  ] Acc=0.8784  P=0.6967  R=0.7356  F1=0.7144
       fusion_alpha=0.255  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 28 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.8743  P=0.8873  R=0.7668  F1=0.7799
✅ Best val F1: 0.7461
✅ Test F1:     0.7799

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9180    0.8960    0.9069       125
          GS     0.5926    0.7619    0.6667        21
         MSI     0.9259    0.9259    0.9259        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8743       183
   macro avg     0.8873    0.7668    0.7799       183
weighted avg     0.8863    0.8743    0.8741       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.2783  std=0.0245  min=0.2446  max=0.3184
   meth : mean=0.4046  std=0.0303  min=0.3513  max=0.4531
   mirna: mean=0.3171  std=0.0094  min=0.3017  max=0.3314

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
[Train] Acc=0.4015  P=0.3472  R=0.3948  F1=0.2648
[Val  ] Acc=0.4730  P=0.3667  R=0.4292  F1=0.2979
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.7788  P=0.6487  R=0.8593  F1=0.7062
[Val  ] Acc=0.8378  P=0.6281  R=0.7276  F1=0.6689
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.9424  P=0.8740  R=0.9697  F1=0.9120
[Val  ] Acc=0.9054  P=0.7496  R=0.7658  F1=0.7572
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.9833  P=0.9627  R=0.9951  F1=0.9779
[Val  ] Acc=0.8784  P=0.7158  R=0.7578  F1=0.7284
       fusion_alpha=0.259  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  20/150
[Train] Acc=0.9970  P=0.9949  R=0.9991  F1=0.9970
[Val  ] Acc=0.8919  P=0.6593  R=0.7618  F1=0.6978
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  25/150
[Train] Acc=0.9894  P=0.9594  R=0.9931  F1=0.9756
[Val  ] Acc=0.8919  P=0.6629  R=0.7436  F1=0.6961
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
⏹️  Early stopping tại epoch 25 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8852  P=0.8798  R=0.8297  F1=0.8509
✅ Best val F1: 0.7572
✅ Test F1:     0.8509

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9206    0.9355    0.9280       124
          GS     0.5500    0.5000    0.5238        22
         MSI     0.9286    0.9630    0.9455        27
      HM-SNV     1.0000    0.7500    0.8571         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8852       183
   macro avg     0.8798    0.8297    0.8509       183
weighted avg     0.8816    0.8852    0.8828       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.2477  std=0.0733  min=0.1198  max=0.3678
   meth : mean=0.4148  std=0.0552  min=0.3344  max=0.5283
   mirna: mean=0.3375  std=0.0429  min=0.2735  max=0.4077

📈 5-fold CV summary
  ACCURACY : mean=0.8800  std=0.0194
  PRECISION: mean=0.8291  std=0.0671
  RECALL   : mean=0.7819  std=0.0561
  F1       : mean=0.7891  std=0.0542