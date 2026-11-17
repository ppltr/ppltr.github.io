import json,sqlite3,sys,re
src,dst=sys.argv[1],sys.argv[2]
rows=json.load(open(src))
DROP={14522,14714,14726,14730,14735,14743,14745,14767,14771,14786,14800,15879,56022,56005,14470,14681,14548,14512,14521,14606,14612,14627,14763,14773,14803,52009,52033,52034,52228,14862,14865,14866,53015,15353,15354,15380,15040,15419,61002}
MOVE={52212:'elec',52231:'elec',14860:'unit',52217:'unit',52218:'unit',52229:'unit',52205:'unit',52221:'mag',52222:'mag'}
c=sqlite3.connect('atpl.db')
EX={i:(a,b) for i,a,b in c.execute("select id,explanation,explanation_en from questions")}
kn=json.load(open('data/_kaynak_notlari.json'))['notlar']
NAMES={'alt':'Altimetre ve hektopaskal','mag':'Manyeto ve ateşleme','elec':'Elektrik sistemi ve voltaj','fuel':'Yakıt türleri ve 100LL','static':'Statik elektrik','unit':'Birimler'}
TUZAK={
'alt':"Statik port kapsülün içine değil, <b>gösterge kutusuna</b> bağlıdır; kapsülün içi neredeyse vakumdur, alçalınca kapsül <b>büzülür</b>. Ayar artınca gösterge artar; ISA'da deniz seviyesinde 1 hPa ≈ <b>27 ft</b> (≈ 8 m).",
'mag':"Kontak OFF = manyetonun primer devresi <b>toprağa bağlanır</b> (topraklanır), açılmaz. P-lead koparsa kontak kapalıyken bile pervane çevrilince motor çalışabilir. Aşırı devir düşüşü → manyeto; sert çalışma → buji.",
'elec':"Sistem (alternatör) gerilimi <b>14 V / 28 V</b>, akü <b>12 V / 24 V</b>. Alternatör arızasında akü boşalana kadar besler; manyetolar elektrik sisteminden bağımsızdır.",
'fuel':"100LL = 100 oktan, <b>low lead</b> (düşük kurşun, kurşunsuz değil), rengi <b>mavi</b>. AVGAS 100 yeşil. Oktan = vuruntuya (detonasyona) direnç.",
'static':"Static wick uçuşta biriken statik yükü havaya boşaltır, <b>telsiz parazitini</b> azaltır; yıldırımdan korumaz. Yakıt ikmalinde topraklama/bonding kablosu kullanılır.",
'unit':"hPa = <b>basınç</b>; Kelvin, °C, °F = sıcaklık. Volt = gerilim, amper = akım, ohm = direnç, watt = güç.",
}
G={k:[] for k in NAMES}
seen=set()
for key,qid,s,sec,te,tt,o in rows:
  if qid in DROP or qid in seen: continue
  seen.add(qid); key=MOVE.get(qid,key)
  ok=[i for i,x in enumerate(o) if x[2]]
  assert ok==[0],qid
  n=kn.get(str(qid),{})
  ex_tr=n.get('tr') or EX[qid][0] or ''
  ex_en=n.get('en') or EX[qid][1] or ''
  G[key].append({'id':qid,'s':s,'sec':sec,'en':te,'tr':tt,'oe':[x[0] for x in o],'ot':[x[1] for x in o],'xt':ex_tr,'xe':ex_en,'yeni':qid>=52201 and qid<52300})
data=[{'k':k,'ad':NAMES[k],'tuzak':TUZAK[k],'q':G[k]} for k in ['alt','mag','elec','fuel','static','unit']]
tot=sum(len(g['q']) for g in data)
html=open(sys.argv[3]).read().replace('__DATA__',json.dumps(data,ensure_ascii=False)).replace('__TOT__',str(tot))
open(dst,'w').write(html)
for g in data: print(g['ad'],len(g['q']))
print('toplam',tot)
