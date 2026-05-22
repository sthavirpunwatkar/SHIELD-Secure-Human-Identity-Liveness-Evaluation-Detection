import os
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate(metrics, output_path="reports/benchmark_report.md"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# SHIELD Benchmark Report
Generated: {timestamp}

## Summary Metrics
| Metric | Value |
| :--- | :--- |
| Total Samples | {metrics['total_samples']} |
| **Accuracy** | **{metrics['accuracy'] * 100:.2f}%** |
| APCER (Spoof Error) | {metrics['apcer'] * 100:.2f}% |
| BPCER (Live Error) | {metrics['bpcer'] * 100:.2f}% |
| **ACER** | **{metrics['acer'] * 100:.2f}%** |
| Inference Speed | {metrics['fps']} FPS |

## Confusion Matrix
- **True Positives (Live correctly identified):** {metrics['tp']}
- **True Negatives (Spoof correctly identified):** {metrics['tn']}
- **False Positives (Spoof identified as Live):** {metrics['fp']}
- **False Negatives (Live identified as Spoof):** {metrics['fn']}

## Conclusion
The current fusion model shows an ACER of {metrics['acer'] * 100:.2f}%. 
Target ACER for research-grade liveness is < 5%.
"""
        with open(output_path, 'w') as f:
            f.write(content)
        
        print(f"Report generated at {output_path}")

if __name__ == "__main__":
    dummy_metrics = {
        "total_samples": 100,
        "accuracy": 0.94,
        "apcer": 0.05,
        "bpcer": 0.07,
        "acer": 0.06,
        "tp": 43, "tn": 51, "fp": 3, "fn": 3,
        "fps": 15.5
    }
    ReportGenerator.generate(dummy_metrics)
