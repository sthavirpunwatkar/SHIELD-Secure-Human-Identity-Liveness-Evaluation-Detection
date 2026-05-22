from .blur_detector import BlurDetector
from .illumination_detector import IlluminationDetector
from .pose_filter import PoseFilter
from .occlusion_detector import OcclusionDetector

class QualityScoreEngine:
    def __init__(self):
        """
        Initializes the Quality Score Engine with all sub-detectors.
        """
        self.blur_detector = BlurDetector()
        self.illumination_detector = IlluminationDetector()
        self.pose_filter = PoseFilter()
        self.occlusion_detector = OcclusionDetector()

    def evaluate(self, frame, face_crop):
        """
        Evaluates the quality of the face frame.
        :param frame: Full BGR frame.
        :param face_crop: Cropped BGR face.
        :return: Dict containing quality metrics and final decision.
        """
        is_blurry, blur_score = self.blur_detector.detect(face_crop)
        illum_status, brightness = self.illumination_detector.detect(face_crop)
        pose_status, pose_info = self.pose_filter.detect(frame)
        is_occluded, occlusion_score = self.occlusion_detector.detect(face_crop)

        # Logic for passing the quality gate
        passes_gate = (
            not is_blurry and 
            illum_status == "good" and 
            pose_status == "frontal" and 
            not is_occluded
        )

        # Calculate a normalized quality score (0.0 to 1.0)
        # For now, a simple binary-weighted score
        score = 0.0
        if not is_blurry: score += 0.25
        if illum_status == "good": score += 0.25
        if pose_status == "frontal": score += 0.25
        if not is_occluded: score += 0.25

        return {
            "quality_score": score,
            "passes_gate": passes_gate,
            "metrics": {
                "blur": {"is_blurry": is_blurry, "score": blur_score},
                "illumination": {"status": illum_status, "brightness": brightness},
                "pose": {"status": pose_status, "info": pose_info},
                "occlusion": {"is_occluded": is_occluded, "score": occlusion_score}
            }
        }

if __name__ == "__main__":
    import numpy as np
    engine = QualityScoreEngine()
    print("QualityScoreEngine ready.")
