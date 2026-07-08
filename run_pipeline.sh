#!/bin/bash
set -e
source backend/venv/bin/activate
echo "Training Anti-Spoofing (EfficientNet-B0)..."
python training/train_antispoof_v2.py --model efficientnet_b0 --batch-size 32

echo "Training RPPG (V2)..."
python training/train_rppg_v2.py --n-samples 50000

echo "Building Frontend Release..."
cd frontend
/home/sp/flutter/bin/flutter build web --web-renderer canvaskit --release
cd ..
echo "Pipeline complete."
