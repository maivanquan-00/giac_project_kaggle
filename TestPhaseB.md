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

🧠 Fold 1 model parameters: 1,583,724
🚀 Bắt đầu training fold 1...

🗓️  Scheduler: onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.2170  P=0.1738  R=0.1403  F1=0.1321
[Val  ] Acc=0.2973  P=0.1972  R=0.2387  F1=0.1885
       Global modality weights: gene=0.327, meth=0.334, mirna=0.338

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.3475  P=0.3112  R=0.3956  F1=0.2697
[Val  ] Acc=0.3514  P=0.3048  R=0.4358  F1=0.2834
       Global modality weights: gene=0.327, meth=0.334, mirna=0.338

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.4734  P=0.3692  R=0.5300  F1=0.3670
[Val  ] Acc=0.4865  P=0.4267  R=0.6325  F1=0.4494
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.6419  P=0.5314  R=0.7382  F1=0.5661
[Val  ] Acc=0.7162  P=0.6285  R=0.7289  F1=0.6597
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.8058  P=0.7091  R=0.8628  F1=0.7602
[Val  ] Acc=0.8514  P=0.7529  R=0.7689  F1=0.7593
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.8786  P=0.8089  R=0.9520  F1=0.8600
[Val  ] Acc=0.7838  P=0.6239  R=0.6711  F1=0.6427
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

Fold 1 | Epoch  30/150
[Train] Acc=0.9636  P=0.9452  R=0.9872  F1=0.9638
[Val  ] Acc=0.8378  P=0.8300  R=0.7649  F1=0.7763
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.9833  P=0.9655  R=0.9908  F1=0.9776
[Val  ] Acc=0.8784  P=0.7869  R=0.7769  F1=0.7761
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

Fold 1 | Epoch  40/150
[Train] Acc=0.9894  P=0.9768  R=0.9969  F1=0.9865
[Val  ] Acc=0.8784  P=0.8782  R=0.7951  F1=0.8183
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

Fold 1 | Epoch  45/150
[Train] Acc=0.9909  P=0.9855  R=0.9973  F1=0.9912
[Val  ] Acc=0.8514  P=0.7551  R=0.7689  F1=0.7578
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  50/150
[Train] Acc=0.9939  P=0.9901  R=0.9982  F1=0.9940
[Val  ] Acc=0.8378  P=0.7405  R=0.7649  F1=0.7497
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

Fold 1 | Epoch  55/150
[Train] Acc=0.9894  P=0.9835  R=0.9969  F1=0.9899
[Val  ] Acc=0.8649  P=0.8554  R=0.7729  F1=0.7933
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

Fold 1 | Epoch  60/150
[Train] Acc=0.9985  P=0.9974  R=0.9996  F1=0.9985
[Val  ] Acc=0.8514  P=0.7551  R=0.7689  F1=0.7578
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

Fold 1 | Epoch  65/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.8378  P=0.8300  R=0.7649  F1=0.7763
       Global modality weights: gene=0.327, meth=0.333, mirna=0.340

⏹️  Early stopping tại epoch 67 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8370  P=0.7300  R=0.8020  F1=0.7594
✅ Best val F1: 0.8458
✅ Test F1:     0.7594

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9375    0.8400    0.8861       125
          GS     0.5625    0.8182    0.6667        22
         MSI     0.7931    0.8519    0.8214        27
      HM-SNV     0.5000    0.5000    0.5000         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8370       184
   macro avg     0.7300    0.8020    0.7594       184
weighted avg     0.8593    0.8370    0.8432       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.3243  std=0.4193  min=0.0003  max=0.9999
   meth : mean=0.4813  std=0.4114  min=0.0000  max=0.9984
   mirna: mean=0.1944  std=0.2698  min=0.0000  max=0.9825

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

🧠 Fold 2 model parameters: 1,583,724
🚀 Bắt đầu training fold 2...

🗓️  Scheduler: onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.1563  P=0.2133  R=0.2379  F1=0.1221
[Val  ] Acc=0.0946  P=0.0756  R=0.2091  F1=0.0952
       Global modality weights: gene=0.334, meth=0.335, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.2686  P=0.3091  R=0.4201  F1=0.2331
[Val  ] Acc=0.2027  P=0.2821  R=0.2986  F1=0.1612
       Global modality weights: gene=0.334, meth=0.335, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.4021  P=0.3709  R=0.5608  F1=0.3576
[Val  ] Acc=0.4459  P=0.3336  R=0.4496  F1=0.3272
       Global modality weights: gene=0.334, meth=0.335, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.6434  P=0.5163  R=0.7428  F1=0.5660
[Val  ] Acc=0.7027  P=0.4923  R=0.6187  F1=0.5314
       Global modality weights: gene=0.334, meth=0.334, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.7982  P=0.6744  R=0.8872  F1=0.7445
[Val  ] Acc=0.8243  P=0.6597  R=0.7690  F1=0.6961
       Global modality weights: gene=0.334, meth=0.335, mirna=0.331

Fold 2 | Epoch  25/150
[Train] Acc=0.9044  P=0.8414  R=0.9415  F1=0.8832
[Val  ] Acc=0.8378  P=0.6800  R=0.6770  F1=0.6777
       Global modality weights: gene=0.335, meth=0.334, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.9727  P=0.9232  R=0.9882  F1=0.9517
[Val  ] Acc=0.8649  P=0.7810  R=0.7810  F1=0.7810
       Global modality weights: gene=0.334, meth=0.334, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.9788  P=0.9513  R=0.9916  F1=0.9705
[Val  ] Acc=0.8649  P=0.7810  R=0.7810  F1=0.7810
       Global modality weights: gene=0.335, meth=0.334, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  40/150
[Train] Acc=0.9727  P=0.9557  R=0.9898  F1=0.9715
[Val  ] Acc=0.8378  P=0.7058  R=0.7730  F1=0.7310
       Global modality weights: gene=0.334, meth=0.334, mirna=0.331

Fold 2 | Epoch  45/150
[Train] Acc=0.9939  P=0.9782  R=0.9982  F1=0.9879
[Val  ] Acc=0.8649  P=0.8694  R=0.7627  F1=0.7989
       Global modality weights: gene=0.334, meth=0.334, mirna=0.331

Fold 2 | Epoch  50/150
[Train] Acc=0.9788  P=0.9313  R=0.9916  F1=0.9578
[Val  ] Acc=0.8514  P=0.7473  R=0.7770  F1=0.7588
       Global modality weights: gene=0.334, meth=0.334, mirna=0.331

Fold 2 | Epoch  55/150
[Train] Acc=0.9954  P=0.9862  R=0.9987  F1=0.9923
[Val  ] Acc=0.8649  P=0.7307  R=0.7810  F1=0.7488
       Global modality weights: gene=0.334, meth=0.334, mirna=0.331

⏹️  Early stopping tại epoch 58 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.8859  P=0.8189  R=0.7755  F1=0.7426
✅ Best val F1: 0.8164
✅ Test F1:     0.7426

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9828    0.9120    0.9461       125
          GS     0.6786    0.8636    0.7600        22
         MSI     0.7667    0.8519    0.8070        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     0.6667    1.0000    0.8000         6

    accuracy                         0.8859       184
   macro avg     0.8189    0.7755    0.7426       184
weighted avg     0.9047    0.8859    0.8868       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.3616  std=0.4524  min=0.0000  max=0.9998
   meth : mean=0.5680  std=0.4545  min=0.0001  max=0.9996
   mirna: mean=0.0704  std=0.1700  min=0.0001  max=0.8395

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

🧠 Fold 3 model parameters: 1,583,724
🚀 Bắt đầu training fold 3...

🗓️  Scheduler: onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.0970  P=0.2318  R=0.2534  F1=0.1004
[Val  ] Acc=0.0541  P=0.2164  R=0.3040  F1=0.0389
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.2833  P=0.2896  R=0.4426  F1=0.2082
[Val  ] Acc=0.3784  P=0.2909  R=0.3951  F1=0.2471
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.4197  P=0.4060  R=0.5866  F1=0.3563
[Val  ] Acc=0.5405  P=0.4314  R=0.6282  F1=0.4256
       Global modality weights: gene=0.338, meth=0.331, mirna=0.332

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.6682  P=0.5383  R=0.7458  F1=0.5823
[Val  ] Acc=0.7703  P=0.6264  R=0.8996  F1=0.6933
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.8167  P=0.6718  R=0.8848  F1=0.7356
[Val  ] Acc=0.7432  P=0.6135  R=0.7855  F1=0.6505
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.9121  P=0.8104  R=0.9683  F1=0.8701
[Val  ] Acc=0.8243  P=0.6398  R=0.8196  F1=0.7006
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.9576  P=0.8950  R=0.9812  F1=0.9325
[Val  ] Acc=0.8649  P=0.8100  R=0.8498  F1=0.7976
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9848  P=0.9302  R=0.9955  F1=0.9575
[Val  ] Acc=0.8784  P=0.8034  R=0.8356  F1=0.7839
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

Fold 3 | Epoch  40/150
[Train] Acc=0.9894  P=0.9724  R=0.9969  F1=0.9841
[Val  ] Acc=0.8919  P=0.8188  R=0.8396  F1=0.7941
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  45/150
[Train] Acc=0.9833  P=0.9639  R=0.9951  F1=0.9787
[Val  ] Acc=0.8649  P=0.7963  R=0.8134  F1=0.7699
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

Fold 3 | Epoch  50/150
[Train] Acc=0.9924  P=0.9897  R=0.9957  F1=0.9926
[Val  ] Acc=0.8919  P=0.8122  R=0.8578  F1=0.7973
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

Fold 3 | Epoch  55/150
[Train] Acc=0.9909  P=0.9675  R=0.9957  F1=0.9807
[Val  ] Acc=0.8649  P=0.7904  R=0.8316  F1=0.7744
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

Fold 3 | Epoch  60/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.8784  P=0.8034  R=0.8356  F1=0.7839
       Global modality weights: gene=0.338, meth=0.331, mirna=0.331

⏹️  Early stopping tại epoch 63 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8579  P=0.6793  R=0.7379  F1=0.7030
✅ Best val F1: 0.8161
✅ Test F1:     0.7030

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9187    0.9040    0.9113       125
          GS     0.6111    0.5238    0.5641        21
         MSI     0.8667    0.9286    0.8966        28
      HM-SNV     0.2500    0.3333    0.2857         3
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.8579       183
   macro avg     0.6793    0.7379    0.7030       183
weighted avg     0.8589    0.8579    0.8572       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.3737  std=0.4466  min=0.0003  max=0.9999
   meth : mean=0.5388  std=0.4142  min=0.0000  max=0.9988
   mirna: mean=0.0876  std=0.1175  min=0.0001  max=0.6730

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

🧠 Fold 4 model parameters: 1,583,724
🚀 Bắt đầu training fold 4...

🗓️  Scheduler: onecycle
Fold 4 | Epoch   1/150
[Train] Acc=0.2697  P=0.1894  R=0.2287  F1=0.1654
[Val  ] Acc=0.2973  P=0.2094  R=0.3488  F1=0.2087
       Global modality weights: gene=0.330, meth=0.341, mirna=0.330

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.3470  P=0.3012  R=0.4137  F1=0.2602
[Val  ] Acc=0.3243  P=0.3323  R=0.4034  F1=0.2633
       Global modality weights: gene=0.330, meth=0.340, mirna=0.330

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.4227  P=0.3610  R=0.5309  F1=0.3406
[Val  ] Acc=0.4595  P=0.3279  R=0.4576  F1=0.3076
       Global modality weights: gene=0.330, meth=0.339, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.6106  P=0.4851  R=0.7223  F1=0.5347
[Val  ] Acc=0.6081  P=0.4056  R=0.6090  F1=0.4384
       Global modality weights: gene=0.330, meth=0.339, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.7455  P=0.6368  R=0.8357  F1=0.7000
[Val  ] Acc=0.7162  P=0.5083  R=0.6410  F1=0.5397
       Global modality weights: gene=0.330, meth=0.339, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.8621  P=0.7668  R=0.9452  F1=0.8333
[Val  ] Acc=0.8108  P=0.5731  R=0.6791  F1=0.6163
       Global modality weights: gene=0.330, meth=0.340, mirna=0.330

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.9091  P=0.8226  R=0.9558  F1=0.8749
[Val  ] Acc=0.8649  P=0.6141  R=0.7133  F1=0.6552
       Global modality weights: gene=0.330, meth=0.339, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.9652  P=0.9406  R=0.9876  F1=0.9622
[Val  ] Acc=0.8649  P=0.6234  R=0.7133  F1=0.6603
       Global modality weights: gene=0.330, meth=0.339, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  40/150
[Train] Acc=0.9758  P=0.9312  R=0.9908  F1=0.9591
[Val  ] Acc=0.8649  P=0.6113  R=0.7133  F1=0.6530
       Global modality weights: gene=0.330, meth=0.340, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  45/150
[Train] Acc=0.9833  P=0.9563  R=0.9951  F1=0.9748
[Val  ] Acc=0.8784  P=0.6366  R=0.7173  F1=0.6685
       Global modality weights: gene=0.330, meth=0.340, mirna=0.331

Fold 4 | Epoch  50/150
[Train] Acc=0.9924  P=0.9696  R=0.9978  F1=0.9833
[Val  ] Acc=0.8784  P=0.6366  R=0.7173  F1=0.6685
       Global modality weights: gene=0.330, meth=0.340, mirna=0.331

Fold 4 | Epoch  55/150
[Train] Acc=0.9970  P=0.9954  R=0.9991  F1=0.9973
[Val  ] Acc=0.8514  P=0.6133  R=0.7093  F1=0.6500
       Global modality weights: gene=0.330, meth=0.340, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  60/150
[Train] Acc=0.9970  P=0.9832  R=0.9991  F1=0.9909
[Val  ] Acc=0.8919  P=0.6499  R=0.7213  F1=0.6740
       Global modality weights: gene=0.330, meth=0.340, mirna=0.331

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  65/150
[Train] Acc=0.9985  P=0.9975  R=0.9996  F1=0.9985
[Val  ] Acc=0.8919  P=0.6620  R=0.7213  F1=0.6813
       Global modality weights: gene=0.330, meth=0.340, mirna=0.331

Fold 4 | Epoch  70/150
[Train] Acc=0.9924  P=0.9763  R=0.9978  F1=0.9867
[Val  ] Acc=0.8649  P=0.6234  R=0.7133  F1=0.6603
       Global modality weights: gene=0.330, meth=0.340, mirna=0.331

Fold 4 | Epoch  75/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.8919  P=0.6620  R=0.7213  F1=0.6813
       Global modality weights: gene=0.330, meth=0.340, mirna=0.331

Fold 4 | Epoch  80/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.8919  P=0.6583  R=0.7213  F1=0.6795
       Global modality weights: gene=0.330, meth=0.340, mirna=0.331

⏹️  Early stopping tại epoch 83 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.8197  P=0.7080  R=0.7407  F1=0.7192
✅ Best val F1: 0.6813
✅ Test F1:     0.7192

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9035    0.8240    0.8619       125
          GS     0.5385    0.6667    0.5957        21
         MSI     0.7647    0.9630    0.8525        27
      HM-SNV     0.3333    0.2500    0.2857         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8197       183
   macro avg     0.7080    0.7407    0.7192       183
weighted avg     0.8318    0.8197    0.8219       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.4157  std=0.4428  min=0.0001  max=1.0000
   meth : mean=0.4968  std=0.4496  min=0.0000  max=0.9995
   mirna: mean=0.0875  std=0.2056  min=0.0000  max=0.9823

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

🧠 Fold 5 model parameters: 1,583,724
🚀 Bắt đầu training fold 5...

🗓️  Scheduler: onecycle
Fold 5 | Epoch   1/150
[Train] Acc=0.1848  P=0.1990  R=0.2039  F1=0.0963
[Val  ] Acc=0.1486  P=0.0324  R=0.2000  F1=0.0557
       Global modality weights: gene=0.327, meth=0.336, mirna=0.337

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.3424  P=0.2987  R=0.3784  F1=0.2684
[Val  ] Acc=0.5270  P=0.2946  R=0.3241  F1=0.2833
       Global modality weights: gene=0.327, meth=0.336, mirna=0.337

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.4439  P=0.3543  R=0.5044  F1=0.3491
[Val  ] Acc=0.5541  P=0.3618  R=0.4958  F1=0.3887
       Global modality weights: gene=0.327, meth=0.336, mirna=0.337

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.5894  P=0.4871  R=0.7148  F1=0.5259
[Val  ] Acc=0.7027  P=0.4868  R=0.6187  F1=0.5308
       Global modality weights: gene=0.326, meth=0.337, mirna=0.336

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.7742  P=0.6544  R=0.8519  F1=0.7070
[Val  ] Acc=0.6757  P=0.5088  R=0.6148  F1=0.5393
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.8667  P=0.7735  R=0.9347  F1=0.8349
[Val  ] Acc=0.7973  P=0.6147  R=0.7196  F1=0.6411
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

Fold 5 | Epoch  30/150
[Train] Acc=0.9348  P=0.8883  R=0.9787  F1=0.9266
[Val  ] Acc=0.8378  P=0.6110  R=0.7094  F1=0.6507
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

Fold 5 | Epoch  35/150
[Train] Acc=0.9742  P=0.9442  R=0.9924  F1=0.9670
[Val  ] Acc=0.8378  P=0.6175  R=0.6729  F1=0.6381
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

Fold 5 | Epoch  40/150
[Train] Acc=0.9788  P=0.9567  R=0.9938  F1=0.9741
[Val  ] Acc=0.8514  P=0.6319  R=0.6769  F1=0.6468
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  45/150
[Train] Acc=0.9864  P=0.9820  R=0.9917  F1=0.9867
[Val  ] Acc=0.8514  P=0.6315  R=0.7316  F1=0.6715
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

Fold 5 | Epoch  50/150
[Train] Acc=0.9818  P=0.9437  R=0.9781  F1=0.9599
[Val  ] Acc=0.8919  P=0.6628  R=0.7436  F1=0.6945
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  55/150
[Train] Acc=0.9955  P=0.9929  R=0.9987  F1=0.9958
[Val  ] Acc=0.8919  P=0.6825  R=0.7072  F1=0.6851
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

Fold 5 | Epoch  60/150
[Train] Acc=0.9909  P=0.9874  R=0.9930  F1=0.9902
[Val  ] Acc=0.8784  P=0.6494  R=0.7436  F1=0.6802
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

Fold 5 | Epoch  65/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.8919  P=0.6825  R=0.7072  F1=0.6851
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

Fold 5 | Epoch  70/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.8649  P=0.8353  R=0.7769  F1=0.7818
       Global modality weights: gene=0.327, meth=0.337, mirna=0.336

⏹️  Early stopping tại epoch 72 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8579  P=0.7687  R=0.7249  F1=0.7379
✅ Best val F1: 0.7818
✅ Test F1:     0.7379

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.8968    0.9113    0.9040       124
          GS     0.5500    0.5000    0.5238        22
         MSI     0.8966    0.9630    0.9286        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8579       183
   macro avg     0.7687    0.7249    0.7379       183
weighted avg     0.8498    0.8579    0.8526       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.3878  std=0.4535  min=0.0000  max=0.9998
   meth : mean=0.5557  std=0.4404  min=0.0000  max=1.0000
   mirna: mean=0.0566  std=0.0954  min=0.0000  max=0.3979

📈 5-fold CV summary
  ACCURACY : mean=0.8517  std=0.0223
  PRECISION: mean=0.7410  std=0.0487
  RECALL   : mean=0.7562  std=0.0284
  F1       : mean=0.7324  std=0.0195


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

         CIN     0.9008    0.8720    0.8862       125
          GS     0.7368    0.6364    0.6829        22
         MSI     0.8261    0.7037    0.7600        27
      HM-SNV     0.5000    0.5000    0.5000         4
         EBV     0.3529    1.0000    0.5217         6

    accuracy                         0.8152       184
   macro avg     0.6633    0.7424    0.6702       184
weighted avg     0.8437    0.8152    0.8231       184

[Test] Acc=0.8152  P=0.6633  R=0.7424  F1=0.6702

🔍 Patient Modality Gate Statistics (N=184)
   Gene expression     : mean=0.3977  std=0.1047
   DNA methylation     : mean=0.2946  std=0.0628
   miRNA               : mean=0.3077  std=0.0419

✔️  Accuracy: 0.8152
   Correct: 150 / 184