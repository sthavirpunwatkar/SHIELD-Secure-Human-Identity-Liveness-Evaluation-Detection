const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    args: [
      '--use-fake-ui-for-media-stream',
      '--use-fake-device-for-media-stream',
      '--use-file-for-fake-video-capture=/tmp/video.y4m'
    ],
    executablePath: '/usr/bin/google-chrome',
    headless: "new"
  });
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', err => console.log('BROWSER ERROR:', err.toString()));

  const fileUrl = 'file://' + path.resolve(__dirname, 'poc.html');
  console.log(`Navigating to ${fileUrl}`);
  await page.goto(fileUrl);
  
  // Wait 10 seconds to let the camera and encoder run for 150 frames at 30 fps
  await new Promise(r => setTimeout(r, 10000));
  
  await browser.close();
  console.log("PoC run complete.");
})();
