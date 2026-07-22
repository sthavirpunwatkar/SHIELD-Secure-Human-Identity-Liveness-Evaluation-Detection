# SHIELD Architecture - Module Inventory

## Frontend Components (Flutter)
| Component | Purpose | Location |
|-----------|---------|----------|
| `camera_screen.dart` | Renders camera preview, handles user UI for passive liveness. | `frontend/lib/screens/` |
| `challenge_screen.dart` | Manages the UI and countdown timers for active challenge sessions. | `frontend/lib/screens/` |
| `pre_verification_screen.dart` | Starting point for validation sessions. | `frontend/lib/screens/` |
| `ChallengeService` | Handles challenge lifecycle, server messages, and countdown states. | `frontend/lib/services/challenge_service.dart` |
| `FrameTransportService` | Transports frames to backend, handles backpressure/queuing. | `frontend/lib/services/frame_transport_service.dart` |
| `CameraCaptureService` | Captures camera frames and generates the stream. | `frontend/lib/services/camera_capture_service.dart` |

## Backend Components (FastAPI)
| Component | Purpose | Location |
|-----------|---------|----------|
| `main.py` | Application entry point, WebSocket routers (`/ws/challenge`, `/ws/verify`). | `backend/main.py` |
| `SessionManager` | Manages active verification sessions and aggregates challenge states. | `inference/session_manager.py` |
| `StreamingDecoder` | H.264 video decoding from binary WebSocket chunks. | `backend/services/video_decoder.py` |
| `FusionService` | Core orchestrator for the pipeline processing of a single frame. | `backend/services/fusion_service.py` |
| `LocalDBService` | Stores metadata and image references into SQLite. | `backend/services/db_service.py` |

## AI / Inference Modules
| Component | Purpose | Location |
|-----------|---------|----------|
| `YoloSegDetector` | Detects faces and masks using YOLOv8-seg, extracts ROIs. | `inference/yolo_detector.py` |
| `QualityScoreEngine` | Evaluates facial capture quality (lighting, blur, etc.). | `inference/quality/` |
| `BehavioralAnalyzer` | Uses landmarks to detect blinks, head turns, and validates challenge actions. | `inference/behavioral_analyzer.py` |
| `AntispoofInference` | Defends against printed/digital spoofs (MiniFASNet). | `inference/antispoof/inference.py` |
| `RPPGDetector` | Extracts physiological signals (Heart Rate) via rPPG. | `inference/rppg_detector.py` |
| `FusionEngine` | Weights and fuses all model confidence scores into a final boolean verdict. | `inference/fusion_engine.py` |

## AI Models
| File Name | Purpose | Location |
|-----------|---------|----------|
| `yolov8n-seg.pt` | YOLOv8 nano model fine-tuned for face segmentation/mask spoofing. | `models/` |
| `minifas_antispoof_v2.onnx` | MiniFASNet for appearance-based liveness. | `models/` |
| `rppg_1dcnn_v2.onnx` | 1D CNN for Remote Photoplethysmography signal classification. | `models/` |
| `face_landmarker.task` | MediaPipe face landmarking task file. | `models/` |
| `efficientnet_fas.onnx` | General face antispoofing model. | `models/` |

## Configuration & Databases
| File / Component | Purpose | Location |
|------------------|---------|----------|
| `shield_local.db` | SQLite database storing all verification session outcomes. | `backend/shield_local.db` |
| `.env` / Environment | Debug mode, demo mode toggles. | Configured via env variables |
