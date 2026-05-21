# Graph Report - project  (2026-05-21)

## Corpus Check
- 93 files · ~35,807 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 354 nodes · 399 edges · 17 communities detected
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 85 edges (avg confidence: 0.75)
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

## God Nodes (most connected - your core abstractions)
1. `main()` - 10 edges
2. `RPPGDetector` - 10 edges
3. `FaceDetector` - 9 edges
4. `FusionService` - 8 edges
5. `AppDelegate` - 8 edges
6. `WriteValue()` - 8 edges
7. `Create()` - 8 edges
8. `BehavioralAnalyzer` - 8 edges
9. `LivenessClassifier` - 8 edges
10. `MiniFASNet` - 8 edges

## Surprising Connections (you probably didn't know these)
- `OnCreate()` --calls--> `SetNextFrameCallback()`  [INFERRED]
  frontend\windows\runner\flutter_window.cpp → frontend\windows\flutter\ephemeral\cpp_client_wrapper\flutter_engine.cc
- `OnCreate()` --calls--> `ForceRedraw()`  [INFERRED]
  frontend\windows\runner\flutter_window.cpp → frontend\windows\flutter\ephemeral\cpp_client_wrapper\flutter_view_controller.cc
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
Nodes (22): Initializes the EfficientNet-B0 liveness classifier.         :param model_path:, flutter(), flutter(), Resize(), SetMethodCallHandler(), DecodeAndProcessResponseEnvelope(), flutter(), DecodeAndProcessResponseEnvelopeInternal() (+14 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (16): FlutterEngine(), GetRegistrarForPlugin(), RelinquishEngine(), ReloadSystemFonts(), SetNextFrameCallback(), ShutDown(), FlutterViewController(), ForceRedraw() (+8 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (23): OnCreate(), wWinMain(), CreateAndAttachConsole(), GetCommandLineArguments(), Utf8FromUtf16(), Create(), Destroy(), EnableFullDpiSupportIfAvailable() (+15 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (9): ResizeChannel(), SendResponseData(), SetChannelWarnsOnOverflow(), flutter(), SetWarnsOnOverflow(), ClearPlugins(), GetInstance(), OnRegistrarDestroyed() (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (8): FirebaseService, Logs verification metadata to Firestore., Uploads a verification snapshot to Firebase Storage., Initializes Firebase Admin SDK with placeholders., WebSocket endpoint for real-time liveness streaming.     Receives binary image, Receives an image frame and runs the SHIELD liveness detection pipeline., verify_liveness(), websocket_verify()

### Community 8 - "Community 8"
Cohesion: 0.14
Nodes (6): dispose, fl_register_plugins(), main(), my_application_activate(), my_application_dispose(), my_application_new()

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (7): flutter(), Send(), SetMessageHandler(), flutter(), test_websocket_send_invalid_data(), test_websocket_send_valid_image(), test_websocket_stress()

### Community 10 - "Community 10"
Cohesion: 0.22
Nodes (3): AppDelegate, FlutterAppDelegate, FlutterImplicitEngineDelegate

### Community 11 - "Community 11"
Cohesion: 0.4
Nodes (2): GeneratedPluginRegistrant, -registerWithRegistry

### Community 12 - "Community 12"
Cohesion: 0.4
Nodes (2): RunnerTests, XCTestCase

### Community 13 - "Community 13"
Cohesion: 0.5
Nodes (2): handle_new_rx_page(), Intercept NOTIFY_DEBUGGER_ABOUT_RX_PAGES and touch the pages.

### Community 14 - "Community 14"
Cohesion: 0.67
Nodes (2): FlutterSceneDelegate, SceneDelegate

### Community 15 - "Community 15"
Cohesion: 0.67
Nodes (2): LivenessDetails, LivenessResult

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): MainActivity

## Knowledge Gaps
- **74 isolated node(s):** `WebSocket endpoint for real-time liveness streaming.     Receives binary image`, `Receives an image frame and runs the SHIELD liveness detection pipeline.`, `Initializes Firebase Admin SDK with placeholders.`, `Logs verification metadata to Firestore.`, `Uploads a verification snapshot to Firebase Storage.` (+69 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 11`** (5 nodes): `GeneratedPluginRegistrant.java`, `GeneratedPluginRegistrant.m`, `GeneratedPluginRegistrant`, `.registerWith()`, `-registerWithRegistry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (5 nodes): `RunnerTests.swift`, `RunnerTests.swift`, `RunnerTests`, `.testExample()`, `XCTestCase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (4 nodes): `handle_new_rx_page()`, `__lldb_init_module()`, `Intercept NOTIFY_DEBUGGER_ABOUT_RX_PAGES and touch the pages.`, `flutter_lldb_helper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (3 nodes): `FlutterSceneDelegate`, `SceneDelegate.swift`, `SceneDelegate`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (3 nodes): `LivenessDetails`, `LivenessResult`, `liveness_result.dart`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (2 nodes): `MainActivity.kt`, `MainActivity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GetInstance()` connect `Community 6` to `Community 5`?**
  _High betweenness centrality (0.259) - this node is a cross-community bridge._
- **Why does `OnCreate()` connect `Community 5` to `Community 4`?**
  _High betweenness centrality (0.257) - this node is a cross-community bridge._
- **Why does `Resize()` connect `Community 3` to `Community 0`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.249) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `main()` (e.g. with `FaceDetector` and `LivenessClassifier`) actually correct?**
  _`main()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `RPPGDetector` (e.g. with `FusionService` and `Initializes all core AI models for orchestration.`) actually correct?**
  _`RPPGDetector` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `FaceDetector` (e.g. with `FusionService` and `Initializes all core AI models for orchestration.`) actually correct?**
  _`FaceDetector` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `FusionService` (e.g. with `FaceDetector` and `LivenessClassifier`) actually correct?**
  _`FusionService` has 5 INFERRED edges - model-reasoned connections that need verification._