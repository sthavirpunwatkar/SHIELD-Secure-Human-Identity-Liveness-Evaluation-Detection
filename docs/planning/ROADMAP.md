# SHIELD Roadmap

## Version 2 (Implementation)

* **Milestone 1: Asynchronous Database Migration**
  * Target: Eliminate synchronous blocks in FastAPI.
* **Milestone 2: 3D Identity Signature Refactor**
  * Target: Implement pose-invariant identity tracking using affine transforms.
* **Milestone 3: Backend H.264 Video Decoding Integration**
  * Target: Stand up Python stream decoder (`aiortc` or FFmpeg PyAV) over WebSocket.
* **Milestone 4: Native Flutter 30 FPS Video Streaming**
  * Target: Replace `takePicture` timer with continuous WebRTC or hardware chunking.

---

## Version 3 (Enterprise Scale)

* **Milestone 5: Message Broker Integration**
  * Target: Decouple API nodes from Inference nodes using Apache Kafka or Redis Streams.
* **Milestone 6: GPU Micro-batching**
  * Target: Implement dynamic batch schedulers for YOLO and MiniFASNet to increase throughput.
* **Milestone 7: Advanced Liveness Modalities**
  * Target: Integrate Deepfake texture analysis and voice liveness.

---

## Future Production (Cloud Infrastructure)

* **Kubernetes Orchestration:** Deploy helm charts separating stateful (Redis) and stateless (FastAPI/Inference) deployments.
* **Cloud Autoscaling (KEDA):** Scale GPU inference pods horizontally based on active Kafka lag metrics.
* **Data Lake Telemetry:** Pipe non-PII inference verdicts into AWS Redshift / S3 for active model retraining pipelines.
