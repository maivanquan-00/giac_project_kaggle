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
[Train] Acc=0.2777  P=0.2981  R=0.3689  F1=0.2344
[Val  ] Acc=0.4189  P=0.4995  R=0.5631  F1=0.4470
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.7269  P=0.6228  R=0.7774  F1=0.6672
[Val  ] Acc=0.7027  P=0.5600  R=0.6471  F1=0.5808
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.9287  P=0.9055  R=0.9710  F1=0.9325
[Val  ] Acc=0.8378  P=0.6405  R=0.6871  F1=0.6609
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.9484  P=0.9078  R=0.9682  F1=0.9356
[Val  ] Acc=0.8514  P=0.8562  R=0.8053  F1=0.8101
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 1 | Epoch  20/150
[Train] Acc=0.9818  P=0.9727  R=0.9925  F1=0.9820
[Val  ] Acc=0.8784  P=0.6782  R=0.7173  F1=0.6952
       fusion_alpha=0.255  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.9803  P=0.9748  R=0.9862  F1=0.9801
[Val  ] Acc=0.8243  P=0.6441  R=0.7013  F1=0.6674
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  30/150
[Train] Acc=0.9757  P=0.9704  R=0.9870  F1=0.9783
[Val  ] Acc=0.8378  P=0.6416  R=0.6871  F1=0.6562
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  35/150
[Train] Acc=0.9909  P=0.9875  R=0.9952  F1=0.9913
[Val  ] Acc=0.9054  P=0.7253  R=0.7253  F1=0.7216
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 36 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8696  P=0.8057  R=0.8041  F1=0.8010
✅ Best val F1: 0.8568
✅ Test F1:     0.8010

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9412    0.8960    0.9180       125
          GS     0.6538    0.7727    0.7083        22
         MSI     0.7667    0.8519    0.8070        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8696       184
   macro avg     0.8057    0.8041    0.8010       184
weighted avg     0.8772    0.8696    0.8718       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.3342  std=0.0002  min=0.3340  max=0.3344
   meth : mean=0.3768  std=0.0002  min=0.3765  max=0.3771
   mirna: mean=0.2890  std=0.0001  min=0.2889  max=0.2891

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
[Train] Acc=0.3748  P=0.2866  R=0.3387  F1=0.2518
[Val  ] Acc=0.6081  P=0.3956  R=0.5725  F1=0.4236
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.7193  P=0.5560  R=0.7160  F1=0.6073
[Val  ] Acc=0.7838  P=0.5087  R=0.6610  F1=0.5544
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.8725  P=0.7758  R=0.9400  F1=0.8243
[Val  ] Acc=0.8919  P=0.8324  R=0.8072  F1=0.7947
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.9530  P=0.9337  R=0.9690  F1=0.9499
[Val  ] Acc=0.8784  P=0.8213  R=0.7850  F1=0.7791
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.9833  P=0.9641  R=0.9929  F1=0.9778
[Val  ] Acc=0.8919  P=0.8349  R=0.7890  F1=0.7882
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
Fold 2 | Epoch  25/150
[Train] Acc=0.9863  P=0.9725  R=0.9960  F1=0.9837
[Val  ] Acc=0.9054  P=0.8614  R=0.7747  F1=0.7906
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.9954  P=0.9925  R=0.9987  F1=0.9955
[Val  ] Acc=0.8784  P=0.8313  R=0.7850  F1=0.7843
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.9636  P=0.9279  R=0.9797  F1=0.9521
[Val  ] Acc=0.8514  P=0.8066  R=0.7587  F1=0.7570
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  40/150
[Train] Acc=0.9560  P=0.8965  R=0.9737  F1=0.9301
[Val  ] Acc=0.8514  P=0.6558  R=0.6627  F1=0.6585
       fusion_alpha=0.249  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  45/150
[Train] Acc=0.9909  P=0.9858  R=0.9973  F1=0.9914
[Val  ] Acc=0.8919  P=0.8983  R=0.7890  F1=0.8264
       fusion_alpha=0.248  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  50/150
[Train] Acc=0.9939  P=0.9801  R=0.9961  F1=0.9878
[Val  ] Acc=0.8784  P=0.8310  R=0.7850  F1=0.7842
       fusion_alpha=0.248  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  55/150
[Train] Acc=0.9924  P=0.9796  R=0.9935  F1=0.9863
[Val  ] Acc=0.8243  P=0.5898  R=0.6547  F1=0.6149
       fusion_alpha=0.247  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 59 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.9076  P=0.8493  R=0.7860  F1=0.7653
✅ Best val F1: 0.8466
✅ Test F1:     0.7653

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9669    0.9360    0.9512       125
          GS     0.7200    0.8182    0.7660        22
         MSI     0.8929    0.9259    0.9091        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     0.6667    1.0000    0.8000         6

    accuracy                         0.9076       184
   macro avg     0.8493    0.7860    0.7653       184
weighted avg     0.9175    0.9076    0.9060       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.3124  std=0.0000  min=0.3124  max=0.3124
   meth : mean=0.3153  std=0.0000  min=0.3153  max=0.3153
   mirna: mean=0.3723  std=0.0000  min=0.3723  max=0.3723

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
[Train] Acc=0.5106  P=0.2639  R=0.2620  F1=0.2562
[Val  ] Acc=0.7162  P=0.4830  R=0.5620  F1=0.4783
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.7576  P=0.6658  R=0.7952  F1=0.7168
[Val  ] Acc=0.8243  P=0.7823  R=0.8236  F1=0.7672
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.9030  P=0.8589  R=0.9598  F1=0.8990
[Val  ] Acc=0.8243  P=0.7719  R=0.8236  F1=0.7819
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.9652  P=0.9174  R=0.9706  F1=0.9423
[Val  ] Acc=0.8919  P=0.8116  R=0.8578  F1=0.8288
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.9848  P=0.9802  R=0.9913  F1=0.9856
[Val  ] Acc=0.8784  P=0.7962  R=0.8356  F1=0.8106
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
Fold 3 | Epoch  25/150
[Train] Acc=0.9742  P=0.9651  R=0.9903  F1=0.9763
[Val  ] Acc=0.8514  P=0.7719  R=0.8276  F1=0.7918
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.9909  P=0.9749  R=0.9973  F1=0.9857
[Val  ] Acc=0.9459  P=0.9662  R=0.8556  F1=0.8937
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9879  P=0.9823  R=0.9964  F1=0.9892
[Val  ] Acc=0.8649  P=0.8831  R=0.8316  F1=0.8334
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  40/150
[Train] Acc=0.9939  P=0.9929  R=0.9961  F1=0.9945
[Val  ] Acc=0.9189  P=0.9235  R=0.8658  F1=0.8743
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  45/150
[Train] Acc=0.9939  P=0.9906  R=0.9982  F1=0.9943
[Val  ] Acc=0.9189  P=0.9298  R=0.8476  F1=0.8716
       fusion_alpha=0.249  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 45 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8689  P=0.6607  R=0.6523  F1=0.6510
✅ Best val F1: 0.8937
✅ Test F1:     0.6510

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.8750    0.9520    0.9119       125
          GS     0.5714    0.3810    0.4571        21
         MSI     1.0000    0.9286    0.9630        28
      HM-SNV     0.0000    0.0000    0.0000         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8689       183
   macro avg     0.6607    0.6523    0.6510       183
weighted avg     0.8444    0.8689    0.8529       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.3413  std=0.0000  min=0.3413  max=0.3413
   meth : mean=0.3482  std=0.0000  min=0.3482  max=0.3482
   mirna: mean=0.3105  std=0.0000  min=0.3105  max=0.3105

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
[Train] Acc=0.4061  P=0.3049  R=0.4103  F1=0.2766
[Val  ] Acc=0.6216  P=0.4478  R=0.5684  F1=0.4547
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.7803  P=0.6215  R=0.7704  F1=0.6780
[Val  ] Acc=0.8243  P=0.6468  R=0.6649  F1=0.6456
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.9288  P=0.8641  R=0.9519  F1=0.9018
[Val  ] Acc=0.8649  P=0.6741  R=0.7133  F1=0.6912
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.9652  P=0.9378  R=0.9669  F1=0.9511
[Val  ] Acc=0.9054  P=0.7269  R=0.7436  F1=0.7349
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.9864  P=0.9793  R=0.9960  F1=0.9871
[Val  ] Acc=0.9054  P=0.7418  R=0.7253  F1=0.7242
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  25/150
[Train] Acc=0.9848  P=0.9789  R=0.9924  F1=0.9851
[Val  ] Acc=0.9054  P=0.7201  R=0.7436  F1=0.7287
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  30/150
[Train] Acc=0.9682  P=0.9365  R=0.9848  F1=0.9594
[Val  ] Acc=0.9054  P=0.7128  R=0.7436  F1=0.7269
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 30 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.8306  P=0.7272  R=0.7164  F1=0.7134
✅ Best val F1: 0.7349
✅ Test F1:     0.7134

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9138    0.8480    0.8797       125
          GS     0.5000    0.7619    0.6038        21
         MSI     0.8889    0.8889    0.8889        27
      HM-SNV     0.3333    0.2500    0.2857         4
         EBV     1.0000    0.8333    0.9091         6

    accuracy                         0.8306       183
   macro avg     0.7272    0.7164    0.7134       183
weighted avg     0.8528    0.8306    0.8374       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.3519  std=0.0058  min=0.3436  max=0.3607
   meth : mean=0.3181  std=0.0030  min=0.3132  max=0.3238
   mirna: mean=0.3300  std=0.0051  min=0.3205  max=0.3385

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
[Train] Acc=0.3591  P=0.2864  R=0.3013  F1=0.2361
[Val  ] Acc=0.6486  P=0.5045  R=0.5987  F1=0.4552
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.7621  P=0.6093  R=0.7971  F1=0.6664
[Val  ] Acc=0.8108  P=0.5566  R=0.7378  F1=0.6154
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.9167  P=0.7971  R=0.9285  F1=0.8462
[Val  ] Acc=0.8378  P=0.7530  R=0.8418  F1=0.7751
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.9636  P=0.9205  R=0.9764  F1=0.9453
[Val  ] Acc=0.8919  P=0.8062  R=0.8214  F1=0.8100
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.9712  P=0.9480  R=0.9686  F1=0.9573
[Val  ] Acc=0.8649  P=0.8106  R=0.8134  F1=0.7767
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  25/150
[Train] Acc=0.9909  P=0.9872  R=0.9952  F1=0.9911
[Val  ] Acc=0.8784  P=0.7971  R=0.7992  F1=0.7938
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 5 | Epoch  30/150
[Train] Acc=0.9773  P=0.9189  R=0.9890  F1=0.9478
[Val  ] Acc=0.9054  P=0.9311  R=0.8072  F1=0.8514
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  35/150
[Train] Acc=0.9970  P=0.9949  R=0.9991  F1=0.9970
[Val  ] Acc=0.9189  P=0.8596  R=0.8294  F1=0.8434
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 5 | Epoch  40/150
[Train] Acc=0.9985  P=0.9974  R=0.9996  F1=0.9985
[Val  ] Acc=0.9189  P=0.8480  R=0.8476  F1=0.8469
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 5 | Epoch  45/150
[Train] Acc=0.9985  P=0.9974  R=0.9996  F1=0.9985
[Val  ] Acc=0.8919  P=0.8444  R=0.7849  F1=0.8084
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 45 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.8852  P=0.8446  R=0.8372  F1=0.8402
✅ Best val F1: 0.8514
✅ Test F1:     0.8402

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9127    0.9274    0.9200       124
          GS     0.6316    0.5455    0.5854        22
         MSI     0.9286    0.9630    0.9455        27
      HM-SNV     0.7500    0.7500    0.7500         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8852       183
   macro avg     0.8446    0.8372    0.8402       183
weighted avg     0.8806    0.8852    0.8824       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.3390  std=0.0000  min=0.3390  max=0.3390
   meth : mean=0.3570  std=0.0000  min=0.3570  max=0.3570
   mirna: mean=0.3040  std=0.0000  min=0.3040  max=0.3040

📈 5-fold CV summary
  ACCURACY : mean=0.8724  std=0.0252
  PRECISION: mean=0.7775  std=0.0730
  RECALL   : mean=0.7592  std=0.0664
  F1       : mean=0.7542  std=0.0663