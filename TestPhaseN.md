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
[Train] Acc=0.2792  P=0.2995  R=0.3833  F1=0.2418
[Val  ] Acc=0.4054  P=0.4252  R=0.5409  F1=0.3962
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.7572  P=0.6287  R=0.7597  F1=0.6674
[Val  ] Acc=0.7297  P=0.5718  R=0.6551  F1=0.5954
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.9256  P=0.8651  R=0.9701  F1=0.9094
[Val  ] Acc=0.8649  P=0.6643  R=0.6951  F1=0.6784
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.9621  P=0.8928  R=0.9819  F1=0.9322
[Val  ] Acc=0.8378  P=0.7666  R=0.7649  F1=0.7397
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
Fold 1 | Epoch  20/150
[Train] Acc=0.9530  P=0.9216  R=0.9797  F1=0.9474
[Val  ] Acc=0.8378  P=0.6441  R=0.7053  F1=0.6695
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 1 | Epoch  25/150
[Train] Acc=0.9863  P=0.9622  R=0.9938  F1=0.9775
[Val  ] Acc=0.8108  P=0.6372  R=0.6973  F1=0.6603
       fusion_alpha=0.255  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 27 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8315  P=0.7867  R=0.7929  F1=0.7804
✅ Best val F1: 0.8359
✅ Test F1:     0.7804

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9292    0.8400    0.8824       125
          GS     0.4857    0.7727    0.5965        22
         MSI     0.8519    0.8519    0.8519        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8315       184
   macro avg     0.7867    0.7929    0.7804       184
weighted avg     0.8614    0.8315    0.8408       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.5575  std=0.4923  min=0.0000  max=1.0000
   meth : mean=0.2488  std=0.4281  min=0.0000  max=1.0000
   mirna: mean=0.1937  std=0.3872  min=0.0000  max=1.0000

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
[Train] Acc=0.4127  P=0.3089  R=0.3956  F1=0.2844
[Val  ] Acc=0.6757  P=0.3847  R=0.5095  F1=0.3702
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.7193  P=0.5751  R=0.7876  F1=0.6295
[Val  ] Acc=0.8243  P=0.5797  R=0.6730  F1=0.6180
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.9059  P=0.8358  R=0.9600  F1=0.8826
[Val  ] Acc=0.8243  P=0.7860  R=0.7690  F1=0.7483
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.9590  P=0.9509  R=0.9772  F1=0.9623
[Val  ] Acc=0.8919  P=0.8418  R=0.8072  F1=0.7966
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
Fold 2 | Epoch  20/150
[Train] Acc=0.9712  P=0.9301  R=0.9856  F1=0.9554
[Val  ] Acc=0.8919  P=0.8573  R=0.7849  F1=0.7952
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
Fold 2 | Epoch  25/150
[Train] Acc=0.9803  P=0.9601  R=0.9878  F1=0.9735
[Val  ] Acc=0.8784  P=0.6445  R=0.6890  F1=0.6590
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.9879  P=0.9815  R=0.9964  F1=0.9887
[Val  ] Acc=0.8919  P=0.8416  R=0.7890  F1=0.7897
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.9909  P=0.9855  R=0.9973  F1=0.9912
[Val  ] Acc=0.8784  P=0.8229  R=0.7667  F1=0.7706
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  40/150
[Train] Acc=0.9317  P=0.8619  R=0.9698  F1=0.9049
[Val  ] Acc=0.8919  P=0.6516  R=0.6930  F1=0.6636
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  45/150
[Train] Acc=0.9863  P=0.9497  R=0.9938  F1=0.9697
[Val  ] Acc=0.8784  P=0.8291  R=0.7485  F1=0.7618
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 49 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.9239  P=0.8290  R=0.9026  F1=0.8612
✅ Best val F1: 0.8041
✅ Test F1:     0.8612

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9831    0.9280    0.9547       125
          GS     0.8000    0.9091    0.8511        22
         MSI     0.8621    0.9259    0.8929        27
      HM-SNV     0.7500    0.7500    0.7500         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.9239       184
   macro avg     0.8290    0.9026    0.8612       184
weighted avg     0.9307    0.9239    0.9256       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.0018  std=0.0124  min=0.0000  max=0.0974
   meth : mean=0.5339  std=0.4959  min=0.0000  max=1.0000
   mirna: mean=0.4643  std=0.4962  min=0.0000  max=1.0000

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
[Train] Acc=0.3561  P=0.2867  R=0.3778  F1=0.2537
[Val  ] Acc=0.5676  P=0.3899  R=0.5868  F1=0.4104
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.7303  P=0.5899  R=0.8022  F1=0.6423
[Val  ] Acc=0.7838  P=0.6357  R=0.7792  F1=0.6782
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.9197  P=0.8683  R=0.9541  F1=0.9052
[Val  ] Acc=0.8243  P=0.7648  R=0.8054  F1=0.7708
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.9318  P=0.8598  R=0.9357  F1=0.8923
[Val  ] Acc=0.8784  P=0.7310  R=0.8396  F1=0.7725
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.9742  P=0.9672  R=0.9861  F1=0.9758
[Val  ] Acc=0.8378  P=0.7828  R=0.8418  F1=0.7628
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
Fold 3 | Epoch  25/150
[Train] Acc=0.9803  P=0.9725  R=0.9921  F1=0.9816
[Val  ] Acc=0.8649  P=0.7872  R=0.8316  F1=0.8020
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.9924  P=0.9787  R=0.9957  F1=0.9869
[Val  ] Acc=0.8919  P=0.8964  R=0.8396  F1=0.8462
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9939  P=0.9902  R=0.9982  F1=0.9941
[Val  ] Acc=0.9054  P=0.9150  R=0.8436  F1=0.8610
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  40/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.8919  P=0.8148  R=0.8396  F1=0.8255
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  45/150
[Train] Acc=0.9955  P=0.9926  R=0.9987  F1=0.9956
[Val  ] Acc=0.9054  P=0.8296  R=0.8436  F1=0.8361
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 47 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8798  P=0.6692  R=0.6634  F1=0.6618
✅ Best val F1: 0.8716
✅ Test F1:     0.6618

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.8889    0.9600    0.9231       125
          GS     0.6000    0.4286    0.5000        21
         MSI     1.0000    0.9286    0.9630        28
      HM-SNV     0.0000    0.0000    0.0000         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8798       183
   macro avg     0.6692    0.6634    0.6618       183
weighted avg     0.8571    0.8798    0.8655       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.6087  std=0.4879  min=0.0000  max=1.0000
   meth : mean=0.2187  std=0.4111  min=0.0000  max=1.0000
   mirna: mean=0.1727  std=0.3737  min=0.0000  max=1.0000

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
[Train] Acc=0.2348  P=0.3070  R=0.3759  F1=0.2212
[Val  ] Acc=0.5000  P=0.4039  R=0.5547  F1=0.3981
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.6773  P=0.5820  R=0.8514  F1=0.6442
[Val  ] Acc=0.7568  P=0.6038  R=0.6854  F1=0.6296
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.9015  P=0.8427  R=0.9530  F1=0.8863
[Val  ] Acc=0.8784  P=0.6340  R=0.7173  F1=0.6686
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  15/150
[Train] Acc=0.9485  P=0.8915  R=0.9711  F1=0.9263
[Val  ] Acc=0.9054  P=0.7269  R=0.7436  F1=0.7349
       fusion_alpha=0.259  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.9894  P=0.9868  R=0.9926  F1=0.9896
[Val  ] Acc=0.9189  P=0.6799  R=0.7476  F1=0.7061
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  25/150
[Train] Acc=0.9758  P=0.9703  R=0.9828  F1=0.9762
[Val  ] Acc=0.8784  P=0.6314  R=0.7356  F1=0.6750
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  30/150
[Train] Acc=0.9864  P=0.9758  R=0.9918  F1=0.9835
[Val  ] Acc=0.9189  P=0.7211  R=0.7658  F1=0.7417
       fusion_alpha=0.255  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.9803  P=0.9486  R=0.9926  F1=0.9689
[Val  ] Acc=0.8919  P=0.7035  R=0.7213  F1=0.7106
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  40/150
[Train] Acc=0.9970  P=0.9770  R=0.9991  F1=0.9877
[Val  ] Acc=0.8919  P=0.7035  R=0.7213  F1=0.7106
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  45/150
[Train] Acc=0.9606  P=0.9212  R=0.9746  F1=0.9463
[Val  ] Acc=0.8649  P=0.6203  R=0.7133  F1=0.6594
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 45 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.8798  P=0.8899  R=0.7900  F1=0.7894
✅ Best val F1: 0.7417
✅ Test F1:     0.7894

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9402    0.8800    0.9091       125
          GS     0.5806    0.8571    0.6923        21
         MSI     0.9286    0.9630    0.9455        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8798       183
   macro avg     0.8899    0.7900    0.7894       183
weighted avg     0.9005    0.8798    0.8814       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.5466  std=0.4990  min=0.0000  max=1.0000
   meth : mean=0.2484  std=0.4307  min=0.0000  max=1.0000
   mirna: mean=0.2050  std=0.4021  min=0.0000  max=1.0000

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
[Train] Acc=0.4152  P=0.2513  R=0.2944  F1=0.2236
[Val  ] Acc=0.5946  P=0.4411  R=0.4754  F1=0.3588
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.7379  P=0.5279  R=0.6722  F1=0.5743
[Val  ] Acc=0.8243  P=0.5771  R=0.7418  F1=0.6312
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.9167  P=0.8153  R=0.9712  F1=0.8743
[Val  ] Acc=0.8649  P=0.8074  R=0.7587  F1=0.7779
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  15/150
[Train] Acc=0.9621  P=0.9069  R=0.9824  F1=0.9412
[Val  ] Acc=0.8919  P=0.7492  R=0.7072  F1=0.7251
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  20/150
[Train] Acc=0.9515  P=0.9067  R=0.9633  F1=0.9317
[Val  ] Acc=0.8243  P=0.6458  R=0.6872  F1=0.6593
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
⏹️  Early stopping tại epoch 24 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8361  P=0.7216  R=0.7466  F1=0.7296
✅ Best val F1: 0.8174
✅ Test F1:     0.7296

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9211    0.8468    0.8824       124
          GS     0.4828    0.6364    0.5490        22
         MSI     0.8710    1.0000    0.9310        27
      HM-SNV     0.3333    0.2500    0.2857         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8361       183
   macro avg     0.7216    0.7466    0.7296       183
weighted avg     0.8507    0.8361    0.8403       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.3352  std=0.4674  min=0.0000  max=1.0000
   meth : mean=0.4073  std=0.4819  min=0.0000  max=1.0000
   mirna: mean=0.2575  std=0.4250  min=0.0000  max=1.0000

📈 5-fold CV summary
  ACCURACY : mean=0.8702  std=0.0339
  PRECISION: mean=0.7793  std=0.0777
  RECALL   : mean=0.7791  std=0.0775
  F1       : mean=0.7645  std=0.0663