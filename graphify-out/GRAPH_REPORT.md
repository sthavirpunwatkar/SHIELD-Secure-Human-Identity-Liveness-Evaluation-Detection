# Graph Report - project  (2026-05-21)

## Corpus Check
- 96 files · ~36,982 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 368 nodes · 413 edges · 19 communities detected
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 87 edges (avg confidence: 0.74)
- Token cost: 0 input · 0 output

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
- [[_COMMUNITY_Community 19|Community 19]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 10 edges
2. `MiniFASNet` - 10 edges
3. `RPPGDetector` - 10 edges
4. `FaceDetector` - 9 edges
5. `FusionService` - 8 edges
6. `AppDelegate` - 8 edges
7. `WriteValue()` - 8 edges
8. `Create()` - 8 edges
9. `BehavioralAnalyzer` - 8 edges
10. `LivenessClassifier` - 8 edges

## Surprising Connections (you probably didn't know these)
- `ForceRedraw()` --calls--> `OnCreate()`  [INFERRED]
  frontend\windows\flutter\ephemeral\cpp_client_wrapper\flutter_view_controller.cc → frontend\windows\runner\flutter_window.cpp
- `train()` --calls--> `MiniFASNet`  [INFERRED]
  training\train_minifas.py → inference\minifas_net.py
- `test_websocket_send_invalid_data()` --calls--> `Send()`  [INFERRED]
  test_backend.py → frontend\windows\flutter\ephemeral\cpp_client_wrapper\core_implementations.cc
- `test_websocket_send_valid_image()` --calls--> `Send()`  [INFERRED]
  test_backend.py → frontend\windows\flutter\ephemeral\cpp_client_wrapper\core_implementations.cc
- `test_websocket_stress()` --calls--> `Send()`  [INFERRED]
  test_backend.py → frontend\windows\flutter\ephemeral\cpp_client_wrapper\core_implementations.cc

## Communities

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (22): BehavioralAnalyzer, Initializes Behavioral analysis. Falls back to simple heuristics if MediaPipe fa, Analyzes motion, blinks, and head turns., FaceDetector, Detects faces in a given frame.         :param frame: OpenCV image (BGR)., Crops a face from the frame based on a bounding box.         :param frame: Open, Initializes the YOLOv8 face detector.         :param model_path: Path to the YO, FusionService (+14 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (28): dispose, LivenessProvider, sendFrame, setServerUrl, build, CameraScreen, _CameraScreenState, dispose (+20 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (28): build, HomeScreen, _HomeScreenState, Icon, initState, main, MaterialApp, Scaffold (+20 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (23): SetChannelWarnsOnOverflow(), Initializes the EfficientNet-B0 liveness classifier.         :param model_path:, flutter(), flutter(), Resize(), SetWarnsOnOverflow(), DecodeAndProcessResponseEnvelope(), flutter() (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (24): SetNextFrameCallback(), OnCreate(), wWinMain(), CreateAndAttachConsole(), GetCommandLineArguments(), Utf8FromUtf16(), Create(), Destroy() (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (14): FlutterEngine(), GetRegistrarForPlugin(), RelinquishEngine(), ReloadSystemFonts(), ShutDown(), FlutterViewController(), ForceRedraw(), HandleTopLevelWindowProc() (+6 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (10): flutter(), Send(), SendResponseData(), SetMessageHandler(), flutter(), flutter(), SetMethodCallHandler(), test_websocket_send_invalid_data() (+2 more)

### Community 7 - "Community 7"
Cohesion: 0.13
Nodes (7): dispose, fl_register_plugins(), main(), my_application_activate(), my_application_dispose(), my_application_new(), my_application_shutdown()

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (8): FirebaseService, Logs verification metadata to Firestore., Uploads a verification snapshot to Firebase Storage., Initializes Firebase Admin SDK with placeholders., WebSocket endpoint for real-time liveness streaming.     Receives binary image, Receives an image frame and runs the SHIELD liveness detection pipeline., verify_liveness(), websocket_verify()

### Community 9 - "Community 9"
Cohesion: 0.22
Nodes (3): AppDelegate, FlutterAppDelegate, FlutterImplicitEngineDelegate

### Community 10 - "Community 10"
Cohesion: 0.32
Nodes (5): ResizeChannel(), ClearPlugins(), GetInstance(), OnRegistrarDestroyed(), PluginRegistrar()

### Community 11 - "Community 11"
Cohesion: 0.29
Nodes (3): Dataset, FASDataset, train()

### Community 12 - "Community 12"
Cohesion: 0.4
Nodes (2): GeneratedPluginRegistrant, -registerWithRegistry

### Community 13 - "Community 13"
Cohesion: 0.4
Nodes (2): RunnerTests, XCTestCase

### Community 14 - "Community 14"
Cohesion: 0.5
Nodes (2): RPPG1DCNN, train_rppg()

### Community 15 - "Community 15"
Cohesion: 0.5
Nodes (2): handle_new_rx_page(), Intercept NOTIFY_DEBUGGER_ABOUT_RX_PAGES and touch the pages.

### Community 16 - "Community 16"
Cohesion: 0.67
Nodes (2): FlutterSceneDelegate, SceneDelegate

### Community 17 - "Community 17"
Cohesion: 0.67
Nodes (2): LivenessDetails, LivenessResult

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): MainActivity

## Knowledge Gaps
- **74 isolated node(s):** `WebSocket endpoint for real-time liveness streaming.     Receives binary image`, `Receives an image frame and runs the SHIELD liveness detection pipeline.`, `Initializes Firebase Admin SDK with placeholders.`, `Logs verification metadata to Firestore.`, `Uploads a verification snapshot to Firebase Storage.` (+69 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 12`** (5 nodes): `GeneratedPluginRegistrant.java`, `GeneratedPluginRegistrant.m`, `GeneratedPluginRegistrant`, `.registerWith()`, `-registerWithRegistry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (5 nodes): `RunnerTests.swift`, `RunnerTests.swift`, `RunnerTests`, `.testExample()`, `XCTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (5 nodes): `RPPG1DCNN`, `.forward()`, `.__init__()`, `train_rppg()`, `train_rppg.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (4 nodes): `handle_new_rx_page()`, `__lldb_init_module()`, `Intercept NOTIFY_DEBUGGER_ABOUT_RX_PAGES and touch the pages.`, `flutter_lldb_helper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (3 nodes): `FlutterSceneDelegate`, `SceneDelegate.swift`, `SceneDelegate`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (3 nodes): `LivenessDetails`, `LivenessResult`, `liveness_result.dart`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (2 nodes): `MainActivity.kt`, `MainActivity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GetInstance()` connect `Community 10` to `Community 3`, `Community 4`?**
  _High betweenness centrality (0.254) - this node is a cross-community bridge._
- **Why does `Resize()` connect `Community 3` to `Community 0`, `Community 10`, `Community 4`?**
  _High betweenness centrality (0.251) - this node is a cross-community bridge._
- **Why does `OnCreate()` connect `Community 4` to `Community 5`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `main()` (e.g. with `FaceDetector` and `LivenessClassifier`) actually correct?**
  _`main()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `MiniFASNet` (e.g. with `FusionService` and `Initializes all core AI models for orchestration.`) actually correct?**
  _`MiniFASNet` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `RPPGDetector` (e.g. with `FusionService` and `Initializes all core AI models for orchestration.`) actually correct?**
  _`RPPGDetector` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `FaceDetector` (e.g. with `FusionService` and `Initializes all core AI models for orchestration.`) actually correct?**
  _`FaceDetector` has 5 INFERRED edges - model-reasoned connections that need verification._