# Graph Report - project  (2026-05-21)

## Corpus Check
- 10 files · ~2,458 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 61 nodes · 92 edges · 7 communities detected
- Extraction: 59% EXTRACTED · 41% INFERRED · 0% AMBIGUOUS · INFERRED: 38 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 10 edges
2. `RPPGDetector` - 10 edges
3. `FaceDetector` - 9 edges
4. `FusionService` - 8 edges
5. `BehavioralAnalyzer` - 8 edges
6. `LivenessClassifier` - 8 edges
7. `MiniFASNet` - 8 edges
8. `Initializes all core AI models for orchestration.` - 6 edges
9. `Runs the multi-modal pipeline on a single frame.         :param frame: OpenCV i` - 6 edges
10. `verify_liveness()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `FaceDetector`  [INFERRED]
  test_inference.py → inference\face_detector.py
- `main()` --calls--> `LivenessClassifier`  [INFERRED]
  test_inference.py → inference\liveness_classifier.py
- `main()` --calls--> `BehavioralAnalyzer`  [INFERRED]
  test_inference.py → inference\behavioral_analyzer.py
- `main()` --calls--> `RPPGDetector`  [INFERRED]
  test_inference.py → inference\rppg_detector.py
- `FusionService` --uses--> `LivenessClassifier`  [INFERRED]
  backend\services\fusion_service.py → inference\liveness_classifier.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.23
Nodes (6): BehavioralAnalyzer, Fallback Behavioral Analyzer using simple heuristics.         Note: MediaPipe w, FaceDetector, Initializes the YOLOv8 face detector.         :param model_path: Path to the YO, FusionService, Initializes all core AI models for orchestration.

### Community 1 - "Community 1"
Cohesion: 0.22
Nodes (6): FirebaseService, Logs verification metadata to Firestore., Uploads a verification snapshot to Firebase Storage., Initializes Firebase Admin SDK with placeholders., Receives an image frame and runs the SHIELD liveness detection pipeline., verify_liveness()

### Community 2 - "Community 2"
Cohesion: 0.24
Nodes (5): Builds a simple 1D CNN for pulse signal classification., Extracts the average green channel value from skin ROIs (forehead/cheeks)., Updates the buffer and returns a liveness score if the window is full., Initializes the rPPG detector.         :param window_size: Number of frames to, RPPGDetector

### Community 3 - "Community 3"
Cohesion: 0.25
Nodes (4): Analyzes the frame for behavioral cues.         :param frame: OpenCV image (BGR, Detects faces in a given frame.         :param frame: OpenCV image (BGR)., Crops a face from the frame based on a bounding box.         :param frame: Open, main()

### Community 4 - "Community 4"
Cohesion: 0.29
Nodes (4): MiniFASNet, Builds a lightweight CNN skeleton for MiniFASNet., Predicts the liveness score for a given face crop.         :param face_crop: Op, Initializes the MiniFASNet anti-spoofing model.         :param model_path: Path

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (3): Runs the multi-modal pipeline on a single frame.         :param frame: OpenCV i, WebSocket endpoint for real-time liveness streaming.     Receives binary image, websocket_verify()

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (3): LivenessClassifier, Predicts if the face crop is Live or Spoof.         :param face_crop: OpenCV im, Initializes the EfficientNet-B0 liveness classifier.         :param model_path:

## Knowledge Gaps
- **19 isolated node(s):** `WebSocket endpoint for real-time liveness streaming.     Receives binary image`, `Receives an image frame and runs the SHIELD liveness detection pipeline.`, `Initializes Firebase Admin SDK with placeholders.`, `Logs verification metadata to Firestore.`, `Uploads a verification snapshot to Firebase Storage.` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `verify_liveness()` connect `Community 1` to `Community 5`?**
  _High betweenness centrality (0.286) - this node is a cross-community bridge._
- **Why does `RPPGDetector` connect `Community 2` to `Community 0`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.196) - this node is a cross-community bridge._
- **Why does `FusionService` connect `Community 0` to `Community 2`, `Community 4`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `main()` (e.g. with `FaceDetector` and `LivenessClassifier`) actually correct?**
  _`main()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `RPPGDetector` (e.g. with `FusionService` and `Initializes all core AI models for orchestration.`) actually correct?**
  _`RPPGDetector` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `FaceDetector` (e.g. with `FusionService` and `Initializes all core AI models for orchestration.`) actually correct?**
  _`FaceDetector` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `FusionService` (e.g. with `FaceDetector` and `LivenessClassifier`) actually correct?**
  _`FusionService` has 5 INFERRED edges - model-reasoned connections that need verification._