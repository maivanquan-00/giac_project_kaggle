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
[Train] Acc=0.0986  P=0.1763  R=0.1495  F1=0.0807
[Val  ] Acc=0.0811  P=0.1646  R=0.2444  F1=0.0735
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.1882  P=0.3033  R=0.3413  F1=0.1939
[Val  ] Acc=0.1892  P=0.2854  R=0.4554  F1=0.2090
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.3338  P=0.3419  R=0.4868  F1=0.2925
[Val  ] Acc=0.4459  P=0.4093  R=0.6205  F1=0.4142
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.5281  P=0.4411  R=0.6469  F1=0.4553
[Val  ] Acc=0.5135  P=0.5392  R=0.5587  F1=0.4734
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.7329  P=0.5877  R=0.8345  F1=0.6436
[Val  ] Acc=0.6892  P=0.6130  R=0.7209  F1=0.6414
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.8346  P=0.7071  R=0.9118  F1=0.7646
[Val  ] Acc=0.7838  P=0.7126  R=0.7489  F1=0.7263
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.8786  P=0.7994  R=0.9424  F1=0.8513
[Val  ] Acc=0.7703  P=0.6052  R=0.6671  F1=0.6271
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.9241  P=0.8502  R=0.9691  F1=0.9000
[Val  ] Acc=0.8378  P=0.8350  R=0.7831  F1=0.7885
Fold 1 | Epoch  40/150
[Train] Acc=0.9423  P=0.8927  R=0.9766  F1=0.9286
[Val  ] Acc=0.8378  P=0.8336  R=0.7831  F1=0.7870
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  45/150
[Train] Acc=0.9484  P=0.8818  R=0.9811  F1=0.9247
[Val  ] Acc=0.8514  P=0.8450  R=0.7871  F1=0.7951
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  50/150
[Train] Acc=0.9681  P=0.9186  R=0.9885  F1=0.9500
[Val  ] Acc=0.8649  P=0.7696  R=0.7911  F1=0.7773
Fold 1 | Epoch  55/150
[Train] Acc=0.9788  P=0.9401  R=0.9916  F1=0.9643
[Val  ] Acc=0.8649  P=0.8592  R=0.7911  F1=0.8039
Fold 1 | Epoch  60/150
[Train] Acc=0.9848  P=0.9702  R=0.9934  F1=0.9813
[Val  ] Acc=0.8919  P=0.9013  R=0.7991  F1=0.8239
⏹️  Early stopping tại epoch 64 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8315  P=0.7078  R=0.8062  F1=0.7484
✅ Best val F1: 0.8473
✅ Test F1:     0.7484

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9450    0.8240    0.8803       125
          GS     0.5625    0.8182    0.6667        22
         MSI     0.7742    0.8889    0.8276        27
      HM-SNV     0.4000    0.5000    0.4444         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8315       184
   macro avg     0.7078    0.8062    0.7484       184
weighted avg     0.8595    0.8315    0.8390       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.3828  std=0.0611  min=0.3151  max=0.4916
   meth : mean=0.3008  std=0.0366  min=0.2372  max=0.3425
   mirna: mean=0.3163  std=0.0246  min=0.2712  max=0.3424

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
[Train] Acc=0.1624  P=0.1812  R=0.2417  F1=0.1119
[Val  ] Acc=0.1486  P=0.2195  R=0.1764  F1=0.0886
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.2367  P=0.2911  R=0.4288  F1=0.2113
[Val  ] Acc=0.1081  P=0.2843  R=0.2706  F1=0.1121
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.3323  P=0.3346  R=0.4620  F1=0.2938
[Val  ] Acc=0.2432  P=0.3211  R=0.4714  F1=0.2410
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.5402  P=0.4418  R=0.6943  F1=0.4688
[Val  ] Acc=0.4054  P=0.4490  R=0.5943  F1=0.4119
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.6859  P=0.5468  R=0.8014  F1=0.5989
[Val  ] Acc=0.7838  P=0.5374  R=0.6792  F1=0.5772
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.7739  P=0.6827  R=0.8934  F1=0.7367
[Val  ] Acc=0.8243  P=0.6863  R=0.7690  F1=0.7202
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.8649  P=0.7585  R=0.9052  F1=0.8089
[Val  ] Acc=0.8108  P=0.6210  R=0.7832  F1=0.6733
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.9241  P=0.8627  R=0.9648  F1=0.9067
[Val  ] Acc=0.8378  P=0.7894  R=0.7730  F1=0.7566
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  40/150
[Train] Acc=0.9332  P=0.8872  R=0.9718  F1=0.9235
[Val  ] Acc=0.8784  P=0.7315  R=0.8174  F1=0.7668
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  45/150
[Train] Acc=0.9530  P=0.8916  R=0.9776  F1=0.9302
[Val  ] Acc=0.8649  P=0.8143  R=0.7810  F1=0.7743
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  50/150
[Train] Acc=0.9681  P=0.9383  R=0.9885  F1=0.9611
[Val  ] Acc=0.8649  P=0.8143  R=0.7810  F1=0.7743
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  55/150
[Train] Acc=0.9833  P=0.9437  R=0.9951  F1=0.9670
[Val  ] Acc=0.8649  P=0.8143  R=0.7810  F1=0.7743
Fold 2 | Epoch  60/150
[Train] Acc=0.9894  P=0.9463  R=0.9969  F1=0.9695
[Val  ] Acc=0.8784  P=0.7917  R=0.7992  F1=0.7617
Fold 2 | Epoch  65/150
[Train] Acc=0.9848  P=0.9664  R=0.9934  F1=0.9793
[Val  ] Acc=0.8784  P=0.8211  R=0.7992  F1=0.7864
⏹️  Early stopping tại epoch 68 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.9022  P=0.7404  R=0.8069  F1=0.7547
✅ Best val F1: 0.8407
✅ Test F1:     0.7547

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     1.0000    0.9040    0.9496       125
          GS     0.7778    0.9545    0.8571        22
         MSI     0.7576    0.9259    0.8333        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     0.6667    1.0000    0.8000         6

    accuracy                         0.9022       184
   macro avg     0.7404    0.8069    0.7547       184
weighted avg     0.9161    0.9022    0.9032       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.3544  std=0.0385  min=0.3077  max=0.4256
   meth : mean=0.3216  std=0.0241  min=0.2781  max=0.3512
   mirna: mean=0.3240  std=0.0144  min=0.2963  max=0.3412

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
[Train] Acc=0.2606  P=0.2091  R=0.1951  F1=0.1620
[Val  ] Acc=0.2703  P=0.2684  R=0.2975  F1=0.2123
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.3045  P=0.3020  R=0.3868  F1=0.2514
[Val  ] Acc=0.2703  P=0.3965  R=0.4522  F1=0.3018
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.3712  P=0.3406  R=0.4956  F1=0.3131
[Val  ] Acc=0.3649  P=0.3924  R=0.5438  F1=0.3299
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.5515  P=0.4555  R=0.6462  F1=0.4720
[Val  ] Acc=0.4865  P=0.4840  R=0.7731  F1=0.4827
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.7182  P=0.5991  R=0.7776  F1=0.6390
[Val  ] Acc=0.7297  P=0.5657  R=0.7774  F1=0.6209
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.8106  P=0.7159  R=0.8991  F1=0.7665
[Val  ] Acc=0.7568  P=0.5859  R=0.7895  F1=0.6383
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.8424  P=0.7643  R=0.9328  F1=0.8216
[Val  ] Acc=0.7568  P=0.5944  R=0.8036  F1=0.6526
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9136  P=0.8598  R=0.9481  F1=0.8971
[Val  ] Acc=0.8243  P=0.6404  R=0.8236  F1=0.7022
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  40/150
[Train] Acc=0.9409  P=0.8850  R=0.9763  F1=0.9248
[Val  ] Acc=0.7973  P=0.6473  R=0.8298  F1=0.6948
Fold 3 | Epoch  45/150
[Train] Acc=0.9576  P=0.9339  R=0.9833  F1=0.9556
[Val  ] Acc=0.7838  P=0.6433  R=0.8258  F1=0.6973
Fold 3 | Epoch  50/150
[Train] Acc=0.9712  P=0.9608  R=0.9915  F1=0.9740
[Val  ] Acc=0.7973  P=0.6567  R=0.8116  F1=0.7041
⏹️  Early stopping tại epoch 51 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8087  P=0.6712  R=0.7077  F1=0.6874
✅ Best val F1: 0.7483
✅ Test F1:     0.6874

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.8908    0.8480    0.8689       125
          GS     0.3462    0.4286    0.3830        21
         MSI     0.9286    0.9286    0.9286        28
      HM-SNV     0.3333    0.3333    0.3333         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8087       183
   macro avg     0.6712    0.7077    0.6874       183
weighted avg     0.8238    0.8087    0.8152       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.3784  std=0.1487  min=0.2481  max=0.6631
   meth : mean=0.3041  std=0.0886  min=0.1415  max=0.3853
   mirna: mean=0.3175  std=0.0602  min=0.1954  max=0.3666

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
[Train] Acc=0.1894  P=0.1973  R=0.2325  F1=0.1432
[Val  ] Acc=0.2432  P=0.2408  R=0.3300  F1=0.1889
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.2197  P=0.2525  R=0.3775  F1=0.1898
[Val  ] Acc=0.2703  P=0.3314  R=0.4563  F1=0.2477
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.3697  P=0.3322  R=0.5464  F1=0.3117
[Val  ] Acc=0.3108  P=0.3268  R=0.4501  F1=0.2636
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.6076  P=0.4671  R=0.7079  F1=0.5114
[Val  ] Acc=0.5270  P=0.4103  R=0.5708  F1=0.4285
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.6894  P=0.5790  R=0.8275  F1=0.6443
[Val  ] Acc=0.7027  P=0.4701  R=0.6370  F1=0.5162
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.8000  P=0.6971  R=0.8864  F1=0.7533
[Val  ] Acc=0.8243  P=0.5788  R=0.6831  F1=0.6179
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.8591  P=0.7679  R=0.9363  F1=0.8298
[Val  ] Acc=0.8649  P=0.6113  R=0.7133  F1=0.6530
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.9242  P=0.8382  R=0.9464  F1=0.8845
[Val  ] Acc=0.8514  P=0.6295  R=0.7276  F1=0.6699
Fold 4 | Epoch  40/150
[Train] Acc=0.9485  P=0.8809  R=0.9636  F1=0.9172
[Val  ] Acc=0.8378  P=0.5809  R=0.7094  F1=0.6264
Fold 4 | Epoch  45/150
[Train] Acc=0.9788  P=0.9579  R=0.9916  F1=0.9738
[Val  ] Acc=0.8784  P=0.6456  R=0.7356  F1=0.6826
⏹️  Early stopping tại epoch 49 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.7923  P=0.6679  R=0.7428  F1=0.6942
✅ Best val F1: 0.7166
✅ Test F1:     0.6942

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9065    0.7760    0.8362       125
          GS     0.4848    0.7619    0.5926        21
         MSI     0.7576    0.9259    0.8333        27
      HM-SNV     0.3333    0.2500    0.2857         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.7923       183
   macro avg     0.6679    0.7428    0.6942       183
weighted avg     0.8220    0.7923    0.7986       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.3654  std=0.0502  min=0.2985  max=0.4630
   meth : mean=0.3196  std=0.0527  min=0.2220  max=0.3899
   mirna: mean=0.3150  std=0.0042  min=0.3064  max=0.3245

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
[Train] Acc=0.2091  P=0.2130  R=0.2571  F1=0.1520
[Val  ] Acc=0.2027  P=0.2196  R=0.2026  F1=0.1455
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.4045  P=0.2821  R=0.3827  F1=0.2502
[Val  ] Acc=0.4595  P=0.2872  R=0.3604  F1=0.2256
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.3848  P=0.3447  R=0.4732  F1=0.3107
[Val  ] Acc=0.4865  P=0.3214  R=0.3474  F1=0.3024
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.4788  P=0.4580  R=0.6642  F1=0.4582
[Val  ] Acc=0.4459  P=0.4012  R=0.5427  F1=0.4069
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.7121  P=0.5569  R=0.7851  F1=0.6121
[Val  ] Acc=0.6486  P=0.5200  R=0.6250  F1=0.5341
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.8182  P=0.7161  R=0.9215  F1=0.7738
[Val  ] Acc=0.7838  P=0.5714  R=0.6974  F1=0.6176
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  30/150
[Train] Acc=0.9121  P=0.8162  R=0.9656  F1=0.8700
[Val  ] Acc=0.7703  P=0.5771  R=0.6752  F1=0.6069
Fold 5 | Epoch  35/150
[Train] Acc=0.9318  P=0.8361  R=0.9741  F1=0.8930
[Val  ] Acc=0.7703  P=0.5523  R=0.6712  F1=0.5858
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  40/150
[Train] Acc=0.9530  P=0.8666  R=0.9819  F1=0.9170
[Val  ] Acc=0.8243  P=0.5806  R=0.7236  F1=0.6184
Fold 5 | Epoch  45/150
[Train] Acc=0.9591  P=0.9020  R=0.9827  F1=0.9380
[Val  ] Acc=0.8243  P=0.5889  R=0.7236  F1=0.6298
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  50/150
[Train] Acc=0.9803  P=0.9587  R=0.9942  F1=0.9754
[Val  ] Acc=0.8784  P=0.8206  R=0.8356  F1=0.7910
Fold 5 | Epoch  55/150
[Train] Acc=0.9818  P=0.9604  R=0.9931  F1=0.9757
[Val  ] Acc=0.8243  P=0.5689  R=0.6689  F1=0.6023
Fold 5 | Epoch  60/150
[Train] Acc=0.9864  P=0.9740  R=0.9938  F1=0.9835
[Val  ] Acc=0.8243  P=0.7521  R=0.7649  F1=0.7161
⏹️  Early stopping tại epoch 62 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8689  P=0.8309  R=0.7430  F1=0.7378
✅ Best val F1: 0.7967
✅ Test F1:     0.7378

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9187    0.9113    0.9150       124
          GS     0.6190    0.5909    0.6047        22
         MSI     0.8667    0.9630    0.9123        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.8689       183
   macro avg     0.8309    0.7430    0.7378       183
weighted avg     0.8712    0.8689    0.8641       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.3989  std=0.1060  min=0.2907  max=0.5952
   meth : mean=0.3063  std=0.0741  min=0.1758  max=0.3851
   mirna: mean=0.2948  std=0.0320  min=0.2289  max=0.3242

📈 5-fold CV summary
  ACCURACY : mean=0.8407  std=0.0400
  PRECISION: mean=0.7236  std=0.0598
  RECALL   : mean=0.7613  std=0.0391
  F1       : mean=0.7245  std=0.0281


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

         CIN     0.8672    0.8880    0.8775       125
          GS     0.6667    0.5455    0.6000        22
         MSI     0.8095    0.6296    0.7083        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     0.4286    1.0000    0.6000         6

    accuracy                         0.8043       184
   macro avg     0.6877    0.7126    0.6714       184
weighted avg     0.8161    0.8043    0.8038       184

[Test] Acc=0.8043  P=0.6877  R=0.7126  F1=0.6714

🔍 Patient Modality Gate Statistics (N=184)
   Gene expression     : mean=0.3781  std=0.0573
   DNA methylation     : mean=0.3036  std=0.0345
   miRNA               : mean=0.3183  std=0.0228

✔️  Accuracy: 0.8043
   Correct: 148 / 184