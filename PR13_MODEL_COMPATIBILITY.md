# PR-013: Model Compatibility Report

## Overview
This document logs the evaluation of external pretrained weights against the SHIELD benchmark requirements.

### TS-CAN (rPPG)
**Status:** Incompatible

**Reason:**
The official pretrained weights for TS-CAN (`mtts_can.hdf5`) are provided exclusively in Keras/TensorFlow HDF5 format. The SHIELD testing environment and benchmark harness strictly rely on a PyTorch backend. Because the PR-013 constraints prohibit structural modifications to the environment or introducing major external deep learning dependencies (like TensorFlow) just for benchmark compatibility, the integration of TS-CAN has been gracefully aborted.

**Recommendation:**
Seek an alternative official PyTorch-native implementation for rPPG benchmarks (such as PhysNet or Rhythm-Mamba) or maintain TS-CAN solely as a theoretical baseline without executing its native `.hdf5` payload in this framework.

### Silent-Face-Anti-Spoofing (MiniFASNet)
**Status:** Fully Compatible

**Reason:**
The `.pth` state dictionary natively loads into the PyTorch runtime. The model was successfully downloaded along with its Python definitions, stripped of its `DataParallel` `module.` prefix dynamically, and operates seamlessly within the `MiniFASNetAdapter`.
