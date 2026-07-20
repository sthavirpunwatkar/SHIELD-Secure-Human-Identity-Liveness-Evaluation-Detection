import asyncio
import websockets
import json
import time
import subprocess
import os
import av
from datetime import datetime, timezone

async def main():
    print("Starting backend...")
    env = os.environ.copy()
    backend_proc = subprocess.Popen(
        ["python", "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        env=env,
        text=True
    )
    
    await asyncio.sleep(5)
    
    # Generate CSV header
    with open("frontend_fps.csv", "w") as f:
        f.write("frameNumber,captureTime,arrivalTime\n")
    
    print("Generating H.264 video using libopenh264...")
    os.system("ffmpeg -i fake_webcam.y4m -c:v libopenh264 -f h264 test.h264 -y")
    
    container = av.open("test.h264")
    video_stream = next(s for s in container.streams if s.type == 'video')
    
    packets = []
    for packet in container.demux(video_stream):
        packets.append(bytes(packet))
        if len(packets) >= 150:
            break
            
    while len(packets) < 150 and len(packets) > 0:
        packets.append(packets[-1])
        
    try:
        uri = "ws://127.0.0.1:8000/ws/verify?x-bypass-seb=1"
        async with websockets.connect(uri) as websocket:
            print("Simulator connected to backend")
            for i in range(150):
                cap_time = datetime.now(timezone.utc).isoformat()
                metadata = {
                    "frameNumber": i,
                    "timestamp": cap_time,
                    "captureTime": cap_time,
                    "resolution": "1280x720",
                    "width": 1280,
                    "height": 720,
                    "imageFormat": "yuv420",
                    "compressionType": "h264",
                    "payloadSize": len(packets[i % len(packets)]),
                    "landmarks": [{"x": 0.5, "y": 0.5, "z": 0.0}] * 478
                }
                
                await websocket.send(json.dumps(metadata))
                await websocket.send(packets[i % len(packets)])
                
                await asyncio.sleep(1/30.0)
                
    except Exception as e:
        print(f"Simulator error: {e}")
        
    print("Stopping everything...")
    backend_proc.terminate()

if __name__ == "__main__":
    asyncio.run(main())
