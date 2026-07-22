import cv2
import numpy as np
import onnxruntime as ort
import sys
import os
sys.path.append(os.path.abspath("."))
from inference.yolo_detector import YoloSegDetector
from scipy.signal import butter, filtfilt

def test_real():
    video_path = '/home/sp/2026-07-06 20-36-14.mp4'
    if not os.path.exists(video_path):
        print("Video not found.")
        return
        
    cap = cv2.VideoCapture(video_path)
    yolo = YoloSegDetector()
    buffer = []
    
    while cap.isOpened() and len(buffer) < 150:
        ret, frame = cap.read()
        if not ret: break
        faces = yolo.detect_faces(frame)
        if not faces: continue
        
        x1, y1, x2, y2 = [int(v) for v in faces[0]['bbox']]
        h, w = frame.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        box_w, box_h = x2 - x1, y2 - y1
        
        if box_h > 0 and box_w > 0:
            roi_y1 = y1 + int(box_h * 0.50)
            roi_y2 = y1 + int(box_h * 0.75)
            roi_x1 = x1 + int(box_w * 0.60)
            roi_x2 = x1 + int(box_w * 0.80)
            roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
            if roi.size > 0:
                buffer.append(float(np.mean(roi[:, :, 1])))
    
    cap.release()
    print(f"Extracted {len(buffer)} frames.")
    
    if len(buffer) < 150:
        return
        
    sig_raw = np.array(buffer, dtype=np.float32)
    b, a = butter(2, [0.7/15.0, 4.0/15.0], btype='band')
    sig_bandpass = filtfilt(b, a, sig_raw)
    
    sig = sig_bandpass.astype(np.float32)
    sig = (sig - sig.mean()) / (sig.std() + 1e-6)
    
    session = ort.InferenceSession("models/rppg_1dcnn_v2_int8.onnx", providers=['CPUExecutionProvider'])
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    sig_in = np.expand_dims(np.expand_dims(sig, axis=0), axis=0)
    out = session.run([output_name], {input_name: sig_in})[0]
    print(f"ONNX Output for real video: {out[0][0]}")

test_real()
