import time
import numpy as np
import cv2
import psutil
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
from inference.rppg_detector import RPPGDetector

def benchmark():
    rppg = RPPGDetector(window_size=150)
    # create a dummy frame
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    times = []
    process = psutil.Process(os.getpid())
    mem_start = process.memory_info().rss / (1024 * 1024)
    
    print("Starting 10-minute long run test (simulated 30fps = 18000 frames)...")
    
    for i in range(18000):
        start = time.perf_counter()
        # just do the update
        rppg.update(frame, bbox=[100, 100, 300, 300])
        times.append((time.perf_counter() - start) * 1000)
        
    mem_end = process.memory_info().rss / (1024 * 1024)
    
    times = np.array(times)
    
    print("--- Performance Benchmarks ---")
    print(f"Average latency: {np.mean(times):.4f} ms")
    print(f"95th percentile latency: {np.percentile(times, 95):.4f} ms")
    print(f"Maximum latency: {np.max(times):.4f} ms")
    print(f"Buffer growth: {len(rppg.signal_buffer)} elements (Expected 150)")
    print(f"Memory start: {mem_start:.2f} MB, Memory end: {mem_end:.2f} MB")
    
if __name__ == '__main__':
    benchmark()
