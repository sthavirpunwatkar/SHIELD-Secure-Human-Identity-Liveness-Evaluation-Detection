import cv2
import numpy as np

class QualityScoreEngine:
    def __init__(self, blur_threshold=20.0, low_illum=15, high_illum=240):
        self.blur_threshold = blur_threshold
        self.low_illum = low_illum
        self.high_illum = high_illum

    def evaluate(self, frame, face_crop):
        if face_crop is None or face_crop.size == 0:
            return {"quality_score": 0.0, "passes_gate": False, "metrics": {}}

        gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
        
        # Blur check
        blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        is_blurry = blur_score < self.blur_threshold
        
        # Illumination check
        mean_brightness = float(np.mean(gray))
        if mean_brightness < self.low_illum:
            illum_status = "underexposed"
        elif mean_brightness > self.high_illum:
            illum_status = "overexposed"
        else:
            illum_status = "good"
            
        passes_gate = not is_blurry and illum_status == "good"
        score = 0.5 if not is_blurry else 0.0
        score += 0.5 if illum_status == "good" else 0.0

        return {
            "quality_score": score,
            "passes_gate": passes_gate,
            "metrics": {
                "blur": {"is_blurry": is_blurry, "score": blur_score},
                "illumination": {"status": illum_status, "brightness": mean_brightness},
            }
        }
