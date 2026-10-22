// npm test; WEB_TEST_BROWSER=webkit selects the WebKit mobile engine.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const engines = require('playwright');

(async () => {
  const root = path.resolve(__dirname, '../docs');
  const server = http.createServer((req,res) => {
    const name = new URL(req.url, 'http://localhost').pathname;
    const file = path.resolve(root, '.' + (name === '/' ? '/index.html' : name));
    if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) { res.writeHead(404); return res.end(); }
    const type = file.endsWith('.html') ? 'text/html; charset=utf-8' : file.endsWith('.xml') ? 'application/xml' : 'text/plain';
    res.writeHead(200, {'Content-Type':type}); res.end(fs.readFileSync(file));
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}/`;
  const engine = process.env.WEB_TEST_BROWSER || 'chromium';
  let browser;
  try {
    browser = await engines[engine].launch({headless:true,
      ...(engine === 'chromium' && process.env.MOBILE_BROWSER_EXECUTABLE ? {executablePath:process.env.MOBILE_BROWSER_EXECUTABLE} : {})});
    const context = await browser.newContext({viewport:{width:390,height:844}, isMobile:true,
      hasTouch:true, timezoneId:'Europe/Istanbul', reducedMotion:'reduce'});
    await context.route('**/*', route => route.request().url().startsWith(base) ? route.continue() : route.abort());
    const page = await context.newPage(), errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const appAction = async name => {
      if (await page.locator('#b' + name).isVisible()) return page.locator('#b' + name).tap();
      if (!await page.locator('#quizExtra').isVisible()) await page.locator('#quizMore').tap();
      await page.locator('#quiz' + name).tap();
    };
    const closed = async () => {
      await page.waitForFunction(() => !document.querySelector('#sheet').open && !['stats','notes','text','review'].includes(history.state?.atplUI) && !/^note:/.test(history.state?.atplUI || ''));
      assert.equal(await page.locator('body').evaluate(el => el.classList.contains('modal-open')), false);
    };
    const a11y = async name => {
      if (!await page.evaluate(() => !!window.axe)) await page.addScriptTag({path:require.resolve('axe-core/axe.min.js')});
      const violations = await page.evaluate(async () => (await axe.run(document, {
        runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']},
      })).violations.map(v => ({id:v.id, impact:v.impact, nodes:v.nodes.map(n => n.target)})));
      assert.deepEqual(violations, [], `${engine}: accessibility ${name}`);
    };
    await page.goto(base);
    assert.equal(await page.locator('html').getAttribute('lang'), 'tr');
    assert.match(await page.title(), /PPL Soru Bankası/);
    assert.ok((await page.locator('meta[name="description"]').getAttribute('content')).length > 100);
    assert.equal(await page.locator('link[rel="canonical"]').getAttribute('href'), 'https://ppltr.github.io/');
    assert.equal(JSON.parse(await page.locator('script[type="application/ld+json"]').textContent())['@type'], 'WebApplication');
    assert.match(await (await page.request.get(base + 'robots.txt')).text(), /Sitemap: https:\/\/ppltr.github.io\/sitemap.xml/);
    assert.match(await (await page.request.get(base + 'sitemap.xml')).text(), /<loc>https:\/\/ppltr.github.io\/<\/loc>/);
    await a11y('home');
    await page.locator('#mPick').tap();
    await a11y('module picker');
    await page.locator('#mPick').tap();

    // A long status page must have a close control reachable at every scroll position.
    await page.locator('#bStats').focus(); await page.keyboard.press('Enter');
    assert.equal(await page.locator('#sheetTitle').textContent(), 'Durum');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'sheetTitle');
    await page.locator('#sheetBody').evaluate(el => { el.scrollTop = el.scrollHeight; });
    const closeRect = await page.locator('#sheetClose').boundingBox();
    assert.ok(closeRect.y >= 0 && closeRect.y + closeRect.height <= 844);
    await page.locator('#sheetClose').tap(); await closed();
    assert.equal(await page.evaluate(() => document.activeElement.id), 'bStats');
    await page.locator('#bStats').tap();
    await page.goBack(); await closed();
    await page.goForward(); await page.waitForFunction(() => document.querySelector('#sheet').open);
    await page.locator('#sheetBack').tap(); await closed();
    await page.locator('#bStats').tap();
    await page.locator('#sheetBack').focus(); await page.keyboard.press('Shift+Tab');
    assert.ok(await page.evaluate(() => document.querySelector('#sheet').contains(document.activeElement)));
    await page.locator('#statsAccount > summary').tap();
    await a11y('account');
    await page.locator('#pname').focus(); await page.keyboard.press('Escape'); await closed();

    // Settings rerenders may not stack history entries or lose the saved prompt.
    await page.locator('#optBox > summary').tap();
    await page.waitForFunction(() => history.state?.atplUI === 'settings');
    const depth = await page.evaluate(() => history.length);
    const prompt = 'Cevabı söylemeden kısa bir ipucu ver. <örnek> & "ipucu"';
    await page.locator('#askPrompt').fill(prompt);
    await page.locator('[data-lang="tr"]').tap();
    await page.locator('[data-lang="en"]').tap();
    assert.equal(await page.locator('#askPrompt').inputValue(), prompt);
    assert.equal(await page.evaluate(() => history.length), depth);
    await page.locator('#ord').scrollIntoViewIfNeeded();
    const backRect = await page.locator('#settingsBack').boundingBox();
    const barRect = await page.locator('.bar').boundingBox();
    assert.ok(backRect.y >= barRect.y + barRect.height - 1 && backRect.y < 844);
    await page.locator('#settingsBack').tap();
    await page.waitForFunction(() => !document.querySelector('#optBox').open && !history.state?.atplUI);
    assert.ok(page.url().startsWith(base));
    await page.locator('#optBox > summary').tap();
    await a11y('settings');
    await page.goBack();
    await page.waitForFunction(() => !document.querySelector('#optBox').open);
    await page.locator('#optBox > summary').tap();
    await page.locator('#reviewQueue').tap();
    assert.equal(await page.locator('#sheetTitle').textContent(), 'İnceleme kuyruğu');
    await page.locator('#sheetBack').tap();
    await page.waitForFunction(() => !document.querySelector('#sheet').open && history.state?.atplUI === 'settings');
    assert.ok(await page.locator('#optBox').evaluate(el => el.open));
    await page.locator('#settingsBack').tap();
    await page.waitForFunction(() => !document.querySelector('#optBox').open && !history.state?.atplUI);
    await page.locator('#goTxt').tap();
    assert.ok(await page.locator('#srTa').isVisible());
    await page.locator('#sheetClose').tap(); await closed();

    // A note's Back returns to the note list; Close exits the entire panel.
    await page.locator('#bNotes').tap(); await page.locator('.noteitem').first().tap();
    await page.locator('#sheetBack').tap();
    await page.waitForFunction(() => history.state?.atplUI === 'notes');
    assert.ok(await page.locator('.noteitem').first().isVisible());
    await page.locator('.noteitem').first().tap();
    await page.locator('#sheetClose').tap(); await closed();
    await page.locator('#bNotes').tap(); await a11y('notes');
    await page.locator('#sheetClose').tap(); await closed();

    // Opening and closing a panel must preserve the question and answer state.
    await page.locator('#go').tap();
    const question = await page.locator('#navBtn').textContent();
    await a11y('question');
    await appAction('Stats'); await a11y('status');
    await page.keyboard.press('ArrowRight'); await page.keyboard.press('a');
    await page.locator('#sheetBack').tap(); await closed();
    assert.equal(await page.locator('#navBtn').textContent(), question);
    assert.equal(await page.locator('.opt:disabled').count(), 0);
    await appAction('Stats');
    await page.reload();
    await page.waitForFunction(() => document.querySelector('#sheet').open);
    await page.locator('#sheetClose').tap(); await closed();
    assert.equal(await page.locator('#navBtn').textContent(), question);
    await appAction('Theme'); await a11y('dark question');
    await appAction('Stats'); await a11y('dark status');
    await page.locator('#sheetClose').tap(); await closed();
    if (process.env.MOBILE_QA_DIR) {
      fs.mkdirSync(process.env.MOBILE_QA_DIR, {recursive:true});
      await appAction('Stats');
      await page.screenshot({path:path.join(process.env.MOBILE_QA_DIR, engine + '-status.png')});
      await page.locator('#sheetClose').tap(); await closed();
    }
    assert.deepEqual(errors, []);
    // Useful crawlable content remains available before JavaScript starts.
    const noJS = await browser.newContext({javaScriptEnabled:false});
    await noJS.route('**/*', route => route.request().url().startsWith(base) ? route.continue() : route.abort());
    const staticPage = await noJS.newPage(); await staticPage.goto(base);
    assert.match(await staticPage.locator('main h1').textContent(), /PPL soru bankası/);
    assert.match(await staticPage.locator('main').textContent(), /JavaScript/);
    await noJS.close();

    // Reproduce the real populated-profile case: analyses must never take over settings.
    const populated = await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,reducedMotion:'reduce'});
    await populated.route('**/*',route=>route.request().url().startsWith(base)?route.continue():route.abort());
    const rich = await populated.newPage();
    rich.on('pageerror',error=>errors.push(error.message));
    const ids = JSON.parse(fs.readFileSync(path.join(root,'index.html'),'utf8')
      .match(/<script id="qdata" type="application\/json">(.*?)<\/script>/s)[1]).q.filter(q=>!q[6]).slice(0,12).map(q=>q[0]);
    await rich.addInitScript(ids=>{
      if (sessionStorage.getItem('settingsTestSeeded')) return;
      sessionStorage.setItem('settingsTestSeeded','1');
      const state={v:2,c:{},star:[],day:{},runs:[],passed:[],pref:{lang:'en',sound:false},qt:{},sor:{}};
      ids.forEach(id=>{state.c[id]=[0,0,6,5,0];state.qt[id]=[240000,2,180000,180000];state.sor[id]=[7,Date.now()]});
      localStorage.setItem('atpl.profiles','["Düzen Testi"]');localStorage.setItem('atpl.profile','Düzen Testi');
      localStorage.setItem('atpl.v2:Düzen Testi',JSON.stringify(state));
    },ids);
    await rich.goto(base);
    await rich.locator('#optBox > summary').tap();
    await rich.waitForFunction(()=>history.state?.atplUI==='settings');
    assert.deepEqual(await rich.locator('.settings-group > legend').allTextContents(),['Çalışma düzeni','Dil ve sorular','Sor düğmesi','Ses']);
    assert.equal(await rich.locator('#optBox .qtlist').count(),0);
    assert.equal(await rich.locator('#mode').evaluate(el=>el.closest('fieldset').dataset.settingsGroup),'study');
    assert.equal(await rich.locator('#askPrompt').evaluate(el=>el.closest('fieldset').dataset.settingsGroup),'ask');
    if (process.env.MOBILE_QA_DIR) await rich.screenshot({path:path.join(process.env.MOBILE_QA_DIR,engine+'-grouped-settings.png')});
    await rich.locator('[data-n="20"]').tap();
    await rich.waitForTimeout(350);
    await rich.reload();
    const saved=await rich.evaluate(()=>JSON.parse(localStorage.getItem('atpl.v2:'+localStorage.getItem('atpl.profile'))));
    assert.equal(saved.pref.count,20); assert.equal(Object.keys(saved.qt).length,12);assert.equal(Object.keys(saved.sor).length,12);
    await rich.locator('#settingsBack').tap();
    await rich.waitForFunction(()=>!document.querySelector('#optBox').open&&!history.state?.atplUI);
    await rich.locator('#bStats').tap();
    assert.equal(await rich.locator('#sheetBody > :first-child').getAttribute('id'),'statsOverview');
    assert.deepEqual(await rich.locator('[data-stats-group]').evaluateAll(groups=>groups.map(g=>g.id)),['statsCourses','statsAnalysis','statsAccount']);
    assert.equal(await rich.locator('#statsAnalysis').evaluate(el=>el.open),false);
    assert.equal(await rich.locator('#statsAnalysis .qtrow').first().isVisible(),false);
    if (process.env.MOBILE_QA_DIR) await rich.screenshot({path:path.join(process.env.MOBILE_QA_DIR,engine+'-populated-overview.png')});
    await rich.locator('#statsAnalysis > summary').tap();
    assert.ok(await rich.locator('#goSlow').isVisible());
    assert.ok(await rich.locator('#goLeech').isVisible());
    assert.ok(await rich.locator('#statsAnalysis .qtrow').count()>10);
    await rich.locator('#statsAccount > summary').tap();
    await rich.locator('#pname').fill('Düzen Testi 2'); await rich.locator('#pSave').tap();
    assert.equal(await rich.locator('#statsAnalysis').evaluate(el=>el.open),true);
    assert.equal(await rich.locator('#statsAccount').evaluate(el=>el.open),true);
    assert.equal(await rich.locator('#pname').inputValue(),'Düzen Testi 2');
    await rich.locator('#sheetClose').tap();
    await rich.waitForFunction(()=>!document.querySelector('#sheet').open&&!history.state?.atplUI);
    await rich.locator('#bStats').tap();
    assert.equal(await rich.locator('#statsAnalysis').evaluate(el=>el.open),false);
    assert.equal(await rich.locator('#sheetBody').evaluate(el=>el.scrollTop),0);
    await rich.locator('#sheetClose').tap();
    await rich.waitForFunction(()=>!document.querySelector('#sheet').open&&!history.state?.atplUI);
    await rich.locator('#bWho').tap();
    assert.ok(await rich.locator('#pname').isVisible());
    assert.equal(await rich.locator('#statsAnalysis').evaluate(el=>el.open),false);
    assert.deepEqual(errors,[]);
    await populated.close();
    console.log(`${engine}: panel exits, Back/Forward, focus, settings, preserved exam, SEO and accessibility passed.`);
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
