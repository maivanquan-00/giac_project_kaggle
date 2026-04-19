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

🧠 Fold 1 model parameters: 3,315,209
🚀 Bắt đầu training fold 1...

🗓️  Scheduler: onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.3171  P=0.2937  R=0.3775  F1=0.2529
[Val  ] Acc=0.5135  P=0.6022  R=0.6587  F1=0.5484
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.7344  P=0.6296  R=0.7680  F1=0.6743
[Val  ] Acc=0.7568  P=0.5865  R=0.6631  F1=0.6122
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.9029  P=0.8326  R=0.9549  F1=0.8814
[Val  ] Acc=0.8649  P=0.8558  R=0.7911  F1=0.8041
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.9514  P=0.9180  R=0.9724  F1=0.9426
[Val  ] Acc=0.8784  P=0.6866  R=0.7173  F1=0.7007
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.9514  P=0.9349  R=0.9771  F1=0.9531
[Val  ] Acc=0.8784  P=0.8858  R=0.7992  F1=0.8255
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 1 | Epoch  25/150
[Train] Acc=0.9681  P=0.9383  R=0.9826  F1=0.9591
[Val  ] Acc=0.8649  P=0.8567  R=0.7911  F1=0.8056
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  30/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000
[Val  ] Acc=0.9189  P=0.9216  R=0.8253  F1=0.8559
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.9924  P=0.9833  R=0.9956  F1=0.9893
[Val  ] Acc=0.8919  P=0.8822  R=0.7991  F1=0.8223
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  40/150
[Train] Acc=0.9954  P=0.9944  R=0.9965  F1=0.9955
[Val  ] Acc=0.9189  P=0.9244  R=0.8071  F1=0.8422
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 1 | Epoch  45/150
[Train] Acc=0.9924  P=0.9758  R=0.9978  F1=0.9864
[Val  ] Acc=0.9189  P=0.9244  R=0.8071  F1=0.8422
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 45 cho Fold 1

📊 Đánh giá trên Test set - Fold 1
[Test ] Acc=0.8696  P=0.8779  R=0.8099  F1=0.8251
✅ Best val F1: 0.8559
✅ Test F1:     0.8251

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9250    0.8880    0.9061       125
          GS     0.6071    0.7727    0.6800        22
         MSI     0.8571    0.8889    0.8727        27
      HM-SNV     1.0000    0.5000    0.6667         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8696       184
   macro avg     0.8779    0.8099    0.8251       184
weighted avg     0.8811    0.8696    0.8720       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 1
   gene : mean=0.2953  std=0.4511  min=0.0007  max=0.9954
   meth : mean=0.5160  std=0.4965  min=0.0021  max=0.9985
   mirna: mean=0.1887  std=0.3852  min=0.0009  max=0.9931

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

🧠 Fold 2 model parameters: 3,315,209
🚀 Bắt đầu training fold 2...

🗓️  Scheduler: onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.2640  P=0.2894  R=0.3644  F1=0.2140
[Val  ] Acc=0.5270  P=0.3872  R=0.5202  F1=0.3646
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.7026  P=0.5954  R=0.6951  F1=0.5903
[Val  ] Acc=0.8243  P=0.5462  R=0.6912  F1=0.5977
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.8998  P=0.8320  R=0.9374  F1=0.8739
[Val  ] Acc=0.8378  P=0.7978  R=0.7912  F1=0.7625
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.9605  P=0.9026  R=0.9841  F1=0.9392
[Val  ] Acc=0.8919  P=0.8413  R=0.8072  F1=0.8001
       fusion_alpha=0.258  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.9484  P=0.9275  R=0.9752  F1=0.9474
[Val  ] Acc=0.8243  P=0.6595  R=0.6730  F1=0.6620
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
Fold 2 | Epoch  25/150
[Train] Acc=0.9818  P=0.9742  R=0.9909  F1=0.9820
[Val  ] Acc=0.9054  P=0.6574  R=0.7152  F1=0.6791
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 2 | Epoch  30/150
[Train] Acc=0.9788  P=0.9608  R=0.9863  F1=0.9728
[Val  ] Acc=0.8784  P=0.6366  R=0.7173  F1=0.6685
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 31 cho Fold 2

📊 Đánh giá trên Test set - Fold 2
[Test ] Acc=0.9130  P=0.8726  R=0.7893  F1=0.7821
✅ Best val F1: 0.8210
✅ Test F1:     0.7821

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9593    0.9440    0.9516       125
          GS     0.8261    0.8636    0.8444        22
         MSI     0.8276    0.8889    0.8571        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.9130       184
   macro avg     0.8726    0.7893    0.7821       184
weighted avg     0.9181    0.9130    0.9099       184

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 2
   gene : mean=0.5357  std=0.4950  min=0.0007  max=0.9984
   meth : mean=0.0050  std=0.0220  min=0.0010  max=0.2195
   mirna: mean=0.4594  std=0.4944  min=0.0005  max=0.9980

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

🧠 Fold 3 model parameters: 3,315,209
🚀 Bắt đầu training fold 3...

🗓️  Scheduler: onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.1576  P=0.2807  R=0.3002  F1=0.1514
[Val  ] Acc=0.3243  P=0.3090  R=0.4763  F1=0.2437
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.6318  P=0.5203  R=0.8030  F1=0.5627
[Val  ] Acc=0.7703  P=0.6395  R=0.8076  F1=0.6935
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.8924  P=0.8110  R=0.9503  F1=0.8608
[Val  ] Acc=0.8784  P=0.8874  R=0.8356  F1=0.8376
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.9485  P=0.9094  R=0.9748  F1=0.9388
[Val  ] Acc=0.8243  P=0.6688  R=0.8378  F1=0.7300
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.9515  P=0.8937  R=0.9677  F1=0.9258
[Val  ] Acc=0.9054  P=0.9060  R=0.8618  F1=0.8592
       fusion_alpha=0.255  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.9788  P=0.9525  R=0.9916  F1=0.9713
[Val  ] Acc=0.9189  P=0.8476  R=0.8476  F1=0.8476
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  30/150
[Train] Acc=0.9667  P=0.9560  R=0.9902  F1=0.9703
[Val  ] Acc=0.9324  P=0.8516  R=0.8516  F1=0.8516
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.9879  P=0.9833  R=0.9943  F1=0.9887
[Val  ] Acc=0.8649  P=0.7783  R=0.8316  F1=0.8001
       fusion_alpha=0.252  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  40/150
[Train] Acc=0.9924  P=0.9676  R=0.9891  F1=0.9773
[Val  ] Acc=0.9054  P=0.7694  R=0.8436  F1=0.7994
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  45/150
[Train] Acc=0.9955  P=0.9821  R=0.9987  F1=0.9901
[Val  ] Acc=0.9324  P=0.8072  R=0.8516  F1=0.8221
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  50/150
[Train] Acc=0.9985  P=0.9975  R=0.9996  F1=0.9985
[Val  ] Acc=0.9054  P=0.8183  R=0.8436  F1=0.8301
       fusion_alpha=0.250  (GAT=0.25, Shortcut=0.75)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  55/150
[Train] Acc=0.9909  P=0.9859  R=0.9973  F1=0.9914
[Val  ] Acc=0.9324  P=0.9478  R=0.8516  F1=0.8830
       fusion_alpha=0.249  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  60/150
[Train] Acc=0.9985  P=0.9867  R=0.9996  F1=0.9929
[Val  ] Acc=0.9189  P=0.9324  R=0.8476  F1=0.8730
       fusion_alpha=0.249  (GAT=0.25, Shortcut=0.75)
Fold 3 | Epoch  65/150
[Train] Acc=0.9985  P=0.9980  R=0.9996  F1=0.9988
[Val  ] Acc=0.9324  P=0.9478  R=0.8516  F1=0.8830
       fusion_alpha=0.248  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 66 cho Fold 3

📊 Đánh giá trên Test set - Fold 3
[Test ] Acc=0.8743  P=0.7288  R=0.7427  F1=0.7288
✅ Best val F1: 0.9095
✅ Test F1:     0.7288

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.8992    0.9280    0.9134       125
          GS     0.6875    0.5238    0.5946        21
         MSI     1.0000    0.9286    0.9630        28
      HM-SNV     0.2000    0.3333    0.2500         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8743       183
   macro avg     0.7288    0.7427    0.7288       183
weighted avg     0.8775    0.8743    0.8738       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 3
   gene : mean=0.4600  std=0.4956  min=0.0022  max=0.9982
   meth : mean=0.3605  std=0.4768  min=0.0007  max=0.9945
   mirna: mean=0.1795  std=0.3785  min=0.0006  max=0.9907

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

🧠 Fold 4 model parameters: 3,315,209
🚀 Bắt đầu training fold 4...

🗓️  Scheduler: onecycle
Fold 4 | Epoch   1/150
[Train] Acc=0.2545  P=0.2911  R=0.3093  F1=0.2123
[Val  ] Acc=0.5676  P=0.4888  R=0.6253  F1=0.4999
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.7061  P=0.5702  R=0.8013  F1=0.6296
[Val  ] Acc=0.7568  P=0.5495  R=0.6996  F1=0.5989
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.8742  P=0.7955  R=0.9369  F1=0.8458
[Val  ] Acc=0.9054  P=0.6602  R=0.7436  F1=0.6949
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.9667  P=0.9160  R=0.9881  F1=0.9474
[Val  ] Acc=0.9054  P=0.6727  R=0.7253  F1=0.6895
       fusion_alpha=0.259  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.9742  P=0.9663  R=0.9866  F1=0.9759
[Val  ] Acc=0.8514  P=0.6633  R=0.7093  F1=0.6822
       fusion_alpha=0.257  (GAT=0.26, Shortcut=0.74)
Fold 4 | Epoch  25/150
[Train] Acc=0.9833  P=0.9767  R=0.9930  F1=0.9845
[Val  ] Acc=0.8784  P=0.7032  R=0.7173  F1=0.7085
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.9848  P=0.9483  R=0.9940  F1=0.9698
[Val  ] Acc=0.8649  P=0.6862  R=0.7133  F1=0.6985
       fusion_alpha=0.254  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  35/150
[Train] Acc=0.9848  P=0.9791  R=0.9918  F1=0.9852
[Val  ] Acc=0.8919  P=0.6970  R=0.7396  F1=0.7166
       fusion_alpha=0.253  (GAT=0.25, Shortcut=0.75)
Fold 4 | Epoch  40/150
[Train] Acc=0.9803  P=0.9413  R=0.9884  F1=0.9635
[Val  ] Acc=0.8784  P=0.7173  R=0.7173  F1=0.7165
       fusion_alpha=0.251  (GAT=0.25, Shortcut=0.75)
⏹️  Early stopping tại epoch 41 cho Fold 4

📊 Đánh giá trên Test set - Fold 4
[Test ] Acc=0.9016  P=0.9067  R=0.8043  F1=0.8063
✅ Best val F1: 0.7461
✅ Test F1:     0.8063

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9496    0.9040    0.9262       125
          GS     0.6552    0.9048    0.7600        21
         MSI     0.9286    0.9630    0.9455        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.9016       183
   macro avg     0.9067    0.8043    0.8063       183
weighted avg     0.9155    0.9016    0.9009       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 4
   gene : mean=0.5465  std=0.4959  min=0.0022  max=0.9989
   meth : mean=0.2444  std=0.4247  min=0.0005  max=0.9943
   mirna: mean=0.2091  std=0.4015  min=0.0005  max=0.9951

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

🧠 Fold 5 model parameters: 3,315,209
🚀 Bắt đầu training fold 5...

🗓️  Scheduler: onecycle
Fold 5 | Epoch   1/150
[Train] Acc=0.2591  P=0.3043  R=0.3447  F1=0.2162
[Val  ] Acc=0.5541  P=0.4250  R=0.6193  F1=0.4362
       fusion_alpha=0.269  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.6727  P=0.5340  R=0.7821  F1=0.5776
[Val  ] Acc=0.7838  P=0.5897  R=0.7298  F1=0.6335
       fusion_alpha=0.267  (GAT=0.27, Shortcut=0.73)
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: /kaggle/working/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.9182  P=0.8456  R=0.9573  F1=0.8870
[Val  ] Acc=0.8784  P=0.7592  R=0.7032  F1=0.7243
       fusion_alpha=0.262  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  15/150
[Train] Acc=0.9621  P=0.9243  R=0.9680  F1=0.9441
[Val  ] Acc=0.8784  P=0.7251  R=0.7214  F1=0.7232
       fusion_alpha=0.259  (GAT=0.26, Shortcut=0.74)
Fold 5 | Epoch  20/150
[Train] Acc=0.9409  P=0.8748  R=0.9757  F1=0.9166
[Val  ] Acc=0.8514  P=0.6341  R=0.6587  F1=0.6290
       fusion_alpha=0.256  (GAT=0.26, Shortcut=0.74)
⏹️  Early stopping tại epoch 22 cho Fold 5

📊 Đánh giá trên Test set - Fold 5
[Test ] Acc=0.7978  P=0.6367  R=0.7237  F1=0.6711
✅ Best val F1: 0.8105
✅ Test F1:     0.6711

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9259    0.8065    0.8621       124
          GS     0.4242    0.6364    0.5091        22
         MSI     0.8333    0.9259    0.8772        27
      HM-SNV     0.2500    0.2500    0.2500         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.7978       183
   macro avg     0.6367    0.7237    0.6711       183
weighted avg     0.8314    0.7978    0.8083       183

  📄 Confusion matrix (absolute) saved: /kaggle/working/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Patient Gate Statistics - Fold 5
   gene : mean=0.0090  std=0.0248  min=0.0019  max=0.2115
   meth : mean=0.4406  std=0.4874  min=0.0013  max=0.9970
   mirna: mean=0.5504  std=0.4898  min=0.0008  max=0.9958

📈 5-fold CV summary
  ACCURACY : mean=0.8713  std=0.0402
  PRECISION: mean=0.8045  std=0.1043
  RECALL   : mean=0.7740  std=0.0345
  F1       : mean=0.7627  std=0.0561

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

         CIN     0.8779    0.9200    0.8984       125
          GS     0.7647    0.5909    0.6667        22
         MSI     0.7308    0.7037    0.7170        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8424       184
   macro avg     0.7794    0.7429    0.7553       184
weighted avg     0.8375    0.8424    0.8378       184

[Test] Acc=0.8424  P=0.7794  R=0.7429  F1=0.7553

🔍 Patient Modality Gate Statistics (N=184)
   Gene expression     : mean=0.2852  std=0.4439
   DNA methylation     : mean=0.5731  std=0.4893
   miRNA               : mean=0.1417  std=0.3350

✔️  Accuracy: 0.8424
   Correct: 155 / 184

   🖥️  Device: cuda
📐 Building 5-fold CV for ablation study...
📂 Loading data từ: /kaggle/input/datasets/maivanquan/datn-2025-2/data_final
  Labels : (917, 3)
  Gene   : (917, 19930)
  Meth   : (917, 23111)
  miRNA  : (917, 1881)

  Samples sau align : 917
  Phân bố subtype   : {np.int64(0): np.int64(624), np.int64(1): np.int64(108), np.int64(2): np.int64(136), np.int64(3): np.int64(19), np.int64(4): np.int64(30)}


******************************************************************************
*  ABLATION — Fold 1/5
*  gene=3000, meth=3000, mirna=1000
******************************************************************************

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

============================================================
🔬 Ablation: gene_only
   Gene=✅  Meth=❌  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2978  Val F1=0.4427
   Epoch  20: Train F1=0.9543  Val F1=0.8278
   ⏹️  Early stop at epoch 40

   ✅ Best Val F1 = 0.8382
[Test ] Acc=0.8587  P=0.7713  R=0.7801  F1=0.7756

   📋 Per-class breakdown (gene_only):
              precision    recall  f1-score   support

         CIN     0.9187    0.9040    0.9113       125
          GS     0.6522    0.6818    0.6667        22
         MSI     0.7857    0.8148    0.8000        27
      HM-SNV     0.5000    0.5000    0.5000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8587       184
   macro avg     0.7713    0.7801    0.7756       184
weighted avg     0.8609    0.8587    0.8597       184


============================================================
🔬 Ablation: meth_only
   Gene=❌  Meth=✅  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2885  Val F1=0.3082
   Epoch  20: Train F1=0.9612  Val F1=0.6791
   Epoch  40: Train F1=0.9970  Val F1=0.8668
   ⏹️  Early stop at epoch 56

   ✅ Best Val F1 = 0.8788
[Test ] Acc=0.8859  P=0.8034  R=0.7663  F1=0.7763

   📋 Per-class breakdown (meth_only):
              precision    recall  f1-score   support

         CIN     0.9200    0.9200    0.9200       125
          GS     0.7083    0.7727    0.7391        22
         MSI     0.8889    0.8889    0.8889        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8859       184
   macro avg     0.8034    0.7663    0.7763       184
weighted avg     0.8836    0.8859    0.8837       184


============================================================
🔬 Ablation: mirna_only
   Gene=❌  Meth=❌  miRNA=✅
============================================================
   Epoch   1: Train F1=0.1997  Val F1=0.3192
   Epoch  20: Train F1=0.9371  Val F1=0.5334
   Epoch  40: Train F1=0.9839  Val F1=0.6219
   ⏹️  Early stop at epoch 53

   ✅ Best Val F1 = 0.6413
[Test ] Acc=0.7065  P=0.6877  R=0.6412  F1=0.6434

   📋 Per-class breakdown (mirna_only):
              precision    recall  f1-score   support

         CIN     0.8482    0.7600    0.8017       125
          GS     0.3000    0.4091    0.3462        22
         MSI     0.5758    0.7037    0.6333        27
      HM-SNV     1.0000    0.5000    0.6667         4
         EBV     0.7143    0.8333    0.7692         6

    accuracy                         0.7065       184
   macro avg     0.6877    0.6412    0.6434       184
weighted avg     0.7416    0.7065    0.7185       184


============================================================
🔬 Ablation: gene+meth
   Gene=✅  Meth=✅  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2853  Val F1=0.4990
   Epoch  20: Train F1=0.9662  Val F1=0.8460
   ⏹️  Early stop at epoch 40

   ✅ Best Val F1 = 0.8668
[Test ] Acc=0.8641  P=0.8125  R=0.8025  F1=0.8024

   📋 Per-class breakdown (gene+meth):
              precision    recall  f1-score   support

         CIN     0.9250    0.8880    0.9061       125
          GS     0.5862    0.7727    0.6667        22
         MSI     0.8846    0.8519    0.8679        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8641       184
   macro avg     0.8125    0.8025    0.8024       184
weighted avg     0.8754    0.8641    0.8677       184


============================================================
🔬 Ablation: gene+mirna
   Gene=✅  Meth=❌  miRNA=✅
============================================================
   Epoch   1: Train F1=0.2942  Val F1=0.4359
   Epoch  20: Train F1=0.9473  Val F1=0.8382
   Epoch  40: Train F1=0.9958  Val F1=0.8498
   ⏹️  Early stop at epoch 50

   ✅ Best Val F1 = 0.8498
[Test ] Acc=0.8641  P=0.7773  R=0.7817  F1=0.7794

   📋 Per-class breakdown (gene+mirna):
              precision    recall  f1-score   support

         CIN     0.9194    0.9120    0.9157       125
          GS     0.6522    0.6818    0.6667        22
         MSI     0.8148    0.8148    0.8148        27
      HM-SNV     0.5000    0.5000    0.5000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8641       184
   macro avg     0.7773    0.7817    0.7794       184
weighted avg     0.8656    0.8641    0.8648       184


============================================================
🔬 Ablation: all
   Gene=✅  Meth=✅  miRNA=✅
============================================================
   Epoch   1: Train F1=0.2800  Val F1=0.6165
   Epoch  20: Train F1=0.9774  Val F1=0.8128
   Epoch  40: Train F1=0.9955  Val F1=0.8422
   ⏹️  Early stop at epoch 43

   ✅ Best Val F1 = 0.8668
[Test ] Acc=0.8750  P=0.8164  R=0.8057  F1=0.8072

   📋 Per-class breakdown (all):
              precision    recall  f1-score   support

         CIN     0.9339    0.9040    0.9187       125
          GS     0.6296    0.7727    0.6939        22
         MSI     0.8519    0.8519    0.8519        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8750       184
   macro avg     0.8164    0.8057    0.8072       184
weighted avg     0.8818    0.8750    0.8771       184


==========================================================================
📊 ABLATION SUMMARY — Fold 1
==========================================================================
Config            Val F1   Test Acc   Test P   Test R  Test F1
--------------------------------------------------------------------------
gene_only         0.8382     0.8587   0.7713   0.7801   0.7756
meth_only         0.8788     0.8859   0.8034   0.7663   0.7763
mirna_only        0.6413     0.7065   0.6877   0.6412   0.6434
gene+meth         0.8668     0.8641   0.8125   0.8025   0.8024
gene+mirna        0.8498     0.8641   0.7773   0.7817   0.7794
all               0.8668     0.8750   0.8164   0.8057   0.8072
==========================================================================


******************************************************************************
*  ABLATION — Fold 2/5
*  gene=3000, meth=3000, mirna=1000
******************************************************************************

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

============================================================
🔬 Ablation: gene_only
   Gene=✅  Meth=❌  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2626  Val F1=0.3269
   Epoch  20: Train F1=0.9519  Val F1=0.8221
   ⏹️  Early stop at epoch 32

   ✅ Best Val F1 = 0.8564
[Test ] Acc=0.8913  P=0.8649  R=0.7979  F1=0.7786

   📋 Per-class breakdown (gene_only):
              precision    recall  f1-score   support

         CIN     0.9739    0.8960    0.9333       125
          GS     0.6364    0.9545    0.7636        22
         MSI     0.8571    0.8889    0.8727        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8913       184
   macro avg     0.8649    0.7979    0.7786       184
weighted avg     0.9132    0.8913    0.8922       184


============================================================
🔬 Ablation: meth_only
   Gene=❌  Meth=✅  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2646  Val F1=0.3521
   Epoch  20: Train F1=0.9631  Val F1=0.6597
   ⏹️  Early stop at epoch 30

   ✅ Best Val F1 = 0.6735
[Test ] Acc=0.8804  P=0.7418  R=0.8298  F1=0.7765

   📋 Per-class breakdown (meth_only):
              precision    recall  f1-score   support

         CIN     0.9823    0.8880    0.9328       125
          GS     0.6250    0.9091    0.7407        22
         MSI     0.8519    0.8519    0.8519        27
      HM-SNV     0.5000    0.5000    0.5000         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.8804       184
   macro avg     0.7418    0.8298    0.7765       184
weighted avg     0.9024    0.8804    0.8861       184


============================================================
🔬 Ablation: mirna_only
   Gene=❌  Meth=❌  miRNA=✅
============================================================
   Epoch   1: Train F1=0.1740  Val F1=0.2237
   Epoch  20: Train F1=0.9137  Val F1=0.4770
   Epoch  40: Train F1=0.9869  Val F1=0.5108
   Epoch  60: Train F1=0.9925  Val F1=0.4926
   ⏹️  Early stop at epoch 64

   ✅ Best Val F1 = 0.5189
[Test ] Acc=0.8424  P=0.7002  R=0.7460  F1=0.7179

   📋 Per-class breakdown (mirna_only):
              precision    recall  f1-score   support

         CIN     0.9310    0.8640    0.8963       125
          GS     0.5517    0.7273    0.6275        22
         MSI     0.8276    0.8889    0.8571        27
      HM-SNV     0.3333    0.2500    0.2857         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8424       184
   macro avg     0.7002    0.7460    0.7179       184
weighted avg     0.8551    0.8424    0.8460       184


============================================================
🔬 Ablation: gene+meth
   Gene=✅  Meth=✅  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2831  Val F1=0.4231
   Epoch  20: Train F1=0.9626  Val F1=0.7762
   ⏹️  Early stop at epoch 26

   ✅ Best Val F1 = 0.8228
[Test ] Acc=0.8913  P=0.8138  R=0.8814  F1=0.8424

   📋 Per-class breakdown (gene+meth):
              precision    recall  f1-score   support

         CIN     0.9739    0.8960    0.9333       125
          GS     0.6667    0.9091    0.7692        22
         MSI     0.8214    0.8519    0.8364        27
      HM-SNV     0.7500    0.7500    0.7500         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8913       184
   macro avg     0.8138    0.8814    0.8424       184
weighted avg     0.9061    0.8913    0.8952       184


============================================================
🔬 Ablation: gene+mirna
   Gene=✅  Meth=❌  miRNA=✅
============================================================
   Epoch   1: Train F1=0.2574  Val F1=0.3793
   Epoch  20: Train F1=0.9777  Val F1=0.8303
   ⏹️  Early stop at epoch 37

   ✅ Best Val F1 = 0.8462
[Test ] Acc=0.9076  P=0.8860  R=0.7935  F1=0.7927

   📋 Per-class breakdown (gene+mirna):
              precision    recall  f1-score   support

         CIN     0.9508    0.9280    0.9393       125
          GS     0.7600    0.8636    0.8085        22
         MSI     0.8621    0.9259    0.8929        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.9076       184
   macro avg     0.8860    0.7935    0.7927       184
weighted avg     0.9130    0.9076    0.9046       184


============================================================
🔬 Ablation: all
   Gene=✅  Meth=✅  miRNA=✅
============================================================
   Epoch   1: Train F1=0.2443  Val F1=0.3876
   Epoch  20: Train F1=0.9748  Val F1=0.7942
   ⏹️  Early stop at epoch 34

   ✅ Best Val F1 = 0.8322
[Test ] Acc=0.9130  P=0.8806  R=0.8936  F1=0.8799

   📋 Per-class breakdown (all):
              precision    recall  f1-score   support

         CIN     0.9746    0.9200    0.9465       125
          GS     0.7143    0.9091    0.8000        22
         MSI     0.8571    0.8889    0.8727        27
      HM-SNV     1.0000    0.7500    0.8571         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.9130       184
   macro avg     0.8806    0.8936    0.8799       184
weighted avg     0.9229    0.9130    0.9155       184


==========================================================================
📊 ABLATION SUMMARY — Fold 2
==========================================================================
Config            Val F1   Test Acc   Test P   Test R  Test F1
--------------------------------------------------------------------------
gene_only         0.8564     0.8913   0.8649   0.7979   0.7786
meth_only         0.6735     0.8804   0.7418   0.8298   0.7765
mirna_only        0.5189     0.8424   0.7002   0.7460   0.7179
gene+meth         0.8228     0.8913   0.8138   0.8814   0.8424
gene+mirna        0.8462     0.9076   0.8860   0.7935   0.7927
all               0.8322     0.9130   0.8806   0.8936   0.8799
==========================================================================


******************************************************************************
*  ABLATION — Fold 3/5
*  gene=3000, meth=3000, mirna=1000
******************************************************************************

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

============================================================
🔬 Ablation: gene_only
   Gene=✅  Meth=❌  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2360  Val F1=0.3647
   Epoch  20: Train F1=0.9633  Val F1=0.8568
   Epoch  40: Train F1=0.9955  Val F1=0.8307
   ⏹️  Early stop at epoch 41

   ✅ Best Val F1 = 0.8681
[Test ] Acc=0.8798  P=0.7684  R=0.7523  F1=0.7588

   📋 Per-class breakdown (gene_only):
              precision    recall  f1-score   support

         CIN     0.9062    0.9280    0.9170       125
          GS     0.7059    0.5714    0.6316        21
         MSI     0.8966    0.9286    0.9123        28
      HM-SNV     0.3333    0.3333    0.3333         3
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8798       183
   macro avg     0.7684    0.7523    0.7588       183
weighted avg     0.8755    0.8798    0.8767       183


============================================================
🔬 Ablation: meth_only
   Gene=❌  Meth=✅  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2418  Val F1=0.4593
   Epoch  20: Train F1=0.9597  Val F1=0.8106
   ⏹️  Early stop at epoch 32

   ✅ Best Val F1 = 0.8106
[Test ] Acc=0.8689  P=0.6598  R=0.6998  F1=0.6777

   📋 Per-class breakdown (meth_only):
              precision    recall  f1-score   support

         CIN     0.9187    0.9040    0.9113       125
          GS     0.5600    0.6667    0.6087        21
         MSI     0.9630    0.9286    0.9455        28
      HM-SNV     0.0000    0.0000    0.0000         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8689       183
   macro avg     0.6598    0.6998    0.6777       183
weighted avg     0.8672    0.8689    0.8672       183


============================================================
🔬 Ablation: mirna_only
   Gene=❌  Meth=❌  miRNA=✅
============================================================
   Epoch   1: Train F1=0.1951  Val F1=0.2550
   Epoch  20: Train F1=0.9354  Val F1=0.5643
   Epoch  40: Train F1=0.9861  Val F1=0.5645
   ⏹️  Early stop at epoch 48

   ✅ Best Val F1 = 0.5799
[Test ] Acc=0.7432  P=0.5323  R=0.5553  F1=0.5387

   📋 Per-class breakdown (mirna_only):
              precision    recall  f1-score   support

         CIN     0.8281    0.8480    0.8379       125
          GS     0.2500    0.1429    0.1818        21
         MSI     0.6667    0.7857    0.7213        28
      HM-SNV     0.2500    0.3333    0.2857         3
         EBV     0.6667    0.6667    0.6667         6

    accuracy                         0.7432       183
   macro avg     0.5323    0.5553    0.5387       183
weighted avg     0.7223    0.7432    0.7301       183


============================================================
🔬 Ablation: gene+meth
   Gene=✅  Meth=✅  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2576  Val F1=0.5293
   Epoch  20: Train F1=0.9707  Val F1=0.8255
   ⏹️  Early stop at epoch 37

   ✅ Best Val F1 = 0.8328
[Test ] Acc=0.8907  P=0.7544  R=0.7555  F1=0.7528

   📋 Per-class breakdown (gene+meth):
              precision    recall  f1-score   support

         CIN     0.9147    0.9440    0.9291       125
          GS     0.6667    0.5714    0.6154        21
         MSI     1.0000    0.9286    0.9630        28
      HM-SNV     0.3333    0.3333    0.3333         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8907       183
   macro avg     0.7544    0.7555    0.7528       183
weighted avg     0.8879    0.8907    0.8883       183


============================================================
🔬 Ablation: gene+mirna
   Gene=✅  Meth=❌  miRNA=✅
============================================================
   Epoch   1: Train F1=0.2534  Val F1=0.3703
   Epoch  20: Train F1=0.9758  Val F1=0.8038
   Epoch  40: Train F1=0.9985  Val F1=0.8156
   ⏹️  Early stop at epoch 49

   ✅ Best Val F1 = 0.8476
[Test ] Acc=0.8470  P=0.7238  R=0.7189  F1=0.7201

   📋 Per-class breakdown (gene+mirna):
              precision    recall  f1-score   support

         CIN     0.8898    0.9040    0.8968       125
          GS     0.5294    0.4286    0.4737        21
         MSI     0.8667    0.9286    0.8966        28
      HM-SNV     0.3333    0.3333    0.3333         3
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8470       183
   macro avg     0.7238    0.7189    0.7201       183
weighted avg     0.8394    0.8470    0.8424       183


============================================================
🔬 Ablation: all
   Gene=✅  Meth=✅  miRNA=✅
============================================================
   Epoch   1: Train F1=0.2760  Val F1=0.4040
   Epoch  20: Train F1=0.9776  Val F1=0.8096
   Epoch  40: Train F1=0.9914  Val F1=0.8195
   ⏹️  Early stop at epoch 52

   ✅ Best Val F1 = 0.8301
[Test ] Acc=0.8798  P=0.7349  R=0.7364  F1=0.7298

   📋 Per-class breakdown (all):
              precision    recall  f1-score   support

         CIN     0.9008    0.9440    0.9219       125
          GS     0.6667    0.4762    0.5556        21
         MSI     1.0000    0.9286    0.9630        28
      HM-SNV     0.2500    0.3333    0.2857         3
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8798       183
   macro avg     0.7349    0.7364    0.7298       183
weighted avg     0.8770    0.8798    0.8757       183


==========================================================================
📊 ABLATION SUMMARY — Fold 3
==========================================================================
Config            Val F1   Test Acc   Test P   Test R  Test F1
--------------------------------------------------------------------------
gene_only         0.8681     0.8798   0.7684   0.7523   0.7588
meth_only         0.8106     0.8689   0.6598   0.6998   0.6777
mirna_only        0.5799     0.7432   0.5323   0.5553   0.5387
gene+meth         0.8328     0.8907   0.7544   0.7555   0.7528
gene+mirna        0.8476     0.8470   0.7238   0.7189   0.7201
all               0.8301     0.8798   0.7349   0.7364   0.7298
==========================================================================


******************************************************************************
*  ABLATION — Fold 4/5
*  gene=3000, meth=3000, mirna=1000
******************************************************************************

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

============================================================
🔬 Ablation: gene_only
   Gene=✅  Meth=❌  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2397  Val F1=0.4089
   Epoch  20: Train F1=0.9709  Val F1=0.7370
   ⏹️  Early stop at epoch 32

   ✅ Best Val F1 = 0.7370
[Test ] Acc=0.8634  P=0.6721  R=0.7051  F1=0.6875

   📋 Per-class breakdown (gene_only):
              precision    recall  f1-score   support

         CIN     0.9106    0.8960    0.9032       125
          GS     0.5833    0.6667    0.6222        21
         MSI     0.8667    0.9630    0.9123        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8634       183
   macro avg     0.6721    0.7051    0.6875       183
weighted avg     0.8496    0.8634    0.8557       183


============================================================
🔬 Ablation: meth_only
   Gene=❌  Meth=✅  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2634  Val F1=0.3790
   Epoch  20: Train F1=0.9526  Val F1=0.7411
   Epoch  40: Train F1=0.9876  Val F1=0.7287
   ⏹️  Early stop at epoch 52

   ✅ Best Val F1 = 0.7505
[Test ] Acc=0.8798  P=0.8962  R=0.7546  F1=0.7800

   📋 Per-class breakdown (meth_only):
              precision    recall  f1-score   support

         CIN     0.9055    0.9200    0.9127       125
          GS     0.6522    0.7143    0.6818        21
         MSI     0.9231    0.8889    0.9057        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8798       183
   macro avg     0.8962    0.7546    0.7800       183
weighted avg     0.8842    0.8798    0.8768       183


============================================================
🔬 Ablation: mirna_only
   Gene=❌  Meth=❌  miRNA=✅
============================================================
   Epoch   1: Train F1=0.1917  Val F1=0.2510
   Epoch  20: Train F1=0.9439  Val F1=0.5741
   ⏹️  Early stop at epoch 27

   ✅ Best Val F1 = 0.6819
[Test ] Acc=0.7705  P=0.6389  R=0.7046  F1=0.6469

   📋 Per-class breakdown (mirna_only):
              precision    recall  f1-score   support

         CIN     0.9307    0.7520    0.8319       125
          GS     0.4444    0.7619    0.5614        21
         MSI     0.6944    0.9259    0.7937        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     0.6250    0.8333    0.7143         6

    accuracy                         0.7705       183
   macro avg     0.6389    0.7046    0.6469       183
weighted avg     0.8206    0.7705    0.7804       183


============================================================
🔬 Ablation: gene+meth
   Gene=✅  Meth=✅  miRNA=❌
============================================================
   Epoch   1: Train F1=0.3024  Val F1=0.4870
   Epoch  20: Train F1=0.9814  Val F1=0.7287
   ⏹️  Early stop at epoch 36

   ✅ Best Val F1 = 0.7381
[Test ] Acc=0.8907  P=0.9032  R=0.7874  F1=0.7964

   📋 Per-class breakdown (gene+meth):
              precision    recall  f1-score   support

         CIN     0.9339    0.9040    0.9187       125
          GS     0.6207    0.8571    0.7200        21
         MSI     0.9615    0.9259    0.9434        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8907       183
   macro avg     0.9032    0.7874    0.7964       183
weighted avg     0.9056    0.8907    0.8909       183


============================================================
🔬 Ablation: gene+mirna
   Gene=✅  Meth=❌  miRNA=✅
============================================================
   Epoch   1: Train F1=0.2643  Val F1=0.3969
   Epoch  20: Train F1=0.9795  Val F1=0.7007
   ⏹️  Early stop at epoch 27

   ✅ Best Val F1 = 0.7166
[Test ] Acc=0.8579  P=0.6665  R=0.7114  F1=0.6866

   📋 Per-class breakdown (gene+mirna):
              precision    recall  f1-score   support

         CIN     0.9167    0.8800    0.8980       125
          GS     0.5769    0.7143    0.6383        21
         MSI     0.8387    0.9630    0.8966        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8579       183
   macro avg     0.6665    0.7114    0.6866       183
weighted avg     0.8489    0.8579    0.8517       183


============================================================
🔬 Ablation: all
   Gene=✅  Meth=✅  miRNA=✅
============================================================
   Epoch   1: Train F1=0.2867  Val F1=0.4386
   Epoch  20: Train F1=0.9720  Val F1=0.7085
   Epoch  40: Train F1=0.9988  Val F1=0.7339
   ⏹️  Early stop at epoch 45

   ✅ Best Val F1 = 0.7339
[Test ] Acc=0.8907  P=0.8969  R=0.7853  F1=0.7941

   📋 Per-class breakdown (all):
              precision    recall  f1-score   support

         CIN     0.9339    0.9040    0.9187       125
          GS     0.6538    0.8095    0.7234        21
         MSI     0.8966    0.9630    0.9286        27
      HM-SNV     1.0000    0.2500    0.4000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8907       183
   macro avg     0.8969    0.7853    0.7941       183
weighted avg     0.8999    0.8907    0.8891       183


==========================================================================
📊 ABLATION SUMMARY — Fold 4
==========================================================================
Config            Val F1   Test Acc   Test P   Test R  Test F1
--------------------------------------------------------------------------
gene_only         0.7370     0.8634   0.6721   0.7051   0.6875
meth_only         0.7505     0.8798   0.8962   0.7546   0.7800
mirna_only        0.6819     0.7705   0.6389   0.7046   0.6469
gene+meth         0.7381     0.8907   0.9032   0.7874   0.7964
gene+mirna        0.7166     0.8579   0.6665   0.7114   0.6866
all               0.7339     0.8907   0.8969   0.7853   0.7941
==========================================================================


******************************************************************************
*  ABLATION — Fold 5/5
*  gene=3000, meth=3000, mirna=1000
******************************************************************************

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

============================================================
🔬 Ablation: gene_only
   Gene=✅  Meth=❌  miRNA=❌
============================================================
   Epoch   1: Train F1=0.2667  Val F1=0.4143
   Epoch  20: Train F1=0.9682  Val F1=0.7395
   ⏹️  Early stop at epoch 30

   ✅ Best Val F1 = 0.7416
[Test ] Acc=0.8689  P=0.8214  R=0.8398  F1=0.8300

   📋 Per-class breakdown (gene_only):
              precision    recall  f1-score   support

         CIN     0.9250    0.8952    0.9098       124
          GS     0.5652    0.5909    0.5778        22
         MSI     0.8667    0.9630    0.9123        27
      HM-SNV     0.7500    0.7500    0.7500         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8689       183
   macro avg     0.8214    0.8398    0.8300       183
weighted avg     0.8718    0.8689    0.8697       183


============================================================
🔬 Ablation: meth_only
   Gene=❌  Meth=✅  miRNA=❌
============================================================
   Epoch   1: Train F1=0.3282  Val F1=0.4358
   Epoch  20: Train F1=0.9680  Val F1=0.7445
   ⏹️  Early stop at epoch 25

   ✅ Best Val F1 = 0.7489
[Test ] Acc=0.7814  P=0.5910  R=0.6705  F1=0.6228

   📋 Per-class breakdown (meth_only):
              precision    recall  f1-score   support

         CIN     0.9159    0.7903    0.8485       124
          GS     0.4242    0.6364    0.5091        22
         MSI     0.7576    0.9259    0.8333        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.7814       183
   macro avg     0.5910    0.6705    0.6228       183
weighted avg     0.8115    0.7814    0.7893       183


============================================================
🔬 Ablation: mirna_only
   Gene=❌  Meth=❌  miRNA=✅
============================================================
   Epoch   1: Train F1=0.1988  Val F1=0.3443
   Epoch  20: Train F1=0.9436  Val F1=0.6981
   Epoch  40: Train F1=0.9894  Val F1=0.6954
   ⏹️  Early stop at epoch 45

   ✅ Best Val F1 = 0.7461
[Test ] Acc=0.7760  P=0.5466  R=0.6114  F1=0.5749

   📋 Per-class breakdown (mirna_only):
              precision    recall  f1-score   support

         CIN     0.8783    0.8145    0.8452       124
          GS     0.3462    0.4091    0.3750        22
         MSI     0.7941    1.0000    0.8852        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     0.7143    0.8333    0.7692         6

    accuracy                         0.7760       183
   macro avg     0.5466    0.6114    0.5749       183
weighted avg     0.7773    0.7760    0.7736       183


============================================================
🔬 Ablation: gene+meth
   Gene=✅  Meth=✅  miRNA=❌
============================================================
   Epoch   1: Train F1=0.3017  Val F1=0.4523
   Epoch  20: Train F1=0.9828  Val F1=0.7067
   ⏹️  Early stop at epoch 32

   ✅ Best Val F1 = 0.7565
[Test ] Acc=0.8852  P=0.8272  R=0.8021  F1=0.8114

   📋 Per-class breakdown (gene+meth):
              precision    recall  f1-score   support

         CIN     0.9194    0.9194    0.9194       124
          GS     0.6500    0.5909    0.6190        22
         MSI     0.9000    1.0000    0.9474        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8852       183
   macro avg     0.8272    0.8021    0.8114       183
weighted avg     0.8812    0.8852    0.8824       183


============================================================
🔬 Ablation: gene+mirna
   Gene=✅  Meth=❌  miRNA=✅
============================================================
   Epoch   1: Train F1=0.2531  Val F1=0.4609
   Epoch  20: Train F1=0.9765  Val F1=0.7938
   Epoch  40: Train F1=0.9985  Val F1=0.7980
   ⏹️  Early stop at epoch 41

   ✅ Best Val F1 = 0.8676
[Test ] Acc=0.8852  P=0.8311  R=0.7738  F1=0.7937

   📋 Per-class breakdown (gene+mirna):
              precision    recall  f1-score   support

         CIN     0.9077    0.9516    0.9291       124
          GS     0.7143    0.4545    0.5556        22
         MSI     0.8667    0.9630    0.9123        27
      HM-SNV     0.6667    0.5000    0.5714         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8852       183
   macro avg     0.8311    0.7738    0.7937       183
weighted avg     0.8761    0.8852    0.8762       183


============================================================
🔬 Ablation: all
   Gene=✅  Meth=✅  miRNA=✅
============================================================
   Epoch   1: Train F1=0.3122  Val F1=0.4400
   ⏹️  Early stop at epoch 20

   ✅ Best Val F1 = 0.7837
[Test ] Acc=0.7869  P=0.6455  R=0.7056  F1=0.6673

   📋 Per-class breakdown (all):
              precision    recall  f1-score   support

         CIN     0.9174    0.8065    0.8584       124
          GS     0.4615    0.5455    0.5000        22
         MSI     0.6579    0.9259    0.7692        27
      HM-SNV     0.3333    0.2500    0.2857         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.7869       183
   macro avg     0.6455    0.7056    0.6673       183
weighted avg     0.8096    0.7869    0.7917       183


==========================================================================
📊 ABLATION SUMMARY — Fold 5
==========================================================================
Config            Val F1   Test Acc   Test P   Test R  Test F1
--------------------------------------------------------------------------
gene_only         0.7416     0.8689   0.8214   0.8398   0.8300
meth_only         0.7489     0.7814   0.5910   0.6705   0.6228
mirna_only        0.7461     0.7760   0.5466   0.6114   0.5749
gene+meth         0.7565     0.8852   0.8272   0.8021   0.8114
gene+mirna        0.8676     0.8852   0.8311   0.7738   0.7937
all               0.7837     0.7869   0.6455   0.7056   0.6673
==========================================================================

##############################################################################
##  📊 ABLATION — 5-FOLD CROSS-VALIDATED SUMMARY
##############################################################################

Config            Fold 1   Fold 2   Fold 3   Fold 4   Fold 5     Mean      Std
-----------------------------------------------------------------------------------
gene_only         0.7756   0.7786   0.7588   0.6875   0.8300   0.7661   0.0459
meth_only         0.7763   0.7765   0.6777   0.7800   0.6228   0.7267   0.0648
mirna_only        0.6434   0.7179   0.5387   0.6469   0.5749   0.6244   0.0623
gene+meth         0.8024   0.8424   0.7528   0.7964   0.8114   0.8011   0.0289
gene+mirna        0.7794   0.7927   0.7201   0.6866   0.7937   0.7545   0.0434
all               0.8072   0.8799   0.7298   0.7941   0.6673   0.7757   0.0722

==========================================================================
Config                Val F1     Test Acc       Test P       Test R      Test F1
--------------------------------------------------------------------------
gene_only        0.808±0.057  0.872±0.012  0.780±0.064  0.775±0.045  0.766±0.046
meth_only        0.772±0.069  0.859±0.039  0.738±0.107  0.744±0.055  0.727±0.065
mirna_only       0.634±0.079  0.768±0.045  0.621±0.070  0.652±0.067  0.624±0.062
gene+meth        0.803±0.048  0.884±0.010  0.822±0.048  0.806±0.041  0.801±0.029
gene+mirna       0.826±0.055  0.872±0.022  0.777±0.077  0.756±0.034  0.754±0.043
all              0.809±0.046  0.869±0.043  0.795±0.094  0.785±0.065  0.776±0.072
==========================================================================