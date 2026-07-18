# PR-010 METRICS SPECIFICATION

## 1. Overview
This specification defines the rigorous statistical metrics used to evaluate the SHIELD pipeline. All calculations will be performed on continuous float outputs before binarization, utilizing `scikit-learn` where applicable.

## 2. Core Metrics Definition

### 2.1 ISO/IEC 30107-3 Standard Metrics
* **APCER (Attack Presentation Classification Error Rate):**
  * *Definition:* Proportion of attack presentations incorrectly classified as bona fide (live).
  * *Formula:* `False Positives / Total Spoofs`
* **BPCER (Bona Fide Presentation Classification Error Rate):**
  * *Definition:* Proportion of bona fide presentations incorrectly classified as spoof.
  * *Formula:* `False Negatives / Total Lives`
* **ACER (Average Classification Error Rate):**
  * *Definition:* The arithmetic mean of APCER and BPCER.
  * *Formula:* `(APCER + BPCER) / 2`

### 2.2 Global Classification Metrics
* **Accuracy:** `(TP + TN) / (Total Samples)`
* **Precision:** `TP / (TP + FP)`
* **Recall (TPR):** `TP / (TP + FN)`
* **F1 Score:** `2 * (Precision * Recall) / (Precision + Recall)`

### 2.3 Threshold-Independent Metrics
* **ROC (Receiver Operating Characteristic) Curve:**
  * Plots True Positive Rate (TPR) against False Positive Rate (FPR) at various threshold settings.
* **AUC (Area Under Curve):**
  * Integral of the ROC curve. Quantifies overall capability to distinguish between classes.
* **EER (Equal Error Rate):**
  * The threshold value where the False Positive Rate (FPR) exactly equals the False Negative Rate (FNR). A lower EER indicates higher systemic accuracy.
* **PR (Precision-Recall) Curve:**
  * Evaluates performance particularly when datasets (Live vs. Spoof) are heavily imbalanced.

## 3. rPPG / Fusion Validation Specs
* **Histograms:** Distribution of raw scores across both modalities, allowing visual inspection of class separability.
* **Threshold Sweeps:** Iterating fusion weights from `(0.0, 1.0)` to `(1.0, 0.0)` in steps of `0.05`, generating an EER for each step to locate the empirical global optimum.
