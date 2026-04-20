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
[Train] Acc=0.2747  P=0.2926  R=0.3637  F1=0.2332
[Val  ] Acc=0.4324  P=0.4306  R=0.5529  F1=0.4102
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.7466  P=0.6183  R=0.7832  F1=0.6718
[Val  ] Acc=0.7027  P=0.5605  R=0.6471  F1=0.5816
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.9287  P=0.8672  R=0.9689  F1=0.9110
[Val  ] Acc=0.8243  P=0.6310  R=0.6831  F1=0.6533
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.9727  P=0.9583  R=0.9845  F1=0.9705
[Val  ] Acc=0.8784  P=0.8699  R=0.7951  F1=0.8128
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 1 | Epoch  20/150
[Train] Acc=0.9712  P=0.9619  R=0.9872  F1=0.9733
[Val  ] Acc=0.8649  P=0.6729  R=0.7133  F1=0.6915
       fusion_alpha=0.255  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  25/150
[Train] Acc=0.9894  P=0.9785  R=0.9947  F1=0.9864
[Val  ] Acc=0.8784  P=0.8767  R=0.8133  F1=0.8267
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.9681  P=0.9280  R=0.9612  F1=0.9438
[Val  ] Acc=0.8108  P=0.6185  R=0.6609  F1=0.6354
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  35/150
[Train] Acc=0.9727  P=0.9501  R=0.9898  F1=0.9685
[Val  ] Acc=0.8919  P=0.8911  R=0.8173  F1=0.8368
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  40/150
[Train] Acc=0.9924  P=0.9758  R=0.9978  F1=0.9864
[Val  ] Acc=0.9054  P=0.9120  R=0.8031  F1=0.8328
       fusion_alpha=0.249  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 41 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8587  P=0.8063  R=0.7968  F1=0.7955
✅ Best val F1: 0.8483
✅ Test F1:     0.7955

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9250    0.8880    0.9061       125
          GS     0.6000    0.8182    0.6923        22
         MSI     0.8400    0.7778    0.8077        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8587       184
   macro avg     0.8063    0.7968    0.7955       184
weighted avg     0.8705    0.8587    0.8619       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.5597  std=0.4883  min=0.0015  max=0.9941
   meth : mean=0.0080  std=0.0178  min=0.0028  max=0.1678
   mirna: mean=0.4323  std=0.4883  min=0.0021  max=0.9956

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
[Train] Acc=0.3718  P=0.3179  R=0.3606  F1=0.2719
[Val  ] Acc=0.5811  P=0.3928  R=0.4908  F1=0.3901
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.7117  P=0.5543  R=0.7909  F1=0.6101
[Val  ] Acc=0.7703  P=0.5021  R=0.6570  F1=0.5400
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.8816  P=0.7907  R=0.9230  F1=0.8403
[Val  ] Acc=0.8649  P=0.7231  R=0.8134  F1=0.7585
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.9651  P=0.9435  R=0.9833  F1=0.9615
[Val  ] Acc=0.9054  P=0.8697  R=0.7930  F1=0.8051
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
Fold 2 | Epoch  20/150
[Train] Acc=0.9378  P=0.9185  R=0.9715  F1=0.9399
[Val  ] Acc=0.8784  P=0.8213  R=0.7850  F1=0.7791
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 2 | Epoch  25/150
[Train] Acc=0.9833  P=0.9697  R=0.9914  F1=0.9799
[Val  ] Acc=0.8919  P=0.8324  R=0.8072  F1=0.7947
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 29 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.9130  P=0.8004  R=0.8510  F1=0.8179
✅ Best val F1: 0.8156
✅ Test F1:     0.8179

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9829    0.9200    0.9504       125
          GS     0.7692    0.9091    0.8333        22
         MSI     0.8333    0.9259    0.8772        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.9130       184
   macro avg     0.8004    0.8510    0.8179       184
weighted avg     0.9209    0.9130    0.9144       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.4447  std=0.4860  min=0.0043  max=0.9962
   meth : mean=0.2691  std=0.4239  min=0.0019  max=0.9894
   mirna: mean=0.2862  std=0.4335  min=0.0020  max=0.9858

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
[Train] Acc=0.5015  P=0.3039  R=0.3956  F1=0.2962
[Val  ] Acc=0.6892  P=0.4981  R=0.6188  F1=0.5373
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.8076  P=0.6727  R=0.7555  F1=0.6868
[Val  ] Acc=0.7838  P=0.8127  R=0.7934  F1=0.7693
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.9303  P=0.8632  R=0.9609  F1=0.9056
[Val  ] Acc=0.7973  P=0.6940  R=0.8116  F1=0.7292
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.9712  P=0.9112  R=0.9894  F1=0.9454
[Val  ] Acc=0.8378  P=0.7769  R=0.8418  F1=0.7910
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 3 | Epoch  20/150
[Train] Acc=0.9636  P=0.9558  R=0.9771  F1=0.9655
[Val  ] Acc=0.8784  P=0.8015  R=0.8538  F1=0.8194
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.9606  P=0.9301  R=0.9809  F1=0.9530
[Val  ] Acc=0.9189  P=0.8371  R=0.8658  F1=0.8496
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.9909  P=0.9746  R=0.9973  F1=0.9855
[Val  ] Acc=0.8919  P=0.8148  R=0.8396  F1=0.8255
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  35/150
[Train] Acc=0.9955  P=0.9926  R=0.9987  F1=0.9956
[Val  ] Acc=0.8649  P=0.7297  R=0.8134  F1=0.7633
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  40/150
[Train] Acc=0.9985  P=0.9975  R=0.9996  F1=0.9985
[Val  ] Acc=0.9054  P=0.8332  R=0.8436  F1=0.8363
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 40 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8852  P=0.6863  R=0.6571  F1=0.6593
✅ Best val F1: 0.8496
✅ Test F1:     0.6593

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.8841    0.9760    0.9278       125
          GS     0.7273    0.3810    0.5000        21
         MSI     0.9630    0.9286    0.9455        28
      HM-SNV     0.0000    0.0000    0.0000         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8852       183
   macro avg     0.6863    0.6571    0.6593       183
weighted avg     0.8628    0.8852    0.8660       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.0060  std=0.0111  min=0.0037  max=0.1544
   meth : mean=0.6051  std=0.4830  min=0.0023  max=0.9941
   mirna: mean=0.3889  std=0.4820  min=0.0022  max=0.9938

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
[Train] Acc=0.3636  P=0.2801  R=0.3354  F1=0.2345
[Val  ] Acc=0.6622  P=0.4335  R=0.6250  F1=0.4605
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.7742  P=0.6105  R=0.8099  F1=0.6758
[Val  ] Acc=0.8649  P=0.6113  R=0.7316  F1=0.6599
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.9303  P=0.8794  R=0.9641  F1=0.9169
[Val  ] Acc=0.8784  P=0.6278  R=0.7214  F1=0.6671
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  15/150
[Train] Acc=0.9833  P=0.9799  R=0.9898  F1=0.9846
[Val  ] Acc=0.8919  P=0.6510  R=0.7213  F1=0.6786
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  20/150
[Train] Acc=0.9394  P=0.9041  R=0.9700  F1=0.9327
[Val  ] Acc=0.9054  P=0.6602  R=0.7436  F1=0.6949
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.9818  P=0.9623  R=0.9909  F1=0.9758
[Val  ] Acc=0.8919  P=0.6550  R=0.7254  F1=0.6835
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  30/150
[Train] Acc=0.9848  P=0.9722  R=0.9934  F1=0.9824
[Val  ] Acc=0.8784  P=0.6392  R=0.7214  F1=0.6732
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.9970  P=0.9954  R=0.9991  F1=0.9973
[Val  ] Acc=0.8919  P=0.6444  R=0.7396  F1=0.6845
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  40/150
[Train] Acc=0.9955  P=0.9950  R=0.9965  F1=0.9958
[Val  ] Acc=0.9189  P=0.6799  R=0.7476  F1=0.7061
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  45/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.9189  P=0.6799  R=0.7476  F1=0.7061
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  50/150
[Train] Acc=0.9848  P=0.9791  R=0.9934  F1=0.9860
[Val  ] Acc=0.8919  P=0.6444  R=0.7396  F1=0.6845
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  55/150
[Train] Acc=0.9833  P=0.9164  R=0.9935  F1=0.9459
[Val  ] Acc=0.8784  P=0.6959  R=0.7032  F1=0.6995
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  60/150
[Train] Acc=0.9848  P=0.9549  R=0.9934  F1=0.9730
[Val  ] Acc=0.9189  P=0.7397  R=0.7293  F1=0.7316
       fusion_alpha=0.249  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 61 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.8689  P=0.8950  R=0.7377  F1=0.7695
✅ Best val F1: 0.7368
✅ Test F1:     0.7695

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.8915    0.9200    0.9055       125
          GS     0.5833    0.6667    0.6222        21
         MSI     1.0000    0.8519    0.9200        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8689       183
   macro avg     0.8950    0.7377    0.7695       183
weighted avg     0.8781    0.8689    0.8672       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.7898  std=0.3936  min=0.0090  max=0.9989
   meth : mean=0.0065  std=0.0035  min=0.0007  max=0.0190
   mirna: mean=0.2037  std=0.3926  min=0.0004  max=0.9833

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
[Train] Acc=0.3515  P=0.2624  R=0.2942  F1=0.2015
[Val  ] Acc=0.6216  P=0.4332  R=0.4874  F1=0.3714
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.7545  P=0.5904  R=0.7521  F1=0.6400
[Val  ] Acc=0.8514  P=0.6819  R=0.7498  F1=0.7073
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.9136  P=0.8416  R=0.9458  F1=0.8842
[Val  ] Acc=0.8784  P=0.7075  R=0.7578  F1=0.7269
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.9333  P=0.8512  R=0.9521  F1=0.8913
[Val  ] Acc=0.8784  P=0.6817  R=0.7214  F1=0.6998
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.9742  P=0.9428  R=0.9865  F1=0.9630
[Val  ] Acc=0.8784  P=0.7291  R=0.7396  F1=0.7323
       fusion_alpha=0.255  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.9758  P=0.9552  R=0.9799  F1=0.9666
[Val  ] Acc=0.8649  P=0.6897  R=0.6627  F1=0.6713
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
Fold 5 | Epoch  30/150
[Train] Acc=0.9909  P=0.9653  R=0.9952  F1=0.9792
[Val  ] Acc=0.8649  P=0.7226  R=0.6809  F1=0.6959
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  35/150
[Train] Acc=0.9924  P=0.9878  R=0.9978  F1=0.9926
[Val  ] Acc=0.8784  P=0.7412  R=0.6849  F1=0.7067
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 5 | Epoch  40/150
[Train] Acc=0.9818  P=0.9315  R=0.9931  F1=0.9598
[Val  ] Acc=0.8514  P=0.6074  R=0.6668  F1=0.6064
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
Fold 5 | Epoch  45/150
[Train] Acc=0.9833  P=0.9763  R=0.9930  F1=0.9840
[Val  ] Acc=0.8784  P=0.6491  R=0.7578  F1=0.6884
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 49 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8689  P=0.8794  R=0.7223  F1=0.7552
✅ Best val F1: 0.7585
✅ Test F1:     0.7552

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.8923    0.9355    0.9134       124
          GS     0.5789    0.5000    0.5366        22
         MSI     0.9259    0.9259    0.9259        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8689       183
   macro avg     0.8794    0.7223    0.7552       183
weighted avg     0.8655    0.8689    0.8616       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.2090  std=0.3916  min=0.0024  max=0.9731
   meth : mean=0.5646  std=0.4867  min=0.0055  max=0.9954
   mirna: mean=0.2265  std=0.4067  min=0.0019  max=0.9863

📈 5-fold CV summary
  ACCURACY : mean=0.8789  std=0.0191
  PRECISION: mean=0.8135  std=0.0740
  RECALL   : mean=0.7530  std=0.0662
  F1       : mean=0.7595  std=0.0545