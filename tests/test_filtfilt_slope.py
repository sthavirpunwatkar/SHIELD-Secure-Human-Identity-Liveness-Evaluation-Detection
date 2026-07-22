import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

b, a = butter(2, [0.7/15.0, 4.0/15.0], btype='band')
# Signal with large slope + cardiac + noise
t = np.linspace(0, 5, 150)
cardiac = np.sin(2 * np.pi * 1.5 * t)
noise = np.random.randn(150) * 0.05
# Huge slope (e.g. user moving closer to light)
slope = np.linspace(100, 200, 150)
sig_raw = slope + cardiac + noise

sig_bandpass = filtfilt(b, a, sig_raw)

print(f"Original amplitude: {np.max(cardiac) - np.min(cardiac)}")
print(f"Filtered signal min: {np.min(sig_bandpass)}, max: {np.max(sig_bandpass)}")
