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
!git clone https://github.com/YOUR_USERNAME/giac_project.git
%cd giac_project
!pip install -r requirements.txt
!python train.py --config configs/config.yaml
```
