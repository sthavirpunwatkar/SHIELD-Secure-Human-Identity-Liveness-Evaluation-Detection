# SHIELD - Dependency Graph & Components

```mermaid
graph TD
    subgraph Frontend [Flutter Application]
        UI[Screens] --> CS[ChallengeService]
        UI --> CM[CameraCaptureService]
        CM --> FS[FrameTransportService]
        FS --> WS_Client[WebSocket Client]
    end

    subgraph Backend [FastAPI Application]
        WS_Server[main.py: WebSocket Router]
        WS_Server --> SD[StreamingDecoder]
        WS_Server --> SM[SessionManager]
        WS_Server --> Fus_Serv[FusionService]
        Fus_Serv --> YOLO[YoloSegDetector]
        Fus_Serv --> QA[QualityScoreEngine]
        Fus_Serv --> BA[BehavioralAnalyzer]
        Fus_Serv --> AS[AntispoofInference]
        Fus_Serv --> RPPG[RPPGDetector]
        Fus_Serv --> FE[FusionEngine]
        SM --> DB[LocalDBService]
    end

    subgraph Storage [Persistent Storage]
        DB --> SQLite[(shield_local.db)]
        DB --> LocalDisk[(local_storage/)]
    end

    WS_Client -- "Binary H.264 + JSON" --> WS_Server
```

## Detailed Explanations
- **Flutter Frontend**: Uses `CameraCaptureService` to continuously retrieve camera frames. These frames are pushed to `FrameTransportService`, which manages backpressure, queues, and encodes them using webcodecs.
- **WebSockets**: Serves as the high-throughput pipeline. Binary frames are interlaced with JSON metadata.
- **FastAPI / StreamingDecoder**: Receives the binary payload, decodes the H.264 chunks into OpenCV BGR frames.
- **FusionService**: The core orchestrator. Passes the frame sequentially through detection (YOLO), quality, behavioral, antispoof (MiniFASNet), and physiological (rPPG) checks.
- **FusionEngine**: Applies weighting algorithms (dynamically adjusted based on active challenges vs passive state) to merge model outputs into one verdict.
- **SessionManager**: Keeps track of challenges passed, timestamps, and prevents timeouts/identity swaps.
