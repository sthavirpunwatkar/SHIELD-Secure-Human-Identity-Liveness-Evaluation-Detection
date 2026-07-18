# PR-010 BENCHMARK PLAN

## 1. Objective
Design automated evaluation scripts to assess Anti-Spoof, rPPG, Behavior, and Fusion pipelines across standard datasets WITHOUT modifying production inference code.

## 2. Evaluation Scripts Architecture

### 2.1 Component Isolation
To evaluate components individually, we will construct a `BenchmarkingHarness` class that instantiates the inference modules (`AntispoofInference`, `RPPGDetector`, `BehavioralAnalyzer`, `FusionEngine`) in a standalone environment, feeding them standardized tensor data or frames extracted from datasets.

### 2.2 Anti-Spoof Benchmark
* **Execution:** Extract spatial face crops from dataset frames and pass them to `AntispoofInference.predict()`.
* **Target Datasets:** SiW, OULU-NPU, CASIA-FASD, Replay-Attack
* **Outputs:** Per-frame scores saved to a CSV mapped to ground truth labels.

### 2.3 rPPG Benchmark
* **Execution:** Stream video frames sequentially into `RPPGDetector.update()` to maintain the 150-frame temporal buffer.
* **Target Datasets:** UBFC-rPPG, PURE
* **Outputs:** Per-window (150-frame) confidence scores and FFT dominant frequencies mapped to ground truth signals.

### 2.4 Behavior Benchmark
* **Execution:** Run `BehavioralAnalyzer` on challenge-specific datasets or synthetic motion videos.
* **Target Datasets:** Custom internal motion sets, SiW protocol subsets.
* **Outputs:** Accuracy of blink detection and head pose bounds.

### 2.5 Fusion Benchmark
* **Execution:** Sweep through combinatorial fusion weights (e.g., `[0.1, 0.9]`, `[0.2, 0.8]`, etc.) using the raw outputs gathered from the isolated Anti-Spoof and rPPG benchmarks.
* **Outputs:** Heatmap of ROC AUCs and EERs across the weight distribution.

## 3. Statistical Generation
The benchmark scripts will automatically compute and plot:
1. **ROC (Receiver Operating Characteristic) Curve**
2. **PR (Precision-Recall) Curve**
3. **Confusion Matrix**
4. **Accuracy, Precision, Recall, F1**
5. **APCER (Attack Presentation Classification Error Rate)**
6. **BPCER (Bona Fide Presentation Classification Error Rate)**
7. **ACER (Average Classification Error Rate)**
8. **EER (Equal Error Rate)**
9. **AUC (Area Under Curve)**

*Implementation Detail:* We will utilize `sklearn.metrics` within `metrics.py` to handle threshold-agnostic calculations (ROC, AUC, EER) over the raw continuous output distributions.
