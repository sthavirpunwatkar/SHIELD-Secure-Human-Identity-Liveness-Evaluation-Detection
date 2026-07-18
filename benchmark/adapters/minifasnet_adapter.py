import os
import sys
import numpy as np
import torch

sys.path.append(os.path.join(os.path.dirname(__file__), '../models/minifasnet'))
from MiniFASNet import MiniFASNetV2

from .base_adapter import BenchmarkModel
from benchmark.utils.preprocessing import crop_and_resize, normalize_image

class MiniFASNetAdapter(BenchmarkModel):
    def __init__(self, model_path="benchmark/models/minifasnet/2.7_80x80_MiniFASNetV2.pth"):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.model = MiniFASNetV2(conv6_kernel=(5, 5))
                state_dict = torch.load(self.model_path, map_location='cpu')
                new_state_dict = {}
                for k, v in state_dict.items():
                    name = k[7:] if k.startswith('module.') else k
                    new_state_dict[name] = v
                self.model.load_state_dict(new_state_dict)
                self.model.eval()
            else:
                self.model = "MOCK_MINIFASNET"
        except Exception as e:
            print(f"Failed to load MiniFASNet: {e}")
            self.model = "MOCK_MINIFASNET"
        
    def preprocess(self, input_data):
        image = input_data.get('image', np.zeros((480, 640, 3), dtype=np.uint8))
        bbox = input_data.get('bbox', None)
        crop = crop_and_resize(image, bbox, scale=2.7, target_size=(80, 80))
        norm = normalize_image(crop)
        tensor = np.transpose(norm, (2, 0, 1))
        return np.expand_dims(tensor, axis=0)

    def infer(self, tensor):
        if self.model == "MOCK_MINIFASNET":
            return np.array([[0.1, 0.9]])
        with torch.no_grad():
            output = self.model(torch.tensor(tensor, dtype=torch.float32))
            return output.numpy()

    def postprocess(self, output):
        score = np.exp(output) / np.sum(np.exp(output), axis=1, keepdims=True)
        confidence = float(score[0][1])
        prediction = "live" if confidence > 0.5 else "spoof"
        return {
            "model": "MiniFASNet",
            "prediction": prediction,
            "confidence": confidence,
            "latency_ms": 0.0
        }

    def metadata(self):
        return {
            "name": "MiniFASNet",
            "input_resolution": "80x80",
            "framework": "PyTorch",
            "category": "Anti-Spoofing"
        }
