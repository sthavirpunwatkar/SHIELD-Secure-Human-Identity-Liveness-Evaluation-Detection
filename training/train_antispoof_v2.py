"""
SHIELD – Advanced Anti-Spoof Training Script v2
================================================

Supports two backbone choices via --model flag:
  • minifasnet_v2   : ~510 K param lightweight DSConv+SE model, 80×80 input
  • efficientnet_b0 : ~5.3 M param pretrained backbone, 224×224 input

Upgrades over train_antispoof.py (v1)
--------------------------------------
1. Real backbone models (MiniFASNet-V2 / EfficientNet-B0) instead of a tiny 3-layer CNN
2. BatchNorm1d feature normalisation in both model heads (weakness fixed)
3. Advanced augmentation: random erasing, cutout, Gaussian blur, colour jitter,
   saturation jitter, random rotation ±15° — targeting print/replay attack artefacts
4. Class-balanced WeightedRandomSampler to handle NUAA's imbalanced test split
5. Label-smoothing CrossEntropyLoss (ε = 0.1)
6. CosineAnnealingWarmRestarts scheduler (T_0 = 10 epochs)
7. Automatic Mixed Precision via torch.cuda.amp (default ON for CUDA)
8. ONNX export after training with dynamic batch axis
9. APCER / BPCER / ACER / Accuracy logged every epoch
10. Metrics history saved to JSON alongside model weights

Output weights
--------------
  MiniFASNet-V2 : models/minifas_antispoof_v2.pt  + models/minifas_antispoof_v2.onnx
  EfficientNet  : models/efficientnet_fas.pt       + models/efficientnet_fas.onnx

Usage
-----
  # Lightweight baseline (fast)
  python training/train_antispoof_v2.py --model minifasnet_v2

  # Transfer-learned EfficientNet (higher accuracy)
  python training/train_antispoof_v2.py --model efficientnet_b0 --batch-size 32

  # Disable AMP (e.g. CPU-only machine)
  python training/train_antispoof_v2.py --model minifasnet_v2 --no-amp
"""

import json
import math
import os
import random
import sys
import time
import warnings

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, WeightedRandomSampler

# ── Project root on sys.path ───────────────────────────────────────────────
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from training.dataset import FASDataset
from training.models.minifasnet_v2 import MiniFASNetV2
from training.models.efficientnet_fas import EfficientNetFAS, IMAGENET_MEAN, IMAGENET_STD


# ===========================================================================
# Advanced augmentation
# ===========================================================================

class AdvancedFASAugmentation:
    """
    Augmentation pipeline targeting print/replay attack artefacts.

    Training transforms applied (in order):
      1. Random horizontal flip               (p=0.5)
      2. Colour jitter: brightness, contrast  (p=0.6)
      3. Saturation jitter (HSV)              (p=0.4)
      4. Random rotation ±15°                 (p=0.4)
      5. Gaussian blur σ∈[0.5,1.5]           (p=0.3) — replay screen softness
      6. JPEG compression quality 40–85       (p=0.4) — print-photo artefacts
      7. Cutout (1–2 patches ≤ img//5)        (p=0.25)
      8. Random erasing (tensor-space)        (p=0.2)

    Evaluation: only resize + normalise.

    Returns torch.Tensor (C, H, W) float32.
    """

    def __init__(
        self,
        is_train: bool = True,
        img_size: int = 80,
        imagenet_norm: bool = False,
    ) -> None:
        self.is_train = is_train
        self.img_size = img_size
        self.imagenet_norm = imagenet_norm
        self._mean = np.array(IMAGENET_MEAN, dtype=np.float32)
        self._std  = np.array(IMAGENET_STD,  dtype=np.float32)

    # ── numpy-space helpers ─────────────────────────────────────────────────

    @staticmethod
    def _hflip(img: np.ndarray) -> np.ndarray:
        return cv2.flip(img, 1) if random.random() < 0.5 else img

    @staticmethod
    def _color_jitter(img: np.ndarray) -> np.ndarray:
        if random.random() > 0.6:
            return img
        alpha = random.uniform(0.7, 1.3)
        beta  = random.uniform(-30, 30)
        return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    @staticmethod
    def _saturation_jitter(img: np.ndarray) -> np.ndarray:
        if random.random() > 0.4:
            return img
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * random.uniform(0.7, 1.3), 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    @staticmethod
    def _rotation(img: np.ndarray) -> np.ndarray:
        if random.random() > 0.4:
            return img
        h, w = img.shape[:2]
        angle = random.uniform(-15.0, 15.0)
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        return cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

    @staticmethod
    def _gaussian_blur(img: np.ndarray) -> np.ndarray:
        if random.random() > 0.3:
            return img
        sigma = random.uniform(0.5, 1.5)
        return cv2.GaussianBlur(img, (5, 5), sigma)

    @staticmethod
    def _jpeg_artifact(img: np.ndarray) -> np.ndarray:
        if random.random() > 0.4:
            return img
        q = random.randint(40, 85)
        ok, enc = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, q])
        return cv2.imdecode(enc, cv2.IMREAD_COLOR) if ok else img

    @staticmethod
    def _cutout(img: np.ndarray) -> np.ndarray:
        if random.random() > 0.25:
            return img
        img = img.copy()
        h, w = img.shape[:2]
        patch = max(4, min(h, w) // 5)
        for _ in range(random.randint(1, 2)):
            cx = random.randint(0, w - 1)
            cy = random.randint(0, h - 1)
            x1, x2 = max(0, cx - patch // 2), min(w, cx + patch // 2)
            y1, y2 = max(0, cy - patch // 2), min(h, cy + patch // 2)
            img[y1:y2, x1:x2] = 0
        return img

    # ── tensor-space helper ─────────────────────────────────────────────────

    @staticmethod
    def _random_erasing(
        t: torch.Tensor,
        p: float = 0.2,
        scale: tuple = (0.02, 0.15),
        ratio: tuple = (0.3, 3.3),
    ) -> torch.Tensor:
        if random.random() >= p:
            return t
        _, h, w = t.shape
        area = h * w
        for _ in range(10):
            ta = random.uniform(*scale) * area
            ar = random.uniform(*ratio)
            ph = int(round(math.sqrt(ta * ar)))
            pw = int(round(math.sqrt(ta / ar)))
            if ph < h and pw < w:
                y = random.randint(0, h - ph)
                x = random.randint(0, w - pw)
                t[:, y:y + ph, x:x + pw] = 0.0
                break
        return t

    # ── main callable ───────────────────────────────────────────────────────

    def __call__(self, img: np.ndarray) -> torch.Tensor:
        """
        Args:
            img: uint8 ndarray (H, W, 3) BGR from cv2.

        Returns:
            torch.Tensor (3, H, W) float32.
        """
        if self.is_train:
            img = self._hflip(img)
            img = self._color_jitter(img)
            img = self._saturation_jitter(img)
            img = self._rotation(img)
            img = self._gaussian_blur(img)
            img = self._jpeg_artifact(img)
            img = self._cutout(img)

        # Resize → float [0,1] → RGB
        img = cv2.resize(img, (self.img_size, self.img_size))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0

        if self.imagenet_norm:
            img = (img - self._mean) / self._std

        tensor = torch.from_numpy(img).permute(2, 0, 1).contiguous()

        if self.is_train:
            tensor = self._random_erasing(tensor)

        return tensor


# ===========================================================================
# Model factory
# ===========================================================================

def build_model(model_name: str) -> nn.Module:
    """Return correctly configured model for the given name."""
    if model_name == "minifasnet_v2":
        return MiniFASNetV2(num_classes=2, drop_rate=0.4)
    elif model_name == "efficientnet_b0":
        return EfficientNetFAS(num_classes=2, drop_rate=0.4, pretrained=True)
    else:
        raise ValueError(
            f"Unknown model '{model_name}'. "
            "Valid choices: minifasnet_v2, efficientnet_b0"
        )


# Output filename mapping (matches task requirements exactly)
_PT_NAMES = {
    "minifasnet_v2":   "minifas_antispoof_v2.pt",
    "efficientnet_b0": "efficientnet_fas.pt",
}
_ONNX_NAMES = {
    "minifasnet_v2":   "minifas_antispoof_v2.onnx",
    "efficientnet_b0": "efficientnet_fas.onnx",
}


# ===========================================================================
# Metrics (ISO/IEC 30107-3)
# ===========================================================================

def compute_fas_metrics(preds: list, labels: list) -> dict:
    """Compute APCER, BPCER, ACER, Accuracy.

    Convention: live=1 (positive class), spoof=0 (negative class)
      APCER = Attack Presentation Classification Error Rate
              = FP / (FP + TN)   [fraction of spoofs passed as live]
      BPCER = Bona Fide Presentation Classification Error Rate
              = FN / (FN + TP)   [fraction of live rejected as spoof]
      ACER  = (APCER + BPCER) / 2
    """
    p = np.array(preds,  dtype=np.int32)
    l = np.array(labels, dtype=np.int32)

    tp = int(np.sum((l == 1) & (p == 1)))
    tn = int(np.sum((l == 0) & (p == 0)))
    fp = int(np.sum((l == 0) & (p == 1)))
    fn = int(np.sum((l == 1) & (p == 0)))

    n_spoof = int(np.sum(l == 0))
    n_live  = int(np.sum(l == 1))
    n_total = n_spoof + n_live

    apcer = fp / n_spoof if n_spoof > 0 else 0.0
    bpcer = fn / n_live  if n_live  > 0 else 0.0
    acer  = (apcer + bpcer) / 2.0
    acc   = (tp + tn) / n_total if n_total > 0 else 0.0

    return {"apcer": apcer, "bpcer": bpcer, "acer": acer, "acc": acc}


# ===========================================================================
# Evaluation
# ===========================================================================

def evaluate(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    criterion: nn.Module,
    use_amp: bool = False,
) -> dict:
    model.eval()
    total_loss = 0.0
    all_preds, all_labels = [], []

    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            with torch.cuda.amp.autocast(enabled=use_amp):
                outputs = model(inputs)
                loss = criterion(outputs, labels)
            total_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().tolist())
            all_labels.extend(labels.cpu().tolist())

    avg_loss = total_loss / max(len(loader.dataset), 1)
    metrics = compute_fas_metrics(all_preds, all_labels)
    metrics["loss"] = avg_loss
    return metrics


# ===========================================================================
# Class-balanced sampler
# ===========================================================================

def make_weighted_sampler(labels: list) -> WeightedRandomSampler:
    counts = np.bincount(labels)
    weights_per_class = 1.0 / (counts.astype(np.float64) + 1e-8)
    sample_weights = [weights_per_class[l] for l in labels]
    return WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(sample_weights),
        replacement=True,
    )


# ===========================================================================
# ONNX export
# ===========================================================================

def export_onnx(
    model: nn.Module,
    save_path: str,
    img_size: int,
    device: torch.device,
) -> None:
    model.eval()
    dummy = torch.randn(1, 3, img_size, img_size, device=device)
    try:
        torch.onnx.export(
            model,
            dummy,
            save_path,
            export_params=True,
            opset_version=17,
            do_constant_folding=True,
            input_names=["face_crop"],
            output_names=["logits"],
            dynamic_axes={
                "face_crop": {0: "batch_size"},
                "logits":    {0: "batch_size"},
            },
        )
        size_mb = os.path.getsize(save_path) / 1e6
        print(f"  [ONNX] Exported → {save_path}  ({size_mb:.1f} MB)")
    except Exception as exc:
        print(f"  [ONNX] Export failed: {exc}")


# ===========================================================================
# Main training routine
# ===========================================================================

def train(args) -> float:
    print("=" * 68)
    print(f"  SHIELD Anti-Spoof Training v2  |  model = {args.model}")
    print("=" * 68)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    use_amp = (not args.no_amp) and (device.type == "cuda")
    print(f"  Device : {device}" + (f"  ({torch.cuda.get_device_name(0)})" if device.type == "cuda" else ""))
    print(f"  AMP    : {use_amp}")

    # ── Config per model ────────────────────────────────────────────────────
    is_efficientnet = args.model == "efficientnet_b0"
    img_size     = 224 if is_efficientnet else 80
    imagenet_norm = is_efficientnet

    # ── Augmentations ────────────────────────────────────────────────────────
    train_aug = AdvancedFASAugmentation(is_train=True,  img_size=img_size, imagenet_norm=imagenet_norm)
    val_aug   = AdvancedFASAugmentation(is_train=False, img_size=img_size, imagenet_norm=imagenet_norm)

    # ── Datasets ─────────────────────────────────────────────────────────────
    train_ds = FASDataset(
        root_dir=args.data_dir, split="train",
        transform=train_aug, img_size=img_size,
    )
    test_ds = FASDataset(
        root_dir=args.data_dir, split="test",
        transform=val_aug, img_size=img_size,
    )

    if len(train_ds) == 0:
        raise RuntimeError(
            f"No training images found in {args.data_dir}/train/.\n"
            "Ensure real/ and spoof/ subdirectories exist."
        )

    print(f"\n  Train samples : {len(train_ds)}")
    print(f"  Test  samples : {len(test_ds)}")

    # ── Class-balanced sampler ────────────────────────────────────────────────
    train_labels = [lbl for (_, lbl) in train_ds.samples]
    sampler = make_weighted_sampler(train_labels)

    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size,
        sampler=sampler,
        num_workers=args.workers,
        pin_memory=(device.type == "cuda"),
        drop_last=True,
    )
    val_loader = DataLoader(
        test_ds,
        batch_size=args.batch_size * 2,
        shuffle=False,
        num_workers=args.workers,
        pin_memory=(device.type == "cuda"),
    )

    # ── Model ────────────────────────────────────────────────────────────────
    model = build_model(args.model).to(device)
    total_p = sum(p.numel() for p in model.parameters())
    train_p = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n  Params : {total_p:,} total | {train_p:,} trainable")

    # ── Loss ─────────────────────────────────────────────────────────────────
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    # ── Optimizer ─────────────────────────────────────────────────────────────
    # EfficientNet: give backbone a 10× lower LR than the new head
    if is_efficientnet:
        head_params = list(model.classifier.parameters())
        head_ids = {id(p) for p in head_params}
        backbone_params = [p for p in model.parameters()
                           if id(p) not in head_ids and p.requires_grad]
        param_groups = [
            {"params": backbone_params, "lr": args.lr * 0.1},
            {"params": head_params,     "lr": args.lr},
        ]
    else:
        param_groups = list(model.parameters())

    optimizer = optim.AdamW(param_groups, lr=args.lr, weight_decay=1e-4)

    # ── Scheduler: CosineAnnealingWarmRestarts ────────────────────────────────
    scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(
        optimizer, T_0=10, T_mult=1, eta_min=1e-6
    )

    # ── AMP scaler ────────────────────────────────────────────────────────────
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

    # ── Output paths (per task spec) ──────────────────────────────────────────
    os.makedirs(args.save_dir, exist_ok=True)
    pt_path   = os.path.join(args.save_dir, _PT_NAMES[args.model])
    onnx_path = os.path.join(args.save_dir, _ONNX_NAMES[args.model])
    json_path = os.path.join(
        args.save_dir,
        _PT_NAMES[args.model].replace(".pt", "_metrics.json"),
    )

    print(f"\n  Weights : {pt_path}")
    print(f"  ONNX    : {onnx_path}")

    # ── EfficientNet: progressive unfreeze after warm-up ──────────────────────
    UNFREEZE_EPOCH = 5 if is_efficientnet else 0

    # ── Training loop ─────────────────────────────────────────────────────────
    best_acer = float("inf")
    patience_count = 0
    history = []

    hdr = (
        f"\n{'Ep':>4}  {'TrLoss':>8}  {'VlLoss':>8}  "
        f"{'APCER':>7}  {'BPCER':>7}  {'ACER':>7}  {'Acc':>7}  {'LR':>9}"
    )
    print(hdr)
    print("-" * 76)

    for epoch in range(1, args.epochs + 1):
        t0 = time.time()

        # Progressive unfreeze for EfficientNet
        if is_efficientnet and epoch == UNFREEZE_EPOCH + 1:
            model.unfreeze_all()
            for pg in optimizer.param_groups:
                pg["lr"] = args.lr * 0.1
            print(f"  [Epoch {epoch}] EfficientNet backbone fully unfrozen. LR → {args.lr*0.1:.2e}")

        model.train()
        running_loss = 0.0
        n_batches = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad(set_to_none=True)

            with torch.cuda.amp.autocast(enabled=use_amp):
                outputs = model(inputs)
                loss = criterion(outputs, labels)

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer)
            scaler.update()

            running_loss += loss.item()
            n_batches += 1

        # Step scheduler once per epoch (pass epoch-1 for warm-restart logic)
        scheduler.step(epoch - 1)

        train_loss = running_loss / max(n_batches, 1)
        vm = evaluate(model, val_loader, device, criterion, use_amp)
        lr_now = optimizer.param_groups[-1]["lr"]

        row = (
            f"{epoch:>4}  {train_loss:>8.4f}  {vm['loss']:>8.4f}  "
            f"{vm['apcer']:>7.4f}  {vm['bpcer']:>7.4f}  {vm['acer']:>7.4f}  "
            f"{vm['acc']:>7.4f}  {lr_now:>9.2e}"
        )
        print(row, flush=True)

        history.append({
            "epoch": epoch,
            "train_loss": round(train_loss, 6),
            "lr": lr_now,
            **{k: round(v, 6) for k, v in vm.items()},
        })

        # Best model checkpoint
        if vm["acer"] < best_acer:
            best_acer = vm["acer"]
            patience_count = 0
            torch.save(model.state_dict(), pt_path)
            print(f"  ✓ Best ACER={best_acer:.4f} — saved → {pt_path}", flush=True)
        else:
            patience_count += 1

        if patience_count >= args.patience:
            print(f"\n  [Early stop] No ACER improvement for {args.patience} epochs.")
            break

    # ── Save metrics JSON ─────────────────────────────────────────────────────
    with open(json_path, "w") as fh:
        json.dump({"model": args.model, "best_acer": best_acer, "history": history}, fh, indent=2)
    print(f"\n  Metrics saved → {json_path}")

    # ── ONNX export (load best weights first) ─────────────────────────────────
    print("\n  Exporting ONNX …")
    if os.path.exists(pt_path):
        model.load_state_dict(torch.load(pt_path, map_location=device))
    export_onnx(model, onnx_path, img_size, device)

    # ── Final summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 68)
    print(f"  Training complete!  Best ACER : {best_acer:.4f}")
    print(f"  PyTorch weights : {pt_path}")
    print(f"  ONNX model      : {onnx_path}")
    print("=" * 68)

    # Final eval on best model
    print("\n  [Final eval on test set]")
    fm = evaluate(model, val_loader, device, criterion, use_amp)
    print(
        f"  APCER={fm['apcer']:.4f}  BPCER={fm['bpcer']:.4f}  "
        f"ACER={fm['acer']:.4f}  Acc={fm['acc']:.4f}"
    )

    return best_acer


# ===========================================================================
# CLI entry point
# ===========================================================================

def parse_args():
    import argparse
    p = argparse.ArgumentParser(
        description="SHIELD Anti-Spoof Training v2",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--model", type=str, default="minifasnet_v2",
        choices=["minifasnet_v2", "efficientnet_b0"],
        help="Backbone architecture to train",
    )
    p.add_argument("--data-dir",    type=str,   default="data/NUAA",  help="Dataset root directory")
    p.add_argument("--epochs",      type=int,   default=60,           help="Maximum training epochs")
    p.add_argument("--batch-size",  type=int,   default=64,           help="Mini-batch size")
    p.add_argument("--lr",          type=float, default=1e-3,         help="Base learning rate")
    p.add_argument("--save-dir",    type=str,   default="models",     help="Directory for saved weights/ONNX")
    p.add_argument("--workers",     type=int,   default=4,            help="DataLoader worker threads")
    p.add_argument("--patience",    type=int,   default=15,           help="Early-stopping patience (epochs)")
    p.add_argument("--no-amp",      action="store_true",              help="Disable automatic mixed precision")
    return p.parse_args()


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    args = parse_args()
    train(args)
