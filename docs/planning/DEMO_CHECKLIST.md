# SHIELD V2 Demonstration Checklist

## Pre-Flight Setup
- [ ] Ensure webcam is unblocked and functional.
- [ ] Connect to internet (required for local network streaming if testing across devices).
- [ ] Run backend with Demo Mode enabled: `DEMO_MODE=true uvicorn main:app`
- [ ] Run frontend via `flutter run` on target device/simulator.

## Demo Flow
1. **Launch Backend**
   - Show terminal logs confirming `models loaded` and `WebSocket connected`.
2. **Launch Frontend**
   - Present the UI and initial handshake.
3. **Passive Verification**
   - Demonstrate the face boundary overlay.
   - Show how looking forward without interacting maintains a steady evaluation.
4. **Active Challenge**
   - Wait for the system to randomly request an action (e.g., "Look Left").
   - Perform the action.
   - Show the green "Live" UI response.
5. **Blink Detection**
   - Perform the "Blink" challenge.
   - Highlight how the backend captures the EAR (Eye Aspect Ratio) drop.
6. **Head Pose**
   - Demonstrate pitch/yaw/roll extraction.
   - Show how aggressive movement forces a rejection or re-verification.
7. **Liveness Verdict**
   - Present a physical photograph to the camera.
   - Show how the system immediately rejects the spoof via MiniFASNet.
8. **Identity Verification**
   - Explain how jumping frames or switching people mid-session aborts the challenge.
9. **Explain Architecture**
   - Briefly describe the WebSocket binary frame streaming.
   - Contrast this with traditional REST API snapshot latency.
10. **Explain Known rPPG Limitation**
    - Acknowledge that the rPPG (heart rate) fusion weight is currently set to `0.0`.
    - Discuss the scientific finding from PR-005.5: the V2 model suffers a synthetic-to-real domain gap and requires retraining on real-world recordings.
