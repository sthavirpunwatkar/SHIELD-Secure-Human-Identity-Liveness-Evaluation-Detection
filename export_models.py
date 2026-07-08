import os
import torch
import sys

sys.path.append(os.path.abspath("."))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Antispoof export
from training.train_antispoof_v2 import build_model, export_onnx as as_export
print("Exporting Antispoof...")
model_as = build_model("efficientnet_b0")
model_as.load_state_dict(torch.load("models/efficientnet_fas.pt", map_location=device, weights_only=True))
model_as.to(device)
as_export(model_as, "models/efficientnet_fas.onnx", 224, device)

# rPPG export
from training.models.rppg_cnn import get_model as build_rppg
from training.train_rppg_v2 import export_onnx as rppg_export
print("Exporting rPPG...")
model_rppg = build_rppg(window_size=150)
model_rppg.load_state_dict(torch.load("models/rppg_1dcnn_v2.pt", map_location=device, weights_only=True))
model_rppg.to(device)
rppg_export(model_rppg, 150, "models/rppg_1dcnn_v2.onnx", device)
