📁 Output root: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551
🌱 Seeds: [42]
⚙️  Config: configs/quickwins/gi_08b_light_reg_focal_smoothing.yaml

============================================================
  Running seed=42  (1/1)
============================================================
$ /usr/bin/python3 -u train.py --config configs/quickwins/gi_08b_light_reg_focal_smoothing.yaml --seed 42 --save-dir results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-scatter'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_scatter/_scatter_cuda.so
  import torch_geometric.typing
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-sparse'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_sparse/_spmm_cuda.so
  import torch_geometric.typing
🔧 Override seed = 42
🔧 Override save_dir = results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints
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
   Gene-Pathway edges : 15,499 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,336 edges
   CpG↔miRNA edges : 18,336
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 1 params: 831,048
🚀 Training Fold 1...  scheduler=onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.0819  P=0.1429  R=0.3255  F1=0.0994  F1w=0.0477
[Val  ] Acc=0.1091  P=0.1166  R=0.3673  F1=0.1531  F1w=0.0633
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3609
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.1380  P=0.2328  R=0.3022  F1=0.1491  F1w=0.1191
[Val  ] Acc=0.1182  P=0.2524  R=0.3257  F1=0.2088  F1w=0.0785
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3449
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.3403  P=0.3314  R=0.4426  F1=0.3063  F1w=0.3874
[Val  ] Acc=0.5091  P=0.3929  R=0.4000  F1=0.3536  F1w=0.5354
       modality_w: cpg=0.503 mirna=0.497  |  val_loss=0.3241
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.5457  P=0.4468  R=0.5422  F1=0.4588  F1w=0.5993
[Val  ] Acc=0.5182  P=0.4593  R=0.5021  F1=0.4331  F1w=0.5729
       modality_w: cpg=0.503 mirna=0.497  |  val_loss=0.2824
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.5811  P=0.4886  R=0.6456  F1=0.5125  F1w=0.6168
[Val  ] Acc=0.6909  P=0.5082  R=0.5851  F1=0.5125  F1w=0.7062
       modality_w: cpg=0.504 mirna=0.496  |  val_loss=0.2656
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.6966  P=0.5653  R=0.7072  F1=0.6031  F1w=0.7208
[Val  ] Acc=0.7364  P=0.5021  R=0.5476  F1=0.5151  F1w=0.7387
       modality_w: cpg=0.507 mirna=0.493  |  val_loss=0.2781
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.7689  P=0.6448  R=0.8302  F1=0.6957  F1w=0.7907
[Val  ] Acc=0.7909  P=0.6021  R=0.6134  F1=0.6064  F1w=0.8028
       modality_w: cpg=0.510 mirna=0.490  |  val_loss=0.2461
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.8299  P=0.7118  R=0.8801  F1=0.7673  F1w=0.8437
[Val  ] Acc=0.8273  P=0.6182  R=0.6234  F1=0.6161  F1w=0.8168
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3033
Fold 1 | Epoch  40/150
[Train] Acc=0.9053  P=0.8223  R=0.9322  F1=0.8655  F1w=0.9116
[Val  ] Acc=0.8545  P=0.6888  R=0.6187  F1=0.6389  F1w=0.8305
       modality_w: cpg=0.516 mirna=0.484  |  val_loss=0.3498
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  45/150
[Train] Acc=0.9181  P=0.8664  R=0.9136  F1=0.8861  F1w=0.9206
[Val  ] Acc=0.8727  P=0.6723  R=0.6651  F1=0.6636  F1w=0.8690
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.3217
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  50/150
[Train] Acc=0.9438  P=0.8967  R=0.9663  F1=0.9265  F1w=0.9462
[Val  ] Acc=0.8909  P=0.7177  R=0.6745  F1=0.6890  F1w=0.8784
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.3873
Fold 1 | Epoch  55/150
[Train] Acc=0.9631  P=0.9288  R=0.9761  F1=0.9511  F1w=0.9638
[Val  ] Acc=0.9000  P=0.7256  R=0.6899  F1=0.7032  F1w=0.8902
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.3985
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  60/150
[Train] Acc=0.9743  P=0.9462  R=0.9862  F1=0.9652  F1w=0.9748
[Val  ] Acc=0.9091  P=0.7375  R=0.7081  F1=0.7215  F1w=0.9070
       modality_w: cpg=0.525 mirna=0.475  |  val_loss=0.4159
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  65/150
[Train] Acc=0.9823  P=0.9426  R=0.9909  F1=0.9645  F1w=0.9828
[Val  ] Acc=0.8909  P=0.7392  R=0.6745  F1=0.6947  F1w=0.8817
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.5213
Fold 1 | Epoch  70/150
[Train] Acc=0.9888  P=0.9605  R=0.9950  F1=0.9766  F1w=0.9890
[Val  ] Acc=0.8636  P=0.6938  R=0.6312  F1=0.6485  F1w=0.8436
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.5964
Fold 1 | Epoch  75/150
[Train] Acc=0.9775  P=0.9614  R=0.9911  F1=0.9755  F1w=0.9779
[Val  ] Acc=0.8818  P=0.7611  R=0.6365  F1=0.6611  F1w=0.8586
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.6071
Fold 1 | Epoch  80/150
[Train] Acc=0.9872  P=0.9650  R=0.9900  F1=0.9771  F1w=0.9872
[Val  ] Acc=0.8909  P=0.7052  R=0.6999  F1=0.7023  F1w=0.8853
       modality_w: cpg=0.528 mirna=0.472  |  val_loss=0.5270
⏹️  Early stopping at epoch 80 (Fold 1)

📊 Test - Fold 1
[Test ] Acc=0.8587  P=0.7703  R=0.7876  F1=0.7783  F1w=0.8609
✅ Best val F1: 0.7215  |  Best val loss: 0.2412
✅ Test F1:     0.7783

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9256    0.8960    0.9106       125
          GS     0.6400    0.7273    0.6809        22
         MSI     0.7857    0.8148    0.8000        27
      HM-SNV     0.5000    0.5000    0.5000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8587       184
   macro avg     0.7703    0.7876    0.7783       184
weighted avg     0.8641    0.8587    0.8609       184


🎯 Per-class F1 - Fold 1
   0:CIN       F1=0.9106
   1:GS        F1=0.6809
   2:MSI       F1=0.8000
   3:HM-SNV    F1=0.5000
   4:EBV       F1=1.0000
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 1
   cpg  : std=0.0648  max=0.3073  nnz=0.693  global_w=0.525
   mirna: std=0.0950  max=0.4903  nnz=0.492  global_w=0.475

🧬 Per-cancer-type F1 - Fold 1
     Cancer      N      F1
       COAD     61  0.8085
       ESCA     20  0.4861
       READ     25  0.8542
       STAD     78  0.6496

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
   Gene-Pathway edges : 15,117 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,232 edges
   CpG↔miRNA edges : 18,232
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 2 params: 834,056
🚀 Training Fold 2...  scheduler=onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.0674  P=0.2766  R=0.2104  F1=0.0492  F1w=0.0708
[Val  ] Acc=0.0364  P=0.0073  R=0.2000  F1=0.0142  F1w=0.0026
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.4069
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.2167  P=0.2176  R=0.2204  F1=0.1264  F1w=0.2861
[Val  ] Acc=0.3818  P=0.1920  R=0.2667  F1=0.1634  F1w=0.4433
       modality_w: cpg=0.501 mirna=0.499  |  val_loss=0.3643
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.4238  P=0.3250  R=0.3575  F1=0.2725  F1w=0.4804
[Val  ] Acc=0.4727  P=0.2654  R=0.3824  F1=0.2777  F1w=0.4961
       modality_w: cpg=0.506 mirna=0.494  |  val_loss=0.3307
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.5457  P=0.4209  R=0.5192  F1=0.4125  F1w=0.5877
[Val  ] Acc=0.4818  P=0.3555  R=0.4371  F1=0.3315  F1w=0.5253
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.3033
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.5618  P=0.5270  R=0.6303  F1=0.5336  F1w=0.5991
[Val  ] Acc=0.6273  P=0.4564  R=0.4562  F1=0.4417  F1w=0.6518
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.3255
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.6950  P=0.5893  R=0.7694  F1=0.6257  F1w=0.7273
[Val  ] Acc=0.6909  P=0.5167  R=0.5731  F1=0.5230  F1w=0.7173
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.3521
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.7512  P=0.6810  R=0.8140  F1=0.7158  F1w=0.7755
[Val  ] Acc=0.6727  P=0.5636  R=0.4921  F1=0.4998  F1w=0.6963
       modality_w: cpg=0.530 mirna=0.470  |  val_loss=0.3690
Fold 2 | Epoch  35/150
[Train] Acc=0.7961  P=0.7216  R=0.8804  F1=0.7717  F1w=0.8153
[Val  ] Acc=0.7727  P=0.6048  R=0.5913  F1=0.5939  F1w=0.7956
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.3823
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  40/150
[Train] Acc=0.8652  P=0.8104  R=0.9411  F1=0.8528  F1w=0.8773
[Val  ] Acc=0.8182  P=0.6826  R=0.6468  F1=0.6543  F1w=0.8351
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.3278
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  45/150
[Train] Acc=0.9165  P=0.8741  R=0.9721  F1=0.9108  F1w=0.9235
[Val  ] Acc=0.8364  P=0.6768  R=0.6325  F1=0.6458  F1w=0.8410
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.3604
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  50/150
[Train] Acc=0.9213  P=0.9011  R=0.9574  F1=0.9203  F1w=0.9272
[Val  ] Acc=0.8182  P=0.6025  R=0.6017  F1=0.6002  F1w=0.8220
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.3420
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  55/150
[Train] Acc=0.9535  P=0.9284  R=0.9691  F1=0.9451  F1w=0.9557
[Val  ] Acc=0.8000  P=0.6445  R=0.5993  F1=0.6125  F1w=0.8110
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.3770
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  60/150
[Train] Acc=0.9727  P=0.9498  R=0.9920  F1=0.9687  F1w=0.9737
[Val  ] Acc=0.8182  P=0.6483  R=0.6116  F1=0.6242  F1w=0.8243
       modality_w: cpg=0.537 mirna=0.463  |  val_loss=0.4035
Fold 2 | Epoch  65/150
[Train] Acc=0.9663  P=0.9279  R=0.9845  F1=0.9536  F1w=0.9672
[Val  ] Acc=0.8000  P=0.7273  R=0.6909  F1=0.7020  F1w=0.8117
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.3923
Fold 2 | Epoch  70/150
[Train] Acc=0.9823  P=0.9616  R=0.9948  F1=0.9773  F1w=0.9827
[Val  ] Acc=0.8000  P=0.7273  R=0.6810  F1=0.6974  F1w=0.8089
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.4215
⏹️  Early stopping at epoch 72 (Fold 2)

📊 Test - Fold 2
[Test ] Acc=0.8859  P=0.6584  R=0.7612  F1=0.6986  F1w=0.8849
✅ Best val F1: 0.7494  |  Best val loss: 0.2773
✅ Test F1:     0.6986

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     1.0000    0.8800    0.9362       125
          GS     0.6286    1.0000    0.7719        22
         MSI     0.8065    0.9259    0.8621        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8859       184
   macro avg     0.6584    0.7612    0.6986       184
weighted avg     0.9008    0.8859    0.8849       184


🎯 Per-class F1 - Fold 2
   0:CIN       F1=0.9362
   1:GS        F1=0.7719
   2:MSI       F1=0.8621
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.9231
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 2
   cpg  : std=0.0597  max=0.2743  nnz=0.709  global_w=0.537
   mirna: std=0.0935  max=0.4813  nnz=0.568  global_w=0.463

🧬 Per-cancer-type F1 - Fold 2
     Cancer      N      F1
       COAD     68  0.5669
       ESCA     19  0.4865
       READ     25  0.6000
       STAD     72  0.7449

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
   Gene-Pathway edges : 15,344 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,313 edges
   CpG↔miRNA edges : 18,313
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 3 params: 831,432
🚀 Training Fold 3...  scheduler=onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.1653  P=0.1619  R=0.1086  F1=0.1003  F1w=0.2293
[Val  ] Acc=0.1622  P=0.2387  R=0.0700  F1=0.0942  F1w=0.2398
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3835
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.3258  P=0.2480  R=0.2735  F1=0.2156  F1w=0.3837
[Val  ] Acc=0.5135  P=0.2851  R=0.3311  F1=0.2759  F1w=0.5407
       modality_w: cpg=0.499 mirna=0.501  |  val_loss=0.3348
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.4494  P=0.3632  R=0.4649  F1=0.3554  F1w=0.4980
[Val  ] Acc=0.5495  P=0.3984  R=0.4816  F1=0.3629  F1w=0.5783
       modality_w: cpg=0.504 mirna=0.496  |  val_loss=0.2698
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.5345  P=0.4478  R=0.5715  F1=0.4443  F1w=0.5787
[Val  ] Acc=0.5225  P=0.3745  R=0.5346  F1=0.3712  F1w=0.5591
       modality_w: cpg=0.505 mirna=0.495  |  val_loss=0.2153
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.6822  P=0.5461  R=0.7018  F1=0.5857  F1w=0.7108
[Val  ] Acc=0.5946  P=0.4333  R=0.5280  F1=0.4247  F1w=0.6450
       modality_w: cpg=0.506 mirna=0.494  |  val_loss=0.2130
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.7030  P=0.5976  R=0.7529  F1=0.6330  F1w=0.7333
[Val  ] Acc=0.6847  P=0.4710  R=0.6037  F1=0.4898  F1w=0.7175
       modality_w: cpg=0.508 mirna=0.492  |  val_loss=0.1761
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.7945  P=0.6818  R=0.8405  F1=0.7335  F1w=0.8133
[Val  ] Acc=0.7477  P=0.5734  R=0.7224  F1=0.6016  F1w=0.7752
       modality_w: cpg=0.511 mirna=0.489  |  val_loss=0.1390
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  35/150
[Train] Acc=0.8395  P=0.7740  R=0.8858  F1=0.8116  F1w=0.8541
[Val  ] Acc=0.7658  P=0.6055  R=0.7120  F1=0.6268  F1w=0.7925
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.1424
Fold 3 | Epoch  40/150
[Train] Acc=0.8892  P=0.8081  R=0.9129  F1=0.8506  F1w=0.8959
[Val  ] Acc=0.8288  P=0.6859  R=0.7826  F1=0.7149  F1w=0.8445
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.1317
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  45/150
[Train] Acc=0.9406  P=0.8695  R=0.9690  F1=0.9118  F1w=0.9433
[Val  ] Acc=0.8198  P=0.6998  R=0.7545  F1=0.7047  F1w=0.8343
       modality_w: cpg=0.518 mirna=0.482  |  val_loss=0.1996
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  50/150
[Train] Acc=0.9438  P=0.9055  R=0.9643  F1=0.9307  F1w=0.9465
[Val  ] Acc=0.8829  P=0.7892  R=0.7631  F1=0.7710  F1w=0.8858
       modality_w: cpg=0.518 mirna=0.482  |  val_loss=0.2067
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  55/150
[Train] Acc=0.9647  P=0.9259  R=0.9817  F1=0.9515  F1w=0.9657
[Val  ] Acc=0.8739  P=0.6876  R=0.7761  F1=0.7222  F1w=0.8806
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.2071
Fold 3 | Epoch  60/150
[Train] Acc=0.9695  P=0.9373  R=0.9804  F1=0.9577  F1w=0.9701
[Val  ] Acc=0.8378  P=0.6449  R=0.6496  F1=0.6387  F1w=0.8390
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.3115
Fold 3 | Epoch  65/150
[Train] Acc=0.9856  P=0.9703  R=0.9913  F1=0.9804  F1w=0.9857
[Val  ] Acc=0.8468  P=0.6535  R=0.7172  F1=0.6795  F1w=0.8506
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.2673
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  70/150
[Train] Acc=0.9936  P=0.9719  R=0.9981  F1=0.9846  F1w=0.9936
[Val  ] Acc=0.8739  P=0.7029  R=0.7732  F1=0.7285  F1w=0.8808
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.2095
Fold 3 | Epoch  75/150
[Train] Acc=0.9968  P=0.9878  R=0.9991  F1=0.9933  F1w=0.9968
[Val  ] Acc=0.8739  P=0.6959  R=0.7852  F1=0.7251  F1w=0.8791
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.1718
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  80/150
[Train] Acc=0.9936  P=0.9789  R=0.9981  F1=0.9882  F1w=0.9936
[Val  ] Acc=0.8739  P=0.7469  R=0.7575  F1=0.7388  F1w=0.8789
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.1958
Fold 3 | Epoch  85/150
[Train] Acc=0.9936  P=0.9920  R=0.9959  F1=0.9939  F1w=0.9936
[Val  ] Acc=0.8829  P=0.7135  R=0.7758  F1=0.7358  F1w=0.8892
       modality_w: cpg=0.524 mirna=0.476  |  val_loss=0.2065
Fold 3 | Epoch  90/150
[Train] Acc=0.9936  P=0.9719  R=0.9964  F1=0.9838  F1w=0.9936
[Val  ] Acc=0.8559  P=0.6774  R=0.7424  F1=0.7002  F1w=0.8629
       modality_w: cpg=0.524 mirna=0.476  |  val_loss=0.2461
Fold 3 | Epoch  95/150
[Train] Acc=0.9968  P=0.9750  R=0.9991  F1=0.9862  F1w=0.9969
[Val  ] Acc=0.8919  P=0.7582  R=0.7883  F1=0.7558  F1w=0.9014
       modality_w: cpg=0.525 mirna=0.475  |  val_loss=0.2250
⏹️  Early stopping at epoch 99 (Fold 3)

📊 Test - Fold 3
[Test ] Acc=0.8525  P=0.7119  R=0.7466  F1=0.7254  F1w=0.8587
✅ Best val F1: 0.7887  |  Best val loss: 0.1037
✅ Test F1:     0.7254

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9250    0.8880    0.9061       125
          GS     0.5417    0.6190    0.5778        21
         MSI     0.8929    0.8929    0.8929        28
      HM-SNV     0.2000    0.3333    0.2500         3
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8525       183
   macro avg     0.7119    0.7466    0.7254       183
weighted avg     0.8667    0.8525    0.8587       183


🎯 Per-class F1 - Fold 3
   0:CIN       F1=0.9061
   1:GS        F1=0.5778
   2:MSI       F1=0.8929
   3:HM-SNV    F1=0.2500
   4:EBV       F1=1.0000
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 3
   cpg  : std=0.0687  max=0.3255  nnz=0.616  global_w=0.524
   mirna: std=0.0864  max=0.4317  nnz=0.552  global_w=0.476

🧬 Per-cancer-type F1 - Fold 3
     Cancer      N      F1
       COAD     74  0.7478
       ESCA      9  0.4706
       READ     20  1.0000
       STAD     80  0.7385

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
   Gene-Pathway edges : 15,801 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,352 edges
   CpG↔miRNA edges : 18,352
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 4 params: 832,904
🚀 Training Fold 4...  scheduler=onecycle
Fold 4 | Epoch   1/150
[Train] Acc=0.0915  P=0.1807  R=0.2350  F1=0.0836  F1w=0.0701
[Val  ] Acc=0.0721  P=0.0331  R=0.1824  F1=0.0502  F1w=0.0341
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3752
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.1445  P=0.2638  R=0.3059  F1=0.1567  F1w=0.1215
[Val  ] Acc=0.0631  P=0.2216  R=0.1796  F1=0.0415  F1w=0.0354
       modality_w: cpg=0.501 mirna=0.499  |  val_loss=0.3684
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.2889  P=0.3411  R=0.3272  F1=0.2434  F1w=0.3362
[Val  ] Acc=0.4324  P=0.3162  R=0.3518  F1=0.3116  F1w=0.4832
       modality_w: cpg=0.505 mirna=0.495  |  val_loss=0.3476
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.4302  P=0.4383  R=0.5458  F1=0.4206  F1w=0.4824
[Val  ] Acc=0.4324  P=0.3619  R=0.4428  F1=0.3351  F1w=0.4815
       modality_w: cpg=0.513 mirna=0.487  |  val_loss=0.3105
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.6356  P=0.5680  R=0.7360  F1=0.5919  F1w=0.6769
[Val  ] Acc=0.7027  P=0.4649  R=0.4899  F1=0.4676  F1w=0.7212
       modality_w: cpg=0.519 mirna=0.481  |  val_loss=0.3543
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.7464  P=0.6598  R=0.7799  F1=0.6899  F1w=0.7755
[Val  ] Acc=0.7658  P=0.5490  R=0.5522  F1=0.5371  F1w=0.7832
       modality_w: cpg=0.524 mirna=0.476  |  val_loss=0.3868
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.8283  P=0.7294  R=0.8400  F1=0.7678  F1w=0.8429
[Val  ] Acc=0.7838  P=0.5861  R=0.6013  F1=0.5837  F1w=0.8022
       modality_w: cpg=0.528 mirna=0.472  |  val_loss=0.3711
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.8363  P=0.7646  R=0.8778  F1=0.8054  F1w=0.8493
[Val  ] Acc=0.7928  P=0.5962  R=0.5657  F1=0.5735  F1w=0.8071
       modality_w: cpg=0.531 mirna=0.469  |  val_loss=0.3507
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  40/150
[Train] Acc=0.8989  P=0.8378  R=0.9568  F1=0.8820  F1w=0.9074
[Val  ] Acc=0.8739  P=0.7044  R=0.7280  F1=0.7098  F1w=0.8823
       modality_w: cpg=0.533 mirna=0.467  |  val_loss=0.3775
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  45/150
[Train] Acc=0.9262  P=0.8922  R=0.9550  F1=0.9170  F1w=0.9309
[Val  ] Acc=0.8649  P=0.7055  R=0.7217  F1=0.7106  F1w=0.8762
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.3930
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  50/150
[Train] Acc=0.9567  P=0.9385  R=0.9873  F1=0.9587  F1w=0.9591
[Val  ] Acc=0.8739  P=0.6711  R=0.7153  F1=0.6854  F1w=0.8786
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.4047
Fold 4 | Epoch  55/150
[Train] Acc=0.9695  P=0.9397  R=0.9871  F1=0.9614  F1w=0.9705
[Val  ] Acc=0.8829  P=0.7079  R=0.7234  F1=0.7149  F1w=0.8847
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.3847
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  60/150
[Train] Acc=0.9663  P=0.9227  R=0.9695  F1=0.9438  F1w=0.9673
[Val  ] Acc=0.8559  P=0.6943  R=0.7190  F1=0.7037  F1w=0.8670
       modality_w: cpg=0.537 mirna=0.463  |  val_loss=0.4249
Fold 4 | Epoch  65/150
[Train] Acc=0.9727  P=0.9407  R=0.9898  F1=0.9630  F1w=0.9736
[Val  ] Acc=0.8559  P=0.7036  R=0.7063  F1=0.7017  F1w=0.8686
       modality_w: cpg=0.537 mirna=0.463  |  val_loss=0.5216
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  70/150
[Train] Acc=0.9775  P=0.9604  R=0.9917  F1=0.9748  F1w=0.9781
[Val  ] Acc=0.8649  P=0.6874  R=0.7217  F1=0.7014  F1w=0.8726
       modality_w: cpg=0.538 mirna=0.462  |  val_loss=0.5043
Fold 4 | Epoch  75/150
[Train] Acc=0.9872  P=0.9805  R=0.9962  F1=0.9878  F1w=0.9874
[Val  ] Acc=0.8739  P=0.6598  R=0.7207  F1=0.6871  F1w=0.8759
       modality_w: cpg=0.539 mirna=0.461  |  val_loss=0.4526
Fold 4 | Epoch  80/150
[Train] Acc=0.9872  P=0.9684  R=0.9962  F1=0.9817  F1w=0.9874
[Val  ] Acc=0.8739  P=0.7111  R=0.7207  F1=0.7142  F1w=0.8812
       modality_w: cpg=0.539 mirna=0.461  |  val_loss=0.5046
Fold 4 | Epoch  85/150
[Train] Acc=0.9920  P=0.9893  R=0.9881  F1=0.9884  F1w=0.9920
[Val  ] Acc=0.8649  P=0.6597  R=0.7181  F1=0.6856  F1w=0.8708
       modality_w: cpg=0.539 mirna=0.461  |  val_loss=0.5145
⏹️  Early stopping at epoch 86 (Fold 4)

📊 Test - Fold 4
[Test ] Acc=0.8415  P=0.6793  R=0.6993  F1=0.6835  F1w=0.8504
✅ Best val F1: 0.7152  |  Best val loss: 0.2577
✅ Test F1:     0.6835

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9316    0.8720    0.9008       125
          GS     0.5484    0.8095    0.6538        21
         MSI     0.9167    0.8148    0.8627        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8415       183
   macro avg     0.6793    0.6993    0.6835       183
weighted avg     0.8673    0.8415    0.8504       183


🎯 Per-class F1 - Fold 4
   0:CIN       F1=0.9008
   1:GS        F1=0.6538
   2:MSI       F1=0.8627
   3:HM-SNV    F1=0.0000
   4:EBV       F1=1.0000
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 4
   cpg  : std=0.0595  max=0.2752  nnz=0.698  global_w=0.537
   mirna: std=0.0872  max=0.4483  nnz=0.604  global_w=0.463

🧬 Per-cancer-type F1 - Fold 4
     Cancer      N      F1
       COAD     61  0.6389
       ESCA     12  0.2857
       READ     31  0.6618
       STAD     79  0.6383

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
   Gene-Pathway edges : 15,307 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,380 edges
   CpG↔miRNA edges : 18,380
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 5 params: 833,352
🚀 Training Fold 5...  scheduler=onecycle
Fold 5 | Epoch   1/150
[Train] Acc=0.0433  P=0.1791  R=0.1484  F1=0.0359  F1w=0.0500
[Val  ] Acc=0.0180  P=0.0040  R=0.2000  F1=0.0079  F1w=0.0007
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3901
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.2231  P=0.1868  R=0.2095  F1=0.1262  F1w=0.2884
[Val  ] Acc=0.2973  P=0.1863  R=0.1761  F1=0.1455  F1w=0.3535
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3647
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.4141  P=0.3551  R=0.4546  F1=0.2698  F1w=0.4618
[Val  ] Acc=0.4685  P=0.2385  R=0.3555  F1=0.2479  F1w=0.4992
       modality_w: cpg=0.503 mirna=0.497  |  val_loss=0.3246
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.5506  P=0.3864  R=0.4966  F1=0.3631  F1w=0.5858
[Val  ] Acc=0.5856  P=0.4653  R=0.5403  F1=0.4328  F1w=0.6172
       modality_w: cpg=0.508 mirna=0.492  |  val_loss=0.2819
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.6501  P=0.4958  R=0.6734  F1=0.5390  F1w=0.6793
[Val  ] Acc=0.7568  P=0.5580  R=0.6367  F1=0.5750  F1w=0.7767
       modality_w: cpg=0.513 mirna=0.487  |  val_loss=0.2177
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.7608  P=0.6345  R=0.8501  F1=0.6973  F1w=0.7794
[Val  ] Acc=0.8018  P=0.5897  R=0.6627  F1=0.6173  F1w=0.8151
       modality_w: cpg=0.518 mirna=0.482  |  val_loss=0.3127
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  30/150
[Train] Acc=0.7865  P=0.6694  R=0.8308  F1=0.7146  F1w=0.8067
[Val  ] Acc=0.7838  P=0.6014  R=0.6035  F1=0.5888  F1w=0.7888
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.3197
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  35/150
[Train] Acc=0.8620  P=0.7849  R=0.9008  F1=0.8299  F1w=0.8711
[Val  ] Acc=0.8378  P=0.6344  R=0.6773  F1=0.6528  F1w=0.8399
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.3914
Fold 5 | Epoch  40/150
[Train] Acc=0.8668  P=0.7643  R=0.9107  F1=0.8180  F1w=0.8760
[Val  ] Acc=0.7838  P=0.6087  R=0.6093  F1=0.6014  F1w=0.7976
       modality_w: cpg=0.524 mirna=0.476  |  val_loss=0.4070
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  45/150
[Train] Acc=0.8957  P=0.8088  R=0.9283  F1=0.8518  F1w=0.9022
[Val  ] Acc=0.8288  P=0.6750  R=0.6648  F1=0.6684  F1w=0.8424
       modality_w: cpg=0.525 mirna=0.475  |  val_loss=0.3930
Fold 5 | Epoch  50/150
[Train] Acc=0.9567  P=0.9320  R=0.9873  F1=0.9557  F1w=0.9587
[Val  ] Acc=0.8468  P=0.6796  R=0.6799  F1=0.6789  F1w=0.8572
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.3166
Fold 5 | Epoch  55/150
[Train] Acc=0.9535  P=0.8940  R=0.9824  F1=0.9319  F1w=0.9555
[Val  ] Acc=0.8649  P=0.6886  R=0.6852  F1=0.6865  F1w=0.8698
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.3197
Fold 5 | Epoch  60/150
[Train] Acc=0.9583  P=0.9143  R=0.9689  F1=0.9386  F1w=0.9596
[Val  ] Acc=0.8378  P=0.6714  R=0.6547  F1=0.6623  F1w=0.8370
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.3491
⏹️  Early stopping at epoch 64 (Fold 5)

📊 Test - Fold 5
[Test ] Acc=0.8525  P=0.7175  R=0.7208  F1=0.7136  F1w=0.8580
✅ Best val F1: 0.7384  |  Best val loss: 0.2157
✅ Test F1:     0.7136

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9187    0.9113    0.9150       124
          GS     0.7222    0.5909    0.6500        22
         MSI     0.8214    0.8519    0.8364        27
      HM-SNV     0.1250    0.2500    0.1667         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8525       183
   macro avg     0.7175    0.7208    0.7136       183
weighted avg     0.8660    0.8525    0.8580       183


🎯 Per-class F1 - Fold 5
   0:CIN       F1=0.9150
   1:GS        F1=0.6500
   2:MSI       F1=0.8364
   3:HM-SNV    F1=0.1667
   4:EBV       F1=1.0000
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/seed_42/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 5
   cpg  : std=0.0648  max=0.2892  nnz=0.606  global_w=0.525
   mirna: std=0.0887  max=0.4532  nnz=0.537  global_w=0.475

🧬 Per-cancer-type F1 - Fold 5
     Cancer      N      F1
       COAD     76  0.6608
       ESCA     19  0.5359
       READ     17  0.4655
       STAD     71  0.7234

📈 5-fold CV summary
  ACCURACY   : mean=0.8582  std=0.0149
  PRECISION  : mean=0.7075  std=0.0381
  RECALL     : mean=0.7431  std=0.0308
  F1         : mean=0.7199  std=0.0324
  F1_WEIGHTED: mean=0.8626  std=0.0117

🧬 Per-cancer-type F1 (5-fold mean ± std):
    Cancer  N/fold   F1 mean   F1 std
      COAD    68.0    0.6846   0.0847
      ESCA    15.8    0.4530   0.0865
      READ    23.6    0.7163   0.1891
      STAD    76.0    0.6989   0.0456

🎯 Per-class F1 (5-fold mean ± std):
         Class   F1 mean   F1 std
             0    0.9137   0.0122
             1    0.6669   0.0626
             2    0.8508   0.0311
             3    0.1833   0.1856
             4    0.9846   0.0308

✅ Seed 42 done — F1 macro = 0.7199, F1 weighted = 0.8626



══════════════════════════════════════════════════════════════════════════════
 📋 COPY KHỐI BÊN DƯỚI (đến dòng ═ tiếp theo) → PASTE VÀO ĐẦU docs/RESULTS.md
══════════════════════════════════════════════════════════════════════════════

## [2026-05-08 07:26] `gi_08b_light_reg_focal_smoothing` — Macro F1: **0.7199 ± 0.0000**

**Config:** `configs/quickwins/gi_08b_light_reg_focal_smoothing.yaml`  |  **Seeds:** [42]  |  **N runs:** 1 × 5 folds

| Metric            | Mean ± Std      | Per-seed means |
| ----------------- | --------------- | -------------- |
| **Macro F1**      | 0.7199 ± 0.0000 | 0.7199         |
| Weighted F1       | 0.8626 ± 0.0000 | 0.8626         |
| Accuracy          | 0.8582 ± 0.0000 | 0.8582         |
| Precision (macro) | 0.7075 ± 0.0000 | 0.7075         |
| Recall (macro)    | 0.7431 ± 0.0000 | 0.7431         |

**Per-fold F1 (macro):**

| Seed | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean   |
| ---- | ------ | ------ | ------ | ------ | ------ | ------ |
| 42   | 0.7783 | 0.6986 | 0.7254 | 0.6835 | 0.7136 | 0.7199 |

**Per-class F1 (mean across seeds):**

| Class   | Seed 42 | Avg    |
| ------- | ------- | ------ |
| 0 (CIN) | 0.9137  | 0.9137 |

---

══════════════════════════════════════════════════════════════════════════════
 ↑↑↑ COPY KHỐI BÊN TRÊN — PASTE VÀO ĐẦU docs/RESULTS.md (sau dòng tiêu đề) ↑↑↑
══════════════════════════════════════════════════════════════════════════════

💾 JSON backup (KHÔNG cần download): results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_065551/multi_seed_summary.json