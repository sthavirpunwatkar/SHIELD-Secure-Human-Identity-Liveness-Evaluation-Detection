# Graph Report - SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection  (2026-06-14)

## Corpus Check
- 108 files · ~26,920,084 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 996 nodes · 1407 edges · 87 communities (76 shown, 11 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 132 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6daef497`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 86|Community 86]]

## God Nodes (most connected - your core abstractions)
1. `ChallengeSession` - 43 edges
2. `TemporalValidator` - 32 edges
3. `SessionManager` - 30 edges
4. `VerificationSession` - 26 edges
5. `BehavioralAnalyzer` - 23 edges
6. `ChallengeType` - 23 edges
7. `RPPGDetector` - 20 edges
8. `FASDataset` - 18 edges
9. `EfficientNetFAS` - 17 edges
10. `QualityScoreEngine` - 16 edges

## Surprising Connections (you probably didn't know these)
- `UploadFile` --uses--> `SessionManager`  [INFERRED]
  backend/main.py → inference/session_manager.py
- `WebSocket` --uses--> `SessionManager`  [INFERRED]
  backend/main.py → inference/session_manager.py
- `FusionService` --uses--> `BehavioralAnalyzer`  [INFERRED]
  backend/services/fusion_service.py → inference/behavioral_analyzer.py
- `FusionService` --uses--> `ChallengeSession`  [INFERRED]
  backend/services/fusion_service.py → inference/challenge_engine.py
- `FusionService` --uses--> `FusionEngine`  [INFERRED]
  backend/services/fusion_service.py → inference/fusion_engine.py

## Import Cycles
- None detected.

## Communities (87 total, 11 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (34): RegisterPlugins(), HWND, LPARAM, LRESULT, UINT, wchar_t, WPARAM, PluginRegistry (+26 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (39): A1. Create `inference/challenge_engine.py` — The Brain, A2. Upgrade `inference/behavioral_analyzer.py` — Real Detection, A3. Upgrade `backend/services/fusion_service.py` — Session-Aware Processing, A4. Upgrade `backend/main.py` — Protocol Messages, Architecture Design, B1. Create `frontend/lib/services/challenge_service.dart`, B2. Create `frontend/lib/widgets/challenge_prompt.dart`, B3. Create `frontend/lib/screens/challenge_screen.dart` (+31 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (36): double?, int?, action, bbox, behavioralScore, blurScore, brightness, challengeIndex (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (35): Animation, AnimationController, CustomPainter, package:flutter/services.dart, _FaceGuideOvalPainter, TickerProviderStateMixin, build, _buildActiveCard (+27 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (27): build_rppg_model_v2(), count_parameters(), FrequencyBranch, get_model(), Upgraded 1D-CNN + FFT Dual-Branch rPPG Model  Architecture:   Branch A (Temporal, x: (B, 1, window_size), Factory helper — mirrors legacy build_rppg_model signature., 1D Conv stack for temporal signal processing. (+19 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (17): BlurDetector, Detects if the face crop is blurry.         :param face_crop: OpenCV image (BGR), Initializes the Blur Detector using Variance of Laplacian.         :param thresh, IlluminationDetector, Detects if the illumination is 'good', 'underexposed', or 'overexposed'., Initializes the Illumination Detector.         :param low_threshold: Minimum mea, OcclusionDetector, Detects if the face is occluded.         :param face_crop: OpenCV image (BGR). (+9 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (28): ChallengeState, double get, int get, _challengeScore, ChallengeService, ChallengeState, _countdownTimer, _currentAction (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (14): BenchmarkEngine, BehavioralAnalyzer, Convert a normalized MediaPipe landmark to pixel coordinates., Convert a normalized MediaPipe landmark to pixel coordinates (2D for solvePnP)., Euclidean distance between two 2D points., Computes the Eye Aspect Ratio (EAR) for a single eye.          EAR = (||p2 - p6|, Detects if a blink is occurring using EAR on both eyes.          A blink is dete, Detects if the mouth is open using MAR (Mouth Aspect Ratio).          MAR = vert (+6 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (22): FlPluginRegistry, fl_register_plugins(), FlView, GApplication, gboolean, gchar, GObject, GtkApplication (+14 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (12): FaceDetector, Detects faces in a given frame.         :param frame: OpenCV image (BGR)., Crops a face from the frame based on a bounding box.         :param frame: OpenC, Initializes the YOLOv8 face detector.         :param model_path: Path to the YOL, LivenessClassifier, Predicts if the face crop is Live or Spoof.         :param face_crop: OpenCV ima, Initializes the EfficientNet-B0 liveness classifier.         :param model_path:, FusionService (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.11
Nodes (10): DataWrangler, Processes a dataset (video or image based).         :param source_dir: Path to r, Initializes the Data Wrangler.         :param output_base: Where to store standa, DateTime?, ReportGenerator, FirebaseService, Logs verification metadata to Firestore., Uploads a verification snapshot to Firebase Storage. (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.11
Nodes (15): _build_v1_model(), Module, ndarray, inference/rppg_detector.py =========================== Real-time rPPG liveness d, Try each (path, variant) candidate in order.  Return the first that         load, Return the architecture matching *variant*., Extract the average green-channel value from the centre-10% crop of         *fra, Ingest one frame and return a liveness probability. (+7 more)

### Community 12 - "Community 12"
Cohesion: 0.11
Nodes (15): count_parameters(), DepthwiseSeparableConv, get_model(), MiniFASNetV2, MiniFASNet-V2 — Lightweight Face Anti-Spoofing Network =========================, Forward pass.          Args:             x: Float tensor (N, 3, 80, 80)., Return total trainable parameter count., Factory — returns a freshly initialised MiniFASNetV2. (+7 more)

### Community 13 - "Community 13"
Cohesion: 0.09
Nodes (22): ChallengeService, ChallengeService get, ChallengeState get, LivenessResult get, LivenessResult, _challengeService, challengeState, _challengeUrl (+14 more)

### Community 14 - "Community 14"
Cohesion: 0.09
Nodes (22): Color, dart:math, build, _buildDynamicFaceGuide, _buildResultSummary, _cameras, _challengeSub, color (+14 more)

### Community 15 - "Community 15"
Cohesion: 0.09
Nodes (21): CameraController?, dart:io, List, package:camera/camera.dart, package:flutter/foundation.dart, build, _cameras, _controller (+13 more)

### Community 16 - "Community 16"
Cohesion: 0.10
Nodes (20): bool get, dart:async, dart:convert, dart:typed_data, ../models/liveness_result.dart, package:web_socket_channel/web_socket_channel.dart, _channel, connect (+12 more)

### Community 17 - "Community 17"
Cohesion: 0.15
Nodes (9): Dataset, Extract green-channel ROI signals from videos., Generate synthetic training data., PyTorch Dataset for rPPG liveness detection training., RPPGDataset, RPPGSignalExtractor, build_rppg_model(), evaluate() (+1 more)

### Community 18 - "Community 18"
Cohesion: 0.11
Nodes (13): ndarray, Validate that the user's response time is humanly plausible.          :param cha, Check that the background region stays stable across stored frames.          The, Clear the internal frame buffer., Extract the background border region of a greyscale frame.          Keeps only t, Lightweight temporal-consistency checker for liveness verification.      Maintai, Initialise the TemporalValidator.          :param min_response_time: Minimum cre, Store a frame (converted to greyscale) and its timestamp.          :param frame: (+5 more)

### Community 19 - "Community 19"
Cohesion: 0.11
Nodes (18): challenge_screen.dart, build, createState, initState, main, ShieldApp, _urlController, MaterialPageRoute (+10 more)

### Community 20 - "Community 20"
Cohesion: 0.14
Nodes (11): ChallengeSession, Marks the start time for the current challenge.          Must be called before `, Process a single frame's action-recognition result.          Call this for each, Returns the running challenge score as passed / total.          :return: Float b, Returns the full session state, suitable for WebSocket responses.          :retu, Checks whether the current challenge has exceeded its timeout.          :return:, Move to the next challenge or mark the session as complete., Selects *n* unique random ChallengeTypes.          :param n: Number of challenge (+3 more)

### Community 21 - "Community 21"
Cohesion: 0.16
Nodes (11): DataLoader, FASAugmentation, FASDataset, PyTorch Dataset for Face Anti-Spoofing training.     Supports directory-based lo, Args:             root_dir: Path to dataset with train/test subdirs containing r, Standard augmentations for FAS training., build_model(), evaluate() (+3 more)

### Community 22 - "Community 22"
Cohesion: 0.13
Nodes (12): Registry of active :class:`VerificationSession` instances.      Handles session, Create and register a new verification session.          :param client_id: Optio, Remove all expired sessions from the registry.          :return: Number of sessi, Check whether a client_id is within its rate limit.          Only sessions creat, Number of currently active (non-expired) sessions., SessionManager, Test basic session creation and lookup., Creating a session should make it retrievable by ID. (+4 more)

### Community 23 - "Community 23"
Cohesion: 0.12
Nodes (10): ChallengeBenchmark, Run *num_trials* simulated challenge sessions and report stats.          Half of, Benchmark blink detection accuracy.          If *video_dir* is provided, frames, Benchmark head-pose estimation accuracy.          Follows the same pattern as :m, Benchmarks for the Active Challenge-Response engine.      Provides three benchma, ChallengeMetrics, FASMetrics, Metrics specific to the Active Challenge-Response protocol.      Operates on a l (+2 more)

### Community 24 - "Community 24"
Cohesion: 0.14
Nodes (10): Any, FlutterAppDelegate, FlutterImplicitEngineBridge, FlutterImplicitEngineDelegate, Bool, AppDelegate, Bool, AppDelegate (+2 more)

### Community 25 - "Community 25"
Cohesion: 0.15
Nodes (10): ndarray, Compile the combined verification result.          Merges the challenge score fr, Look up a session by its ID.          :param session_id: UUID string of the desi, A single end-to-end liveness-verification session.      Bundles a :class:`Challe, Check whether this session has exceeded its TTL.          :return: ``True`` when, Ingest a single video frame for verification.          Performs the following in, VerificationSession, Test duplicate-frame detection in a VerificationSession. (+2 more)

### Community 26 - "Community 26"
Cohesion: 0.17
Nodes (15): ChangeNotifier, HomeScreen, _HomeScreenState, LivenessProvider, CameraScreen, _CameraScreenState, _startStreaming, ChallengeScreen (+7 more)

### Community 27 - "Community 27"
Cohesion: 0.19
Nodes (11): Enum, ChallengeType, SHIELD – Active Challenge-Response Engine  Server-side state machine that genera, Enumeration of supported liveness-challenge actions., SHIELD – Verification Session Manager  Manages active verification sessions, com, SHIELD – Temporal Validator  Validates that challenge responses are temporally c, SHIELD – Sprint D: Active Challenge-Response Test Suite  Comprehensive pytest te, Test frame coherence detection. (+3 more)

### Community 28 - "Community 28"
Cohesion: 0.13
Nodes (14): Current Status, Data sources, Detailed flow, How to use this repo, Key capabilities, ML Pipeline, Models and architecture, Notes (+6 more)

### Community 29 - "Community 29"
Cohesion: 0.29
Nodes (5): AdvancedFASAugmentation, ndarray, Tensor, Args:             img: uint8 ndarray (H, W, 3) BGR from cv2.          Returns:, Augmentation pipeline targeting print/replay attack artefacts.      Training tra

### Community 30 - "Community 30"
Cohesion: 0.15
Nodes (8): EfficientNetFAS, get_model(), EfficientNet-B0 Fine-Tuned for Face Anti-Spoofing (FAS)  Uses torchvision's Effi, EfficientNet-B0 adapted for Face Anti-Spoofing via transfer learning.      Strat, Unfreeze all backbone parameters (call after initial warm-up)., Factory function — returns a fine-tuned EfficientNetFAS., Tensor, WeightedRandomSampler

### Community 31 - "Community 31"
Cohesion: 0.27
Nodes (11): device, build_model(), compute_fas_metrics(), evaluate(), export_onnx(), make_weighted_sampler(), Module, SHIELD – Advanced Anti-Spoof Training Script v2 ================================ (+3 more)

### Community 32 - "Community 32"
Cohesion: 0.15
Nodes (12): Architecture, Datasets, graphify, Metrics, Models, Objective, Project Type, Repository Structure (+4 more)

### Community 33 - "Community 33"
Cohesion: 0.15
Nodes (12): 📈 Current Status & Next Steps, Milestone 0: Foundation & Infrastructure (Pre-May 2026), Milestone 1: Signal Quality & Pre-processing (Sprint 1), Milestone 2: Explainable Multimodal Fusion (Sprint 2), Milestone 3: Physiological Verification - Deep rPPG (Sprint 3), Milestone 4: Systematic Evaluation Framework (Sprints 4 & 5), Milestone 5: Active Challenge-Response Protocol (Sprint 6) - COMPLETED, Milestone 6: UI/UX Overhaul & Guidance System (Sprint 7) - COMPLETED (+4 more)

### Community 34 - "Community 34"
Cohesion: 0.23
Nodes (9): string, wchar_t, _In_, _In_opt_, wWinMain(), CreateAndAttachConsole(), GetCommandLineArguments(), Utf8FromUtf16() (+1 more)

### Community 35 - "Community 35"
Cohesion: 0.17
Nodes (11): FUTURE RESEARCH VERSION, GEMINI_NEXT.md, IMPORTANT IMPLEMENTATION RULES, Mission, Required checks, SPRINT 1 — PIPELINE STABILIZATION, SPRINT 2 — ANTI SPOOF INTEGRATION, SPRINT 3 — rPPG UPGRADE (+3 more)

### Community 36 - "Community 36"
Cohesion: 0.22
Nodes (8): WebSocket endpoint for passive liveness detection (no challenge prompts).     Re, Receives an image frame and runs the SHIELD liveness detection pipeline., WebSocket endpoint for active challenge-response liveness streaming.     Receive, verify_liveness(), websocket_challenge(), websocket_verify_passive(), UploadFile, WebSocket

### Community 37 - "Community 37"
Cohesion: 0.22
Nodes (8): DartProject, HWND, LPARAM, LRESULT, FlutterWindow(), UINT, WPARAM, MessageHandler()

### Community 38 - "Community 38"
Cohesion: 0.20
Nodes (8): package:flutter_test/flutter_test.dart, package:provider/provider.dart, package:shield_app/main.dart, package:shield_app/providers/liveness_provider.dart, ../providers/liveness_provider.dart, main, build, _buildDetailRow

### Community 39 - "Community 39"
Cohesion: 0.27
Nodes (4): DeepRPPGDetector, PhysNet, Initializes the Deep rPPG Detector., Processes a sequence of frames to extract pulse signal.         :param frames: L

### Community 40 - "Community 40"
Cohesion: 0.28
Nodes (7): _make_frame(), _make_noisy_frame(), ndarray, Two similar frames → coherent; one wildly different → incoherent., Frames with the same background should be consistent., Create a uniform BGR dummy frame filled with *value*., Create a BGR dummy frame with slight Gaussian noise.

### Community 41 - "Community 41"
Cohesion: 0.32
Nodes (3): AntispoofInference, Standardized inference wrapper for anti-spoof models.         Prioritizes loadin, Performs inference on a face crop.         :param face_crop: BGR image.

### Community 42 - "Community 42"
Cohesion: 0.32
Nodes (4): FusionEngine, Fuses multiple liveness scores into a single final score.         :param rppg_sc, Initializes the Fusion Engine with customizable weights.         :param weights:, test_fusion_engine()

### Community 43 - "Community 43"
Cohesion: 0.29
Nodes (4): MiniFASNet, Builds a lightweight CNN skeleton for MiniFASNet., Predicts the liveness score for a given face crop.         :param face_crop: Ope, Initializes the MiniFASNet anti-spoofing model.         :param model_path: Path

### Community 44 - "Community 44"
Cohesion: 0.29
Nodes (4): RegisterGeneratedPlugins(), FlutterPluginRegistry, NSWindow, MainFlutterWindow

### Community 45 - "Community 45"
Cohesion: 0.29
Nodes (3): RunnerTests, RunnerTests, XCTestCase

### Community 47 - "Community 47"
Cohesion: 0.33
Nodes (5): handle_new_rx_page(), __lldb_init_module(), Intercept NOTIFY_DEBUGGER_ABOUT_RX_PAGES and touch the pages., SBDebugger, SBFrame

### Community 48 - "Community 48"
Cohesion: 0.40
Nodes (4): 1. Challenge Protocol Robustness, 2. Blink Detection Benchmark, 3. Head Pose (Yaw/Pitch) Benchmark, SHIELD Benchmark Report (Synthetic Evaluation)

### Community 49 - "Community 49"
Cohesion: 0.40
Nodes (4): Conclusion, Confusion Matrix, SHIELD Benchmark Report, Summary Metrics

### Community 51 - "Community 51"
Cohesion: 0.50
Nodes (3): Pass 2 out of 3 challenges and verify the resulting score., Passing 2/3 challenges should yield score ≈ 0.6667., TestChallengePartialPass

### Community 52 - "Community 52"
Cohesion: 0.50
Nodes (3): Verify that `is_timed_out()` fires correctly., Starting a challenge and sleeping past the timeout should flag it., TestChallengeTimeoutDetection

### Community 53 - "Community 53"
Cohesion: 0.50
Nodes (3): Verify that retries are consumed before a challenge is marked failed., With max_retries=2, three timeouts are needed to fail a challenge., TestChallengeRetryLogic

### Community 54 - "Community 54"
Cohesion: 0.50
Nodes (3): Verify that the generated challenge sequence contains unique items., Each challenge in a session's sequence must be unique., TestChallengeSequenceUniqueness

### Community 55 - "Community 55"
Cohesion: 0.50
Nodes (3): Verify that sequences are randomised across sessions., 10 independent sessions should NOT all produce the same order., TestChallengeSequenceRandomness

### Community 56 - "Community 56"
Cohesion: 0.50
Nodes (3): Simulate passing every challenge and verify a perfect score., Passing all challenges should yield score == 1.0., TestChallengePassAll

### Community 57 - "Community 57"
Cohesion: 0.50
Nodes (3): Simulate failing every challenge via timeout and verify score == 0.0., Timing out on all challenges (with max_retries=0) → score == 0.0., TestChallengeFailAll

### Community 86 - "Community 86"
Cohesion: 0.25
Nodes (7): AI/Inference Pipeline, 🔍 Audit Checklist, Backend (Python/FastAPI), Frontend (Flutter/Dart), 🛡️ Overview Agent - Senior System Auditor, 🎯 Primary Directives, 🛠️ Tools & Workflow

## Knowledge Gaps
- **273 isolated node(s):** `SBFrame`, `SBDebugger`, `flutter_export_environment.sh script`, `UIApplication`, `Any` (+268 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_rppg_model_v2()` connect `Community 4` to `Community 11`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Why does `train()` connect `Community 4` to `Community 21`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `ChallengeSession` (e.g. with `BenchmarkEngine` and `ChallengeBenchmark`) actually correct?**
  _`ChallengeSession` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `TemporalValidator` (e.g. with `ndarray` and `SessionManager`) actually correct?**
  _`TemporalValidator` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `SessionManager` (e.g. with `ChallengeSession` and `TemporalValidator`) actually correct?**
  _`SessionManager` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `VerificationSession` (e.g. with `ChallengeSession` and `TemporalValidator`) actually correct?**
  _`VerificationSession` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `BehavioralAnalyzer` (e.g. with `BenchmarkEngine` and `ChallengeBenchmark`) actually correct?**
  _`BehavioralAnalyzer` has 3 INFERRED edges - model-reasoned connections that need verification._