import cv2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from backend.services.fusion_service import fusion_service

def run():
    video_path = '/home/sp/Downloads/202606231804.mp4'
    cap = cv2.VideoCapture(video_path)
    
    class MockDetector:
        def detect_faces(self, frame):
            return [{"bbox": [100, 100, 300, 300], "is_mask_spoof": False}]
        def crop_face(self, frame, bbox):
            return frame
            
    class MockQuality:
        def evaluate(self, frame, crop):
            return {"passes_gate": True, "quality_score": 1.0, "metrics": {}}
            
    fusion_service.detector = MockDetector()
    fusion_service.quality_engine = MockQuality()
    
    count = 0
    while cap.isOpened() and count < 10:
        ret, frame = cap.read()
        if not ret: break
        print(f"\n--- Processing frame {count} ---")
        try:
            res = fusion_service.process_frame(frame, frame_number=count, capture_timestamp="")
        except Exception as e:
            print(f"EXCEPTION: {e}")
        count += 1
    cap.release()

if __name__ == '__main__':
    run()
