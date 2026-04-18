# GIAC Cancer Subtype Classification
## HeteroGAT + Sparse Cross-Attention (cải tiến từ MoXGATE)

### Cấu trúc project
```
giac_project/
├── README.md
├── requirements.txt
├── configs/
│   └── config.yaml          # Toàn bộ hyperparameter
├── src/
│   ├── data/
│   │   ├── dataset.py       # Load & preprocess data MoXGATE
│   │   └── graph_builder.py # Xây dựng Heterogeneous Graph (emQTL + STRING + miRTarBase)
│   ├── models/
│   │   ├── gat_encoder.py   # Module 1: GAT Encoder cho từng omic
│   │   ├── sparse_attention.py  # Module 2: Sparsemax Cross-Attention
│   │   └── classifier.py    # Module 3: Focal Loss Classifier + interpretability
│   ├── model.py             # Ghép 3 module thành full model
│   └── utils.py             # Metrics, logging, helpers
├── train.py                 # Script chính để train
├── evaluate.py              # Evaluate + xuất top-K gene per patient
└── notebooks/
    └── colab_runner.ipynb   # Notebook chạy trên Colab
```

### Chạy trên Colab
```python
!git clone https://github.com/maivanquan-00/giac_project_colab
%cd giac_project
!pip install -r requirements.txt
!python train.py --config configs/config.yaml
```

### Chạy trên Kaggle (khuyến nghị)
```bash
pip install -r requirements.txt
```

Quick check (CPU-friendly, chạy 1-2 folds trước):
```bash
python train.py --config configs/config.quick_check.yaml --cv-folds 1
python train.py --config configs/config.quick_check.yaml --cv-folds 2
```

Evaluate checkpoint mới nhất (tự động lấy từ logging.save_dir nếu không truyền --checkpoint):
```bash
python evaluate.py --config configs/config.quick_check.yaml --split test
```

Full run (khi quick check ổn):
```bash
python train.py --config configs/config.yaml --cv-folds 5
python evaluate.py --config configs/config.yaml --split test
```
