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
[Train] Acc=0.0865  P=0.1430  R=0.1384  F1=0.0691
[Val  ] Acc=0.0946  P=0.1023  R=0.4120  F1=0.0714
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.2124  P=0.2894  R=0.3488  F1=0.1828
[Val  ] Acc=0.1486  P=0.3017  R=0.4604  F1=0.1401
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.3187  P=0.3337  R=0.4440  F1=0.2762
[Val  ] Acc=0.4324  P=0.3830  R=0.5882  F1=0.3928
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.4901  P=0.4254  R=0.6233  F1=0.4258
[Val  ] Acc=0.4865  P=0.5665  R=0.6690  F1=0.5413
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.7147  P=0.5841  R=0.7906  F1=0.6342
[Val  ] Acc=0.6486  P=0.6047  R=0.7312  F1=0.6250
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.7936  P=0.6892  R=0.9035  F1=0.7468
[Val  ] Acc=0.7297  P=0.7022  R=0.7369  F1=0.7080
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.8467  P=0.7622  R=0.9126  F1=0.8134
[Val  ] Acc=0.7703  P=0.6102  R=0.6712  F1=0.6304
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.9029  P=0.8264  R=0.9629  F1=0.8803
[Val  ] Acc=0.8784  P=0.8780  R=0.8133  F1=0.8263
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  40/150
[Train] Acc=0.9226  P=0.8578  R=0.9692  F1=0.9030
[Val  ] Acc=0.8514  P=0.8532  R=0.8053  F1=0.8085
Fold 1 | Epoch  45/150
[Train] Acc=0.9560  P=0.9325  R=0.9790  F1=0.9533
[Val  ] Acc=0.8243  P=0.8358  R=0.7973  F1=0.7929
Fold 1 | Epoch  50/150
[Train] Acc=0.9545  P=0.9149  R=0.9748  F1=0.9416
[Val  ] Acc=0.8919  P=0.6748  R=0.7213  F1=0.6821
⏹️  Early stopping tại epoch 50 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.7663  P=0.6038  R=0.6929  F1=0.6389
✅ Best val F1: 0.8263
✅ Test F1:     0.6389

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9000    0.7920    0.8426       125
          GS     0.4545    0.6818    0.5455        22
         MSI     0.7143    0.7407    0.7273        27
      HM-SNV     0.2000    0.2500    0.2222         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.7663       184
   macro avg     0.6038    0.6929    0.6389       184
weighted avg     0.7994    0.7663    0.7771       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.5036  std=0.4198  min=0.0001  max=0.9995
   meth : mean=0.3263  std=0.3857  min=0.0000  max=0.9998
   mirna: mean=0.1701  std=0.2510  min=0.0000  max=0.9556

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
[Train] Acc=0.4734  P=0.2551  R=0.2897  F1=0.2443
[Val  ] Acc=0.6216  P=0.2324  R=0.3116  F1=0.2446
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.3869  P=0.2566  R=0.3173  F1=0.2353
[Val  ] Acc=0.5135  P=0.3610  R=0.4514  F1=0.3182
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.4143  P=0.3331  R=0.4814  F1=0.3216
[Val  ] Acc=0.4595  P=0.3115  R=0.4293  F1=0.2718
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.4932  P=0.3955  R=0.5991  F1=0.4070
[Val  ] Acc=0.5541  P=0.3783  R=0.4220  F1=0.3606
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.6161  P=0.5150  R=0.7424  F1=0.5617
[Val  ] Acc=0.5541  P=0.4653  R=0.5686  F1=0.4546
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.7466  P=0.6253  R=0.8218  F1=0.6719
[Val  ] Acc=0.6892  P=0.4989  R=0.6370  F1=0.5214
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.8543  P=0.7426  R=0.9150  F1=0.7969
[Val  ] Acc=0.7973  P=0.5400  R=0.6690  F1=0.5792
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.8983  P=0.7892  R=0.9519  F1=0.8468
[Val  ] Acc=0.7973  P=0.5467  R=0.6690  F1=0.5843
Fold 2 | Epoch  40/150
[Train] Acc=0.9378  P=0.8659  R=0.9737  F1=0.9108
[Val  ] Acc=0.8378  P=0.5642  R=0.6810  F1=0.6027
Fold 2 | Epoch  45/150
[Train] Acc=0.9484  P=0.8651  R=0.9587  F1=0.9050
[Val  ] Acc=0.8378  P=0.5730  R=0.6810  F1=0.6098
⏹️  Early stopping tại epoch 48 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.7609  P=0.5418  R=0.6671  F1=0.5771
✅ Best val F1: 0.6263
✅ Test F1:     0.5771

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9608    0.7840    0.8634       125
          GS     0.5000    0.7273    0.5926        22
         MSI     0.7407    0.7407    0.7407        27
      HM-SNV     0.0909    0.2500    0.1333         4
         EBV     0.4167    0.8333    0.5556         6

    accuracy                         0.7609       184
   macro avg     0.5418    0.6671    0.5771       184
weighted avg     0.8367    0.7609    0.7871       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.1911  std=0.2559  min=0.0001  max=0.9643
   meth : mean=0.4627  std=0.3699  min=0.0002  max=0.9907
   mirna: mean=0.3462  std=0.3581  min=0.0038  max=0.9997

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
[Train] Acc=0.0833  P=0.1951  R=0.2824  F1=0.0826
[Val  ] Acc=0.0541  P=0.0850  R=0.1545  F1=0.0813
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.1455  P=0.2288  R=0.3128  F1=0.1192
[Val  ] Acc=0.0270  P=0.0154  R=0.2000  F1=0.0286
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.3439  P=0.3142  R=0.4313  F1=0.2683
[Val  ] Acc=0.5135  P=0.4360  R=0.5554  F1=0.3778
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.5182  P=0.4460  R=0.6636  F1=0.4487
[Val  ] Acc=0.5270  P=0.4782  R=0.7162  F1=0.4816
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.7030  P=0.5847  R=0.8057  F1=0.6399
[Val  ] Acc=0.7432  P=0.5607  R=0.7490  F1=0.6181
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.8439  P=0.7281  R=0.9185  F1=0.7930
[Val  ] Acc=0.8108  P=0.6767  R=0.8792  F1=0.7429
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.8803  P=0.7488  R=0.9173  F1=0.8113
[Val  ] Acc=0.7838  P=0.6376  R=0.8116  F1=0.6874
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9212  P=0.8380  R=0.9316  F1=0.8772
[Val  ] Acc=0.8378  P=0.7612  R=0.8094  F1=0.7757
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  40/150
[Train] Acc=0.9379  P=0.8612  R=0.9546  F1=0.9001
[Val  ] Acc=0.8378  P=0.6636  R=0.8418  F1=0.7210
Fold 3 | Epoch  45/150
[Train] Acc=0.9455  P=0.9030  R=0.9797  F1=0.9362
[Val  ] Acc=0.8108  P=0.7781  R=0.7872  F1=0.7451
Fold 3 | Epoch  50/150
[Train] Acc=0.9636  P=0.9530  R=0.9872  F1=0.9675
[Val  ] Acc=0.8378  P=0.7993  R=0.8054  F1=0.7756
⏹️  Early stopping tại epoch 50 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.7978  P=0.6635  R=0.6958  F1=0.6778
✅ Best val F1: 0.7757
✅ Test F1:     0.6778

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.8908    0.8480    0.8689       125
          GS     0.4348    0.4762    0.4545        21
         MSI     0.7419    0.8214    0.7797        28
      HM-SNV     0.2500    0.3333    0.2857         3
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.7978       183
   macro avg     0.6635    0.6958    0.6778       183
weighted avg     0.8087    0.7978    0.8024       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.3463  std=0.4020  min=0.0004  max=0.9997
   meth : mean=0.4575  std=0.3959  min=0.0000  max=0.9977
   mirna: mean=0.1962  std=0.2656  min=0.0001  max=0.9563

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
[Train] Acc=0.3182  P=0.1831  R=0.2398  F1=0.1393
[Val  ] Acc=0.4865  P=0.1744  R=0.3360  F1=0.1714
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.4606  P=0.3301  R=0.4177  F1=0.3024
[Val  ] Acc=0.4730  P=0.2725  R=0.3502  F1=0.2021
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.4167  P=0.3383  R=0.4469  F1=0.3079
[Val  ] Acc=0.5000  P=0.2502  R=0.4129  F1=0.2483
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.5576  P=0.4462  R=0.6574  F1=0.4764
[Val  ] Acc=0.5135  P=0.3096  R=0.4493  F1=0.2853
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.6712  P=0.5725  R=0.8040  F1=0.6271
[Val  ] Acc=0.6757  P=0.4379  R=0.5783  F1=0.4754
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.7939  P=0.6693  R=0.8521  F1=0.7343
[Val  ] Acc=0.7568  P=0.5076  R=0.6023  F1=0.5288
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.8621  P=0.7709  R=0.9143  F1=0.8260
[Val  ] Acc=0.8108  P=0.5455  R=0.6832  F1=0.5950
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.9061  P=0.8669  R=0.9581  F1=0.9020
[Val  ] Acc=0.8108  P=0.5867  R=0.6832  F1=0.6250
Fold 4 | Epoch  40/150
[Train] Acc=0.9030  P=0.8554  R=0.9673  F1=0.8959
[Val  ] Acc=0.8108  P=0.5903  R=0.6649  F1=0.6205
Fold 4 | Epoch  45/150
[Train] Acc=0.9561  P=0.9138  R=0.9700  F1=0.9387
[Val  ] Acc=0.8243  P=0.5918  R=0.6689  F1=0.6221
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  50/150
[Train] Acc=0.9742  P=0.9526  R=0.9908  F1=0.9703
[Val  ] Acc=0.8378  P=0.5777  R=0.6871  F1=0.6227
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  55/150
[Train] Acc=0.9712  P=0.9553  R=0.9873  F1=0.9702
[Val  ] Acc=0.8514  P=0.5962  R=0.6769  F1=0.6283
Fold 4 | Epoch  60/150
[Train] Acc=0.9758  P=0.9017  R=0.9929  F1=0.9364
[Val  ] Acc=0.8514  P=0.6291  R=0.6911  F1=0.6502
Fold 4 | Epoch  65/150
[Train] Acc=0.9879  P=0.9814  R=0.9964  F1=0.9884
[Val  ] Acc=0.8649  P=0.6294  R=0.6951  F1=0.6523
⏹️  Early stopping tại epoch 68 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.8251  P=0.6453  R=0.6939  F1=0.6656
✅ Best val F1: 0.6523
✅ Test F1:     0.6656

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9052    0.8400    0.8714       125
          GS     0.4828    0.6667    0.5600        21
         MSI     0.8387    0.9630    0.8966        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8251       183
   macro avg     0.6453    0.6939    0.6656       183
weighted avg     0.8302    0.8251    0.8245       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.4341  std=0.3892  min=0.0010  max=0.9996
   meth : mean=0.4291  std=0.4282  min=0.0001  max=0.9977
   mirna: mean=0.1368  std=0.2487  min=0.0003  max=0.9443

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
[Train] Acc=0.2773  P=0.1780  R=0.1748  F1=0.1495
[Val  ] Acc=0.3378  P=0.2310  R=0.2863  F1=0.2010
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.5136  P=0.2859  R=0.3381  F1=0.2605
[Val  ] Acc=0.5135  P=0.4057  R=0.3270  F1=0.2812
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.4545  P=0.3465  R=0.4700  F1=0.3301
[Val  ] Acc=0.4189  P=0.3322  R=0.3861  F1=0.3166
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.5212  P=0.4067  R=0.6079  F1=0.4301
[Val  ] Acc=0.6486  P=0.4768  R=0.6481  F1=0.5228
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.7061  P=0.6032  R=0.7860  F1=0.6481
[Val  ] Acc=0.7432  P=0.5950  R=0.7814  F1=0.6520
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.8015  P=0.6935  R=0.9101  F1=0.7486
[Val  ] Acc=0.7027  P=0.6519  R=0.7694  F1=0.6730
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  30/150
[Train] Acc=0.8879  P=0.7817  R=0.9361  F1=0.8238
[Val  ] Acc=0.7568  P=0.6699  R=0.8036  F1=0.6991
Fold 5 | Epoch  35/150
[Train] Acc=0.9227  P=0.8340  R=0.9671  F1=0.8875
[Val  ] Acc=0.7838  P=0.5850  R=0.7298  F1=0.6317
Fold 5 | Epoch  40/150
[Train] Acc=0.9515  P=0.8689  R=0.9687  F1=0.9090
[Val  ] Acc=0.8108  P=0.6218  R=0.7196  F1=0.6540
⏹️  Early stopping tại epoch 41 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.7814  P=0.6525  R=0.7206  F1=0.6748
✅ Best val F1: 0.7187
✅ Test F1:     0.6748

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9327    0.7823    0.8509       124
          GS     0.4688    0.6818    0.5556        22
         MSI     0.7500    0.8889    0.8136        27
      HM-SNV     0.1111    0.2500    0.1538         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.7814       183
   macro avg     0.6525    0.7206    0.6748       183
weighted avg     0.8342    0.7814    0.7995       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.3894  std=0.3949  min=0.0030  max=0.9980
   meth : mean=0.4381  std=0.3808  min=0.0001  max=0.9864
   mirna: mean=0.1724  std=0.2369  min=0.0018  max=0.9387

📈 5-fold CV summary
  ACCURACY : mean=0.7863  std=0.0233
  PRECISION: mean=0.6214  std=0.0446
  RECALL   : mean=0.6941  std=0.0170
  F1       : mean=0.6468  std=0.0374

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

         CIN     0.8273    0.9200    0.8712       125
          GS     0.5500    0.5000    0.5238        22
         MSI     0.6429    0.3333    0.4390        27
      HM-SNV     0.4286    0.7500    0.5455         4
         EBV     0.2500    0.1667    0.2000         6

    accuracy                         0.7554       184
   macro avg     0.5398    0.5340    0.5159       184
weighted avg     0.7396    0.7554    0.7373       184

[Test] Acc=0.7554  P=0.5398  R=0.5340  F1=0.5159

🔍 Patient Modality Gate Statistics (N=184)
   Gene expression     : mean=0.4929  std=0.3705
   DNA methylation     : mean=0.3179  std=0.3570
   miRNA               : mean=0.1892  std=0.2570

✔️  Accuracy: 0.7554
   Correct: 139 / 184