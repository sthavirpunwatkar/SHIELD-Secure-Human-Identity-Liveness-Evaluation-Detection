import cv2
import numpy as np
from inference.antispoof.inference import AntispoofInference

inf = AntispoofInference("models/efficientnet_fas.onnx")

# Create dummy image
dummy = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8).astype(np.float32) / 255.0
dummy = np.transpose(dummy, (2, 0, 1))
dummy = np.expand_dims(dummy, axis=0)

outputs = inf.session.run([inf.output_name], {inf.input_name: dummy})[0]
print("Raw outputs:", outputs)
