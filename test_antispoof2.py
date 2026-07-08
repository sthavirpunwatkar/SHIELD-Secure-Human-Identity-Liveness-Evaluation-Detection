import cv2
import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
from inference.antispoof.inference import AntispoofInference
from inference.yolo_detector import YoloSegDetector

def test():
    inf = AntispoofInference()
    det = YoloSegDetector()
    
    cap = cv2.VideoCapture('/home/sp/2026-07-06 20-36-14.mp4')
    # skip some frames
    for _ in range(30):
        ret, frame = cap.read()
    
    faces = det.detect_faces(frame)
    if not faces:
        print("No face detected")
        return
    bbox = faces[0]['bbox']
    crop = det.crop_face(frame, bbox)
    
    # Try raw BGR
    img_base = cv2.resize(crop, (inf.input_size, inf.input_size)).astype(np.float32) / 255.0
    img_bgr = np.transpose(img_base, (2, 0, 1))
    img_bgr = np.expand_dims(img_bgr, axis=0)
    out_bgr = inf.session.run([inf.output_name], {inf.input_name: img_bgr})[0][0]
    prob_bgr = np.exp(out_bgr) / np.sum(np.exp(out_bgr))
    print("Raw BGR (/255):", prob_bgr)
    
    # Try RGB
    img_rgb_base = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    img_rgb_base = cv2.resize(img_rgb_base, (inf.input_size, inf.input_size)).astype(np.float32) / 255.0
    img_rgb = np.transpose(img_rgb_base, (2, 0, 1))
    img_rgb = np.expand_dims(img_rgb, axis=0)
    out_rgb = inf.session.run([inf.output_name], {inf.input_name: img_rgb})[0][0]
    prob_rgb = np.exp(out_rgb) / np.sum(np.exp(out_rgb))
    print("Raw RGB (/255):", prob_rgb)
    
    # Try RGB + ImageNet
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img_norm = (img_rgb_base - mean) / std
    img_norm = np.transpose(img_norm, (2, 0, 1))
    img_norm = np.expand_dims(img_norm, axis=0)
    out_norm = inf.session.run([inf.output_name], {inf.input_name: img_norm})[0][0]
    prob_norm = np.exp(out_norm) / np.sum(np.exp(out_norm))
    print("RGB + ImageNet Norm:", prob_norm)

test()
