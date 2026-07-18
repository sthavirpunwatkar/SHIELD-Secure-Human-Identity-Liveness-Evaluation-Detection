import numpy as np
import onnxruntime as ort

sig = np.loadtxt("debug/model_input.csv", delimiter=",")
sig = np.expand_dims(np.expand_dims(sig, axis=0), axis=0).astype(np.float32)

session1 = ort.InferenceSession("models/rppg_1dcnn_v2.onnx", providers=['CPUExecutionProvider'])
out1 = session1.run(None, {session1.get_inputs()[0].name: sig})[0][0][0]

session2 = ort.InferenceSession("models/rppg_1dcnn_v2_int8.onnx", providers=['CPUExecutionProvider'])
out2 = session2.run(None, {session2.get_inputs()[0].name: sig})[0][0][0]

print(f"FP32 Model Score: {out1}")
print(f"INT8 Model Score: {out2}")
