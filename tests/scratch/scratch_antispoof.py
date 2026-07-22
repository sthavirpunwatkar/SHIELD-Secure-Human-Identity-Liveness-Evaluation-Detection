import cv2
import numpy as np
from inference.antispoof.inference import AntispoofInference

inf = AntispoofInference("models/efficientnet_fas.onnx")

print("Testing with Real subject_0.jpg")
frame = cv2.imread("data/raw_mock/live/subject_0.jpg")
face_crop = cv2.resize(frame, (224, 224))
img = face_crop.astype(np.float32) / 255.0
img = np.transpose(img, (2, 0, 1))
img = np.expand_dims(img, axis=0)
outputs = inf.session.run([inf.output_name], {inf.input_name: img})[0]
print("Real Raw outputs:", outputs)

print("Testing with Spoof attack_0.jpg")
frame = cv2.imread("data/raw_mock/spoof/attack_0.jpg")
face_crop = cv2.resize(frame, (224, 224))
img = face_crop.astype(np.float32) / 255.0
img = np.transpose(img, (2, 0, 1))
img = np.expand_dims(img, axis=0)
outputs = inf.session.run([inf.output_name], {inf.input_name: img})[0]
print("Spoof Raw outputs:", outputs)
