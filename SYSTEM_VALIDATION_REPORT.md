# SYSTEM VALIDATION REPORT

## Section A: Engineering Validation

The following engineering components of the SHIELD pipeline have been directly verified through runtime testing and backend log analysis:

- **WebCodecs encoding:** Successfully captures and encodes webcam frames in the browser.
- **H264 Annex-B generation:** Successfully formats encoded chunks for transmission.
- **WebSocket synchronization:** Successfully transmits and receives binary video chunks alongside text metadata in real-time.
- **Backend packet ordering:** Successfully receives and buffers packets for decoding.
- **PyAV decoding:** Successfully decodes H264 chunks back into raw frames.
- **Face detection:** Successfully detects faces (e.g., MediaPipe/YOLO execution).
- **ROI extraction:** Successfully extracts bounding boxes (e.g., `[254, 192, 377, 351]`).
- **Behavioral inference:** Successfully computes facial landmarks and head pose (yaw, pitch, roll).
- **Anti-spoof inference:** Successfully runs the spatial anti-spoof model and returns a confidence score.
- **rPPG inference:** Successfully buffers 150 frames, applies signal detrending and Butterworth bandpass filtering (when `scipy` is available), and computes an ONNX confidence score.
- **Fusion execution:** Successfully combines Anti-Spoof and rPPG scores using configured weights to produce a final verdict.

*The engineering pipeline is verified. The machine-learning performance has NOT yet been benchmarked against standardized datasets.*

## Section B: Known ML Issues

The following items have been observed during initial engineering smoke tests:

- **Live users occasionally classified as Spoof:** Missing dependencies (like `scipy`) previously caused rPPG scores to default to near zero.
- **rPPG confidence variation:** During manual testing, rPPG confidence varied during head movement. The cause has not yet been experimentally isolated.
- **Replay attacks not characterized:** The system's response to video replay attacks was observed during manual tests, but interactions between spatial Anti-Spoofing and rPPG for these attacks have not been formally quantified.
- **Threshold calibration:** The current fusion thresholds have not yet been calibrated using benchmark datasets.
- **Active challenge requires validation:** The challenge component of the fusion mechanism currently defaults to `0.0` and remains untested.

## Out of Scope

This validation does not establish:

- Detection accuracy
- APCER
- BPCER
- ACER
- ROC/AUC
- Equal Error Rate (EER)
- Generalization across cameras
- Robustness to replay attacks
- Robustness to masks
- Robustness to presentation attacks

These evaluations are reserved for PR-010 Model Calibration.

## TODO: PR-010 Model Calibration

- [ ] Benchmark on SiW
- [ ] Benchmark on CASIA-FASD
- [ ] Benchmark on Replay-Attack
- [ ] Benchmark on UBFC-rPPG
- [ ] Tune fusion thresholds
- [ ] Evaluate ROC/EER
- [ ] Retrain only if benchmark results justify it
