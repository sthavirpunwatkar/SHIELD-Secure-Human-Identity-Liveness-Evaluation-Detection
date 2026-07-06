# Graph Report - SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection  (2026-07-06)

## Corpus Check
- 143 files · ~121,568 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1317 nodes · 1736 edges · 99 communities (85 shown, 14 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 113 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `43132176`
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
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]
- [[_COMMUNITY_Community 98|Community 98]]

## God Nodes (most connected - your core abstractions)
1. `ChallengeSession` - 44 edges
2. `SessionManager` - 32 edges
3. `TemporalValidator` - 32 edges
4. `VerificationSession` - 27 edges
5. `BehavioralAnalyzer` - 26 edges
6. `RPPGDetector` - 23 edges
7. `ChallengeType` - 22 edges
8. `FASDataset` - 18 edges
9. `🚀 Milestones & Progress` - 17 edges
10. `LivenessProvider` - 15 edges

## Surprising Connections (you probably didn't know these)
- `WebSocket` --uses--> `SessionManager`  [INFERRED]
  backend/main.py → inference/session_manager.py
- `UploadFile` --uses--> `SessionManager`  [INFERRED]
  backend/main.py → inference/session_manager.py
- `FusionService` --uses--> `BehavioralAnalyzer`  [INFERRED]
  backend/services/fusion_service.py → inference/behavioral_analyzer.py
- `FusionService` --uses--> `ChallengeSession`  [INFERRED]
  backend/services/fusion_service.py → inference/challenge_engine.py
- `FusionService` --uses--> `FusionEngine`  [INFERRED]
  backend/services/fusion_service.py → inference/fusion_engine.py

## Import Cycles
- None detected.

## Communities (99 total, 14 thin omitted)

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
Nodes (30): Animation, AnimationController, Color, dart:math, package:flutter/services.dart, build, _buildActiveCard, _buildContent (+22 more)

### Community 5 - "Community 5"
Cohesion: 0.31
Nodes (3): QualityScoreEngine, test_quality_gate(), verify_serialization()

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (29): ChallengeState, double get, int get, _challengeScore, ChallengeService, ChallengeState, _countdownTimer, _currentAction (+21 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (22): fl_register_plugins(), FlView, FlPluginRegistry, GObject, GApplication, gboolean, gchar, GtkApplication (+14 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (15): Receives an image frame and runs the SHIELD liveness detection pipeline., verify_liveness(), Registry of active :class:`VerificationSession` instances.      Handles session, Create and register a new verification session.          :param client_id: Optio, Remove all expired sessions from the registry.          :return: Number of sessi, Check whether a client_id is within its rate limit.          Only sessions creat, Number of currently active (non-expired) sessions., SessionManager (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (25): ChallengeService, ChallengeService get, ChallengeState get, LivenessResult, LivenessResult get, LivenessService, LivenessResult, _challengeService (+17 more)

### Community 10 - "Community 10"
Cohesion: 0.07
Nodes (33): ChangeNotifier, LivenessProvider, _startStreaming, bbox, build, _buildDynamicFaceGuide, _buildResultSummary, _cameras (+25 more)

### Community 11 - "Community 11"
Cohesion: 0.10
Nodes (20): CameraController?, List, package:camera/camera.dart, build, _cameras, _controller, createState, dispose (+12 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (34): 📈 Current Status & Next Steps, Milestone 0: Foundation & Infrastructure (Pre-May 2026), Milestone 10: Fusion Weights Optimization (July 2026) - COMPLETED, Milestone 11: Active Identity Consistency Check (July 2026) - COMPLETED, Milestone 12: CDAC Academic Review Presentation (July 2026) - COMPLETED, Milestone 13: Flutter Web Port Stability & Layout Hardening (July 2026) - COMPLETED, Milestone 14: Quality Gate Calibration & Live Tracking Integration (July 2026) - COMPLETED, Milestone 15: Challenge Engine & UI State Synchronization (July 2026) - COMPLETED (+26 more)

### Community 13 - "Community 13"
Cohesion: 0.10
Nodes (19): bool get, dart:async, dart:typed_data, ../models/liveness_result.dart, package:web_socket_channel/web_socket_channel.dart, _channel, connect, dispose (+11 more)

### Community 14 - "Community 14"
Cohesion: 0.15
Nodes (9): Dataset, Extract green-channel ROI signals from videos., Generate synthetic training data., PyTorch Dataset for rPPG liveness detection training., RPPGDataset, RPPGSignalExtractor, build_rppg_model(), evaluate() (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.22
Nodes (13): evaluate(), export_onnx(), extract_roi_signal_from_video(), generate_live_signal(), generate_spoof_signal(), load_video_data(), ndarray, SHIELD – Upgraded rPPG Training Script v2  Training approach:   1. Synthetic dat (+5 more)

### Community 16 - "Community 16"
Cohesion: 0.16
Nodes (8): Detects faces and masks in a given frame.         :param frame: OpenCV image (BG, Crops a face from the frame based on a bounding box.         :param frame: OpenC, Initializes the YOLOv8-seg face and mask detector.         :param model_path: Pa, YoloSegDetector, FusionService, Specialized processing for challenge-mode frames.         Runs the full pipeline, Initializes all core AI models for orchestration., Runs the multi-modal pipeline on a single frame.         :param frame: OpenCV im

### Community 17 - "Community 17"
Cohesion: 0.13
Nodes (10): Convert a normalized MediaPipe landmark to pixel coordinates., Convert a normalized MediaPipe landmark to pixel coordinates (2D for solvePnP)., Euclidean distance between two 2D points., Computes the Eye Aspect Ratio (EAR) for a single eye.          EAR = (||p2 - p6|, Detects if a blink is occurring using EAR on both eyes.          A blink is dete, Detects if the mouth is open using MAR (Mouth Aspect Ratio).          MAR = vert, Detects a smile using the ratio of lip corner distance to vertical mouth opening, Estimates head pose (yaw, pitch, roll) using cv2.solvePnP with 6 facial landmark (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.12
Nodes (14): ChallengeSession, Marks the start time for the current challenge.          Must be called before `, Process a single frame's action-recognition result.          Call this for each, Returns the running challenge score as passed / total.          :return: Float b, Returns the full session state, suitable for WebSocket responses.          :retu, Checks whether the current challenge has exceeded its timeout.          :return:, Move to the next challenge or mark the session as complete., Selects *n* unique random ChallengeTypes.          :param n: Number of challenge (+6 more)

### Community 19 - "Community 19"
Cohesion: 0.50
Nodes (3): Simulate failing every challenge via timeout and verify score == 0.0., Timing out on all challenges (with max_retries=0) → score == 0.0., TestChallengeFailAll

### Community 20 - "Community 20"
Cohesion: 0.17
Nodes (7): fl_message_codec, G_DECLARE_DERIVABLE_TYPE(), FL, FlMessageCodec, G_MODULE_EXPORT, GObject, MESSAGE_CODEC

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (13): _build_v1_model(), Module, ndarray, Try each (path, variant) candidate in order.  Return the first that         load, Return the architecture matching *variant*., Extract the average green-channel value from the centre-10% crop of         *fra, Ingest one frame and return a liveness probability., Clear the signal buffer (e.g. between subjects). (+5 more)

### Community 22 - "Community 22"
Cohesion: 0.14
Nodes (12): Compile the combined verification result.          Merges the challenge score fr, A single end-to-end liveness-verification session.      Bundles a :class:`Challe, Look up a session by its ID.          :param session_id: UUID string of the desi, Check whether this session has exceeded its TTL.          :return: ``True`` when, Ingest a single video frame for verification.          Performs the following in, VerificationSession, ndarray, _make_frame() (+4 more)

### Community 23 - "Community 23"
Cohesion: 0.14
Nodes (10): Any, FlutterAppDelegate, FlutterImplicitEngineBridge, FlutterImplicitEngineDelegate, Bool, AppDelegate, Bool, AppDelegate (+2 more)

### Community 24 - "Community 24"
Cohesion: 0.10
Nodes (18): WebSocket endpoint for passive liveness detection (no challenge prompts).     Re, WebSocket endpoint for active challenge-response liveness streaming.     Receive, websocket_challenge(), websocket_verify_passive(), Exception, Request, Verifies the Safe Exam Browser RequestHash.     The RequestHash is a SHA256 hash, FastAPI dependency to verify SEB headers for HTTP requests. (+10 more)

### Community 25 - "Community 25"
Cohesion: 0.10
Nodes (13): ndarray, Validate that the user's response time is humanly plausible.          :param cha, Check that the background region stays stable across stored frames.          The, Clear the internal frame buffer., Extract the background border region of a greyscale frame.          Keeps only t, Lightweight temporal-consistency checker for liveness verification.      Maintai, Initialise the TemporalValidator.          :param min_response_time: Minimum cre, Store a frame (converted to greyscale) and its timestamp.          :param frame: (+5 more)

### Community 26 - "Community 26"
Cohesion: 0.19
Nodes (7): WeightTuner, BehavioralAnalyzer, Resets temporal tracking counters (call between sessions)., Initializes Behavioral analysis. Falls back to simple heuristics if MediaPipe fa, inference/rppg_detector.py =========================== Real-time rPPG liveness d, test_weight_tuner(), main()

### Community 27 - "Community 27"
Cohesion: 0.17
Nodes (11): challenge_screen.dart, build, MaterialPageRoute, build, _buildPrepCard, _checkSebStatus, createState, initState (+3 more)

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
Cohesion: 0.12
Nodes (17): createState, initState, main, ShieldApp, _urlController, package:flutter_localizations/flutter_localizations.dart, package:flutter/material.dart, package:shield_app/l10n/app_localizations.dart (+9 more)

### Community 34 - "Community 34"
Cohesion: 0.11
Nodes (12): BenchmarkEngine, ChallengeBenchmark, Run *num_trials* simulated challenge sessions and report stats.          Half of, Benchmark blink detection accuracy.          If *video_dir* is provided, frames, Benchmark head-pose estimation accuracy.          Follows the same pattern as :m, Benchmarks for the Active Challenge-Response engine.      Provides three benchma, FASMetrics, Calculates Anti-Spoofing Metrics.         :param y_true: List of true labels (1 (+4 more)

### Community 35 - "Community 35"
Cohesion: 0.03
Nodes (72): app_localizations_en.dart, app_localizations_es.dart, app_localizations_fr.dart, actionBlink, actionNod, actionNodDown, actionNodUp, actionOpenMouth (+64 more)

### Community 36 - "Community 36"
Cohesion: 0.03
Nodes (58): actionBlink, actionNod, actionNodDown, actionNodUp, actionOpenMouth, actionPerform, actionRaiseEyebrows, actionSmile (+50 more)

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
Nodes (59): app_localizations.dart, actionBlink, actionNod, actionNodDown, actionNodUp, actionOpenMouth, actionPerform, actionRaiseEyebrows (+51 more)

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
Cohesion: 0.20
Nodes (8): _make_noisy_frame(), Test frame coherence detection., Two similar frames → coherent; one wildly different → incoherent., Test background consistency detection., Frames with the same background should be consistent., Create a BGR dummy frame with slight Gaussian noise., TestTemporalBackgroundConsistency, TestTemporalFrameCoherence

### Community 54 - "Community 54"
Cohesion: 0.29
Nodes (6): convert_to_yolo(), download_mock_dataset(), extract_polygons_from_mask(), Since CASIA-SURF and HKBU require signed agreements and registration,     we cre, Extract polygons from a binary mask for YOLOv8-seg., Converts masks to YOLOv8-seg polygon format.     Classes: 0=face, 1=mask.

### Community 55 - "Community 55"
Cohesion: 0.29
Nodes (7): fl_method_response, FlMethodResponse, G_DECLARE_DERIVABLE_TYPE(), FL, G_MODULE_EXPORT, GObject, METHOD_RESPONSE

### Community 56 - "Community 56"
Cohesion: 0.17
Nodes (6): DateTime?, ReportGenerator, LocalDBService, Logs verification metadata to SQLite DB., Initializes SQLite DB and local storage., Uploads a verification snapshot to local storage.

### Community 57 - "Community 57"
Cohesion: 0.29
Nodes (7): fl_plugin_registrar, FlPluginRegistrar, G_DECLARE_INTERFACE(), FL, G_BEGIN_DECLS, GObject, PLUGIN_REGISTRAR

### Community 64 - "Community 64"
Cohesion: 0.29
Nodes (4): Proof that TemporalValidator is part of the SessionManager workflow., Proof that ChallengeSession is integrated with FusionService., Proof that RPPGDetector is available in FusionService., TestAuditIntegrity

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
Cohesion: 0.14
Nodes (13): Enum, ChallengeType, SHIELD – Active Challenge-Response Engine  Server-side state machine that genera, Enumeration of supported liveness-challenge actions., SHIELD – Verification Session Manager  Manages active verification sessions, com, SHIELD – Temporal Validator  Validates that challenge responses are temporally c, SHIELD – Sprint D: Active Challenge-Response Test Suite  Comprehensive pytest te, Pass 2 out of 3 challenges and verify the resulting score. (+5 more)

### Community 88 - "Community 88"
Cohesion: 0.33
Nodes (7): AppLocalizations, _AppLocalizationsDelegate, AppLocalizationsEn, AppLocalizationsEs, AppLocalizationsFr, of, LocalizationsDelegate

### Community 89 - "Community 89"
Cohesion: 0.22
Nodes (14): HomeScreen, _HomeScreenState, CameraScreen, _CameraScreenState, ChallengeScreen, _ChallengeScreenState, PreVerificationScreen, _PreVerificationScreenState (+6 more)

### Community 93 - "Community 93"
Cohesion: 0.33
Nodes (5): package:flutter_test/flutter_test.dart, package:provider/provider.dart, package:shield_app/main.dart, package:shield_app/providers/liveness_provider.dart, main

### Community 94 - "Community 94"
Cohesion: 0.50
Nodes (3): Verify that retries are consumed before a challenge is marked failed., With max_retries=2, three timeouts are needed to fail a challenge., TestChallengeRetryLogic

### Community 96 - "Community 96"
Cohesion: 0.50
Nodes (3): Verify that sequences are randomised across sessions., 10 independent sessions should NOT all produce the same order., TestChallengeSequenceRandomness

### Community 97 - "Community 97"
Cohesion: 0.50
Nodes (3): Simulate passing every challenge and verify a perfect score., Passing all challenges should yield score == 1.0., TestChallengePassAll

### Community 98 - "Community 98"
Cohesion: 0.67
Nodes (3): CustomPainter, _FaceGuideOvalPainter, _CountdownRingPainter

## Knowledge Gaps
- **590 isolated node(s):** `SecurityService`, `hasVirtualCamera`, `_checkLinuxVirtualCamera`, `_checkWindowsVirtualCamera`, `_checkMacOSVirtualCamera` (+585 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `Community 8` to `Community 64`, `Community 97`, `Community 96`, `Community 18`, `Community 19`, `Community 53`, `Community 22`, `Community 87`, `Community 24`, `Community 25`, `Community 94`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `ChallengeSession` connect `Community 18` to `Community 64`, `Community 97`, `Community 34`, `Community 96`, `Community 8`, `Community 16`, `Community 19`, `Community 53`, `Community 22`, `Community 87`, `Community 25`, `Community 94`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `BehavioralAnalyzer` connect `Community 26` to `Community 16`, `Community 17`, `Community 34`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `ChallengeSession` (e.g. with `BenchmarkEngine` and `ChallengeBenchmark`) actually correct?**
  _`ChallengeSession` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `SessionManager` (e.g. with `ChallengeSession` and `TemporalValidator`) actually correct?**
  _`SessionManager` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `TemporalValidator` (e.g. with `SessionManager` and `VerificationSession`) actually correct?**
  _`TemporalValidator` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `VerificationSession` (e.g. with `ChallengeSession` and `TemporalValidator`) actually correct?**
  _`VerificationSession` has 15 INFERRED edges - model-reasoned connections that need verification._