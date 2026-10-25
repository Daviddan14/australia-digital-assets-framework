// Print the document HTML to an A4 PDF with page numbers.
// Usage: node scripts/pdf.cjs <in.html> <out.pdf> <title>
const { chromium } = require("playwright");

(async () => {
  const [input, output, title] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + input, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  const foot =
    '<div style="width:100%;font:7pt Helvetica,Arial,sans-serif;color:#5A6A75;padding:0 18mm;display:flex;justify-content:space-between">' +
    "<span>" + title + " &middot; General information, not legal advice</span>" +
    '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>';
  await page.pdf({
    path: output,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate: foot,
    tagged: true,
    outline: true,
  });
  await browser.close();
})().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
