import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import cv2

class LivenessClassifier:
    def __init__(self, model_path=None):
        """
        Initializes the EfficientNet-B0 liveness classifier.
        :param model_path: Path to the trained model weights.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize EfficientNet-B0 with modern weights API
        weights = models.EfficientNet_B0_Weights.DEFAULT
        self.model = models.efficientnet_b0(weights=weights)
        # Modify the final layer for binary classification (Live vs Spoof)
        num_ftrs = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Linear(num_ftrs, 2)
        
        if model_path:
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                print(f"Loaded weights from {model_path}")
            except Exception as e:
                print(f"Could not load weights: {e}")
        
        self.model.to(self.device)
        self.model.eval()

        # Define transforms
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, face_crop):
        """
        Predicts if the face crop is Live or Spoof.
        :param face_crop: OpenCV image (BGR).
        :return: (verdict, confidence)
        """
        # Convert BGR to RGB
        face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(face_rgb)
        
        input_tensor = self.transform(pil_img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
        verdict = "Live" if predicted.item() == 1 else "Spoof"
        return verdict, confidence.item()

if __name__ == "__main__":
    import cv2
    classifier = LivenessClassifier()
    print("LivenessClassifier initialized successfully.")
