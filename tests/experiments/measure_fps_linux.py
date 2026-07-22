import asyncio
import websockets
import json
import time
import subprocess
import os

async def main():
    print("Starting backend...")
    env = os.environ.copy()
    backend_proc = subprocess.Popen(
        ["python", "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8001"],
        env=env,
        text=True
    )
    
    await asyncio.sleep(5)
    
    csv_lines = ["frameNumber,captureTime,arrivalTime"]
    frame_count = 0
    start_time = time.time()
    
    async def proxy(client_ws):
        try:
            path = client_ws.request.path
            print(f"Client connected to proxy for {path}")
            async with websockets.connect(f"ws://127.0.0.1:8001{path}") as backend_ws:
                print(f"Proxy connected to backend for {path}")
                
                async def forward_to_backend():
                    nonlocal frame_count
                    async for message in client_ws:
                        arrival_time = time.time()
                        if isinstance(message, str):
                            try:
                                data = json.loads(message)
                                if "captureTime" in data:
                                    capture_time = data["captureTime"]
                                    frame_number = data.get("frameNumber", frame_count)
                                    csv_lines.append(f"{frame_number},{capture_time},{arrival_time}")
                                    frame_count += 1
                                    if frame_count % 10 == 0:
                                        print(f"Captured {frame_count} frames...")
                            except json.JSONDecodeError:
                                pass
                        await backend_ws.send(message)
                        
                async def forward_to_client():
                    async for message in backend_ws:
                        await client_ws.send(message)
                        
                await asyncio.gather(forward_to_backend(), forward_to_client())
        except Exception as e:
            pass

    start_server = websockets.serve(proxy, "127.0.0.1", 8000)
    proxy_server = await start_server
    print("Proxy server listening on 8000")
    
    print("Starting Linux frontend...")
    frontend_proc = subprocess.Popen(
        ["./frontend/build/linux/x64/release/bundle/shield_app"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    print("Waiting 15 seconds to collect frames...")
    await asyncio.sleep(15)
    
    print("Stopping everything...")
    frontend_proc.terminate()
    proxy_server.close()
    backend_proc.terminate()
    
    with open("frontend_fps.csv", "w") as f:
        f.write("\n".join(csv_lines))
        
    print(f"Done. Collected {frame_count} frames.")
    if frame_count > 0:
        print(f"Average FPS: {frame_count / 15.0:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
