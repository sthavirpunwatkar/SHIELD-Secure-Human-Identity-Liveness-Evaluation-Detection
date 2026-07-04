import cv2
import numpy as np
import time
import sys
import os

# Add root to path to allow sibling imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from inference.face_detector import FaceDetector
from inference.antispoof import AntispoofInference
from inference.behavioral_analyzer import BehavioralAnalyzer
from inference.rppg_detector import RPPGDetector
from inference.quality import QualityScoreEngine
from inference.fusion_engine import FusionEngine
from inference.challenge_engine import ChallengeSession


class FusionService:
    def __init__(self):
        """
        Initializes all core AI models for orchestration.
        """
        self.detector = FaceDetector()
        self.quality_engine = QualityScoreEngine()
        self.antispoof = AntispoofInference()
        self.behavioral = BehavioralAnalyzer()
        self.rppg = RPPGDetector()
        self.fusion_engine = FusionEngine()

    def process_frame(self, frame, challenge_session=None):
        """
        Runs the multi-modal pipeline on a single frame.
        :param frame: OpenCV image (BGR).
        :param challenge_session: Optional ChallengeSession for active challenge processing.
        :return: Dict containing the final verdict and detailed scores.
        """
        start_time = time.time()

        # 1. Face Detection
        faces = self.detector.detect_faces(frame)
        if not faces:
            return {
                "type": "verdict",
                "verdict": "No Face Detected",
                "confidence": 0.0,
                "status": "fail",
                "details": {}
            }

        face_info = faces[0]
        bbox = face_info['bbox']
        crop = self.detector.crop_face(frame, bbox)

        # 2. Quality Gate
        quality_res = self.quality_engine.evaluate(frame, crop)
        if not quality_res["passes_gate"]:
            return {
                "type": "verdict",
                "verdict": "Low Quality",
                "confidence": quality_res["quality_score"],
                "status": "fail",
                "quality_metrics": quality_res["metrics"],
                "details": {"reason": "Quality gate failed"}
            }

        # 3. Multi-Modal Inference
        
        # JPEG Compression Defense (clears adversarial noise)
        _, jpeg_buf = cv2.imencode('.jpg', crop, [cv2.IMWRITE_JPEG_QUALITY, 90])
        defended_crop = cv2.imdecode(jpeg_buf, cv2.IMREAD_COLOR)
        if defended_crop is not None:
            crop = defended_crop

        as_score = self.antispoof.predict(crop)

        # Behavioral Score (Blink) — now uses real EAR-based detection
        behavior = self.behavioral.analyze(frame, faces=faces)
        blink_score = 1.0 if behavior['blink_detected'] else 0.0

        # Physiological Score (rPPG)
        rppg_score = self.rppg.update(frame)

        # 4. Challenge Score
        challenge_score = 0.5  # Default neutral if no active session
        challenge_info = None

        if challenge_session is not None:
            current_challenge = challenge_session.get_current_challenge()
            if current_challenge is not None:
                # Verify the current challenge using behavioral analyzer
                challenge_result = self.behavioral.verify_challenge(
                    frame, current_challenge.value
                )
                challenge_info = {
                    "action": current_challenge.value,
                    "action_detected": challenge_result["action_detected"],
                    "confidence": challenge_result["confidence"],
                    "details": challenge_result["details"]
                }

                # Submit the frame result to the challenge session
                session_update = challenge_session.submit_frame_result(
                    challenge_result["action_detected"]
                )
                challenge_info["session_update"] = session_update

            # Use the challenge session's computed score
            challenge_score = challenge_session.get_challenge_score()

        # 5. Decision Fusion
        fusion_res = self.fusion_engine.fuse(
            rppg_score=rppg_score,
            blink_score=blink_score,
            antispoof_score=as_score,
            challenge_score=challenge_score
        )

        processing_time = time.time() - start_time
        h, w = frame.shape[:2]

        result = {
            "type": "verdict",
            "verdict": fusion_res["verdict"],
            "confidence": fusion_res["final_score"],
            "status": "success",
            "processing_time_ms": int(processing_time * 1000),
            "frame_size": [w, h],
            "details": fusion_res["breakdown"],
            "quality_metrics": quality_res["metrics"],
            "bbox": bbox
        }

        # Include challenge information if active
        if challenge_info is not None:
            result["challenge_info"] = challenge_info

        return result

    def process_challenge_frame(self, frame, challenge_session):
        """
        Specialized processing for challenge-mode frames.
        Runs the full pipeline AND evaluates the current challenge action.

        :param frame: OpenCV image (BGR).
        :param challenge_session: Active ChallengeSession instance.
        :return: Dict with verdict + challenge status.
        """
        return self.process_frame(frame, challenge_session=challenge_session)


# Global instance
fusion_service = FusionService()
