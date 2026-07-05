"""
SHIELD – Upgraded rPPG Training Script v2

Training approach:
  1. Synthetic data generation (physics-based):
       Live  → smooth sinusoidal BPM signal + physiological variability + noise
       Spoof → random noise / flat / low-frequency drift patterns
  2. Optional: real video ROI extraction (scans data/ for .mp4/.avi)

Model: RPPGCNNv2 (dual-branch temporal + frequency)
Window: 150 frames (5 seconds @ 30fps)

Output:
  models/rppg_1dcnn_v2.pt    — PyTorch weights
  models/rppg_1dcnn_v2.onnx  — ONNX for production inference
  models/rppg_training_metrics.json
"""

import os
import sys
import argparse
import json
import time
import math
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split
from torch.cuda.amp import GradScaler, autocast

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from training.models.rppg_cnn import get_model as get_rppg_model


# ─────────────────────────────────────────────────────────
# Physics-based synthetic rPPG signal generator
# ─────────────────────────────────────────────────────────

def generate_live_signal(window_size: int, bpm_range=(55, 100), fps=30) -> np.ndarray:
    """
    Generate a realistic live rPPG signal with:
    - Primary cardiac frequency (BPM)
    - Respiratory modulation (12-25 breaths/min)
    - Motion artifact (small random walk)
    - Gaussian measurement noise
    """
    n = window_size
    t = np.linspace(0, n / fps, n, dtype=np.float32)

    # Primary cardiac component
    bpm = random.uniform(*bpm_range)
    cardiac_freq = bpm / 60.0
    phase = random.uniform(0, 2 * math.pi)
    cardiac = np.sin(2 * math.pi * cardiac_freq * t + phase)

    # Respiratory modulation (amplitude modulation)
    resp_bpm = random.uniform(12, 25)
    resp_freq = resp_bpm / 60.0
    resp = 1.0 + 0.15 * np.sin(2 * math.pi * resp_freq * t)
    cardiac = cardiac * resp

    # Second harmonic (realistic PPG shape)
    harmonic = 0.3 * np.sin(2 * 2 * math.pi * cardiac_freq * t + phase + 0.5)

    # Random walk motion artifact
    motion = np.cumsum(np.random.randn(n).astype(np.float32)) * 0.02
    motion = motion - motion.mean()

    # Gaussian noise
    noise = np.random.randn(n).astype(np.float32) * 0.05

    signal = cardiac + harmonic + motion + noise

    # Z-score normalize
    signal = (signal - signal.mean()) / (signal.std() + 1e-6)
    return signal.astype(np.float32)


def generate_spoof_signal(window_size: int, fps=30) -> np.ndarray:
    """
    Generate a spoof signal (no cardiac periodicity):
    Types: flat, random walk, low-frequency drift, white noise, device flicker
    """
    n = window_size
    t = np.linspace(0, n / fps, n, dtype=np.float32)
    spoof_type = random.choice(["flat", "random_walk", "drift", "white_noise", "flicker"])

    if spoof_type == "flat":
        signal = np.ones(n, dtype=np.float32) * random.uniform(-0.1, 0.1)
        signal += np.random.randn(n).astype(np.float32) * 0.01

    elif spoof_type == "random_walk":
        signal = np.cumsum(np.random.randn(n).astype(np.float32)) * 0.1

    elif spoof_type == "drift":
        # Very slow frequency below cardiac range (< 0.5 Hz)
        freq = random.uniform(0.05, 0.45)
        signal = np.sin(2 * math.pi * freq * t).astype(np.float32)
        signal += np.random.randn(n).astype(np.float32) * 0.1

    elif spoof_type == "white_noise":
        signal = np.random.randn(n).astype(np.float32)

    elif spoof_type == "flicker":
        # Screen flicker: 50/60 Hz mains + random harmonics
        mains = random.choice([50.0, 60.0])
        signal = 0.8 * np.sin(2 * math.pi * mains * t).astype(np.float32)
        signal += np.random.randn(n).astype(np.float32) * 0.2

    # Z-score normalize
    signal = (signal - signal.mean()) / (signal.std() + 1e-6)
    return signal.astype(np.float32)


# ─────────────────────────────────────────────────────────
# Video ROI signal extraction (optional)
# ─────────────────────────────────────────────────────────

def extract_roi_signal_from_video(video_path: str, window_size: int, fps_target: int = 30):
    """Extract green-channel ROI signals from a video file. Returns list of windows."""
    import cv2

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []

    signals = []
    buffer = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        h, w = frame.shape[:2]
        roi = frame[int(h * 0.35):int(h * 0.65), int(w * 0.35):int(w * 0.65)]
        green = float(np.mean(roi[:, :, 1]))
        buffer.append(green)
        frame_count += 1

        if len(buffer) >= window_size:
            window = np.array(buffer[-window_size:], dtype=np.float32)
            window = (window - window.mean()) / (window.std() + 1e-6)
            signals.append(window)

    cap.release()
    return signals


def load_video_data(data_root: str, window_size: int):
    """Scan data_root for video files and extract ROI windows."""
    video_ext = {".mp4", ".avi", ".mov", ".mkv"}
    X, y = [], []

    data_path = Path(data_root)
    if not data_path.exists():
        return X, y

    for video_file in data_path.rglob("*"):
        if video_file.suffix.lower() not in video_ext:
            continue
        # Infer label from path: paths with 'live' or 'real' or 'ubfc' or 'pure' → 1.0, else 0.0
        label = 1.0 if any(k in str(video_file).lower() for k in ["live", "real", "client", "ubfc", "pure"]) else 0.0
        windows = extract_roi_signal_from_video(str(video_file), window_size)
        for w in windows:
            X.append(w)
            y.append(label)
        if windows:
            print(f"  Video: {video_file.name} | windows={len(windows)} | label={'live' if label else 'spoof'}")

    return X, y


# ─────────────────────────────────────────────────────────
# Evaluation
# ─────────────────────────────────────────────────────────

def evaluate(model, dataloader, device, criterion, use_amp=False):
    model.eval()
    total_loss = 0.0
    all_preds, all_labels = [], []

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            with torch.amp.autocast("cuda", enabled=use_amp):
                outputs = model(inputs).squeeze(-1)
            loss = criterion(outputs.float(), labels.float())
            total_loss += loss.item() * inputs.size(0)
            preds = (outputs > 0.5).float()
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    n = len(dataloader.dataset)
    total_loss /= n
    all_preds  = np.array(all_preds)
    all_labels = np.array(all_labels)
    acc = float((all_preds == all_labels).mean())

    return {"loss": round(total_loss, 6), "acc": round(acc, 6)}


# ─────────────────────────────────────────────────────────
# ONNX export
# ─────────────────────────────────────────────────────────

def export_onnx(model, window_size, save_path, device):
    model.eval()
    dummy = torch.randn(1, 1, window_size, device=device)
    try:
        torch.onnx.export(
            model, dummy, save_path,
            input_names=["rppg_signal"],
            output_names=["liveness_prob"],
            opset_version=17,
            do_constant_folding=True,
        )
        print(f"  [ONNX] Exported FP32 to {save_path}")
        
        try:
            from onnxruntime.quantization import quantize_dynamic, QuantType
            int8_path = save_path.replace(".onnx", "_int8.onnx")
            
            # Quantize directly (no pre-process needed if no dynamic axes)
            quantize_dynamic(save_path, int8_path, weight_type=QuantType.QUInt8)
            print(f"  [ONNX] Exported INT8 to {int8_path}")
            
        except ImportError:
            print("  [ONNX] onnxruntime not installed, skipping quantization.")
        except Exception as e:
            print(f"  [ONNX] Quantization failed: {e}")

    except Exception as e:
        print(f"  [ONNX] Export failed: {e}")


# ─────────────────────────────────────────────────────────
# Main training routine
# ─────────────────────────────────────────────────────────

def train(args):
    print("=" * 60)
    print(f"SHIELD rPPG Training v2  |  window={args.window_size}")
    print("=" * 60)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    use_amp = device.type == "cuda"
    print(f"Device: {device}  |  Mixed Precision: {use_amp}")

    # ── Generate synthetic dataset ───────────────────────
    n_live  = args.n_samples // 2
    n_spoof = args.n_samples - n_live
    print(f"\nGenerating synthetic data: {n_live} live + {n_spoof} spoof samples...")

    X_all, y_all = [], []

    for _ in range(n_live):
        X_all.append(generate_live_signal(args.window_size))
        y_all.append(1.0)

    for _ in range(n_spoof):
        X_all.append(generate_spoof_signal(args.window_size))
        y_all.append(0.0)

    # ── Optionally load video data ───────────────────────
    if not args.synthetic_only:
        print("\nScanning data/ for video files...")
        vid_X, vid_y = load_video_data(args.data_dir, args.window_size)
        if vid_X:
            print(f"Found {len(vid_X)} windows from video files.")
            X_all.extend(vid_X)
            y_all.extend(vid_y)
        else:
            print("No video files found. Using synthetic-only data.")

    X_np = np.array(X_all, dtype=np.float32)  # (N, T)
    y_np = np.array(y_all, dtype=np.float32)  # (N,)

    # Shuffle
    perm = np.random.permutation(len(X_np))
    X_np, y_np = X_np[perm], y_np[perm]

    # Build tensors: (N, 1, T)
    X_t = torch.from_numpy(X_np[:, None, :])
    y_t = torch.from_numpy(y_np)

    dataset = TensorDataset(X_t, y_t)
    train_size = int(0.85 * len(dataset))
    val_size = len(dataset) - train_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True,  num_workers=0)
    val_loader   = DataLoader(val_ds,   batch_size=args.batch_size, shuffle=False, num_workers=0)

    print(f"Dataset: {len(dataset)} total | {train_size} train | {val_size} val")

    # ── Model ─────────────────────────────────────────────
    model = get_rppg_model(window_size=args.window_size).to(device)
    total_p = sum(p.numel() for p in model.parameters())
    print(f"RPPGCNNv2: {total_p:,} parameters")

    criterion = nn.BCELoss()  # Model already includes Sigmoid
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-6)
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    os.makedirs(args.save_dir, exist_ok=True)
    pt_path     = os.path.join(args.save_dir, "rppg_1dcnn_v2.pt")
    onnx_path   = os.path.join(args.save_dir, "rppg_1dcnn_v2.onnx")
    metrics_log = os.path.join(args.save_dir, "rppg_training_metrics.json")

    best_loss = float("inf")
    patience_counter = 0
    history = []

    print(f"\nSave paths:\n  Weights: {pt_path}\n  ONNX:    {onnx_path}\n")

    for epoch in range(1, args.epochs + 1):
        model.train()
        running_loss = 0.0
        t0 = time.time()

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad(set_to_none=True)

            with torch.amp.autocast("cuda", enabled=use_amp):
                outputs = model(inputs).squeeze(-1)
            loss = criterion(outputs.float(), labels.float())

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer)
            scaler.update()
            running_loss += loss.item() * inputs.size(0)

        scheduler.step()
        train_loss = running_loss / len(train_loader.dataset)
        val_m = evaluate(model, val_loader, device, criterion, use_amp)
        elapsed = time.time() - t0

        print(
            f"Epoch {epoch:3d}/{args.epochs} "
            f"| Train Loss: {train_loss:.5f} "
            f"| Val Loss: {val_m['loss']:.5f} "
            f"| Val Acc: {val_m['acc']:.4f} "
            f"| LR: {optimizer.param_groups[0]['lr']:.2e} "
            f"| {elapsed:.1f}s"
        )

        history.append({"epoch": epoch, "train_loss": round(train_loss, 6), **val_m})

        if val_m["loss"] < best_loss:
            best_loss = val_m["loss"]
            patience_counter = 0
            torch.save(model.state_dict(), pt_path)
            print(f"  ✓ Best Val Loss={best_loss:.5f} — saved")
        else:
            patience_counter += 1
            if patience_counter >= args.patience:
                print(f"Early stopping at epoch {epoch}.")
                break

    # ── Save metrics ────────────────────────────────────────
    with open(metrics_log, "w") as f:
        json.dump({"best_loss": best_loss, "history": history}, f, indent=2)

    # ── ONNX export ─────────────────────────────────────────
    model.load_state_dict(torch.load(pt_path, map_location=device))
    export_onnx(model, args.window_size, onnx_path, device)

    print(f"\n{'=' * 60}")
    print(f"rPPG Training complete! Best Val Loss: {best_loss:.5f}")
    print(f"  PyTorch: {pt_path}")
    print(f"  ONNX:    {onnx_path}")
    print(f"{'=' * 60}")
    return best_loss


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SHIELD rPPG Training v2")
    parser.add_argument("--data-dir",       type=str,   default="data",
                        help="Root dir to scan for video files")
    parser.add_argument("--window-size",    type=int,   default=150,
                        help="Signal window size in frames")
    parser.add_argument("--n-samples",      type=int,   default=20000,
                        help="Total synthetic samples to generate")
    parser.add_argument("--epochs",         type=int,   default=100)
    parser.add_argument("--batch-size",     type=int,   default=256)
    parser.add_argument("--lr",             type=float, default=1e-3)
    parser.add_argument("--save-dir",       type=str,   default="models")
    parser.add_argument("--patience",       type=int,   default=20)
    parser.add_argument("--synthetic-only", action="store_true", default=False)
    args = parser.parse_args()
    train(args)
