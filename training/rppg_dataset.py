import os
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset

class RPPGDataset(Dataset):
    """
    PyTorch Dataset for rPPG liveness detection training.
    """
    def __init__(self, video_dir=None, signal_dir=None, window_size=30, 
                 stride=15, split='train'):
        self.window_size = window_size
        self.samples = []  # [(signal_window, label), ...]
        
        if signal_dir and os.path.exists(signal_dir):
            self._load_from_signals(signal_dir)
        elif video_dir and os.path.exists(video_dir):
            self._extract_from_videos(video_dir)
        else:
            print("RPPGDataset: No data source found. Generating synthetic training data.")
            self._generate_synthetic_data()
    
    def _extract_from_videos(self, video_dir):
        """Extract green-channel ROI signals from videos."""
        for label_name in ['live', 'real']:
            label_dir = os.path.join(video_dir, label_name)
            if os.path.exists(label_dir):
                self._process_video_dir(label_dir, label=1)
        for label_name in ['spoof', 'attack', 'fake']:
            label_dir = os.path.join(video_dir, label_name)
            if os.path.exists(label_dir):
                self._process_video_dir(label_dir, label=0)
                
    def _process_video_dir(self, dir_path, label):
        extractor = RPPGSignalExtractor()
        for file in os.listdir(dir_path):
            if file.lower().endswith(('.mp4', '.avi', '.mov')):
                vid_path = os.path.join(dir_path, file)
                sig = extractor.extract_from_video(vid_path)
                if len(sig) >= self.window_size:
                    sig = extractor.bandpass_filter(sig)
                    # Windowing
                    for i in range(0, len(sig) - self.window_size + 1, self.window_size // 2):
                        window = sig[i:i + self.window_size]
                        # Normalize
                        window = (window - np.mean(window)) / (np.std(window) + 1e-6)
                        self.samples.append((window, label))
    
    def _generate_synthetic_data(self, num_live=500, num_spoof=500):
        """Generate synthetic training data."""
        # Live: sine wave + noise
        t = np.arange(self.window_size)
        for _ in range(num_live):
            freq = np.random.uniform(1.0, 1.5) # 60-90 BPM
            phase = np.random.uniform(0, 2*np.pi)
            sig = np.sin(2 * np.pi * freq * t / 30 + phase)
            noise = np.random.normal(0, 0.2, self.window_size)
            sig = sig + noise
            sig = (sig - np.mean(sig)) / (np.std(sig) + 1e-6)
            self.samples.append((sig, 1))
            
        # Spoof: random noise
        for _ in range(num_spoof):
            sig = np.random.normal(0, 1.0, self.window_size)
            sig = (sig - np.mean(sig)) / (np.std(sig) + 1e-6)
            self.samples.append((sig, 0))
    
    def _load_from_signals(self, signal_dir):
        pass # To be implemented
        
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        signal, label = self.samples[idx]
        tensor = torch.FloatTensor(signal).unsqueeze(0)  # [1, window_size]
        return tensor, torch.FloatTensor([label])

class RPPGSignalExtractor:
    def __init__(self, roi_type='forehead'):
        self.roi_type = roi_type
        
    def extract_from_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        sig = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            h, w = frame.shape[:2]
            roi = frame[int(h*0.2):int(h*0.4), int(w*0.4):int(w*0.6)]
            if roi.size > 0:
                avg_green = np.mean(roi[:, :, 1])
                sig.append(avg_green)
        cap.release()
        return np.array(sig)
        
    @staticmethod
    def bandpass_filter(signal, fps=30, low_hz=0.7, high_hz=4.0):
        # Fallback to simple moving average if scipy is not available
        try:
            from scipy.signal import butter, filtfilt
            nyq = 0.5 * fps
            low = low_hz / nyq
            high = high_hz / nyq
            b, a = butter(2, [low, high], btype='band')
            return filtfilt(b, a, signal)
        except ImportError:
            # Simple fallback
            return signal - np.mean(signal)
