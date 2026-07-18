import matplotlib.pyplot as plt

def plot_waveform(waveform, filepath="waveform.png"):
    plt.figure(figsize=(10, 4))
    plt.plot(waveform)
    plt.title("rPPG Waveform")
    plt.xlabel("Frames")
    plt.ylabel("Amplitude")
    plt.savefig(filepath)
    plt.close()
