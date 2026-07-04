class FusionEngine:
    def __init__(self, weights=None):
        """
        Initializes the Fusion Engine with customizable weights.
        :param weights: Dict containing weights for each component.
        """
        if weights is None:
            # Default weights as per gemini_next_update.md
            self.weights = {
                "rppg": 0.10,
                "blink": 0.10,
                "antispoof": 0.15,
                "challenge": 0.65
            }
        else:
            self.weights = weights

    def fuse(self, rppg_score, blink_score, antispoof_score, challenge_score=0.5):
        """
        Fuses multiple liveness scores into a single final score.
        :param rppg_score: Physiological score (0-1)
        :param blink_score: Behavioral/Blink score (0-1)
        :param antispoof_score: Deep learning anti-spoof score (0-1)
        :param challenge_score: Active challenge response score (0-1)
        :return: Dict with final_score and breakdown.
        """
        final_score = (
            (self.weights["rppg"] * rppg_score) +
            (self.weights["blink"] * blink_score) +
            (self.weights["antispoof"] * antispoof_score) +
            (self.weights["challenge"] * challenge_score)
        )

        verdict = "Live" if final_score > 0.5 else "Spoof"
        
        return {
            "final_score": round(final_score, 4),
            "verdict": verdict,
            "breakdown": {
                "rppg": rppg_score,
                "blink": blink_score,
                "antispoof": antispoof_score,
                "challenge": challenge_score,
                "combined": round(final_score, 4)
            },
            "weights": self.weights
        }

if __name__ == "__main__":
    engine = FusionEngine()
    result = engine.fuse(0.8, 1.0, 0.9, 0.5)
    print(f"Fusion Result: {result}")
