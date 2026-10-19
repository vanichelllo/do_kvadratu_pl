// node interact.js <html> <out-prefix> "<js1>" "<js2>" ... — після кожного js робить знімок 1280×800
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const SP = __dirname;
const [file, prefix, ...codes] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  for (const theme of ['light', 'dark']) {
    const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.route('**/mathjax@3.2.2/es5/tex-svg.js', r => r.fulfill({ path: SP + '/mj/package/es5/tex-svg.js', contentType: 'application/javascript' }));
    await p.goto('file://' + require('path').resolve(file)); await p.waitForTimeout(1500);
    if (theme === 'dark') await p.click('#btn-theme');
    for (let i = 0; i < codes.length; i++) {
      await p.evaluate(codes[i]); await p.waitForTimeout(700);
      await p.screenshot({ path: `${prefix}-${theme}-${i + 1}.png` });
    }
    if (errs.length) console.log(theme, 'JS-ПОМИЛКИ', errs);
    await p.close();
  }
  await b.close();
})();
