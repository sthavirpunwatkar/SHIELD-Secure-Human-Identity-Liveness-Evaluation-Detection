import cv2
import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
from inference.antispoof.inference import AntispoofInference

def test():
    inf = AntispoofInference()
    
    cap = cv2.VideoCapture('/home/sp/2026-07-06 20-36-14.mp4')
    ret, frame = cap.read()
    
    # Fake crop (center)
    h, w = frame.shape[:2]
    crop = frame[h//4:3*h//4, w//4:3*w//4]
    
    # Preprocessing identical to what's in inference.py
    img = cv2.resize(crop, (inf.input_size, inf.input_size))
    img = img.astype(np.float32) / 255.0
    
    # Try raw BGR
    img_bgr = np.transpose(img, (2, 0, 1))
    img_bgr = np.expand_dims(img_bgr, axis=0)
    out_bgr = inf.session.run([inf.output_name], {inf.input_name: img_bgr})[0][0]
    exp = np.exp(out_bgr - np.max(out_bgr))
    prob_bgr = exp / np.sum(exp)
    print("Raw BGR (/255):", out_bgr, "Probs:", prob_bgr)
    
    # Try RGB
    img_rgb_base = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    img_rgb_base = cv2.resize(img_rgb_base, (inf.input_size, inf.input_size)).astype(np.float32) / 255.0
    img_rgb = np.transpose(img_rgb_base, (2, 0, 1))
    img_rgb = np.expand_dims(img_rgb, axis=0)
    out_rgb = inf.session.run([inf.output_name], {inf.input_name: img_rgb})[0][0]
    exp = np.exp(out_rgb - np.max(out_rgb))
    prob_rgb = exp / np.sum(exp)
    print("Raw RGB (/255):", out_rgb, "Probs:", prob_rgb)
    
    # Try RGB + ImageNet
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img_norm = (img_rgb_base - mean) / std
    img_norm = np.transpose(img_norm, (2, 0, 1))
    img_norm = np.expand_dims(img_norm, axis=0)
    out_norm = inf.session.run([inf.output_name], {inf.input_name: img_norm})[0][0]
    exp = np.exp(out_norm - np.max(out_norm))
    prob_norm = exp / np.sum(exp)
    print("RGB + ImageNet Norm:", out_norm, "Probs:", prob_norm)
    
test()
