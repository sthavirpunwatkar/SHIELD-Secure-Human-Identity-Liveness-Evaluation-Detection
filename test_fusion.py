from inference.fusion_engine import FusionEngine

def test_fusion_engine():
    print("--- SHIELD Fusion Engine Test ---")
    engine = FusionEngine()

    # Case 1: High liveness in all components
    print("\nCase 1: Clear Live")
    result = engine.fuse(rppg_score=0.9, blink_score=1.0, antispoof_score=0.95, challenge_score=1.0)
    print(f"Final Score: {result['final_score']}, Verdict: {result['verdict']}")

    # Case 2: Mixed signals
    print("\nCase 2: Mixed Signals (Possible Spoof)")
    result = engine.fuse(rppg_score=0.2, blink_score=0.1, antispoof_score=0.3, challenge_score=0.5)
    print(f"Final Score: {result['final_score']}, Verdict: {result['verdict']}")

    # Case 3: Anti-spoof model says real, but physiological says fake
    print("\nCase 3: Physiological Failure (Possible Replay)")
    result = engine.fuse(rppg_score=0.1, blink_score=0.5, antispoof_score=0.8, challenge_score=0.5)
    print(f"Final Score: {result['final_score']}, Verdict: {result['verdict']}")

    print("\n--- Fusion Engine Test Complete ---")

if __name__ == "__main__":
    test_fusion_engine()
