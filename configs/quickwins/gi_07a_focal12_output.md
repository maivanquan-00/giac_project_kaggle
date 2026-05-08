📁 Output root: results/gi_07a_focal12_multiseed_20260508_075456
🌱 Seeds: [42]
⚙️  Config: configs/quickwins/gi_07a_focal12.yaml

============================================================
  Running seed=42  (1/1)
============================================================
$ /usr/bin/python3 -u train.py --config configs/quickwins/gi_07a_focal12.yaml --seed 42 --save-dir results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-scatter'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_scatter/_scatter_cuda.so
  import torch_geometric.typing
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-sparse'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_sparse/_spmm_cuda.so
  import torch_geometric.typing
🔧 Override seed = 42
🔧 Override save_dir = results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints
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
   Gene-Pathway edges : 15,495 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,336 edges
   CpG↔miRNA edges : 18,336
✨ Using MANUAL focal_alpha from config: [1.0, 4.5, 1.5, 12.0, 2.0]

🧠 Fold 1 params: 831,048
🚀 Training Fold 1...  scheduler=onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.0803  P=0.1973  R=0.2211  F1=0.0905  F1w=0.0681
[Val  ] Acc=0.1000  P=0.1114  R=0.3173  F1=0.1430  F1w=0.0614
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=2.0395
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.1637  P=0.2301  R=0.2780  F1=0.1532  F1w=0.1823
[Val  ] Acc=0.3818  P=0.2739  R=0.2611  F1=0.2301  F1w=0.4111
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.7996
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.4831  P=0.2203  R=0.2399  F1=0.2131  F1w=0.5013
[Val  ] Acc=0.5909  P=0.1814  R=0.2369  F1=0.2037  F1w=0.5379
       modality_w: cpg=0.504 mirna=0.496  |  val_loss=1.6547
Fold 1 | Epoch  15/150
[Train] Acc=0.5891  P=0.3744  R=0.3248  F1=0.3262  F1w=0.6029
[Val  ] Acc=0.6636  P=0.2613  R=0.2554  F1=0.2449  F1w=0.6010
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=1.6168
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.5971  P=0.3932  R=0.4034  F1=0.3780  F1w=0.6257
[Val  ] Acc=0.7000  P=0.3390  R=0.3435  F1=0.3348  F1w=0.6721
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=1.5873
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.6597  P=0.5377  R=0.4613  F1=0.4461  F1w=0.6812
[Val  ] Acc=0.7545  P=0.3924  R=0.3861  F1=0.3882  F1w=0.7309
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=1.5308
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.7095  P=0.5801  R=0.6028  F1=0.5528  F1w=0.7410
[Val  ] Acc=0.7818  P=0.4067  R=0.4421  F1=0.4202  F1w=0.7694
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=1.5506
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.7978  P=0.6262  R=0.6625  F1=0.6376  F1w=0.8075
[Val  ] Acc=0.8273  P=0.6498  R=0.4970  F1=0.5277  F1w=0.8100
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=1.5680
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  40/150
[Train] Acc=0.8539  P=0.7113  R=0.7432  F1=0.7182  F1w=0.8595
[Val  ] Acc=0.7909  P=0.4348  R=0.4095  F1=0.4194  F1w=0.7681
       modality_w: cpg=0.540 mirna=0.460  |  val_loss=1.8201
Fold 1 | Epoch  45/150
[Train] Acc=0.8620  P=0.7072  R=0.7439  F1=0.7144  F1w=0.8681
[Val  ] Acc=0.8182  P=0.7140  R=0.5370  F1=0.5971  F1w=0.8027
       modality_w: cpg=0.540 mirna=0.460  |  val_loss=1.9697
Fold 1 | Epoch  50/150
[Train] Acc=0.8636  P=0.7289  R=0.7760  F1=0.7421  F1w=0.8705
[Val  ] Acc=0.7818  P=0.6546  R=0.4691  F1=0.5275  F1w=0.7611
       modality_w: cpg=0.539 mirna=0.461  |  val_loss=2.2312
Fold 1 | Epoch  55/150
[Train] Acc=0.8700  P=0.6931  R=0.7632  F1=0.7163  F1w=0.8772
[Val  ] Acc=0.7727  P=0.6516  R=0.3995  F1=0.4561  F1w=0.7414
       modality_w: cpg=0.538 mirna=0.462  |  val_loss=2.4002
⏹️  Early stopping at epoch 57 (Fold 1)

📊 Test - Fold 1
[Test ] Acc=0.7609  P=0.5723  R=0.4863  F1=0.5130  F1w=0.7468
✅ Best val F1: 0.6388  |  Best val loss: 1.4358
✅ Test F1:     0.5130

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.8116    0.8960    0.8517       125
          GS     0.5000    0.5909    0.5417        22
         MSI     0.8000    0.4444    0.5714        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     0.7500    0.5000    0.6000         6

    accuracy                         0.7609       184
   macro avg     0.5723    0.4863    0.5130       184
weighted avg     0.7530    0.7609    0.7468       184


🎯 Per-class F1 - Fold 1
   0:CIN       F1=0.8517
   1:GS        F1=0.5417
   2:MSI       F1=0.5714
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.6000
  📄 Confusion matrix (absolute) saved: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 1
   cpg  : std=0.0555  max=0.2589  nnz=0.760  global_w=0.537
   mirna: std=0.0969  max=0.4971  nnz=0.446  global_w=0.463

🧬 Per-cancer-type F1 - Fold 1
     Cancer      N      F1
       COAD     61  0.5372
       ESCA     20  0.4861
       READ     25  0.5464
       STAD     78  0.4818

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
   Gene-Pathway edges : 15,135 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,232 edges
   CpG↔miRNA edges : 18,232
✨ Using MANUAL focal_alpha from config: [1.0, 4.5, 1.5, 12.0, 2.0]

🧠 Fold 2 params: 834,056
🚀 Training Fold 2...  scheduler=onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.1220  P=0.2231  R=0.2517  F1=0.1093  F1w=0.1504
[Val  ] Acc=0.2000  P=0.1964  R=0.1223  F1=0.1185  F1w=0.2696
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=2.0593
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.2536  P=0.2120  R=0.2067  F1=0.1499  F1w=0.3157
[Val  ] Acc=0.5000  P=0.1864  R=0.2484  F1=0.1934  F1w=0.4982
       modality_w: cpg=0.502 mirna=0.498  |  val_loss=1.7912
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.4591  P=0.2413  R=0.2369  F1=0.1938  F1w=0.4766
[Val  ] Acc=0.6182  P=0.3879  R=0.2548  F1=0.2318  F1w=0.5825
       modality_w: cpg=0.508 mirna=0.492  |  val_loss=1.5741
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.5602  P=0.3219  R=0.2915  F1=0.2851  F1w=0.5789
[Val  ] Acc=0.6909  P=0.3365  R=0.2929  F1=0.3031  F1w=0.6490
       modality_w: cpg=0.518 mirna=0.482  |  val_loss=1.4642
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.6196  P=0.3666  R=0.3934  F1=0.3637  F1w=0.6403
[Val  ] Acc=0.7000  P=0.3435  R=0.3644  F1=0.3476  F1w=0.6776
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=1.6643
Fold 2 | Epoch  25/150
[Train] Acc=0.6372  P=0.3827  R=0.4078  F1=0.3795  F1w=0.6595
[Val  ] Acc=0.7364  P=0.4095  R=0.3623  F1=0.3549  F1w=0.7005
       modality_w: cpg=0.531 mirna=0.469  |  val_loss=1.6896
Fold 2 | Epoch  30/150
[Train] Acc=0.6726  P=0.4284  R=0.4658  F1=0.4297  F1w=0.6925
[Val  ] Acc=0.7455  P=0.3679  R=0.3650  F1=0.3594  F1w=0.7091
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=1.8552
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.7159  P=0.5183  R=0.5532  F1=0.5165  F1w=0.7358
[Val  ] Acc=0.7545  P=0.5850  R=0.4560  F1=0.4749  F1w=0.7439
       modality_w: cpg=0.538 mirna=0.462  |  val_loss=1.8956
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  40/150
[Train] Acc=0.7496  P=0.5388  R=0.5572  F1=0.5167  F1w=0.7676
[Val  ] Acc=0.8091  P=0.6316  R=0.5015  F1=0.5189  F1w=0.7946
       modality_w: cpg=0.542 mirna=0.458  |  val_loss=1.9912
Fold 2 | Epoch  45/150
[Train] Acc=0.8042  P=0.6804  R=0.7465  F1=0.6972  F1w=0.8216
[Val  ] Acc=0.7727  P=0.5462  R=0.5341  F1=0.5364  F1w=0.7747
       modality_w: cpg=0.544 mirna=0.456  |  val_loss=2.1680
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  50/150
[Train] Acc=0.8122  P=0.6887  R=0.7319  F1=0.6891  F1w=0.8275
[Val  ] Acc=0.7727  P=0.6089  R=0.5370  F1=0.5526  F1w=0.7786
       modality_w: cpg=0.546 mirna=0.454  |  val_loss=2.1967
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  55/150
[Train] Acc=0.8539  P=0.7582  R=0.7757  F1=0.7525  F1w=0.8656
[Val  ] Acc=0.8182  P=0.6629  R=0.5850  F1=0.6149  F1w=0.8231
       modality_w: cpg=0.550 mirna=0.450  |  val_loss=2.3331
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  60/150
[Train] Acc=0.8748  P=0.7477  R=0.8380  F1=0.7825  F1w=0.8833
[Val  ] Acc=0.8273  P=0.6659  R=0.6298  F1=0.6401  F1w=0.8360
       modality_w: cpg=0.553 mirna=0.447  |  val_loss=2.3021
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  65/150
[Train] Acc=0.8892  P=0.7721  R=0.8618  F1=0.8035  F1w=0.8979
[Val  ] Acc=0.7909  P=0.6782  R=0.6743  F1=0.6558  F1w=0.7981
       modality_w: cpg=0.555 mirna=0.445  |  val_loss=1.9379
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  70/150
[Train] Acc=0.9069  P=0.8300  R=0.9059  F1=0.8589  F1w=0.9119
[Val  ] Acc=0.8000  P=0.6563  R=0.5825  F1=0.6065  F1w=0.8086
       modality_w: cpg=0.557 mirna=0.443  |  val_loss=2.6362
Fold 2 | Epoch  75/150
[Train] Acc=0.9294  P=0.8428  R=0.8800  F1=0.8595  F1w=0.9315
[Val  ] Acc=0.8091  P=0.6722  R=0.5950  F1=0.6188  F1w=0.8213
       modality_w: cpg=0.557 mirna=0.443  |  val_loss=2.5805
Fold 2 | Epoch  80/150
[Train] Acc=0.9454  P=0.8792  R=0.9139  F1=0.8945  F1w=0.9471
[Val  ] Acc=0.8091  P=0.6665  R=0.6296  F1=0.6389  F1w=0.8115
       modality_w: cpg=0.557 mirna=0.443  |  val_loss=2.7455
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  85/150
[Train] Acc=0.9486  P=0.8904  R=0.9463  F1=0.9147  F1w=0.9500
[Val  ] Acc=0.8182  P=0.6847  R=0.5948  F1=0.6307  F1w=0.8238
       modality_w: cpg=0.556 mirna=0.444  |  val_loss=2.9750
Fold 2 | Epoch  90/150
[Train] Acc=0.9711  P=0.9601  R=0.9633  F1=0.9613  F1w=0.9712
[Val  ] Acc=0.8273  P=0.6787  R=0.6142  F1=0.6419  F1w=0.8364
       modality_w: cpg=0.557 mirna=0.443  |  val_loss=3.0091
Fold 2 | Epoch  95/150
[Train] Acc=0.9647  P=0.9188  R=0.9596  F1=0.9366  F1w=0.9659
[Val  ] Acc=0.8364  P=0.6769  R=0.6296  F1=0.6488  F1w=0.8465
       modality_w: cpg=0.558 mirna=0.442  |  val_loss=3.0156
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch 100/150
[Train] Acc=0.9647  P=0.9000  R=0.9627  F1=0.9256  F1w=0.9660
[Val  ] Acc=0.8455  P=0.6901  R=0.6669  F1=0.6777  F1w=0.8533
       modality_w: cpg=0.558 mirna=0.442  |  val_loss=3.0567
Fold 2 | Epoch 105/150
[Train] Acc=0.9727  P=0.9235  R=0.9572  F1=0.9355  F1w=0.9733
[Val  ] Acc=0.8273  P=0.6775  R=0.6142  F1=0.6421  F1w=0.8391
       modality_w: cpg=0.558 mirna=0.442  |  val_loss=3.2470
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch 110/150
[Train] Acc=0.9663  P=0.8936  R=0.9306  F1=0.9056  F1w=0.9668
[Val  ] Acc=0.8091  P=0.6690  R=0.5696  F1=0.6076  F1w=0.8129
       modality_w: cpg=0.558 mirna=0.442  |  val_loss=3.3338
Fold 2 | Epoch 115/150
[Train] Acc=0.9888  P=0.9734  R=0.9756  F1=0.9745  F1w=0.9888
[Val  ] Acc=0.8182  P=0.6184  R=0.6116  F1=0.6146  F1w=0.8274
       modality_w: cpg=0.559 mirna=0.441  |  val_loss=3.4015
Fold 2 | Epoch 120/150
[Train] Acc=0.9727  P=0.9457  R=0.9717  F1=0.9574  F1w=0.9731
[Val  ] Acc=0.8545  P=0.7049  R=0.6222  F1=0.6580  F1w=0.8623
       modality_w: cpg=0.558 mirna=0.442  |  val_loss=3.3791
Fold 2 | Epoch 125/150
[Train] Acc=0.9679  P=0.9214  R=0.9591  F1=0.9360  F1w=0.9688
[Val  ] Acc=0.8364  P=0.6308  R=0.5944  F1=0.6105  F1w=0.8377
       modality_w: cpg=0.558 mirna=0.442  |  val_loss=3.5498
⏹️  Early stopping at epoch 126 (Fold 2)

📊 Test - Fold 2
[Test ] Acc=0.9130  P=0.8355  R=0.8711  F1=0.8515  F1w=0.9149
✅ Best val F1: 0.6805  |  Best val loss: 1.4453
✅ Test F1:     0.8515

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9672    0.9440    0.9555       125
          GS     0.6800    0.7727    0.7234        22
         MSI     0.9231    0.8889    0.9057        27
      HM-SNV     0.7500    0.7500    0.7500         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.9130       184
   macro avg     0.8355    0.8711    0.8515       184
weighted avg     0.9181    0.9130    0.9149       184


🎯 Per-class F1 - Fold 2
   0:CIN       F1=0.9555
   1:GS        F1=0.7234
   2:MSI       F1=0.9057
   3:HM-SNV    F1=0.7500
   4:EBV       F1=0.9231
  📄 Confusion matrix (absolute) saved: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 2
   cpg  : std=0.0557  max=0.2576  nnz=0.799  global_w=0.558
   mirna: std=0.0921  max=0.4769  nnz=0.600  global_w=0.442

🧬 Per-cancer-type F1 - Fold 2
     Cancer      N      F1
       COAD     68  0.8086
       ESCA     19  0.4865
       READ     25  0.6000
       STAD     72  0.9159

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
   Gene-Pathway edges : 15,311 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,313 edges
   CpG↔miRNA edges : 18,313
✨ Using MANUAL focal_alpha from config: [1.0, 4.5, 1.5, 12.0, 2.0]

🧠 Fold 3 params: 831,432
🚀 Training Fold 3...  scheduler=onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.3467  P=0.2182  R=0.1965  F1=0.1877  F1w=0.4131
[Val  ] Acc=0.5946  P=0.1699  R=0.1992  F1=0.1832  F1w=0.5397
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.8313
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.4848  P=0.2401  R=0.2522  F1=0.2257  F1w=0.4951
[Val  ] Acc=0.5586  P=0.1735  R=0.2269  F1=0.1919  F1w=0.5219
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.6629
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.5762  P=0.2236  R=0.2529  F1=0.2209  F1w=0.5466
[Val  ] Acc=0.6396  P=0.1992  R=0.2506  F1=0.2220  F1w=0.5707
       modality_w: cpg=0.505 mirna=0.495  |  val_loss=1.5168
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.6100  P=0.3115  R=0.3000  F1=0.2765  F1w=0.5971
[Val  ] Acc=0.7387  P=0.3589  R=0.3347  F1=0.3356  F1w=0.6901
       modality_w: cpg=0.516 mirna=0.484  |  val_loss=1.3316
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.6806  P=0.3969  R=0.3890  F1=0.3787  F1w=0.6828
[Val  ] Acc=0.7387  P=0.3678  R=0.4066  F1=0.3836  F1w=0.7252
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=1.1130
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.6870  P=0.4743  R=0.4873  F1=0.4591  F1w=0.7081
[Val  ] Acc=0.7748  P=0.4595  R=0.4900  F1=0.4712  F1w=0.7708
       modality_w: cpg=0.533 mirna=0.467  |  val_loss=0.8190
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.7127  P=0.5229  R=0.5191  F1=0.4953  F1w=0.7386
[Val  ] Acc=0.7928  P=0.7220  R=0.6280  F1=0.5826  F1w=0.8234
       modality_w: cpg=0.537 mirna=0.463  |  val_loss=0.6524
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.7673  P=0.5764  R=0.6129  F1=0.5809  F1w=0.7856
[Val  ] Acc=0.7928  P=0.6556  R=0.6684  F1=0.6018  F1w=0.8192
       modality_w: cpg=0.539 mirna=0.461  |  val_loss=0.7099
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  40/150
[Train] Acc=0.8459  P=0.6471  R=0.6875  F1=0.6604  F1w=0.8546
[Val  ] Acc=0.8018  P=0.6637  R=0.6429  F1=0.6333  F1w=0.8167
       modality_w: cpg=0.541 mirna=0.459  |  val_loss=0.8817
Fold 3 | Epoch  45/150
[Train] Acc=0.8475  P=0.7315  R=0.7507  F1=0.7315  F1w=0.8577
[Val  ] Acc=0.8018  P=0.7253  R=0.7362  F1=0.6538  F1w=0.8197
       modality_w: cpg=0.543 mirna=0.457  |  val_loss=0.5033
Fold 3 | Epoch  50/150
[Train] Acc=0.9037  P=0.7968  R=0.8201  F1=0.8015  F1w=0.9076
[Val  ] Acc=0.8108  P=0.7387  R=0.7830  F1=0.6755  F1w=0.8268
       modality_w: cpg=0.544 mirna=0.456  |  val_loss=0.5290
Fold 3 | Epoch  55/150
[Train] Acc=0.8668  P=0.7008  R=0.7518  F1=0.7181  F1w=0.8743
[Val  ] Acc=0.8018  P=0.7334  R=0.7953  F1=0.6626  F1w=0.8185
       modality_w: cpg=0.544 mirna=0.456  |  val_loss=0.5787
⏹️  Early stopping at epoch 59 (Fold 3)

📊 Test - Fold 3
[Test ] Acc=0.7432  P=0.6417  R=0.5497  F1=0.5770  F1w=0.7775
✅ Best val F1: 0.7219  |  Best val loss: 0.4515
✅ Test F1:     0.5770

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9018    0.8080    0.8523       125
          GS     0.4118    0.6667    0.5091        21
         MSI     0.8947    0.6071    0.7234        28
      HM-SNV     0.0000    0.0000    0.0000         3
         EBV     1.0000    0.6667    0.8000         6

    accuracy                         0.7432       183
   macro avg     0.6417    0.5497    0.5770       183
weighted avg     0.8329    0.7432    0.7775       183


🎯 Per-class F1 - Fold 3
   0:CIN       F1=0.8523
   1:GS        F1=0.5091
   2:MSI       F1=0.7234
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.8000
  📄 Confusion matrix (absolute) saved: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 3
   cpg  : std=0.0612  max=0.2794  nnz=0.674  global_w=0.541
   mirna: std=0.0954  max=0.4924  nnz=0.538  global_w=0.459

🧬 Per-cancer-type F1 - Fold 3
     Cancer      N      F1
       COAD     74  0.5521
       ESCA      9  0.4706
       READ     20  0.4595
       STAD     80  0.5489

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
   Gene-Pathway edges : 15,770 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,352 edges
   CpG↔miRNA edges : 18,352
✨ Using MANUAL focal_alpha from config: [1.0, 4.5, 1.5, 12.0, 2.0]

🧠 Fold 4 params: 832,904
🚀 Training Fold 4...  scheduler=onecycle
Fold 4 | Epoch   1/150
[Train] Acc=0.2921  P=0.2092  R=0.2614  F1=0.1610  F1w=0.3582
[Val  ] Acc=0.4505  P=0.1362  R=0.2307  F1=0.1412  F1w=0.4424
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.9236
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.4831  P=0.2158  R=0.2587  F1=0.2095  F1w=0.4937
[Val  ] Acc=0.6216  P=0.1542  R=0.1967  F1=0.1721  F1w=0.5349
       modality_w: cpg=0.499 mirna=0.501  |  val_loss=1.7927
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.5185  P=0.2325  R=0.2354  F1=0.2050  F1w=0.5040
[Val  ] Acc=0.5405  P=0.1553  R=0.1854  F1=0.1668  F1w=0.5104
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.7098
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.5474  P=0.5176  R=0.2737  F1=0.2650  F1w=0.5475
[Val  ] Acc=0.4865  P=0.1943  R=0.2330  F1=0.1859  F1w=0.5097
       modality_w: cpg=0.513 mirna=0.487  |  val_loss=1.6996
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.6051  P=0.5190  R=0.3955  F1=0.3927  F1w=0.6317
[Val  ] Acc=0.5676  P=0.3891  R=0.3498  F1=0.3394  F1w=0.6126
       modality_w: cpg=0.525 mirna=0.475  |  val_loss=1.6414
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.6421  P=0.4803  R=0.4863  F1=0.4565  F1w=0.6818
[Val  ] Acc=0.7207  P=0.4585  R=0.5207  F1=0.4677  F1w=0.7383
       modality_w: cpg=0.531 mirna=0.469  |  val_loss=1.3666
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.7239  P=0.5950  R=0.5965  F1=0.5656  F1w=0.7507
[Val  ] Acc=0.7838  P=0.6020  R=0.5230  F1=0.5405  F1w=0.7941
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=1.5532
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.8010  P=0.6659  R=0.6948  F1=0.6535  F1w=0.8161
[Val  ] Acc=0.8108  P=0.5799  R=0.5274  F1=0.5466  F1w=0.8098
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=1.8481
Fold 4 | Epoch  40/150
[Train] Acc=0.8090  P=0.7122  R=0.7579  F1=0.7197  F1w=0.8216
[Val  ] Acc=0.8018  P=0.5655  R=0.5465  F1=0.5527  F1w=0.8052
       modality_w: cpg=0.538 mirna=0.462  |  val_loss=1.9181
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  45/150
[Train] Acc=0.8443  P=0.7163  R=0.7351  F1=0.7120  F1w=0.8541
[Val  ] Acc=0.8288  P=0.5815  R=0.5290  F1=0.5416  F1w=0.8261
       modality_w: cpg=0.538 mirna=0.462  |  val_loss=1.9987
Fold 4 | Epoch  50/150
[Train] Acc=0.8587  P=0.7392  R=0.7837  F1=0.7540  F1w=0.8676
[Val  ] Acc=0.8198  P=0.6544  R=0.5701  F1=0.5918  F1w=0.8241
       modality_w: cpg=0.543 mirna=0.457  |  val_loss=1.9909
Fold 4 | Epoch  55/150
[Train] Acc=0.8989  P=0.7923  R=0.8462  F1=0.8102  F1w=0.9029
[Val  ] Acc=0.8559  P=0.6982  R=0.5971  F1=0.6254  F1w=0.8589
       modality_w: cpg=0.544 mirna=0.456  |  val_loss=2.2578
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  60/150
[Train] Acc=0.9037  P=0.7928  R=0.8733  F1=0.8208  F1w=0.9098
[Val  ] Acc=0.8108  P=0.6154  R=0.6002  F1=0.5952  F1w=0.8192
       modality_w: cpg=0.544 mirna=0.456  |  val_loss=2.4245
Fold 4 | Epoch  65/150
[Train] Acc=0.9230  P=0.8444  R=0.9117  F1=0.8707  F1w=0.9260
[Val  ] Acc=0.8288  P=0.6768  R=0.6273  F1=0.6361  F1w=0.8430
       modality_w: cpg=0.547 mirna=0.453  |  val_loss=2.4253
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  70/150
[Train] Acc=0.9454  P=0.8954  R=0.9648  F1=0.9254  F1w=0.9477
[Val  ] Acc=0.8288  P=0.7125  R=0.5618  F1=0.6042  F1w=0.8292
       modality_w: cpg=0.547 mirna=0.453  |  val_loss=2.5624
Fold 4 | Epoch  75/150
[Train] Acc=0.9567  P=0.9146  R=0.9464  F1=0.9271  F1w=0.9583
[Val  ] Acc=0.8559  P=0.6957  R=0.6917  F1=0.6870  F1w=0.8668
       modality_w: cpg=0.549 mirna=0.451  |  val_loss=2.6268
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  80/150
[Train] Acc=0.9470  P=0.9148  R=0.9305  F1=0.9208  F1w=0.9487
[Val  ] Acc=0.8288  P=0.6428  R=0.5964  F1=0.6092  F1w=0.8310
       modality_w: cpg=0.548 mirna=0.452  |  val_loss=2.7961
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  85/150
[Train] Acc=0.9775  P=0.9711  R=0.9560  F1=0.9617  F1w=0.9780
[Val  ] Acc=0.8198  P=0.6771  R=0.6064  F1=0.6236  F1w=0.8261
       modality_w: cpg=0.549 mirna=0.451  |  val_loss=2.8185
Fold 4 | Epoch  90/150
[Train] Acc=0.9663  P=0.8964  R=0.9598  F1=0.9241  F1w=0.9672
[Val  ] Acc=0.8108  P=0.6862  R=0.4964  F1=0.5357  F1w=0.8065
       modality_w: cpg=0.549 mirna=0.451  |  val_loss=3.2505
Fold 4 | Epoch  95/150
[Train] Acc=0.9727  P=0.9415  R=0.9634  F1=0.9504  F1w=0.9731
[Val  ] Acc=0.8378  P=0.6854  R=0.6300  F1=0.6444  F1w=0.8485
       modality_w: cpg=0.548 mirna=0.452  |  val_loss=3.0309
Fold 4 | Epoch 100/150
[Train] Acc=0.9839  P=0.9770  R=0.9471  F1=0.9595  F1w=0.9836
[Val  ] Acc=0.8198  P=0.6879  R=0.5682  F1=0.6018  F1w=0.8239
       modality_w: cpg=0.548 mirna=0.452  |  val_loss=3.1247
⏹️  Early stopping at epoch 102 (Fold 4)

📊 Test - Fold 4
[Test ] Acc=0.7923  P=0.6748  R=0.6046  F1=0.6257  F1w=0.8009
✅ Best val F1: 0.7101  |  Best val loss: 1.3230
✅ Test F1:     0.6257

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.8651    0.8720    0.8685       125
          GS     0.5714    0.7619    0.6531        21
         MSI     0.9375    0.5556    0.6977        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     1.0000    0.8333    0.9091         6

    accuracy                         0.7923       183
   macro avg     0.6748    0.6046    0.6257       183
weighted avg     0.8276    0.7923    0.8009       183


🎯 Per-class F1 - Fold 4
   0:CIN       F1=0.8685
   1:GS        F1=0.6531
   2:MSI       F1=0.6977
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.9091
  📄 Confusion matrix (absolute) saved: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 4
   cpg  : std=0.0603  max=0.2829  nnz=0.765  global_w=0.549
   mirna: std=0.0956  max=0.5055  nnz=0.681  global_w=0.451

🧬 Per-cancer-type F1 - Fold 4
     Cancer      N      F1
       COAD     61  0.5903
       ESCA     12  0.2857
       READ     31  0.6571
       STAD     79  0.5749

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
   Gene-Pathway edges : 15,268 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,380 edges
   CpG↔miRNA edges : 18,380
✨ Using MANUAL focal_alpha from config: [1.0, 4.5, 1.5, 12.0, 2.0]

🧠 Fold 5 params: 833,352
🚀 Training Fold 5...  scheduler=onecycle
Fold 5 | Epoch   1/150
[Train] Acc=0.1108  P=0.3032  R=0.2767  F1=0.1349  F1w=0.0903
[Val  ] Acc=0.0541  P=0.0575  R=0.1654  F1=0.0645  F1w=0.0410
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=2.1074
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.1878  P=0.2336  R=0.2295  F1=0.1483  F1w=0.2271
[Val  ] Acc=0.3063  P=0.3459  R=0.2112  F1=0.1895  F1w=0.3812
       modality_w: cpg=0.501 mirna=0.499  |  val_loss=1.8527
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.4735  P=0.2701  R=0.2830  F1=0.2420  F1w=0.5040
[Val  ] Acc=0.5946  P=0.2020  R=0.2885  F1=0.2245  F1w=0.5599
       modality_w: cpg=0.506 mirna=0.494  |  val_loss=1.5996
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.5875  P=0.2867  R=0.3002  F1=0.2772  F1w=0.5989
[Val  ] Acc=0.6937  P=0.3683  R=0.3030  F1=0.3101  F1w=0.6645
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=1.5251
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.6228  P=0.4094  R=0.3931  F1=0.3745  F1w=0.6476
[Val  ] Acc=0.7207  P=0.3244  R=0.3022  F1=0.3036  F1w=0.6673
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=1.3942
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.6645  P=0.4764  R=0.4513  F1=0.4381  F1w=0.6866
[Val  ] Acc=0.7838  P=0.4386  R=0.4070  F1=0.4184  F1w=0.7538
       modality_w: cpg=0.530 mirna=0.470  |  val_loss=1.3268
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  30/150
[Train] Acc=0.7753  P=0.5781  R=0.5931  F1=0.5705  F1w=0.7862
[Val  ] Acc=0.7838  P=0.6408  R=0.4960  F1=0.5463  F1w=0.7699
       modality_w: cpg=0.537 mirna=0.463  |  val_loss=1.4989
  💾 Saved checkpoint: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  35/150
[Train] Acc=0.8010  P=0.5587  R=0.5821  F1=0.5607  F1w=0.8079
[Val  ] Acc=0.7838  P=0.6544  R=0.4741  F1=0.5177  F1w=0.7853
       modality_w: cpg=0.544 mirna=0.456  |  val_loss=1.4849
Fold 5 | Epoch  40/150
[Train] Acc=0.8652  P=0.7084  R=0.7164  F1=0.6792  F1w=0.8721
[Val  ] Acc=0.8378  P=0.7107  R=0.5373  F1=0.5991  F1w=0.8327
       modality_w: cpg=0.546 mirna=0.454  |  val_loss=1.4978
Fold 5 | Epoch  45/150
[Train] Acc=0.8764  P=0.7408  R=0.7929  F1=0.7594  F1w=0.8826
[Val  ] Acc=0.7658  P=0.5817  R=0.4294  F1=0.4801  F1w=0.7665
       modality_w: cpg=0.550 mirna=0.450  |  val_loss=1.5430
Fold 5 | Epoch  50/150
[Train] Acc=0.8973  P=0.8226  R=0.7966  F1=0.7999  F1w=0.9002
[Val  ] Acc=0.7838  P=0.6370  R=0.4948  F1=0.5462  F1w=0.7890
       modality_w: cpg=0.551 mirna=0.449  |  val_loss=1.7319
⏹️  Early stopping at epoch 51 (Fold 5)

📊 Test - Fold 5
[Test ] Acc=0.8087  P=0.6295  R=0.5746  F1=0.5928  F1w=0.8082
✅ Best val F1: 0.6549  |  Best val loss: 1.2973
✅ Test F1:     0.5928

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.8837    0.9194    0.9012       124
          GS     0.6111    0.5000    0.5500        22
         MSI     0.7600    0.7037    0.7308        27
      HM-SNV     0.1429    0.2500    0.1818         4
         EBV     0.7500    0.5000    0.6000         6

    accuracy                         0.8087       183
   macro avg     0.6295    0.5746    0.5928       183
weighted avg     0.8121    0.8087    0.8082       183


🎯 Per-class F1 - Fold 5
   0:CIN       F1=0.9012
   1:GS        F1=0.5500
   2:MSI       F1=0.7308
   3:HM-SNV    F1=0.1818
   4:EBV       F1=0.6000
  📄 Confusion matrix (absolute) saved: results/gi_07a_focal12_multiseed_20260508_075456/seed_42/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 5
   cpg  : std=0.0624  max=0.2822  nnz=0.652  global_w=0.539
   mirna: std=0.0932  max=0.4751  nnz=0.480  global_w=0.461

🧬 Per-cancer-type F1 - Fold 5
     Cancer      N      F1
       COAD     76  0.5537
       ESCA     19  0.7206
       READ     17  0.2889
       STAD     71  0.6203

📈 5-fold CV summary
  ACCURACY   : mean=0.8036  std=0.0593
  PRECISION  : mean=0.6708  std=0.0888
  RECALL     : mean=0.6173  std=0.1328
  F1         : mean=0.6320  std=0.1157
  F1_WEIGHTED: mean=0.8097  std=0.0568

🧬 Per-cancer-type F1 (5-fold mean ± std):
    Cancer  N/fold   F1 mean   F1 std
      COAD    68.0    0.6084   0.1016
      ESCA    15.8    0.4899   0.1381
      READ    23.6    0.5104   0.1284
      STAD    76.0    0.6284   0.1506

🎯 Per-class F1 (5-fold mean ± std):
         Class   F1 mean   F1 std
             0    0.8858   0.0392
             1    0.5954   0.0801
             2    0.7258   0.1068
             3    0.1864   0.2905
             4    0.7664   0.1424

✅ Seed 42 done — F1 macro = 0.6320, F1 weighted = 0.8097



══════════════════════════════════════════════════════════════════════════════
 📋 COPY KHỐI BÊN DƯỚI (đến dòng ═ tiếp theo) → PASTE VÀO ĐẦU docs/RESULTS.md
══════════════════════════════════════════════════════════════════════════════

## [2026-05-08 08:22] `gi_07a_focal12` — Macro F1: **0.6320 ± 0.0000**

**Config:** `configs/quickwins/gi_07a_focal12.yaml`  |  **Seeds:** [42]  |  **N runs:** 1 × 5 folds

| Metric            | Mean ± Std      | Per-seed means |
| ----------------- | --------------- | -------------- |
| **Macro F1**      | 0.6320 ± 0.0000 | 0.6320         |
| Weighted F1       | 0.8097 ± 0.0000 | 0.8097         |
| Accuracy          | 0.8036 ± 0.0000 | 0.8036         |
| Precision (macro) | 0.6708 ± 0.0000 | 0.6708         |
| Recall (macro)    | 0.6173 ± 0.0000 | 0.6173         |

**Per-fold F1 (macro):**

| Seed | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean   |
| ---- | ------ | ------ | ------ | ------ | ------ | ------ |
| 42   | 0.5130 | 0.8515 | 0.5770 | 0.6257 | 0.5928 | 0.6320 |

**Per-class F1 (mean across seeds):**

| Class   | Seed 42 | Avg    |
| ------- | ------- | ------ |
| 0 (CIN) | 0.8858  | 0.8858 |

---

══════════════════════════════════════════════════════════════════════════════
 ↑↑↑ COPY KHỐI BÊN TRÊN — PASTE VÀO ĐẦU docs/RESULTS.md (sau dòng tiêu đề) ↑↑↑
══════════════════════════════════════════════════════════════════════════════

💾 JSON backup (KHÔNG cần download): results/gi_07a_focal12_multiseed_20260508_075456/multi_seed_summary.json