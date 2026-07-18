# SHIELD PR-010F: Benchmark Results Template

## 1. Context
- **Dataset Description**: 
- **Protocol**: 
- **Model**: 
- **Configuration**: (e.g., input size, batch size, threshold setting)

## 2. Evaluation Metrics
*Primary classification and error rate metrics.*

| Metric | Score | 
|---|---|
| **AUC** (Area Under Curve) | |
| **EER** (Equal Error Rate) | |
| **APCER** (Attack Presentation Classification Error Rate) | |
| **BPCER** (Bona Fide Presentation Classification Error Rate) | |
| **ACER** (Average Classification Error Rate) | |

## 3. Visualizations
- **ROC Curve**: [Insert relative link to ROC plot]
- **Confusion Matrix**: [Insert relative link to Confusion Matrix plot]

## 4. Qualitative Analysis
### 4.1 Failure Analysis
- *Identify the most common false acceptances (spoofs passing as live).*
- *Identify the most common false rejections (live rejected as spoof).*
- *Correlate failures with specific conditions (e.g., poor lighting, specific attack type).*

### 4.2 Success Cases
- *Identify scenarios where the model excels robustly against expectation.*

## 5. Runtime Statistics
- **Average Inference Latency (ms)**: 
- **Throughput (FPS)**: 
- **Peak GPU Memory Usage (MB)**: 
- **CPU Utilization (%)**: 

## 6. Conclusion
- *Summarize the performance.*
- *State explicitly whether the results justify passing this baseline evaluation or recommend further action per the Decision Policy.*
