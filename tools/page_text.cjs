// Print the visible text of a page that only renders in a browser.
// Usage: node tools/page_text.cjs <url>
const { chromium } = require("playwright");

(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy });
  const page = await browser.newPage();
  await page.goto(process.argv[2], { waitUntil: "load", timeout: 90000 });
  await page.waitForTimeout(2500);
  process.stdout.write(await page.evaluate(() => document.body.innerText));
  await browser.close();
})().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
