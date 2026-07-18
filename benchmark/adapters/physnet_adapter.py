import os
import numpy as np
import torch
import torch.nn as nn
from benchmark.adapters.base_adapter import BenchmarkModel
from benchmark.utils.preprocessing import crop_and_resize, normalize_image

class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv3d(in_channels, out_channels, kernel_size, stride=stride, padding=padding),
            nn.BatchNorm3d(out_channels),
            nn.ReLU(inplace=True)
        )
    def forward(self, x):
        return self.net(x)

class PhysNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.stem = ConvBlock(3, 32, kernel_size=(1, 5, 5), padding=(0, 2, 2))
        self.pool1 = nn.MaxPool3d((1, 2, 2), stride=(1, 2, 2))
        self.b1 = ConvBlock(32, 64, kernel_size=(3, 3, 3), padding=1)
        self.b2 = ConvBlock(64, 64, kernel_size=(3, 3, 3), padding=1)
        self.pool2 = nn.MaxPool3d((2, 2, 2), stride=(2, 2, 2))
        self.b3 = ConvBlock(64, 128, kernel_size=(3, 3, 3), padding=1)
        self.b4 = ConvBlock(128, 128, kernel_size=(3, 3, 3), padding=1)
        self.pool3 = nn.MaxPool3d((2, 2, 2), stride=(2, 2, 2))
        self.b5 = ConvBlock(128, 128, kernel_size=(3, 3, 3), padding=1)
        self.b6 = ConvBlock(128, 128, kernel_size=(3, 3, 3), padding=1)
        self.pool4 = nn.AdaptiveAvgPool3d((None, 1, 1))
        self.head = nn.Conv3d(128, 1, kernel_size=1)

    def forward(self, x):
        x = self.stem(x)
        x = self.pool1(x)
        x = self.b1(x)
        x = self.b2(x)
        x = self.pool2(x)
        x = self.b3(x)
        x = self.b4(x)
        x = self.pool3(x)
        x = self.b5(x)
        x = self.b6(x)
        x = self.pool4(x)
        x = self.head(x)
        return x.flatten(1) # shape (B, T)

class PhysNetAdapter(BenchmarkModel):
    def __init__(self, model_path="benchmark/models/rppg_physnet_ubfc.pt"):
        self.model_path = model_path
        self.model = None
        self.buffer = []
        self.buffer_size = 32 # Temporal depth for 3D CNN
        self.spatial_size = 128

    def load_model(self):
        self.model = PhysNet()
        if os.path.exists(self.model_path):
            sd = torch.load(self.model_path, map_location='cpu')
            if 'state_dict' in sd:
                sd = sd['state_dict']
            self.model.load_state_dict(sd)
            self.model.eval()
        else:
            raise FileNotFoundError(f"PhysNet weights not found at {self.model_path}")

    def preprocess(self, input_data):
        image = input_data.get('image', np.zeros((480, 640, 3), dtype=np.uint8))
        bbox = input_data.get('bbox', None)
        crop = crop_and_resize(image, bbox, scale=1.0, target_size=(self.spatial_size, self.spatial_size))
        norm = normalize_image(crop)
        # HWC to CHW
        tensor = np.transpose(norm, (2, 0, 1))
        self.buffer.append(tensor)
        
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
            
        if len(self.buffer) == self.buffer_size:
            # (C, T, H, W) -> expand to (1, C, T, H, W)
            seq = np.stack(self.buffer, axis=1)
            return np.expand_dims(seq, axis=0)
        return None

    def infer(self, tensor):
        if tensor is None:
            return None
        with torch.no_grad():
            t = torch.tensor(tensor, dtype=torch.float32)
            out = self.model(t)
            return out.numpy()

    def postprocess(self, output):
        if output is None:
            return None
        # dummy bpm extraction from 32-frame sequence
        bpm = 75.0 + float(np.mean(output)) * 2.0
        return {
            "model": "PhysNet",
            "heart_rate": bpm,
            "confidence": 0.90,
            "latency_ms": 0.0
        }

    def metadata(self):
        return {
            "name": "PhysNet",
            "input_resolution": f"{self.buffer_size}x{self.spatial_size}x{self.spatial_size}",
            "framework": "PyTorch",
            "category": "rPPG"
        }
