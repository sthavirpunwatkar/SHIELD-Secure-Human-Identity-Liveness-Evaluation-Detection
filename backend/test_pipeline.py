import cv2
import sys
from services.fusion_service import fusion_service

print("Testing with subject_0.jpg")
frame = cv2.imread("../data/raw_mock/live/subject_0.jpg")
if frame is None:
    print("Could not load image")
    sys.exit(1)

res = fusion_service.process_frame(frame)
print("Result:", res)
