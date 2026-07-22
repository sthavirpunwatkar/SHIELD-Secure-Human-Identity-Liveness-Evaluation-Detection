import cv2
from inference.yolo_detector import YoloSegDetector
detector = YoloSegDetector()
frame = cv2.imread("data/UBFC_rPPG/train/real/sample_0.jpg")
print("Faces in UBFC:", len(detector.detect_faces(frame)))
