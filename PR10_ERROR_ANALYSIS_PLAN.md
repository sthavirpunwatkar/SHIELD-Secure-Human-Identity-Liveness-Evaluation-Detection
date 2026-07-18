# PR-010 ERROR ANALYSIS PLAN

## 1. Objective
To systematically categorize and quantify pipeline failures (False Lives and False Spoofs) across all benchmark datasets, establishing the root cause of misclassification without arbitrary conjecture.

## 2. Automated Tagging Logic
The error analysis script will ingest the benchmark results (ground truth vs. predicted) and automatically tag failures based on threshold breakdowns and dataset metadata.

### 2.1 Categorization Output
Every failed sample will be tagged with one or more of the following:
* **False Live:** Ground truth Spoof, predicted Live.
* **False Spoof:** Ground truth Live, predicted Spoof.

### 2.2 Root Cause Modality
* **AntiSpoof Failure:** Anti-Spoof score confidently predicted the wrong label (e.g., Spoof score > 0.8 for a Live target).
* **rPPG Failure:** rPPG score confidently predicted the wrong label (e.g., rPPG > 0.9 for a printed photo).
* **Fusion Failure:** Individual modalities were mixed/uncertain (e.g., rPPG=0.9, AntiSpoof=0.1) and the fixed fusion weights pushed the final score over/under the threshold incorrectly.

### 2.3 Environmental / Attack Modality (Metadata Extracted)
By referencing the dataset sub-directories and file attributes, we will automatically map the root cause to specific conditions:
* **Motion Blur / Pose:** Failure correlates with high dynamic movement (from PURE or SiW subsets).
* **Occlusion / Glasses:** Failure correlates with specific subject attributes (from CelebA-Spoof labels).
* **Lighting:** Failure correlates with low/adverse lighting conditions (from OULU-NPU).
* **Screen Replay:** Failure occurs exclusively on iPad/Mobile screen attacks (SiW protocol).
* **Printed Photo:** Failure occurs on paper cutouts.
* **3D/Silicone Mask:** Failure occurs on 3D masks.

### 2.4 Upstream Failures
* **Face Detection Failure:** No bounding box returned; pipeline aborted.
* **ROI Failure:** Insufficient spatial variance or tracking lost; signal flatlines.
* **Behavior Failure:** Landmarks not detected; unable to parse yaw/pitch.

## 3. Reporting Structure
The automated script will generate a consolidated JSON array of failed samples, grouped by root cause, and output an aggregate statistic table detailing which environmental factor contributes most to the BPCER and APCER.
