import os
import json
import cv2
import time
from inference.fusion_engine import FusionEngine
from inference.antispoof import AntispoofInference
from inference.rppg_detector import RPPGDetector
from inference.behavioral_analyzer import BehavioralAnalyzer
from .metrics import FASMetrics

class BenchmarkEngine:
    def __init__(self, manifest_path="data/processed/manifest.json"):
        self.manifest_path = manifest_path
        self.fusion_engine = FusionEngine()
        self.antispoof = AntispoofInference()
        self.rppg = RPPGDetector()
        self.behavioral = BehavioralAnalyzer()

    def run_benchmark(self):
        if not os.path.exists(self.manifest_path):
            print(f"Manifest not found at {self.manifest_path}. Run DataWrangler first.")
            return None

        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)

        print(f"--- Starting Benchmark on {len(manifest)} samples ---")
        
        results = []
        y_true = []
        y_pred = []
        
        start_time = time.time()
        
        for item in manifest:
            img_path = item["path"]
            label = item["label"]
            
            frame = cv2.imread(img_path)
            if frame is None: continue
            
            # Use simple center crop for benchmark if face detector is not explicitly called
            h, w = frame.shape[:2]
            crop = frame[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]
            
            # Get component scores
            try:
                as_score = self.antispoof.predict(crop)
            except RuntimeError:
                as_score = 0.0

            try:
                rppg_score = self.rppg.update(frame)
            except RuntimeError:
                rppg_score = 0.0
            behavior = self.behavioral.analyze(frame)
            blink_score = 1.0 if behavior["blink_detected"] else 0.0
            
            # Fusion
            fusion_res = self.fusion_engine.fuse(
                rppg_score=rppg_score,
                blink_score=blink_score,
                antispoof_score=as_score,
                challenge_score=0.0, # Not testing active challenges here
                is_challenge_active=False
            )
            
            y_true.append(1 if label == "live" else 0)
            y_pred.append(fusion_res["final_score"])
            
            results.append({
                "path": img_path,
                "label": label,
                "score": fusion_res["final_score"],
                "verdict": fusion_res["verdict"]
            })

        total_time = time.time() - start_time
        fps = len(manifest) / total_time if total_time > 0 else 0
        
        metrics = FASMetrics.calculate(y_true, y_pred)
        metrics["fps"] = round(fps, 2)
        metrics["total_samples"] = len(manifest)
        
        return metrics, results

if __name__ == "__main__":
    engine = BenchmarkEngine()
    # stats, res = engine.run_benchmark()
    print("BenchmarkEngine ready.")


# ------------------------------------------------------------------
# Challenge-Response Benchmark
# ------------------------------------------------------------------

class ChallengeBenchmark:
    """Benchmarks for the Active Challenge-Response engine.

    Provides three benchmark methods that exercise the challenge
    protocol, blink detection, and head-pose estimation pipelines.
    Each method can run in *synthetic* mode (no real video data needed)
    or against a directory of real video frames.
    """

    def __init__(self) -> None:
        from inference.challenge_engine import ChallengeSession, ChallengeType
        from inference.behavioral_analyzer import BehavioralAnalyzer

        self.ChallengeSession = ChallengeSession
        self.ChallengeType = ChallengeType
        self.behavioral = BehavioralAnalyzer()

    # ------------------------------------------------------------------
    # Protocol benchmark
    # ------------------------------------------------------------------

    def benchmark_challenge_protocol(self, num_trials: int = 50) -> dict:
        """Run *num_trials* simulated challenge sessions and report stats.

        Half of the sessions simulate a user who passes every challenge;
        the other half simulate a user who never responds (timeout).

        :param num_trials: Number of sessions to simulate.
        :return: Dict with ``pass_rate``, ``fail_rate``,
            ``avg_time_per_session_ms``, and ``total_trials``.
        """
        passed = 0
        total_time_ms = 0.0

        for i in range(num_trials):
            t0 = time.time()
            session = self.ChallengeSession(
                num_challenges=3,
                timeout_per_challenge=0.05,
                max_retries=0,
            )

            while session.get_current_challenge() is not None:
                session.start_current_challenge()
                # Even trials pass, odd trials fail (timeout)
                if i % 2 == 0:
                    session.submit_frame_result(action_detected=True)
                else:
                    time.sleep(0.06)
                    session.submit_frame_result(action_detected=False)

            elapsed_ms = (time.time() - t0) * 1000.0
            total_time_ms += elapsed_ms

            if session.get_challenge_score() == 1.0:
                passed += 1

        pass_rate = passed / num_trials if num_trials else 0.0

        return {
            "pass_rate": round(pass_rate, 4),
            "fail_rate": round(1.0 - pass_rate, 4),
            "avg_time_per_session_ms": round(total_time_ms / max(num_trials, 1), 2),
            "total_trials": num_trials,
        }

    # ------------------------------------------------------------------
    # Blink-detection benchmark
    # ------------------------------------------------------------------

    def benchmark_blink_detection(self, video_dir: str = None) -> dict:
        """Benchmark blink detection accuracy.

        If *video_dir* is provided, frames are loaded from that
        directory (``*.jpg`` / ``*.png``).  Otherwise synthetic grey
        frames are used — these will **not** trigger real MediaPipe
        detections, so the benchmark reports baseline false-positive
        rates on blank images.

        :param video_dir: Optional path to a directory of BGR frames.
        :return: Dict with ``detection_rate`` and
            ``false_positive_rate``.
        """
        frames: list = []

        if video_dir and os.path.isdir(video_dir):
            for fname in sorted(os.listdir(video_dir)):
                if fname.lower().endswith((".jpg", ".png")):
                    fpath = os.path.join(video_dir, fname)
                    img = cv2.imread(fpath)
                    if img is not None:
                        frames.append(img)
        else:
            # Synthetic frames (uniform grey — no real face)
            import numpy as np
            for _ in range(20):
                frames.append(np.full((480, 640, 3), 128, dtype=np.uint8))

        detections = 0
        for frame in frames:
            result = self.behavioral.verify_challenge(frame, "blink")
            if result["action_detected"]:
                detections += 1

        total = len(frames) if frames else 1
        detection_rate = detections / total
        # On synthetic data every detection is a false positive
        false_positive_rate = detection_rate if video_dir is None else 0.0

        return {
            "detection_rate": round(detection_rate, 4),
            "false_positive_rate": round(false_positive_rate, 4),
            "total_frames": total,
        }

    # ------------------------------------------------------------------
    # Head-pose benchmark
    # ------------------------------------------------------------------

    def benchmark_head_pose(self, video_dir: str = None) -> dict:
        """Benchmark head-pose estimation accuracy.

        Follows the same pattern as :meth:`benchmark_blink_detection`:
        real frames from *video_dir* or synthetic grey frames.

        :param video_dir: Optional path to a directory of BGR frames.
        :return: Dict with ``detection_rate`` and
            ``false_positive_rate``.
        """
        frames: list = []

        if video_dir and os.path.isdir(video_dir):
            for fname in sorted(os.listdir(video_dir)):
                if fname.lower().endswith((".jpg", ".png")):
                    fpath = os.path.join(video_dir, fname)
                    img = cv2.imread(fpath)
                    if img is not None:
                        frames.append(img)
        else:
            import numpy as np
            for _ in range(20):
                frames.append(np.full((480, 640, 3), 128, dtype=np.uint8))

        detections = 0
        for frame in frames:
            result = self.behavioral.verify_challenge(frame, "turn_left")
            if result["action_detected"]:
                detections += 1

        total = len(frames) if frames else 1
        detection_rate = detections / total
        false_positive_rate = detection_rate if video_dir is None else 0.0

        return {
            "detection_rate": round(detection_rate, 4),
            "false_positive_rate": round(false_positive_rate, 4),
            "total_frames": total,
        }


if __name__ == "__main__":
    engine = BenchmarkEngine()
    print("BenchmarkEngine ready.")

    cb = ChallengeBenchmark()
    print("\n--- Challenge Protocol Benchmark (5 trials) ---")
    print(cb.benchmark_challenge_protocol(num_trials=5))
    print("\n--- Blink Detection Benchmark (synthetic) ---")
    print(cb.benchmark_blink_detection())
    print("\n--- Head Pose Benchmark (synthetic) ---")
    print(cb.benchmark_head_pose())

