import cv2
import time
import sys
import os
import numpy as np
import asyncio
import sqlite3

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from inference.yolo_detector import YoloSegDetector
from inference.behavioral_analyzer import BehavioralAnalyzer
from inference.rppg_detector import RPPGDetector
from inference.session_manager import VerificationSession
from services.db_service import db_service

def exp1_rppg_roi():
    print("--- EXP 1: rPPG ROI ---")
    rppg = RPPGDetector()
    # Create black frame (100x100)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    # Put a "green face" at the top-left (0:30, 0:30)
    frame[0:30, 0:30, 1] = 255
    # The center is black
    signal = rppg.extract_roi_signal(frame)
    if signal == 0.0:
        print("RESULT: 0.0 (Extracted background/center instead of face)")
    else:
        print(f"RESULT: {signal} (Extracted face)")
    print()

def exp2_identity_yaw():
    print("--- EXP 2: Identity Signature Yaw ---")
    analyzer = BehavioralAnalyzer()
    session = VerificationSession()
    
    video_path = '/home/sp/2026-07-06 20-36-14.mp4'
    cap = cv2.VideoCapture(video_path)
    
    signatures = []
    poses = []
    
    count = 0
    while cap.isOpened() and count < 150:
        ret, frame = cap.read()
        if not ret: break
        
        # Test every 15 frames
        if count % 15 == 0:
            res = analyzer.analyze(frame)
            if res.get('landmarks_found'):
                landmarks = res['raw_landmarks']
                sig = session._calculate_landmark_signature(landmarks)
                if sig is not None:
                    signatures.append(sig)
                    poses.append(res['pose']['yaw'])
        count += 1
    cap.release()
    
    if len(signatures) >= 2:
        # Compare first signature with others
        base_sig = signatures[0]
        max_dist = 0
        max_yaw_diff = 0
        for i in range(1, len(signatures)):
            dist = np.linalg.norm(base_sig - signatures[i])
            yaw_diff = abs(poses[0] - poses[i])
            if dist > max_dist:
                max_dist = dist
                max_yaw_diff = yaw_diff
                
        print(f"Max Identity Distance: {max_dist:.4f} (Threshold: 0.50)")
        print(f"Yaw Diff at Max Distance: {max_yaw_diff:.2f} degrees")
        if max_dist > 0.50:
            print("RESULT: FAILED (Identity swap triggered by head turn)")
        elif max_dist > 0.20:
            print("RESULT: VULNERABLE (Large distance shift from yaw)")
        else:
            print("RESULT: STABLE")
    else:
        print("RESULT: Not enough data")
    print()

def exp3_async_blocking():
    print("--- EXP 3: Async Event Loop Blocking ---")
    import time
    
    async def blocking_db_write():
        # simulate db write
        start = time.time()
        for i in range(100):
            db_service.log_verification({"session_id": f"test_{i}", "verdict": "Live"})
        return time.time() - start

    async def background_task():
        start = time.time()
        await asyncio.sleep(0.1)
        return time.time() - start

    async def main():
        # Start background task that should wake up in 100ms
        task1 = asyncio.create_task(background_task())
        
        # Start a blocking DB write concurrently
        db_time = await blocking_db_write()
        
        # See how long the background task actually took
        bg_time = await task1
        
        print(f"DB Write Time: {db_time*1000:.2f} ms")
        print(f"Background Task (expected 100ms) took: {bg_time*1000:.2f} ms")
        if bg_time > 0.15:
            print("RESULT: BLOCKED (Event loop was halted by sync SQLite)")
        else:
            print("RESULT: NOT BLOCKED")
            
    asyncio.run(main())
    print()

def exp4_jpeg_defense_latency():
    print("--- EXP 4: JPEG Defense Latency ---")
    crop = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    start = time.time()
    for _ in range(100):
        _, jpeg_buf = cv2.imencode('.jpg', crop, [cv2.IMWRITE_JPEG_QUALITY, 90])
        defended_crop = cv2.imdecode(jpeg_buf, cv2.IMREAD_COLOR)
    end = time.time()
    
    avg_ms = ((end - start) / 100) * 1000
    print(f"Avg Latency per encode/decode: {avg_ms:.2f} ms")
    if avg_ms > 2.0:
        print("RESULT: HIGH LATENCY BOTTLENECK")
    else:
        print("RESULT: ACCEPTABLE")
    print()

def exp5_yolo_redundancy():
    print("--- EXP 5: YOLO Redundancy ---")
    yolo = YoloSegDetector()
    analyzer = BehavioralAnalyzer()
    
    video_path = '/home/sp/2026-07-06 20-36-14.mp4'
    cap = cv2.VideoCapture(video_path)
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("Failed to read video")
        return
        
    start = time.time()
    faces = yolo.detect_faces(frame)
    yolo_time = (time.time() - start) * 1000
    
    start = time.time()
    res = analyzer.analyze(frame)
    mp_time = (time.time() - start) * 1000
    
    print(f"YOLO Time: {yolo_time:.2f} ms")
    print(f"MediaPipe Time: {mp_time:.2f} ms")
    if res.get('landmarks_found') and faces:
        print("RESULT: REDUNDANT (Both found face successfully)")
    else:
        print("RESULT: NOT REDUNDANT")
    print()

if __name__ == '__main__':
    exp1_rppg_roi()
    exp2_identity_yaw()
    exp3_async_blocking()
    exp4_jpeg_defense_latency()
    exp5_yolo_redundancy()
