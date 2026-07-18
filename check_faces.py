import cv2
import sys
sys.path.append('backend')
from inference.yolo_detector import YoloSegDetector

yolo = YoloSegDetector()
cap = cv2.VideoCapture('/home/sp/Public/screen record/2026-07-05 00-12-39.mp4')
ret, frame = cap.read()
if ret:
    faces = yolo.detect_faces(frame)
    print(f"Faces found: {len(faces)}")
else:
    print("Could not read video")
