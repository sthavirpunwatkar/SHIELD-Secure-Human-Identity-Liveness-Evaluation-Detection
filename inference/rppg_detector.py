import cv2
import numpy as np
import torch
import torch.nn as nn

class RPPGDetector:
    def __init__(self, window_size=30):
        """
        Initializes the rPPG detector.
        :param window_size: Number of frames to analyze for pulse detection.
        """
        self.window_size = window_size
        self.signal_buffer = []
        
        # Skeleton for 1D CNN
        self.model = self._build_model()
        self.model.eval()

    def _build_model(self):
        """
        Builds a simple 1D CNN for pulse signal classification.
        """
        model = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Conv1d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        return model

    def extract_roi_signal(self, frame, landmarks=None):
        """
        Extracts the average green channel value from skin ROIs (forehead/cheeks).
        """
        # For now, we'll take the center of the frame as a placeholder ROI
        h, w = frame.shape[:2]
        roi = frame[int(h*0.4):int(h*0.6), int(w*0.4):int(w*0.6)]
        
        # Green channel is typically most sensitive to blood volume changes
        avg_green = np.mean(roi[:, :, 1])
        return avg_green

    def update(self, frame):
        """
        Updates the buffer and returns a liveness score if the window is full.
        """
        signal = self.extract_roi_signal(frame)
        self.signal_buffer.append(signal)
        
        if len(self.signal_buffer) > self.window_size:
            self.signal_buffer.pop(0)
            
        if len(self.signal_buffer) == self.window_size:
            # Normalize signal
            sig = np.array(self.signal_buffer)
            sig = (sig - np.mean(sig)) / (np.std(sig) + 1e-6)
            
            # Inference (Placeholder)
            input_tensor = torch.FloatTensor(sig).unsqueeze(0).unsqueeze(0)
            with torch.no_grad():
                score = self.model(input_tensor).item()
            return score
        
        return 0.5 # Neutral score until buffer is full

if __name__ == "__main__":
    detector = RPPGDetector()
    print("RPPGDetector initialized successfully.")
