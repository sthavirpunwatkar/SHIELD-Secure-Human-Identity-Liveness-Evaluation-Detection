import numpy as np
from scipy.signal import butter, filtfilt

sig_raw = np.full(150, 128.0) + np.random.randn(150) * 0.01
fps = 30.0
nyq = 0.5 * fps
b, a = butter(2, [0.7/nyq, 4.0/nyq], btype='band')

sig_bandpass = filtfilt(b, a, sig_raw)
print("Min:", sig_bandpass.min(), "Max:", sig_bandpass.max())
print("Mean:", sig_bandpass.mean(), "Std:", sig_bandpass.std())
