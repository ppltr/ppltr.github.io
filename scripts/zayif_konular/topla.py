import sqlite3,re,collections,json,sys
c=sqlite3.connect('atpl.db')
T=[
('static','Statik elektrik',r'static (discharg|wick|electric|charge)|\bbonding\b|static dischargers|statik (yük|elektrik|boşalt)',{'020','060'}),
('fuel','Yakıt türleri / 100LL',r'avgas|100 ?ll|octane|oktan|tetraethyl|fuel grade|mogas|fuel.{0,30}colou?r|yakıt.{0,30}renk|detonation',{'020','030'}),
('alt','Altimetre / hektopaskal',r'altimeter|altimetre|aneroid|capsule|kapsül|subscale|hPa\b|hectopascal|hektopaskal|millibar|\bQNH\b|\bQFE\b|\bQNE\b',{'020','050','010','060'}),
('mag','Manyeto / ateşleme',r'magneto|manyeto|ignition|ateşleme|spark plug|buji|impulse coupling|dead.?cut|p-lead',{'020'}),
('elec','Elektrik sistemi / voltaj',r'\bvolts?\b|voltaj|gerilim|alternator|alternatör|generator|jeneratör|battery|akü|ammeter|ampermetre|\bfuses?\b|sigorta|circuit breaker|bus ?bar|\bwatts?\b|\bamperes?\b|voltmeter',{'020'}),
('unit','Birimler',r'kelvin|fahrenheit|unit of temperature|which unit|hangi birim|in which unit',{'020','050'}),
]
rows=c.execute("select q.id,q.subject_code,s.code,coalesce(q.text_en,q.text),coalesce(q.text_tr,q.text),q.dup_of from questions q join sections s on s.id=q.section_id").fetchall()
O=collections.defaultdict(list)
for qid,t,te,tt,ok in c.execute("select question_id,text,text_en,text_tr,is_correct from options order by question_id,ord"):
  O[qid].append((te or t, tt or t, ok))
out=[]
for qid,s,sec,te,tt,dup in rows:
  if dup: continue
  blob=te+' '+tt+' '+' '.join(a+' '+b for a,b,_ in O[qid])
  for key,name,p,subs in T:
    if s in subs and re.search(p,blob,re.I):
      out.append((key,qid,s,sec,te,tt,O[qid])); break
if sys.argv[1:]==['list']:
  for key,qid,s,sec,te,tt,o in out: print(key,qid,s,sec,te[:90].replace('\n',' '),'→',[a for a,b,k in o if k][0][:50])
else:
  json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False)
