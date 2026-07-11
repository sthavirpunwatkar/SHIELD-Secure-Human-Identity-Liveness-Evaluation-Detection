import cv2
import time
import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from inference.yolo_detector import YoloSegDetector
from inference.antispoof import AntispoofInference
from inference.behavioral_analyzer import BehavioralAnalyzer
from inference.rppg_detector import RPPGDetector

def run_ablation():
    video_path = '/home/sp/2026-07-06 20-36-14.mp4'
    cap = cv2.VideoCapture(video_path)
    
    yolo = YoloSegDetector()
    antispoof = AntispoofInference()
    behavioral = BehavioralAnalyzer()
    rppg = RPPGDetector()

    configs = {
        'A': ['yolo'],
        'B': ['yolo', 'antispoof'],
        'C': ['yolo', 'mediapipe'],
        'D': ['yolo', 'blink'],
        'F': ['yolo', 'rppg'],
        'J': ['yolo', 'antispoof', 'mediapipe', 'rppg']
    }
    
    frames_to_test = []
    count = 0
    while cap.isOpened() and count < 30:
        ret, frame = cap.read()
        if not ret: break
        frames_to_test.append(frame)
        count += 1
    cap.release()
    
    results = {}
    for cfg, modules in configs.items():
        latencies = []
        for frame in frames_to_test:
            from backend.services.fusion_service import fusion_service
            res = fusion_service.process_frame(frame, frame_number=0, capture_timestamp="")
            print(res)
            latencies.append((end_t - start_t) * 1000)
            
        results[cfg] = np.mean(latencies) if latencies else 0
        print(f"Config {cfg}: Avg Latency {results[cfg]:.2f} ms")

if __name__ == '__main__':
    run_ablation()
