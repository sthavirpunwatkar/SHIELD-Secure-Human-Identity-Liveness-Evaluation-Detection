import cv2
import numpy as np

def crop_and_resize(image, bbox, scale=1.0, target_size=(80, 80)):
    if bbox is None:
        return cv2.resize(image, target_size)
    x, y, w, h = bbox
    cx, cy = x + w/2, y + h/2
    w, h = w * scale, h * scale
    x1, y1 = int(max(0, cx - w/2)), int(max(0, cy - h/2))
    x2, y2 = int(min(image.shape[1], cx + w/2)), int(min(image.shape[0], cy + h/2))
    crop = image[y1:y2, x1:x2]
    if crop.size == 0:
        return cv2.resize(image, target_size)
    return cv2.resize(crop, target_size)

def normalize_image(image, mean=0.0, std=255.0):
    return (image.astype(np.float32) - mean) / std
