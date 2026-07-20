# PR-019 Root Cause Verification & Runtime Evidence Report

**Objective:** Scientifically verify the hypothesis that frontend capture FPS is causing buffer underflow or incorrect synchronization, leading to `rPPG Confidence = 0.0000`.

## Methodology
To isolate the issue from potential frontend bugs or network unpredictability, we created a localized WebSocket simulator (`tests/experiments/measure_fps_simulator.py`) to bypass the browser. 

The simulator:
1. Demuxes an H.264 video (`test.h264`, 30 FPS).
2. Sends frames perfectly spaced by exactly 33ms (simulating a stable 30 FPS frontend).
3. Connects directly to the backend `ws://127.0.0.1:8000/ws/verify`.
4. The backend was temporarily instrumented to measure the time each frame arrived at the internal processing loop.

## Runtime Data
The collected data (`frontend_fps.csv`) tracked 150 consecutive frames. We analyzed the capture timestamp (when the frame was dispatched) versus the arrival timestamp (when the backend `while True` loop received it for processing).

**Summary of FPS:**
* **Frontend Output Rate:** 150 frames over ~5.24 seconds = **28.6 FPS**.
* **Backend Processing Rate:** 150 frames over ~9.48 seconds = **15.8 FPS** (this is higher than real-world 4 FPS because our simulated face skips some heavier detections, but the bottleneck remains intact).

**Evidence of Backpressure:**
Because the backend processes frames slower than the frontend dispatches them, the internal buffer (likely OS-level TCP buffers and Python's asyncio queue) absorbs the incoming frames. This causes a constantly growing delay before a frame reaches the backend's processing logic.

* Frame 0 processing delay: ~1 ms
* Frame 50 processing delay: ~360 ms
* Frame 100 processing delay: ~3.30 seconds
* Frame 150 processing delay: **~4.24 seconds**

## Mathematical Proof
The `rPPG` model requires a temporal window of 150 consecutive frames before it computes confidence.
```python
if len(self.signal_buffer) < self.window_size: # window_size = 150
    return 0.0
```

Meanwhile, the active challenge timeouts in exactly 5.0 seconds. 

At a real-world processing speed of ~4 FPS (due to YOLO, MiniFASNet, and rPPG logic), the backend will only process:
`4 frames/sec * 5.0 seconds = 20 frames`

Even under our highly optimistic 15.8 FPS test conditions, the backend processed:
`15.8 frames/sec * 5.0 seconds = 79 frames`

In all scenarios, the backend mathematically **cannot** reach the 150th frame before the 5.0-second challenge timeout occurs. 

## The Core Bug
1. The backend does not process frames fast enough to fill the 150-frame buffer within the 5.0s window.
2. When the challenge times out, `len(self.rppg.signal_buffer) < 150`, so the `RPPGDetector` returns `0.0`.
3. The `FusionEngine` naively includes this `0.0` as a legitimate prediction rather than treating it as a "Not Ready" state.

## Conclusion
The hypothesis is **CONFIRMED**. The growing queue caused by backpressure guarantees that the rPPG buffer is never filled before the challenge expires, producing the `rPPG Confidence = 0.0000` regression. 
