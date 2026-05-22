import cv2
import numpy as np

class IlluminationDetector:
    def __init__(self, low_threshold=40, high_threshold=220):
        """
        Initializes the Illumination Detector.
        :param low_threshold: Minimum mean brightness for 'good' illumination.
        :param high_threshold: Maximum mean brightness for 'good' illumination.
        """
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def detect(self, face_crop):
        """
        Detects if the illumination is 'good', 'underexposed', or 'overexposed'.
        :param face_crop: OpenCV image (BGR).
        :return: (status, mean_brightness)
        """
        if face_crop is None or face_crop.size == 0:
            return "unknown", 0.0

        gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
        mean_brightness = float(np.mean(gray))

        if mean_brightness < self.low_threshold:
            status = "underexposed"
        elif mean_brightness > self.high_threshold:
            status = "overexposed"
        else:
            status = "good"

        return status, mean_brightness

if __name__ == "__main__":
    detector = IlluminationDetector()
    dummy_face = np.ones((100, 100, 3), dtype=np.uint8) * 128
    status, brightness = detector.detect(dummy_face)
    print(f"Status: {status}, Brightness: {brightness}")
