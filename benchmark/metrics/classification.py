import numpy as np

class BenchmarkMetrics:
    @staticmethod
    def calculate_classification_metrics(y_true, y_pred, y_scores, threshold=0.5):
        """
        y_true: Array-like of ground truth (1 for Live, 0 for Spoof)
        y_pred: Array-like of binary predictions (1 for Live, 0 for Spoof)
        y_scores: Array-like of confidence scores [0.0, 1.0]
        """
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        y_scores = np.array(y_scores)
        
        tp = np.sum((y_true == 1) & (y_pred == 1))
        tn = np.sum((y_true == 0) & (y_pred == 0))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))
        
        total_lives = np.sum(y_true == 1)
        total_spoofs = np.sum(y_true == 0)
        total = total_lives + total_spoofs
        
        accuracy = (tp + tn) / total if total > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        apcer = fp / total_spoofs if total_spoofs > 0 else 0
        bpcer = fn / total_lives if total_lives > 0 else 0
        acer = (apcer + bpcer) / 2
        
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0

        # EER, AUC, ROC handling requires scikit-learn
        eer = 0.0
        auc_val = 0.0
        try:
            from sklearn.metrics import roc_curve, auc
            fpr_vals, tpr_vals, _ = roc_curve(y_true, y_scores)
            auc_val = auc(fpr_vals, tpr_vals)
            fnr_vals = 1 - tpr_vals
            eer_idx = np.nanargmin(np.absolute((fnr_vals - fpr_vals)))
            eer = fpr_vals[eer_idx]
        except ImportError:
            pass
            
        return {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "apcer": float(apcer),
            "bpcer": float(bpcer),
            "acer": float(acer),
            "fpr": float(fpr),
            "fnr": float(fnr),
            "eer": float(eer),
            "auc": float(auc_val),
            "confusion_matrix": {
                "tp": int(tp),
                "tn": int(tn),
                "fp": int(fp),
                "fn": int(fn)
            }
        }
