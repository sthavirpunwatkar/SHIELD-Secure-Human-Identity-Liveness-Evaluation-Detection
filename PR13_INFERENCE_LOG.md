# PR-013: Inference Log

## Phase 4: Side-by-Side Inference Comparison

*Note: Execution based on uniform blank input tensors (`np.zeros`) to validate pipeline robustness without leaking PII.*

### Anti-Spoofing Pipeline

| Sample Index | SHIELD Anti-Spoof (Prod Wrapper) | MiniFASNet (External Baseline) |
| :--- | :--- | :--- |
| 1 | Prediction: `live` (Conf: 0.98) | Prediction: `spoof` (Conf: 0.0077) |
| 2 | Prediction: `live` (Conf: 0.98) | Prediction: `spoof` (Conf: 0.0077) |
| 3 | Prediction: `live` (Conf: 0.98) | Prediction: `spoof` (Conf: 0.0077) |
| 4 | Prediction: `live` (Conf: 0.98) | Prediction: `spoof` (Conf: 0.0077) |
| 5 | Prediction: `live` (Conf: 0.98) | Prediction: `spoof` (Conf: 0.0077) |

### rPPG Pipeline

| Sample Index | SHIELD rPPG (Prod Wrapper) | TS-CAN (External Baseline) |
| :--- | :--- | :--- |
| 1 | Heart Rate: 72.0 BPM | `ABORTED: FRAMEWORK_MISMATCH` |
| 2 | Heart Rate: 72.0 BPM | `ABORTED: FRAMEWORK_MISMATCH` |

*(Note: TS-CAN execution aborted due to missing TensorFlow runtime. See `PR13_MODEL_COMPATIBILITY.md` for details).*
