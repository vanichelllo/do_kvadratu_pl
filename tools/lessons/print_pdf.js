const { chromium } = require('/opt/node-tools/node_modules/playwright');
const [src, out] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + require('path').resolve(src)); await p.waitForTimeout(500);
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-family:Inter,sans-serif;font-size:8px;color:#7f8c8d;width:100%;padding:0 12mm;display:flex;justify-content:space-between"><span>ДО КВАДРАТУ · Дерево тем</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: '14mm', bottom: '16mm', left: '12mm', right: '12mm' } });
  await b.close();
})();
