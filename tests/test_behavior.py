import cv2
from inference.behavioral_analyzer import BehavioralAnalyzer

analyzer = BehavioralAnalyzer()
frame = cv2.imread(".venv/lib/python3.14/site-packages/ultralytics/assets/zidane.jpg")
if frame is None:
    print("Could not load image")
    exit(1)

result = analyzer.analyze(frame)
print("Landmarks found:", result.get("landmarks_found"))
