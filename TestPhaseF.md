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
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.5296  P=0.4404  R=0.6596  F1=0.4562
[Val  ] Acc=0.5270  P=0.5442  R=0.5627  F1=0.4800
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.7178  P=0.5743  R=0.8001  F1=0.6230
[Val  ] Acc=0.6892  P=0.6076  R=0.7209  F1=0.6334
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.8361  P=0.7101  R=0.9085  F1=0.7711
[Val  ] Acc=0.7703  P=0.7078  R=0.7449  F1=0.7206
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.8862  P=0.8211  R=0.9505  F1=0.8691
[Val  ] Acc=0.7703  P=0.6052  R=0.6671  F1=0.6271
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.9287  P=0.8677  R=0.9705  F1=0.9114
[Val  ] Acc=0.8649  P=0.8558  R=0.7911  F1=0.8041
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  40/150
[Train] Acc=0.9378  P=0.8880  R=0.9753  F1=0.9251
[Val  ] Acc=0.8378  P=0.8336  R=0.7831  F1=0.7870
Fold 1 | Epoch  45/150
[Train] Acc=0.9560  P=0.8905  R=0.9833  F1=0.9309
[Val  ] Acc=0.8514  P=0.8450  R=0.7871  F1=0.7951
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  50/150
[Train] Acc=0.9727  P=0.9331  R=0.9898  F1=0.9592
[Val  ] Acc=0.8649  P=0.7696  R=0.7911  F1=0.7773
Fold 1 | Epoch  55/150
[Train] Acc=0.9742  P=0.9252  R=0.9887  F1=0.9546
[Val  ] Acc=0.8649  P=0.8030  R=0.7911  F1=0.7707
Fold 1 | Epoch  60/150
[Train] Acc=0.9833  P=0.9561  R=0.9951  F1=0.9746
[Val  ] Acc=0.9189  P=0.9456  R=0.8071  F1=0.8443
⏹️  Early stopping tại epoch 64 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8587  P=0.8371  R=0.8200  F1=0.8057
✅ Best val F1: 0.8568
✅ Test F1:     0.8057

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9469    0.8560    0.8992       125
          GS     0.6000    0.8182    0.6923        22
         MSI     0.7812    0.9259    0.8475        27
      HM-SNV     1.0000    0.5000    0.6667         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8587       184
   macro avg     0.8371    0.8200    0.8057       184
weighted avg     0.8793    0.8587    0.8626       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.3879  std=0.0679  min=0.3122  max=0.5126
   meth : mean=0.2986  std=0.0400  min=0.2270  max=0.3444
   mirna: mean=0.3135  std=0.0279  min=0.2604  max=0.3434

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
[Train] Acc=0.5387  P=0.4380  R=0.6852  F1=0.4637
[Val  ] Acc=0.4189  P=0.4510  R=0.5983  F1=0.4176
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.6920  P=0.5535  R=0.8234  F1=0.6080
[Val  ] Acc=0.7432  P=0.5042  R=0.6307  F1=0.5391
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.7693  P=0.6855  R=0.8883  F1=0.7332
[Val  ] Acc=0.8243  P=0.6863  R=0.7690  F1=0.7202
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.8558  P=0.7514  R=0.9052  F1=0.8015
[Val  ] Acc=0.8243  P=0.6545  R=0.7872  F1=0.7024
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.9211  P=0.8497  R=0.9661  F1=0.8993
[Val  ] Acc=0.8243  P=0.7754  R=0.7690  F1=0.7472
Fold 2 | Epoch  40/150
[Train] Acc=0.9378  P=0.8918  R=0.9731  F1=0.9270
[Val  ] Acc=0.8514  P=0.7042  R=0.7770  F1=0.7335
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  45/150
[Train] Acc=0.9514  P=0.8877  R=0.9771  F1=0.9271
[Val  ] Acc=0.8649  P=0.8047  R=0.7810  F1=0.7691
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  50/150
[Train] Acc=0.9712  P=0.9418  R=0.9894  F1=0.9637
[Val  ] Acc=0.8649  P=0.8143  R=0.7810  F1=0.7743
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  55/150
[Train] Acc=0.9863  P=0.9567  R=0.9960  F1=0.9750
[Val  ] Acc=0.8649  P=0.7847  R=0.7810  F1=0.7495
Fold 2 | Epoch  60/150
[Train] Acc=0.9863  P=0.9502  R=0.9960  F1=0.9717
[Val  ] Acc=0.8649  P=0.7847  R=0.7810  F1=0.7495
Fold 2 | Epoch  65/150
[Train] Acc=0.9894  P=0.9849  R=0.9947  F1=0.9896
[Val  ] Acc=0.8784  P=0.8211  R=0.7992  F1=0.7864
⏹️  Early stopping tại epoch 68 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.8913  P=0.7312  R=0.7962  F1=0.7448
✅ Best val F1: 0.8244
✅ Test F1:     0.7448

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9912    0.8960    0.9412       125
          GS     0.7407    0.9091    0.8163        22
         MSI     0.7576    0.9259    0.8333        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     0.6667    1.0000    0.8000         6

    accuracy                         0.8913       184
   macro avg     0.7312    0.7962    0.7448       184
weighted avg     0.9057    0.8913    0.8926       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.3562  std=0.0386  min=0.3105  max=0.4276
   meth : mean=0.3201  std=0.0240  min=0.2767  max=0.3486
   mirna: mean=0.3238  std=0.0147  min=0.2957  max=0.3409

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
[Val  ] Acc=0.4730  P=0.4799  R=0.7691  F1=0.4748
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.7227  P=0.5995  R=0.7837  F1=0.6410
[Val  ] Acc=0.7162  P=0.5739  R=0.7592  F1=0.6119
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.8121  P=0.7096  R=0.9017  F1=0.7641
[Val  ] Acc=0.7568  P=0.5828  R=0.7712  F1=0.6342
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.8485  P=0.7723  R=0.9346  F1=0.8288
[Val  ] Acc=0.7568  P=0.5944  R=0.8036  F1=0.6526
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9182  P=0.8605  R=0.9632  F1=0.9032
[Val  ] Acc=0.8243  P=0.6404  R=0.8236  F1=0.7022
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  40/150
[Train] Acc=0.9409  P=0.8850  R=0.9763  F1=0.9248
[Val  ] Acc=0.8108  P=0.6674  R=0.8338  F1=0.7165
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  45/150
[Train] Acc=0.9576  P=0.9290  R=0.9833  F1=0.9530
[Val  ] Acc=0.7703  P=0.6373  R=0.8218  F1=0.6895
Fold 3 | Epoch  50/150
[Train] Acc=0.9727  P=0.9625  R=0.9920  F1=0.9752
[Val  ] Acc=0.7973  P=0.6567  R=0.8116  F1=0.7041
Fold 3 | Epoch  55/150
[Train] Acc=0.9833  P=0.9683  R=0.9930  F1=0.9801
[Val  ] Acc=0.8108  P=0.6584  R=0.8156  F1=0.7106
⏹️  Early stopping tại epoch 58 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8306  P=0.6582  R=0.7379  F1=0.6922
✅ Best val F1: 0.7777
✅ Test F1:     0.6922

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9145    0.8560    0.8843       125
          GS     0.4800    0.5714    0.5217        21
         MSI     0.8966    0.9286    0.9123        28
      HM-SNV     0.2500    0.3333    0.2857         3
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.8306       183
   macro avg     0.6582    0.7379    0.6922       183
weighted avg     0.8456    0.8306    0.8363       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.3659  std=0.0924  min=0.2801  max=0.5481
   meth : mean=0.3098  std=0.0576  min=0.2007  max=0.3646
   mirna: mean=0.3243  std=0.0349  min=0.2512  max=0.3553

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
[Train] Acc=0.1697  P=0.2068  R=0.2000  F1=0.1205
[Val  ] Acc=0.1081  P=0.0386  R=0.2273  F1=0.0652
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.3636  P=0.2869  R=0.3647  F1=0.2429
[Val  ] Acc=0.3784  P=0.2468  R=0.3215  F1=0.2314
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.3879  P=0.3082  R=0.4714  F1=0.2899
[Val  ] Acc=0.4730  P=0.3178  R=0.4576  F1=0.3112
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.5773  P=0.4509  R=0.6959  F1=0.4878
[Val  ] Acc=0.6081  P=0.3734  R=0.5259  F1=0.4092
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.7030  P=0.5866  R=0.7984  F1=0.6483
[Val  ] Acc=0.7703  P=0.4960  R=0.6570  F1=0.5402
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.8045  P=0.7167  R=0.8778  F1=0.7766
[Val  ] Acc=0.8378  P=0.5970  R=0.6689  F1=0.6177
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.8530  P=0.7836  R=0.9238  F1=0.8327
[Val  ] Acc=0.8378  P=0.5967  R=0.6770  F1=0.6299
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.8848  P=0.8039  R=0.9428  F1=0.8585
[Val  ] Acc=0.8649  P=0.6113  R=0.7133  F1=0.6530
Fold 4 | Epoch  40/150
[Train] Acc=0.9364  P=0.8784  R=0.9733  F1=0.9199
[Val  ] Acc=0.8514  P=0.6110  R=0.7093  F1=0.6508
Fold 4 | Epoch  45/150
[Train] Acc=0.9485  P=0.9003  R=0.9806  F1=0.9360
[Val  ] Acc=0.8514  P=0.6110  R=0.7093  F1=0.6508
⏹️  Early stopping tại epoch 46 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.7978  P=0.6932  R=0.7739  F1=0.7160
✅ Best val F1: 0.6744
✅ Test F1:     0.7160

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9400    0.7520    0.8356       125
          GS     0.4634    0.9048    0.6129        21
         MSI     0.8125    0.9630    0.8814        27
      HM-SNV     0.2500    0.2500    0.2500         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.7978       183
   macro avg     0.6932    0.7739    0.7160       183
weighted avg     0.8534    0.7978    0.8094       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.3799  std=0.0475  min=0.3151  max=0.4660
   meth : mean=0.3161  std=0.0485  min=0.2349  max=0.3826
   mirna: mean=0.3040  std=0.0049  min=0.2941  max=0.3149

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
[Train] Acc=0.1667  P=0.2064  R=0.1923  F1=0.1066
[Val  ] Acc=0.0946  P=0.1931  R=0.2564  F1=0.0753
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.3409  P=0.2877  R=0.3459  F1=0.2095
[Val  ] Acc=0.3108  P=0.1763  R=0.3022  F1=0.1481
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.4364  P=0.3489  R=0.4993  F1=0.3286
[Val  ] Acc=0.2973  P=0.3006  R=0.4096  F1=0.2726
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.5530  P=0.4856  R=0.6514  F1=0.4979
[Val  ] Acc=0.7027  P=0.4841  R=0.6370  F1=0.5283
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.6985  P=0.5781  R=0.7934  F1=0.6274
[Val  ] Acc=0.6757  P=0.5495  R=0.6512  F1=0.5624
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.8348  P=0.7034  R=0.9082  F1=0.7740
[Val  ] Acc=0.7297  P=0.5337  R=0.6632  F1=0.5648
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  30/150
[Train] Acc=0.8864  P=0.8007  R=0.9554  F1=0.8601
[Val  ] Acc=0.8243  P=0.5998  R=0.6872  F1=0.6356
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  35/150
[Train] Acc=0.9212  P=0.9019  R=0.9747  F1=0.9309
[Val  ] Acc=0.8243  P=0.7822  R=0.8014  F1=0.7515
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  40/150
[Train] Acc=0.9515  P=0.9199  R=0.9820  F1=0.9477
[Val  ] Acc=0.7973  P=0.7396  R=0.7752  F1=0.7121
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  45/150
[Train] Acc=0.9697  P=0.9363  R=0.9803  F1=0.9564
[Val  ] Acc=0.8514  P=0.7903  R=0.8094  F1=0.7554
Fold 5 | Epoch  50/150
[Train] Acc=0.9652  P=0.9228  R=0.9898  F1=0.9539
[Val  ] Acc=0.8378  P=0.5864  R=0.7094  F1=0.6203
Fold 5 | Epoch  55/150
[Train] Acc=0.9697  P=0.9283  R=0.9911  F1=0.9576
[Val  ] Acc=0.8378  P=0.5903  R=0.7094  F1=0.6221
⏹️  Early stopping tại epoch 58 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8525  P=0.7546  R=0.7232  F1=0.7297
✅ Best val F1: 0.7863
✅ Test F1:     0.7297

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9106    0.9032    0.9069       124
          GS     0.5238    0.5000    0.5116        22
         MSI     0.8387    0.9630    0.8966        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8525       183
   macro avg     0.7546    0.7232    0.7297       183
weighted avg     0.8474    0.8525    0.8484       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.4065  std=0.1138  min=0.2941  max=0.6207
   meth : mean=0.2823  std=0.0792  min=0.1432  max=0.3658
   mirna: mean=0.3112  std=0.0350  min=0.2361  max=0.3404

📈 5-fold CV summary
  ACCURACY : mean=0.8462  std=0.0310
  PRECISION: mean=0.7349  std=0.0608
  RECALL   : mean=0.7703  std=0.0358
  F1       : mean=0.7377  std=0.0382


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

         CIN     0.8603    0.9360    0.8966       125
          GS     0.7692    0.4545    0.5714        22
         MSI     0.8182    0.6667    0.7347        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     0.6000    1.0000    0.7500         6

    accuracy                         0.8315       184
   macro avg     0.7429    0.7114    0.7048       184
weighted avg     0.8305    0.8315    0.8221       184

[Test] Acc=0.8315  P=0.7429  R=0.7114  F1=0.7048

🔍 Patient Modality Gate Statistics (N=184)
   Gene expression     : mean=0.3827  std=0.0638
   DNA methylation     : mean=0.3016  std=0.0378
   miRNA               : mean=0.3157  std=0.0260

✔️  Accuracy: 0.8315
   Correct: 153 / 184