# PR-015: Preprocessing Parity Report

## MiniFASNet Parity
- **Face Crop:** Matches the original paper's MTCNN-based crop.
- **Crop Expansion:** Matches the original scale parameter `2.7`.
- **RGB/BGR Conversion:** The model expects BGR. Our harness correctly feeds BGR via OpenCV conventions.
- **Normalization:** MinMax/mean normalization matching the `transform.py` of the official implementation.
- **Resize:** Forced `80x80` alignment.
- **Tensor Layout:** `NCHW` implemented natively.

## PhysNet Parity
- **Face ROI:** Tracks the core facial bounding box.
- **Temporal Window:** `32` frames matching `rPPG-Toolbox` standard depth.
- **Frame Ordering:** Chronological queue.
- **Normalization:** Subtract mean and divide by standard deviation per frame.
- **Tensor Layout:** `(Batch, Channels, Time, Height, Width)` properly matched `(1, 3, 32, 128, 128)`.
- **Resize:** `128x128` aligned with the standard PhysNet definition.
