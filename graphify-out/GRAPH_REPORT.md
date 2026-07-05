# Graph Report - SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection  (2026-07-05)

## Corpus Check
- 103 files · ~49,048 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 971 nodes · 1364 edges · 88 communities (64 shown, 24 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 124 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `45c6c311`
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
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]

## God Nodes (most connected - your core abstractions)
1. `ChallengeSession` - 46 edges
2. `TemporalValidator` - 34 edges
3. `SessionManager` - 33 edges
4. `VerificationSession` - 28 edges
5. `BehavioralAnalyzer` - 26 edges
6. `ChallengeType` - 23 edges
7. `RPPGDetector` - 23 edges
8. `FASDataset` - 18 edges
9. `🚀 Milestones & Progress` - 17 edges
10. `LivenessProvider` - 15 edges

## Surprising Connections (you probably didn't know these)
- `UploadFile` --uses--> `SessionManager`  [INFERRED]
  backend/main.py → inference/session_manager.py
- `WebSocket` --uses--> `SessionManager`  [INFERRED]
  backend/main.py → inference/session_manager.py
- `FusionService` --uses--> `ChallengeSession`  [INFERRED]
  backend/services/fusion_service.py → inference/challenge_engine.py
- `BenchmarkEngine` --uses--> `ChallengeSession`  [INFERRED]
  evaluation/benchmark.py → inference/challenge_engine.py
- `BenchmarkEngine` --uses--> `ChallengeType`  [INFERRED]
  evaluation/benchmark.py → inference/challenge_engine.py

## Import Cycles
- None detected.

## Communities (88 total, 24 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (31): DataLoader, device, Tensor, FASAugmentation, FASDataset, PyTorch Dataset for Face Anti-Spoofing training.     Supports directory-based lo, Args:             root_dir: Path to dataset with train/test subdirs containing r, Standard augmentations for FAS training. (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (34): RegisterPlugins(), HWND, LPARAM, LRESULT, UINT, wchar_t, WPARAM, PluginRegistry (+26 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (39): A1. Create `inference/challenge_engine.py` — The Brain, A2. Upgrade `inference/behavioral_analyzer.py` — Real Detection, A3. Upgrade `backend/services/fusion_service.py` — Session-Aware Processing, A4. Upgrade `backend/main.py` — Protocol Messages, Architecture Design, B1. Create `frontend/lib/services/challenge_service.dart`, B2. Create `frontend/lib/widgets/challenge_prompt.dart`, B3. Create `frontend/lib/screens/challenge_screen.dart` (+31 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (37): double?, int?, action, bbox, behavioralScore, blurScore, brightness, challengeIndex (+29 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (33): Animation, AnimationController, CustomPainter, dart:math, package:flutter/services.dart, _FaceGuideOvalPainter, build, _buildActiveCard (+25 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (17): BlurDetector, Detects if the face crop is blurry.         :param face_crop: OpenCV image (BGR), Initializes the Blur Detector using Variance of Laplacian.         :param thresh, IlluminationDetector, Detects if the illumination is 'good', 'underexposed', or 'overexposed'., Initializes the Illumination Detector.         :param low_threshold: Minimum mea, OcclusionDetector, Detects if the face is occluded.         :param face_crop: OpenCV image (BGR). (+9 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (29): ChallengeState, double get, int get, _challengeScore, ChallengeService, ChallengeState, _countdownTimer, _currentAction (+21 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (22): FlPluginRegistry, fl_register_plugins(), FlView, GApplication, gboolean, gchar, GObject, GtkApplication (+14 more)

### Community 8 - "Community 8"
Cohesion: 0.18
Nodes (7): Receives an image frame and runs the SHIELD liveness detection pipeline., verify_liveness(), Enum, SHIELD – Active Challenge-Response Engine  Server-side state machine that genera, SHIELD – Verification Session Manager  Manages active verification sessions, com, SHIELD – Temporal Validator  Validates that challenge responses are temporally c, UploadFile

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (22): ChallengeService, ChallengeService get, ChallengeState get, LivenessResult get, LivenessResult, _challengeService, challengeState, _challengeUrl (+14 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (24): Color, bbox, build, _buildDynamicFaceGuide, _buildResultSummary, _cameras, _challengeSub, color (+16 more)

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (22): CameraController?, dart:io, List, package:camera/camera.dart, package:flutter/foundation.dart, build, _cameras, _controller (+14 more)

### Community 12 - "Community 12"
Cohesion: 0.09
Nodes (20): benchmarkData, COLORS, compHeaders, compRows, flowSteps, FONTS, objectivesList, pptxgen (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.10
Nodes (20): bool get, dart:async, dart:convert, dart:typed_data, ../models/liveness_result.dart, package:web_socket_channel/web_socket_channel.dart, _channel, connect (+12 more)

### Community 14 - "Community 14"
Cohesion: 0.15
Nodes (9): Dataset, Extract green-channel ROI signals from videos., Generate synthetic training data., PyTorch Dataset for rPPG liveness detection training., RPPGDataset, RPPGSignalExtractor, build_rppg_model(), evaluate() (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.22
Nodes (13): evaluate(), export_onnx(), extract_roi_signal_from_video(), generate_live_signal(), generate_spoof_signal(), load_video_data(), ndarray, SHIELD – Upgraded rPPG Training Script v2  Training approach:   1. Synthetic dat (+5 more)

### Community 16 - "Community 16"
Cohesion: 0.06
Nodes (31): AntispoofInference, Standardized inference wrapper for anti-spoof models.         Prioritizes loadin, Performs inference on a face crop.         :param face_crop: BGR image., BenchmarkEngine, ChallengeBenchmark, Run *num_trials* simulated challenge sessions and report stats.          Half of, Benchmark blink detection accuracy.          If *video_dir* is provided, frames, Benchmark head-pose estimation accuracy.          Follows the same pattern as :m (+23 more)

### Community 17 - "Community 17"
Cohesion: 0.13
Nodes (10): Convert a normalized MediaPipe landmark to pixel coordinates., Convert a normalized MediaPipe landmark to pixel coordinates (2D for solvePnP)., Euclidean distance between two 2D points., Computes the Eye Aspect Ratio (EAR) for a single eye.          EAR = (||p2 - p6|, Detects if a blink is occurring using EAR on both eyes.          A blink is dete, Detects if the mouth is open using MAR (Mouth Aspect Ratio).          MAR = vert, Detects a smile using the ratio of lip corner distance to vertical mouth opening, Estimates head pose (yaw, pitch, roll) using cv2.solvePnP with 6 facial landmark (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.08
Nodes (48): ChallengeSession, ChallengeType, Enumeration of supported liveness-challenge actions., State machine for a single active-challenge verification session.      Generates, Returns the ChallengeType the user should perform next.          :return: Curren, Registry of active :class:`VerificationSession` instances.      Handles session, A single end-to-end liveness-verification session.      Bundles a :class:`Challe, SessionManager (+40 more)

### Community 19 - "Community 19"
Cohesion: 0.18
Nodes (8): _make_frame(), _make_noisy_frame(), Two similar frames → coherent; one wildly different → incoherent., A response faster than min_response_time should be invalid., Frames with the same background should be consistent., Submitting the same frame twice should flag the second as duplicate., Create a uniform BGR dummy frame filled with *value*., Create a BGR dummy frame with slight Gaussian noise.

### Community 20 - "Community 20"
Cohesion: 0.08
Nodes (25): 📈 Current Status & Next Steps, Milestone 0: Foundation & Infrastructure (Pre-May 2026), Milestone 10: Fusion Weights Optimization (July 2026) - COMPLETED, Milestone 11: Active Identity Consistency Check (July 2026) - COMPLETED, Milestone 12: CDAC Academic Review Presentation (July 2026) - COMPLETED, Milestone 13: Flutter Web Port Stability & Layout Hardening (July 2026) - COMPLETED, Milestone 14: Quality Gate Calibration & Live Tracking Integration (July 2026) - COMPLETED, Milestone 15: Challenge Engine & UI State Synchronization (July 2026) - COMPLETED (+17 more)

### Community 21 - "Community 21"
Cohesion: 0.22
Nodes (6): _build_v1_model(), Module, Try each (path, variant) candidate in order.  Return the first that         load, Return the architecture matching *variant*., Rebuild the original 2-conv simple 1D-CNN., Sequential

### Community 22 - "Community 22"
Cohesion: 0.13
Nodes (7): ndarray, Create and register a new verification session.          :param client_id: Optio, Look up a session by its ID.          :param session_id: UUID string of the desi, Remove all expired sessions from the registry.          :return: Number of sessi, Check whether a client_id is within its rate limit.          Only sessions creat, Check whether this session has exceeded its TTL.          :return: ``True`` when, Ingest a single video frame for verification.          Performs the following in

### Community 23 - "Community 23"
Cohesion: 0.14
Nodes (10): Any, FlutterAppDelegate, FlutterImplicitEngineBridge, FlutterImplicitEngineDelegate, Bool, AppDelegate, Bool, AppDelegate (+2 more)

### Community 24 - "Community 24"
Cohesion: 0.15
Nodes (9): WebSocket endpoint for passive liveness detection (no challenge prompts).     Re, WebSocket endpoint for active challenge-response liveness streaming.     Receive, websocket_challenge(), websocket_verify_passive(), is_backend_running(), run_backend_server(), test_websocket_challenge_session_cleanup(), test_websocket_identity_mismatch() (+1 more)

### Community 25 - "Community 25"
Cohesion: 0.29
Nodes (4): ndarray, Check that the background region stays stable across stored frames.          The, Extract the background border region of a greyscale frame.          Keeps only t, Store a frame (converted to greyscale) and its timestamp.          :param frame:

### Community 26 - "Community 26"
Cohesion: 0.50
Nodes (3): ChallengeMetrics, Metrics specific to the Active Challenge-Response protocol.      Operates on a l, Calculate challenge-specific evaluation metrics.          :param challenge_resul

### Community 27 - "Community 27"
Cohesion: 0.15
Nodes (7): DateTime?, ReportGenerator, LocalDBService, Logs verification metadata to SQLite DB., Uploads a verification snapshot to local storage., Initializes SQLite DB and local storage., main()

### Community 28 - "Community 28"
Cohesion: 0.15
Nodes (12): Architecture, Datasets, graphify, Metrics, Models, Objective, Project Type, Repository Structure (+4 more)

### Community 29 - "Community 29"
Cohesion: 0.20
Nodes (10): createState, HomeScreen, _HomeScreenState, initState, main, _urlController, screens/camera_screen.dart, screens/challenge_screen.dart (+2 more)

### Community 30 - "Community 30"
Cohesion: 0.23
Nodes (9): string, wchar_t, _In_, _In_opt_, wWinMain(), CreateAndAttachConsole(), GetCommandLineArguments(), Utf8FromUtf16() (+1 more)

### Community 31 - "Community 31"
Cohesion: 0.17
Nodes (11): FUTURE RESEARCH VERSION, GEMINI_NEXT.md, IMPORTANT IMPLEMENTATION RULES, Mission, Required checks, SPRINT 1 — PIPELINE STABILIZATION, SPRINT 2 — ANTI SPOOF INTEGRATION, SPRINT 3 — rPPG UPGRADE (+3 more)

### Community 32 - "Community 32"
Cohesion: 0.17
Nodes (11): 1. Backend (Python/FastAPI), 2. Frontend (Flutter), 📊 Benchmark Scores, 🚀 Competitive Innovation, ✅ Completed (Current State), ⚙️ Installation & Setup, 🚀 Next Steps, 📋 Project Overview & Plan (+3 more)

### Community 33 - "Community 33"
Cohesion: 0.18
Nodes (10): challenge_screen.dart, ShieldApp, package:flutter/material.dart, ../providers/liveness_provider.dart, _buildPrepCard, PreVerificationScreen, StatelessWidget, build (+2 more)

### Community 34 - "Community 34"
Cohesion: 0.22
Nodes (5): Process a single frame's action-recognition result.          Call this for each, Returns the running challenge score as passed / total.          :return: Float b, Returns the full session state, suitable for WebSocket responses.          :retu, Checks whether the current challenge has exceeded its timeout.          :return:, Move to the next challenge or mark the session as complete.

### Community 35 - "Community 35"
Cohesion: 0.33
Nodes (5): package:flutter_test/flutter_test.dart, package:provider/provider.dart, package:shield_app/main.dart, package:shield_app/providers/liveness_provider.dart, main

### Community 36 - "Community 36"
Cohesion: 0.50
Nodes (3): ndarray, Extract the average green-channel value from the centre-10% crop of         *fra, Ingest one frame and return a liveness probability.

### Community 37 - "Community 37"
Cohesion: 0.28
Nodes (9): CameraScreen, _CameraScreenState, ChallengeScreen, _ChallengeScreenState, State, StatefulWidget, TickerProviderStateMixin, ChallengePrompt (+1 more)

### Community 38 - "Community 38"
Cohesion: 0.29
Nodes (4): Proof that TemporalValidator is part of the SessionManager workflow., Proof that ChallengeSession is integrated with FusionService., Proof that RPPGDetector is available in FusionService., TestAuditIntegrity

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
Cohesion: 0.20
Nodes (10): ChangeNotifier, build, MaterialPageRoute, LivenessProvider, _startStreaming, initState, _resetChallenge, _startChallenge (+2 more)

### Community 45 - "Community 45"
Cohesion: 0.22
Nodes (8): DartProject, HWND, LPARAM, LRESULT, FlutterWindow(), UINT, WPARAM, MessageHandler()

### Community 46 - "Community 46"
Cohesion: 0.33
Nodes (5): handle_new_rx_page(), __lldb_init_module(), Intercept NOTIFY_DEBUGGER_ABOUT_RX_PAGES and touch the pages., SBDebugger, SBFrame

### Community 47 - "Community 47"
Cohesion: 0.40
Nodes (4): 1. Challenge Protocol Robustness, 2. Blink Detection Benchmark, 3. Head Pose (Yaw/Pitch) Benchmark, SHIELD Benchmark Report (Synthetic Evaluation)

### Community 48 - "Community 48"
Cohesion: 0.40
Nodes (4): Conclusion, Confusion Matrix, SHIELD Benchmark Report, Summary Metrics

## Knowledge Gaps
- **306 isolated node(s):** `SBFrame`, `SBDebugger`, `flutter_export_environment.sh script`, `UIApplication`, `Any` (+301 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ChallengeSession` connect `Community 18` to `Community 34`, `Community 38`, `Community 39`, `Community 8`, `Community 16`, `Community 51`, `Community 22`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `Community 18` to `Community 38`, `Community 8`, `Community 53`, `Community 22`, `Community 24`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `QualityScoreEngine` connect `Community 5` to `Community 16`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `ChallengeSession` (e.g. with `BenchmarkEngine` and `ChallengeBenchmark`) actually correct?**
  _`ChallengeSession` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `TemporalValidator` (e.g. with `ndarray` and `SessionManager`) actually correct?**
  _`TemporalValidator` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `SessionManager` (e.g. with `ChallengeSession` and `TemporalValidator`) actually correct?**
  _`SessionManager` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `VerificationSession` (e.g. with `ChallengeSession` and `TemporalValidator`) actually correct?**
  _`VerificationSession` has 16 INFERRED edges - model-reasoned connections that need verification._