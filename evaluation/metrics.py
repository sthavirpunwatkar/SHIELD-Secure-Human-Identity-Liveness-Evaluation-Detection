import numpy as np

class FASMetrics:
    @staticmethod
    def calculate(y_true, y_pred_scores, threshold=0.5):
        """
        Calculates Anti-Spoofing Metrics.
        :param y_true: List of true labels (1 for Live, 0 for Spoof)
        :param y_pred_scores: List of predicted liveness scores (0 to 1)
        """
        y_true = np.array(y_true)
        y_pred_scores = np.array(y_pred_scores)
        y_pred = (y_pred_scores > threshold).astype(int)

        # True Positives, False Positives, True Negatives, False Negatives
        tp = np.sum((y_true == 1) & (y_pred == 1))
        tn = np.sum((y_true == 0) & (y_pred == 0))
        fp = np.sum((y_true == 0) & (y_pred == 1)) # Spoof classified as Live
        fn = np.sum((y_true == 1) & (y_pred == 0)) # Live classified as Spoof

        # APCER: Attack Presentation Classification Error Rate (False Acceptance Rate for spoofs)
        # BPCER: Bona Fide Presentation Classification Error Rate (False Rejection Rate for live)
        
        spoof_count = np.sum(y_true == 0)
        live_count = np.sum(y_true == 1)

        apcer = fp / spoof_count if spoof_count > 0 else 0
        bpcer = fn / live_count if live_count > 0 else 0
        acer = (apcer + bpcer) / 2

        accuracy = (tp + tn) / (live_count + spoof_count) if (live_count + spoof_count) > 0 else 0

        return {
            "accuracy": round(accuracy, 4),
            "apcer": round(apcer, 4),
            "bpcer": round(bpcer, 4),
            "acer": round(acer, 4),
            "tp": int(tp),
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn)
        }

class ChallengeMetrics:
    """Metrics specific to the Active Challenge-Response protocol.

    Operates on a list of per-session result dicts, each containing:
        * ``passed``  (bool)  – whether the session challenge was passed
        * ``response_time_ms`` (float) – response latency in milliseconds
        * ``is_attack`` (bool) – ground-truth label (True = attack, False = legit)
    """

    @staticmethod
    def calculate(challenge_results: list) -> dict:
        """Calculate challenge-specific evaluation metrics.

        :param challenge_results: List of dicts, each with keys
            ``passed`` (bool), ``response_time_ms`` (float),
            ``is_attack`` (bool).
        :return: Dictionary with the following metrics:

            * **challenge_pass_rate** (CPR) – fraction of legitimate
              users who passed the challenge.
            * **challenge_false_reject_rate** (CFRR) – fraction of
              legitimate users who *failed* the challenge (= 1 − CPR).
            * **attack_prevention_rate** (APR) – fraction of attack
              attempts that were correctly blocked (i.e. did **not**
              pass the challenge).
            * **mean_response_time_ms** (MRT) – arithmetic mean of
              ``response_time_ms`` across all results.
            * **median_response_time_ms** – median response time.
            * **total_samples** – total number of result dicts processed.
        """
        if not challenge_results:
            return {
                "challenge_pass_rate": 0.0,
                "challenge_false_reject_rate": 0.0,
                "attack_prevention_rate": 0.0,
                "mean_response_time_ms": 0.0,
                "median_response_time_ms": 0.0,
                "total_samples": 0,
            }

        legit = [r for r in challenge_results if not r["is_attack"]]
        attacks = [r for r in challenge_results if r["is_attack"]]

        # Challenge Pass Rate (CPR) — legit users who passed
        legit_passed = sum(1 for r in legit if r["passed"])
        cpr = legit_passed / len(legit) if legit else 0.0

        # Challenge False Reject Rate (CFRR) — legit users who failed
        cfrr = 1.0 - cpr

        # Attack Prevention Rate (APR) — attacks that did NOT pass
        attacks_blocked = sum(1 for r in attacks if not r["passed"])
        apr = attacks_blocked / len(attacks) if attacks else 0.0

        # Response-time statistics
        times = np.array([r["response_time_ms"] for r in challenge_results])
        mean_rt = float(np.mean(times))
        median_rt = float(np.median(times))

        return {
            "challenge_pass_rate": round(cpr, 4),
            "challenge_false_reject_rate": round(cfrr, 4),
            "attack_prevention_rate": round(apr, 4),
            "mean_response_time_ms": round(mean_rt, 2),
            "median_response_time_ms": round(median_rt, 2),
            "total_samples": len(challenge_results),
        }


if __name__ == "__main__":
    # FASMetrics test
    y_true = [1, 1, 0, 0, 0]
    y_scores = [0.9, 0.4, 0.1, 0.8, 0.2]
    print("FASMetrics:", FASMetrics.calculate(y_true, y_scores))

    # ChallengeMetrics test
    sample_results = [
        {"passed": True,  "response_time_ms": 450.0, "is_attack": False},
        {"passed": True,  "response_time_ms": 520.0, "is_attack": False},
        {"passed": False, "response_time_ms": 300.0, "is_attack": False},
        {"passed": False, "response_time_ms": 100.0, "is_attack": True},
        {"passed": True,  "response_time_ms":  80.0, "is_attack": True},
    ]
    print("ChallengeMetrics:", ChallengeMetrics.calculate(sample_results))
