import torch
import torch.nn as nn
import cv2
import numpy as np

class MiniFASNet:
    def __init__(self, model_path=None):
        """
        Initializes the MiniFASNet anti-spoofing model.
        :param model_path: Path to the trained model weights.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Placeholder architecture for MiniFASNet
        # In a real scenario, this would load the specific MiniFASNet structure
        self.model = self._build_skeleton()
        
        if model_path:
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                print(f"MiniFASNet: Loaded weights from {model_path}")
            except Exception as e:
                print(f"MiniFASNet: Could not load weights: {e}")
        
        self.model.to(self.device)
        self.model.eval()

    def _build_skeleton(self):
        """
        Builds a lightweight CNN skeleton for MiniFASNet.
        """
        model = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(64, 3) # Classes: Real, Spoof, Uncertain
        )
        return model

    def predict(self, face_crop):
        """
        Predicts the liveness score for a given face crop.
        :param face_crop: OpenCV image (BGR).
        :return: (verdict, confidence)
        """
        # Preprocessing
        img = cv2.resize(face_crop, (80, 80)) # MiniFASNet often uses small inputs
        img = img.astype(np.float32) / 255.0
        img = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(img)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
        classes = ["Spoof", "Live", "Uncertain"]
        verdict = classes[predicted.item()]
        
        return verdict, confidence.item()

if __name__ == "__main__":
    model = MiniFASNet()
    print("MiniFASNet initialized successfully.")
