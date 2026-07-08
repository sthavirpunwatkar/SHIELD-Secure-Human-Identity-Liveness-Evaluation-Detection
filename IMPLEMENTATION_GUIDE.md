# SHIELD V2 Implementation Guide

## Implementation Order
1. Milestone 1: Async DB
2. Milestone 2: Identity Signature
3. Milestone 4: Frontend Stream
4. Milestone 3: Backend Stream Decode

---

## Milestone 1: Asynchronous Database Migration
* **Objective:** Remove event-loop blocking by migrating from synchronous `sqlite3` to an asynchronous driver (`aiosqlite` or `asyncpg`).
* **Files expected to change:** `backend/services/db_service.py`, `backend/main.py`.
* **Dependencies:** None.
* **Expected risks:** Data loss during migration, unhandled `await` coroutines crashing endpoints.
* **Verification steps:** Run `locust` to simulate 100 concurrent WebSocket connections. Ensure zero timeouts.
* **Rollback strategy:** Revert `db_service.py` git checkout; restore `shield_local.db.bak`.
* **Success criteria:** 100% of DB calls execute via `await`. Zero event loop blocking warnings.

---

## Milestone 2: 3D Identity Signature Refactor
* **Objective:** Make the identity verification pose-invariant to prevent false rejections during challenge prompts (yaw/pitch).
* **Files expected to change:** `inference/session_manager.py`.
* **Dependencies:** MediaPipe FaceLandmarker logic.
* **Expected risks:** Decreased strictness leading to false acceptance of visually similar impostors.
* **Verification steps:** Test pipeline against 10 recorded videos featuring >15° head yaw.
* **Rollback strategy:** Revert strictly to the 2D geometric distance metric.
* **Success criteria:** Identity match remains >0.90 even when face is turned.

---

## Milestone 3: Backend H.264 Video Stream Decoding
* **Objective:** Parse incoming continuous video bytes and reconstruct timestamped numpy arrays for inference.
* **Files expected to change:** `backend/main.py`, `backend/services/fusion_service.py`.
* **Dependencies:** `aiortc` or `av` (PyAV), Frontend Milestone 4.
* **Expected risks:** Memory leaks from un-freed video buffers, massive CPU spikes during decoding.
* **Verification steps:** Monitor backend RAM usage during an active 2-minute stream session.
* **Rollback strategy:** Fallback to standard base64 JPEG decoding logic.
* **Success criteria:** 150-frame buffer fills in exactly 5 seconds.

---

## Milestone 4: Native Flutter 30 FPS Video Streaming
* **Objective:** Capture continuous hardware-encoded video from the mobile device to satisfy Nyquist limits.
* **Files expected to change:** `frontend/lib/screens/camera_screen.dart`, `frontend/lib/providers/liveness_provider.dart`.
* **Dependencies:** `flutter_webrtc` or advanced `camera` plugins.
* **Expected risks:** Heavy battery drain, broken hardware encoders on older Android devices.
* **Verification steps:** Trace WebSocket logs to verify exactly ~30 payloads arrive per second.
* **Rollback strategy:** Revert to 500ms `Timer` fallback (`_useTimerFallback`).
* **Success criteria:** Smooth 30 FPS stream with no visual stuttering.
