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
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        
        await page.goto("http://localhost:8000/app/")
        await asyncio.sleep(5)
        
        await page.screenshot(path="screenshot.png")
        print("Saved screenshot.png")
        await browser.close()
        
    backend_proc.terminate()

if __name__ == "__main__":
    asyncio.run(main())
