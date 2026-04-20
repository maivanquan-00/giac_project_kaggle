preprocessing:
  gene_top_k: 5000
  meth_top_k: 5000
  mirna_top_k: 1881
  feature_selection_method: "anova"
  val_size: 0.1
  cv_folds: 5

  /kaggle/working/giac_project_kaggle
🖥️  Device: cuda
📂 Loading data từ: /kaggle/input/datasets/maivanquan/datn-2025-2/data_final
  Labels : (917, 3)
  Gene   : (917, 19930)
  Meth   : (917, 23111)
  miRNA  : (917, 1881)

  Samples sau align : 917
  Phân bố subtype   : {np.int64(0): np.int64(624), np.int64(1): np.int64(108), np.int64(2): np.int64(136), np.int64(3): np.int64(19), np.int64(4): np.int64(30)}

📐 Fold 1: gene=5000, meth=5000, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 5000
   CpG   nodes : 5000
   miRNA nodes : 1881
   Parsing emQTL COAD... 102,485 edges
   Parsing emQTL ESCA... 29,670 edges
   Parsing emQTL READ... 173 edges
   Parsing emQTL STAD... 41,716 edges
   CpG→Gene edges  : 174,044
   Building ENSP→symbol map từ alias file... 5,093 proteins mapped
   Parsing STRING links... 18,313 unique edges
   Gene↔Gene edges : 36,626
   Parsing hsa_MTI.csv... 111,777 edges
   miRNA→Gene edges: 111,777

🧠 Fold 1 model parameters: 5,189,513
🚀 Bắt đầu training fold 1...

🗓️  Scheduler: onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.2049  P=0.3496  R=0.3500  F1=0.2313
[Val  ] Acc=0.3919  P=0.4698  R=0.7228  F1=0.4439
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.7527  P=0.6222  R=0.8432  F1=0.6594
[Val  ] Acc=0.7568  P=0.5998  R=0.6631  F1=0.6209
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.9697  P=0.9206  R=0.9826  F1=0.9478
[Val  ] Acc=0.8649  P=0.8567  R=0.7911  F1=0.8056
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
Fold 1 | Epoch  15/150
[Train] Acc=0.9545  P=0.9128  R=0.9748  F1=0.9404
[Val  ] Acc=0.8514  P=0.8450  R=0.7871  F1=0.7951
       fusion_alpha=0.259  (GAT=0.26, Shortcut=0.74)
Fold 1 | Epoch  20/150
[Train] Acc=0.9560  P=0.8772  R=0.9422  F1=0.9069
[Val  ] Acc=0.8514  P=0.8418  R=0.7689  F1=0.7874
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
⏹️  Early stopping tại epoch 24 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8315  P=0.8178  R=0.7370  F1=0.7272
✅ Best val F1: 0.8460
✅ Test F1:     0.7272

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9224    0.8560    0.8880       125
          GS     0.5161    0.7273    0.6038        22
         MSI     0.7931    0.8519    0.8214        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8315       184
   macro avg     0.8178    0.7370    0.7272       184
weighted avg     0.8544    0.8315    0.8348       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.4873  std=0.4924  min=0.0027  max=0.9963
   meth : mean=0.0085  std=0.0176  min=0.0024  max=0.1697
   mirna: mean=0.5043  std=0.4911  min=0.0013  max=0.9931

📐 Fold 2: gene=5000, meth=5000, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 5000
   CpG   nodes : 5000
   miRNA nodes : 1881
   Parsing emQTL COAD... 100,299 edges
   Parsing emQTL ESCA... 29,936 edges
   Parsing emQTL READ... 174 edges
   Parsing emQTL STAD... 41,857 edges
   CpG→Gene edges  : 172,266
   Building ENSP→symbol map từ alias file... 5,090 proteins mapped
   Parsing STRING links... 18,154 unique edges
   Gene↔Gene edges : 36,308
   Parsing hsa_MTI.csv... 111,519 edges
   miRNA→Gene edges: 111,519

🧠 Fold 2 model parameters: 5,189,513
🚀 Bắt đầu training fold 2...

🗓️  Scheduler: onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.3354  P=0.3561  R=0.4750  F1=0.3004
[Val  ] Acc=0.5946  P=0.4348  R=0.5543  F1=0.4402
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.7329  P=0.6065  R=0.8307  F1=0.6596
[Val  ] Acc=0.8378  P=0.6668  R=0.7912  F1=0.7072
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.9181  P=0.8322  R=0.9443  F1=0.8756
[Val  ] Acc=0.8108  P=0.6796  R=0.7650  F1=0.7129
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
Fold 2 | Epoch  15/150
[Train] Acc=0.9605  P=0.9266  R=0.9841  F1=0.9522
[Val  ] Acc=0.8649  P=0.6313  R=0.6850  F1=0.6510
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.9757  P=0.9461  R=0.9864  F1=0.9648
[Val  ] Acc=0.9189  P=0.8610  R=0.8152  F1=0.8144
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.9757  P=0.9374  R=0.9864  F1=0.9597
[Val  ] Acc=0.8784  P=0.6313  R=0.6890  F1=0.6530
       fusion_alpha=0.255  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  30/150
[Train] Acc=0.9681  P=0.9321  R=0.9788  F1=0.9538
[Val  ] Acc=0.8378  P=0.5978  R=0.6952  F1=0.6380
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  35/150
[Train] Acc=0.9712  P=0.9221  R=0.9764  F1=0.9455
[Val  ] Acc=0.8649  P=0.6094  R=0.7032  F1=0.6220
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 36 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.8913  P=0.8481  R=0.8105  F1=0.8048
✅ Best val F1: 0.8238
✅ Test F1:     0.8048

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9355    0.9280    0.9317       125
          GS     0.6800    0.7727    0.7234        22
         MSI     0.9583    0.8519    0.9020        27
      HM-SNV     1.0000    0.5000    0.6667         4
         EBV     0.6667    1.0000    0.8000         6

    accuracy                         0.8913       184
   macro avg     0.8481    0.8105    0.8048       184
weighted avg     0.9009    0.8913    0.8924       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.0054  std=0.0160  min=0.0021  max=0.2187
   meth : mean=0.5109  std=0.4961  min=0.0011  max=0.9967
   mirna: mean=0.4838  std=0.4951  min=0.0012  max=0.9968

📐 Fold 3: gene=5000, meth=5000, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 5000
   CpG   nodes : 5000
   miRNA nodes : 1881
   Parsing emQTL COAD... 100,711 edges
   Parsing emQTL ESCA... 29,955 edges
   Parsing emQTL READ... 158 edges
   Parsing emQTL STAD... 42,064 edges
   CpG→Gene edges  : 172,888
   Building ENSP→symbol map từ alias file... 5,091 proteins mapped
   Parsing STRING links... 17,895 unique edges
   Gene↔Gene edges : 35,790
   Parsing hsa_MTI.csv... 111,994 edges
   miRNA→Gene edges: 111,994

🧠 Fold 3 model parameters: 5,189,513
🚀 Bắt đầu training fold 3...

🗓️  Scheduler: onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.2500  P=0.3088  R=0.3758  F1=0.2211
[Val  ] Acc=0.2973  P=0.3628  R=0.5251  F1=0.2768
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.7227  P=0.6891  R=0.7376  F1=0.6472
[Val  ] Acc=0.7162  P=0.5380  R=0.7098  F1=0.5824
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.9091  P=0.8586  R=0.9409  F1=0.8928
[Val  ] Acc=0.8378  P=0.7769  R=0.8418  F1=0.7910
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.9712  P=0.9517  R=0.9852  F1=0.9675
[Val  ] Acc=0.8514  P=0.8163  R=0.8458  F1=0.7919
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
Fold 3 | Epoch  20/150
[Train] Acc=0.9621  P=0.9384  R=0.9809  F1=0.9574
[Val  ] Acc=0.8243  P=0.7266  R=0.8196  F1=0.7520
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 3 | Epoch  25/150
[Train] Acc=0.9803  P=0.9645  R=0.9942  F1=0.9784
[Val  ] Acc=0.8514  P=0.7850  R=0.8458  F1=0.8022
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 29 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8689  P=0.7540  R=0.7411  F1=0.7429
✅ Best val F1: 0.8504
✅ Test F1:     0.7429

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9055    0.9200    0.9127       125
          GS     0.5789    0.5238    0.5500        21
         MSI     0.9286    0.9286    0.9286        28
      HM-SNV     0.5000    0.3333    0.4000         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8689       183
   macro avg     0.7540    0.7411    0.7429       183
weighted avg     0.8633    0.8689    0.8654       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.5846  std=0.4856  min=0.0014  max=0.9958
   meth : mean=0.0077  std=0.0192  min=0.0028  max=0.1710
   mirna: mean=0.4078  std=0.4857  min=0.0014  max=0.9958

📐 Fold 4: gene=5000, meth=5000, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 5000
   CpG   nodes : 5000
   miRNA nodes : 1881
   Parsing emQTL COAD... 100,365 edges
   Parsing emQTL ESCA... 30,241 edges
   Parsing emQTL READ... 157 edges
   Parsing emQTL STAD... 42,112 edges
   CpG→Gene edges  : 172,875
   Building ENSP→symbol map từ alias file... 5,094 proteins mapped
   Parsing STRING links... 18,381 unique edges
   Gene↔Gene edges : 36,762
   Parsing hsa_MTI.csv... 112,554 edges
   miRNA→Gene edges: 112,554

🧠 Fold 4 model parameters: 5,189,513
🚀 Bắt đầu training fold 4...

🗓️  Scheduler: onecycle
Fold 4 | Epoch   1/150
[Train] Acc=0.3742  P=0.2822  R=0.2842  F1=0.2200
[Val  ] Acc=0.6351  P=0.3499  R=0.3804  F1=0.3208
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.8015  P=0.6574  R=0.8304  F1=0.7222
[Val  ] Acc=0.8649  P=0.6166  R=0.7498  F1=0.6703
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.9318  P=0.8844  R=0.9593  F1=0.9182
[Val  ] Acc=0.8784  P=0.6340  R=0.7173  F1=0.6686
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.9682  P=0.9246  R=0.9853  F1=0.9512
[Val  ] Acc=0.8919  P=0.7098  R=0.7254  F1=0.7172
       fusion_alpha=0.259  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  20/150
[Train] Acc=0.9818  P=0.9679  R=0.9925  F1=0.9795
[Val  ] Acc=0.8784  P=0.6866  R=0.7173  F1=0.7007
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  25/150
[Train] Acc=0.9970  P=0.9950  R=0.9991  F1=0.9970
[Val  ] Acc=0.8919  P=0.6510  R=0.7213  F1=0.6786
       fusion_alpha=0.255  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 29 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.8361  P=0.8527  R=0.7534  F1=0.7528
✅ Best val F1: 0.7269
✅ Test F1:     0.7528

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9130    0.8400    0.8750       125
          GS     0.4839    0.7143    0.5769        21
         MSI     0.8667    0.9630    0.9123        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8361       183
   macro avg     0.8527    0.7534    0.7528       183
weighted avg     0.8617    0.8361    0.8400       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.4880  std=0.4957  min=0.0010  max=0.9963
   meth : mean=0.5068  std=0.4969  min=0.0012  max=0.9966
   mirna: mean=0.0052  std=0.0052  min=0.0024  max=0.0468

📐 Fold 5: gene=5000, meth=5000, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 5000
   CpG   nodes : 5000
   miRNA nodes : 1881
   Parsing emQTL COAD... 100,538 edges
   Parsing emQTL ESCA... 29,814 edges
   Parsing emQTL READ... 167 edges
   Parsing emQTL STAD... 41,955 edges
   CpG→Gene edges  : 172,474
   Building ENSP→symbol map từ alias file... 5,093 proteins mapped
   Parsing STRING links... 18,270 unique edges
   Gene↔Gene edges : 36,540
   Parsing hsa_MTI.csv... 112,126 edges
   miRNA→Gene edges: 112,126

🧠 Fold 5 model parameters: 5,189,513
🚀 Bắt đầu training fold 5...

🗓️  Scheduler: onecycle
Fold 5 | Epoch   1/150
[Train] Acc=0.3091  P=0.2727  R=0.3697  F1=0.2196
[Val  ] Acc=0.5405  P=0.3840  R=0.5971  F1=0.3940
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.7288  P=0.5703  R=0.7538  F1=0.6232
[Val  ] Acc=0.8378  P=0.6064  R=0.7458  F1=0.6595
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.9258  P=0.8465  R=0.9691  F1=0.8968
[Val  ] Acc=0.8784  P=0.7350  R=0.6849  F1=0.6959
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.9500  P=0.9399  R=0.9810  F1=0.9562
[Val  ] Acc=0.9054  P=0.7367  R=0.7294  F1=0.7324
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.9803  P=0.9360  R=0.9889  F1=0.9601
[Val  ] Acc=0.8784  P=0.7158  R=0.7578  F1=0.7284
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.9985  P=0.9974  R=0.9996  F1=0.9985
[Val  ] Acc=0.8514  P=0.7164  R=0.6769  F1=0.6941
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 5 | Epoch  30/150
[Train] Acc=0.9833  P=0.9765  R=0.9764  F1=0.9758
[Val  ] Acc=0.8784  P=0.7291  R=0.7396  F1=0.7323
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 5 | Epoch  35/150
[Train] Acc=0.9773  P=0.9589  R=0.9831  F1=0.9706
[Val  ] Acc=0.8514  P=0.6298  R=0.6952  F1=0.6550
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 38 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8525  P=0.7561  R=0.7382  F1=0.7371
✅ Best val F1: 0.7997
✅ Test F1:     0.7371

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9322    0.8871    0.9091       124
          GS     0.4815    0.5909    0.5306        22
         MSI     0.8667    0.9630    0.9123        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8525       183
   macro avg     0.7561    0.7382    0.7371       183
weighted avg     0.8611    0.8525    0.8545       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.4644  std=0.4841  min=0.0000  max=0.9984
   meth : mean=0.1184  std=0.3052  min=0.0000  max=0.9678
   mirna: mean=0.4172  std=0.4751  min=0.0006  max=1.0000

📈 5-fold CV summary
  ACCURACY : mean=0.8560  std=0.0220
  PRECISION: mean=0.8057  std=0.0431
  RECALL   : mean=0.7561  std=0.0278
  F1       : mean=0.7530  std=0.0272