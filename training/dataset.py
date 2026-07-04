import os
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset
import random

class FASAugmentation:
    """Standard augmentations for FAS training."""
    def __init__(self, is_train=True):
        self.is_train = is_train
    
    def __call__(self, image):
        # image is numpy array (H, W, C)
        if self.is_train:
            # Random horizontal flip
            if random.random() < 0.5:
                image = cv2.flip(image, 1)
            
            # Random JPEG compression to simulate artifacts
            if random.random() < 0.3:
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), random.randint(50, 95)]
                result, encimg = cv2.imencode('.jpg', image, encode_param)
                if result:
                    image = cv2.imdecode(encimg, 1)
                    
            # Color jitter (brightness/contrast)
            if random.random() < 0.3:
                alpha = random.uniform(0.8, 1.2) # Contrast
                beta = random.uniform(-20, 20)   # Brightness
                image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
                
        # Normalize to float32 [0, 1]
        image = image.astype(np.float32) / 255.0
        return image

class FASDataset(Dataset):
    """
    PyTorch Dataset for Face Anti-Spoofing training.
    Supports directory-based loading.
    """
    def __init__(self, root_dir=None, manifest_path=None, split='train', 
                 transform=None, img_size=80, use_face_detector=False):
        """
        Args:
            root_dir: Path to dataset with train/test subdirs containing real/ and spoof/ folders
            manifest_path: Alternatively, path to manifest.json from DataWrangler
            split: 'train', 'val', or 'test'
            transform: Optional callable for augmentation
            img_size: Target image size (default 80x80 matching MiniFASNet)
            use_face_detector: If True, use YOLO to crop face before resizing
        """
        self.root_dir = root_dir
        self.split = split
        self.img_size = img_size
        self.transform = transform if transform is not None else FASAugmentation(is_train=(split == 'train'))
        self.use_face_detector = use_face_detector
        
        self.samples = []
        if root_dir:
            self._load_from_dir()
            
    def _load_from_dir(self):
        split_dir = os.path.join(self.root_dir, self.split)
        if not os.path.exists(split_dir):
            print(f"Warning: {split_dir} does not exist.")
            return
            
        # Map folders to labels
        for label_name, label_val in [('real', 1), ('live', 1), ('spoof', 0), ('fake', 0)]:
            class_dir = os.path.join(split_dir, label_name)
            if os.path.exists(class_dir):
                for file in os.listdir(class_dir):
                    if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                        self.samples.append((os.path.join(class_dir, file), label_val))
                        
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = cv2.imread(img_path)
        
        if image is None:
            # Fallback for bad images
            image = np.zeros((self.img_size, self.img_size, 3), dtype=np.uint8)
            
        if self.use_face_detector:
            # Simple center crop for now if face detector is requested but not implemented here
            h, w = image.shape[:2]
            image = image[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]
            
        image = cv2.resize(image, (self.img_size, self.img_size))
        
        if self.transform:
            image = self.transform(image)
            
        # Convert to tensor [C, H, W] if it's not already one
        if isinstance(image, torch.Tensor):
            tensor = image
        else:
            tensor = torch.from_numpy(image).permute(2, 0, 1)
        return tensor, torch.tensor(label, dtype=torch.long)
