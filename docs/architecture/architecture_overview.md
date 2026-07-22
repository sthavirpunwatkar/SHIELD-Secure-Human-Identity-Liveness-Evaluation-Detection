# SHIELD System Architecture Documentation

## DIAGRAM 1: Overall System Architecture
```mermaid
graph LR
    User([User]) -->|Interacts| Flutter[Flutter Frontend]
    Flutter -->|Captures Video| Camera[Camera Service]
    Camera -->|H.264 Encode| Encoder[WebCodecs]
    Encoder -->|WS Transport| FastAPI[FastAPI Backend]
    
    subgraph Server
        FastAPI --> Auth[SEB Auth & Trust]
        Auth --> Pipeline[AI Inference Pipeline]
        Pipeline --> DB[Local Database]
    end
    
    Pipeline -->|Verdict| FastAPI
    FastAPI -->|WS JSON| Flutter
    Flutter -->|Displays Result| User
```

## DIAGRAM 3: Backend Architecture
```mermaid
graph TD
    WS[WebSocket Routers] -->|Raw Bytes| Decoder[StreamingDecoder]
    WS -->|JSON Commands| SM[SessionManager]
    Decoder -->|Decoded Frames| FS[FusionService]
    
    subgraph Services
        FS
        SM
        DB[LocalDBService]
    end
    
    subgraph AI Orchestration [FusionService]
        Yolo[YOLOv8-Seg]
        Qual[QualityScoreEngine]
        Behav[BehavioralAnalyzer]
        Anti[MiniFASNet Antispoof]
        rPPG[rPPG 1D-CNN]
        FE[FusionEngine]
    end
    
    FS --> Yolo
    FS --> Qual
    FS --> Behav
    FS --> Anti
    FS --> rPPG
    
    Yolo & Qual & Behav & Anti & rPPG --> FE
    FE -->|Score & Verdict| SM
    SM -->|Save State| DB
```

## DIAGRAM 4: Frontend Architecture
```mermaid
graph TD
    subgraph UI Screens
        PS[Pre-Verification Screen]
        CS[Challenge Screen]
        CamS[Camera Screen]
    end
    
    subgraph Services
        CCS[CameraCaptureService]
        ChalS[ChallengeService]
        FTS[FrameTransportService]
        SEB[SecurityService]
        Codec[WebCodecs]
    end
    
    CS --> ChalS
    CamS --> CCS
    PS --> SEB
    
    CCS --> Codec
    Codec --> FTS
    FTS -->|WebSocket| Backend[Backend API]
    ChalS -->|Listens to WS| FTS
```

## DIAGRAM 5: Request Lifecycle
```mermaid
graph TD
    A[User Starts Session] --> B[Camera Captures Frame]
    B --> C[Frame Encoded to H.264 chunk]
    C --> D[Sent via WebSocket]
    D --> E[FastAPI Validates SEB Trust]
    E --> F[Decoded into OpenCV BGR]
    F --> G[YOLO Face Detect & Crop]
    G --> H[Quality Check]
    H --> I[Behavior/Landmarks Check]
    I --> J[MiniFASNet AntiSpoof Check]
    J --> K[rPPG Feature Extraction]
    K --> L[Fusion Engine Multi-Modal Merge]
    L --> M[Verdict Generated]
    M --> N[Saved to DB/Logs]
    N --> O[Returned to Frontend]
```

## DIAGRAM 6: AI Inference Pipeline
```mermaid
graph TD
    Frame[Raw Frame] --> Yolo[YoloSegDetector]
    Yolo -->|bbox| Crop[Face Crop]
    Yolo -->|is_mask_spoof| MaskCheck{Mask Found?}
    
    MaskCheck -- Yes --> SpoofVerdict[Verdict: Spoof]
    MaskCheck -- No --> QSE[QualityScoreEngine]
    
    QSE -->|passes_gate| GateCheck{Passes?}
    GateCheck -- No --> LQ[Verdict: Low Quality]
    GateCheck -- No --> SpoofVerdict
    GateCheck -- Yes --> BA[BehavioralAnalyzer]
    
    BA -->|EAR, MAR, Pose| Landmarks[Landmarks Extracted]
    Landmarks -->|Challenge Active?| ChalCheck{Action Performed?}
    
    Landmarks --> AS[AntispoofInference / MiniFASNet]
    AS -->|Confidence Score| RPPG[RPPGDetector]
    
    RPPG -->|Window Buffer HR| FE[FusionEngine]
    ChalCheck -->|Score| FE
    AS --> FE
    BA -->|Behavior Score| FE
    
    FE -->|Threshold/Weights applied| FinalDecision[Final Verdict]
```

## DIAGRAM 7: Fusion Engine
```mermaid
graph TD
    subgraph Inputs
        RPPG[rPPG Score 0-1]
        Behav[Behavior Score 0-1]
        AS[Antispoof Score 0-1]
        Chal[Challenge Score 0-1]
    end
    
    Inputs --> Logic[Fusion Engine Weights]
    Logic --> |Challenge Active| W1[rPPG: 0.1, Beh: 0.1, AS: 0.4, Chal: 0.4]
    Logic --> |Passive| W2[rPPG: 0.3, Beh: 0.2, AS: 0.5, Chal: 0]
    Logic --> |Passive No Movement| W3[rPPG: 0.4, Beh: 0, AS: 0.6, Chal: 0]
    
    W1 & W2 & W3 --> Agg[Aggregate Score]
    
    Agg --> FinalCheck{Score > 0.5?}
    FinalCheck -- Yes --> Live[Verdict: Live]
    FinalCheck -- No --> Spoof[Verdict: Spoof]
    
    AS -.->|Score < 0.25| Spoof
```

## DIAGRAM 8: Sequence Diagram
```mermaid
sequenceDiagram
    participant User
    participant Flutter
    participant CameraService
    participant FastAPI
    participant FusionService
    participant DB
    
    User->>Flutter: Start Challenge Session
    Flutter->>FastAPI: WebSocket Connect (/ws/challenge)
    FastAPI-->>Flutter: Connect OK
    Flutter->>FastAPI: {"type": "start_challenge"}
    FastAPI-->>Flutter: {"type": "challenge", "action": "blink"}
    
    loop Every Frame
        CameraService->>Flutter: Capture Frame
        Flutter->>FastAPI: Binary Frame Chunk
        FastAPI->>FusionService: process_challenge_frame()
        FusionService->>FusionService: YOLO -> Behav -> AntiSpoof -> rPPG -> Fusion
        FusionService-->>FastAPI: Verdict + Challenge Update
        FastAPI-->>Flutter: {"type": "challenge_result"} (if passed)
    end
    
    FastAPI->>DB: save session results
    FastAPI-->>Flutter: Final Verdict JSON
    Flutter->>User: Display Result
```

## DIAGRAM 9: Activity Diagram
```mermaid
stateDiagram-v2
    [*] --> Launch
    Launch --> ValidateSEB
    ValidateSEB --> ConnectingWS
    ConnectingWS --> ActiveSession
    
    state ActiveSession {
        [*] --> Idle
        Idle --> Capturing : Received Challenge
        Capturing --> Decoding
        Decoding --> InferencePipeline
        InferencePipeline --> Decision
        Decision --> Capturing : Challenge not complete
        Decision --> Success : All passed
        Decision --> Failed : Timeout/Spoof
    }
    
    ActiveSession --> DBLogging
    DBLogging --> [*]
    
    ConnectingWS --> Error : WS Failure
    ActiveSession --> Error : Protocol Error
    Error --> [*]
```

## DIAGRAM 10: State Diagram (Session)
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Connecting : ws.connect()
    Connecting --> Connected : accepted
    Connected --> Capturing : challenge issued
    Capturing --> Detecting : frame received
    Detecting --> Liveness : AI pipeline passed
    Detecting --> Spoof : AI pipeline failed
    Liveness --> Verified : session complete
    Spoof --> Rejected : session aborted
    Verified --> Disconnected
    Rejected --> Disconnected
    Disconnected --> [*]
```

## DIAGRAM 11: Database ER Diagram
```mermaid
erDiagram
    VERIFICATION {
        string id PK "UUID"
        string session_id "UUID"
        string verdict "Live/Spoof"
        float confidence "0.0 - 1.0"
        string details "JSON breakdown"
        string image_url "Path to snapshot"
        datetime timestamp
    }
```

## DIAGRAM 12: Deployment Diagram
```mermaid
graph TD
    subgraph Client Device
        FlutterApp[Mobile/Desktop App]
        Cam[Hardware Camera]
    end
    
    subgraph Cloud / Server
        Docker[Docker Engine]
        subgraph Docker Container
            FastAPI[Uvicorn / FastAPI Server]
            SQLite[(shield_local.db)]
            Disk[(Local Images)]
            Models[(ONNX/PT Models)]
        end
    end
    
    Cam --> FlutterApp
    FlutterApp -->|WSS over Internet| FastAPI
    FastAPI --> SQLite
    FastAPI --> Disk
    FastAPI --> Models
```

## DIAGRAM 13: Docker Architecture
```mermaid
graph TD
    subgraph Host Network
        Port[Host Port 8000]
    end
    
    subgraph Docker Container: shield_backend
        Port --> Uvicorn[Uvicorn Process]
        Uvicorn --> FastAPI[FastAPI App]
        
        subgraph Volumes
            V1[./models:/app/models]
            V2[./local_storage:/app/local_storage]
            V3[./logs:/app/logs]
            V4[./shield_local.db:/app/shield_local.db]
        end
        
        FastAPI --> V1
        FastAPI --> V2
        FastAPI --> V3
        FastAPI --> V4
    end
```

## DIAGRAM 14: API Communication
```mermaid
graph TD
    App[Client App]
    API[FastAPI Router]
    
    App -->|GET /health| API
    API -->|JSON 200 OK| App
    
    App -->|GET /metrics/debug| API
    API -->|JSON Metrics| App
    
    App -->|WSS /ws/challenge| API
    API -->|Challenge Text| App
    App -->|Binary Frame| API
    API -->|Verdict Text| App
```

## DIAGRAM 15: Data Flow Diagram (Level 1)
```mermaid
graph TD
    Client((Client App))
    
    Process1((Frame Decoder))
    Process2((AI Inference))
    Process3((Fusion Logic))
    Process4((DB Service))
    
    Store1[(Model Files)]
    Store2[(SQLite DB)]
    
    Client -->|Video Stream| Process1
    Process1 -->|OpenCV BGR Matrix| Process2
    Store1 -->|Weights| Process2
    Process2 -->|Individual Scores| Process3
    Process3 -->|Final Boolean Verdict| Process4
    Process4 -->|Log Data| Store2
    Process3 -->|Response JSON| Client
```

## DIAGRAM 16: Component Diagram
```mermaid
componentDiagram
    [Client Frontend (Flutter)] as Client
    [WebSocket Manager] as WS
    [Video Decoder Service] as Video
    [AI Fusion Engine] as AI
    [Database Service] as DB
    
    Client --> WS : Uses
    WS --> Video : Depends on
    WS --> AI : Depends on
    WS --> DB : Depends on
```

## DIAGRAM 17: Execution Timeline
```mermaid
gantt
    title Single Frame Request Execution Timeline
    dateFormat  s.ms
    axisFormat  %L ms
    
    section Network
    WS Receive            :a1, 0, 5ms
    
    section Decoding
    H.264 Decode          :a2, after a1, 15ms
    
    section AI Pipeline
    YOLO Detect & Crop    :a3, after a2, 20ms
    Quality Check         :a4, after a3, 5ms
    Behavior/Landmarks    :a5, after a4, 15ms
    MiniFASNet            :a6, after a5, 20ms
    rPPG Processing       :a7, after a6, 10ms
    
    section Post-Proc
    Fusion Algorithm      :a8, after a7, 2ms
    DB Logging            :a9, after a8, 5ms
    WS Send JSON          :a10, after a9, 3ms
```
