// Знімки всіх слайдів презентації: node shot_lesson.js <html> <папка для знімків>
// Робить wide-light, wide-dark (1280×800) і phone-light (360×740); пише JS-помилки й переповнення слайда.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const SP = __dirname;
const [file, outDir] = process.argv.slice(2);
require('fs').mkdirSync(outDir, { recursive: true });
(async () => {
  const b = await chromium.launch();
  for (const [w, h, theme, tag] of [[1280, 800, 'light', 'wide-light'], [1280, 800, 'dark', 'wide-dark'], [360, 740, 'light', 'phone-light']]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.route('**/mathjax@3.2.2/es5/tex-svg.js', r => r.fulfill({ path: SP + '/mj/package/es5/tex-svg.js', contentType: 'application/javascript' }));
    await p.goto('file://' + require('path').resolve(file));
    await p.waitForTimeout(2000);
    if (theme === 'dark') await p.click('#btn-theme');
    const total = await p.evaluate(() => document.querySelectorAll('.slide-card').length);
    for (let s = 1; s <= total; s++) {
      await p.evaluate(n => goToSlide(n), s);
      // Розкриваємо приховані відповіді й кроки, щоб побачити повний вміст слайда
      await p.evaluate(() => {
        const c = document.querySelector('.slide-card.active');
        c.querySelectorAll('.hidden-answer').forEach(e => e.classList.add('shown'));
        c.querySelectorAll('.step').forEach(e => e.classList.add('shown'));
        c.querySelectorAll('.quiz-explanation').forEach(e => e.style.display = 'block');
      });
      await p.waitForTimeout(600);
      const [v, hz] = await p.evaluate(() => { const c = document.querySelector('.slide-card.active'); return [c.scrollHeight > c.clientHeight + 2, document.documentElement.scrollWidth > innerWidth]; });
      if (hz) console.log(`${tag} слайд ${s}: ГОРИЗОНТАЛЬНЕ переповнення`);
      if (v && tag !== 'phone-light') console.log(`${tag} слайд ${s}: вміст не вміщується по висоті (з усіма розкритими відповідями)`);
      await p.screenshot({ path: `${outDir}/${tag}-${s}.png` });
    }
    // Клавіші ← → мають гортати
    await p.evaluate(() => goToSlide(1));
    await p.keyboard.press('ArrowRight');
    const counter = await p.evaluate(() => document.getElementById('slide-counter').textContent);
    if (!counter.startsWith('Слайд 2')) console.log(`${tag}: стрілка → не гортає (лічильник: ${counter})`);
    if (errs.length) console.log(`${tag} JS-ПОМИЛКИ:`, errs);
    await p.close();
  }
  await b.close();
  console.log(`знімки: ${outDir}`);
})();
