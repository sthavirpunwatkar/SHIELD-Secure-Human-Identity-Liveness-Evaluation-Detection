# Graph Report - SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection  (2026-07-09)

## Corpus Check
- 160 files · ~210,655 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1473 nodes · 1938 edges · 120 communities (103 shown, 17 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 115 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `71ae20e2`
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
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
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
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]
- [[_COMMUNITY_Community 98|Community 98]]
- [[_COMMUNITY_Community 100|Community 100]]
- [[_COMMUNITY_Community 102|Community 102]]
- [[_COMMUNITY_Community 103|Community 103]]
- [[_COMMUNITY_Community 104|Community 104]]
- [[_COMMUNITY_Community 105|Community 105]]
- [[_COMMUNITY_Community 106|Community 106]]
- [[_COMMUNITY_Community 107|Community 107]]
- [[_COMMUNITY_Community 108|Community 108]]
- [[_COMMUNITY_Community 109|Community 109]]
- [[_COMMUNITY_Community 110|Community 110]]
- [[_COMMUNITY_Community 111|Community 111]]
- [[_COMMUNITY_Community 112|Community 112]]
- [[_COMMUNITY_Community 113|Community 113]]
- [[_COMMUNITY_Community 114|Community 114]]
- [[_COMMUNITY_Community 115|Community 115]]
- [[_COMMUNITY_Community 116|Community 116]]
- [[_COMMUNITY_Community 117|Community 117]]

## God Nodes (most connected - your core abstractions)
1. `ChallengeSession` - 44 edges
2. `RPPGDetector` - 32 edges
3. `SessionManager` - 32 edges
4. `TemporalValidator` - 32 edges
5. `VerificationSession` - 27 edges
6. `BehavioralAnalyzer` - 26 edges
7. `ChallengeType` - 22 edges
8. `FASDataset` - 18 edges
9. `🚀 Milestones & Progress` - 17 edges
10. `SHIELD Production Readiness & Root Cause Investigation Report` - 15 edges

## Surprising Connections (you probably didn't know these)
- `FusionService` --uses--> `BehavioralAnalyzer`  [INFERRED]
  backend/services/fusion_service.py → inference/behavioral_analyzer.py
- `FusionService` --uses--> `ChallengeSession`  [INFERRED]
  backend/services/fusion_service.py → inference/challenge_engine.py
- `FusionService` --uses--> `FusionEngine`  [INFERRED]
  backend/services/fusion_service.py → inference/fusion_engine.py
- `FusionService` --uses--> `RPPGDetector`  [INFERRED]
  backend/services/fusion_service.py → inference/rppg_detector.py
- `BenchmarkEngine` --uses--> `RPPGDetector`  [INFERRED]
  evaluation/benchmark.py → inference/rppg_detector.py

## Import Cycles
- None detected.

## Communities (120 total, 17 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (31): DataLoader, device, Tensor, FASAugmentation, FASDataset, PyTorch Dataset for Face Anti-Spoofing training.     Supports directory-based lo, Args:             root_dir: Path to dataset with train/test subdirs containing r, Standard augmentations for FAS training. (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (42): DartProject, RegisterPlugins(), HWND, LPARAM, LRESULT, FlutterWindow(), UINT, WPARAM (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (39): A1. Create `inference/challenge_engine.py` — The Brain, A2. Upgrade `inference/behavioral_analyzer.py` — Real Detection, A3. Upgrade `backend/services/fusion_service.py` — Session-Aware Processing, A4. Upgrade `backend/main.py` — Protocol Messages, Architecture Design, B1. Create `frontend/lib/services/challenge_service.dart`, B2. Create `frontend/lib/widgets/challenge_prompt.dart`, B3. Create `frontend/lib/screens/challenge_screen.dart` (+31 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (37): double?, int?, action, bbox, behavioralScore, blurScore, brightness, challengeIndex (+29 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (33): Animation, AnimationController, Color, CustomPainter, package:flutter/services.dart, _FaceGuideOvalPainter, ChallengeState, build (+25 more)

### Community 5 - "Community 5"
Cohesion: 0.31
Nodes (3): QualityScoreEngine, test_quality_gate(), verify_serialization()

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (28): ChallengeState, double get, int get, _challengeScore, ChallengeService, _countdownTimer, _currentAction, _currentIndex (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (22): fl_register_plugins(), FlView, FlPluginRegistry, GObject, GApplication, gboolean, gchar, GtkApplication (+14 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (13): Registry of active :class:`VerificationSession` instances.      Handles session, Create and register a new verification session.          :param client_id: Optio, Remove all expired sessions from the registry.          :return: Number of sessi, Check whether a client_id is within its rate limit.          Only sessions creat, Number of currently active (non-expired) sessions., SessionManager, Proof that TemporalValidator is part of the SessionManager workflow., Test basic session creation and lookup. (+5 more)

### Community 9 - "Community 9"
Cohesion: 0.07
Nodes (28): ChallengeService, ChallengeService get, ChallengeState get, LivenessResult, LivenessResult get, LivenessService, LivenessResult, _challengeService (+20 more)

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (22): dart:math, bbox, build, _buildDynamicFaceGuide, _buildResultSummary, _cameraService, _challengeSub, color (+14 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (18): build, CameraScreen, _CameraScreenState, _cameraService, createState, dispose, _errorMessage, _frameSub (+10 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (34): 📈 Current Status & Next Steps, Milestone 0: Foundation & Infrastructure (Pre-May 2026), Milestone 10: Fusion Weights Optimization (July 2026) - COMPLETED, Milestone 11: Active Identity Consistency Check (July 2026) - COMPLETED, Milestone 12: CDAC Academic Review Presentation (July 2026) - COMPLETED, Milestone 13: Flutter Web Port Stability & Layout Hardening (July 2026) - COMPLETED, Milestone 14: Quality Gate Calibration & Live Tracking Integration (July 2026) - COMPLETED, Milestone 15: Challenge Engine & UI State Synchronization (July 2026) - COMPLETED (+26 more)

### Community 13 - "Community 13"
Cohesion: 0.11
Nodes (17): bool get, dart:async, ../models/liveness_result.dart, package:web_socket_channel/web_socket_channel.dart, _channel, connect, dispose, _isConnected (+9 more)

### Community 14 - "Community 14"
Cohesion: 0.15
Nodes (9): Dataset, Extract green-channel ROI signals from videos., Generate synthetic training data., PyTorch Dataset for rPPG liveness detection training., RPPGDataset, RPPGSignalExtractor, build_rppg_model(), evaluate() (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.20
Nodes (13): evaluate(), export_onnx(), extract_roi_signal_from_video(), generate_live_signal(), generate_spoof_signal(), load_video_data(), ndarray, SHIELD – Upgraded rPPG Training Script v2  Training approach:   1. Synthetic dat (+5 more)

### Community 16 - "Community 16"
Cohesion: 0.16
Nodes (8): Detects faces and masks in a given frame.         :param frame: OpenCV image (BG, Crops a face from the frame based on a bounding box.         :param frame: OpenC, Initializes the YOLOv8-seg face and mask detector.         :param model_path: Pa, YoloSegDetector, FusionService, Specialized processing for challenge-mode frames.         Runs the full pipeline, Initializes all core AI models for orchestration., Runs the multi-modal pipeline on a single frame.         :param frame: OpenCV im

### Community 17 - "Community 17"
Cohesion: 0.13
Nodes (10): Convert a normalized MediaPipe landmark to pixel coordinates., Convert a normalized MediaPipe landmark to pixel coordinates (2D for solvePnP)., Euclidean distance between two 2D points., Computes the Eye Aspect Ratio (EAR) for a single eye.          EAR = (||p2 - p6|, Detects if a blink is occurring using EAR on both eyes.          A blink is dete, Detects if the mouth is open using MAR (Mouth Aspect Ratio).          MAR = vert, Detects a smile using the ratio of lip corner distance to vertical mouth opening, Estimates head pose (yaw, pitch, roll) using cv2.solvePnP with 6 facial landmark (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.16
Nodes (10): ChallengeSession, Marks the start time for the current challenge.          Must be called before `, Process a single frame's action-recognition result.          Call this for each, Returns the running challenge score as passed / total.          :return: Float b, Returns the full session state, suitable for WebSocket responses.          :retu, Checks whether the current challenge has exceeded its timeout.          :return:, Move to the next challenge or mark the session as complete., State machine for a single active-challenge verification session.      Generates (+2 more)

### Community 19 - "Community 19"
Cohesion: 0.50
Nodes (3): Simulate failing every challenge via timeout and verify score == 0.0., Timing out on all challenges (with max_retries=0) → score == 0.0., TestChallengeFailAll

### Community 20 - "Community 20"
Cohesion: 0.17
Nodes (7): fl_message_codec, G_DECLARE_DERIVABLE_TYPE(), FL, FlMessageCodec, G_MODULE_EXPORT, GObject, MESSAGE_CODEC

### Community 21 - "Community 21"
Cohesion: 0.22
Nodes (6): _build_v1_model(), Try each (path, variant) candidate in order.  Return the first that         load, Return the architecture matching *variant*., Rebuild the original 2-conv simple 1D-CNN., Module, Sequential

### Community 22 - "Community 22"
Cohesion: 0.14
Nodes (10): Compile the combined verification result.          Merges the challenge score fr, A single end-to-end liveness-verification session.      Bundles a :class:`Challe, Look up a session by its ID.          :param session_id: UUID string of the desi, Check whether this session has exceeded its TTL.          :return: ``True`` when, Ingest a single video frame for verification.          Performs the following in, VerificationSession, ndarray, Test duplicate-frame detection in a VerificationSession. (+2 more)

### Community 23 - "Community 23"
Cohesion: 0.14
Nodes (10): Any, FlutterAppDelegate, FlutterImplicitEngineBridge, FlutterImplicitEngineDelegate, Bool, AppDelegate, Bool, AppDelegate (+2 more)

### Community 24 - "Community 24"
Cohesion: 0.07
Nodes (24): WebSocket endpoint for passive liveness detection (no challenge prompts).     Re, Receives an image frame and runs the SHIELD liveness detection pipeline., WebSocket endpoint for active challenge-response liveness streaming.     Receive, verify_liveness(), websocket_challenge(), websocket_verify_passive(), Exception, Request (+16 more)

### Community 25 - "Community 25"
Cohesion: 0.10
Nodes (14): SHIELD – Verification Session Manager  Manages active verification sessions, com, ndarray, SHIELD – Temporal Validator  Validates that challenge responses are temporally c, Validate that the user's response time is humanly plausible.          :param cha, Check that the background region stays stable across stored frames.          The, Clear the internal frame buffer., Extract the background border region of a greyscale frame.          Keeps only t, Lightweight temporal-consistency checker for liveness verification.      Maintai (+6 more)

### Community 26 - "Community 26"
Cohesion: 0.16
Nodes (9): BenchmarkEngine, FASMetrics, Calculates Anti-Spoofing Metrics.         :param y_true: List of true labels (1, WeightTuner, BehavioralAnalyzer, Resets temporal tracking counters (call between sessions)., Initializes Behavioral analysis. Falls back to simple heuristics if MediaPipe fa, test_weight_tuner() (+1 more)

### Community 27 - "Community 27"
Cohesion: 0.22
Nodes (8): challenge_screen.dart, _buildPrepCard, _checkSebStatus, createState, initState, _isChecking, _isSebActive, ../services/security_service.dart

### Community 28 - "Community 28"
Cohesion: 0.22
Nodes (8): fl_pixel_buffer_texture, fl_texture_registrar, FlTextureRegistrar, G_DECLARE_INTERFACE(), FL, G_BEGIN_DECLS, GObject, TEXTURE_REGISTRAR

### Community 29 - "Community 29"
Cohesion: 0.22
Nodes (7): fl_standard_message_codec, FlStandardMessageCodec, G_DECLARE_DERIVABLE_TYPE(), FL, FlMessageCodec, G_BEGIN_DECLS, STANDARD_MESSAGE_CODEC

### Community 30 - "Community 30"
Cohesion: 0.23
Nodes (9): string, wchar_t, _In_, _In_opt_, wWinMain(), CreateAndAttachConsole(), GetCommandLineArguments(), Utf8FromUtf16() (+1 more)

### Community 31 - "Community 31"
Cohesion: 0.22
Nodes (6): FlPixelBufferTexture, G_DECLARE_DERIVABLE_TYPE(), FL, G_BEGIN_DECLS, GObject, PIXEL_BUFFER_TEXTURE

### Community 32 - "Community 32"
Cohesion: 0.17
Nodes (11): 1. Backend (Python/FastAPI), 2. Frontend (Flutter), 📊 Benchmark Scores, 🚀 Competitive Innovation, ✅ Completed (Current State), ⚙️ Installation & Setup, 🚀 Next Steps, 📋 Project Overview & Plan (+3 more)

### Community 33 - "Community 33"
Cohesion: 0.10
Nodes (20): createState, initState, main, _urlController, package:flutter_localizations/flutter_localizations.dart, package:flutter/material.dart, package:flutter_test/flutter_test.dart, package:provider/provider.dart (+12 more)

### Community 34 - "Community 34"
Cohesion: 0.22
Nodes (5): ChallengeBenchmark, Run *num_trials* simulated challenge sessions and report stats.          Half of, Benchmark blink detection accuracy.          If *video_dir* is provided, frames, Benchmark head-pose estimation accuracy.          Follows the same pattern as :m, Benchmarks for the Active Challenge-Response engine.      Provides three benchma

### Community 35 - "Community 35"
Cohesion: 0.03
Nodes (72): app_localizations_en.dart, app_localizations_es.dart, app_localizations_fr.dart, actionBlink, actionNod, actionNodDown, actionNodUp, actionOpenMouth (+64 more)

### Community 36 - "Community 36"
Cohesion: 0.03
Nodes (59): app_localizations.dart, actionBlink, actionNod, actionNodDown, actionNodUp, actionOpenMouth, actionPerform, actionRaiseEyebrows (+51 more)

### Community 37 - "Community 37"
Cohesion: 0.50
Nodes (3): ChallengeMetrics, Metrics specific to the Active Challenge-Response protocol.      Operates on a l, Calculate challenge-specific evaluation metrics.          :param challenge_resul

### Community 38 - "Community 38"
Cohesion: 0.22
Nodes (8): 1. Plan Mode Default, 4. Verification Before Done, Core Principles, graphify, SHIELD – Secure Human Identity & Liveness Evaluation Detection, Task Management, Workflow Hooks, Workflow Orchestration

### Community 39 - "Community 39"
Cohesion: 0.32
Nodes (3): AntispoofInference, Standardized inference wrapper for anti-spoof models.         Prioritizes loadin, Performs inference on a face crop.         :param face_crop: BGR image.

### Community 40 - "Community 40"
Cohesion: 0.25
Nodes (7): dart:convert, package:crypto/crypto.dart, _configKey, _configKeyHash, SebSigner, signUrl, static const String

### Community 41 - "Community 41"
Cohesion: 0.25
Nodes (7): AI/Inference Pipeline, 🔍 Audit Checklist, Backend (Python/FastAPI), Frontend (Flutter/Dart), 🛡️ Overview Agent - Senior System Auditor, 🎯 Primary Directives, 🛠️ Tools & Workflow

### Community 42 - "Community 42"
Cohesion: 0.29
Nodes (4): RegisterGeneratedPlugins(), FlutterPluginRegistry, NSWindow, MainFlutterWindow

### Community 43 - "Community 43"
Cohesion: 0.29
Nodes (3): RunnerTests, RunnerTests, XCTestCase

### Community 44 - "Community 44"
Cohesion: 0.03
Nodes (59): actionBlink, actionNod, actionNodDown, actionNodUp, actionOpenMouth, actionPerform, actionRaiseEyebrows, actionSmile (+51 more)

### Community 45 - "Community 45"
Cohesion: 0.03
Nodes (58): actionBlink, actionNod, actionNodDown, actionNodUp, actionOpenMouth, actionPerform, actionRaiseEyebrows, actionSmile (+50 more)

### Community 46 - "Community 46"
Cohesion: 0.33
Nodes (5): handle_new_rx_page(), __lldb_init_module(), Intercept NOTIFY_DEBUGGER_ABOUT_RX_PAGES and touch the pages., SBDebugger, SBFrame

### Community 47 - "Community 47"
Cohesion: 0.40
Nodes (4): 1. Challenge Protocol Robustness, 2. Blink Detection Benchmark, 3. Head Pose (Yaw/Pitch) Benchmark, SHIELD Benchmark Report (Synthetic Evaluation)

### Community 48 - "Community 48"
Cohesion: 0.40
Nodes (4): Conclusion, Confusion Matrix, SHIELD Benchmark Report, Summary Metrics

### Community 51 - "Community 51"
Cohesion: 0.29
Nodes (7): fl_method_codec, FlMethodCodec, G_DECLARE_DERIVABLE_TYPE(), FL, G_BEGIN_DECLS, GObject, METHOD_CODEC

### Community 52 - "Community 52"
Cohesion: 0.14
Nodes (12): dart:io, package:flutter/foundation.dart, return, seb/seb_checker.dart, false, isSafeExamBrowserActive, _checkLinuxVirtualCamera, _checkMacOSVirtualCamera (+4 more)

### Community 53 - "Community 53"
Cohesion: 0.14
Nodes (14): _make_frame(), _make_noisy_frame(), SHIELD – Sprint D: Active Challenge-Response Test Suite  Comprehensive pytest te, Test frame coherence detection., Two similar frames → coherent; one wildly different → incoherent., Test that suspiciously fast responses are flagged., A response faster than min_response_time should be invalid., Test background consistency detection. (+6 more)

### Community 54 - "Community 54"
Cohesion: 0.29
Nodes (6): convert_to_yolo(), download_mock_dataset(), extract_polygons_from_mask(), Since CASIA-SURF and HKBU require signed agreements and registration,     we cre, Extract polygons from a binary mask for YOLOv8-seg., Converts masks to YOLOv8-seg polygon format.     Classes: 0=face, 1=mask.

### Community 55 - "Community 55"
Cohesion: 0.29
Nodes (7): fl_method_response, FlMethodResponse, G_DECLARE_DERIVABLE_TYPE(), FL, G_MODULE_EXPORT, GObject, METHOD_RESPONSE

### Community 56 - "Community 56"
Cohesion: 0.22
Nodes (9): @JS, dart:js_interop, dart:typed_data, encodeFrame, _encodeFrameFromJpegBytes, initialize, _initWebCodecsEncoder, _isInitialized (+1 more)

### Community 57 - "Community 57"
Cohesion: 0.29
Nodes (7): fl_plugin_registrar, FlPluginRegistrar, G_DECLARE_INTERFACE(), FL, G_BEGIN_DECLS, GObject, PLUGIN_REGISTRAR

### Community 64 - "Community 64"
Cohesion: 0.50
Nodes (3): Pass 2 out of 3 challenges and verify the resulting score., Passing 2/3 challenges should yield score ≈ 0.6667., TestChallengePartialPass

### Community 78 - "Community 78"
Cohesion: 0.25
Nodes (7): fl_plugin_registry, G_DECLARE_INTERFACE(), FL, FlPluginRegistry, G_BEGIN_DECLS, GObject, PLUGIN_REGISTRY

### Community 83 - "Community 83"
Cohesion: 0.29
Nodes (7): fl_texture, FlTexture, G_DECLARE_INTERFACE(), FL, G_BEGIN_DECLS, GObject, TEXTURE

### Community 84 - "Community 84"
Cohesion: 0.29
Nodes (7): fl_texture_gl, FlTextureGL, G_DECLARE_DERIVABLE_TYPE(), FL, G_BEGIN_DECLS, GObject, TEXTURE_GL

### Community 85 - "Community 85"
Cohesion: 0.40
Nodes (4): dart:html, contains, isSafeExamBrowserActive, userAgent

### Community 87 - "Community 87"
Cohesion: 0.25
Nodes (6): Enum, ChallengeType, SHIELD – Active Challenge-Response Engine  Server-side state machine that genera, Enumeration of supported liveness-challenge actions., Selects *n* unique random ChallengeTypes.          :param n: Number of challenge, Initialises a ChallengeSession and generates its challenge sequence.          :p

### Community 88 - "Community 88"
Cohesion: 0.33
Nodes (7): AppLocalizations, _AppLocalizationsDelegate, AppLocalizationsEn, AppLocalizationsEs, AppLocalizationsFr, of, LocalizationsDelegate

### Community 89 - "Community 89"
Cohesion: 0.18
Nodes (16): HomeScreen, _HomeScreenState, ShieldApp, ChallengeScreen, _ChallengeScreenState, PreVerificationScreen, _PreVerificationScreenState, _state (+8 more)

### Community 93 - "Community 93"
Cohesion: 0.09
Nodes (13): run_ablation(), exp1_rppg_roi(), inference/rppg_detector.py =========================== Real-time rPPG liveness d, Extract the average green-channel value from the facial skin ROI.         If a f, Ingest one frame and return a liveness probability., Clear the signal buffer (e.g. between subjects)., Fraction of the window that is currently filled [0, 1]., Frame-by-frame rPPG liveness scorer.      Parameters     ----------     window_s (+5 more)

### Community 94 - "Community 94"
Cohesion: 0.50
Nodes (3): Verify that retries are consumed before a challenge is marked failed., With max_retries=2, three timeouts are needed to fail a challenge., TestChallengeRetryLogic

### Community 95 - "Community 95"
Cohesion: 0.50
Nodes (3): Verify that `is_timed_out()` fires correctly., Starting a challenge and sleeping past the timeout should flag it., TestChallengeTimeoutDetection

### Community 96 - "Community 96"
Cohesion: 0.50
Nodes (3): Verify that sequences are randomised across sessions., 10 independent sessions should NOT all produce the same order., TestChallengeSequenceRandomness

### Community 97 - "Community 97"
Cohesion: 0.50
Nodes (3): Simulate passing every challenge and verify a perfect score., Passing all challenges should yield score == 1.0., TestChallengePassAll

### Community 98 - "Community 98"
Cohesion: 0.10
Nodes (19): CameraController?, CameraController? get, CameraState get, List, ../models/camera_frame.dart, CameraState, ../models/camera_state.dart, errorUnknown (+11 more)

### Community 100 - "Community 100"
Cohesion: 0.50
Nodes (3): Verify that the generated challenge sequence contains unique items., Each challenge in a session's sequence must be unique., TestChallengeSequenceUniqueness

### Community 102 - "Community 102"
Cohesion: 0.12
Nodes (15): PHASE 0 — BUILD & EXECUTION VALIDATION, PHASE 10 — SECURITY REVIEW, PHASE 11 — PRODUCTION READINESS, PHASE 12 — SIMPLIFICATION, PHASE 13 — REFACTORING ROADMAP, PHASE 1 — COMPLETE ARCHITECTURE, PHASE 2 — EXECUTION TRACE, PHASE 3 — RUNTIME PROFILING (+7 more)

### Community 103 - "Community 103"
Cohesion: 0.13
Nodes (14): 2026 07 06 20 11 15, Acceptance Examples, Actors, Deferred to Planning, Dependencies / Assumptions, Key Decisions, Key Flows, Next Steps (+6 more)

### Community 104 - "Community 104"
Cohesion: 0.14
Nodes (13): Completed Experiments, Completed Research, Current Architecture, Current Progress Percentage, Current Version, Future Work, Implemented Features, Known Issues (+5 more)

### Community 105 - "Community 105"
Cohesion: 0.19
Nodes (4): FusionEngine, Fuses multiple liveness scores into a single final score.         Uses dynamic w, Initializes the Fusion Engine with customizable weights.         :param weights:, test_fusion_engine()

### Community 106 - "Community 106"
Cohesion: 0.18
Nodes (7): CameraImage, DateTime, ReportGenerator, CameraFrame, image, timestamp, package:camera/camera.dart

### Community 107 - "Community 107"
Cohesion: 0.29
Nodes (10): ChangeNotifier, build, LivenessProvider, MaterialPageRoute, LivenessProvider, _startStreaming, _resetChallenge, _startChallenge (+2 more)

### Community 108 - "Community 108"
Cohesion: 0.25
Nodes (7): Candidate Findings, F1. No obvious failure detected automatically, Human Review Checklist, Product Feedback Analysis, Selected Moments, Source, Transcript

### Community 109 - "Community 109"
Cohesion: 0.29
Nodes (4): LocalDBService, Logs verification metadata to SQLite DB., Initializes SQLite DB and local storage., Uploads a verification snapshot to local storage.

### Community 110 - "Community 110"
Cohesion: 0.29
Nodes (6): Analysis Artifacts, Local-Only Frames, Local Raw Files, Original Source, Source Materials, Transcript

### Community 111 - "Community 111"
Cohesion: 0.29
Nodes (6): Architectural Decisions, Changelog, Experiments Concluded, Investigations Completed, [v1.0] - 2026-07-08, Verified Fixes

### Community 112 - "Community 112"
Cohesion: 0.29
Nodes (6): Implementation Order, Milestone 1: Asynchronous Database Migration, Milestone 2: 3D Identity Signature Refactor, Milestone 3: Backend H.264 Video Stream Decoding, Milestone 4: Native Flutter 30 FPS Video Streaming, SHIELD V2 Implementation Guide

### Community 113 - "Community 113"
Cohesion: 0.40
Nodes (4): 1. Visual/UI Problems, 2. Functional Problems, 3. Requirements, 4. Usability/UX Problems

### Community 114 - "Community 114"
Cohesion: 0.40
Nodes (4): Future Production (Cloud Infrastructure), SHIELD Roadmap, Version 2 (Implementation), Version 3 (Enterprise Scale)

## Knowledge Gaps
- **667 isolated node(s):** `SHIELD Bug Tracker`, `Verified Fixes`, `Investigations Completed`, `Experiments Concluded`, `Architectural Decisions` (+662 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RPPGDetector` connect `Community 93` to `Community 34`, `Community 105`, `Community 16`, `Community 21`, `Community 25`, `Community 26`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `Community 8` to `Community 64`, `Community 97`, `Community 96`, `Community 100`, `Community 18`, `Community 19`, `Community 53`, `Community 22`, `Community 24`, `Community 25`, `Community 94`, `Community 95`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `ChallengeSession` connect `Community 18` to `Community 64`, `Community 97`, `Community 34`, `Community 96`, `Community 100`, `Community 8`, `Community 105`, `Community 16`, `Community 19`, `Community 53`, `Community 22`, `Community 87`, `Community 25`, `Community 26`, `Community 94`, `Community 95`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `ChallengeSession` (e.g. with `BenchmarkEngine` and `ChallengeBenchmark`) actually correct?**
  _`ChallengeSession` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `RPPGDetector` (e.g. with `BenchmarkEngine` and `ChallengeBenchmark`) actually correct?**
  _`RPPGDetector` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `SessionManager` (e.g. with `ChallengeSession` and `TemporalValidator`) actually correct?**
  _`SessionManager` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `TemporalValidator` (e.g. with `SessionManager` and `VerificationSession`) actually correct?**
  _`TemporalValidator` has 16 INFERRED edges - model-reasoned connections that need verification._