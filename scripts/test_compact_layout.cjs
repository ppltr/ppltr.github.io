// Measures usable question space, not just horizontal overflow.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const engines = require('playwright');

(async () => {
  const html = fs.readFileSync(path.join(__dirname,'../docs/index.html'),'utf8');
  const server = http.createServer((req,res) => {res.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});res.end(html);});
  await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
  const base = `http://127.0.0.1:${server.address().port}/`;
  const engine = process.env.WEB_TEST_BROWSER || 'chromium';
  let browser;
  try {
    browser = await engines[engine].launch({headless:true,
      ...(engine === 'chromium' && process.env.MOBILE_BROWSER_EXECUTABLE ? {executablePath:process.env.MOBILE_BROWSER_EXECUTABLE} : {})});
    const page = await browser.newPage({viewport:{width:402,height:734}, isMobile:true,hasTouch:true,reducedMotion:'reduce'});
    const errors = [];
    page.on('pageerror',e => errors.push(e.message));
    await page.route('**/*',r => r.request().url().startsWith(base) ? r.continue() : r.abort());
    await page.addInitScript(() => {
      localStorage.setItem('atpl.profiles','["Tasarım Testi"]');
      localStorage.setItem('atpl.profile','Tasarım Testi');
      localStorage.setItem('atpl.v2:Tasarım Testi', JSON.stringify({v:2,c:{},star:[],day:{},passed:[],
        pref:{lang:'en',sound:false},runs:[{id:'layout-test',t0:Date.now(),tN:Date.now(),
        ids:[14260,14227],i:0,round:1,missed:[],log:[],done:false,sure:0,sureTam:true}]}));
    });
    const results = [];
    // 402×874 is the logical screen; 402×734 leaves room for browser chrome.
    for (const height of [734,874]) {
      await page.setViewportSize({width:402,height});
      await page.goto(base);
      for (let index=0;index<2;index++) {
        const dimensions = await page.evaluate(() => ({
          questionTop:document.querySelector('.qt').getBoundingClientRect().top,
          headerHeight:document.querySelector('.meta').getBoundingClientRect().height,
          footerHeight:document.querySelector('.foot').getBoundingClientRect().height,
          footerTop:document.querySelector('.foot').getBoundingClientRect().top,
          lastOptionBottom:document.querySelector('.opt:last-child').getBoundingClientRect().bottom,
          optionHeights:[...document.querySelectorAll('.opt')].map(el=>el.getBoundingClientRect().height),
          fontSize:parseFloat(getComputedStyle(document.querySelector('.opt')).fontSize),
          questionFontSize:parseFloat(getComputedStyle(document.querySelector('.qt')).fontSize),
          width:document.documentElement.scrollWidth,
        }));
        assert.equal(await page.locator('.opt').count(),4);
        assert.ok(dimensions.headerHeight <= 48, `Header too tall: ${JSON.stringify(dimensions)}`);
        assert.ok(dimensions.questionTop <= 100, `Question starts too low: ${JSON.stringify(dimensions)}`);
        assert.ok(dimensions.footerHeight <= 60, 'Footer must remain one slim row');
        assert.ok(dimensions.lastOptionBottom <= dimensions.footerTop - 6, `Four options do not fit: ${JSON.stringify(dimensions)}`);
        assert.ok(dimensions.optionHeights.every(h=>h>=44), 'Keep comfortable touch targets');
        assert.ok(dimensions.fontSize >= 16, 'Do not shrink the text to fake a fit');
        assert.ok(dimensions.questionFontSize >= 17, 'Keep the question readable');
        assert.ok(dimensions.width <= 402);
        assert.equal(await page.locator('#quizExtra').isVisible(),false);
        results.push({height,question:index+1,...dimensions});
        if (process.env.MOBILE_QA_DIR) {
          fs.mkdirSync(process.env.MOBILE_QA_DIR,{recursive:true});
          await page.screenshot({path:path.join(process.env.MOBILE_QA_DIR,`${engine}-iphone17-${height}-${index+1}.png`)});
        }
        if (!index) await page.locator('.foot .nvb[data-nav=next]').tap();
      }
    }
    await page.locator('#quizMore').tap();
    assert.ok(await page.locator('#runStart').isVisible());
    assert.ok(await page.locator('#questionWall').isVisible());
    await page.locator('#tmr').tap();
    assert.equal(await page.locator('#tmr').getAttribute('aria-pressed'),'true');
    await page.locator('#quizStats').tap();
    await page.locator('#sheetBack').tap();
    assert.equal(await page.locator('#quizExtra').isVisible(),false);
    assert.ok(await page.locator('#quizMore').isVisible());
    assert.deepEqual(errors,[]);
    console.log(engine+' iPhone 17 Pro content-space checks: '+JSON.stringify(results));
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve=>server.close(resolve));
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
