import numpy as np

def get_stats(filename):
    sig = np.loadtxt(filename, delimiter=',')
    mean = np.mean(sig)
    std = np.std(sig)
    min_v = np.min(sig)
    max_v = np.max(sig)
    
    # Compute FFT
    # detrend for fft
    sig_detrend = sig - np.mean(sig)
    # Hann window
    # window = np.hanning(len(sig_detrend))
    # sig_detrend = sig_detrend * window
    
    freqs = np.fft.rfftfreq(len(sig_detrend), 1.0/30.0)
    fft_mag = np.abs(np.fft.rfft(sig_detrend))
    
    # Valid pulse range (0.7 to 4.0 Hz, 42 to 240 BPM)
    valid_idx = np.where((freqs >= 0.7) & (freqs <= 4.0))[0]
    
    if len(valid_idx) > 0:
        valid_freqs = freqs[valid_idx]
        valid_mag = fft_mag[valid_idx]
        
        dom_idx = np.argmax(valid_mag)
        dom_freq = valid_freqs[dom_idx]
        est_bpm = dom_freq * 60.0
        
        peak_power = valid_mag[dom_idx] ** 2
        total_power = np.sum(valid_mag ** 2)
        snr = 10 * np.log10(peak_power / (total_power - peak_power + 1e-6))
    else:
        dom_freq = 0
        est_bpm = 0
        snr = 0
        
    print(f"--- {filename} ---")
    print(f"Mean: {mean:.4f}")
    print(f"Std : {std:.4f}")
    print(f"Min : {min_v:.4f}")
    print(f"Max : {max_v:.4f}")
    print(f"Dominant Freq: {dom_freq:.4f} Hz")
    print(f"Estimated BPM: {est_bpm:.2f}")
    print(f"SNR (dB): {snr:.4f}")
    print()

files = ["debug/raw_signal.csv", "debug/detrended_signal.csv", "debug/bandpassed_signal.csv", "debug/model_input.csv"]
for f in files:
    get_stats(f)
