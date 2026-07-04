import cv2
import numpy as np

class BlurDetector:
    def __init__(self, threshold=20.0):
        """
        Initializes the Blur Detector using Variance of Laplacian.
        :param threshold: Threshold below which a frame is considered blurry.
        """
        self.threshold = threshold

    def detect(self, face_crop):
        """
        Detects if the face crop is blurry.
        :param face_crop: OpenCV image (BGR).
        :return: (is_blurry, blur_score)
        """
        if face_crop is None or face_crop.size == 0:
            return True, 0.0

        gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
        # Compute the Laplacian of the image and then the variance
        blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        
        is_blurry = bool(blur_score < self.threshold)
        return is_blurry, blur_score

if __name__ == "__main__":
    detector = BlurDetector()
    dummy_face = np.zeros((100, 100, 3), dtype=np.uint8)
    is_blurry, score = detector.detect(dummy_face)
    print(f"Is Blurry: {is_blurry}, Score: {score}")
