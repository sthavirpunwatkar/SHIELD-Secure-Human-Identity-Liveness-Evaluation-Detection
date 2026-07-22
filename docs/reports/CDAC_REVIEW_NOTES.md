# CDAC Reviewer Notes

## Architectural Design Decisions & Trade-offs
The SHIELD V2 architecture was systematically designed to decouple complex domain concerns into strict, isolated abstractions.

**Why FrameEncoder exists:**
Encoding raw YUV420 to H.264 in pure Dart is computationally impossible for real-time mobile pipelines. By strictly defining the `FrameEncoder` interface, we successfully decoupled the business logic (Transport) from the platform-specific hardware acceleration constraints (JNI/Swift).

**Why backend already supports streaming:**
The `StreamingDecoder` (PyAV) was finalized immediately to establish a concrete, immutable contract. The backend demands H.264 Annex B chunks. Because this contract is immutable, backend and AI engineers can iterate on the Fusion pipeline without waiting for iOS/Android native engineers to finalize hardware acceleration.

**Why a native encoder is platform-specific and separated:**
Writing memory-safe native JNI buffers for Android `MediaCodec` and Swift wrappers for Apple `VideoToolbox` is an entirely distinct engineering domain (Systems Engineering) from Flutter UI or Python AI development. This was intentionally designated as a separate engineering Epic (V3 Roadmap) to isolate risk.

**Why this separation improves maintainability:**
Future engineers tasked with implementing the native encoder are constrained *only* by the `FrameEncoder` interface. They do not need to understand WebSockets, FastAPI, MediaPipe, or the Fusion Pipeline. They simply receive `CameraImage` bytes and emit H.264 bytes. This guarantees strict architectural integrity and massively accelerates onboarding.
