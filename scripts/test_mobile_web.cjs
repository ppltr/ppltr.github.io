// NODE_PATH=<node_modules> node scripts/test_mobile_web.cjs
// Optional: MOBILE_BROWSER_EXECUTABLE, MOBILE_QA_DIR (screenshots).
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const engines = require('playwright');

(async () => {
  const html = fs.readFileSync(path.join(__dirname, '../docs/index.html'));
  const server = http.createServer((req, res) => {
    res.writeHead(200, {'Content-Type':'text/html; charset=utf-8'});
    res.end(html);
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}/`;
  let browser;
  try {
    const engine = process.env.WEB_TEST_BROWSER || 'chromium';
    browser = await engines[engine].launch({headless:true,
      ...(engine === 'chromium' && process.env.MOBILE_BROWSER_EXECUTABLE ? {executablePath:process.env.MOBILE_BROWSER_EXECUTABLE} : {})});
    const page = await browser.newPage({viewport:{width:414,height:896}, isMobile:true,
      hasTouch:true, deviceScaleFactor:1, timezoneId:'Europe/Istanbul'});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.route('**/*', route => route.request().url().startsWith(base) ? route.continue() : route.abort());
    await page.emulateMedia({reducedMotion:'reduce'});
    const sizes = [[320,480],[320,568],[360,780],[375,812],[390,844],[400,844],[401,844],
      [414,896],[430,932],[480,854],[568,320],[600,960],[667,375],[719,1024],[844,390]];
    const layout = async label => {
      const width = page.viewportSize().width;
      const result = await page.evaluate(() => ({
        // Mobile browsers enlarge innerWidth when content overflows. Compare to
        // the emulated device width instead of accepting that enlarged viewport.
        width:document.documentElement.scrollWidth,
        clipped:[...document.querySelectorAll('.bar,.meta,.walltime,.foot,.opt,.head')]
          .map(el => ({name:el.className, rect:el.getBoundingClientRect().toJSON()}))
          .filter(el => el.rect.width && (el.rect.left < -1 || el.rect.right > document.documentElement.clientWidth + 1)),
      }));
      assert.ok(result.width <= width + 1, `${label}: page ${result.width}px exceeds device ${width}px`);
      assert.deepEqual(result.clipped, [], `${label}: controls clipped`);
    };
    const matrix = async label => {
      for (const [width,height] of sizes) {
        await page.setViewportSize({width,height});
        await layout(`${label} ${width}x${height}`);
      }
      await page.setViewportSize({width:414,height:896});
    };
    const shot = async name => {
      if (!process.env.MOBILE_QA_DIR) return;
      fs.mkdirSync(process.env.MOBILE_QA_DIR, {recursive:true});
      await page.screenshot({path:path.join(process.env.MOBILE_QA_DIR, name + '.png')});
    };
    await page.goto(base);
    // Include the signed-out Google control, even when its remote SDK is blocked.
    await page.locator('#bLogin').evaluate(el => el.classList.remove('hidden'));
    await matrix('home');
    await page.locator('#optBox > summary').click();
    await matrix('settings');
    assert.ok(await page.locator('#askPrompt').evaluate(el => parseFloat(getComputedStyle(el).fontSize) >= 16));
    await page.locator('#go').click();
    await matrix('question');
    await shot('mobile-question');
    await page.waitForTimeout(350);
    await page.addInitScript(() => {
      const seed = sessionStorage.getItem('mobile-test-seed');
      if (!seed) return;
      const {key,state} = JSON.parse(seed);
      localStorage.setItem(key, JSON.stringify(state));
      sessionStorage.removeItem('mobile-test-seed');
    });
    await page.evaluate(() => {
      const key = 'atpl.v2:' + localStorage.getItem('atpl.profile');
      const state = JSON.parse(localStorage.getItem(key)), run = state.runs[0];
      run.i = 999; run.t0 = Date.now() - 26 * 3600000; run.sure = 4 * 3600000;
      run.qN = 999; run.qTop = 999 * 120000;
      run.qAn = [run.ids[999], 3 * 3600000];
      const k = run.round + ':' + run.ids[999];
      run.qWall = {[k]:[0,Date.now() - 3 * 3600000]}; run.qWallOpen = k;
      // Seed on the next load, after the old page has flushed its own state.
      sessionStorage.setItem('mobile-test-seed', JSON.stringify({key,state}));
    });
    await page.reload();
    assert.match(await page.locator('#navBtn').textContent(), /^1000\//);
    assert.match(await page.locator('#tmr .tv').textContent(), /^4:/);
    assert.match(await page.locator('#questionWall').textContent(), /^3:/);
    await matrix('long timers and question 1000');
    await page.locator('#tmr').tap();
    assert.equal(await page.locator('#tmr').getAttribute('aria-pressed'), 'true');
    const wrong = await page.evaluate(() => {
      const db = JSON.parse(document.querySelector('#qdata').textContent);
      const id = +document.querySelector('.card .head > .lbl.num').textContent;
      const q = db.q.find(q => q[0] === id);
      return [...document.querySelectorAll('.opt')].findIndex(el =>
        el.children[1].textContent !== (q[13] || q[4])[0]);
    });
    await page.locator('.opt').nth(wrong).tap();
    await matrix('answered question');
    const next = await page.locator('#next').evaluate(el => ({width:el.clientWidth, text:el.scrollWidth, height:el.clientHeight}));
    assert.ok(next.text <= next.width, 'Continue label must fit');
    assert.ok(next.height >= 44, 'Continue needs a touch target');
    await shot('mobile-answer');
    await page.locator('#navBtn').tap();
    await matrix('navigation panel');
    await page.locator('#navNo').fill('1001');
    await page.locator('#navGo').tap();
    assert.match(await page.locator('#navBtn').textContent(), /^1001\//);
    await page.locator('#bTheme').tap();
    await matrix('theme');
    await shot('mobile-dark');
    await page.locator('#bStats').tap();
    await matrix('stats panel');
    assert.deepEqual(errors, []);
    console.log('Mobile device layouts, long timers, answer controls, navigation, settings and stats passed.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
