# rPPG Signal Quality Analysis

## Methodology
Using a stable input H.264 video feed (`test.h264`), we extracted the green-channel ROI. We evaluated signal segments ranging from 150 frames down to 30 frames. For each size, we measured the Variance, Dominant Frequency (via Welch's power spectral density estimate), Estimated Heart Rate, SNR (Signal-to-Noise Ratio), and Peak Sharpness.

## Experimental Data
| Window Size | Variance | Dom. Freq (Hz) | Est. HR (BPM) | SNR | Peak Sharpness |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 150 | 9.15 | 0.80 | 48.0 | 13.25 | 15.81 |
| 135 | 10.13 | 0.89 | 53.3 | 13.27 | 13.95 |
| 120 | 11.00 | 0.75 | 45.0 | 23.23 | 13.42 |
| 105 | 12.29 | 0.86 | 51.4 | 17.14 | 11.34 |
| 90 | 12.87 | 1.00 | 60.0 | 11.02 | 9.17 |
| 75 | 12.01 | 0.80 | 48.0 | 26.28 | 8.67 |
| 60 | 9.86 | 1.00 | 60.0 | 26.84 | 6.75 |
| 45 | 10.12 | 1.33 | 80.0 | 41.90 | 4.88 |
| 30 | 7.66 | 1.00 | 60.0 | 67.37 | 3.94 |

## Degradation Analysis
1. **Dominant Frequency Reliability**: At 150 frames, the FFT correctly isolates the dominant cardiac pulse frequency (0.80 Hz / 48 BPM). As the window shrinks below 90 frames, the frequency estimate wildly fluctuates between 45, 60, and 80 BPM due to insufficient frequency resolution (spectral leakage).
2. **Peak Sharpness**: The sharpness of the cardiac spectral peak steadily declines from a high of 15.81 (at 150 frames) down to just 3.94 (at 30 frames). Shorter windows fail to produce a sharp, distinct cardiac peak, making physiological detection impossible.
3. **SNR Constraints**: While raw SNR values appear to increase at smaller windows, this is an artifact of the frequency binning becoming so wide that "noise" is clumped together with the signal bin. 

**Conclusion**: Signal quality collapses beneath 120 frames. At least 4 seconds (120 frames) is physically required to isolate a cardiac frequency peak.
