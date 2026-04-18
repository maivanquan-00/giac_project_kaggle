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
[Train] Acc=0.1897  P=0.3063  R=0.3455  F1=0.1974
[Val  ] Acc=0.1892  P=0.2854  R=0.4554  F1=0.2090
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.3338  P=0.3435  R=0.4884  F1=0.2935
[Val  ] Acc=0.3919  P=0.3767  R=0.5903  F1=0.3721
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.5068  P=0.4366  R=0.6448  F1=0.4427
[Val  ] Acc=0.4865  P=0.5344  R=0.5507  F1=0.4630
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.7132  P=0.5680  R=0.8116  F1=0.6217
[Val  ] Acc=0.6892  P=0.6130  R=0.7209  F1=0.6414
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.8361  P=0.7033  R=0.9069  F1=0.7657
[Val  ] Acc=0.7703  P=0.7078  R=0.7449  F1=0.7206
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.8862  P=0.7954  R=0.9473  F1=0.8492
[Val  ] Acc=0.7973  P=0.6086  R=0.6569  F1=0.6292
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.9287  P=0.8588  R=0.9726  F1=0.9054
[Val  ] Acc=0.8514  P=0.8444  R=0.7871  F1=0.7960
Fold 1 | Epoch  40/150
[Train] Acc=0.9423  P=0.8835  R=0.9788  F1=0.9238
[Val  ] Acc=0.8378  P=0.8228  R=0.7649  F1=0.7729
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  45/150
[Train] Acc=0.9621  P=0.9105  R=0.9873  F1=0.9443
[Val  ] Acc=0.8514  P=0.8450  R=0.7871  F1=0.7951
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  50/150
[Train] Acc=0.9712  P=0.9162  R=0.9894  F1=0.9494
[Val  ] Acc=0.8514  P=0.8450  R=0.7871  F1=0.7951
Fold 1 | Epoch  55/150
[Train] Acc=0.9757  P=0.9243  R=0.9929  F1=0.9560
[Val  ] Acc=0.8784  P=0.7878  R=0.7951  F1=0.7869
⏹️  Early stopping tại epoch 58 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8424  P=0.8093  R=0.8019  F1=0.7814
✅ Best val F1: 0.8328
✅ Test F1:     0.7814

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9298    0.8480    0.8870       125
          GS     0.5667    0.7727    0.6538        22
         MSI     0.8000    0.8889    0.8421        27
      HM-SNV     1.0000    0.5000    0.6667         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.8424       184
   macro avg     0.8093    0.8019    0.7814       184
weighted avg     0.8630    0.8424    0.8468       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.3884  std=0.0768  min=0.3027  max=0.5356
   meth : mean=0.2974  std=0.0463  min=0.2115  max=0.3508
   mirna: mean=0.3142  std=0.0305  min=0.2530  max=0.3465

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
[Train] Acc=0.1608  P=0.1983  R=0.1770  F1=0.1213
[Val  ] Acc=0.1486  P=0.2777  R=0.2866  F1=0.1678
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.2079  P=0.2579  R=0.3667  F1=0.1889
[Val  ] Acc=0.1081  P=0.1482  R=0.3253  F1=0.1310
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.3642  P=0.3423  R=0.5054  F1=0.3239
[Val  ] Acc=0.2432  P=0.3437  R=0.4896  F1=0.2558
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.4977  P=0.4494  R=0.6600  F1=0.4539
[Val  ] Acc=0.4324  P=0.4772  R=0.5570  F1=0.4475
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.5994  P=0.5401  R=0.7662  F1=0.5672
[Val  ] Acc=0.6622  P=0.5206  R=0.6290  F1=0.5400
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.8058  P=0.6828  R=0.8734  F1=0.7326
[Val  ] Acc=0.7703  P=0.5904  R=0.6752  F1=0.6205
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.8938  P=0.7768  R=0.9624  F1=0.8348
[Val  ] Acc=0.8243  P=0.6667  R=0.7872  F1=0.7083
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.9241  P=0.8338  R=0.9713  F1=0.8863
[Val  ] Acc=0.8378  P=0.6739  R=0.7912  F1=0.7168
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  40/150
[Train] Acc=0.9454  P=0.8513  R=0.9818  F1=0.9036
[Val  ] Acc=0.8514  P=0.6822  R=0.7952  F1=0.7203
Fold 2 | Epoch  45/150
[Train] Acc=0.9605  P=0.9020  R=0.9863  F1=0.9375
[Val  ] Acc=0.8649  P=0.8143  R=0.7810  F1=0.7743
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  50/150
[Train] Acc=0.9727  P=0.9410  R=0.9877  F1=0.9624
[Val  ] Acc=0.8649  P=0.7245  R=0.7992  F1=0.7547
Fold 2 | Epoch  55/150
[Train] Acc=0.9909  P=0.9791  R=0.9973  F1=0.9879
[Val  ] Acc=0.8784  P=0.7286  R=0.8032  F1=0.7588
⏹️  Early stopping tại epoch 57 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.8750  P=0.7094  R=0.7764  F1=0.7219
✅ Best val F1: 0.7876
✅ Test F1:     0.7219

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9737    0.8880    0.9289       125
          GS     0.6923    0.8182    0.7500        22
         MSI     0.7812    0.9259    0.8475        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     0.6000    1.0000    0.7500         6

    accuracy                         0.8750       184
   macro avg     0.7094    0.7764    0.7219       184
weighted avg     0.8893    0.8750    0.8768       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.3620  std=0.0650  min=0.2929  max=0.4855
   meth : mean=0.3106  std=0.0423  min=0.2325  max=0.3575
   mirna: mean=0.3274  std=0.0227  min=0.2820  max=0.3499

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
[Train] Acc=0.2318  P=0.2066  R=0.1706  F1=0.1409
[Val  ] Acc=0.2568  P=0.2308  R=0.1895  F1=0.1563
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.3803  P=0.2824  R=0.3315  F1=0.2400
[Val  ] Acc=0.3784  P=0.1754  R=0.3040  F1=0.1511
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.4258  P=0.3301  R=0.4738  F1=0.3104
[Val  ] Acc=0.4595  P=0.4260  R=0.4900  F1=0.3723
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.5364  P=0.4381  R=0.6455  F1=0.4553
[Val  ] Acc=0.6081  P=0.5192  R=0.8273  F1=0.5371
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.7106  P=0.5840  R=0.8261  F1=0.6369
[Val  ] Acc=0.7027  P=0.6513  R=0.7876  F1=0.6712
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.8379  P=0.7169  R=0.9108  F1=0.7786
[Val  ] Acc=0.7568  P=0.6178  R=0.8036  F1=0.6698
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.9000  P=0.8131  R=0.9418  F1=0.8647
[Val  ] Acc=0.8243  P=0.7819  R=0.8378  F1=0.7713
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9348  P=0.8603  R=0.9750  F1=0.9075
[Val  ] Acc=0.7973  P=0.6545  R=0.8298  F1=0.7066
Fold 3 | Epoch  40/150
[Train] Acc=0.9621  P=0.9404  R=0.9846  F1=0.9601
[Val  ] Acc=0.8514  P=0.7777  R=0.8458  F1=0.7681
⏹️  Early stopping tại epoch 40 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8142  P=0.6556  R=0.7030  F1=0.6735
✅ Best val F1: 0.7713
✅ Test F1:     0.6735

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9008    0.8720    0.8862       125
          GS     0.4400    0.5238    0.4783        21
         MSI     0.8800    0.7857    0.8302        28
      HM-SNV     0.2000    0.3333    0.2500         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8142       183
   macro avg     0.6556    0.7030    0.6735       183
weighted avg     0.8318    0.8142    0.8216       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.3398  std=0.0533  min=0.2365  max=0.4691
   meth : mean=0.3145  std=0.0583  min=0.1912  max=0.3852
   mirna: mean=0.3457  std=0.0671  min=0.2519  max=0.5176

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
[Train] Acc=0.2015  P=0.1858  R=0.1692  F1=0.1296
[Val  ] Acc=0.3514  P=0.1602  R=0.1182  F1=0.1322
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.3348  P=0.2791  R=0.3492  F1=0.2436
[Val  ] Acc=0.2703  P=0.2665  R=0.2198  F1=0.2033
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.3545  P=0.3279  R=0.4954  F1=0.2907
[Val  ] Acc=0.4054  P=0.3115  R=0.4194  F1=0.2883
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.5652  P=0.4302  R=0.6498  F1=0.4588
[Val  ] Acc=0.5405  P=0.3338  R=0.4322  F1=0.3424
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.7061  P=0.5626  R=0.8009  F1=0.6264
[Val  ] Acc=0.7568  P=0.4925  R=0.6489  F1=0.5327
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.8000  P=0.6792  R=0.8939  F1=0.7452
[Val  ] Acc=0.8108  P=0.5498  R=0.6832  F1=0.5893
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.8909  P=0.8024  R=0.9343  F1=0.8519
[Val  ] Acc=0.8514  P=0.6071  R=0.7093  F1=0.6489
Fold 4 | Epoch  35/150
[Train] Acc=0.9318  P=0.8697  R=0.9694  F1=0.9132
[Val  ] Acc=0.8243  P=0.6105  R=0.7013  F1=0.6462
⏹️  Early stopping tại epoch 39 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.7486  P=0.6265  R=0.7516  F1=0.6644
✅ Best val F1: 0.7003
✅ Test F1:     0.6644

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9348    0.6880    0.7926       125
          GS     0.4091    0.8571    0.5538        21
         MSI     0.7647    0.9630    0.8525        27
      HM-SNV     0.1667    0.2500    0.2000         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.7486       183
   macro avg     0.6265    0.7516    0.6644       183
weighted avg     0.8300    0.7486    0.7654       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.3265  std=0.0214  min=0.2923  max=0.3657
   meth : mean=0.3278  std=0.0444  min=0.2460  max=0.4015
   mirna: mean=0.3457  std=0.0254  min=0.3025  max=0.3943

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
[Train] Acc=0.1470  P=0.1910  R=0.2054  F1=0.1014
[Val  ] Acc=0.0541  P=0.0518  R=0.3040  F1=0.0419
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.2773  P=0.2703  R=0.3019  F1=0.1910
[Val  ] Acc=0.2297  P=0.1700  R=0.3560  F1=0.1231
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.5091  P=0.3724  R=0.5451  F1=0.3739
[Val  ] Acc=0.5135  P=0.3234  R=0.4554  F1=0.3327
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.5424  P=0.4338  R=0.6721  F1=0.4562
[Val  ] Acc=0.4730  P=0.4571  R=0.6872  F1=0.4446
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.7015  P=0.5674  R=0.7884  F1=0.6179
[Val  ] Acc=0.6622  P=0.5408  R=0.6432  F1=0.5629
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.8106  P=0.6721  R=0.8931  F1=0.7368
[Val  ] Acc=0.7703  P=0.7734  R=0.7854  F1=0.7415
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  30/150
[Train] Acc=0.8697  P=0.7560  R=0.8885  F1=0.8054
[Val  ] Acc=0.7568  P=0.5736  R=0.6672  F1=0.6079
Fold 5 | Epoch  35/150
[Train] Acc=0.9152  P=0.8495  R=0.9649  F1=0.8967
[Val  ] Acc=0.8243  P=0.8044  R=0.7832  F1=0.7661
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  40/150
[Train] Acc=0.9515  P=0.8918  R=0.9836  F1=0.9313
[Val  ] Acc=0.7838  P=0.7436  R=0.7347  F1=0.7045
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  45/150
[Train] Acc=0.9682  P=0.9436  R=0.9907  F1=0.9649
[Val  ] Acc=0.8649  P=0.7231  R=0.8134  F1=0.7585
Fold 5 | Epoch  50/150
[Train] Acc=0.9667  P=0.9311  R=0.9902  F1=0.9579
[Val  ] Acc=0.8649  P=0.8333  R=0.8134  F1=0.7967
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  55/150
[Train] Acc=0.9758  P=0.9243  R=0.9929  F1=0.9561
[Val  ] Acc=0.8378  P=0.8064  R=0.7507  F1=0.7544
Fold 5 | Epoch  60/150
[Train] Acc=0.9576  P=0.9125  R=0.9860  F1=0.9441
[Val  ] Acc=0.8784  P=0.8471  R=0.7992  F1=0.7993
⏹️  Early stopping tại epoch 62 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8306  P=0.7096  R=0.7243  F1=0.7140
✅ Best val F1: 0.8199
✅ Test F1:     0.7140

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9145    0.8629    0.8880       124
          GS     0.4615    0.5455    0.5000        22
         MSI     0.8387    0.9630    0.8966        27
      HM-SNV     0.3333    0.2500    0.2857         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8306       183
   macro avg     0.7096    0.7243    0.7140       183
weighted avg     0.8390    0.8306    0.8331       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.4024  std=0.0632  min=0.3308  max=0.5319
   meth : mean=0.3100  std=0.0484  min=0.2147  max=0.3671
   mirna: mean=0.2877  std=0.0148  min=0.2534  max=0.3021

📈 5-fold CV summary
  ACCURACY : mean=0.8222  std=0.0418
  PRECISION: mean=0.7021  std=0.0624
  RECALL   : mean=0.7514  std=0.0354
  F1       : mean=0.7111  std=0.0416


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

         CIN     0.8516    0.8720    0.8617       125
          GS     0.5000    0.5000    0.5000        22
         MSI     0.8000    0.5926    0.6809        27
      HM-SNV     0.6000    0.7500    0.6667         4
         EBV     0.5556    0.8333    0.6667         6

    accuracy                         0.7826       184
   macro avg     0.6614    0.7096    0.6752       184
weighted avg     0.7868    0.7826    0.7813       184

[Test] Acc=0.7826  P=0.6614  R=0.7096  F1=0.6752

🔍 Patient Modality Gate Statistics (N=184)
   Gene expression     : mean=0.3822  std=0.0707
   DNA methylation     : mean=0.3010  std=0.0430
   miRNA               : mean=0.3168  std=0.0277

✔️  Accuracy: 0.7826
   Correct: 144 / 184