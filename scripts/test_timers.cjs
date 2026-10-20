// node scripts/test_timers.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, '../web/template.html'), 'utf8');
const fn = name => {
  const match = html.match(new RegExp('function ' + name + '\\([^]*?\\n}'));
  assert.ok(match, name + ' missing');
  return match[0];
};
const context = vm.createContext({});
const run = code => vm.runInContext(code, context);
run(`
  let R = {round:1, i:0, list:[[101],[102]], picked:null, qWall:{}, qWallOpen:null};
  ${html.match(/const wallKey = [^\n]+/)[0]}
  ${fn('soruToplam')}
  ${fn('toplamKapat')}
  ${fn('toplamAc')}
`);

// Passage of time counts independently of focus, idle status and manual pause.
run('toplamAc(1000); R.durdu = true');
assert.equal(run("soruToplam('1:101', 181000)"), 180000);
// Redrawing the same question must not restart its clock.
run('toplamAc(181000)');
assert.equal(run("soruToplam('1:101', 182000)"), 181000);
// Navigation closes the previous interval; returning accumulates only visits.
run('R.i = 1; toplamAc(182000)');
assert.equal(run("soruToplam('1:101', 192000)"), 181000);
run('R.i = 0; toplamAc(192000)');
assert.equal(run("soruToplam('1:101', 202000)"), 191000);
assert.equal(run("soruToplam('1:102', 202000)"), 10000);
// Saved open timestamps survive reload, including time with the tab closed.
run('R = JSON.parse(JSON.stringify(R)); toplamAc(212000)');
assert.equal(run("soruToplam('1:101', 222000)"), 211000);
// Answering freezes the elapsed time, including later redraws and navigation.
run('toplamKapat(222000); R.picked = 1; toplamAc(232000)');
assert.equal(run("soruToplam('1:101', 242000)"), 211000);
// A retry gets a separate interval; earlier attempts remain intact.
run('R.round = 2; R.picked = null; toplamAc(242000)');
assert.equal(run("soruToplam('2:101', 247000)"), 5000);
assert.equal(run("soruToplam('1:101', 247000)"), 211000);
// Returning home stops question time; resuming excludes time on the home page.
run('toplamKapat(247000); toplamAc(257000)');
assert.equal(run("soruToplam('2:101', 262000)"), 10000);
// Older answered questions have no invented elapsed-time history.
run('R = {round:1, i:0, list:[[101]], picked:0, qWall:{}, qWallOpen:null}; toplamAc(1000)');
assert.equal(run("soruToplam('1:101', 5000)"), null);
console.log('elapsed question timing: pause, navigation, reload, answer freeze, retry and legacy checks passed');
