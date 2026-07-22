import asyncio
from playwright.async_api import async_playwright
import json
import time
import subprocess
import os

async def main():
    print("Starting backend...")
    env = os.environ.copy()
    backend_proc = subprocess.Popen(
        ["python", "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    await asyncio.sleep(5)
    
    csv_lines = ["frameNumber,captureTime,arrivalTime"]
    frame_count = 0
    start_time = time.time()
    
    # We will use the proxy to intercept websocket traffic and record arrival_time
    # Actually, if we just want captureTime and arrivalTime, we can run a proxy in this script!
    
    async def proxy(client_ws, path):
        try:
            async with websockets.connect(f"ws://127.0.0.1:8000{path}") as backend_ws:
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

    import websockets
    start_server = websockets.serve(proxy, "127.0.0.1", 8001)
    proxy_server = await start_server
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, # Run headful!
            args=[
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
                f"--use-file-for-fake-video-capture={os.path.abspath('fake_webcam.y4m')}",
                "--disable-web-security"
            ]
        )
        context = await browser.new_context()
        page = await context.new_page()
        
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        
        print("Navigating to http://localhost:8000/app/")
        # Inject Javascript to redirect websocket to 8001?
        # NO! I patched main.dart to connect to ws://127.0.0.1:8000/ws/verify. I can patch it to 8001!
        await page.goto("http://localhost:8000/app/")
        await asyncio.sleep(5)
        
        print("Waiting 15 seconds to collect frames...")
        await asyncio.sleep(15)
        await browser.close()
        
    proxy_server.close()
    backend_proc.terminate()
    
    with open("frontend_fps.csv", "w") as f:
        f.write("\n".join(csv_lines))
        
    print(f"Done. Collected {frame_count} frames.")
    if frame_count > 0:
        print(f"Average FPS: {frame_count / 15.0:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
