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
  const BY_ID = new Map(QS.map(q => [q[0], q]));
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
  ${fn('runCode')}
  ${fn('resumeSelection')}
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
assert.ok(script.includes('airlawExtra:false'), 'supplementary Air Law must default off');
run("XT[2]={a:['010'],u:['010']}; F.pick={'010':[]}; F.airlawExtra=false");
assert.equal(run('inScope(q)'), false, 'shared supplementary must leave Air Law scope');
assert.equal(run("F.pick={'030':[]}; inScope(q)"), true, 'other subject remains available');
assert.equal(run("F.pick={'010':[]}; F.airlawExtra=true; inScope(q)"), true);
run("F.airlawExtra=false; XT[4]={u:['010'],o:1}; const extra=[4,0,0,'Optional?',['A','B'],0,0,0]; BY_ID.set(4,extra); const regular=[5,0,0,'Core?',['A','B'],0,0,0]; BY_ID.set(5,regular); const duplicate=[6,0,0,'Same?',['A','B'],0,1,0]; BY_ID.set(6,duplicate)");
assert.equal(run('inToggles(extra)'), false);
assert.equal(run('inScope(regular)'), true);
assert.equal(run("resumeSelection({code:'010',ids:[4,6,5],i:1,missed:[4,6,5]}).list.map(q=>q[0]).join(',')"), '5');
assert.equal(run("resumeSelection({code:'010',ids:[4,6,5],i:1}).i"), 0, 'filtered prefix must not skip unsolved core');
assert.equal(run("resumeSelection({code:'010',ids:[4,6,5],i:1,missed:[4,6,5]}).missed.join(',')"), '5');
assert.equal(run("resumeSelection({code:'030',ids:[2],i:0}).list.length"), 1);
assert.equal(run("F.airlawExtra=true; F.hideDup=false; resumeSelection({code:'010',ids:[4,6,5],i:1}).list.length"), 3);
assert.equal(run("const rec={code:'010',ids:[4,6,5],i:1,log:[{id:4,ok:true}],missed:[4]}; const before=JSON.stringify(rec); resumeSelection(rec); JSON.stringify(rec)===before"), true, 'saved history must remain intact');
console.log('web scope, shared ID, review exclusion, labels and escaping checks passed');
