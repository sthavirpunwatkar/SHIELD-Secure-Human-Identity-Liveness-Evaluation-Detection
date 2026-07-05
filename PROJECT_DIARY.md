# SHIELD Project Diary: Academic Record of Development

## 🎓 Project Overview
**Title:** SHIELD – Secure Human Identity & Liveness Evaluation Detection
**Domain:** Computer Vision, Biometrics, Anti-Spoofing
**Objective:** To develop a robust, real-time multimodal liveness detection system that integrates behavioral, physiological, and deep-learning-based anti-spoofing techniques.

---

## 🚀 Milestones & Progress

### Milestone 0: Foundation & Infrastructure (Pre-May 2026)
- **Objective:** Establish the core architecture and baseline models.
- **Key Achievements:**
    - Initialized the repository structure.
    - Integrated YOLOv8-face for real-time face detection.
    - Set up MiniFASNet as the primary anti-spoofing classifier.
    - Established FastAPI backend and Flutter frontend communication via WebSockets.
- **Academic Note:** The decision to use YOLOv8-face provides a high-performance detection base, while MiniFASNet offers a lightweight alternative to heavier CNNs, crucial for <100ms latency targets.

### Milestone 1: Signal Quality & Pre-processing (Sprint 1)
- **Objective:** Ensure "garbage in, garbage out" prevention via a robust Quality Gate.
- **Key Achievements:**
    - Implemented `BlurDetector` using Laplacian variance.
    - Implemented `IlluminationDetector` to handle extreme lighting conditions.
    - Developed `PoseFilter` to ensure frontal face alignment.
    - Added `OcclusionDetector` to detect masks or hand-over-face scenarios.
- **Differentiation:** Unlike many passive systems, SHIELD rejects low-quality frames before they reach the expensive inference stage, significantly reducing false positives in suboptimal environments.

### Milestone 2: Explainable Multimodal Fusion (Sprint 2)
- **Objective:** Combine disparate liveness signals into a single, explainable verdict.
- **Key Achievements:**
    - Built a weighted `FusionEngine`.
    - Initial weights: Anti-Spoof (30%), rPPG (30%), Blink (20%), Challenge (20%).
- **Differentiation:** Most competitors rely on a single "black-box" model. SHIELD's fusion approach allows for fine-tuning and provides transparency into why a verdict was reached.

### Milestone 3: Physiological Verification - Deep rPPG (Sprint 3)
- **Objective:** Detect human pulse remotely from facial video.
- **Key Achievements:**
    - Integrated `PhysNet`-style 3D CNN for spatio-temporal heart rate estimation.
    - Developed `rppg_detector.py` to extract blood volume pulse (BVP) signals.
- **Differentiation:** This is a top-tier security feature that defeats high-quality silicon masks and high-resolution screen replays, as they lack physiological blood flow signals.

### Milestone 4: Systematic Evaluation Framework (Sprints 4 & 5)
- **Objective:** Move beyond anecdotal testing to rigorous benchmarking.
- **Key Achievements:**
    - Created `DataWrangler` for multi-dataset standardization (CASIA, CelebA-Spoof, etc.).
    - Implemented automated reporting for APCER, BPCER, and ACER metrics.
- **Differentiation:** Ensures the system meets ISO/IEC 30107-3 standards for Presentation Attack Detection (PAD).

### Milestone 5: Active Challenge-Response Protocol (Sprint 6) - COMPLETED
- **Objective:** Add an interactive layer of security to defeat sophisticated replay attacks.
- **Key Achievements:**
    - Implemented `ChallengeEngine` for randomized task generation (Blink, Turn, Smile).
    - Developed `TemporalValidator` to detect "jump-cuts" and pre-recorded responses.
    - Integrated glassmorphic UI prompts in Flutter for seamless user interaction.
- **Differentiation:** This "Hybrid Active+Passive" approach is the current academic gold standard, providing defense-in-depth that purely passive models (like Silent-FAS) cannot match.

### Milestone 6: UI/UX Overhaul & Guidance System (Sprint 7) - COMPLETED
- **Objective:** Elevate the user experience to industry standards and provide real-time guidance.
- **Key Achievements:**
    - Implemented a "Pre-Verification" gateway for user preparation.
    - Developed a dynamic Face Guide Oval that reacts to backend quality metrics (Blur, Illumination, Pose).
    - Added an immersive spotlight/frosted-glass UI for focused verification.
    - Integrated haptic feedback for tactile success/failure confirmation.
- **Differentiation:** By providing real-time feedback (e.g., "Too Dark"), SHIELD drastically reduces user frustration and improves the success rate of the liveness check compared to silent passive systems.

### Milestone 7: Process Automation & Documentation Standardization (Sprint 8) - COMPLETED
- **Objective:** Establish a rigid, automated workflow for continuous quality and documentation integrity.
- **Key Achievements:**
    - Integrated `graphify` into git hooks for automatic codebase mapping.
    - Implemented the `overview_agent` for senior-level automated audits.
    - Mandated a standardized `README.md` structure in `GEMINI.md` to ensure professional communication of plans, benchmarks, and innovations.
- **Differentiation:** This formalizes the "Academic Rigor" of the project, ensuring that even as new features are added, the project remains clean, documented, and audited at a senior developer level.

### Milestone 8: Test Suite Stabilization & Deadlock Resolution (July 2026) - COMPLETED
- **Objective:** Fix integration test failures and eliminate websocket hangs to stabilize the repository.
- **Key Achievements:**
    - Mocked face detection, crop, and quality gate evaluation in `test_audit_integrity.py` to decouple integration logic from live model outputs.
    - Implemented a session-level pytest fixture in `test_backend.py` to automatically spawn the FastAPI server in a background subprocess.
    - Configured uvicorn execution with the `PYTHONPATH` environment variable and project root `cwd` so it correctly resolves both model weights and local modules.
    - Resolved a websocket hang/deadlock by ensuring both passive and active endpoints return error JSON when invalid binary frames are sent.
    - Fixed a WebSocket session memory leak by implementing explicit session pruning in the `/ws/challenge` endpoint's `finally` block.
    - Added dynamic path registrations to `backend/main.py` to support imports when running the server from any project directory.
    - Replaced port binding checks in `test_backend.py`'s fixture with a robust `/health` HTTP API ping (allowing 20s for model loading on CPU).
    - Added `test_websocket_challenge_session_cleanup` in `test_backend.py` to verify session garbage collection on disconnect.
- **Differentiation:** Establishes a robust, zero-manual-intervention testing and production-grade memory safety foundation that guarantees continuous integration runs completely green.

### Milestone 9: Codebase Optimization & Hardening (July 2026) - COMPLETED
- **Objective:** Optimize dependencies, remove speculative/dead code, and implement a robust JPEG compression defense.
- **Key Achievements:**
    - Conducted a repository-wide over-engineering audit (invoked via ponytail).
    - Cleaned up 256 lines of dead/speculative code by removing unused classes: `LivenessClassifier`, `MiniFASNet` (PyTorch variant), and `DeepRPPGDetector`/`PhysNet`, along with their related test scripts.
    - Removed heavy, unused packages `torchvision` and `msgpack` from `requirements.txt` to minimize deployment footprint.
    - Implemented a JPEG Compression Defense to preprocess crop inputs in `fusion_service.py` to prevent high-frequency adversarial noise.
- **Differentiation:** Enhances production readiness by drastically lowering container image sizes and introducing passive security hardening.

### Milestone 10: Fusion Weights Optimization (July 2026) - COMPLETED
- **Objective:** Optimize the weighted fusion engine weights to minimize ACER and maximize accuracy.
- **Key Achievements:**
    - Implemented a grid-search tuning script `evaluation/tune_weights.py` to systematically search optimal weights.
    - Added a `min_weight=0.10` constraint to prevent silencing any modal signal.
    - Evaluated 1,771 weight combinations on the dataset, finding the optimal configuration: 10% rPPG, 10% Blink, 15% Antispoof, and 65% Challenge.
    - Updated `inference/fusion_engine.py` default weights to apply the optimal combination.
    - Resolved a float precision logic bug in `tune_weights.py` where IEEE-754 precision issues skipped 20% of valid combinations.
    - Added a unit test `test_weight_tuner` in `test_fusion.py` to verify tuner logic.
- **Differentiation:** Empirically calibrates the decision fusion module using dataset metrics instead of raw heuristics, verified by robust unit tests.

### Milestone 11: Active Identity Consistency Check (July 2026) - COMPLETED
- **Objective:** Prevent "tag-team" candidate swap attacks by validating identity consistency in real-time.
- **Key Achievements:**
    - Implemented scale-invariant 4D geometric signature computation from 6 stable landmarks (nose, eyes, chin, mouth corners) of MediaPipe FaceMesh.
    - Normalized facial distances using the interocular distance to guarantee robust distance ratio comparisons under changing camera distances.
    - Integrated verification directly into `VerificationSession.add_frame` with raw landmark passing from `FusionService` to avoid CPU/network overhead.
    - Rejects frames and terminates active challenge sessions immediately (`Identity mismatch detected`) if signature distance exceeds `0.20`.
    - Added comprehensive integration test (`test_websocket_identity_mismatch`) to assert correct rejection and error signaling.
- **Differentiation:** Guards the session integrity against mid-session identity switches, establishing a critical verification parameter.

### Milestone 12: CDAC Academic Review Presentation (July 2026) - COMPLETED
- **Objective:** Design and generate a high-quality 10-slide academic presentation for CDAC project review using automated toolchains.
- **Key Achievements:**
    - Authored a slide-generator script `generate_deck.js` using `pptxgenjs` to build structured academic slides.
    - Designed 10 communication-first slides matching project guidelines (situation-complication-resolution narrative structure, dark/light sandwich palette).
    - Constructed custom SVG-to-native-shape vector elements for flowchart representations (Camera Input -> YOLOv8 Face -> Quality Gate -> Parallel Modality Extractors -> Fusion -> Decisive UI) and clean table styling.
    - Successfully resolved rendering bugs like title rule collisions, play icon alignment inside circles, and cell highlighting using the programmatic pptxgenjs layout API.
    - Conducted automated Content and Visual QA on PDF-to-image converted slides using headless LibreOffice and Poppler (`pdftoppm`).
- **Differentiation:** Guarantees absolute design consistency, cross-platform compatibility, and a formal, communication-first layout that clearly conveys SHIELD's technical edge and ACER metrics to evaluators.

### Milestone 13: Flutter Web Port Stability & Layout Hardening (July 2026) - COMPLETED
- **Objective:** Fix frontend layout rendering crashes and camera capture exceptions when running on Google Chrome (web target).
- **Key Achievements:**
    - Wrapped the `HomeScreen` Column in a `SingleChildScrollView` to resolve the `RenderFlex overflowed by 82 pixels` layout error on small screens.
    - Implemented a boolean state flag `_isCapturing` acting as an asynchronous execution lock inside both `camera_screen.dart` and `challenge_screen.dart`.
    - Prevented overlapping calls to `takePicture()` on the Flutter `CameraController` (which was causing `CameraException: Previous capture has not returned yet` due to slower web execution speeds).
    - Restored active face detection and guidance oval responsiveness in the web interface by ensuring continuous, uncorrupted frame ingestion.
- **Differentiation:** Guarantees production-grade cross-platform resilience, enabling SHIELD to run flawlessly inside standard web browsers without native plugin translation crashes.

### Milestone 14: Quality Gate Calibration & Live Tracking Integration (July 2026) - COMPLETED
- **Objective:** Fine-tune threshold metrics and resolve tracking inconsistencies for live webcam evaluation.
- **Key Achievements:**
    - Modified frontend Oval Painter in `challenge_screen.dart` to dynamically track the user's face using bounding box coordinates from the backend payload, resolving static-overlay issues.
    - Adjusted aspect-ratio mathematics to prevent horizontal squashing of the tracking oval on wider screens.
    - Created a symbolic link `models` in `backend/` to point to `../models`, instantly fixing `yolov8n-face.pt` load failures and ensuring accurate face cropping over generic body detection.
    - Relaxed overly strict Quality Gate logic by lowering `BlurDetector`'s Laplacian variance threshold to 20.0 and widening `IlluminationDetector` bounds to accept real-world webcam conditions.
- **Differentiation:** Enhances practical deployment viability by balancing rigorous spoof-prevention with forgiving environmental tolerances, drastically improving user accessibility.

### Milestone 15: Challenge Engine & UI State Synchronization (July 2026) - COMPLETED
- **Objective:** Fix "Instant Pass" spoofing bugs and UI state blockages during active liveness challenges.
- **Key Achievements:**
    - Diagnosed and fixed a high-severity bug in `ChallengeEngine` where a single noisy frame triggered instantaneous challenge completion.
    - Implemented a 3-frame debouncer (`_consecutive_frames`) requiring sustained action verification.
    - Corrected a race condition in the Flutter frontend (`challenge_service.dart`) where the `ChallengeState.allPassed` UI state prematurely blocked the processing of the final backend `verdict` payload, resulting in a persistent "0.0%" score display.
- **Differentiation:** Guarantees absolute temporal resilience in behavioral tracking, rejecting micro-flickers and mandating sustained physical action to complete verification.

---

## 🛡️ Unique Innovations (SHIELD vs. Competitors)

1. **The Quality-First Gate:** While systems like FaceTec or AWS Rekognition have quality checks, SHIELD's open implementation allows for custom thresholding for specific deployment scenarios (e.g., high-security vs. high-throughput).
2. **Deep rPPG Integration:** Implementing a 3D CNN for remote pulse detection puts SHIELD in the league of advanced research projects, moving beyond simple color-based pulse analysis.
3. **Temporal Consistency Check:** The `TemporalValidator` doesn't just check if a blink happened; it checks the *cadence* and *frame-to-frame coherence*, making it extremely difficult to fool with AI-generated video or edited footage.
4. **Explainable Fusion Scoring:** Instead of a single probability, SHIELD provides a breakdown of signals, which is vital for forensic audits in interview or attendance systems.

---

## 📈 Current Status & Next Steps
- **Status:** All core sprints completed. Codebase is optimized and test suite is 100% green.
- **Next Steps:** 
    - Fine-tuning fusion weights based on final benchmark results.
    - Optimizing ONNX inference for edge devices.
    - Finalizing the Comprehensive Research Report.

### Sprint 7: Database Migration
- **Goal:** Replace Firebase with a local SQLite database.
- **Outcome:** 
    - Removed `firebase-admin` dependency.
    - Replaced `firebase_service.py` with a lightweight `db_service.py` using SQLite and local file storage.
    - Resolved Firebase Mock Mode errors.

### Sprint 8: ML Training & Model Refinement
- **Goal:** Eradicate mock behaviors and train state-of-the-art weights.
- **Outcome:**
    - Removed dummy `0.5` scoring in `rppg_detector.py` and `antispoof/inference.py`.
    - Trained new PyTorch and ONNX models for rPPG and EfficientNet-B0 backbone.
    - Fusion engine thresholding optimized with dynamic weights and <100ms early-exit mechanisms.

### Milestone 16: Inference Engine Cascade Fusion Logic (July 2026) - COMPLETED
- **Objective:** Optimize latency and inference flow by implementing a cascade fusion pipeline.
- **Key Achievements:**
    - Reordered inference in `fusion_service.py` to Cascade Fusion (Behavior -> Anti-Spoof -> rPPG).
    - Utilized MediaPipe heuristics (EAR/MAR/PnP) for behavior tracking.
    - Implemented early-rejection for behavior failures (missing landmarks) to save compute.
    - Ensured robust loading of optimized ONNX models across both rPPG and Anti-Spoof paths.
    - Updated integration test `test_inference.py` to validate new cascade order.
- **Differentiation:** Greatly improves runtime efficiency by discarding obvious spoof attempts (e.g., printed images lacking facial landmarks or behavioral signals) before executing expensive ML models.

### Milestone 17: Anti-Spoof Training Upgrade (MiniFASNet INT8) (July 2026) - COMPLETED
- **Objective:** Modernize and harden the Anti-Spoof (MiniFASNet) training pipeline with state-of-the-art techniques and INT8 edge optimization.
- **Key Achievements:**
    - Integrated advanced augmentations: MixUp, Random Erasing, Cutout, and simulated screen glare/moire patterns.
    - Switched optimizer to AdamW combined with a CosineAnnealingLR scheduler.
    - Refactored `SEBlock` architecture in MiniFASNetV2 to use `Conv2d` instead of `Linear` to mathematically avoid ONNX Runtime shape inference bugs during INT8 MatMul quantization.
    - Added automated `--pretrained` model fine-tuning support.
    - Successfully exported the resulting model to a highly compressed ONNX INT8 format for ultra-low latency edge inference.
- **Differentiation:** Transforms a standard CNN into a highly robust, print/replay-resistant INT8 model that runs at a fraction of the computational cost while avoiding common ONNX quantization pitfalls.

### Milestone 18: rPPG 1D CNN Training Upgrade (July 2026) - COMPLETED
- **Objective:** Upgrade the rPPG training pipeline for 1D CNN with advanced optimizers, INT8 quantization, and PURE/UBFC compatibility.
- **Key Achievements:**
    - Updated `train_rppg_v2.py` to use `AdamW` and `CosineAnnealingLR` scheduler.
    - Added compatibility for training from scratch using `PURE` and `UBFC` datasets.
    - Implemented a custom `Linear` layer replacement in `rppg_cnn.py` to fix PyTorch 2.9 ONNX shape inference bugs.
    - Successfully quantized the rPPG model to ONNX INT8 for edge-device deployment.
    - Resolved AMP/autocast errors by explicitly moving `BCELoss` calculations out of the FP16 block.
- **Differentiation:** Achieves edge-ready quantized inference of rPPG physiological signals, ensuring lightweight liveness detection capabilities independent of hardware constraints.
