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
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream",
                "--use-file-for-fake-video-capture=/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/fake_webcam.y4m",
                "--disable-web-security",
                "--disable-gpu",
                "--disable-software-rasterizer"
            ]
        )
        context = await browser.new_context()
        page = await context.new_page()
        
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        
        def on_web_socket(ws):
            print(f"WebSocket opened: {ws.url}")
            def on_frame_sent(frame):
                nonlocal frame_count
                if isinstance(frame, str):
                    try:
                        data = json.loads(frame)
                        if "captureTime" in data:
                            frame_num = data.get("frameNumber", frame_count)
                            cap_time = data["captureTime"]
                            arr_time = time.time()
                            csv_lines.append(f"{frame_num},{cap_time},{arr_time}")
                            frame_count += 1
                            if frame_count % 10 == 0:
                                print(f"Captured {frame_count} frames...")
                    except json.JSONDecodeError:
                        pass
            ws.on("framesent", on_frame_sent)
            
        page.on("websocket", on_web_socket)
        
        print("Navigating to http://localhost:8000/app/")
        await page.goto("http://localhost:8000/app/")
        await asyncio.sleep(5)
        
        print("Clicking first button to start...")
        try:
            await page.mouse.click(400, 500)
            await asyncio.sleep(2)
            await page.mouse.click(400, 500)
        except Exception as e:
            print("Click error:", e)
            
        print("Waiting 15 seconds to collect frames...")
        await asyncio.sleep(15)
        await browser.close()
        
    backend_proc.terminate()
    
    with open("frontend_fps.csv", "w") as f:
        f.write("\n".join(csv_lines))
        
    print(f"Done. Collected {frame_count} frames.")
    if frame_count > 0:
        print(f"Average FPS: {frame_count / 15.0:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
