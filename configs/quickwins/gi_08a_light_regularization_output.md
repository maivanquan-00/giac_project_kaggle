📁 Output root: results/gi_08a_light_regularization_multiseed_20260508_061920
🌱 Seeds: [42]
⚙️  Config: configs/quickwins/gi_08a_light_regularization.yaml

============================================================
  Running seed=42  (1/1)
============================================================
$ /usr/bin/python3 -u train.py --config configs/quickwins/gi_08a_light_regularization.yaml --seed 42 --save-dir results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-scatter'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_scatter/_scatter_cuda.so
  import torch_geometric.typing
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-sparse'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_sparse/_spmm_cuda.so
  import torch_geometric.typing
🔧 Override seed = 42
🔧 Override save_dir = results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints
🖥️  Device: cuda  |  Seed: 42
📂 Loading data từ: /kaggle/input/datasets/maivanquan/datn-2025-2/data_final
  Labels : (917, 3)
  Gene   : (917, 19930)
  Meth   : (917, 23111)
  miRNA  : (917, 1881)

  Samples sau align : 917
  Filter cancer_types=['COAD', 'ESCA', 'READ', 'STAD']: 917 samples
  Phân bố subtype   : {np.int64(0): np.int64(624), np.int64(1): np.int64(108), np.int64(2): np.int64(136), np.int64(3): np.int64(19), np.int64(4): np.int64(30)}
  Phân bố cancer_type: {'COAD': np.int64(340), 'ESCA': np.int64(79), 'READ': np.int64(118), 'STAD': np.int64(380)}

📐 Fold 1: gene=3614, meth=3758, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3614
   CpG   nodes : 3758
   miRNA nodes : 1881
   Parsing emQTL COAD... 13,385 edges
   Parsing emQTL ESCA... 2,681 edges
   Parsing emQTL READ... 13 edges
   Parsing emQTL STAD... 9,580 edges
   CpG→Gene edges  : 25,659
   Building ENSP→symbol map từ alias file... 3,711 proteins mapped
   Parsing STRING links... 16,322 unique edges
   Gene↔Gene edges : 32,644
   Parsing hsa_MTI.csv... 145,709 edges
   miRNA→Gene edges: 145,709
   Gene-Pathway edges : 15,459 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,336 edges
   CpG↔miRNA edges : 18,336
⚖️  Using computed focal_alpha: [0.0767, 0.4455, 0.3497, 2.5018, 1.6262]

🧠 Fold 1 params: 831,048
🚀 Training Fold 1...  scheduler=onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.0851  P=0.1482  R=0.3286  F1=0.1038  F1w=0.0513
[Val  ] Acc=0.1091  P=0.1068  R=0.4019  F1=0.1515  F1w=0.0590
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.2980
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.1429  P=0.2789  R=0.3443  F1=0.1543  F1w=0.1179
[Val  ] Acc=0.1091  P=0.2086  R=0.3202  F1=0.1827  F1w=0.0674
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.2860
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.3291  P=0.3432  R=0.4881  F1=0.3107  F1w=0.3692
[Val  ] Acc=0.4364  P=0.3944  R=0.4012  F1=0.3519  F1w=0.4857
       modality_w: cpg=0.503 mirna=0.497  |  val_loss=0.2647
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.4992  P=0.4375  R=0.5422  F1=0.4422  F1w=0.5587
[Val  ] Acc=0.5000  P=0.4110  R=0.4367  F1=0.4015  F1w=0.5544
       modality_w: cpg=0.504 mirna=0.496  |  val_loss=0.2479
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.6019  P=0.5091  R=0.6452  F1=0.5312  F1w=0.6486
[Val  ] Acc=0.7545  P=0.5797  R=0.6107  F1=0.5909  F1w=0.7721
       modality_w: cpg=0.507 mirna=0.493  |  val_loss=0.2014
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.7512  P=0.5794  R=0.6983  F1=0.6186  F1w=0.7723
[Val  ] Acc=0.7000  P=0.5779  R=0.6468  F1=0.5933  F1w=0.7320
       modality_w: cpg=0.511 mirna=0.489  |  val_loss=0.2011
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.7608  P=0.6484  R=0.8266  F1=0.6945  F1w=0.7843
[Val  ] Acc=0.8000  P=0.6458  R=0.6409  F1=0.6408  F1w=0.8113
       modality_w: cpg=0.513 mirna=0.487  |  val_loss=0.2184
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.8026  P=0.6914  R=0.8847  F1=0.7451  F1w=0.8209
[Val  ] Acc=0.8545  P=0.6831  R=0.6765  F1=0.6796  F1w=0.8530
       modality_w: cpg=0.516 mirna=0.484  |  val_loss=0.2147
Fold 1 | Epoch  40/150
[Train] Acc=0.8796  P=0.8014  R=0.9127  F1=0.8458  F1w=0.8873
[Val  ] Acc=0.8545  P=0.6767  R=0.6736  F1=0.6727  F1w=0.8490
       modality_w: cpg=0.519 mirna=0.481  |  val_loss=0.2327
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  45/150
[Train] Acc=0.9149  P=0.8606  R=0.9237  F1=0.8878  F1w=0.9188
[Val  ] Acc=0.8545  P=0.6757  R=0.6638  F1=0.6677  F1w=0.8493
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.2368
Fold 1 | Epoch  50/150
[Train] Acc=0.9133  P=0.8677  R=0.9609  F1=0.9059  F1w=0.9187
[Val  ] Acc=0.8727  P=0.7029  R=0.7171  F1=0.7096  F1w=0.8777
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.2321
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  55/150
[Train] Acc=0.9438  P=0.9146  R=0.9699  F1=0.9395  F1w=0.9460
[Val  ] Acc=0.8727  P=0.7238  R=0.6535  F1=0.6663  F1w=0.8553
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.3148
Fold 1 | Epoch  60/150
[Train] Acc=0.9518  P=0.8871  R=0.9774  F1=0.9264  F1w=0.9538
[Val  ] Acc=0.8909  P=0.7182  R=0.6843  F1=0.6940  F1w=0.8784
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.3081
Fold 1 | Epoch  65/150
[Train] Acc=0.9775  P=0.9463  R=0.9894  F1=0.9663  F1w=0.9780
[Val  ] Acc=0.8909  P=0.7644  R=0.6589  F1=0.6742  F1w=0.8677
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.3339
Fold 1 | Epoch  70/150
[Train] Acc=0.9759  P=0.9532  R=0.9907  F1=0.9704  F1w=0.9767
[Val  ] Acc=0.8909  P=0.7063  R=0.6999  F1=0.7020  F1w=0.8843
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.3597
⏹️  Early stopping at epoch 72 (Fold 1)

📊 Test - Fold 1
[Test ] Acc=0.8370  P=0.7392  R=0.7812  F1=0.7576  F1w=0.8398
✅ Best val F1: 0.7320  |  Best val loss: 0.1729
✅ Test F1:     0.7576

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9000    0.8640    0.8816       125
          GS     0.5926    0.7273    0.6531        22
         MSI     0.8462    0.8148    0.8302        27
      HM-SNV     0.5000    0.5000    0.5000         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8370       184
   macro avg     0.7392    0.7812    0.7576       184
weighted avg     0.8453    0.8370    0.8398       184


🎯 Per-class F1 - Fold 1
   0:CIN       F1=0.8816
   1:GS        F1=0.6531
   2:MSI       F1=0.8302
   3:HM-SNV    F1=0.5000
   4:EBV       F1=0.9231
  📄 Confusion matrix (absolute) saved: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 1
   cpg  : std=0.0561  max=0.2582  nnz=0.762  global_w=0.522
   mirna: std=0.0891  max=0.4628  nnz=0.564  global_w=0.478

🧬 Per-cancer-type F1 - Fold 1
     Cancer      N      F1
       COAD     61  0.8814
       ESCA     20  0.3829
       READ     25  0.9103
       STAD     78  0.6296

📐 Fold 2: gene=3636, meth=3783, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3636
   CpG   nodes : 3783
   miRNA nodes : 1881
   Parsing emQTL COAD... 12,495 edges
   Parsing emQTL ESCA... 2,372 edges
   Parsing emQTL READ... 14 edges
   Parsing emQTL STAD... 9,519 edges
   CpG→Gene edges  : 24,400
   Building ENSP→symbol map từ alias file... 3,735 proteins mapped
   Parsing STRING links... 14,364 unique edges
   Gene↔Gene edges : 28,728
   Parsing hsa_MTI.csv... 145,537 edges
   miRNA→Gene edges: 145,537
   Gene-Pathway edges : 15,149 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,232 edges
   CpG↔miRNA edges : 18,232
⚖️  Using computed focal_alpha: [0.0767, 0.4455, 0.3497, 2.5018, 1.6262]

🧠 Fold 2 params: 834,056
🚀 Training Fold 2...  scheduler=onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.1316  P=0.2152  R=0.2161  F1=0.0872  F1w=0.0853
[Val  ] Acc=0.1273  P=0.1180  R=0.2344  F1=0.1029  F1w=0.0621
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3043
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.2568  P=0.2444  R=0.3304  F1=0.1952  F1w=0.2768
[Val  ] Acc=0.5182  P=0.2423  R=0.4176  F1=0.2631  F1w=0.5284
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.2821
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.3900  P=0.3523  R=0.4394  F1=0.3059  F1w=0.4233
[Val  ] Acc=0.5455  P=0.3939  R=0.4707  F1=0.3241  F1w=0.5695
       modality_w: cpg=0.502 mirna=0.498  |  val_loss=0.2401
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.4960  P=0.3994  R=0.5243  F1=0.4115  F1w=0.5262
[Val  ] Acc=0.6182  P=0.4229  R=0.5187  F1=0.4165  F1w=0.6474
       modality_w: cpg=0.506 mirna=0.494  |  val_loss=0.2051
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.6308  P=0.4920  R=0.6139  F1=0.5270  F1w=0.6579
[Val  ] Acc=0.7273  P=0.4705  R=0.5398  F1=0.4940  F1w=0.7331
       modality_w: cpg=0.506 mirna=0.494  |  val_loss=0.2161
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.6950  P=0.6185  R=0.7612  F1=0.6543  F1w=0.7222
[Val  ] Acc=0.8000  P=0.5640  R=0.6281  F1=0.5836  F1w=0.8026
       modality_w: cpg=0.509 mirna=0.491  |  val_loss=0.1716
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.7239  P=0.6481  R=0.7895  F1=0.6906  F1w=0.7458
[Val  ] Acc=0.7818  P=0.5794  R=0.6009  F1=0.5877  F1w=0.7961
       modality_w: cpg=0.510 mirna=0.490  |  val_loss=0.2602
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.8250  P=0.7445  R=0.8619  F1=0.7895  F1w=0.8373
[Val  ] Acc=0.8091  P=0.6128  R=0.6343  F1=0.6208  F1w=0.8208
       modality_w: cpg=0.510 mirna=0.490  |  val_loss=0.2411
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  40/150
[Train] Acc=0.8507  P=0.7600  R=0.8773  F1=0.8008  F1w=0.8624
[Val  ] Acc=0.8273  P=0.7057  R=0.7214  F1=0.6930  F1w=0.8401
       modality_w: cpg=0.511 mirna=0.489  |  val_loss=0.2197
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  45/150
[Train] Acc=0.8780  P=0.8317  R=0.9398  F1=0.8742  F1w=0.8870
[Val  ] Acc=0.8273  P=0.6170  R=0.6397  F1=0.6233  F1w=0.8387
       modality_w: cpg=0.513 mirna=0.487  |  val_loss=0.2705
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  50/150
[Train] Acc=0.9101  P=0.8367  R=0.9434  F1=0.8821  F1w=0.9144
[Val  ] Acc=0.8000  P=0.6845  R=0.7163  F1=0.6741  F1w=0.8218
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.2922
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  55/150
[Train] Acc=0.9278  P=0.8989  R=0.9579  F1=0.9243  F1w=0.9309
[Val  ] Acc=0.8182  P=0.6908  R=0.6991  F1=0.6936  F1w=0.8223
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.2936
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  60/150
[Train] Acc=0.9454  P=0.9373  R=0.9664  F1=0.9498  F1w=0.9477
[Val  ] Acc=0.8455  P=0.7174  R=0.7493  F1=0.7151  F1w=0.8575
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.2868
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  65/150
[Train] Acc=0.9454  P=0.9053  R=0.9687  F1=0.9333  F1w=0.9472
[Val  ] Acc=0.8364  P=0.7150  R=0.7044  F1=0.6941  F1w=0.8472
       modality_w: cpg=0.513 mirna=0.487  |  val_loss=0.2819
Fold 2 | Epoch  70/150
[Train] Acc=0.9486  P=0.9075  R=0.9719  F1=0.9363  F1w=0.9508
[Val  ] Acc=0.8455  P=0.7211  R=0.7395  F1=0.7113  F1w=0.8593
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.3070
Fold 2 | Epoch  75/150
[Train] Acc=0.9695  P=0.9488  R=0.9842  F1=0.9653  F1w=0.9703
[Val  ] Acc=0.8364  P=0.6636  R=0.6198  F1=0.6352  F1w=0.8450
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.3815
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  80/150
[Train] Acc=0.9839  P=0.9685  R=0.9804  F1=0.9734  F1w=0.9843
[Val  ] Acc=0.8091  P=0.6859  R=0.6866  F1=0.6631  F1w=0.8235
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.3389
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  85/150
[Train] Acc=0.9791  P=0.9570  R=0.9899  F1=0.9725  F1w=0.9795
[Val  ] Acc=0.8636  P=0.7408  R=0.7321  F1=0.7190  F1w=0.8736
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3661
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  90/150
[Train] Acc=0.9920  P=0.9883  R=0.9931  F1=0.9906  F1w=0.9920
[Val  ] Acc=0.8636  P=0.7398  R=0.7321  F1=0.7153  F1w=0.8742
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3433
Fold 2 | Epoch  95/150
[Train] Acc=0.9952  P=0.9947  R=0.9868  F1=0.9906  F1w=0.9952
[Val  ] Acc=0.8545  P=0.7265  R=0.7196  F1=0.7057  F1w=0.8639
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3558
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch 100/150
[Train] Acc=0.9920  P=0.9753  R=0.9881  F1=0.9812  F1w=0.9921
[Val  ] Acc=0.8545  P=0.7265  R=0.7196  F1=0.7057  F1w=0.8639
       modality_w: cpg=0.516 mirna=0.484  |  val_loss=0.3738
Fold 2 | Epoch 105/150
[Train] Acc=0.9984  P=0.9995  R=0.9973  F1=0.9984  F1w=0.9984
[Val  ] Acc=0.8182  P=0.6914  R=0.7060  F1=0.6782  F1w=0.8314
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3760
Fold 2 | Epoch 110/150
[Train] Acc=0.9952  P=0.9941  R=0.9963  F1=0.9952  F1w=0.9952
[Val  ] Acc=0.8455  P=0.7175  R=0.7267  F1=0.7018  F1w=0.8572
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3721
Fold 2 | Epoch 115/150
[Train] Acc=0.9984  P=0.9973  R=0.9995  F1=0.9984  F1w=0.9984
[Val  ] Acc=0.8636  P=0.7487  R=0.7321  F1=0.7335  F1w=0.8657
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3594
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch 120/150
[Train] Acc=0.9952  P=0.9921  R=0.9986  F1=0.9953  F1w=0.9952
[Val  ] Acc=0.8636  P=0.7437  R=0.7321  F1=0.7258  F1w=0.8686
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3598
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch 125/150
[Train] Acc=0.9984  P=0.9973  R=0.9995  F1=0.9984  F1w=0.9984
[Val  ] Acc=0.8545  P=0.7335  R=0.7294  F1=0.7148  F1w=0.8628
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3629
Fold 2 | Epoch 130/150
[Train] Acc=0.9984  P=0.9973  R=0.9995  F1=0.9984  F1w=0.9984
[Val  ] Acc=0.8636  P=0.7437  R=0.7321  F1=0.7258  F1w=0.8686
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3645
Fold 2 | Epoch 135/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000  F1w=1.0000
[Val  ] Acc=0.8636  P=0.7437  R=0.7321  F1=0.7258  F1w=0.8686
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3654
Fold 2 | Epoch 140/150
[Train] Acc=0.9984  P=0.9995  R=0.9973  F1=0.9984  F1w=0.9984
[Val  ] Acc=0.8636  P=0.7437  R=0.7321  F1=0.7258  F1w=0.8686
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3681
⏹️  Early stopping at epoch 141 (Fold 2)

📊 Test - Fold 2
[Test ] Acc=0.9185  P=0.6858  R=0.7483  F1=0.7142  F1w=0.9108
✅ Best val F1: 0.7406  |  Best val loss: 0.1716
✅ Test F1:     0.7142

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9754    0.9520    0.9636       125
          GS     0.7037    0.8636    0.7755        22
         MSI     0.8929    0.9259    0.9091        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.9185       184
   macro avg     0.6858    0.7483    0.7142       184
weighted avg     0.9057    0.9185    0.9108       184


🎯 Per-class F1 - Fold 2
   0:CIN       F1=0.9636
   1:GS        F1=0.7755
   2:MSI       F1=0.9091
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.9231
  📄 Confusion matrix (absolute) saved: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 2
   cpg  : std=0.0503  max=0.2347  nnz=0.847  global_w=0.515
   mirna: std=0.0932  max=0.4843  nnz=0.587  global_w=0.485

🧬 Per-cancer-type F1 - Fold 2
     Cancer      N      F1
       COAD     68  0.6075
       ESCA     19  0.4865
       READ     25  0.6000
       STAD     72  0.7524

📐 Fold 3: gene=3613, meth=3765, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3613
   CpG   nodes : 3765
   miRNA nodes : 1881
   Parsing emQTL COAD... 11,940 edges
   Parsing emQTL ESCA... 2,499 edges
   Parsing emQTL READ... 6 edges
   Parsing emQTL STAD... 9,750 edges
   CpG→Gene edges  : 24,195
   Building ENSP→symbol map từ alias file... 3,728 proteins mapped
   Parsing STRING links... 15,591 unique edges
   Gene↔Gene edges : 31,182
   Parsing hsa_MTI.csv... 145,988 edges
   miRNA→Gene edges: 145,988
   Gene-Pathway edges : 15,330 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,313 edges
   CpG↔miRNA edges : 18,313
⚖️  Using computed focal_alpha: [0.0798, 0.456, 0.3668, 2.4103, 1.6872]

🧠 Fold 3 params: 831,432
🚀 Training Fold 3...  scheduler=onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.3708  P=0.2248  R=0.2261  F1=0.2024  F1w=0.4340
[Val  ] Acc=0.4775  P=0.1826  R=0.1967  F1=0.1692  F1w=0.4962
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3143
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.4222  P=0.2540  R=0.2878  F1=0.2456  F1w=0.4735
[Val  ] Acc=0.5135  P=0.2851  R=0.3175  F1=0.2877  F1w=0.5533
       modality_w: cpg=0.499 mirna=0.501  |  val_loss=0.2874
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.5393  P=0.3556  R=0.4386  F1=0.3709  F1w=0.5732
[Val  ] Acc=0.5856  P=0.3411  R=0.3888  F1=0.3539  F1w=0.6121
       modality_w: cpg=0.505 mirna=0.495  |  val_loss=0.2466
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.6260  P=0.4940  R=0.6410  F1=0.5276  F1w=0.6589
[Val  ] Acc=0.5856  P=0.4039  R=0.5189  F1=0.4276  F1w=0.6169
       modality_w: cpg=0.510 mirna=0.490  |  val_loss=0.1781
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.5875  P=0.4948  R=0.6723  F1=0.5262  F1w=0.6234
[Val  ] Acc=0.6306  P=0.5285  R=0.6069  F1=0.5453  F1w=0.6654
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.1505
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.6709  P=0.6147  R=0.7892  F1=0.6506  F1w=0.7029
[Val  ] Acc=0.6577  P=0.6471  R=0.7278  F1=0.6226  F1w=0.7169
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.1391
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.7673  P=0.6919  R=0.8668  F1=0.7456  F1w=0.7883
[Val  ] Acc=0.7387  P=0.6625  R=0.7436  F1=0.6516  F1w=0.7786
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.1331
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.7801  P=0.6818  R=0.8878  F1=0.7338  F1w=0.8025
[Val  ] Acc=0.7568  P=0.6104  R=0.6375  F1=0.5942  F1w=0.7877
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.1606
Fold 3 | Epoch  40/150
[Train] Acc=0.8347  P=0.7676  R=0.8868  F1=0.8100  F1w=0.8500
[Val  ] Acc=0.7928  P=0.6491  R=0.7524  F1=0.6702  F1w=0.8149
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.1237
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  45/150
[Train] Acc=0.8796  P=0.8228  R=0.9312  F1=0.8642  F1w=0.8891
[Val  ] Acc=0.8378  P=0.6770  R=0.7655  F1=0.6954  F1w=0.8567
       modality_w: cpg=0.516 mirna=0.484  |  val_loss=0.0918
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  50/150
[Train] Acc=0.9278  P=0.8714  R=0.9587  F1=0.9072  F1w=0.9322
[Val  ] Acc=0.8288  P=0.6086  R=0.6932  F1=0.6320  F1w=0.8453
       modality_w: cpg=0.518 mirna=0.482  |  val_loss=0.0992
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  55/150
[Train] Acc=0.9438  P=0.9086  R=0.9790  F1=0.9386  F1w=0.9469
[Val  ] Acc=0.8739  P=0.7781  R=0.8912  F1=0.7841  F1w=0.8858
       modality_w: cpg=0.519 mirna=0.481  |  val_loss=0.0828
Fold 3 | Epoch  60/150
[Train] Acc=0.9470  P=0.9191  R=0.9760  F1=0.9435  F1w=0.9499
[Val  ] Acc=0.8108  P=0.7172  R=0.7696  F1=0.7095  F1w=0.8462
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.1116
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  65/150
[Train] Acc=0.9518  P=0.9019  R=0.9858  F1=0.9384  F1w=0.9539
[Val  ] Acc=0.8919  P=0.7553  R=0.8159  F1=0.7753  F1w=0.8995
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.1072
Fold 3 | Epoch  70/150
[Train] Acc=0.9631  P=0.9379  R=0.9731  F1=0.9526  F1w=0.9644
[Val  ] Acc=0.8829  P=0.7838  R=0.9037  F1=0.7975  F1w=0.8948
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.0643
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  75/150
[Train] Acc=0.9791  P=0.9416  R=0.9800  F1=0.9599  F1w=0.9795
[Val  ] Acc=0.9099  P=0.7919  R=0.8311  F1=0.8071  F1w=0.9136
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.0783
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  80/150
[Train] Acc=0.9743  P=0.9540  R=0.9902  F1=0.9706  F1w=0.9751
[Val  ] Acc=0.9009  P=0.7818  R=0.8186  F1=0.7944  F1w=0.9052
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.1071
Fold 3 | Epoch  85/150
[Train] Acc=0.9823  P=0.9683  R=0.9931  F1=0.9799  F1w=0.9827
[Val  ] Acc=0.9279  P=0.8080  R=0.8363  F1=0.8198  F1w=0.9280
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.1294
Fold 3 | Epoch  90/150
[Train] Acc=0.9856  P=0.9661  R=0.9935  F1=0.9792  F1w=0.9858
[Val  ] Acc=0.8829  P=0.7523  R=0.8162  F1=0.7653  F1w=0.8939
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.0737
Fold 3 | Epoch  95/150
[Train] Acc=0.9872  P=0.9820  R=0.9940  F1=0.9877  F1w=0.9874
[Val  ] Acc=0.9189  P=0.7912  R=0.8465  F1=0.8145  F1w=0.9207
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.0903
⏹️  Early stopping at epoch 99 (Fold 3)

📊 Test - Fold 3
[Test ] Acc=0.8361  P=0.6713  R=0.6316  F1=0.6498  F1w=0.8409
✅ Best val F1: 0.8782  |  Best val loss: 0.0588
✅ Test F1:     0.6498

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.8960    0.8960    0.8960       125
          GS     0.5714    0.5714    0.5714        21
         MSI     0.8889    0.8571    0.8727        28
      HM-SNV     0.0000    0.0000    0.0000         3
         EBV     1.0000    0.8333    0.9091         6

    accuracy                         0.8361       183
   macro avg     0.6713    0.6316    0.6498       183
weighted avg     0.8464    0.8361    0.8409       183


🎯 Per-class F1 - Fold 3
   0:CIN       F1=0.8960
   1:GS        F1=0.5714
   2:MSI       F1=0.8727
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.9091
  📄 Confusion matrix (absolute) saved: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 3
   cpg  : std=0.0642  max=0.3035  nnz=0.678  global_w=0.521
   mirna: std=0.0875  max=0.4421  nnz=0.557  global_w=0.479

🧬 Per-cancer-type F1 - Fold 3
     Cancer      N      F1
       COAD     74  0.5802
       ESCA      9  0.4706
       READ     20  1.0000
       STAD     80  0.6467

📐 Fold 4: gene=3629, meth=3772, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3629
   CpG   nodes : 3772
   miRNA nodes : 1881
   Parsing emQTL COAD... 13,108 edges
   Parsing emQTL ESCA... 2,427 edges
   Parsing emQTL READ... 17 edges
   Parsing emQTL STAD... 10,070 edges
   CpG→Gene edges  : 25,622
   Building ENSP→symbol map từ alias file... 3,721 proteins mapped
   Parsing STRING links... 14,884 unique edges
   Gene↔Gene edges : 29,768
   Parsing hsa_MTI.csv... 145,941 edges
   miRNA→Gene edges: 145,941
   Gene-Pathway edges : 15,749 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,352 edges
   CpG↔miRNA edges : 18,352
⚖️  Using computed focal_alpha: [0.0767, 0.4397, 0.3537, 2.503, 1.6269]

🧠 Fold 4 params: 832,904
🚀 Training Fold 4...  scheduler=onecycle
Fold 4 | Epoch   1/150
[Train] Acc=0.0899  P=0.1933  R=0.1756  F1=0.0976  F1w=0.1073
[Val  ] Acc=0.0270  P=0.1467  R=0.0298  F1=0.0369  F1w=0.0392
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3284
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.1091  P=0.2159  R=0.2271  F1=0.1123  F1w=0.1197
[Val  ] Acc=0.0991  P=0.2630  R=0.1694  F1=0.0943  F1w=0.0717
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3231
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.2488  P=0.2857  R=0.3221  F1=0.2123  F1w=0.2992
[Val  ] Acc=0.3063  P=0.2913  R=0.3836  F1=0.2486  F1w=0.3468
       modality_w: cpg=0.501 mirna=0.499  |  val_loss=0.2935
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.5313  P=0.3969  R=0.5255  F1=0.4072  F1w=0.5803
[Val  ] Acc=0.5225  P=0.3799  R=0.4239  F1=0.3643  F1w=0.5803
       modality_w: cpg=0.506 mirna=0.494  |  val_loss=0.2486
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.6693  P=0.5325  R=0.6956  F1=0.5706  F1w=0.7047
[Val  ] Acc=0.7207  P=0.4817  R=0.5954  F1=0.5074  F1w=0.7428
       modality_w: cpg=0.509 mirna=0.491  |  val_loss=0.2434
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.7223  P=0.5939  R=0.7788  F1=0.6466  F1w=0.7494
[Val  ] Acc=0.7027  P=0.4967  R=0.6264  F1=0.5378  F1w=0.7240
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.2409
Fold 4 | Epoch  30/150
[Train] Acc=0.8010  P=0.7322  R=0.8967  F1=0.7864  F1w=0.8210
[Val  ] Acc=0.8108  P=0.6454  R=0.6621  F1=0.6503  F1w=0.8212
       modality_w: cpg=0.517 mirna=0.483  |  val_loss=0.3106
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.8652  P=0.7908  R=0.8823  F1=0.8249  F1w=0.8767
[Val  ] Acc=0.8198  P=0.6181  R=0.6647  F1=0.6376  F1w=0.8270
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.3542
Fold 4 | Epoch  40/150
[Train] Acc=0.8604  P=0.7934  R=0.9098  F1=0.8364  F1w=0.8723
[Val  ] Acc=0.8198  P=0.6511  R=0.6174  F1=0.6272  F1w=0.8347
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.3695
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  45/150
[Train] Acc=0.9149  P=0.8588  R=0.9638  F1=0.9028  F1w=0.9197
[Val  ] Acc=0.8108  P=0.5879  R=0.6803  F1=0.6238  F1w=0.8252
       modality_w: cpg=0.529 mirna=0.471  |  val_loss=0.4045
Fold 4 | Epoch  50/150
[Train] Acc=0.9085  P=0.8292  R=0.9536  F1=0.8798  F1w=0.9139
[Val  ] Acc=0.8198  P=0.6257  R=0.6957  F1=0.6541  F1w=0.8331
       modality_w: cpg=0.531 mirna=0.469  |  val_loss=0.4177
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  55/150
[Train] Acc=0.9518  P=0.9350  R=0.9724  F1=0.9497  F1w=0.9545
[Val  ] Acc=0.8108  P=0.6395  R=0.6548  F1=0.6457  F1w=0.8270
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.4860
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  60/150
[Train] Acc=0.9647  P=0.9361  R=0.9829  F1=0.9577  F1w=0.9658
[Val  ] Acc=0.8378  P=0.6708  R=0.6919  F1=0.6786  F1w=0.8502
       modality_w: cpg=0.533 mirna=0.467  |  val_loss=0.4576
Fold 4 | Epoch  65/150
[Train] Acc=0.9759  P=0.9538  R=0.9812  F1=0.9666  F1w=0.9764
[Val  ] Acc=0.8468  P=0.6706  R=0.7127  F1=0.6871  F1w=0.8568
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.4406
Fold 4 | Epoch  70/150
[Train] Acc=0.9807  P=0.9598  R=0.9926  F1=0.9750  F1w=0.9813
[Val  ] Acc=0.8559  P=0.6369  R=0.7154  F1=0.6709  F1w=0.8589
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.4799
Fold 4 | Epoch  75/150
[Train] Acc=0.9856  P=0.9710  R=0.9941  F1=0.9819  F1w=0.9858
[Val  ] Acc=0.8739  P=0.7037  R=0.7335  F1=0.7170  F1w=0.8793
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.4848
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  80/150
[Train] Acc=0.9872  P=0.9685  R=0.9940  F1=0.9807  F1w=0.9873
[Val  ] Acc=0.8559  P=0.6668  R=0.7063  F1=0.6833  F1w=0.8611
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.4980
Fold 4 | Epoch  85/150
[Train] Acc=0.9936  P=0.9786  R=0.9959  F1=0.9868  F1w=0.9936
[Val  ] Acc=0.8378  P=0.6663  R=0.6883  F1=0.6758  F1w=0.8489
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.5444
Fold 4 | Epoch  90/150
[Train] Acc=0.9920  P=0.9821  R=0.9954  F1=0.9886  F1w=0.9920
[Val  ] Acc=0.8649  P=0.6846  R=0.7217  F1=0.7002  F1w=0.8683
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.5390
Fold 4 | Epoch  95/150
[Train] Acc=0.9968  P=0.9947  R=0.9991  F1=0.9969  F1w=0.9968
[Val  ] Acc=0.8468  P=0.6687  R=0.7127  F1=0.6866  F1w=0.8556
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.5200
⏹️  Early stopping at epoch 95 (Fold 4)

📊 Test - Fold 4
[Test ] Acc=0.8251  P=0.6565  R=0.6548  F1=0.6549  F1w=0.8303
✅ Best val F1: 0.7170  |  Best val loss: 0.2045
✅ Test F1:     0.6549

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9024    0.8880    0.8952       125
          GS     0.5000    0.5714    0.5333        21
         MSI     0.8800    0.8148    0.8462        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8251       183
   macro avg     0.6565    0.6548    0.6549       183
weighted avg     0.8364    0.8251    0.8303       183


🎯 Per-class F1 - Fold 4
   0:CIN       F1=0.8952
   1:GS        F1=0.5333
   2:MSI       F1=0.8462
   3:HM-SNV    F1=0.0000
   4:EBV       F1=1.0000
  📄 Confusion matrix (absolute) saved: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 4
   cpg  : std=0.0681  max=0.3253  nnz=0.630  global_w=0.535
   mirna: std=0.0796  max=0.4012  nnz=0.646  global_w=0.465

🧬 Per-cancer-type F1 - Fold 4
     Cancer      N      F1
       COAD     61  0.6169
       ESCA     12  0.2143
       READ     31  0.6119
       STAD     79  0.6108

📐 Fold 5: gene=3632, meth=3776, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3632
   CpG   nodes : 3776
   miRNA nodes : 1881
   Parsing emQTL COAD... 12,951 edges
   Parsing emQTL ESCA... 2,600 edges
   Parsing emQTL READ... 10 edges
   Parsing emQTL STAD... 9,796 edges
   CpG→Gene edges  : 25,357
   Building ENSP→symbol map từ alias file... 3,736 proteins mapped
   Parsing STRING links... 14,268 unique edges
   Gene↔Gene edges : 28,536
   Parsing hsa_MTI.csv... 145,352 edges
   miRNA→Gene edges: 145,352
   Gene-Pathway edges : 15,276 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,380 edges
   CpG↔miRNA edges : 18,380
⚖️  Using computed focal_alpha: [0.0767, 0.4455, 0.3497, 2.5018, 1.6262]

🧠 Fold 5 params: 833,352
🚀 Training Fold 5...  scheduler=onecycle
Fold 5 | Epoch   1/150
[Train] Acc=0.1589  P=0.1965  R=0.1776  F1=0.1221  F1w=0.1898
[Val  ] Acc=0.2342  P=0.2089  R=0.2395  F1=0.1681  F1w=0.2395
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3053
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.2584  P=0.2431  R=0.2982  F1=0.2047  F1w=0.2838
[Val  ] Acc=0.3784  P=0.2453  R=0.3141  F1=0.2270  F1w=0.3937
       modality_w: cpg=0.501 mirna=0.499  |  val_loss=0.2953
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.4093  P=0.3108  R=0.4113  F1=0.3071  F1w=0.4548
[Val  ] Acc=0.5315  P=0.3871  R=0.5298  F1=0.3975  F1w=0.5622
       modality_w: cpg=0.504 mirna=0.496  |  val_loss=0.2576
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.5795  P=0.4189  R=0.5412  F1=0.4450  F1w=0.6184
[Val  ] Acc=0.6036  P=0.4583  R=0.5143  F1=0.4483  F1w=0.6492
       modality_w: cpg=0.508 mirna=0.492  |  val_loss=0.2095
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.6372  P=0.5261  R=0.6823  F1=0.5635  F1w=0.6707
[Val  ] Acc=0.7207  P=0.5424  R=0.5851  F1=0.5561  F1w=0.7362
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.1968
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.6902  P=0.5870  R=0.7630  F1=0.6253  F1w=0.7155
[Val  ] Acc=0.7297  P=0.5550  R=0.5935  F1=0.5592  F1w=0.7588
       modality_w: cpg=0.516 mirna=0.484  |  val_loss=0.2377
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  30/150
[Train] Acc=0.7945  P=0.6666  R=0.8444  F1=0.7241  F1w=0.8105
[Val  ] Acc=0.7838  P=0.6126  R=0.6220  F1=0.6080  F1w=0.8039
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.2294
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  35/150
[Train] Acc=0.8315  P=0.7223  R=0.8845  F1=0.7755  F1w=0.8432
[Val  ] Acc=0.8018  P=0.6123  R=0.6371  F1=0.6194  F1w=0.8190
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.2718
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  40/150
[Train] Acc=0.8716  P=0.8165  R=0.9209  F1=0.8532  F1w=0.8829
[Val  ] Acc=0.8468  P=0.6939  R=0.6700  F1=0.6812  F1w=0.8582
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.3105
  💾 Saved checkpoint: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  45/150
[Train] Acc=0.8925  P=0.8088  R=0.9508  F1=0.8642  F1w=0.8991
[Val  ] Acc=0.8468  P=0.6473  R=0.6799  F1=0.6613  F1w=0.8552
       modality_w: cpg=0.524 mirna=0.476  |  val_loss=0.2404
Fold 5 | Epoch  50/150
[Train] Acc=0.9342  P=0.8431  R=0.9744  F1=0.8973  F1w=0.9368
[Val  ] Acc=0.8198  P=0.6730  R=0.6424  F1=0.6540  F1w=0.8392
       modality_w: cpg=0.525 mirna=0.475  |  val_loss=0.3525
Fold 5 | Epoch  55/150
[Train] Acc=0.9486  P=0.9173  R=0.9598  F1=0.9358  F1w=0.9505
[Val  ] Acc=0.8198  P=0.6757  R=0.6424  F1=0.6524  F1w=0.8322
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.2973
Fold 5 | Epoch  60/150
[Train] Acc=0.9615  P=0.8906  R=0.9853  F1=0.9302  F1w=0.9630
[Val  ] Acc=0.8378  P=0.6765  R=0.6448  F1=0.6590  F1w=0.8481
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.3055
⏹️  Early stopping at epoch 60 (Fold 5)

📊 Test - Fold 5
[Test ] Acc=0.8197  P=0.6480  R=0.6651  F1=0.6479  F1w=0.8288
✅ Best val F1: 0.6812  |  Best val loss: 0.1882
✅ Test F1:     0.6479

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9217    0.8548    0.8870       124
          GS     0.6190    0.5909    0.6047        22
         MSI     0.7879    0.9630    0.8667        27
      HM-SNV     0.1111    0.2500    0.1538         4
         EBV     0.8000    0.6667    0.7273         6

    accuracy                         0.8197       183
   macro avg     0.6480    0.6651    0.6479       183
weighted avg     0.8439    0.8197    0.8288       183


🎯 Per-class F1 - Fold 5
   0:CIN       F1=0.8870
   1:GS        F1=0.6047
   2:MSI       F1=0.8667
   3:HM-SNV    F1=0.1538
   4:EBV       F1=0.7273
  📄 Confusion matrix (absolute) saved: results/gi_08a_light_regularization_multiseed_20260508_061920/seed_42/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 5
   cpg  : std=0.0657  max=0.2980  nnz=0.602  global_w=0.523
   mirna: std=0.0823  max=0.4065  nnz=0.568  global_w=0.477

🧬 Per-cancer-type F1 - Fold 5
     Cancer      N      F1
       COAD     76  0.6065
       ESCA     19  1.0000
       READ     17  0.4308
       STAD     71  0.6452

📈 5-fold CV summary
  ACCURACY   : mean=0.8473  std=0.0362
  PRECISION  : mean=0.6801  std=0.0322
  RECALL     : mean=0.6962  std=0.0580
  F1         : mean=0.6849  std=0.0439
  F1_WEIGHTED: mean=0.8501  std=0.0307

🧬 Per-cancer-type F1 (5-fold mean ± std):
    Cancer  N/fold   F1 mean   F1 std
      COAD    68.0    0.6585   0.1121
      ESCA    15.8    0.5108   0.2630
      READ    23.6    0.7106   0.2116
      STAD    76.0    0.6570   0.0494

🎯 Per-class F1 (5-fold mean ± std):
         Class   F1 mean   F1 std
             0    0.9047   0.0299
             1    0.6276   0.0838
             2    0.8650   0.0267
             3    0.1308   0.1940
             4    0.8965   0.0905

✅ Seed 42 done — F1 macro = 0.6849, F1 weighted = 0.8501



══════════════════════════════════════════════════════════════════════════════
 📋 COPY KHỐI BÊN DƯỚI (đến dòng ═ tiếp theo) → PASTE VÀO ĐẦU docs/RESULTS.md
══════════════════════════════════════════════════════════════════════════════

## [2026-05-08 06:51] `gi_08a_light_regularization` — Macro F1: **0.6849 ± 0.0000**

**Config:** `configs/quickwins/gi_08a_light_regularization.yaml`  |  **Seeds:** [42]  |  **N runs:** 1 × 5 folds

| Metric            | Mean ± Std      | Per-seed means |
| ----------------- | --------------- | -------------- |
| **Macro F1**      | 0.6849 ± 0.0000 | 0.6849         |
| Weighted F1       | 0.8501 ± 0.0000 | 0.8501         |
| Accuracy          | 0.8473 ± 0.0000 | 0.8473         |
| Precision (macro) | 0.6801 ± 0.0000 | 0.6801         |
| Recall (macro)    | 0.6962 ± 0.0000 | 0.6962         |

**Per-fold F1 (macro):**

| Seed | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean   |
| ---- | ------ | ------ | ------ | ------ | ------ | ------ |
| 42   | 0.7576 | 0.7142 | 0.6498 | 0.6549 | 0.6479 | 0.6849 |

**Per-class F1 (mean across seeds):**

| Class   | Seed 42 | Avg    |
| ------- | ------- | ------ |
| 0 (CIN) | 0.9047  | 0.9047 |

---

══════════════════════════════════════════════════════════════════════════════
 ↑↑↑ COPY KHỐI BÊN TRÊN — PASTE VÀO ĐẦU docs/RESULTS.md (sau dòng tiêu đề) ↑↑↑
══════════════════════════════════════════════════════════════════════════════

💾 JSON backup (KHÔNG cần download): results/gi_08a_light_regularization_multiseed_20260508_061920/multi_seed_summary.json