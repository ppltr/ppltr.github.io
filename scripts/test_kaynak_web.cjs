// Çalışma şablonunun gerçek kapsam ve kaynak çizimi işlevlerini çalıştırır.
// node scripts/test_kaynak_web.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, '../web/template.html'), 'utf8');
const script = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)]
  .map(m => m[1]).find(s => s.includes('function inScope'));
new vm.Script(script); // Şablonun tamamı JS sözdizimi açısından geçerli olmalı.
const fn = name => {
  const single = script.match(new RegExp('function ' + name + '\\([^\\n]*}[^\\S\\n]*\\n'));
  if (single) return single[0];
  const m = script.match(new RegExp('function ' + name + '\\([^]*?\\n}'));
  assert.ok(m, name + ' function missing');
  return m[0];
};
const declaration = name => script.match(new RegExp('const ' + name + ' =[^\\n]+'))[0];
const context = vm.createContext({console});
vm.runInContext(`
  const SUBJ = [{c:'010', n:'Air Law',sec:[['010-01'],['010-X']]}, {c:'030',n:'Performance',sec:[['030-01']]}];
  const XT = {2:{a:['010'],k:'d'}, 3:{r:1}};
  const KS = {unsafe:['<img src=x onerror=bad>', 'javascript:bad']};
  const S = {passed:[], c:{}};
  const F = {pick:{'010':[]}, hideDup:true,gen:true,ek:true,rev:true,hideFlag:false,q:''};
  const q = [2,1,0,'TORA?',['TORA','TODA'],0,0,0];
  const uncertain = [3,0,0,'Unknown?',['A','B'],0,0,0];
  const QS = [q,uncertain];
  const xOf = q => XT[q[0]] || null;
  const isRev = q => !!(XT[q[0]] && XT[q[0]].r);
  const isEk = q => !!(XT[q[0]] && XT[q[0]].o);
  const pickedAny = () => Object.keys(F.pick).length > 0;
  const card = id => S.c[id];
  const subjName = s => s.n;
  const trMode = () => true;
  const esc = s => String(s).replace(/[&<>\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));
  ${fn('isPassed')}
  ${declaration('qSubjects')}
  ${declaration('inSubject')}
  ${declaration('qSection')}
  ${declaration('notPassed')}
  ${fn('matchPick')}
  ${fn('inScope')}
  ${fn('inToggles')}
  ${fn('moduleStat')}
  ${fn('xTags')}
  ${fn('xNote')}
`, context);
const run = code => vm.runInContext(code, context);
assert.equal(run('inScope(q)'), true);
assert.equal(run('inScope(uncertain)'), false, 'legacy rev:true must not enable scored review');
assert.equal(run('inToggles(uncertain,true)'), false);
assert.equal(run("F.pick={'010':['010-X']}; inScope(q)"), true);
assert.equal(run("F.pick={'010':['010-01']}; inScope(q)"), false);
assert.equal(run("S.passed=['030']; F.pick={'010':[]}; inScope(q)"), true);
assert.equal(run("moduleStat('010').total"), 1);
assert.equal(run("moduleStat('030').total"), 0);
assert.equal(run("S.passed=['030','010']; inScope(q)"), false);
assert.equal(run("S.passed=[]; F.pick={'010':[],'030':[]}; QS.filter(inScope).length"), 1);
assert.match(run('xTags(q)'), /Kullanıcının sınavda karşılaştığını doğruladığı soru/);
assert.ok(!run('xTags(q)').includes('★ sınavda çıktı'));
const rendered = run("XT[2]={e:'<script>bad</script>',s:[['unsafe','<Q>','<p>','javascript:bad']]}; xNote(q)");
assert.ok(!rendered.includes('<script>'));
assert.ok(!rendered.includes('<img'));
assert.ok(!rendered.includes('href='), 'non-http links must never become clickable');
assert.ok(rendered.includes('&lt;script&gt;'));
assert.ok(rendered.includes('&lt;Q&gt;'));
console.log('web scope, shared ID, review exclusion, labels and escaping checks passed');
