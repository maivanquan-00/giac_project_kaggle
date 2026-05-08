📁 Output root: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600
🌱 Seeds: [42]
⚙️  Config: configs/quickwins/gi_08c_balanced_sampler_ce.yaml

============================================================
  Running seed=42  (1/1)
============================================================
$ /usr/bin/python3 -u train.py --config configs/quickwins/gi_08c_balanced_sampler_ce.yaml --seed 42 --save-dir results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-scatter'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_scatter/_scatter_cuda.so
  import torch_geometric.typing
/usr/local/lib/python3.12/dist-packages/torch_geometric/__init__.py:4: UserWarning: An issue occurred while importing 'torch-sparse'. Disabling its usage. Stacktrace: Could not load this library: /usr/local/lib/python3.12/dist-packages/torch_sparse/_spmm_cuda.so
  import torch_geometric.typing
🔧 Override seed = 42
🔧 Override save_dir = results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints
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
   Gene-Pathway edges : 15,435 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,336 edges
   CpG↔miRNA edges : 18,336
⚖️  Using neutral class weights / focal_alpha: all ones

🧠 Fold 1 params: 831,048
🚀 Training Fold 1...  scheduler=onecycle
Fold 1 | Epoch   1/150
[Train] Acc=0.2520  P=0.2971  R=0.2502  F1=0.2139  F1w=0.2120
[Val  ] Acc=0.1000  P=0.1292  R=0.3894  F1=0.1421  F1w=0.0561
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.8542
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch   5/150
[Train] Acc=0.3788  P=0.3150  R=0.3770  F1=0.3048  F1w=0.3050
[Val  ] Acc=0.0727  P=0.2756  R=0.2431  F1=0.1018  F1w=0.0657
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.7031
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  10/150
[Train] Acc=0.5634  P=0.5784  R=0.5694  F1=0.5382  F1w=0.5337
[Val  ] Acc=0.2364  P=0.4582  R=0.5139  F1=0.3546  F1w=0.2482
       modality_w: cpg=0.503 mirna=0.497  |  val_loss=1.4400
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  15/150
[Train] Acc=0.6742  P=0.6674  R=0.6811  F1=0.6717  F1w=0.6660
[Val  ] Acc=0.4818  P=0.4956  R=0.5111  F1=0.4679  F1w=0.5451
       modality_w: cpg=0.503 mirna=0.497  |  val_loss=1.1510
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  20/150
[Train] Acc=0.8315  P=0.8329  R=0.8336  F1=0.8291  F1w=0.8270
[Val  ] Acc=0.7909  P=0.5731  R=0.6007  F1=0.5851  F1w=0.7966
       modality_w: cpg=0.509 mirna=0.491  |  val_loss=0.6825
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  25/150
[Train] Acc=0.9165  P=0.9171  R=0.9189  F1=0.9173  F1w=0.9153
[Val  ] Acc=0.8273  P=0.6192  R=0.6812  F1=0.6451  F1w=0.8316
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.5666
Fold 1 | Epoch  30/150
[Train] Acc=0.9310  P=0.9312  R=0.9331  F1=0.9316  F1w=0.9299
[Val  ] Acc=0.8091  P=0.6019  R=0.6279  F1=0.6121  F1w=0.8088
       modality_w: cpg=0.519 mirna=0.481  |  val_loss=0.6600
Fold 1 | Epoch  35/150
[Train] Acc=0.9502  P=0.9506  R=0.9513  F1=0.9506  F1w=0.9499
[Val  ] Acc=0.8727  P=0.6994  R=0.6917  F1=0.6928  F1w=0.8683
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.5826
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  40/150
[Train] Acc=0.9615  P=0.9604  R=0.9613  F1=0.9607  F1w=0.9612
[Val  ] Acc=0.8909  P=0.7143  R=0.7225  F1=0.7175  F1w=0.8898
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.6119
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  45/150
[Train] Acc=0.9823  P=0.9825  R=0.9828  F1=0.9826  F1w=0.9823
[Val  ] Acc=0.9000  P=0.7144  R=0.7251  F1=0.7189  F1w=0.8947
       modality_w: cpg=0.525 mirna=0.475  |  val_loss=0.6407
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_1.pt
Fold 1 | Epoch  50/150
[Train] Acc=0.9711  P=0.9712  R=0.9713  F1=0.9710  F1w=0.9709
[Val  ] Acc=0.8727  P=0.6981  R=0.6663  F1=0.6715  F1w=0.8570
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.7930
Fold 1 | Epoch  55/150
[Train] Acc=0.9856  P=0.9855  R=0.9849  F1=0.9852  F1w=0.9855
[Val  ] Acc=0.8727  P=0.7126  R=0.6663  F1=0.6713  F1w=0.8562
       modality_w: cpg=0.528 mirna=0.472  |  val_loss=0.9316
Fold 1 | Epoch  60/150
[Train] Acc=0.9872  P=0.9867  R=0.9869  F1=0.9866  F1w=0.9871
[Val  ] Acc=0.8818  P=0.6926  R=0.6944  F1=0.6900  F1w=0.8734
       modality_w: cpg=0.529 mirna=0.471  |  val_loss=0.9046
Fold 1 | Epoch  65/150
[Train] Acc=0.9936  P=0.9932  R=0.9930  F1=0.9931  F1w=0.9936
[Val  ] Acc=0.8909  P=0.7078  R=0.6843  F1=0.6883  F1w=0.8742
       modality_w: cpg=0.527 mirna=0.473  |  val_loss=0.9264
⏹️  Early stopping at epoch 65 (Fold 1)

📊 Test - Fold 1
[Test ] Acc=0.8152  P=0.6190  R=0.6988  F1=0.6491  F1w=0.8229
✅ Best val F1: 0.7189  |  Best val loss: 0.5666
✅ Test F1:     0.6491

📋 Classification Report - Fold 1
              precision    recall  f1-score   support

         CIN     0.9450    0.8240    0.8803       125
          GS     0.5000    0.8182    0.6207        22
         MSI     0.7931    0.8519    0.8214        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8152       184
   macro avg     0.6190    0.6988    0.6491       184
weighted avg     0.8461    0.8152    0.8229       184


🎯 Per-class F1 - Fold 1
   0:CIN       F1=0.8803
   1:GS        F1=0.6207
   2:MSI       F1=0.8214
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.9231
  📄 Confusion matrix (absolute) saved: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/visualizations/fold_1/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 1
   cpg  : std=0.0580  max=0.2690  nnz=0.718  global_w=0.525
   mirna: std=0.0998  max=0.5136  nnz=0.459  global_w=0.475

🧬 Per-cancer-type F1 - Fold 1
     Cancer      N      F1
       COAD     61  0.6376
       ESCA     20  0.4861
       READ     25  0.5285
       STAD     78  0.6176

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
   Gene-Pathway edges : 15,151 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,232 edges
   CpG↔miRNA edges : 18,232
⚖️  Using neutral class weights / focal_alpha: all ones

🧠 Fold 2 params: 834,056
🚀 Training Fold 2...  scheduler=onecycle
Fold 2 | Epoch   1/150
[Train] Acc=0.1990  P=0.2033  R=0.2000  F1=0.1943  F1w=0.1948
[Val  ] Acc=0.1909  P=0.1833  R=0.3282  F1=0.1455  F1w=0.2195
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.6072
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch   5/150
[Train] Acc=0.3098  P=0.3163  R=0.3096  F1=0.3099  F1w=0.3097
[Val  ] Acc=0.4091  P=0.2517  R=0.3104  F1=0.2308  F1w=0.4740
       modality_w: cpg=0.501 mirna=0.499  |  val_loss=1.4754
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  10/150
[Train] Acc=0.5185  P=0.5080  R=0.5164  F1=0.5081  F1w=0.5093
[Val  ] Acc=0.4455  P=0.3063  R=0.4137  F1=0.2946  F1w=0.4926
       modality_w: cpg=0.509 mirna=0.491  |  val_loss=1.2642
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  15/150
[Train] Acc=0.6774  P=0.6748  R=0.6808  F1=0.6733  F1w=0.6714
[Val  ] Acc=0.5273  P=0.4813  R=0.5123  F1=0.4507  F1w=0.5877
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=1.1224
Fold 2 | Epoch  20/150
[Train] Acc=0.8154  P=0.8132  R=0.8174  F1=0.8128  F1w=0.8105
[Val  ] Acc=0.5727  P=0.5481  R=0.5857  F1=0.5197  F1w=0.6276
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=1.0110
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  25/150
[Train] Acc=0.8491  P=0.8469  R=0.8490  F1=0.8463  F1w=0.8469
[Val  ] Acc=0.7727  P=0.5853  R=0.6513  F1=0.6020  F1w=0.7976
       modality_w: cpg=0.525 mirna=0.475  |  val_loss=0.8460
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  30/150
[Train] Acc=0.8973  P=0.8973  R=0.9004  F1=0.8987  F1w=0.8963
[Val  ] Acc=0.7727  P=0.5795  R=0.6739  F1=0.6034  F1w=0.7937
       modality_w: cpg=0.530 mirna=0.470  |  val_loss=0.7899
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  35/150
[Train] Acc=0.9326  P=0.9332  R=0.9304  F1=0.9309  F1w=0.9324
[Val  ] Acc=0.7727  P=0.6163  R=0.6739  F1=0.6255  F1w=0.7967
       modality_w: cpg=0.535 mirna=0.465  |  val_loss=0.8425
Fold 2 | Epoch  40/150
[Train] Acc=0.9486  P=0.9482  R=0.9474  F1=0.9477  F1w=0.9483
[Val  ] Acc=0.7909  P=0.5748  R=0.6388  F1=0.5950  F1w=0.8022
       modality_w: cpg=0.537 mirna=0.463  |  val_loss=0.7421
Fold 2 | Epoch  45/150
[Train] Acc=0.9759  P=0.9756  R=0.9756  F1=0.9756  F1w=0.9759
[Val  ] Acc=0.8091  P=0.5681  R=0.6147  F1=0.5843  F1w=0.8161
       modality_w: cpg=0.540 mirna=0.460  |  val_loss=0.8441
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_2.pt
Fold 2 | Epoch  50/150
[Train] Acc=0.9775  P=0.9773  R=0.9775  F1=0.9773  F1w=0.9774
[Val  ] Acc=0.7727  P=0.5938  R=0.6513  F1=0.6062  F1w=0.7893
       modality_w: cpg=0.544 mirna=0.456  |  val_loss=1.0118
Fold 2 | Epoch  55/150
[Train] Acc=0.9839  P=0.9839  R=0.9836  F1=0.9837  F1w=0.9839
[Val  ] Acc=0.8091  P=0.5811  R=0.6690  F1=0.6149  F1w=0.8167
       modality_w: cpg=0.547 mirna=0.453  |  val_loss=1.0555
Fold 2 | Epoch  60/150
[Train] Acc=0.9920  P=0.9927  R=0.9922  F1=0.9924  F1w=0.9920
[Val  ] Acc=0.8273  P=0.5874  R=0.6743  F1=0.6218  F1w=0.8295
       modality_w: cpg=0.547 mirna=0.453  |  val_loss=1.0894
Fold 2 | Epoch  65/150
[Train] Acc=0.9727  P=0.9731  R=0.9717  F1=0.9723  F1w=0.9727
[Val  ] Acc=0.8364  P=0.6225  R=0.6770  F1=0.6451  F1w=0.8375
       modality_w: cpg=0.550 mirna=0.450  |  val_loss=1.0760
⏹️  Early stopping at epoch 67 (Fold 2)

📊 Test - Fold 2
[Test ] Acc=0.8587  P=0.6227  R=0.7266  F1=0.6633  F1w=0.8614
✅ Best val F1: 0.6620  |  Best val loss: 0.7371
✅ Test F1:     0.6633

📋 Classification Report - Fold 2
              precision    recall  f1-score   support

         CIN     0.9820    0.8720    0.9237       125
          GS     0.5882    0.9091    0.7143        22
         MSI     0.7931    0.8519    0.8214        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     0.7500    1.0000    0.8571         6

    accuracy                         0.8587       184
   macro avg     0.6227    0.7266    0.6633       184
weighted avg     0.8783    0.8587    0.8614       184


🎯 Per-class F1 - Fold 2
   0:CIN       F1=0.9237
   1:GS        F1=0.7143
   2:MSI       F1=0.8214
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.8571
  📄 Confusion matrix (absolute) saved: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/visualizations/fold_2/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 2
   cpg  : std=0.0677  max=0.3048  nnz=0.578  global_w=0.542
   mirna: std=0.0879  max=0.4459  nnz=0.546  global_w=0.458

🧬 Per-cancer-type F1 - Fold 2
     Cancer      N      F1
       COAD     68  0.5690
       ESCA     19  1.0000
       READ     25  0.4756
       STAD     72  0.6984

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
   Gene-Pathway edges : 15,355 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,313 edges
   CpG↔miRNA edges : 18,313
⚖️  Using neutral class weights / focal_alpha: all ones

🧠 Fold 3 params: 831,432
🚀 Training Fold 3...  scheduler=onecycle
Fold 3 | Epoch   1/150
[Train] Acc=0.1926  P=0.2223  R=0.2059  F1=0.1771  F1w=0.1731
[Val  ] Acc=0.4054  P=0.2227  R=0.2394  F1=0.2240  F1w=0.4382
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.5892
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch   5/150
[Train] Acc=0.3258  P=0.3061  R=0.3216  F1=0.2978  F1w=0.3001
[Val  ] Acc=0.2162  P=0.2637  R=0.4088  F1=0.2123  F1w=0.2368
       modality_w: cpg=0.499 mirna=0.501  |  val_loss=1.6120
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  10/150
[Train] Acc=0.5602  P=0.5371  R=0.5498  F1=0.5312  F1w=0.5391
[Val  ] Acc=0.3874  P=0.3840  R=0.5386  F1=0.3372  F1w=0.4503
       modality_w: cpg=0.504 mirna=0.496  |  val_loss=1.4296
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  15/150
[Train] Acc=0.6404  P=0.6385  R=0.6367  F1=0.6262  F1w=0.6282
[Val  ] Acc=0.6126  P=0.5017  R=0.6800  F1=0.5204  F1w=0.6505
       modality_w: cpg=0.504 mirna=0.496  |  val_loss=1.1204
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  20/150
[Train] Acc=0.8122  P=0.8050  R=0.8068  F1=0.8050  F1w=0.8099
[Val  ] Acc=0.6847  P=0.5625  R=0.7583  F1=0.5927  F1w=0.7245
       modality_w: cpg=0.509 mirna=0.491  |  val_loss=0.8522
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  25/150
[Train] Acc=0.9021  P=0.8989  R=0.9006  F1=0.8991  F1w=0.9004
[Val  ] Acc=0.7658  P=0.5645  R=0.6719  F1=0.5879  F1w=0.7813
       modality_w: cpg=0.512 mirna=0.488  |  val_loss=0.6891
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  30/150
[Train] Acc=0.9342  P=0.9339  R=0.9346  F1=0.9342  F1w=0.9342
[Val  ] Acc=0.7838  P=0.5974  R=0.6870  F1=0.6201  F1w=0.8070
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=0.5382
Fold 3 | Epoch  35/150
[Train] Acc=0.9390  P=0.9393  R=0.9394  F1=0.9385  F1w=0.9385
[Val  ] Acc=0.7928  P=0.6895  R=0.7969  F1=0.7054  F1w=0.8253
       modality_w: cpg=0.519 mirna=0.481  |  val_loss=0.6007
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  40/150
[Train] Acc=0.9679  P=0.9684  R=0.9691  F1=0.9685  F1w=0.9678
[Val  ] Acc=0.8108  P=0.6620  R=0.7923  F1=0.6944  F1w=0.8356
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.7187
Fold 3 | Epoch  45/150
[Train] Acc=0.9711  P=0.9702  R=0.9712  F1=0.9705  F1w=0.9710
[Val  ] Acc=0.8468  P=0.6966  R=0.7900  F1=0.7326  F1w=0.8566
       modality_w: cpg=0.525 mirna=0.475  |  val_loss=0.5961
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  50/150
[Train] Acc=0.9759  P=0.9764  R=0.9762  F1=0.9761  F1w=0.9759
[Val  ] Acc=0.8468  P=0.6959  R=0.7929  F1=0.7254  F1w=0.8587
       modality_w: cpg=0.528 mirna=0.472  |  val_loss=0.6539
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  55/150
[Train] Acc=0.9952  P=0.9954  R=0.9952  F1=0.9953  F1w=0.9952
[Val  ] Acc=0.8468  P=0.6997  R=0.9158  F1=0.7541  F1w=0.8603
       modality_w: cpg=0.529 mirna=0.471  |  val_loss=0.6485
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  60/150
[Train] Acc=0.9920  P=0.9913  R=0.9916  F1=0.9915  F1w=0.9920
[Val  ] Acc=0.8829  P=0.7636  R=0.8458  F1=0.7952  F1w=0.8897
       modality_w: cpg=0.530 mirna=0.470  |  val_loss=0.5584
Fold 3 | Epoch  65/150
[Train] Acc=0.9920  P=0.9914  R=0.9923  F1=0.9918  F1w=0.9920
[Val  ] Acc=0.8829  P=0.7776  R=0.8203  F1=0.7958  F1w=0.8866
       modality_w: cpg=0.529 mirna=0.471  |  val_loss=0.5928
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  70/150
[Train] Acc=0.9888  P=0.9884  R=0.9888  F1=0.9886  F1w=0.9888
[Val  ] Acc=0.8829  P=0.7582  R=0.8232  F1=0.7832  F1w=0.8903
       modality_w: cpg=0.531 mirna=0.469  |  val_loss=0.4947
Fold 3 | Epoch  75/150
[Train] Acc=0.9936  P=0.9934  R=0.9936  F1=0.9935  F1w=0.9936
[Val  ] Acc=0.8919  P=0.7625  R=0.8357  F1=0.7913  F1w=0.8996
       modality_w: cpg=0.531 mirna=0.469  |  val_loss=0.5265
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch  80/150
[Train] Acc=0.9952  P=0.9953  R=0.9953  F1=0.9953  F1w=0.9952
[Val  ] Acc=0.9099  P=0.8084  R=0.8409  F1=0.8227  F1w=0.9126
       modality_w: cpg=0.531 mirna=0.469  |  val_loss=0.4961
Fold 3 | Epoch  85/150
[Train] Acc=0.9968  P=0.9967  R=0.9972  F1=0.9969  F1w=0.9968
[Val  ] Acc=0.8739  P=0.7392  R=0.7979  F1=0.7647  F1w=0.8774
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.6528
Fold 3 | Epoch  90/150
[Train] Acc=0.9872  P=0.9860  R=0.9873  F1=0.9866  F1w=0.9872
[Val  ] Acc=0.8739  P=0.7458  R=0.7979  F1=0.7669  F1w=0.8796
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.7438
Fold 3 | Epoch  95/150
[Train] Acc=0.9968  P=0.9968  R=0.9972  F1=0.9970  F1w=0.9968
[Val  ] Acc=0.8919  P=0.7860  R=0.8357  F1=0.8060  F1w=0.8975
       modality_w: cpg=0.533 mirna=0.467  |  val_loss=0.6884
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_3.pt
Fold 3 | Epoch 100/150
[Train] Acc=0.9904  P=0.9904  R=0.9911  F1=0.9907  F1w=0.9904
[Val  ] Acc=0.8829  P=0.7940  R=0.7948  F1=0.7940  F1w=0.8817
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.6442
Fold 3 | Epoch 105/150
[Train] Acc=0.9968  P=0.9970  R=0.9965  F1=0.9967  F1w=0.9968
[Val  ] Acc=0.9009  P=0.7985  R=0.8412  F1=0.8140  F1w=0.9062
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.6889
Fold 3 | Epoch 110/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000  F1w=1.0000
[Val  ] Acc=0.8919  P=0.7966  R=0.7974  F1=0.7967  F1w=0.8907
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.7333
Fold 3 | Epoch 115/150
[Train] Acc=1.0000  P=1.0000  R=1.0000  F1=1.0000  F1w=1.0000
[Val  ] Acc=0.8649  P=0.6701  R=0.7078  F1=0.6850  F1w=0.8717
       modality_w: cpg=0.533 mirna=0.467  |  val_loss=0.9102
⏹️  Early stopping at epoch 116 (Fold 3)

📊 Test - Fold 3
[Test ] Acc=0.8251  P=0.6608  R=0.6498  F1=0.6552  F1w=0.8349
✅ Best val F1: 0.8719  |  Best val loss: 0.4398
✅ Test F1:     0.6552

📋 Classification Report - Fold 3
              precision    recall  f1-score   support

         CIN     0.9016    0.8800    0.8907       125
          GS     0.4762    0.4762    0.4762        21
         MSI     0.9259    0.8929    0.9091        28
      HM-SNV     0.0000    0.0000    0.0000         3
         EBV     1.0000    1.0000    1.0000         6

    accuracy                         0.8251       183
   macro avg     0.6608    0.6498    0.6552       183
weighted avg     0.8450    0.8251    0.8349       183


🎯 Per-class F1 - Fold 3
   0:CIN       F1=0.8907
   1:GS        F1=0.4762
   2:MSI       F1=0.9091
   3:HM-SNV    F1=0.0000
   4:EBV       F1=1.0000
  📄 Confusion matrix (absolute) saved: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/visualizations/fold_3/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 3
   cpg  : std=0.0707  max=0.3313  nnz=0.604  global_w=0.533
   mirna: std=0.0871  max=0.4276  nnz=0.451  global_w=0.467

🧬 Per-cancer-type F1 - Fold 3
     Cancer      N      F1
       COAD     74  0.5712
       ESCA      9  0.4706
       READ     20  0.4872
       STAD     80  0.6463

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
   Gene-Pathway edges : 15,805 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,352 edges
   CpG↔miRNA edges : 18,352
⚖️  Using neutral class weights / focal_alpha: all ones

🧠 Fold 4 params: 832,904
🚀 Training Fold 4...  scheduler=onecycle
Fold 4 | Epoch   1/150
[Train] Acc=0.2039  P=0.1680  R=0.2086  F1=0.1732  F1w=0.1694
[Val  ] Acc=0.3153  P=0.1884  R=0.1696  F1=0.1466  F1w=0.3777
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.5589
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch   5/150
[Train] Acc=0.2873  P=0.2785  R=0.2976  F1=0.2689  F1w=0.2658
[Val  ] Acc=0.3874  P=0.2847  R=0.4131  F1=0.2646  F1w=0.4336
       modality_w: cpg=0.499 mirna=0.501  |  val_loss=1.5811
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  10/150
[Train] Acc=0.5457  P=0.5261  R=0.5281  F1=0.5176  F1w=0.5319
[Val  ] Acc=0.4775  P=0.3160  R=0.4306  F1=0.3151  F1w=0.5075
       modality_w: cpg=0.507 mirna=0.493  |  val_loss=1.2655
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  15/150
[Train] Acc=0.7079  P=0.7079  R=0.7089  F1=0.7048  F1w=0.7048
[Val  ] Acc=0.4685  P=0.4611  R=0.5352  F1=0.4309  F1w=0.4972
       modality_w: cpg=0.515 mirna=0.485  |  val_loss=1.0712
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  20/150
[Train] Acc=0.8427  P=0.8254  R=0.8270  F1=0.8255  F1w=0.8397
[Val  ] Acc=0.6396  P=0.4556  R=0.5076  F1=0.4628  F1w=0.6733
       modality_w: cpg=0.520 mirna=0.480  |  val_loss=0.9029
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  25/150
[Train] Acc=0.8828  P=0.8836  R=0.8857  F1=0.8845  F1w=0.8827
[Val  ] Acc=0.8288  P=0.6010  R=0.6546  F1=0.6231  F1w=0.8306
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.6042
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  30/150
[Train] Acc=0.9422  P=0.9398  R=0.9401  F1=0.9398  F1w=0.9418
[Val  ] Acc=0.8288  P=0.6621  R=0.6947  F1=0.6749  F1w=0.8393
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.6302
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_4.pt
Fold 4 | Epoch  35/150
[Train] Acc=0.9535  P=0.9513  R=0.9521  F1=0.9516  F1w=0.9533
[Val  ] Acc=0.8559  P=0.6887  R=0.6681  F1=0.6730  F1w=0.8626
       modality_w: cpg=0.524 mirna=0.476  |  val_loss=0.6568
Fold 4 | Epoch  40/150
[Train] Acc=0.9711  P=0.9738  R=0.9707  F1=0.9717  F1w=0.9709
[Val  ] Acc=0.8378  P=0.6677  R=0.6664  F1=0.6565  F1w=0.8493
       modality_w: cpg=0.523 mirna=0.477  |  val_loss=0.6718
Fold 4 | Epoch  45/150
[Train] Acc=0.9695  P=0.9703  R=0.9690  F1=0.9686  F1w=0.9696
[Val  ] Acc=0.8739  P=0.6891  R=0.6734  F1=0.6760  F1w=0.8726
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.7193
Fold 4 | Epoch  50/150
[Train] Acc=0.9807  P=0.9802  R=0.9813  F1=0.9805  F1w=0.9807
[Val  ] Acc=0.8739  P=0.7054  R=0.6734  F1=0.6851  F1w=0.8754
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.7068
⏹️  Early stopping at epoch 52 (Fold 4)

📊 Test - Fold 4
[Test ] Acc=0.8306  P=0.6724  R=0.6579  F1=0.6516  F1w=0.8412
✅ Best val F1: 0.7182  |  Best val loss: 0.5134
✅ Test F1:     0.6516

📋 Classification Report - Fold 4
              precision    recall  f1-score   support

         CIN     0.9375    0.8400    0.8861       125
          GS     0.5625    0.8571    0.6792        21
         MSI     0.8621    0.9259    0.8929        27
      HM-SNV     0.0000    0.0000    0.0000         4
         EBV     1.0000    0.6667    0.8000         6

    accuracy                         0.8306       183
   macro avg     0.6724    0.6579    0.6516       183
weighted avg     0.8649    0.8306    0.8412       183


🎯 Per-class F1 - Fold 4
   0:CIN       F1=0.8861
   1:GS        F1=0.6792
   2:MSI       F1=0.8929
   3:HM-SNV    F1=0.0000
   4:EBV       F1=0.8000
  📄 Confusion matrix (absolute) saved: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/visualizations/fold_4/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 4
   cpg  : std=0.0674  max=0.3189  nnz=0.639  global_w=0.524
   mirna: std=0.0970  max=0.5030  nnz=0.544  global_w=0.476

🧬 Per-cancer-type F1 - Fold 4
     Cancer      N      F1
       COAD     61  0.8668
       ESCA     12  0.4286
       READ     31  0.6451
       STAD     79  0.6016

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
   Gene-Pathway edges : 15,290 unique
   Parsing miRNA family info... 1,432 unique edges
   miRNA-Family edges : 1,432 unique
   Building CpG↔miRNA co-regulation edges... 18,380 edges
   CpG↔miRNA edges : 18,380
⚖️  Using neutral class weights / focal_alpha: all ones

🧠 Fold 5 params: 833,352
🚀 Training Fold 5...  scheduler=onecycle
Fold 5 | Epoch   1/150
[Train] Acc=0.2119  P=0.2070  R=0.2133  F1=0.1732  F1w=0.1738
[Val  ] Acc=0.0270  P=0.0082  R=0.1500  F1=0.0156  F1w=0.0028
       modality_w: cpg=0.500 mirna=0.500  |  val_loss=1.8468
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch   5/150
[Train] Acc=0.2697  P=0.2766  R=0.2683  F1=0.2349  F1w=0.2356
[Val  ] Acc=0.1171  P=0.3037  R=0.3466  F1=0.1167  F1w=0.1329
       modality_w: cpg=0.502 mirna=0.498  |  val_loss=1.6804
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  10/150
[Train] Acc=0.4992  P=0.4841  R=0.4915  F1=0.4721  F1w=0.4764
[Val  ] Acc=0.6577  P=0.4706  R=0.4860  F1=0.4431  F1w=0.6719
       modality_w: cpg=0.507 mirna=0.493  |  val_loss=1.3103
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  15/150
[Train] Acc=0.7239  P=0.7293  R=0.7327  F1=0.7293  F1w=0.7218
[Val  ] Acc=0.6126  P=0.5794  R=0.5621  F1=0.5531  F1w=0.6778
       modality_w: cpg=0.508 mirna=0.492  |  val_loss=1.0916
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  20/150
[Train] Acc=0.8074  P=0.8123  R=0.8111  F1=0.8108  F1w=0.8068
[Val  ] Acc=0.7207  P=0.6015  R=0.6291  F1=0.6010  F1w=0.7574
       modality_w: cpg=0.514 mirna=0.486  |  val_loss=0.9158
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  25/150
[Train] Acc=0.8828  P=0.8856  R=0.8856  F1=0.8850  F1w=0.8824
[Val  ] Acc=0.8018  P=0.6234  R=0.6853  F1=0.6401  F1w=0.8154
       modality_w: cpg=0.518 mirna=0.482  |  val_loss=0.6797
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  30/150
[Train] Acc=0.9326  P=0.9309  R=0.9314  F1=0.9310  F1w=0.9324
[Val  ] Acc=0.8108  P=0.5841  R=0.6566  F1=0.6122  F1w=0.8123
       modality_w: cpg=0.522 mirna=0.478  |  val_loss=0.7566
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  35/150
[Train] Acc=0.9615  P=0.9618  R=0.9629  F1=0.9622  F1w=0.9612
[Val  ] Acc=0.8108  P=0.6457  R=0.6595  F1=0.6490  F1w=0.8253
       modality_w: cpg=0.526 mirna=0.474  |  val_loss=0.6355
Fold 5 | Epoch  40/150
[Train] Acc=0.9663  P=0.9673  R=0.9677  F1=0.9674  F1w=0.9662
[Val  ] Acc=0.8288  P=0.6604  R=0.6677  F1=0.6622  F1w=0.8432
       modality_w: cpg=0.528 mirna=0.472  |  val_loss=0.6758
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  45/150
[Train] Acc=0.9486  P=0.9490  R=0.9493  F1=0.9491  F1w=0.9486
[Val  ] Acc=0.8288  P=0.7018  R=0.6352  F1=0.6556  F1w=0.8416
       modality_w: cpg=0.530 mirna=0.470  |  val_loss=0.7299
  💾 Saved checkpoint: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/best_model_fold_5.pt
Fold 5 | Epoch  50/150
[Train] Acc=0.9775  P=0.9771  R=0.9765  F1=0.9764  F1w=0.9775
[Val  ] Acc=0.8288  P=0.6748  R=0.6718  F1=0.6723  F1w=0.8445
       modality_w: cpg=0.532 mirna=0.468  |  val_loss=0.7856
Fold 5 | Epoch  55/150
[Train] Acc=0.9823  P=0.9831  R=0.9832  F1=0.9830  F1w=0.9823
[Val  ] Acc=0.8198  P=0.6584  R=0.6621  F1=0.6586  F1w=0.8351
       modality_w: cpg=0.534 mirna=0.466  |  val_loss=0.9099
Fold 5 | Epoch  60/150
[Train] Acc=0.9872  P=0.9878  R=0.9874  F1=0.9875  F1w=0.9871
[Val  ] Acc=0.8559  P=0.6846  R=0.6570  F1=0.6687  F1w=0.8558
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.8641
Fold 5 | Epoch  65/150
[Train] Acc=0.9856  P=0.9850  R=0.9849  F1=0.9849  F1w=0.9855
[Val  ] Acc=0.8559  P=0.6558  R=0.6883  F1=0.6665  F1w=0.8644
       modality_w: cpg=0.536 mirna=0.464  |  val_loss=0.8959
⏹️  Early stopping at epoch 66 (Fold 5)

📊 Test - Fold 5
[Test ] Acc=0.8470  P=0.6816  R=0.7474  F1=0.7050  F1w=0.8631
✅ Best val F1: 0.7169  |  Best val loss: 0.6093
✅ Test F1:     0.7050

📋 Classification Report - Fold 5
              precision    recall  f1-score   support

         CIN     0.9643    0.8710    0.9153       124
          GS     0.6957    0.7273    0.7111        22
         MSI     0.8000    0.8889    0.8421        27
      HM-SNV     0.0909    0.2500    0.1333         4
         EBV     0.8571    1.0000    0.9231         6

    accuracy                         0.8470       183
   macro avg     0.6816    0.7474    0.7050       183
weighted avg     0.8851    0.8470    0.8631       183


🎯 Per-class F1 - Fold 5
   0:CIN       F1=0.9153
   1:GS        F1=0.7111
   2:MSI       F1=0.8421
   3:HM-SNV    F1=0.1333
   4:EBV       F1=0.9231
  📄 Confusion matrix (absolute) saved: results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/seed_42/checkpoints/visualizations/fold_5/confusion_matrix_test_absolute.csv

🔍 Attention Stats - Fold 5
   cpg  : std=0.0673  max=0.3006  nnz=0.570  global_w=0.531
   mirna: std=0.0884  max=0.4566  nnz=0.611  global_w=0.469

🧬 Per-cancer-type F1 - Fold 5
     Cancer      N      F1
       COAD     76  0.4712
       ESCA     19  0.6571
       READ     17  0.7966
       STAD     71  0.7109

📈 5-fold CV summary
  ACCURACY   : mean=0.8353  std=0.0156
  PRECISION  : mean=0.6513  std=0.0257
  RECALL     : mean=0.6961  std=0.0379
  F1         : mean=0.6648  std=0.0206
  F1_WEIGHTED: mean=0.8447  std=0.0155

🧬 Per-cancer-type F1 (5-fold mean ± std):
    Cancer  N/fold   F1 mean   F1 std
      COAD    68.0    0.6232   0.1329
      ESCA    15.8    0.6085   0.2107
      READ    23.6    0.5866   0.1209
      STAD    76.0    0.6550   0.0432

🎯 Per-class F1 (5-fold mean ± std):
         Class   F1 mean   F1 std
             0    0.8992   0.0171
             1    0.6403   0.0887
             2    0.8574   0.0367
             3    0.0267   0.0533
             4    0.9007   0.0677

✅ Seed 42 done — F1 macro = 0.6648, F1 weighted = 0.8447



══════════════════════════════════════════════════════════════════════════════
 📋 COPY KHỐI BÊN DƯỚI (đến dòng ═ tiếp theo) → PASTE VÀO ĐẦU docs/RESULTS.md
══════════════════════════════════════════════════════════════════════════════

## [2026-05-08 07:54] `gi_08c_balanced_sampler_ce` — Macro F1: **0.6648 ± 0.0000**

**Config:** `configs/quickwins/gi_08c_balanced_sampler_ce.yaml`  |  **Seeds:** [42]  |  **N runs:** 1 × 5 folds

| Metric            | Mean ± Std      | Per-seed means |
| ----------------- | --------------- | -------------- |
| **Macro F1**      | 0.6648 ± 0.0000 | 0.6648         |
| Weighted F1       | 0.8447 ± 0.0000 | 0.8447         |
| Accuracy          | 0.8353 ± 0.0000 | 0.8353         |
| Precision (macro) | 0.6513 ± 0.0000 | 0.6513         |
| Recall (macro)    | 0.6961 ± 0.0000 | 0.6961         |

**Per-fold F1 (macro):**

| Seed | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean   |
| ---- | ------ | ------ | ------ | ------ | ------ | ------ |
| 42   | 0.6491 | 0.6633 | 0.6552 | 0.6516 | 0.7050 | 0.6648 |

**Per-class F1 (mean across seeds):**

| Class   | Seed 42 | Avg    |
| ------- | ------- | ------ |
| 0 (CIN) | 0.8992  | 0.8992 |

---

══════════════════════════════════════════════════════════════════════════════
 ↑↑↑ COPY KHỐI BÊN TRÊN — PASTE VÀO ĐẦU docs/RESULTS.md (sau dòng tiêu đề) ↑↑↑
══════════════════════════════════════════════════════════════════════════════

💾 JSON backup (KHÔNG cần download): results/gi_08c_balanced_sampler_ce_multiseed_20260508_072600/multi_seed_summary.json