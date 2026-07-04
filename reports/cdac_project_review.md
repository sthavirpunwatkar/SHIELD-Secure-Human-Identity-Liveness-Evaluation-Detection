# 🛡️ SHIELD - CDAC Project Review Slide Deck (McKinsey Action Theme)

This document serves as a slide-by-slide text guide and backup for the generated PowerPoint presentation `reports/cdac_project_review.pptx`.

---

## Slide 1: Title & Problem Formulation (SCR Cover Slide)

### Slide Content
*   **Project Title:** SHIELD
*   **Sub-title:** Multimodal Real-Time Biometric Liveness & Identity Verification
*   **Project Metadata:**
    *   **Project Partners:** Sthavir Sunil Punwatkar, [Project Partner 2]
    *   **Project Guide:** [Project Guide Name]
    *   **Context:** CDAC Project Review  |  Domain: Biometrics & Computer Vision
*   **SITUATION & COMPLICATION (SCR Overlay Card):**
    *   **Situation:** Remote high-stakes evaluations (exams, interviews) rely on standard 2D webcams for candidate authentication.
    *   **Complication:** Traditional facial recognition is bypassed by presentation attacks (printed photos, video replay screens) and mid-session identity swapping.
    *   **Resolution:** SHIELD introduces a unified real-time framework integrating facial texture patterns, physiological cardiac pulse (rPPG), and active behavioral challenges.
*   **Right Side Illustration:** Holographic cyber shield visual framed on the right.

---

## Slide 2: Objectives (Target Resolution Matrix)

### Slide Content
*   **Action Title:** Objectives: Establishing a Standard-Compliant, Low-Latency Defense for Remote Identity Verification
*   **🎯 Core Objectives:**
    *   Develop an end-to-end, real-time liveness pipeline processing multi-layered verification streams in <100ms.
    *   Implement non-intrusive biological checks by extracting blood volume pulse (BVP) from standard RGB video feeds (rPPG).
    *   Introduce randomized active challenge-response tasks combined with frame validation to counter pre-recorded replays.
    *   Construct an explainable multi-modal decision fusion engine to facilitate detailed audit trails.
*   **⚙️ Engineering Targets & KPIs:**
    *   **ISO/IEC 30107-3 Standard Adherence:** Deliver an ACER (Average Classification Error Rate) under 1.5% to verify enterprise-level security.
    *   **Edge-Deployable Performance:** Optimize inference workloads to support execution in under 100ms on consumer-grade CPUs.
    *   **Zero-Dependency RGB Deployment:** Perform biological, texture, and active checks using simple 2D webcams without dedicated sensors.

---

## Slide 3: Architecture (Data-Driven Pipeline)

### Slide Content
*   **Action Title:** Architecture: Multi-Tiered Verification Processing Raw Webcam Frames to Final Score Fusion
*   **⚙️ PIPELINE DATA FLOWCHART:**
    *   Visual architecture modeled as a neural block diagram, showing data routing through the processing steps:
        1.  **Video Frames (BGR stream)** (Pink input card)
        2.  ➔ *Connects to:* **YOLOv8-Face Detection** (Orange processing card)
        3.  ➔ *Connects to:* **Signal Quality Filter Gate** (Yellow quality verification card)
        4.  ➔ *Splits into Parallel Inference block (3x layer stack):*
            *   **Passive Texture CNN** (Teal card)
            *   **Physiological rPPG** (Teal card)
            *   **Active Challenges** (Teal card)
        5.  ➔ *Converges to:* **Weighted Decision Fusion** (Yellow fusion card)
        6.  ➔ *Connects to:* **Linear Decision Threshold** (Purple linear classifier card)
        7.  ➔ *Connects to:* **Output Verdict (Live/Spoof)** (Green softmax card)

---

## Slide 4: Defense Pillars (Multimodal Mechanisms)

### Slide Content
*   **Action Title:** Defense Pillars: Combining Spatial Textures, Cardiac Physiology, and Active Directives
*   **Four Pillars Details:**
    1.  **Passive Texture:** MiniFASNet CNN classification parsing high-frequency surface patterns to detect print paper/screen structures.
    2.  **Physiological rPPG:** 3D spatio-temporal CNN extracting cardiac micro-signals from skin color shifts to verify living tissue.
    3.  **Active Challenges:** Randomized directives (Blink, Turn, Smile) validated dynamically to establish immediate user cooperation.
    4.  **Temporal Validator:** Time-series integrity checking to trace jump-cuts and confirm time sync between challenge events.

---

## Slide 5: Results & Performance Evaluation

### Slide Content
*   **Action Title:** Results: SHIELD Exceeds Enterprise Standards with 1.0% ACER at 85ms Latency
*   **Metrics Comparison Table:**

| Metric Parameter | SHIELD Score |
| :--- | :--- |
| **APCER (Attack Error Rate)** | **1.2%** |
| **BPCER (Bona Fide Error Rate)** | **0.8%** |
| **ACER (Average Error Rate)** | **1.0%** |
| **End-to-End Inference Latency** | **85 ms** |

*   **📊 ISO/IEC 30107-3 Standard Metrics & Setup:**
    *   **APCER:** Attack Presentation Classification Error Rate. Measures the % of spoof attacks incorrectly classified as live.
    *   **BPCER:** Bona Fide Presentation Classification Error Rate. Measures the % of genuine live users incorrectly flagged as spoofs.
    *   **ACER:** Average Classification Error Rate. Calculated as the average of APCER and BPCER: ACER = (APCER + BPCER) / 2.
    *   **Calibration:** Evaluated on CASIA-FASD and CelebA-Spoof (10,000+ frames). System weights tuned via 1,771 test combinations under min_weight=0.10 constraint to achieve 1.0% ACER.
*   **Right Side Illustration:** Speedometer telemetry dashboard visual.

---

## Slide 6: Novelty & Key Contributions

### Slide Content
*   **Action Title:** Novelty: Scale-Invariant Identity Landmark Trajectories Prevent Mid-Session Swapping
*   **Three Key Novelties:**
    1.  **Real-Time Scale-Invariant Identity Consistency Check:**
        Defeats mid-session candidate swapping (tag-team fraud):
        *   Computes scale-invariant 4D geometric signature ratios (nose, eyes, chin, lip corners) using MediaPipe FaceMesh landmarks.
        *   Signature distance is verified frame-by-frame. Websocket is killed immediately if signature drift exceeds threshold (>0.20).
    2.  **JPEG Compression Defenses:**
        Enhances resilience against adversarial spatial noise attacks:
        *   Integrates compression filters into the face crop step to cancel out artificial noise patterns generated by digital camera overlays.
    3.  **System Grid Search Optimization:**
        *   Evaluated 1,771 separate sensor weight parameter combinations mathematically to eliminate sub-model silence.
*   **Right Side Illustration:** 3D face mesh wireframe visual.

---

## Slide 7: Deployment & UI Operations

### Slide Content
*   **Action Title:** Deployment: Flutter Dashboard and WebSocket Ingestion Enable Seamless Live Audit Trails
*   **📱 Interactive Flutter Telemetry Dashboard:**
    *   **Quality Telemetry Guide:** Interactive oval frame changing colors dynamically based on real-time quality parameters (Blur, Exposure, Pose).
    *   **Explainable Biometrics:** Displays clear confidence breakdowns for texture, biological rPPG, and active challenge scores in real-time.
    *   **Secure Ingestion Gateway:** Informs user of capture instructions prior to starting high-stakes verification flows.
*   **🎥 Live Demonstration Protocol:**
    Websocket-based real-time capture and verification pipeline:
    *   *Active Verification:* Core session starts, requesting random user movements.
    *   *Print Spoof Defense:* User presents photo print, system immediately blocks frame based on texture and heart-rate checks.
    *   *Replay Loop Defense:* Dynamic challenge mismatch catches loop playbacks.
    *   *Identity Swap Defense:* Mid-session candidate swap triggers geometric landmark signature mismatch, killing the connection instantly.
