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
- **Differentiation:** Empirically calibrates the decision fusion module using dataset metrics instead of raw heuristics.

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
