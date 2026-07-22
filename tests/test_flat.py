import numpy as np
from scipy.signal import butter, filtfilt

b, a = butter(2, [0.7/15.0, 4.0/15.0], btype='band')
x = np.full(150, 128.0)
y = filtfilt(b, a, x)
print(y.min(), y.max(), y.mean(), y.std())
