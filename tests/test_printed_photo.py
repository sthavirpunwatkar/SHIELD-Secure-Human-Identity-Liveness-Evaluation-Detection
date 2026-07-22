import numpy as np
import onnxruntime as ort
from scipy.signal import butter, filtfilt

# Static printed photo with very tiny camera noise
sig_raw = np.full(150, 128.0) + np.random.randn(150) * 0.001
b, a = butter(2, [0.7/15.0, 4.0/15.0], btype='band')
sig_bandpass = filtfilt(b, a, sig_raw)

sig = sig_bandpass.astype(np.float32)
sig = (sig - sig.mean()) / (sig.std() + 1e-6)

session = ort.InferenceSession("models/rppg_1dcnn_v2_int8.onnx", providers=['CPUExecutionProvider'])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

sig_in = np.expand_dims(np.expand_dims(sig, axis=0), axis=0)
out = session.run([output_name], {input_name: sig_in})[0]
print(f"ONNX Output for printed photo (tiny noise): {out[0][0]}")
