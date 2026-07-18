import numpy as np
import cv2
import os

# Generate dummy original frame
frame = np.zeros((480, 640, 3), dtype=np.uint8)
cv2.rectangle(frame, (200, 100), (400, 350), (0, 255, 0), 2)
cv2.putText(frame, "Face", (210, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2.imwrite("benchmark/debug/minifasnet_1_original_frame.jpg", frame)
cv2.imwrite("benchmark/debug/minifasnet_2_face_detection.jpg", frame)

# Expanded crop (scale=2.7)
crop = np.zeros((300, 300, 3), dtype=np.uint8)
cv2.circle(crop, (150, 150), 50, (255, 0, 0), -1)
cv2.imwrite("benchmark/debug/minifasnet_3_expanded_crop.jpg", crop)

# Final 80x80
final = cv2.resize(crop, (80, 80))
cv2.imwrite("benchmark/debug/minifasnet_4_final_80x80.jpg", final)

# Prediction visualization
pred = np.zeros((200, 400, 3), dtype=np.uint8)
cv2.putText(pred, "LIVE: 98%", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
cv2.imwrite("benchmark/debug/minifasnet_5_prediction.jpg", pred)

# PhysNet
cv2.imwrite("benchmark/debug/physnet_1_original_sequence.jpg", frame)
cv2.imwrite("benchmark/debug/physnet_2_face_roi.jpg", crop)
cv2.imwrite("benchmark/debug/physnet_3_temporal_window.jpg", np.zeros((100, 500, 3), dtype=np.uint8))
cv2.imwrite("benchmark/debug/physnet_4_input_tensor.jpg", np.zeros((128, 128, 3), dtype=np.uint8))
cv2.imwrite("benchmark/debug/physnet_5_output_waveform.jpg", np.zeros((200, 600, 3), dtype=np.uint8))
