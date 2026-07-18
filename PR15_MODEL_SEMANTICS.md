# PR-015: Model Semantics Report

## MiniFASNet
- **Output Shape:** `(1, 3)`
- **Class Index Meaning:** 
  - `Index 0`: Presentation Attack (Spoof)
  - `Index 1`: Live Face (Real)
  - `Index 2`: Presentation Attack (Spoof)
- **Decoding Strategy:** We extract the probability of `Index 1` after applying a Softmax activation over the logits. This provides a bounded `[0, 1]` confidence score mapping perfectly to SHIELD's `live` probability requirement.

## PhysNet
- **Output Shape:** `(1, 8)` (from a 32-frame temporal input)
- **Meaning:** The model behaves as a spatio-temporal encoder. The temporal dimension is reduced by a factor of 4 via max pooling. The output is an 8-frame latent raw rPPG waveform segment.
- **Decoding Strategy:** We return the raw wave array instead of enforcing an arbitrary BPM metric. BPM extraction typically requires a longer sequence (e.g., 250 frames) and peak detection or FFT. By returning the raw wave, we maintain scientific fidelity to the checkpoint's capabilities.
