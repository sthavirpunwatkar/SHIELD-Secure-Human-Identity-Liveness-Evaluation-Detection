# PR-010 DATASET SURVEY

## 1. Presentation Attack (PA) Datasets

### 1.1 SiW (Spoof in the Wild)
* **License:** Academic (EULA required)
* **Download Source:** IEEE Xplore / Michigan State University (CVLab)
* **Protocol:** 3 protocols (1: sensor/attack variations, 2: cross-medium, 3: cross-PA)
* **Subjects:** 165
* **Attack Types:** Print, Replay (4 devices), Silicone Masks
* **Camera Specs:** 1080p high-resolution webcam
* **Lighting:** Various indoor and outdoor environments
* **Frame Rate:** 30 fps
* **Annotations:** Bounding boxes, live/spoof labels
* **Expected Preprocessing:** Standard face detection and cropping.

### 1.2 OULU-NPU
* **License:** Academic 
* **Download Source:** University of Oulu
* **Protocol:** 4 protocols (evaluate generalizability across sensors, illumination, and attacks)
* **Subjects:** 55
* **Attack Types:** Print (2 printers), Replay (2 screens)
* **Camera Specs:** 6 different mobile phone cameras
* **Lighting:** 3 illumination conditions
* **Frame Rate:** 30 fps, 1080p
* **Annotations:** Live/spoof labels
* **Expected Preprocessing:** Strict protocol requires zero overlap between training and testing sensors/attacks.

### 1.3 CASIA-FASD
* **License:** Academic
* **Download Source:** CASIA (Chinese Academy of Sciences)
* **Protocol:** Low, Normal, and High quality subgroups
* **Subjects:** 50
* **Attack Types:** Warped photo, Cut-out photo (mask), Video replay
* **Camera Specs:** USB webcams (3 qualities)
* **Lighting:** Controlled indoor
* **Frame Rate:** ~25-30 fps
* **Annotations:** Live/spoof labels
* **Expected Preprocessing:** Requires robust normalization due to varied camera resolutions.

### 1.4 Replay-Attack (Idiap)
* **License:** Academic (Idiap Research Institute)
* **Download Source:** Idiap website
* **Protocol:** Train/Dev/Test splits
* **Subjects:** 50
* **Attack Types:** Print, Mobile Replay, Tablet Replay
* **Camera Specs:** 320x240 resolution (MacBook webcam)
* **Lighting:** Controlled and adverse lighting
* **Frame Rate:** 25 fps
* **Annotations:** Bounding boxes, live/spoof labels
* **Expected Preprocessing:** Low resolution requires upscaling or specific spatial feature extraction.

### 1.5 MSU MFSD (Mobile Face Spoofing Database)
* **License:** Academic
* **Download Source:** Michigan State University
* **Protocol:** Cross-sensor evaluation
* **Subjects:** 35
* **Attack Types:** Printed photo, iPad replay, iPhone replay
* **Camera Specs:** Laptop webcam and Android mobile camera
* **Lighting:** Indoor
* **Frame Rate:** ~30 fps
* **Annotations:** Live/spoof labels
* **Expected Preprocessing:** Face cropping and alignment.

### 1.6 CelebA-Spoof
* **License:** Non-commercial research
* **Download Source:** GitHub / Baidu
* **Protocol:** Massive intra/inter-dataset protocols
* **Subjects:** 10,177
* **Attack Types:** 43 different attack types including 3D masks and deepfakes
* **Camera Specs:** Highly diverse (web-scraped and generated)
* **Lighting:** Unconstrained
* **Frame Rate:** N/A (Image based)
* **Annotations:** 40 attribute labels (illumination, spoof type, environment)
* **Expected Preprocessing:** Requires robust facial alignment due to extreme pose variations.

---

## 2. rPPG Datasets

### 2.1 UBFC-rPPG
* **License:** Academic
* **Download Source:** UBFC (Universite Bourgogne Franche-Comte)
* **Protocol:** Continuous evaluation (no fixed train/test split)
* **Subjects:** 42
* **Attack Types:** N/A (Live only)
* **Camera Specs:** Logitech C920 HD Pro (uncompressed)
* **Lighting:** Natural/indoor mix
* **Frame Rate:** 30 fps
* **Annotations:** Ground truth BVP (Blood Volume Pulse), heart rate, SpO2 (CMS50E pulse oximeter)
* **Expected Preprocessing:** Detrending, bandpass filtering, precise ROI tracking over time.

### 2.2 PURE (Pulse Rate from Face Videos)
* **License:** Academic
* **Download Source:** Technical University of Munich
* **Protocol:** Setup evaluation (6 different motion/lighting tasks per subject)
* **Subjects:** 10 (60 videos total)
* **Attack Types:** N/A (Live only)
* **Camera Specs:** eco274CVGE RGB camera (uncompressed)
* **Lighting:** Controlled indoor
* **Frame Rate:** 30 Hz (and 60Hz)
* **Annotations:** Ground truth BVP and heart rate
* **Expected Preprocessing:** Advanced ROI tracking required due to heavy motion tasks (e.g., talking, head rotation).

### 2.3 COHFACE
* **License:** Academic (Idiap)
* **Download Source:** Idiap Research Institute
* **Protocol:** Train/Test splits
* **Subjects:** 40 (160 videos)
* **Attack Types:** N/A (Live only)
* **Camera Specs:** Logitech HD webcam
* **Lighting:** Controlled and natural
* **Frame Rate:** 20 fps
* **Annotations:** BVP, heart rate, respiration
* **Expected Preprocessing:** Compressed video requires handling of spatial/temporal artifacts. Bandpass filters must adapt to 20 fps sampling frequency.

### 2.4 MMSE-HR
* **License:** Academic (Binghamton University)
* **Download Source:** BP4D+ extension
* **Protocol:** Continuous evaluation
* **Subjects:** 40
* **Attack Types:** N/A (Live only)
* **Camera Specs:** 2D and 3D sensors
* **Lighting:** Controlled indoor
* **Frame Rate:** 25 fps
* **Annotations:** Blood pressure, heart rate, respiration, facial expressions
* **Expected Preprocessing:** Requires handling of emotion-induced facial distortions affecting the ROI.
