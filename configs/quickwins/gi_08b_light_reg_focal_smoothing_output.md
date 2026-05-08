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


📁 Output root: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018
🌱 Seeds: [42, 123, 2024]
⚙️  Config: configs/quickwins/gi_08b_light_reg_focal_smoothing.yaml

============================================================
  Running seed=42  (1/3)
============================================================
$ /usr/bin/python3 -u train.py --config configs/quickwins/gi_08b_light_reg_focal_smoothing.yaml --seed 42 --save-dir results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-scatter'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_scatter/_scatter_cuda.so
  import torch_geometric.typing
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-sparse'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_sparse/_spmm_cuda.so
  import torch_geometric.typing
🔧 Override seed = 42
🔧 Override save_dir = results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints
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
   Gene-Pathway edges : 15,491 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,336 edges
   CpG↔miRNA edges : 18,336
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 1 params: 831,048
🚀 Training Fold 1...  scheduler=onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.0819  P=0.1416  R=0.3255  F1=0.0988  F1w=0.0472
[Val  ] Acc=0.1091  P=0.1166  R=0.3673  F1=0.1531  F1w=0.0633
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3610
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.1380  P=0.2536  R=0.3302  F1=0.1515  F1w=0.1182
[Val  ] Acc=0.1182  P=0.2524  R=0.3257  F1=0.2088  F1w=0.0785
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3449
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.3579  P=0.3324  R=0.4483  F1=0.3110  F1w=0.4081
[Val  ] Acc=0.5000  P=0.4013  R=0.4101  F1=0.3569  F1w=0.5343
       modality_w: cpg=0.502 mirna=0.498  |  val_loss=0.3170
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.5104  P=0.4238  R=0.5370  F1=0.4289  F1w=0.5675
[Val  ] Acc=0.4182  P=0.4564  R=0.4404  F1=0.3885  F1w=0.4920
       modality_w: cpg=0.502 mirna=0.498  |  val_loss=0.2933
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.5730  P=0.4946  R=0.6901  F1=0.5159  F1w=0.6154
[Val  ] Acc=0.6545  P=0.4621  R=0.5046  F1=0.4614  F1w=0.6744
       modality_w: cpg=0.505 mirna=0.495  |  val_loss=0.2719
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.7191  P=0.5899  R=0.7561  F1=0.6411  F1w=0.7401
[Val  ] Acc=0.6727  P=0.5494  R=0.5296  F1=0.5265  F1w=0.7027
       modality_w: cpg=0.510 mirna=0.490  |  val_loss=0.2783
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.7384  P=0.6098  R=0.8092  F1=0.6510  F1w=0.7678
[Val  ] Acc=0.7909  P=0.6205  R=0.6065  F1=0.6093  F1w=0.8110
       modality_w: cpg=0.511 mirna=0.489  |  val_loss=0.2793
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.8283  P=0.7449  R=0.8788  F1=0.7900  F1w=0.8416
[Val  ] Acc=0.8455  P=0.6265  R=0.6866  F1=0.6535  F1w=0.8443
       modality_w: cpg=0.513 mirna=0.487  |  val_loss=0.2926
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  40/150
[Train] Acc=0.8828  P=0.8132  R=0.9205  F1=0.8543  F1w=0.8910
[Val  ] Acc=0.8000  P=0.6209  R=0.5681  F1=0.5902  F1w=0.7880
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3915
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  45/150
[Train] Acc=0.9213  P=0.8811  R=0.9318  F1=0.9004  F1w=0.9257
[Val  ] Acc=0.8636  P=0.6864  R=0.6566  F1=0.6694  F1w=0.8581
       modality_w: cpg=0.518 mirna=0.482  |  val_loss=0.3990
Fold 1 | Epoch  50/150
[Train] Acc=0.9213  P=0.8933  R=0.9515  F1=0.9170  F1w=0.9261
[Val  ] Acc=0.9000  P=0.7158  R=0.7153  F1=0.7152  F1w=0.8991
       modality_w: cpg=0.518 mirna=0.482  |  val_loss=0.4452
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  55/150
[Train] Acc=0.9294  P=0.8657  R=0.9553  F1=0.9045  F1w=0.9325
[Val  ] Acc=0.8636  P=0.7093  R=0.6283  F1=0.6406  F1w=0.8366
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.4878
Fold 1 | Epoch  60/150
[Train] Acc=0.9727  P=0.9352  R=0.9920  F1=0.9616  F1w=0.9734
[Val  ] Acc=0.9000  P=0.7256  R=0.6899  F1=0.7032  F1w=0.8902
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.4577
Fold 1 | Epoch  65/150
[Train] Acc=0.9759  P=0.9593  R=0.9907  F1=0.9742  F1w=0.9763
[Val  ] Acc=0.9000  P=0.7340  R=0.6899  F1=0.7035  F1w=0.8896
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.5382
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  70/150
[Train] Acc=0.9856  P=0.9707  R=0.9958  F1=0.9826  F1w=0.9858
[Val  ] Acc=0.8818  P=0.7164  R=0.6620  F1=0.6769  F1w=0.8688
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.5828
Fold 1 | Epoch  75/150
[Train] Acc=0.9888  P=0.9841  R=0.9944  F1=0.9891  F1w=0.9889
[Val  ] Acc=0.8909  P=0.7281  R=0.6745  F1=0.6890  F1w=0.8776
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.5728
Fold 1 | Epoch  80/150
[Train] Acc=0.9888  P=0.9707  R=0.9950  F1=0.9824  F1w=0.9889
[Val  ] Acc=0.8818  P=0.7212  R=0.6591  F1=0.6731  F1w=0.8648
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.6520
Fold 1 | Epoch  85/150
[Train] Acc=0.9920  P=0.9875  R=0.9976  F1=0.9924  F1w=0.9920
[Val  ] Acc=0.8909  P=0.7281  R=0.6745  F1=0.6890  F1w=0.8776
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.6407
⏹️  Early stopping at epoch 86 (Fold 1)

📊 Test - Fold 1
[Test ] Acc=0.8533  P=0.7345  R=0.7785  F1=0.7538  F1w=0.8555
✅ Best val F1: 0.7169  |  Best val loss: 0.2365
✅ Test F1:     0.7538

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9106    0.8960    0.9032       125
          GS     0.6250    0.6818    0.6522        22
         MSI     0.8800    0.8148    0.8462        27
      HM-SNV     0.4000    0.5000    0.4444         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8533       184
   macro avg     0.7345    0.7785    0.7538       184
weighted avg     0.8591    0.8533    0.8555       184


🎯 Per-class F1 - Fold 1
   0:CIN       F1=0.9032
   1:GS        F1=0.6522
   2:MSI       F1=0.8462
   3:HM-SNV    F1=0.4444
   4:EBV       F1=0.9231
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 1
   cpg  : std=0.0605  max=0.2831  nnz=0.717  global_w=0.520
   mirna: std=0.0924  max=0.4750  nnz=0.523  global_w=0.480

🧬 Per-cancer-type F1 - Fold 1
     Cancer      N      F1
       COAD     61  0.9001
       ESCA     20  0.4861
       READ     25  0.7856
       STAD     78  0.6328

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
   Gene-Pathway edges : 15,165 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,232 edges
   CpG↔miRNA edges : 18,232
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 2 params: 834,056
🚀 Training Fold 2...  scheduler=onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.0514  P=0.2347  R=0.2621  F1=0.0584  F1w=0.0361
[Val  ] Acc=0.0364  P=0.0148  R=0.3000  F1=0.0281  F1w=0.0039
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3637
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.1364  P=0.2574  R=0.2696  F1=0.1117  F1w=0.1642
[Val  ] Acc=0.2091  P=0.2538  R=0.3796  F1=0.1486  F1w=0.2470
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3431
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.3274  P=0.3711  R=0.4151  F1=0.2523  F1w=0.3703
[Val  ] Acc=0.4545  P=0.4440  R=0.3742  F1=0.2708  F1w=0.4929
       modality_w: cpg=0.504 mirna=0.496  |  val_loss=0.2872
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.4735  P=0.3755  R=0.4984  F1=0.3637  F1w=0.5131
[Val  ] Acc=0.3091  P=0.3327  R=0.4188  F1=0.2701  F1w=0.3217
       modality_w: cpg=0.509 mirna=0.491  |  val_loss=0.2761
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.5457  P=0.4308  R=0.5365  F1=0.4321  F1w=0.5860
[Val  ] Acc=0.5818  P=0.3896  R=0.5335  F1=0.3939  F1w=0.6158
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.2780
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.6485  P=0.5501  R=0.6958  F1=0.5789  F1w=0.6815
[Val  ] Acc=0.6182  P=0.4387  R=0.4957  F1=0.4445  F1w=0.6539
       modality_w: cpg=0.519 mirna=0.481  |  val_loss=0.2975
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.6934  P=0.5702  R=0.7206  F1=0.6033  F1w=0.7235
[Val  ] Acc=0.6545  P=0.5765  R=0.5693  F1=0.5448  F1w=0.6961
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.3381
Fold 2 | Epoch  35/150
[Train] Acc=0.8074  P=0.7119  R=0.8617  F1=0.7571  F1w=0.8248
[Val  ] Acc=0.7455  P=0.5838  R=0.5960  F1=0.5767  F1w=0.7705
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.3884
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  40/150
[Train] Acc=0.8411  P=0.7679  R=0.9056  F1=0.8167  F1w=0.8549
[Val  ] Acc=0.7727  P=0.5826  R=0.5942  F1=0.5781  F1w=0.7947
       modality_w: cpg=0.530 mirna=0.470  |  val_loss=0.4272
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  45/150
[Train] Acc=0.8812  P=0.7926  R=0.9000  F1=0.8338  F1w=0.8899
[Val  ] Acc=0.7818  P=0.6512  R=0.6216  F1=0.6221  F1w=0.8057
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.4100
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  50/150
[Train] Acc=0.9294  P=0.8928  R=0.9657  F1=0.9230  F1w=0.9336
[Val  ] Acc=0.7636  P=0.6348  R=0.5817  F1=0.5888  F1w=0.7916
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.3774
Fold 2 | Epoch  55/150
[Train] Acc=0.9502  P=0.9137  R=0.9729  F1=0.9408  F1w=0.9517
[Val  ] Acc=0.7818  P=0.6417  R=0.5841  F1=0.6021  F1w=0.7993
       modality_w: cpg=0.533 mirna=0.467  |  val_loss=0.4087
Fold 2 | Epoch  60/150
[Train] Acc=0.9679  P=0.9458  R=0.9844  F1=0.9634  F1w=0.9689
[Val  ] Acc=0.8000  P=0.6556  R=0.5739  F1=0.6095  F1w=0.8142
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.4754
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  65/150
[Train] Acc=0.9759  P=0.9380  R=0.9794  F1=0.9576  F1w=0.9765
[Val  ] Acc=0.7818  P=0.5748  R=0.5460  F1=0.5589  F1w=0.7912
       modality_w: cpg=0.537 mirna=0.463  |  val_loss=0.5012
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  70/150
[Train] Acc=0.9823  P=0.9570  R=0.9774  F1=0.9668  F1w=0.9825
[Val  ] Acc=0.8273  P=0.6294  R=0.6390  F1=0.6311  F1w=0.8331
       modality_w: cpg=0.538 mirna=0.462  |  val_loss=0.5166
Fold 2 | Epoch  75/150
[Train] Acc=0.9856  P=0.9737  R=0.9840  F1=0.9786  F1w=0.9857
[Val  ] Acc=0.8182  P=0.6460  R=0.6167  F1=0.6230  F1w=0.8240
       modality_w: cpg=0.539 mirna=0.461  |  val_loss=0.5233
Fold 2 | Epoch  80/150
[Train] Acc=0.9936  P=0.9936  R=0.9936  F1=0.9936  F1w=0.9936
[Val  ] Acc=0.8182  P=0.6687  R=0.6167  F1=0.6374  F1w=0.8268
       modality_w: cpg=0.540 mirna=0.460  |  val_loss=0.5378
Fold 2 | Epoch  85/150
[Train] Acc=0.9888  P=0.9759  R=0.9818  F1=0.9782  F1w=0.9888
[Val  ] Acc=0.8273  P=0.6792  R=0.6292  F1=0.6507  F1w=0.8359
       modality_w: cpg=0.540 mirna=0.460  |  val_loss=0.5845
⏹️  Early stopping at epoch 89 (Fold 2)

📊 Test - Fold 2
[Test ] Acc=0.8424  P=0.5820  R=0.6694  F1=0.6155  F1w=0.8372
✅ Best val F1: 0.6591  |  Best val loss: 0.2385
✅ Test F1:     0.6155

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9262    0.9040    0.9150       125
          GS     0.5909    0.5909    0.5909        22
         MSI     0.7931    0.8519    0.8214        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     0.6000    1.0000    0.7500         6

    accuracy                         0.8424       184
   macro avg     0.5820    0.6694    0.6155       184
weighted avg     0.8358    0.8424    0.8372       184


🎯 Per-class F1 - Fold 2
   0:CIN       F1=0.9150
   1:GS        F1=0.5909
   2:MSI       F1=0.8214
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.7500
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 2
   cpg  : std=0.0667  max=0.2997  nnz=0.587  global_w=0.538
   mirna: std=0.0835  max=0.4218  nnz=0.608  global_w=0.462

🧬 Per-cancer-type F1 - Fold 2
     Cancer      N      F1
       COAD     68  0.4265
       ESCA     19  0.3148
       READ     25  0.4926
       STAD     72  0.6776

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
   Gene-Pathway edges : 15,353 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,313 edges
   CpG↔miRNA edges : 18,313
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 3 params: 831,432
🚀 Training Fold 3...  scheduler=onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.2311  P=0.2352  R=0.1809  F1=0.1562  F1w=0.3101
[Val  ] Acc=0.1532  P=0.1822  R=0.2191  F1=0.1092  F1w=0.2048
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3790
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.3483  P=0.2512  R=0.2998  F1=0.2311  F1w=0.4093
[Val  ] Acc=0.5405  P=0.2994  R=0.2809  F1=0.2774  F1w=0.5860
       modality_w: cpg=0.499 mirna=0.501  |  val_loss=0.3462
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.3949  P=0.3380  R=0.4478  F1=0.3177  F1w=0.4462
[Val  ] Acc=0.4685  P=0.3657  R=0.5426  F1=0.3452  F1w=0.5146
       modality_w: cpg=0.502 mirna=0.498  |  val_loss=0.2582
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.4639  P=0.4196  R=0.5474  F1=0.4165  F1w=0.5094
[Val  ] Acc=0.4324  P=0.3639  R=0.5054  F1=0.3391  F1w=0.4644
       modality_w: cpg=0.504 mirna=0.496  |  val_loss=0.2151
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.5698  P=0.4709  R=0.5988  F1=0.4885  F1w=0.6110
[Val  ] Acc=0.5766  P=0.4615  R=0.5899  F1=0.4559  F1w=0.6267
       modality_w: cpg=0.505 mirna=0.495  |  val_loss=0.1879
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.6485  P=0.6068  R=0.7629  F1=0.6278  F1w=0.6852
[Val  ] Acc=0.7477  P=0.6214  R=0.6122  F1=0.5878  F1w=0.7739
       modality_w: cpg=0.503 mirna=0.497  |  val_loss=0.2135
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.7608  P=0.6738  R=0.8069  F1=0.7097  F1w=0.7864
[Val  ] Acc=0.6847  P=0.5884  R=0.6342  F1=0.5664  F1w=0.7285
       modality_w: cpg=0.506 mirna=0.494  |  val_loss=0.1845
Fold 3 | Epoch  35/150
[Train] Acc=0.8106  P=0.7257  R=0.8877  F1=0.7776  F1w=0.8271
[Val  ] Acc=0.7568  P=0.6530  R=0.6553  F1=0.6266  F1w=0.7949
       modality_w: cpg=0.506 mirna=0.494  |  val_loss=0.1878
Fold 3 | Epoch  40/150
[Train] Acc=0.8925  P=0.7864  R=0.9197  F1=0.8388  F1w=0.8987
[Val  ] Acc=0.7928  P=0.6377  R=0.6571  F1=0.6393  F1w=0.8097
       modality_w: cpg=0.508 mirna=0.492  |  val_loss=0.2530
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  45/150
[Train] Acc=0.9181  P=0.8819  R=0.9475  F1=0.9085  F1w=0.9228
[Val  ] Acc=0.7658  P=0.6328  R=0.6550  F1=0.6193  F1w=0.7998
       modality_w: cpg=0.510 mirna=0.490  |  val_loss=0.2137
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  50/150
[Train] Acc=0.9358  P=0.8652  R=0.9575  F1=0.9054  F1w=0.9384
[Val  ] Acc=0.8378  P=0.7109  R=0.7932  F1=0.7247  F1w=0.8550
       modality_w: cpg=0.511 mirna=0.489  |  val_loss=0.1228
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  55/150
[Train] Acc=0.9502  P=0.9059  R=0.9753  F1=0.9367  F1w=0.9522
[Val  ] Acc=0.8378  P=0.6298  R=0.6653  F1=0.6394  F1w=0.8469
       modality_w: cpg=0.511 mirna=0.489  |  val_loss=0.2570
Fold 3 | Epoch  60/150
[Train] Acc=0.9551  P=0.9118  R=0.9806  F1=0.9428  F1w=0.9566
[Val  ] Acc=0.8649  P=0.6853  R=0.7008  F1=0.6884  F1w=0.8729
       modality_w: cpg=0.511 mirna=0.489  |  val_loss=0.2901
Fold 3 | Epoch  65/150
[Train] Acc=0.9535  P=0.9127  R=0.9624  F1=0.9349  F1w=0.9548
[Val  ] Acc=0.8559  P=0.6678  R=0.7307  F1=0.6887  F1w=0.8611
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.2542
Fold 3 | Epoch  70/150
[Train] Acc=0.9872  P=0.9561  R=0.9962  F1=0.9753  F1w=0.9873
[Val  ] Acc=0.8649  P=0.6818  R=0.7234  F1=0.6937  F1w=0.8723
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.3356
⏹️  Early stopping at epoch 70 (Fold 3)

📊 Test - Fold 3
[Test ] Acc=0.7923  P=0.5993  R=0.6394  F1=0.6139  F1w=0.8089
✅ Best val F1: 0.7247  |  Best val loss: 0.1228
✅ Test F1:     0.6139

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9052    0.8400    0.8714       125
          GS     0.4615    0.5714    0.5106        21
         MSI     0.8800    0.7857    0.8302        28
      HM-SNV     0.0000    0.0000    0.0000         3
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.7923       183
   macro avg     0.5993    0.6394    0.6139       183
weighted avg     0.8305    0.7923    0.8089       183


🎯 Per-class F1 - Fold 3
   0:CIN       F1=0.8714
   1:GS        F1=0.5106
   2:MSI       F1=0.8302
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.8571
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 3
   cpg  : std=0.0698  max=0.3323  nnz=0.627  global_w=0.511
   mirna: std=0.0901  max=0.4509  nnz=0.482  global_w=0.489

🧬 Per-cancer-type F1 - Fold 3
     Cancer      N      F1
       COAD     74  0.4354
       ESCA      9  0.4706
       READ     20  0.4737
       STAD     80  0.6217

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
   Gene-Pathway edges : 15,814 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,352 edges
   CpG↔miRNA edges : 18,352
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 4 params: 832,904
🚀 Training Fold 4...  scheduler=onecycle
Fold 4 | Epoch   1/150
[Train] Acc=0.0754  P=0.1750  R=0.1517  F1=0.0473  F1w=0.0989
[Val  ] Acc=0.0360  P=0.0073  R=0.2000  F1=0.0142  F1w=0.0026
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3902
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.2135  P=0.2236  R=0.2834  F1=0.1483  F1w=0.2739
[Val  ] Acc=0.3423  P=0.2951  R=0.3252  F1=0.1866  F1w=0.3955
       modality_w: cpg=0.501 mirna=0.499  |  val_loss=0.3834
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.4238  P=0.3210  R=0.4584  F1=0.3201  F1w=0.4707
[Val  ] Acc=0.4234  P=0.3433  R=0.3709  F1=0.3122  F1w=0.4758
       modality_w: cpg=0.507 mirna=0.493  |  val_loss=0.3513
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.5538  P=0.4238  R=0.5562  F1=0.4415  F1w=0.5964
[Val  ] Acc=0.4775  P=0.4139  R=0.4616  F1=0.3952  F1w=0.5323
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.3113
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.7287  P=0.6175  R=0.7576  F1=0.6615  F1w=0.7532
[Val  ] Acc=0.7027  P=0.5317  R=0.5973  F1=0.5367  F1w=0.7283
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.3002
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.7721  P=0.7166  R=0.8020  F1=0.7362  F1w=0.7955
[Val  ] Acc=0.8108  P=0.5948  R=0.6748  F1=0.6237  F1w=0.8199
       modality_w: cpg=0.519 mirna=0.481  |  val_loss=0.3337
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.8331  P=0.7561  R=0.8656  F1=0.7978  F1w=0.8447
[Val  ] Acc=0.8198  P=0.6041  R=0.6647  F1=0.6287  F1w=0.8314
       modality_w: cpg=0.518 mirna=0.482  |  val_loss=0.3653
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.8700  P=0.7816  R=0.8943  F1=0.8229  F1w=0.8794
[Val  ] Acc=0.8288  P=0.6769  R=0.5855  F1=0.6136  F1w=0.8360
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.5024
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  40/150
[Train] Acc=0.8941  P=0.8249  R=0.9254  F1=0.8655  F1w=0.9016
[Val  ] Acc=0.8288  P=0.6142  R=0.6292  F1=0.6193  F1w=0.8340
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.5072
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  45/150
[Train] Acc=0.9294  P=0.8896  R=0.9397  F1=0.9112  F1w=0.9328
[Val  ] Acc=0.8649  P=0.6543  R=0.7035  F1=0.6732  F1w=0.8718
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.5061
Fold 4 | Epoch  50/150
[Train] Acc=0.9502  P=0.9080  R=0.9730  F1=0.9367  F1w=0.9526
[Val  ] Acc=0.8468  P=0.6404  R=0.6982  F1=0.6611  F1w=0.8564
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.5428
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  55/150
[Train] Acc=0.9615  P=0.9506  R=0.9864  F1=0.9658  F1w=0.9631
[Val  ] Acc=0.8559  P=0.6860  R=0.6626  F1=0.6666  F1w=0.8641
       modality_w: cpg=0.525 mirna=0.475  |  val_loss=0.5305
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  60/150
[Train] Acc=0.9679  P=0.9291  R=0.9805  F1=0.9531  F1w=0.9685
[Val  ] Acc=0.8649  P=0.6887  R=0.7126  F1=0.6965  F1w=0.8735
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.5748
Fold 4 | Epoch  65/150
[Train] Acc=0.9888  P=0.9844  R=0.9922  F1=0.9882  F1w=0.9889
[Val  ] Acc=0.8378  P=0.6630  R=0.7010  F1=0.6767  F1w=0.8496
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.5355
Fold 4 | Epoch  70/150
[Train] Acc=0.9920  P=0.9821  R=0.9937  F1=0.9878  F1w=0.9920
[Val  ] Acc=0.8468  P=0.6419  R=0.6472  F1=0.6436  F1w=0.8524
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.6098
Fold 4 | Epoch  75/150
[Train] Acc=0.9968  P=0.9968  R=0.9968  F1=0.9968  F1w=0.9968
[Val  ] Acc=0.8649  P=0.6829  R=0.7090  F1=0.6934  F1w=0.8694
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.5770
⏹️  Early stopping at epoch 78 (Fold 4)

📊 Test - Fold 4
[Test ] Acc=0.8142  P=0.6515  R=0.5802  F1=0.5945  F1w=0.8158
✅ Best val F1: 0.7148  |  Best val loss: 0.2771
✅ Test F1:     0.5945

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.8934    0.8720    0.8826       125
          GS     0.4839    0.7143    0.5769        21
         MSI     0.8800    0.8148    0.8462        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     1.0000    0.5000    0.6667         6

    accuracy                         0.8142       183
   macro avg     0.6515    0.5802    0.5945       183
weighted avg     0.8284    0.8142    0.8158       183


🎯 Per-class F1 - Fold 4
   0:CIN       F1=0.8826
   1:GS        F1=0.5769
   2:MSI       F1=0.8462
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.6667
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 4
   cpg  : std=0.0549  max=0.2439  nnz=0.708  global_w=0.526
   mirna: std=0.0918  max=0.4661  nnz=0.500  global_w=0.474

🧬 Per-cancer-type F1 - Fold 4
     Cancer      N      F1
       COAD     61  0.8529
       ESCA     12  0.2143
       READ     31  0.6067
       STAD     79  0.5313

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
   Gene-Pathway edges : 15,273 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,380 edges
   CpG↔miRNA edges : 18,380
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 5 params: 833,352
🚀 Training Fold 5...  scheduler=onecycle
Fold 5 | Epoch   1/150
[Train] Acc=0.4510  P=0.1830  R=0.1766  F1=0.1757  F1w=0.4693
[Val  ] Acc=0.5586  P=0.1674  R=0.2105  F1=0.1861  F1w=0.5074
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3855
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.4205  P=0.2216  R=0.2456  F1=0.2120  F1w=0.4508
[Val  ] Acc=0.4324  P=0.2336  R=0.2510  F1=0.1921  F1w=0.4575
       modality_w: cpg=0.501 mirna=0.499  |  val_loss=0.3690
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.4639  P=0.3261  R=0.3731  F1=0.3122  F1w=0.5067
[Val  ] Acc=0.5135  P=0.4876  R=0.4641  F1=0.3322  F1w=0.5418
       modality_w: cpg=0.505 mirna=0.495  |  val_loss=0.3310
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.5586  P=0.4129  R=0.5056  F1=0.4194  F1w=0.5954
[Val  ] Acc=0.6486  P=0.4656  R=0.5705  F1=0.4844  F1w=0.6710
       modality_w: cpg=0.508 mirna=0.492  |  val_loss=0.3218
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.6469  P=0.5288  R=0.6635  F1=0.5589  F1w=0.6712
[Val  ] Acc=0.7117  P=0.5155  R=0.6532  F1=0.5574  F1w=0.7301
       modality_w: cpg=0.511 mirna=0.489  |  val_loss=0.3551
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.7303  P=0.5844  R=0.7537  F1=0.6331  F1w=0.7519
[Val  ] Acc=0.7928  P=0.6230  R=0.6769  F1=0.6425  F1w=0.8058
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.3214
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  30/150
[Train] Acc=0.7480  P=0.6258  R=0.8428  F1=0.6867  F1w=0.7683
[Val  ] Acc=0.7748  P=0.6312  R=0.6716  F1=0.6416  F1w=0.7978
       modality_w: cpg=0.517 mirna=0.483  |  val_loss=0.2971
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  35/150
[Train] Acc=0.8315  P=0.7315  R=0.9003  F1=0.7870  F1w=0.8447
[Val  ] Acc=0.8108  P=0.6422  R=0.6978  F1=0.6580  F1w=0.8201
       modality_w: cpg=0.518 mirna=0.482  |  val_loss=0.3974
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  40/150
[Train] Acc=0.8780  P=0.7878  R=0.9283  F1=0.8393  F1w=0.8867
[Val  ] Acc=0.8108  P=0.6571  R=0.6595  F1=0.6542  F1w=0.8290
       modality_w: cpg=0.521 mirna=0.479  |  val_loss=0.3143
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  45/150
[Train] Acc=0.9053  P=0.8002  R=0.9111  F1=0.8461  F1w=0.9105
[Val  ] Acc=0.8559  P=0.6317  R=0.6953  F1=0.6586  F1w=0.8607
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.3468
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  50/150
[Train] Acc=0.9133  P=0.8290  R=0.9443  F1=0.8738  F1w=0.9184
[Val  ] Acc=0.8739  P=0.6740  R=0.7104  F1=0.6895  F1w=0.8748
       modality_w: cpg=0.524 mirna=0.476  |  val_loss=0.3216
Fold 5 | Epoch  55/150
[Train] Acc=0.9535  P=0.9040  R=0.9830  F1=0.9389  F1w=0.9552
[Val  ] Acc=0.8739  P=0.6671  R=0.7203  F1=0.6898  F1w=0.8711
       modality_w: cpg=0.525 mirna=0.475  |  val_loss=0.4354
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  60/150
[Train] Acc=0.9535  P=0.8883  R=0.9818  F1=0.9279  F1w=0.9555
[Val  ] Acc=0.8739  P=0.6890  R=0.7104  F1=0.6982  F1w=0.8771
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.3283
Fold 5 | Epoch  65/150
[Train] Acc=0.9743  P=0.9334  R=0.9885  F1=0.9582  F1w=0.9750
[Val  ] Acc=0.8739  P=0.7218  R=0.6849  F1=0.7010  F1w=0.8833
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.4255
Fold 5 | Epoch  70/150
[Train] Acc=0.9759  P=0.9471  R=0.9907  F1=0.9676  F1w=0.9765
[Val  ] Acc=0.8829  P=0.6860  R=0.7229  F1=0.7022  F1w=0.8868
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.3969
Fold 5 | Epoch  75/150
[Train] Acc=0.9904  P=0.9851  R=0.9972  F1=0.9909  F1w=0.9905
[Val  ] Acc=0.8559  P=0.6900  R=0.6825  F1=0.6862  F1w=0.8684
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.4160
⏹️  Early stopping at epoch 78 (Fold 5)

📊 Test - Fold 5
[Test ] Acc=0.8470  P=0.6821  R=0.6582  F1=0.6680  F1w=0.8573
✅ Best val F1: 0.7161  |  Best val loss: 0.2617
✅ Test F1:     0.6680

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9407    0.8952    0.9174       124
          GS     0.6364    0.6364    0.6364        22
         MSI     0.8333    0.9259    0.8772        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     1.0000    0.8333    0.9091         6

    accuracy                         0.8470       183
   macro avg     0.6821    0.6582    0.6680       183
weighted avg     0.8696    0.8470    0.8573       183


🎯 Per-class F1 - Fold 5
   0:CIN       F1=0.9174
   1:GS        F1=0.6364
   2:MSI       F1=0.8772
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.9091
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_42/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 5
   cpg  : std=0.0604  max=0.2686  nnz=0.680  global_w=0.526
   mirna: std=0.0947  max=0.4870  nnz=0.484  global_w=0.474

🧬 Per-cancer-type F1 - Fold 5
     Cancer      N      F1
       COAD     76  0.5614
       ESCA     19  0.6571
       READ     17  0.3472
       STAD     71  0.7155

📈 5-fold CV summary
  ACCURACY   : mean=0.8298  std=0.0230
  PRECISION  : mean=0.6499  std=0.0554
  RECALL     : mean=0.6651  std=0.0645
  F1         : mean=0.6491  std=0.0578
  F1_WEIGHTED: mean=0.8350  std=0.0199

🧬 Per-cancer-type F1 (5-fold mean ± std):
    Cancer  N/fold   F1 mean   F1 std
      COAD    68.0    0.6353   0.2032
      ESCA    15.8    0.4286   0.1524
      READ    23.6    0.5411   0.1473
      STAD    76.0    0.6358   0.0620

🎯 Per-class F1 (5-fold mean ± std):
         Class   F1 mean   F1 std
             0    0.8979   0.0181
             1    0.5934   0.0499
             2    0.8442   0.0190
             3    0.0889   0.1778
             4    0.8212   0.0983

✅ Seed 42 done — F1 macro = 0.6491, F1 weighted = 0.8350

============================================================
  Running seed=123  (2/3)
============================================================
$ /usr/bin/python3 -u train.py --config configs/quickwins/gi_08b_light_reg_focal_smoothing.yaml --seed 123 --save-dir results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-scatter'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_scatter/_scatter_cuda.so
  import torch_geometric.typing
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-sparse'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_sparse/_spmm_cuda.so
  import torch_geometric.typing
🔧 Override seed = 123
🔧 Override save_dir = results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints
🖥️  Device: cuda  |  Seed: 123
📂 Loading data từ: /kaggle/input/datasets/maivanquan/datn-2025-2/data_final
  Labels : (917, 3)
  Gene   : (917, 19930)
  Meth   : (917, 23111)
  miRNA  : (917, 1881)

  Samples sau align : 917
  Filter cancer_types=['COAD', 'ESCA', 'READ', 'STAD']: 917 samples
  Phân bố subtype   : {np.int64(0): np.int64(624), np.int64(1): np.int64(108), np.int64(2): np.int64(136), np.int64(3): np.int64(19), np.int64(4): np.int64(30)}
  Phân bố cancer_type: {'COAD': np.int64(340), 'ESCA': np.int64(79), 'READ': np.int64(118), 'STAD': np.int64(380)}

📐 Fold 1: gene=3626, meth=3778, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3626
   CpG   nodes : 3778
   miRNA nodes : 1881
   Parsing emQTL COAD... 13,077 edges
   Parsing emQTL ESCA... 2,575 edges
   Parsing emQTL READ... 10 edges
   Parsing emQTL STAD... 9,546 edges
   CpG→Gene edges  : 25,208
   Building ENSP→symbol map từ alias file... 3,742 proteins mapped
   Parsing STRING links... 13,848 unique edges
   Gene↔Gene edges : 27,696
   Parsing hsa_MTI.csv... 145,551 edges
   miRNA→Gene edges: 145,551
   Gene-Pathway edges : 15,416 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,299 edges
   CpG↔miRNA edges : 18,299
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 1 params: 833,096
🚀 Training Fold 1...  scheduler=onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.2745  P=0.2255  R=0.1931  F1=0.1786  F1w=0.3520
[Val  ] Acc=0.1727  P=0.2118  R=0.2324  F1=0.1384  F1w=0.2112
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3760
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.3130  P=0.2339  R=0.2005  F1=0.1845  F1w=0.3755
[Val  ] Acc=0.3091  P=0.3392  R=0.2880  F1=0.2226  F1w=0.3887
       modality_w: cpg=0.502 mirna=0.498  |  val_loss=0.3469
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.4398  P=0.3666  R=0.4217  F1=0.3243  F1w=0.4968
[Val  ] Acc=0.5091  P=0.4394  R=0.5193  F1=0.4123  F1w=0.5412
       modality_w: cpg=0.509 mirna=0.491  |  val_loss=0.2715
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.5409  P=0.4318  R=0.5298  F1=0.4385  F1w=0.5846
[Val  ] Acc=0.5636  P=0.4052  R=0.5224  F1=0.4277  F1w=0.5961
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.2411
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.5987  P=0.5025  R=0.6394  F1=0.5256  F1w=0.6332
[Val  ] Acc=0.5273  P=0.4257  R=0.5412  F1=0.4420  F1w=0.5677
       modality_w: cpg=0.519 mirna=0.481  |  val_loss=0.2490
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.6790  P=0.5818  R=0.7778  F1=0.6250  F1w=0.7085
[Val  ] Acc=0.6091  P=0.4983  R=0.5554  F1=0.5019  F1w=0.6576
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.2232
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  30/150
[Train] Acc=0.7721  P=0.6770  R=0.8279  F1=0.7204  F1w=0.7928
[Val  ] Acc=0.6909  P=0.5378  R=0.6089  F1=0.5541  F1w=0.7256
       modality_w: cpg=0.524 mirna=0.476  |  val_loss=0.2525
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  35/150
[Train] Acc=0.8507  P=0.7541  R=0.9197  F1=0.8007  F1w=0.8653
[Val  ] Acc=0.8364  P=0.6095  R=0.6995  F1=0.6453  F1w=0.8427
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.2623
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  40/150
[Train] Acc=0.8780  P=0.7892  R=0.9137  F1=0.8320  F1w=0.8870
[Val  ] Acc=0.7545  P=0.5696  R=0.6402  F1=0.5936  F1w=0.7768
       modality_w: cpg=0.528 mirna=0.472  |  val_loss=0.2970
Fold 1 | Epoch  45/150
[Train] Acc=0.9053  P=0.8243  R=0.9558  F1=0.8727  F1w=0.9119
[Val  ] Acc=0.7545  P=0.5254  R=0.6246  F1=0.5636  F1w=0.7644
       modality_w: cpg=0.529 mirna=0.471  |  val_loss=0.3669
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  50/150
[Train] Acc=0.9518  P=0.8919  R=0.9780  F1=0.9280  F1w=0.9540
[Val  ] Acc=0.8273  P=0.5940  R=0.6460  F1=0.6174  F1w=0.8256
       modality_w: cpg=0.531 mirna=0.469  |  val_loss=0.2922
Fold 1 | Epoch  55/150
[Train] Acc=0.9470  P=0.8940  R=0.9664  F1=0.9251  F1w=0.9492
[Val  ] Acc=0.8091  P=0.5606  R=0.6279  F1=0.5875  F1w=0.8082
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.2661
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  60/150
[Train] Acc=0.9711  P=0.9140  R=0.9898  F1=0.9464  F1w=0.9721
[Val  ] Acc=0.7909  P=0.5362  R=0.6226  F1=0.5672  F1w=0.7937
       modality_w: cpg=0.533 mirna=0.467  |  val_loss=0.2504
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  65/150
[Train] Acc=0.9791  P=0.9193  R=0.9888  F1=0.9477  F1w=0.9802
[Val  ] Acc=0.8091  P=0.5470  R=0.6279  F1=0.5758  F1w=0.8073
       modality_w: cpg=0.534 mirna=0.466  |  val_loss=0.3052
Fold 1 | Epoch  70/150
[Train] Acc=0.9920  P=0.9890  R=0.9954  F1=0.9921  F1w=0.9920
[Val  ] Acc=0.8091  P=0.6822  R=0.7253  F1=0.7011  F1w=0.8139
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.2837
Fold 1 | Epoch  75/150
[Train] Acc=0.9936  P=0.9898  R=0.9942  F1=0.9920  F1w=0.9936
[Val  ] Acc=0.8364  P=0.5972  R=0.6359  F1=0.6136  F1w=0.8281
       modality_w: cpg=0.537 mirna=0.463  |  val_loss=0.3533
Fold 1 | Epoch  80/150
[Train] Acc=0.9888  P=0.9755  R=0.9967  F1=0.9858  F1w=0.9889
[Val  ] Acc=0.8182  P=0.5827  R=0.6306  F1=0.6043  F1w=0.8144
       modality_w: cpg=0.537 mirna=0.463  |  val_loss=0.3812
⏹️  Early stopping at epoch 83 (Fold 1)

📊 Test - Fold 1
[Test ] Acc=0.8533  P=0.7242  R=0.7550  F1=0.7371  F1w=0.8593
✅ Best val F1: 0.7285  |  Best val loss: 0.2232
✅ Test F1:     0.7371

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9237    0.8720    0.8971       125
          GS     0.5714    0.7273    0.6400        22
         MSI     0.9259    0.9259    0.9259        27
      HM-SNV     0.2000    0.2500    0.2222         4
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8533       184
   macro avg     0.7242    0.7550    0.7371       184
weighted avg     0.8687    0.8533    0.8593       184


🎯 Per-class F1 - Fold 1
   0:CIN       F1=0.8971
   1:GS        F1=0.6400
   2:MSI       F1=0.9259
   3:HM-SNV    F1=0.2222
   4:EBV       F1=1.0000
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 1
   cpg  : std=0.0644  max=0.2959  nnz=0.602  global_w=0.533
   mirna: std=0.0889  max=0.4492  nnz=0.508  global_w=0.467

🧬 Per-cancer-type F1 - Fold 1
     Cancer      N      F1
       COAD     70  0.8735
       ESCA     15  0.2963
       READ     23  0.5536
       STAD     76  0.7578

📐 Fold 2: gene=3650, meth=3788, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3650
   CpG   nodes : 3788
   miRNA nodes : 1881
   Parsing emQTL COAD... 13,471 edges
   Parsing emQTL ESCA... 2,604 edges
   Parsing emQTL READ... 11 edges
   Parsing emQTL STAD... 9,941 edges
   CpG→Gene edges  : 26,027
   Building ENSP→symbol map từ alias file... 3,769 proteins mapped
   Parsing STRING links... 13,562 unique edges
   Gene↔Gene edges : 27,124
   Parsing hsa_MTI.csv... 145,442 edges
   miRNA→Gene edges: 145,442
   Gene-Pathway edges : 15,293 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,410 edges
   CpG↔miRNA edges : 18,410
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 2 params: 835,272
🚀 Training Fold 2...  scheduler=onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.2616  P=0.2077  R=0.2124  F1=0.1647  F1w=0.3007
[Val  ] Acc=0.2455  P=0.2641  R=0.2929  F1=0.1617  F1w=0.1880
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3547
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.3451  P=0.2707  R=0.3039  F1=0.2440  F1w=0.3890
[Val  ] Acc=0.3818  P=0.2666  R=0.3178  F1=0.2301  F1w=0.4067
       modality_w: cpg=0.502 mirna=0.498  |  val_loss=0.3253
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.4976  P=0.4244  R=0.4163  F1=0.3877  F1w=0.5405
[Val  ] Acc=0.4727  P=0.3562  R=0.4570  F1=0.3400  F1w=0.5035
       modality_w: cpg=0.508 mirna=0.492  |  val_loss=0.2929
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.5650  P=0.4597  R=0.5692  F1=0.4741  F1w=0.6027
[Val  ] Acc=0.5182  P=0.3659  R=0.4802  F1=0.3545  F1w=0.5511
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.2791
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  20/150
[Train] Acc=0.6148  P=0.4587  R=0.6098  F1=0.4845  F1w=0.6517
[Val  ] Acc=0.5909  P=0.4264  R=0.5558  F1=0.4243  F1w=0.6210
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.2556
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.7849  P=0.6265  R=0.7587  F1=0.6710  F1w=0.8018
[Val  ] Acc=0.6545  P=0.4696  R=0.5843  F1=0.4726  F1w=0.6827
       modality_w: cpg=0.524 mirna=0.476  |  val_loss=0.2938
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.8154  P=0.6700  R=0.8220  F1=0.7238  F1w=0.8283
[Val  ] Acc=0.7273  P=0.5058  R=0.5710  F1=0.5184  F1w=0.7385
       modality_w: cpg=0.528 mirna=0.472  |  val_loss=0.3147
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.8684  P=0.8044  R=0.8842  F1=0.8334  F1w=0.8778
[Val  ] Acc=0.7364  P=0.5288  R=0.6436  F1=0.5482  F1w=0.7531
       modality_w: cpg=0.529 mirna=0.471  |  val_loss=0.2909
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  40/150
[Train] Acc=0.9149  P=0.8586  R=0.9431  F1=0.8946  F1w=0.9192
[Val  ] Acc=0.7455  P=0.4886  R=0.6208  F1=0.5169  F1w=0.7619
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.2906
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  45/150
[Train] Acc=0.9647  P=0.9322  R=0.9879  F1=0.9569  F1w=0.9660
[Val  ] Acc=0.8091  P=0.7452  R=0.7593  F1=0.7120  F1w=0.8196
       modality_w: cpg=0.533 mirna=0.467  |  val_loss=0.2410
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  50/150
[Train] Acc=0.9390  P=0.8931  R=0.9674  F1=0.9259  F1w=0.9416
[Val  ] Acc=0.8000  P=0.6368  R=0.7538  F1=0.6699  F1w=0.8123
       modality_w: cpg=0.534 mirna=0.466  |  val_loss=0.2916
Fold 2 | Epoch  55/150
[Train] Acc=0.9647  P=0.9168  R=0.9801  F1=0.9461  F1w=0.9654
[Val  ] Acc=0.8091  P=0.6484  R=0.7593  F1=0.6725  F1w=0.8215
       modality_w: cpg=0.534 mirna=0.466  |  val_loss=0.2856
Fold 2 | Epoch  60/150
[Train] Acc=0.9839  P=0.9582  R=0.9936  F1=0.9751  F1w=0.9842
[Val  ] Acc=0.7818  P=0.6050  R=0.6370  F1=0.6044  F1w=0.7922
       modality_w: cpg=0.534 mirna=0.466  |  val_loss=0.3109
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  65/150
[Train] Acc=0.9839  P=0.9647  R=0.9708  F1=0.9673  F1w=0.9841
[Val  ] Acc=0.8000  P=0.5407  R=0.6310  F1=0.5735  F1w=0.8017
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.3063
Fold 2 | Epoch  70/150
[Train] Acc=0.9839  P=0.9564  R=0.9953  F1=0.9749  F1w=0.9842
[Val  ] Acc=0.8364  P=0.7665  R=0.6917  F1=0.7064  F1w=0.8345
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.3357
Fold 2 | Epoch  75/150
[Train] Acc=0.9936  P=0.9896  R=0.9981  F1=0.9937  F1w=0.9936
[Val  ] Acc=0.8273  P=0.7442  R=0.6417  F1=0.6741  F1w=0.8248
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.3598
Fold 2 | Epoch  80/150
[Train] Acc=0.9872  P=0.9565  R=0.9923  F1=0.9736  F1w=0.9873
[Val  ] Acc=0.8545  P=0.6952  R=0.7069  F1=0.6937  F1w=0.8528
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.3460
⏹️  Early stopping at epoch 84 (Fold 2)

📊 Test - Fold 2
[Test ] Acc=0.8370  P=0.6752  R=0.6888  F1=0.6565  F1w=0.8356
✅ Best val F1: 0.7567  |  Best val loss: 0.2410
✅ Test F1:     0.6565

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9206    0.9280    0.9243       125
          GS     0.5600    0.6364    0.5957        22
         MSI     0.8500    0.6296    0.7234        27
      HM-SNV     0.5000    0.2500    0.3333         4
         EBV     0.5455    1.0000    0.7059         6

    accuracy                         0.8370       184
   macro avg     0.6752    0.6888    0.6565       184
weighted avg     0.8458    0.8370    0.8356       184


🎯 Per-class F1 - Fold 2
   0:CIN       F1=0.9243
   1:GS        F1=0.5957
   2:MSI       F1=0.7234
   3:HM-SNV    F1=0.3333
   4:EBV       F1=0.7059
  📄 Confusion matrix (absolute) saved: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 2
   cpg  : std=0.0612  max=0.2826  nnz=0.691  global_w=0.535
   mirna: std=0.0830  max=0.4156  nnz=0.561  global_w=0.465

🧬 Per-cancer-type F1 - Fold 2
     Cancer      N      F1
       COAD     62  0.3798
       ESCA      9  1.0000
       READ     31  0.6987
       STAD     82  0.6543

📐 Fold 3: gene=3636, meth=3756, mirna=1881

🔨 Xây dựng Heterogeneous Graph...
   Gene  nodes : 3636
   CpG   nodes : 3756
   miRNA nodes : 1881
   Parsing emQTL COAD... 12,879 edges
   Parsing emQTL ESCA... 2,366 edges
   Parsing emQTL READ... 5 edges
   Parsing emQTL STAD... 9,646 edges
   CpG→Gene edges  : 24,896
   Building ENSP→symbol map từ alias file... 3,732 proteins mapped
   Parsing STRING links... 16,921 unique edges
   Gene↔Gene edges : 33,842
   Parsing hsa_MTI.csv... 146,444 edges
   miRNA→Gene edges: 146,444
   Gene-Pathway edges : 15,521 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,276 edges
   CpG↔miRNA edges : 18,276
✨ Using MANUAL focal_alpha from config: [0.1, 0.7, 0.35, 3.2, 1.65]

🧠 Fold 3 params: 832,328
🚀 Training Fold 3...  scheduler=onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.2311  P=0.2026  R=0.1582  F1=0.1334  F1w=0.2970
[Val  ] Acc=0.3423  P=0.2411  R=0.2737  F1=0.1804  F1w=0.4078
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=0.3818
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.3692  P=0.2483  R=0.2853  F1=0.2249  F1w=0.4238
[Val  ] Acc=0.5225  P=0.3658  R=0.3069  F1=0.2729  F1w=0.5661
       modality_w: cpg=0.501 mirna=0.499  |  val_loss=0.3638
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.4559  P=0.3228  R=0.4349  F1=0.3044  F1w=0.4939
[Val  ] Acc=0.4775  P=0.4493  R=0.3687  F1=0.2927  F1w=0.5234
       modality_w: cpg=0.506 mirna=0.494  |  val_loss=0.3233
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.5120  P=0.4143  R=0.5359  F1=0.4275  F1w=0.5556
[Val  ] Acc=0.4685  P=0.3579  R=0.3385  F1=0.2937  F1w=0.5291
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.2785
  💾 Saved checkpoint: results/gi_08b_light_reg_focal_smoothing_multiseed_20260508_083018/seed_123/checkpoints/best_model_fold_3.pt