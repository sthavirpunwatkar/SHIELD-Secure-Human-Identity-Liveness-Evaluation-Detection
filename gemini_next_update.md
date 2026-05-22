# GEMINI_NEXT.md
Version: SHIELD Development Roadmap
Project: SHIELD – Secure Human Identity & Liveness Evaluation Detection

## Mission

Transform SHIELD from:

Current:
Rule-based liveness + algorithmic rPPG

Target:
Research-grade multimodal liveness platform with:
- Face quality validation
- Anti-spoof model
- Deep rPPG
- Fusion engine
- Benchmark framework
- Dataset + evaluation pipeline

Development order is mandatory:

1. Pipeline stabilization
2. Anti-spoof integration
3. Deep rPPG upgrade
4. Dataset creation
5. Benchmarking
6. Research expansion

---

# SPRINT 1 — PIPELINE STABILIZATION

Goal:
Increase reliability before introducing new models.

Current:

Camera
 → Face Detection
 → rPPG
 → Blink
 → Motion
 → Decision

Target:

Camera
 → Face Quality Gate
 → Face Detection + Tracking
 → Passive Liveness
 → Active Challenge
 → Fusion Engine
 → Decision

## Tasks

Implement:

src/
 └── quality/
      blur_detector.py
      illumination_detector.py
      pose_filter.py
      occlusion_detector.py
      quality_score.py

### Required checks

1. Blur detection
Reject blurry frames.

Methods:
- Variance of Laplacian

Output:
{
 "blur": false,
 "score": 0.89
}

---

2. Illumination check

Reject:
- overexposed
- underexposed

Output:

{
 "illumination":"good"
}

---

3. Pose validation

Reject:

yaw > threshold
pitch > threshold

Allow:
frontal / near frontal faces

---

4. Occlusion detection

Detect:
- hand
- glasses reflection
- mask
- partial face loss

---

5. Quality score

Output:

{
 "quality":0.86,
 "blur":false,
 "illumination":"good",
 "pose":"frontal"
}

Only allow inference if quality threshold passes.

Acceptance criteria:

- Stable under low light
- Stable under slight motion
- Explainable outputs available

---

# SPRINT 2 — ANTI SPOOF INTEGRATION

Goal:
Move beyond rule-only detection.

Integrate pretrained anti-spoof model.

Priority:

1. Silent Face Anti Spoofing
2. MiniFASNet
3. CDCN

Create:

src/
 └── antispoof/
      model_loader.py
      inference.py
      score_adapter.py
      preprocessing.py

Output:

{
 "antispoof_score":0.93
}

Fusion:

final_score =
0.30 * rppg +
0.20 * blink +
0.30 * antispoof +
0.20 * challenge

Deliverables:

✓ spoof score
✓ replay attack detection
✓ print attack detection

---

# SPRINT 3 — rPPG UPGRADE

Current:

ROI
 → signal extraction
 → FFT
 → pulse

Future:

Face sequence
 → EfficientPhys
 → pulse waveform
 → liveness

Investigate:

- EfficientPhys
- PhysNet
- MTTS-CAN

Folder:

src/
 └── rppg_dl/
      efficientphys/
      physnet/
      adapters/

Keep legacy rPPG pipeline active.

Run side-by-side comparison.

Benchmark:

legacy vs deep rPPG

Do NOT remove old pipeline until validated.

---

# SPRINT 4 — DATASET CREATION

Create:

dataset/

 live/
    normal/
    blink/
    speaking/
    motion/

 spoof/
    print/
    replay/
    phone_screen/
    tablet/
    mask/

Target:

50–100 subjects

Capture:

lighting:
- daylight
- indoor
- low light

devices:
- mobile
- webcam

Metadata:

subject_id
attack_type
lighting
device
fps
distance

---

# SPRINT 5 — EVALUATION

Create:

evaluation/

 benchmark.py
 metrics.py
 report_generator.py

Metrics:

Accuracy
FAR
FRR
APCER
BPCER
EER

Benchmark attacks:

1. Printed photo
2. Screen replay
3. Phone replay
4. Motion spoof
5. Mask attack

Generate automatic report.

Output:

reports/
 benchmark_report.md

---

# FUTURE RESEARCH VERSION

Target architecture:

Face
 + rPPG
 + blink
 + challenge
 + anti-spoof
 + depth
 + temporal validation

 → Fusion
 → Liveness

Roadmap:

SHIELD v1
Rules + rPPG

SHIELD v2
+ Anti-spoof
+ DL rPPG

SHIELD v3
Multimodal research platform

---

# IMPORTANT IMPLEMENTATION RULES

DO NOT:

- remove legacy pipeline
- train custom models immediately
- optimize prematurely

DO:

- benchmark every change
- preserve explainability
- keep modular design
- compare old vs new outputs
- store all metrics

Success criteria:

Accuracy > 95%
FAR < 5%
Stable under replay attacks