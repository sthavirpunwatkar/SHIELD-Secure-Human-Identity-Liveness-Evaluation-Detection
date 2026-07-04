import os
import sys
import unittest

# Add root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.services.fusion_service import fusion_service
from inference.session_manager import SessionManager
from inference.temporal_validator import TemporalValidator
from inference.challenge_engine import ChallengeSession

class TestAuditIntegrity(unittest.TestCase):
    def test_temporal_validator_integration(self):
        """Proof that TemporalValidator is part of the SessionManager workflow."""
        sm = SessionManager()
        session = sm.create_session(client_id="test_client")
        self.assertIsInstance(session.temporal_validator, TemporalValidator)
        print("✓ TemporalValidator found in SessionManager.")

    def test_challenge_engine_integration(self):
        """Proof that ChallengeSession is integrated with FusionService."""
        from unittest.mock import MagicMock
        import numpy as np

        # Save original methods
        orig_detect = fusion_service.detector.detect_faces
        orig_crop = fusion_service.detector.crop_face
        orig_evaluate = fusion_service.quality_engine.evaluate
        orig_verify = fusion_service.behavioral.verify_challenge

        try:
            # Mock them
            fusion_service.detector.detect_faces = MagicMock(return_value=[{"bbox": [0, 0, 10, 10]}])
            fusion_service.detector.crop_face = MagicMock(return_value=np.zeros((10, 10, 3), dtype=np.uint8))
            fusion_service.quality_engine.evaluate = MagicMock(return_value={"passes_gate": True, "quality_score": 0.95, "metrics": {}})
            fusion_service.behavioral.verify_challenge = MagicMock(return_value={
                "action_detected": True,
                "confidence": 0.98,
                "details": {}
            })

            cs = ChallengeSession(num_challenges=1)
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            
            # This call should not crash and should return a dict with challenge_info
            result = fusion_service.process_frame(frame, challenge_session=cs)
            self.assertIn("challenge_info", result)
            print("✓ ChallengeSession integrated with FusionService.")
        finally:
            # Restore
            fusion_service.detector.detect_faces = orig_detect
            fusion_service.detector.crop_face = orig_crop
            fusion_service.quality_engine.evaluate = orig_evaluate
            fusion_service.behavioral.verify_challenge = orig_verify

    def test_rppg_detector_state(self):
        """Proof that RPPGDetector is available in FusionService."""
        from inference.rppg_detector import RPPGDetector
        self.assertIsInstance(fusion_service.rppg, RPPGDetector)
        print("✓ RPPGDetector found in FusionService.")

if __name__ == "__main__":
    unittest.main()
