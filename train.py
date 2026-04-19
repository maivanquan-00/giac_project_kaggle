# """
# train.py
# --------
# Train GIAC with either a single split or stratified cross-validation.
# """

# import argparse
# import os

# import numpy as np
# import torch
# from torch.utils.data import DataLoader
# import yaml

# from src.data.dataset import build_cv_datasets, build_datasets
# from src.data.graph_builder import build_hetero_graph
# from src.model import GIACModel
# from src.utils import (
#     EarlyStopping,
#     compute_metrics,
#     ensure_dir,
#     plot_confusion_matrix_figure,
#     plot_cv_metrics,
#     plot_split_class_distribution,
#     plot_training_curves,
#     print_classification_report,
#     print_metrics,
#     save_checkpoint,
#     save_confusion_matrix_csv,
#     set_seed,
# )


# SUBTYPE_NAMES = ["CIN", "GS", "MSI", "HM-SNV", "EBV"]


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--config", default="configs/config.yaml")
#     parser.add_argument("--cv-folds", type=int, default=None, help="Override number of CV folds")
#     return parser.parse_args()


# def train_epoch(model, loader, optimizer, graph, device, scheduler=None):
#     model.train()
#     total_loss = 0.0
#     all_preds, all_labels = [], []

#     for batch in loader:
#         batch = {k: v.to(device) for k, v in batch.items()}

#         optimizer.zero_grad()
#         logits = model(batch, graph)
#         loss = model.compute_loss(logits, batch["label"])
#         loss.backward()
#         torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
#         optimizer.step()
#         if scheduler is not None:
#             scheduler.step()

#         total_loss += loss.item()
#         all_preds.extend(logits.argmax(dim=-1).cpu().tolist())
#         all_labels.extend(batch["label"].cpu().tolist())

#     metrics = compute_metrics(all_labels, all_preds)
#     metrics["loss"] = total_loss / max(len(loader), 1)
#     return metrics


# @torch.no_grad()
# def eval_epoch(model, loader, graph, device, return_predictions: bool = False):
#     model.eval()
#     all_preds, all_labels = [], []

#     for batch in loader:
#         batch = {k: v.to(device) for k, v in batch.items()}
#         logits = model(batch, graph)
#         all_preds.extend(logits.argmax(dim=-1).cpu().tolist())
#         all_labels.extend(batch["label"].cpu().tolist())

#     metrics = compute_metrics(all_labels, all_preds)
#     if return_predictions:
#         return metrics, all_labels, all_preds
#     return metrics


# @torch.no_grad()
# def collect_gate_stats(model, loader, graph, device):
#     """Thu thập patient gate weights từ test set để kiểm tra fusion có hoạt động."""
#     model.eval()
#     all_gates = []
#     for batch in loader:
#         batch = {k: v.to(device) for k, v in batch.items()}
#         _, _, weights = model(batch, graph, return_interpretability=True)
#         all_gates.append(weights["patient"].cpu())
#     gates = torch.cat(all_gates, dim=0)  # (N, 3)
#     return {
#         "mean": gates.mean(dim=0).tolist(),
#         "std":  gates.std(dim=0).tolist(),
#         "min":  gates.min(dim=0).values.tolist(),
#         "max":  gates.max(dim=0).values.tolist(),
#     }


# def make_loaders(datasets: dict, train_batch_size: int):
#     train_loader = DataLoader(
#         datasets["train"],
#         batch_size=train_batch_size,
#         shuffle=True,
#         num_workers=2,
#         pin_memory=True,
#     )
#     val_loader = DataLoader(datasets["val"], batch_size=64, shuffle=False)
#     test_loader = DataLoader(datasets["test"], batch_size=64, shuffle=False)
#     return train_loader, val_loader, test_loader


# def compute_class_weights(dataset, num_classes: int, device):
#     labels = dataset.label.cpu().numpy()
#     counts = np.bincount(labels, minlength=num_classes).astype(np.float32)
#     counts = np.clip(counts, a_min=1.0, a_max=None)
#     weights = len(labels) / (num_classes * counts)
#     weights = weights / weights.mean()
#     return torch.tensor(weights, dtype=torch.float32, device=device)


# def fit_one_split(cfg, datasets, feature_names, dims, metadata, device, fold_name: str):
#     train_loader, val_loader, test_loader = make_loaders(
#         datasets, cfg["training"]["batch_size"]
#     )
#     graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device=str(device))

#     model = GIACModel(dims, cfg["model"], cfg["training"]).to(device)
#     model.set_class_weights(
#         compute_class_weights(datasets["train"], cfg["model"]["num_classes"], device)
#     )

#     optimizer = torch.optim.AdamW(
#         model.parameters(),
#         lr=cfg["training"]["learning_rate"],
#         weight_decay=cfg["training"]["weight_decay"],
#     )

#     scheduler_name = cfg["training"].get("scheduler", "onecycle").lower()
#     if scheduler_name == "onecycle":
#         scheduler = torch.optim.lr_scheduler.OneCycleLR(
#             optimizer,
#             max_lr=cfg["training"].get("max_learning_rate", cfg["training"]["learning_rate"] * 5.0),
#             epochs=cfg["training"]["epochs"],
#             steps_per_epoch=max(len(train_loader), 1),
#             pct_start=cfg["training"].get("onecycle_pct_start", 0.1),
#             div_factor=cfg["training"].get("onecycle_div_factor", 10.0),
#             final_div_factor=cfg["training"].get("onecycle_final_div_factor", 100.0),
#         )
#         scheduler_step_per_batch = True
#     else:
#         scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
#             optimizer, T_max=cfg["training"]["epochs"]
#         )
#         scheduler_step_per_batch = False

#     early_stop = EarlyStopping(patience=cfg["training"]["patience"])

#     n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
#     print(f"\n🧠 {fold_name} model parameters: {n_params:,}")
#     print(f"🚀 Bắt đầu training {fold_name.lower()}...\n")
#     print(f"🗓️  Scheduler: {scheduler_name}")

#     best_val_f1 = 0.0
#     save_dir = cfg["logging"]["save_dir"]
#     viz_dir = os.path.join(save_dir, "visualizations", fold_name.lower().replace(" ", "_"))
#     ensure_dir(viz_dir)
#     ckpt_name = "best_model.pt" if fold_name == "Single split" else f"best_model_{fold_name.lower().replace(' ', '_')}.pt"
#     ckpt_path = os.path.join(save_dir, ckpt_name)
#     history = {"train_loss": [], "train_f1": [], "val_f1": []}

#     plot_split_class_distribution(
#         {
#             "train": datasets["train"].label.cpu().numpy(),
#             "val": datasets["val"].label.cpu().numpy(),
#             "test": datasets["test"].label.cpu().numpy(),
#         },
#         path=os.path.join(viz_dir, "class_distribution.png"),
#         title=f"{fold_name} - Class Distribution",
#         class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
#     )

#     for epoch in range(1, cfg["training"]["epochs"] + 1):
#         train_metrics = train_epoch(
#             model,
#             train_loader,
#             optimizer,
#             graph,
#             device,
#             scheduler=scheduler if scheduler_step_per_batch else None,
#         )
#         val_metrics = eval_epoch(model, val_loader, graph, device)
#         if not scheduler_step_per_batch:
#             scheduler.step()
#         history["train_loss"].append(train_metrics["loss"])
#         history["train_f1"].append(train_metrics["f1"])
#         history["val_f1"].append(val_metrics["f1"])

#         if epoch % cfg["logging"]["log_interval"] == 0 or epoch == 1:
#             print(f"{fold_name} | Epoch {epoch:3d}/{cfg['training']['epochs']}")
#             print_metrics(train_metrics, "Train")
#             print_metrics(val_metrics, "Val  ")


#         if val_metrics["f1"] > best_val_f1:
#             best_val_f1 = val_metrics["f1"]
#             save_checkpoint(
#                 model,
#                 optimizer,
#                 epoch,
#                 val_metrics,
#                 path=ckpt_path,
#                 extra_state={
#                     "preprocessing": metadata["preprocess"],
#                     "split_info": metadata["split_info"],
#                     "feature_names": feature_names,
#                     "dims": dims,
#                     "fold_name": fold_name,
#                     "config": cfg,
#                     "history": history,
#                 },
#             )

#         if early_stop.step(val_metrics["f1"]):
#             print(f"⏹️  Early stopping tại epoch {epoch} cho {fold_name}")
#             break

#     ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
#     model.load_state_dict(ckpt["model"])
#     test_metrics, test_labels, test_preds = eval_epoch(
#         model, test_loader, graph, device, return_predictions=True
#     )

#     print(f"\n📊 Đánh giá trên Test set - {fold_name}")
#     print_metrics(test_metrics, "Test ")
#     print(f"✅ Best val F1: {best_val_f1:.4f}")
#     print(f"✅ Test F1:     {test_metrics['f1']:.4f}")

#     plot_training_curves(
#         history,
#         path=os.path.join(viz_dir, "training_curves.png"),
#         title=fold_name,
#     )
#     plot_confusion_matrix_figure(
#         test_labels,
#         test_preds,
#         path=os.path.join(viz_dir, "confusion_matrix_test.png"),
#         title=f"{fold_name} - Test Confusion Matrix",
#         class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
#         normalize=True,
#     )

#     # ── A1: Per-class Classification Report ───────────────────────
#     print(f"\n📋 Classification Report - {fold_name}")
#     print_classification_report(
#         test_labels, test_preds,
#         class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
#     )
#     save_confusion_matrix_csv(
#         test_labels, test_preds,
#         path=os.path.join(viz_dir, "confusion_matrix_test_absolute.csv"),
#         class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
#     )

#     # ── A3: Patient Gate Statistics ────────────────────────────────
#     gate_stats = collect_gate_stats(model, test_loader, graph, device)
#     print(f"\n🔍 Patient Gate Statistics - {fold_name}")
#     for i, name in enumerate(["gene", "meth", "mirna"]):
#         print(
#             f"   {name:5s}: mean={gate_stats['mean'][i]:.4f}  "
#             f"std={gate_stats['std'][i]:.4f}  "
#             f"min={gate_stats['min'][i]:.4f}  "
#             f"max={gate_stats['max'][i]:.4f}"
#         )

#     return {
#         "fold": fold_name,
#         "best_val_f1": best_val_f1,
#         "test_metrics": test_metrics,
#         "checkpoint": ckpt_path,
#         "viz_dir": viz_dir,
#     }


# def summarize_cv(results: list):
#     metric_names = ["accuracy", "precision", "recall", "f1"]
#     print("\n📈 5-fold CV summary")
#     for name in metric_names:
#         values = np.array([result["test_metrics"][name] for result in results], dtype=np.float64)
#         print(f"  {name.upper():9s}: mean={values.mean():.4f}  std={values.std(ddof=0):.4f}")


# def main():
#     args = parse_args()

#     with open(args.config) as f:
#         cfg = yaml.safe_load(f)

#     set_seed(cfg["training"]["seed"])
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     print(f"🖥️  Device: {device}")

#     cv_folds = args.cv_folds if args.cv_folds is not None else cfg.get("preprocessing", {}).get("cv_folds", 5)

#     if cv_folds and cv_folds > 1:
#         fold_packages = build_cv_datasets(cfg["data"], cfg["training"]["seed"], n_splits=cv_folds)
#         results = []
#         for fold_package in fold_packages:
#             fold_no = fold_package["fold"]
#             datasets, feature_names, dims, metadata = fold_package["datasets"]
#             print(
#                 f"\n📐 Fold {fold_no}: "
#                 f"gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}"
#             )
#             results.append(
#                 fit_one_split(
#                     cfg,
#                     datasets,
#                     feature_names,
#                     dims,
#                     metadata,
#                     device,
#                     fold_name=f"Fold {fold_no}",
#                 )
#             )
#         summarize_cv(results)
#         plot_cv_metrics(
#             results,
#             path=os.path.join(cfg["logging"]["save_dir"], "visualizations", "cv_metrics_summary.png"),
#             title="5-Fold CV Test Metrics",
#         )
#     else:
#         datasets, feature_names, dims, metadata = build_datasets(
#             cfg["data"], cfg["training"]["seed"]
#         )
#         print(f"\n📐 Feature dims: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
#         fit_one_split(cfg, datasets, feature_names, dims, metadata, device, fold_name="Single split")


# if __name__ == "__main__":
#     main()


# """
# train.py
# --------
# Train GIAC with either a single split or stratified cross-validation.
# """

# import argparse
# import os

# import numpy as np
# import torch
# from torch.utils.data import DataLoader
# import yaml

# from src.data.dataset import build_cv_datasets, build_datasets
# from src.data.graph_builder import build_hetero_graph
# from src.model import GIACModel
# from src.utils import (
#     EarlyStopping,
#     compute_metrics,
#     ensure_dir,
#     plot_confusion_matrix_figure,
#     plot_cv_metrics,
#     plot_split_class_distribution,
#     plot_training_curves,
#     print_classification_report,
#     print_metrics,
#     save_checkpoint,
#     save_confusion_matrix_csv,
#     set_seed,
# )


# SUBTYPE_NAMES = ["CIN", "GS", "MSI", "HM-SNV", "EBV"]


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--config", default="configs/config.yaml")
#     parser.add_argument("--cv-folds", type=int, default=None, help="Override number of CV folds")
#     return parser.parse_args()


# def train_epoch(model, loader, optimizer, graph, device, scheduler=None):
#     model.train()
#     total_loss = 0.0
#     all_preds, all_labels = [], []

#     for batch in loader:
#         batch = {k: v.to(device) for k, v in batch.items()}

#         optimizer.zero_grad()
#         logits = model(batch, graph)
#         loss = model.compute_loss(logits, batch["label"])
#         loss.backward()
#         torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
#         optimizer.step()
#         if scheduler is not None:
#             scheduler.step()

#         total_loss += loss.item()
#         all_preds.extend(logits.argmax(dim=-1).cpu().tolist())
#         all_labels.extend(batch["label"].cpu().tolist())

#     metrics = compute_metrics(all_labels, all_preds)
#     metrics["loss"] = total_loss / max(len(loader), 1)
#     return metrics


# @torch.no_grad()
# def eval_epoch(model, loader, graph, device, return_predictions: bool = False):
#     model.eval()
#     all_preds, all_labels = [], []

#     for batch in loader:
#         batch = {k: v.to(device) for k, v in batch.items()}
#         logits = model(batch, graph)
#         all_preds.extend(logits.argmax(dim=-1).cpu().tolist())
#         all_labels.extend(batch["label"].cpu().tolist())

#     metrics = compute_metrics(all_labels, all_preds)
#     if return_predictions:
#         return metrics, all_labels, all_preds
#     return metrics


# @torch.no_grad()
# def collect_gate_stats(model, loader, graph, device):
#     """Thu thập patient gate weights từ test set để kiểm tra fusion có hoạt động."""
#     model.eval()
#     all_gates = []
#     for batch in loader:
#         batch = {k: v.to(device) for k, v in batch.items()}
#         _, _, weights = model(batch, graph, return_interpretability=True)
#         all_gates.append(weights["patient"].cpu())
#     gates = torch.cat(all_gates, dim=0)  # (N, 3)
#     return {
#         "mean": gates.mean(dim=0).tolist(),
#         "std":  gates.std(dim=0).tolist(),
#         "min":  gates.min(dim=0).values.tolist(),
#         "max":  gates.max(dim=0).values.tolist(),
#     }


# def make_loaders(datasets: dict, train_batch_size: int):
#     train_loader = DataLoader(
#         datasets["train"],
#         batch_size=train_batch_size,
#         shuffle=True,
#         num_workers=2,
#         pin_memory=True,
#     )
#     val_loader = DataLoader(datasets["val"], batch_size=64, shuffle=False)
#     test_loader = DataLoader(datasets["test"], batch_size=64, shuffle=False)
#     return train_loader, val_loader, test_loader


# def compute_class_weights(dataset, num_classes: int, device):
#     labels = dataset.label.cpu().numpy()
#     counts = np.bincount(labels, minlength=num_classes).astype(np.float32)
#     counts = np.clip(counts, a_min=1.0, a_max=None)
#     weights = len(labels) / (num_classes * counts)
#     weights = weights / weights.mean()
#     return torch.tensor(weights, dtype=torch.float32, device=device)


# def fit_one_split(cfg, datasets, feature_names, dims, metadata, device, fold_name: str):
#     train_loader, val_loader, test_loader = make_loaders(
#         datasets, cfg["training"]["batch_size"]
#     )
#     graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device=str(device))

#     model = GIACModel(dims, cfg["model"], cfg["training"]).to(device)
#     model.set_class_weights(
#         compute_class_weights(datasets["train"], cfg["model"]["num_classes"], device)
#     )

#     optimizer = torch.optim.AdamW(
#         model.parameters(),
#         lr=cfg["training"]["learning_rate"],
#         weight_decay=cfg["training"]["weight_decay"],
#     )

#     scheduler_name = cfg["training"].get("scheduler", "onecycle").lower()
#     if scheduler_name == "onecycle":
#         scheduler = torch.optim.lr_scheduler.OneCycleLR(
#             optimizer,
#             max_lr=cfg["training"].get("max_learning_rate", cfg["training"]["learning_rate"] * 5.0),
#             epochs=cfg["training"]["epochs"],
#             steps_per_epoch=max(len(train_loader), 1),
#             pct_start=cfg["training"].get("onecycle_pct_start", 0.1),
#             div_factor=cfg["training"].get("onecycle_div_factor", 10.0),
#             final_div_factor=cfg["training"].get("onecycle_final_div_factor", 100.0),
#         )
#         scheduler_step_per_batch = True
#     else:
#         scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
#             optimizer, T_max=cfg["training"]["epochs"]
#         )
#         scheduler_step_per_batch = False

#     early_stop = EarlyStopping(patience=cfg["training"]["patience"])

#     n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
#     print(f"\n🧠 {fold_name} model parameters: {n_params:,}")
#     print(f"🚀 Bắt đầu training {fold_name.lower()}...\n")
#     print(f"🗓️  Scheduler: {scheduler_name}")

#     best_val_f1 = 0.0
#     save_dir = cfg["logging"]["save_dir"]
#     viz_dir = os.path.join(save_dir, "visualizations", fold_name.lower().replace(" ", "_"))
#     ensure_dir(viz_dir)
#     ckpt_name = "best_model.pt" if fold_name == "Single split" else f"best_model_{fold_name.lower().replace(' ', '_')}.pt"
#     ckpt_path = os.path.join(save_dir, ckpt_name)
#     history = {"train_loss": [], "train_f1": [], "val_f1": []}

#     plot_split_class_distribution(
#         {
#             "train": datasets["train"].label.cpu().numpy(),
#             "val": datasets["val"].label.cpu().numpy(),
#             "test": datasets["test"].label.cpu().numpy(),
#         },
#         path=os.path.join(viz_dir, "class_distribution.png"),
#         title=f"{fold_name} - Class Distribution",
#         class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
#     )

#     for epoch in range(1, cfg["training"]["epochs"] + 1):
#         train_metrics = train_epoch(
#             model,
#             train_loader,
#             optimizer,
#             graph,
#             device,
#             scheduler=scheduler if scheduler_step_per_batch else None,
#         )
#         val_metrics = eval_epoch(model, val_loader, graph, device)
#         if not scheduler_step_per_batch:
#             scheduler.step()
#         history["train_loss"].append(train_metrics["loss"])
#         history["train_f1"].append(train_metrics["f1"])
#         history["val_f1"].append(val_metrics["f1"])

#         if epoch % cfg["logging"]["log_interval"] == 0 or epoch == 1:
#             print(f"{fold_name} | Epoch {epoch:3d}/{cfg['training']['epochs']}")
#             print_metrics(train_metrics, "Train")
#             print_metrics(val_metrics, "Val  ")
#             alpha = torch.sigmoid(model.fusion_alpha).item()
#             print(f"       fusion_alpha={alpha:.3f}  (GAT={alpha:.2f}, Shortcut={1-alpha:.2f})")


#         if val_metrics["f1"] > best_val_f1:
#             best_val_f1 = val_metrics["f1"]
#             save_checkpoint(
#                 model,
#                 optimizer,
#                 epoch,
#                 val_metrics,
#                 path=ckpt_path,
#                 extra_state={
#                     "preprocessing": metadata["preprocess"],
#                     "split_info": metadata["split_info"],
#                     "feature_names": feature_names,
#                     "dims": dims,
#                     "fold_name": fold_name,
#                     "config": cfg,
#                     "history": history,
#                 },
#             )

#         if early_stop.step(val_metrics["f1"]):
#             print(f"⏹️  Early stopping tại epoch {epoch} cho {fold_name}")
#             break

#     ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
#     model.load_state_dict(ckpt["model"])
#     test_metrics, test_labels, test_preds = eval_epoch(
#         model, test_loader, graph, device, return_predictions=True
#     )

#     print(f"\n📊 Đánh giá trên Test set - {fold_name}")
#     print_metrics(test_metrics, "Test ")
#     print(f"✅ Best val F1: {best_val_f1:.4f}")
#     print(f"✅ Test F1:     {test_metrics['f1']:.4f}")

#     plot_training_curves(
#         history,
#         path=os.path.join(viz_dir, "training_curves.png"),
#         title=fold_name,
#     )
#     plot_confusion_matrix_figure(
#         test_labels,
#         test_preds,
#         path=os.path.join(viz_dir, "confusion_matrix_test.png"),
#         title=f"{fold_name} - Test Confusion Matrix",
#         class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
#         normalize=True,
#     )

#     # ── A1: Per-class Classification Report ───────────────────────
#     print(f"\n📋 Classification Report - {fold_name}")
#     print_classification_report(
#         test_labels, test_preds,
#         class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
#     )
#     save_confusion_matrix_csv(
#         test_labels, test_preds,
#         path=os.path.join(viz_dir, "confusion_matrix_test_absolute.csv"),
#         class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
#     )

#     # ── A3: Patient Gate Statistics ────────────────────────────────
#     gate_stats = collect_gate_stats(model, test_loader, graph, device)
#     print(f"\n🔍 Patient Gate Statistics - {fold_name}")
#     for i, name in enumerate(["gene", "meth", "mirna"]):
#         print(
#             f"   {name:5s}: mean={gate_stats['mean'][i]:.4f}  "
#             f"std={gate_stats['std'][i]:.4f}  "
#             f"min={gate_stats['min'][i]:.4f}  "
#             f"max={gate_stats['max'][i]:.4f}"
#         )

#     return {
#         "fold": fold_name,
#         "best_val_f1": best_val_f1,
#         "test_metrics": test_metrics,
#         "checkpoint": ckpt_path,
#         "viz_dir": viz_dir,
#     }


# def summarize_cv(results: list):
#     metric_names = ["accuracy", "precision", "recall", "f1"]
#     print("\n📈 5-fold CV summary")
#     for name in metric_names:
#         values = np.array([result["test_metrics"][name] for result in results], dtype=np.float64)
#         print(f"  {name.upper():9s}: mean={values.mean():.4f}  std={values.std(ddof=0):.4f}")


# def main():
#     args = parse_args()

#     with open(args.config) as f:
#         cfg = yaml.safe_load(f)

#     set_seed(cfg["training"]["seed"])
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     print(f"🖥️  Device: {device}")

#     cv_folds = args.cv_folds if args.cv_folds is not None else cfg.get("preprocessing", {}).get("cv_folds", 5)

#     if cv_folds and cv_folds > 1:
#         fold_packages = build_cv_datasets(cfg["data"], cfg["training"]["seed"], n_splits=cv_folds)
#         results = []
#         for fold_package in fold_packages:
#             fold_no = fold_package["fold"]
#             datasets, feature_names, dims, metadata = fold_package["datasets"]
#             print(
#                 f"\n📐 Fold {fold_no}: "
#                 f"gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}"
#             )
#             results.append(
#                 fit_one_split(
#                     cfg,
#                     datasets,
#                     feature_names,
#                     dims,
#                     metadata,
#                     device,
#                     fold_name=f"Fold {fold_no}",
#                 )
#             )
#         summarize_cv(results)
#         plot_cv_metrics(
#             results,
#             path=os.path.join(cfg["logging"]["save_dir"], "visualizations", "cv_metrics_summary.png"),
#             title="5-Fold CV Test Metrics",
#         )
#     else:
#         datasets, feature_names, dims, metadata = build_datasets(
#             cfg["data"], cfg["training"]["seed"]
#         )
#         print(f"\n📐 Feature dims: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
#         fit_one_split(cfg, datasets, feature_names, dims, metadata, device, fold_name="Single split")


# if __name__ == "__main__":
#     main()

"""
train.py
--------
Train GIAC with either a single split or stratified cross-validation.
"""

import argparse
import os

import numpy as np
import torch
from torch.utils.data import DataLoader
import yaml

from src.data.dataset import build_cv_datasets, build_datasets
from src.data.graph_builder import build_hetero_graph
from src.model import GIACModel
from src.utils import (
    EarlyStopping,
    compute_metrics,
    ensure_dir,
    plot_confusion_matrix_figure,
    plot_cv_metrics,
    plot_split_class_distribution,
    plot_training_curves,
    print_classification_report,
    print_metrics,
    save_checkpoint,
    save_confusion_matrix_csv,
    set_seed,
)


SUBTYPE_NAMES = ["CIN", "GS", "MSI", "HM-SNV", "EBV"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--cv-folds", type=int, default=None, help="Override number of CV folds")
    return parser.parse_args()


def train_epoch(model, loader, optimizer, graph, device, scheduler=None):
    model.train()
    total_loss = 0.0
    all_preds, all_labels = [], []

    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}

        optimizer.zero_grad()
        logits, patient_gate = model(batch, graph)
        loss = model.compute_loss(logits, batch["label"], patient_gate)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        if scheduler is not None:
            scheduler.step()

        total_loss += loss.item()
        all_preds.extend(logits.argmax(dim=-1).cpu().tolist())
        all_labels.extend(batch["label"].cpu().tolist())

    metrics = compute_metrics(all_labels, all_preds)
    metrics["loss"] = total_loss / max(len(loader), 1)
    return metrics


@torch.no_grad()
def eval_epoch(model, loader, graph, device, return_predictions: bool = False):
    model.eval()
    all_preds, all_labels = [], []

    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        logits, _ = model(batch, graph)
        all_preds.extend(logits.argmax(dim=-1).cpu().tolist())
        all_labels.extend(batch["label"].cpu().tolist())

    metrics = compute_metrics(all_labels, all_preds)
    if return_predictions:
        return metrics, all_labels, all_preds
    return metrics


@torch.no_grad()
def collect_gate_stats(model, loader, graph, device):
    """Thu thập patient gate weights từ test set để kiểm tra fusion có hoạt động."""
    model.eval()
    all_gates = []
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        _, _, weights = model(batch, graph, return_interpretability=True)
        all_gates.append(weights["patient"].cpu())
    gates = torch.cat(all_gates, dim=0)  # (N, 3)
    return {
        "mean": gates.mean(dim=0).tolist(),
        "std":  gates.std(dim=0).tolist(),
        "min":  gates.min(dim=0).values.tolist(),
        "max":  gates.max(dim=0).values.tolist(),
    }


def make_loaders(datasets: dict, train_batch_size: int):
    train_loader = DataLoader(
        datasets["train"],
        batch_size=train_batch_size,
        shuffle=True,
        num_workers=2,
        pin_memory=True,
    )
    val_loader = DataLoader(datasets["val"], batch_size=64, shuffle=False)
    test_loader = DataLoader(datasets["test"], batch_size=64, shuffle=False)
    return train_loader, val_loader, test_loader


def compute_class_weights(dataset, num_classes: int, device):
    labels = dataset.label.cpu().numpy()
    counts = np.bincount(labels, minlength=num_classes).astype(np.float32)
    counts = np.clip(counts, a_min=1.0, a_max=None)
    weights = len(labels) / (num_classes * counts)
    weights = weights / weights.mean()
    return torch.tensor(weights, dtype=torch.float32, device=device)


def fit_one_split(cfg, datasets, feature_names, dims, metadata, device, fold_name: str):
    train_loader, val_loader, test_loader = make_loaders(
        datasets, cfg["training"]["batch_size"]
    )
    graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device=str(device))

    model = GIACModel(dims, cfg["model"], cfg["training"]).to(device)
    model.set_class_weights(
        compute_class_weights(datasets["train"], cfg["model"]["num_classes"], device)
    )

    # fusion_alpha cần lr cao hơn 10x để gradient không quá nhỏ
    _base_lr = cfg["training"]["learning_rate"]
    _wd      = cfg["training"]["weight_decay"]
    optimizer = torch.optim.AdamW([
        {"params": [p for n, p in model.named_parameters()
                    if "fusion_alpha" not in n],
         "lr": _base_lr, "weight_decay": _wd},
        {"params": [model.fusion_alpha],
         "lr": _base_lr * 10, "weight_decay": 0.0},
    ])

    scheduler_name = cfg["training"].get("scheduler", "onecycle").lower()
    if scheduler_name == "onecycle":
        scheduler = torch.optim.lr_scheduler.OneCycleLR(
            optimizer,
            max_lr=cfg["training"].get("max_learning_rate", cfg["training"]["learning_rate"] * 5.0),
            epochs=cfg["training"]["epochs"],
            steps_per_epoch=max(len(train_loader), 1),
            pct_start=cfg["training"].get("onecycle_pct_start", 0.1),
            div_factor=cfg["training"].get("onecycle_div_factor", 10.0),
            final_div_factor=cfg["training"].get("onecycle_final_div_factor", 100.0),
        )
        scheduler_step_per_batch = True
    else:
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=cfg["training"]["epochs"]
        )
        scheduler_step_per_batch = False

    early_stop = EarlyStopping(patience=cfg["training"]["patience"])

    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n🧠 {fold_name} model parameters: {n_params:,}")
    print(f"🚀 Bắt đầu training {fold_name.lower()}...\n")
    print(f"🗓️  Scheduler: {scheduler_name}")

    best_val_f1 = 0.0
    save_dir = cfg["logging"]["save_dir"]
    viz_dir = os.path.join(save_dir, "visualizations", fold_name.lower().replace(" ", "_"))
    ensure_dir(viz_dir)
    ckpt_name = "best_model.pt" if fold_name == "Single split" else f"best_model_{fold_name.lower().replace(' ', '_')}.pt"
    ckpt_path = os.path.join(save_dir, ckpt_name)
    history = {"train_loss": [], "train_f1": [], "val_f1": []}

    plot_split_class_distribution(
        {
            "train": datasets["train"].label.cpu().numpy(),
            "val": datasets["val"].label.cpu().numpy(),
            "test": datasets["test"].label.cpu().numpy(),
        },
        path=os.path.join(viz_dir, "class_distribution.png"),
        title=f"{fold_name} - Class Distribution",
        class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
    )

    for epoch in range(1, cfg["training"]["epochs"] + 1):
        train_metrics = train_epoch(
            model,
            train_loader,
            optimizer,
            graph,
            device,
            scheduler=scheduler if scheduler_step_per_batch else None,
        )
        val_metrics = eval_epoch(model, val_loader, graph, device)
        if not scheduler_step_per_batch:
            scheduler.step()
        history["train_loss"].append(train_metrics["loss"])
        history["train_f1"].append(train_metrics["f1"])
        history["val_f1"].append(val_metrics["f1"])

        if epoch % cfg["logging"]["log_interval"] == 0 or epoch == 1:
            print(f"{fold_name} | Epoch {epoch:3d}/{cfg['training']['epochs']}")
            print_metrics(train_metrics, "Train")
            print_metrics(val_metrics, "Val  ")
            alpha = torch.sigmoid(model.fusion_alpha).item()
            print(f"       fusion_alpha={alpha:.3f}  (GAT={alpha:.2f}, Shortcut={1-alpha:.2f})")


        if val_metrics["f1"] > best_val_f1:
            best_val_f1 = val_metrics["f1"]
            save_checkpoint(
                model,
                optimizer,
                epoch,
                val_metrics,
                path=ckpt_path,
                extra_state={
                    "preprocessing": metadata["preprocess"],
                    "split_info": metadata["split_info"],
                    "feature_names": feature_names,
                    "dims": dims,
                    "fold_name": fold_name,
                    "config": cfg,
                    "history": history,
                },
            )

        if early_stop.step(val_metrics["f1"]):
            print(f"⏹️  Early stopping tại epoch {epoch} cho {fold_name}")
            break

    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    test_metrics, test_labels, test_preds = eval_epoch(
        model, test_loader, graph, device, return_predictions=True
    )

    print(f"\n📊 Đánh giá trên Test set - {fold_name}")
    print_metrics(test_metrics, "Test ")
    print(f"✅ Best val F1: {best_val_f1:.4f}")
    print(f"✅ Test F1:     {test_metrics['f1']:.4f}")

    plot_training_curves(
        history,
        path=os.path.join(viz_dir, "training_curves.png"),
        title=fold_name,
    )
    plot_confusion_matrix_figure(
        test_labels,
        test_preds,
        path=os.path.join(viz_dir, "confusion_matrix_test.png"),
        title=f"{fold_name} - Test Confusion Matrix",
        class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
        normalize=True,
    )

    # ── A1: Per-class Classification Report ───────────────────────
    print(f"\n📋 Classification Report - {fold_name}")
    print_classification_report(
        test_labels, test_preds,
        class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
    )
    save_confusion_matrix_csv(
        test_labels, test_preds,
        path=os.path.join(viz_dir, "confusion_matrix_test_absolute.csv"),
        class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
    )

    # ── A3: Patient Gate Statistics ────────────────────────────────
    gate_stats = collect_gate_stats(model, test_loader, graph, device)
    print(f"\n🔍 Patient Gate Statistics - {fold_name}")
    for i, name in enumerate(["gene", "meth", "mirna"]):
        print(
            f"   {name:5s}: mean={gate_stats['mean'][i]:.4f}  "
            f"std={gate_stats['std'][i]:.4f}  "
            f"min={gate_stats['min'][i]:.4f}  "
            f"max={gate_stats['max'][i]:.4f}"
        )

    return {
        "fold": fold_name,
        "best_val_f1": best_val_f1,
        "test_metrics": test_metrics,
        "checkpoint": ckpt_path,
        "viz_dir": viz_dir,
    }


def summarize_cv(results: list):
    metric_names = ["accuracy", "precision", "recall", "f1"]
    print("\n📈 5-fold CV summary")
    for name in metric_names:
        values = np.array([result["test_metrics"][name] for result in results], dtype=np.float64)
        print(f"  {name.upper():9s}: mean={values.mean():.4f}  std={values.std(ddof=0):.4f}")


def main():
    args = parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    set_seed(cfg["training"]["seed"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥️  Device: {device}")

    cv_folds = args.cv_folds if args.cv_folds is not None else cfg.get("preprocessing", {}).get("cv_folds", 5)

    if cv_folds and cv_folds > 1:
        fold_packages = build_cv_datasets(cfg["data"], cfg["training"]["seed"], n_splits=cv_folds)
        results = []
        for fold_package in fold_packages:
            fold_no = fold_package["fold"]
            datasets, feature_names, dims, metadata = fold_package["datasets"]
            print(
                f"\n📐 Fold {fold_no}: "
                f"gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}"
            )
            results.append(
                fit_one_split(
                    cfg,
                    datasets,
                    feature_names,
                    dims,
                    metadata,
                    device,
                    fold_name=f"Fold {fold_no}",
                )
            )
        summarize_cv(results)
        plot_cv_metrics(
            results,
            path=os.path.join(cfg["logging"]["save_dir"], "visualizations", "cv_metrics_summary.png"),
            title="5-Fold CV Test Metrics",
        )
    else:
        datasets, feature_names, dims, metadata = build_datasets(
            cfg["data"], cfg["training"]["seed"]
        )
        print(f"\n📐 Feature dims: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
        fit_one_split(cfg, datasets, feature_names, dims, metadata, device, fold_name="Single split")


if __name__ == "__main__":
    main()