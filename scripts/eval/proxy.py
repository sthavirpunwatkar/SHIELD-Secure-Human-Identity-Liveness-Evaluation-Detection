import asyncio
import websockets
import json
import time

csv_lines = ["frameNumber,captureTime,arrivalTime"]

async def proxy(client_ws, path):
    try:
        async with websockets.connect(f"ws://127.0.0.1:8001{path}") as backend_ws:
            print(f"Proxy connected to backend for {path}")
            
            async def forward_to_backend():
                frame_count = 0
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
                        except json.JSONDecodeError:
                            pass
                    await backend_ws.send(message)
                    
            async def forward_to_client():
                async for message in backend_ws:
                    await client_ws.send(message)
                    
            await asyncio.gather(forward_to_backend(), forward_to_client())
    except Exception as e:
        print(f"Proxy error: {e}")
    finally:
        with open("frontend_fps.csv", "w") as f:
            f.write("\n".join(csv_lines))
        print(f"Proxy saved {len(csv_lines)-1} frames to frontend_fps.csv")

start_server = websockets.serve(proxy, "127.0.0.1", 8000)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
