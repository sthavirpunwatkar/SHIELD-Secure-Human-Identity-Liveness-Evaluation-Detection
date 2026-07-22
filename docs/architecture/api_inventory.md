# SHIELD - API Inventory

## REST Endpoints

### `GET /health`
- **Purpose**: System health check and metrics.
- **Inputs**: None.
- **Outputs**: JSON containing status (`healthy`), memory usage, uptime, camera/decoder readiness, model status.
- **Usage**: Used for readiness/liveness probes and system monitoring.

### `GET /metrics/debug`
- **Purpose**: Exposes debug-level telemetry.
- **Inputs**: None.
- **Outputs**: JSON containing `active_sessions`, `average_latency`, `queue_depth`, `frames_processed`, `frames_dropped`, `uptime`, `backend_fps`.
- **Usage**: Internal observability and optimization.

## WebSocket Endpoints

### `WS /ws/challenge`
- **Purpose**: Active challenge-response liveness streaming.
- **Communication Protocol**:
  - **Client -> Server (Text)**: Commands like `{"type": "start_challenge"}` and metadata like `{"frameNumber": 1}`.
  - **Client -> Server (Binary)**: Encoded H.264 video frame chunks.
  - **Server -> Client (Text/JSON)**: Returns `challenge` actions, `challenge_result` (pass/fail per challenge), and the final `verdict`. Errors and timeout updates are also sent over text.
- **Auth/Validation**: Requires valid SEB Cryptographic Trust Verification headers.
- **Lifecyle**: Creates a `SessionManager` session. Connects -> Issues Challenges -> Streams Frames -> Returns Final Verdict -> Disconnects.

### `WS /ws/verify`
- **Purpose**: Passive liveness detection (no prompts).
- **Communication Protocol**:
  - **Client -> Server (Text)**: Metadata like `{"frameNumber": 1}`.
  - **Client -> Server (Binary)**: Encoded H.264 video frame chunks.
  - **Server -> Client (Text/JSON)**: Returns real-time `verdict` per frame.
- **Auth/Validation**: Requires valid SEB Cryptographic Trust Verification headers.
- **Lifecyle**: Connects -> Streams Frames -> Continuous Feedback -> Disconnects.

## Static File Mounts
- `GET /snapshots/*`: Serves image files stored in `local_storage/snapshots/`.
- `GET /app/*`: Serves the compiled Flutter frontend build located at `frontend/build/web`.
