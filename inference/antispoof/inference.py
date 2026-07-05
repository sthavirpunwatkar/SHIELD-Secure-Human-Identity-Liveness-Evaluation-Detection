import os
import cv2
import numpy as np

class AntispoofInference:
    def __init__(self, model_path=None):
        """
        Standardized inference wrapper for anti-spoof models.
        Prioritizes loading ONNX models for fast production inference.
        """
        # Try best models first if no path provided
        if not model_path:
            candidates = [
                'models/efficientnet_fas.onnx',
                'models/minifas_antispoof_v2.onnx',
                'models/minifas_antispoof_v1.pt'
            ]
            for cand in candidates:
                if os.path.exists(cand):
                    model_path = cand
                    break
            if not model_path:
                model_path = 'models/minifas_antispoof_v2.onnx' # fallback string
                
        self.model_path = model_path
        self.is_onnx = model_path.endswith('.onnx')
        self.is_efficientnet = 'efficientnet' in model_path.lower()
        self.input_size = 224 if self.is_efficientnet else 80
        
        self.weights_loaded = False
        self.session = None
        self.model = None
        
        self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            print(f"Antispoof: {self.model_path} not found. Weights not loaded.")
            return

        try:
            if self.is_onnx:
                import onnxruntime as ort
                providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
                self.session = ort.InferenceSession(self.model_path, providers=providers)
                self.input_name = self.session.get_inputs()[0].name
                self.output_name = self.session.get_outputs()[0].name
                print(f"Antispoof: Loaded ONNX model from {self.model_path} (input: {self.input_size}x{self.input_size})")
                self.weights_loaded = True
            else:
                # Legacy PyTorch load
                import torch
                self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                # Fallback to older minifas v1 architecture if it's the old .pt file
                import torch.nn as nn
                self.model = nn.Sequential(
                    nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),
                    nn.BatchNorm2d(32), nn.ReLU(),
                    nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
                    nn.BatchNorm2d(64), nn.ReLU(),
                    nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
                    nn.BatchNorm2d(128), nn.ReLU(),
                    nn.AdaptiveAvgPool2d(1), nn.Flatten(),
                    nn.Dropout(0.3), nn.Linear(128, 2)
                )
                self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
                self.model = self.model.to(self.device)
                self.model.eval()
                print(f"Antispoof: Loaded PyTorch weights from {self.model_path}")
                self.weights_loaded = True
        except Exception as e:
            print(f"Antispoof: Load failed for {self.model_path}: {e}")

    def predict(self, face_crop):
        """
        Performs inference on a face crop.
        :param face_crop: BGR image.
        :return: score (0.0 to 1.0, where 1.0 is Real)
        """
        if face_crop is None or face_crop.size == 0:
            return 0.0

        if not self.weights_loaded:
            raise RuntimeError("Antispoof: weights not loaded. Mock fallback disabled.")
            
        # Preprocessing
        img = cv2.resize(face_crop, (self.input_size, self.input_size))
        img = img.astype(np.float32) / 255.0
        
        # ONNX Inference
        if self.is_onnx:
            # [1, C, H, W]
            img = np.transpose(img, (2, 0, 1))
            img = np.expand_dims(img, axis=0)
            
            outputs = self.session.run([self.output_name], {self.input_name: img})[0]
            # Softmax
            exp_preds = np.exp(outputs[0] - np.max(outputs[0]))
            probs = exp_preds / np.sum(exp_preds)
            return float(probs[1]) # Index 1 is Real
            
        # PyTorch Inference
        import torch
        img = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).to(self.device)
        with torch.no_grad():
            outputs = self.model(img)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            real_score = probabilities[0][1].item()
            
        return real_score

if __name__ == "__main__":
    inf = AntispoofInference()
    print("AntispoofInference ready.")
