# PR-011: External Models Download Guide

> **IMPORTANT:** In accordance with PR-011 constraints, NO models should be downloaded automatically by the SHIELD core pipeline, and no weights should be checked into the repository. 

This guide serves as a manual instruction set for developers running the benchmark harness locally.

## Model 1: Silent-Face-Anti-Spoofing (MiniFASNet)

**Location:** 
[minivision-ai/Silent-Face-Anti-Spoofing](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing)

**Instructions:**
1. Navigate to the `resources/anti_spoof_models` directory in the official repository.
2. Locate the pretrained `.pth` files. The primary model to download is `2.7_80x80_MiniFASNetV2.pth`.
3. Download the file locally.
4. Place the weights inside your local benchmark directory: 
   `SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/tests/benchmarks/weights/minifasnet/2.7_80x80_MiniFASNetV2.pth`
5. Do **not** commit this file to git. Ensure it is covered by `.gitignore`.

## Model 2: TS-CAN

**Location:**
[xin71/MTTS-CAN](https://github.com/xin71/MTTS-CAN) or via the [rPPG-Toolbox](https://github.com/ubicomplab/rPPG-Toolbox)

**Instructions:**
1. Navigate to the rPPG-Toolbox repository.
2. Locate the model weights link in their README under the TS-CAN section.
3. Download the TS-CAN PyTorch `.pth` checkpoint (e.g., weights trained on UBFC-rPPG).
4. Place the weights inside your local benchmark directory:
   `SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/tests/benchmarks/weights/tscan/tscan_ubfc.pth`
5. Do **not** commit this file to git. Ensure it is covered by `.gitignore`.

---
*Note: The benchmark harness will gracefully skip these external models if the weights are not found at the designated paths.*
