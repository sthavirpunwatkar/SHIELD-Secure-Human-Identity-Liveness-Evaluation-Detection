import cv2
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from services.fusion_service import fusion_service

def test_video(video_path):
    print(f"Testing video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        # Test every 15th frame to speed up testing but still get a sense
        if frame_count % 15 == 0:
            res = fusion_service.process_frame(frame)
            print(f"Frame {frame_count}: Verdict={res['verdict']}, Score={res.get('confidence')}")
            if res['verdict'] == 'Spoof':
                print(f"  Reason: {res.get('details', {}).get('reason')}")
                print(f"  Breakdown: {res.get('details', {})}")
                
    cap.release()
    print("Done.\n")

if __name__ == '__main__':
    test_video('/home/sp/2026-07-06 20-36-14.mp4')
    test_video('/home/sp/2026-07-06 20-37-48.mp4')
