"""
train.py
--------
Script chính để train model. Chạy trên Colab:

  !python train.py --config configs/config.yaml
"""

import argparse
import yaml
import torch
from torch.utils.data import DataLoader

from src.data.dataset      import build_datasets
from src.data.graph_builder import build_hetero_graph
from src.model             import GIACModel
from src.utils             import set_seed, compute_metrics, print_metrics, \
                                  save_checkpoint, EarlyStopping


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--resume", default=None, help="Path to checkpoint để resume")
    return parser.parse_args()


def train_epoch(model, loader, optimizer, graph, device):
    model.train()
    total_loss = 0.0
    all_preds, all_labels = [], []

    for batch in loader:
        # Move batch to device
        batch = {k: v.to(device) for k, v in batch.items()}

        optimizer.zero_grad()
        logits = model(batch, graph)
        loss   = model.compute_loss(logits, batch["label"])

        loss.backward()
        # Gradient clipping — tránh exploding gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        total_loss += loss.item()
        preds = logits.argmax(dim=-1).cpu().tolist()
        all_preds.extend(preds)
        all_labels.extend(batch["label"].cpu().tolist())

    metrics = compute_metrics(all_labels, all_preds)
    metrics["loss"] = total_loss / len(loader)
    return metrics


@torch.no_grad()
def eval_epoch(model, loader, graph, device):
    model.eval()
    all_preds, all_labels = [], []

    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        logits = model(batch, graph)
        preds  = logits.argmax(dim=-1).cpu().tolist()
        all_preds.extend(preds)
        all_labels.extend(batch["label"].cpu().tolist())

    return compute_metrics(all_labels, all_preds)


def main():
    args = parse_args()

    # ── Load config ──────────────────────────────────────────────────
    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    set_seed(cfg["training"]["seed"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥️  Device: {device}")

    # ── Data ─────────────────────────────────────────────────────────
    datasets, feature_names, dims = build_datasets(cfg["data"], cfg["training"]["seed"])
    print(f"\n📐 Feature dims: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")

    train_loader = DataLoader(
        datasets["train"],
        batch_size  = cfg["training"]["batch_size"],
        shuffle     = True,
        num_workers = 2,
        pin_memory  = True,
    )
    val_loader  = DataLoader(datasets["val"],  batch_size=64, shuffle=False)
    test_loader = DataLoader(datasets["test"], batch_size=64, shuffle=False)

    # ── Graph ─────────────────────────────────────────────────────────
    print("\n🔨 Building Heterogeneous Graph...")
    graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device=str(device))

    # ── Model ─────────────────────────────────────────────────────────
    model = GIACModel(dims, cfg["model"], cfg["training"]).to(device)
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n🧠 Model parameters: {n_params:,}")

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr           = cfg["training"]["learning_rate"],
        weight_decay = cfg["training"]["weight_decay"],
    )
    # Cosine LR scheduler
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=cfg["training"]["epochs"]
    )

    early_stop = EarlyStopping(patience=cfg["training"]["patience"])
    best_val_f1 = 0.0
    log_interval = cfg["logging"]["log_interval"]
    save_dir     = cfg["logging"]["save_dir"]

    # ── Training loop ─────────────────────────────────────────────────
    print("\n🚀 Bắt đầu training...\n")
    for epoch in range(1, cfg["training"]["epochs"] + 1):
        train_metrics = train_epoch(model, train_loader, optimizer, graph, device)
        val_metrics   = eval_epoch(model, val_loader, graph, device)
        scheduler.step()

        if epoch % log_interval == 0 or epoch == 1:
            print(f"Epoch {epoch:3d}/{cfg['training']['epochs']}")
            print_metrics(train_metrics, "Train")
            print_metrics(val_metrics,   "Val  ")
            # In modality weights (xem omic nào đang được model ưu tiên)
            w = model.sparse_cross_attn.modality_weights.detach().cpu()
            print(f"       Modality weights: gene={w[0]:.3f}, meth={w[1]:.3f}, mirna={w[2]:.3f}")
            print()

        # Save best checkpoint
        if val_metrics["f1"] > best_val_f1:
            best_val_f1 = val_metrics["f1"]
            save_checkpoint(
                model, optimizer, epoch, val_metrics,
                path=f"{save_dir}/best_model.pt"
            )

        if early_stop.step(val_metrics["f1"]):
            print(f"⏹️  Early stopping tại epoch {epoch}")
            break

    # ── Final evaluation trên test set ────────────────────────────────
    print("\n📊 Đánh giá trên Test set (ESCA)...")
    # Load best checkpoint
    ckpt = torch.load(f"{save_dir}/best_model.pt", map_location=device)
    model.load_state_dict(ckpt["model"])

    test_metrics = eval_epoch(model, test_loader, graph, device)
    print_metrics(test_metrics, "Test ")
    print(f"\n✅ Best val F1: {best_val_f1:.4f}")
    print(f"✅ Test F1:     {test_metrics['f1']:.4f}")


if __name__ == "__main__":
    main()
