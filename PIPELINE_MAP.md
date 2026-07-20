# SHIELD Inference Pipeline

Camera
↓
Frame
↓
Face Detection (YOLO/MTCNN or simulated bbox)
↓
Face Crop
↓
ROI Extraction (0.50-0.75 height, 0.60-0.80 width of face bbox)
↓
Signal Extraction (Mean Green Channel)
↓
Temporal Buffer (150 frames)
↓
Signal Detrending (Mean subtraction)
↓
Bandpass Filtering (0.7-4.0 Hz, 2nd order Butterworth)
↓
Normalization (Standardization: (sig - mean) / std)
↓
Tensor Creation (Shape: 1x1x150)
↓
ONNX/PyTorch Model Inference
↓
Raw Output (Sigmoid / Logits)
↓
RPPG Confidence Computation
↓
Fusion Engine (Combining with blink and antispoof scores)
↓
Final Decision (Live/Spoof)
