import cv2
import sys
import os
import numpy as np
import onnxruntime as ort

def get_probs(model_path, crop):
    session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    # Preprocess
    img = cv2.resize(crop, (80 if 'minifas' in model_path else 224, 80 if 'minifas' in model_path else 224))
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    
    out = session.run([output_name], {input_name: img})[0][0]
    prob = np.exp(out) / np.sum(np.exp(out))
    return prob

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
from inference.yolo_detector import YoloSegDetector

det = YoloSegDetector()
cap = cv2.VideoCapture('/home/sp/2026-07-06 20-36-14.mp4')
for _ in range(30):
    ret, frame = cap.read()
bbox = det.detect_faces(frame)[0]['bbox']
crop = det.crop_face(frame, bbox)

candidates = [
    'backend/models/efficientnet_fas.onnx',
    'backend/models/minifas_antispoof_v2_int8.onnx',
    'backend/models/minifas_antispoof_v2.onnx'
]

for cand in candidates:
    if os.path.exists(cand):
        print(cand, get_probs(cand, crop))
    else:
        print(cand, "not found")
