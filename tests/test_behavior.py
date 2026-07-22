import cv2
import pytest
from inference.behavioral_analyzer import BehavioralAnalyzer

@pytest.mark.skip(reason="Needs local image and dependencies")
def test_behavior():
    analyzer = BehavioralAnalyzer()
    frame = cv2.imread(".venv/lib/python3.14/site-packages/ultralytics/assets/zidane.jpg")
    if frame is None:
        print("Could not load image")
        return

    result = analyzer.analyze(frame)
    print("Landmarks found:", result.get("landmarks_found"))
