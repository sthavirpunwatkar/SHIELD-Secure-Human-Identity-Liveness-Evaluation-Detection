class BenchmarkVisualization:
    @staticmethod
    def plot_roc_curve(fpr, tpr, auc_val, output_path):
        """
        Generates and saves an ROC curve.
        """
        pass

    @staticmethod
    def plot_pr_curve(precision, recall, output_path):
        """
        Generates and saves a Precision-Recall curve.
        """
        pass

    @staticmethod
    def plot_confidence_histograms(live_scores, spoof_scores, output_path):
        """
        Generates a histogram of confidence scores separated by ground truth.
        """
        pass

    @staticmethod
    def plot_confusion_matrix(cm_dict, output_path):
        """
        Generates a visual confusion matrix from a dictionary of TP, TN, FP, FN.
        """
        pass

    @staticmethod
    def plot_latency_histogram(latencies_ms, output_path):
        """
        Generates a histogram of inference latencies.
        """
        pass
