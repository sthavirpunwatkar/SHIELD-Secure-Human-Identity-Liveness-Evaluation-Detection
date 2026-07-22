import numpy as np
import onnxruntime as ort
from scipy.signal import butter, filtfilt

b, a = butter(2, [0.7/15.0, 4.0/15.0], btype='band')
noise = np.random.randn(150) * 0.05
sig_bandpass = filtfilt(b, a, noise)
sig_bandpass = (sig_bandpass - sig_bandpass.mean()) / (sig_bandpass.std() + 1e-6)

session = ort.InferenceSession("models/rppg_1dcnn_v2_int8.onnx", providers=['CPUExecutionProvider'])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

sig = np.expand_dims(np.expand_dims(sig_bandpass.astype(np.float32), axis=0), axis=0)
out = session.run([output_name], {input_name: sig})[0]
print(f"ONNX Output for bandpassed noise: {out[0][0]}")
