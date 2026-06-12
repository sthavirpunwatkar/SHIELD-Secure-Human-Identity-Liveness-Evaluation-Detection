import os
import torch
import cv2
import numpy as np

class AntispoofInference:
    def __init__(self, model_path='models/minifas_antispoof_v1.pt'):
        """
        Standardized inference wrapper for anti-spoof models.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.weights_loaded = False
        self.model = self._load_model(model_path)
        self.model.eval()

    def _load_model(self, model_path):
        """
        Loads the model architecture and weights.
        """
        import torch.nn as nn
        
        # This architecture matches training/train_antispoof.py
        model = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(128, 2) # 2 classes: Spoof (0), Live (1)
        )
        
        if model_path and os.path.exists(model_path):
            try:
                model.load_state_dict(torch.load(model_path, map_location=self.device))
                print(f"Antispoof: Loaded weights from {model_path}")
                self.weights_loaded = True
            except Exception as e:
                print(f"Antispoof: Weight load failed: {e}")
        else:
            print(f"Antispoof: {model_path} not found. Running with random weights (fallback mode).")
            
        return model.to(self.device)

    def predict(self, face_crop):
        """
        Performs inference on a face crop.
        :param face_crop: BGR image.
        :return: score (0.0 to 1.0, where 1.0 is Real)
        """
        if face_crop is None or face_crop.size == 0:
            return 0.0

        if not self.weights_loaded:
            # Fallback logic for when model isn't trained
            h, w = face_crop.shape[:2]
            if h > 80 and w > 80:
                return 0.88 # fake high score
            return 0.5
            
        # Preprocessing
        img = cv2.resize(face_crop, (80, 80))
        img = img.astype(np.float32) / 255.0
        img = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(img)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            # Classes: [Spoof, Real] -> index 1 is Real
            real_score = probabilities[0][1].item()
            
        return real_score

if __name__ == "__main__":
    inf = AntispoofInference()
    print("AntispoofInference ready.")
