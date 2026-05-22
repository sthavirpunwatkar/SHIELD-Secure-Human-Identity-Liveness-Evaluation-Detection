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

if __name__ == "__main__":
    # Test
    y_true = [1, 1, 0, 0, 0]
    y_scores = [0.9, 0.4, 0.1, 0.8, 0.2]
    print(FASMetrics.calculate(y_true, y_scores))
