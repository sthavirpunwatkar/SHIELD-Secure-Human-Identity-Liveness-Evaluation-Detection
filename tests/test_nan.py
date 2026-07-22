import numpy as np
import onnxruntime as ort

session = ort.InferenceSession("models/rppg_1dcnn_v2_int8.onnx", providers=['CPUExecutionProvider'])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

sig = np.full((1, 1, 150), np.nan, dtype=np.float32)
out = session.run([output_name], {input_name: sig})[0]
print(f"ONNX Output for NaN tensor: {out[0][0]}")
