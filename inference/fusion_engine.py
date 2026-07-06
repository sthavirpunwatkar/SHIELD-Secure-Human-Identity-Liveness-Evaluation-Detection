class FusionEngine:
    def __init__(self, weights=None):
        """
        Initializes the Fusion Engine with customizable weights.
        :param weights: Optional dict. If not provided, dynamic weights are used.
        """
        self.weights = weights

    def fuse(self, rppg_score, blink_score, antispoof_score, challenge_score=0.0, is_challenge_active=False):
        """
        Fuses multiple liveness scores into a single final score.
        Uses dynamic weighting depending on whether a challenge is active.
        """
        if self.weights is not None:
            active_weights = self.weights
        elif is_challenge_active:
            active_weights = {
                "rppg": 0.10,
                "blink": 0.10,
                "antispoof": 0.40,
                "challenge": 0.40
            }
        else:
            if blink_score == 0.0:
                active_weights = {
                    "rppg": 0.20,
                    "blink": 0.0,
                    "antispoof": 0.80,
                    "challenge": 0.0
                }
            else:
                active_weights = {
                    "rppg": 0.20,
                    "blink": 0.20,
                    "antispoof": 0.60,
                    "challenge": 0.0
                }

        # Critical Explainable Thresholds
        if antispoof_score < 0.25:
            final_score = float(antispoof_score)
            verdict = "Spoof"
            reason = "Critically failed appearance anti-spoofing."
        else:
            final_score = (
                (active_weights["rppg"] * rppg_score) +
                (active_weights["blink"] * blink_score) +
                (active_weights["antispoof"] * antispoof_score) +
                (active_weights.get("challenge", 0) * challenge_score)
            )
            verdict = "Live" if final_score > 0.5 else "Spoof"
            reason = "Passed multi-modal checks." if final_score > 0.5 else "Multi-modal combined score below threshold."

        return {
            "final_score": round(final_score, 4),
            "verdict": verdict,
            "reason": reason,
            "breakdown": {
                "rppg": round(rppg_score, 4),
                "blink": round(blink_score, 4),
                "antispoof": round(antispoof_score, 4),
                "challenge": round(challenge_score, 4) if is_challenge_active else None,
                "combined": round(final_score, 4)
            },
            "weights": active_weights
        }

if __name__ == "__main__":
    engine = FusionEngine()
    result = engine.fuse(0.8, 1.0, 0.9, 0.5)
    print(f"Fusion Result: {result}")
