# PPL Soru Bankası — çalışma kuralları

PPL teori sınavlarına hazırlık için soru bankası ve çalışma sitesi.
Sorular ATPL TV platformundaki *PPL Turkey (English)* sınav raporlarından elle çevrildi.

**Banka ağırlıkla PPL.** ATPL soruları ileride eklenecek. Seviye `subjects.level`
sütununda ve dışa aktarımdaki `lv` alanında tutulur, varsayılan `ppl`. ATPL eklenirken
veri JSON'una `"level": "atpl"` yaz; uygulamada seviye süzgeci o zaman eklenir. Depo
dizini tarihsel olarak `atpl/` adında, karışmasın.

**502 · Güvenlik Bilinci PPL değil**, SHGM güvenlik bilinci sınavının dersidir;
`"level": "gb"` ile işaretli. Seviye süzgeci eklenirken bu modülü PPL'in içine sayma.
Uygulamada modül listesinde 501'in yanında görünür — bu bilinçli.

## Bozulmaması gereken kural

**Veritabanında her sorunun doğru cevabı A şıkkıdır.** Kaynak rapor şıkları doğru cevap
en başta olacak şekilde veriyor; bu sıra `data/*.json` içinde ve `atpl.db`'de korunur.
Şıkları veritabanında karıştırma. Karıştırma yalnızca sunum katmanında yapılır:

- `server/` — sunucuda, tur tohumu + soru id'sinden türeyen sabit sırayla
- `web/` artifact — tarayıcıda

## Yerleşim

```
data/*.json          soru kaynağı (elle çevrilmiş, tek doğruluk kaynağı)
data/tr/*.json       soruların Türkçe çevirisi (id → metin + şıklar)
data/tr/_dersler.json ders ve bölüm adlarının Türkçesi
data/_tekrarlar.json elle doğrulanmış tekrar grupları
scripts/init_db.py   data/ → atpl.db  (idempotent, ON CONFLICT ile günceller)
scripts/check_tr.py  çevirileri kaynakla karşılaştırıp doğrular
scripts/find_duplicates.py  benzer soru tarayıcı
scripts/topic_gap.py   ders notunda olup soruda olmayan konuları listeler
atpl.db              üretilmiş soru bankası — elle düzenleme, JSON'u düzelt
server/              FastAPI çalışma sitesi (misafir öncelikli, giriş isteğe bağlı)
server/app.db        kullanıcı verisi — .gitignore'da, YEDEKLENMESİ GEREKEN TEK DOSYA
web/template.html    çalışma uygulamasının kaynağı (build_web.py veriyi gömer)
web/atpl-soru-bankasi.html  üretilmiş tek dosya — elle düzenleme, template'i düzelt
notes/               ders notları ve cheat sheet'ler
```

Soru değişikliği her zaman `data/*.json` üzerinden yapılır, sonra:

```bash
python3 scripts/init_db.py     # bankayı yeniden üret
python3 scripts/build_web.py   # artifact sürümünü tazele
```

`init_db.py` tabloları düşürmez; kullanıcı verisi ayrı dosyada olduğu için güvenlidir.

## Soru dili (İngilizce / Türkçe)

**Her sorunun iki dilde de karşılığı vardır ve kip içinde dil karışmaz.** Varsayılan
İngilizcedir — sınavda öyle çıkıyor. Kaynak dosyalara dokunulmaz; karşılıklar ayrı
klasörlerde durur:

- `data/tr/*.json` — kaynağı İngilizce olan soruların Türkçesi (2.207 soru)
- `data/en/*.json` — kaynağı Türkçe olan soruların İngilizcesi (501, 502, ders notu
  soruları; 450 soru). Bunlar dosya düzeyinde `"lang": "tr"` taşır.

```json
{ "questions": { "14227": { "text": "Soru?", "options": ["Şık 1", "Şık 2"] } } }
```

- **Şıklar sırayla eşlenir.** Kaynakta doğru cevap ilk şıktır; çeviri aynı sırayı
  taşımak zorundadır. Sayı tutmazsa `init_db.py` ve `check_tr.py` derlemeyi durdurur —
  sıra kayarsa yanlış şık doğru diye işaretlenirdi.
- Bir dilde karşılığı eksik kalan soru o kipte **kaynak dilinde** görünür. Bu bir
  gerileme sayılır: `check_tr.py` iki yönü de sayar, `init_db.py` eksik varsa uyarır.
  Yeni soru eklerken diğer dildeki karşılığını da ekle.
- Ders/bölüm adları `data/tr/_dersler.json` ve `data/en/_dersler.json` içinde.

Çeviri eklendikten sonra:

```bash
python3 scripts/check_tr.py            # şık sayısı, boş/çevrilmemiş metin, çift id
python3 scripts/init_db.py && python3 scripts/build_web.py
```

Uygulamada tercih `F.lang` (`'en'` varsayılan), Ayarlar'daki **Soru dili** satırından
seçilir ve `S.pref` içinde saklanıp cihazlar arasında eşitlenir. Metin seçimi tek yerden
geçer: `qText(q)` / `qOpts(q)` / `subjName(s)` / `secName(sc)`. Soru metnini doğrudan
`q[3]`, şıkları `q[4]` diye okuma — dil süzgeci devre dışı kalır. Seçim her çizimde
yapıldığı için yarım kalan tura dönünce kalan sorular da seçili dilde gelir.

**İlerleme dilden bağımsızdır.** Kayıt soru **id'sine** bağlı; dili değiştirmek
çözülmüşleri sıfırlamaz ve aynı soruyu iki dilde iki kez sormaz. Şık dizilerinin uzunluğu
iki dilde aynı olduğu için tur ortasında dil değiştirmek cevap konumlarını da bozmaz.

Dışa aktarımda soru satırı: `q[3]`/`q[4]` kaynak metin+şıklar, `q[10]`/`q[11]` Türkçesi,
`q[12]`/`q[13]` İngilizcesi. **Kaynak dilin alanı boş bırakılır** — o dilde zaten
`q[3]`/`q[4]` okunur, aynı metin iki kez gömülmez. Bölüm satırı da benzer:
`[kod, kaynak ad, Türkçe ad, İngilizce ad]`, sondaki boşlar atılır.

## Tekrar grupları

`data/_tekrarlar.json` içinde her grubun ilk id'si kanonik, diğerleri `dup_of` ile
ona bağlanır. **Cevabı farklı olan benzer sorular tekrar sayılmaz** — onlar sınavın
en değerli tuzakları (ör. 15613 METAR'da true north / 15666 ATIS'te magnetic north).
Yeni ders eklerken hem metin benzerliğini hem de "cevabı aynı ama metni farklı"
çiftleri tara; karar insana ait.

**Tarayıcılar dil-kördür.** `find_duplicates.py` ve `topic_gap.py` yalnız sorunun kaynak
dilindeki metnine bakar; Türkçe ders notu/üretilmiş soru ile İngilizce banka arasında
eşleşme kuramazlar. 090'da "tekrar yok" sonucu bu yüzden eksik çıktı: 96 üretilmiş
sorudan 14'ü bankada zaten sorulan bilgiyi soruyordu. Dili karışık bir derste
karşılaştırmayı iki dilde yap (`text_en` / `text_tr` sütunları) ve adayları tek tek oku.

**Üretilmiş soru gerçek bir soruyla aynı bilgiyi soruyorsa gerçek soru kanoniktir**,
üretilmiş olan ona bağlanır. Gerçek sorular (ATPL TV ve ders notu) hiçbir zaman
üretilmiş bir soru yüzünden gizlenmez; kullanıcı ikisinin de kalmasını istedi. Tekrar
sayılanlar:

- Aynı bilgiyi **ters yönden** sormak (16388 "manyetik baş hangi Q kodu" / 90907 "QDM nedir").
- **Kural ve örnek**: kuralı soran ile onu bir örneğe uygulayan (16345 TC-ABC → T-BC /
  90937 Tip 1 kısaltma kuralı; 16322 / 90926 saatte yalnız dakika).
- **"Hangisi değildir" biçimi**: doğru şıkları tam olarak başka bir sorunun cevabı olan
  soru (16430 CAVOK tanımı / 90920 CAVOK'un parçası olmayan; 59007 / 90903 ATS amacı).
- Bir kuralın iki yüzü (16352 tehlike çağrısı o anki frekansta / 90959 121.5 ne zaman).
- Üretilmişler arasında da aynı ölçü: kapsamlı olan ya da kuralı soran kalır, dar olan
  ya da örnek olan gizlenir (90922 / 90943, 90948 / 90976).

Cevabı farklı olanlar yine tuzaktır, bağlanmaz: 90948 (fit, ×1.25) / 90949 (uçuş
seviyesi, ×12) birbirinin çeldiricisi. Yalnız konusu aynı olan da bağlanmaz: 90915 ATIS
yayınının içeriğini sorar, 16454 ATIS'in ne olduğunu — ayrı bilgi.

090'da iki tur inceleme yapıldı (2026-09): önce iki dilde benzerlik adaylarıyla, sonra
82 görünür üretilmiş sorunun 203 gerçek soruyla tek tek karşılaştırılmasıyla. Sonuç:
96 üretilmişin 25'i gizli, 71'i bankada ve ders notu sorularında sorulmayan bir bilgiyi
soruyor — çoğu B3/B4'teki VHF tekniği (yayılım, menzil, 8.33 kHz, parazit, anten,
frekans yönetimi); ATPL TV bankasında bu konularda yalnız 4 soru var.

**Kaynakta çelişki:** ders notu antenler için hem "büyük uçakta kuyrukta dikey
stabilizatörde" (B3) hem "gövdenin üst ve alt kısmında" (B4) diyor; 90972 ve 90995 bunları
ayrı ayrı soruyor. Gerçekte VHF antenleri gövdededir, kuyruktaki çoğunlukla HF'dir. Sınav
notu izlediği için sorular olduğu gibi bırakıldı.

Yan etkisi bilinerek kabul edildi: kanonik İngilizce bankadaysa (090-01…06), yalnız
"Ders Notundan Üretilmiş" (090-U) seçiliyken o bilgi turda hiç çıkmaz; modülün tamamı
seçiliyken kanonik soru gelir. 090'ın ders notu soruları (590xx, gerçek SHGM soruları) İngilizce
bankaya bilerek bağlanmadı. 070'te 90725/90726, 502'de 95257 aynı durumda ama henüz
bağlanmadı — kullanıcı yalnız 090'ı istedi.

## Çalışma uygulaması (`web/`)

Asıl kullanılan sürüm bu: tek dosya, sunucusuz, `localStorage` tabanlı.

Varsayılanlar `DEFAULTS` sabitinde: `deck:'new'` (çözülmemişler), `count:0` (sınırsız tur),
`pick:{}` (**tüm banka**).

**Kapsam varsayılan olarak bütün bankadır.** Açılışta modül daraltması yapılmaz —
`autoPickModule()` yalnız "Sıradaki modüle geç" ve geçilen ders işaretlemesinde çalışır.
"Başla" tek turda kapsamdaki bütün soruları açar; bölüm bölüm ya da 20'şerlik turlara
bölme yoktur (tur uzunluğu Ayarlar'dan isteyerek daraltılabilir, varsayılanı Tümü).
Kullanıcı bunu açıkça istedi; modül odaklı eski akışa geri döndürme.

Sayaçlar **toplam / çözülmemiş** okur (çözülen/toplam değil): kimlik satırında
`G.total`/`G.total - G.seen`, kapsam kutusunda `total` ve `counts['new']`.

Ekran üç katmandır ve bu sırayı koru: (1) `.idline` — avatar + ad + toplam istatistik,
tek satır, dokunulunca Durum paneli; (2) `.hero` — ilerleme halkası (`ringSvg`) + modül
kutusu + **tek** birincil düğme; (3) `.chiprow` — deste çipleri, sayısı sıfır olan deste
hiç çizilmez. İlk ziyarette (`G.seen === 0`) hero "Hoş geldin" sürümüne düşer ve çip
satırı gizlenir. Ana ekranı sayı yığınına çevirme — kullanıcı tek birincil eylem istedi.

**Yarım kalan tur varken birincil eylem "Devam et"tir, "Başla" değil.** Hero'nun eylem
satırını tek bir yer üretir: `home()` içindeki `hact(label, disabled)`. `openRun()` bir
tur döndürüyorsa `#go` "Devam et" olur (alt satırında turun adı ve `runSeen`/`n0`
sayacı, `.gsub`) ve `resumeRun` çağırır; yanında ikincil `#goNew` "Yeni tur" durur.
`#goNew` `yeniTur` bayrağını kaldırıp seçiciyi açar: kullanıcı kapsamı **eliyle** seçer,
`#go` o zaman "Başla · N soru" olur, yanında `#goBack` "Vazgeç" ile eski turuna döner.
Bayrak `start()` ve `resumeRun()` içinde sıfırlanır. Kaldığı yerde 266 soru kalmış
kullanıcıya "Başla · 266 soru" demek turu baştan başlatıyordu; bu düzeni bozma.

`.gsub` adı bilerek `.sub` değil: genel `.sub` kuralı rengi `--ink-2`'ye çeker ve alt
satır pembe düğme üzerinde okunmaz olur.

**Konu seçimi ayrı bir bölüm değil.** Modül kutusuna (`modPick`, `#mPick`) dokununca
altında `#picker` açılır; kapsam yalnız oradan seçilir. Ayrı "Konular" akordeonu isteme,
kullanıcı açıkça kaldırttı. Seçici içinde iki ayrı davranış var, ikisini de koru:
modül/bölüm **adına** dokunmak (`data-solo`) seçimi tek başına ona alır ve seçiciyi
kapatır (dropdown gibi), **kutucuğa** (`data-s`) dokunmak çoklu seçim yapar ve seçici
açık kalır. `pickOpen` durumu `home()` yeniden çizimleri arasında korunur.

**Tur içinde gezinme.** `R.orders[i]` her sorunun şık sırasını, `R.picks[i]` verilen
cevabı tutar; ikisi de indeks bazlı olduğu için geri gidince şıklar yeniden karışmaz ve
cevap görünür kalır. `pick()` `R.picked !== null` ise erken döner — geri gidip yeniden
cevaplamak **çift puanlamaz**. Yeni yanlış turunda `orders`/`picks` sıfırlanır.
`resumeRun` cevapları `R.log`'dan geri kurar: kayıtta kaynak şık indeksi durur, yeni
karıştırmadaki karşılığı `orderFor(i).indexOf(...)` ile bulunur.

`goTo(i)` / `prevQ()` / `nextQ()` konumu değiştirir ve bekleyen otomatik geçişi iptal
eder. `nextQ` son soruda turu kazara bitirmez — ancak cevap verilmişse `next()`'e düşer.

**Parmakla kaydırma** telefonda tek gezinme yoludur: sola sonraki, sağa önceki soru.
Dikey kaydırmayı bozmamak için hareket yatay baskın (1.5 kat), 55 pikselden uzun ve
800 ms'den kısa olmalı; `.navpop`, `.figbox`, form alanları ve açık Durum paneli
dışlanır. Kaydırma sonrası 400 ms boyunca şık tıklaması yok sayılır (`sonKaydirma`) —
yoksa parmağın kalktığı şık seçilmiş olurdu. Bunu kaldırma, ok tuşları telefonda yok.

**Klavye:** `A`–`E` ve `1`–`5` cevaplar, `←` `→` soru değiştirir, `Home`/`End` başa ve
sona gider, `Enter` devam eder, `S` yıldızlar, `P` tur sayacını durdurup sürdürür,
`Esc` açık paneli kapatır.

**Etkin süre.** Süre yalnız sen sayfadayken sayılır: sayfa görünür olmalı ve iki
etkinlik (dokunma, tuş, fare, kaydırma) arası `BOS_MS` (3 dk) geçmemeli. Geçerse aradaki
sürenin **hiçbiri** sayılmaz (başından kalktın), geçmezse **tamamı** sayılır (soruyu
düşünüyordun). Sayaç açık aralığı da gösterir, `BOS_MS` dolunca o kısım geri düşer ve
çip `.bosta` olur. Kullanıcı "bilgisayarı bırakıp gidince saymasın" dedi; eşiği
büyütürsen gidilen süre sayılır, küçültürsen düşünme süresi kaybolur.

- Dinleyiciler `window`'da **yakalama evresinde**: aralık, tıklamanın değiştireceği
  durumdan (tur açık mı, sayaç durdu mu) önce kapanmalı. `pointerdown`/`keydown` hemen,
  fare ve kaydırma seli saniyede bir işlenir (`etkinlik`).
- Gizlenişte ve `pagehide`'da `sureBirak()` aralığı kapatır ve `sonEtkin`'i siler —
  gizliyken geçen süre sayılmaz. "Sor" ile açılan sohbet sekmesinde geçen süre de
  sayılmaz; kullanıcı "sayfada aktif olduğumuz süre" dedi.
- **Tur sayacı** soru ekranının üst satırındaki `#tmr` çipidir: `R.sure` (ms) ve elle
  durdurma `R.durdu`, ikisi de tur kaydında (`rec.sure`, `rec.durdu`) saklanır, sayfa
  yenilenince ve başka cihazda sürer. Elle durdurma yalnız turu durdurur, toplam süre
  saymaya devam eder. Simge yapılacak eylemi gösterir ve CSS ile çizilir — iOS ⏸'yi
  renkli emojiye çeviriyor.
- `sureYaz()` tur kaydına süreyi yazarken `tN`'ye dokunmaz; birleştirmede turun ilerlemesi
  ölçülürken yalnız süre değişikliği sayılmasın.
- **Rapor ve geçmiş satırı** etkin süreyi ve soru başına ortalamayı yalnız `sureTam`
  turlarda yazar (sayaç baştan beri açık). Sayaçtan önce başlamış turun eski cevapları
  zamanlanmadığı için ortalama yanıltıcı çıkıyordu; o turlar duvar saatine düşer.
- **Boşta süre** (kullanıcı "ekran açık kaldı, ne kadar boşa harcadım" diye istedi): sayfa
  görünür ve bilgisayar uyanıkken `BOS_MS`'den uzun hiç dokunulmayan aralık. Saniye tıkı
  (`tik`) uyanık süreyi `bekBos`'ta biriktirir; aralık kapanırken `BOS_MS`'yi aşmışsa bu
  kısım `bosEkle` ile boşta sayılır. Görünürken iki tık arası `UYKU_MS`'yi (5 sn) aşarsa
  bilgisayar uyudu ya da sayfa dondu demektir: aralık uykudan önceki son tıkta kapanır,
  uyku ne çalışma ne boşta sayılır. Görünür olunca `sonTik` de sıfırlanmalı, yoksa arka
  planda seyrekleşen tık sahte uyku sanılır. Elle durdurulmuş turda boşta tura yazılmaz.
- **Aralık, kapandığı andaki duruma yazılır** (tur açık mı, durdu mu). Doğruluğu yakalama
  evresindeki `pointerdown`/`keydown` sağlar: tıklama durumu değiştirmeden önce aralık
  kapanır. `home()` gibi programla yapılan geçişlerde `etkinKapat` **çağırma** — eşitleme
  ekranı tazeledikçe boşluk 3 dakikadan kısa parçalara bölünür ve boşta hiç yakalanmaz.
  Testte `.click()` `pointerdown` üretmez; önce `PointerEvent('pointerdown')` gönder.
- **Ekranda:** soru ekranında ilerleme çubuğunun yanında `#tstat` "boşta · toplam"
  (bu tur; toplam = çalışma + boşta, dikeyde yer yemesin diye çubukla aynı satırda),
  kimlik satırında toplam çalışma süresi ("12 sa çalışma"; dar ekranda satır sarılır),
  Durum panelinde boşta bugün / son 7 gün / toplam, tur raporunda turun boşta süresi
  (yalnız `bosTam` turda — boşta ölçümü baştan beri açık).
- **Soru başı ortalama** iki sayacın yanında: tur sayacının solunda `#tort` çalışma
  süresine göre, `#tstat`'ın sonunda toplam (çalışma + boşta) süreye göre. Bölen, taban
  anından beri verilen cevap sayısıdır (`R.log.length - ort0.n`). `rec.ort0 = {n, s, b}`
  yeni turda sıfırdır; süre ölçümü baştan açık olmayan eski tur ilk açıldığında o anki
  cevap sayısı ve süreler taban alınır — eski cevaplar zamanlanmadığı için ortalamaya
  karışsalar ortalama yanlış çıkardı. İlk cevaba kadar ortalama gizli. Yer açmak için
  400 piksel altında üst satırdaki "Soru" kelimesi düşer (`.qw`); sıra alt şeritte de
  yazıyor. 360 pikselde ölçüldü: satır 332 pikselin 274'ünü kullanıyor.
- **Toplam süre** `S.sure[cihaz] = {t, g:{gün: ms}}` içinde, boşta süre `S.bos[cihaz]` aynı
  biçimde; cihaz kimliği `atpl.cihaz`.
  Her cihaz yalnız kendi sayacını artırır; `mergeState` cihaz bazında **en büyüğü** alır,
  toplam hepsinin toplamıdır. Tek sayıyla tutup en büyüğü almak, telefon ve bilgisayarın
  aynı gün çalışmasında birini silerdi; toplayarak birleştirmek her eşitlemede ikiye
  katlardı. Gün kayıtları 120 günde budanır. Durum panelinde bugün / son 7 gün / toplam.

**Şık vurgusu imleç kıpırdayınca açılır.** Yeni soruda, son dokunulan yerdeki ya da
hareketsiz imlecin altındaki şık "seçili" gibi yanıyordu; kullanıcı bunu "odak kalıyor"
diye bildirdi. Gerçek odak değildi, üzerine gelme vurgusuydu. `.opt:hover` artık yalnız
`@media (hover:hover) and (pointer:fine)` içinde ve `.opts.hov` iken çalışır: `draw()`
imlecin o anki yerini `hovCapa`'ya alır, fare oradan 4 pikselden fazla kıpırdayınca
`.hov` eklenir. Kuralı düz `.opt:hover`'a geri çevirme.

**Dikey yer ölçülüdür.** Soru ekranı uzun metinli sorularda ekrandan taşmasın diye
sıkı tutuluyor: sayfa alt boşluğu 24px (eylem şeridi zaten `position:sticky`, altında
80px ölü alana gerek yok), `.qt` 14px üst boşluk, `.opts` 9px/6px, `.opt` 10-11px iç
boşluk. Yazı boyutları küçültülmedi — okunurluk sınavda önemli. Bu değerleri büyütmeden
önce 375×812'de uzun bir soruyla (ör. 14634) ölç: aynı 30 soruda kaydırma gerektiren
soru 13'ten 2'ye inmişti.

**Gezinme alt şeritte, dikeyde bedava.** `.foot` sticky kutusu iki şeyi sarar: açılır
`#navPop` ve eylem satırı `.acts`. Eylem satırının solunda `.navgrp` durur — `◀`,
`#navBtn` (`4/2547`), `▶` — yani önceki/sonraki her zaman görünür ve başparmağın altında,
ama **yeni satır açmaz**, eylem düğmeleriyle aynı yüksekliği paylaşır. `#navBtn` panelı
açar (`navOpen`, çizimler arası korunur): ilk/önceki/sonraki/son, numara kutusu ve "Git".
Panel `.acts`'ın hemen üstünde açılır; "Git" tek atımlık olduğu için `navGo` paneli kapatır.
Üst satırdaki sayaç artık salt bilgi (`.qpos`), düğme değil.

Kullanıcı ilk turda bu düğmeleri bulamadığını söyledi — görünürlüğü geri alma. Ama
kalıcı **ikinci** bir çubuk da ekleme; kural "hep görünür ama fazladan satır yok".
`Atla` düğmesi kaldırıldı: `▶` zaten cevaplamadan geçiriyor ve son soruda turu kazara
bitirmiyor (`nextQ`).

Bağlama `el('view').querySelectorAll('[data-nav]')` üzerinden yapılır — düğmeler iki
yerde (şeritte ve panelde), seçiciyi `#navPop` ile daraltma.

**Soruyu yapay zekâya sorma.** Kart başlığındaki `Sor` düğmesi (`askBtn`) soruyu,
gördüğün sıradaki şıkları, doğru cevabı ve verdiğin cevabı düz metne çevirip
(`askText`) panoya kopyalar ve seçilen sohbeti yeni sekmede açar. Düğme gerçek bir
`<a target="_blank">`; `window.open` sandbox'ta engellenebiliyor. Sağlayıcı `AI`
sözlüğünde (ChatGPT varsayılan; Claude, Gemini, Grok, Perplexity, Google), seçim
`F.ai` ile Ayarlar'dan yapılır.

**Satır içi API eklemeyi deneme.** Bu dosya herkese açık statik bir sayfa olarak
yayınlanıyor; API anahtarı gömmek anahtarı sızdırır ve faturayı kullanıcıya keser.
Artifact çalışma zamanının yetenekleri de (`artifact`, `downloads`, `mcp`, `self`)
dil modeli çağrısı içermiyor. Kopyala-ve-aç yolu bilinçli tercihtir.

Şekil gerektiren soruda metne "şekil metne aktarılamadı" notu eklenir — yoksa model
görmediği bir çizim hakkında uydurur. Adres `URL_MAX`'i aşarsa düğme yalnız kopyalar.

**Geri bildirim.** `feedback(ok)` kartta tek atımlık renk vurgusu (`fok`/`fbad`/`fnew`)
ve `beep()` ile WebAudio notası çalar; ses dosyası yoktur. `prefers-reduced-motion`
açıksa animasyon çalışmaz. **Sınav modunda ses ve renk nötrdür** (`fnew` + tek nota) —
aksi hâlde doğru cevabı ele verir. `F.sound` Ayarlar'dan kapatılır.

**Geçilen sınavlar.** `S.passed` profil bazında geçilen ders kodlarını tutar. Geçilen
ders kapsamdan tümüyle çıkar: `inScope` ve `inToggles` `notPassed(q)` ile eler, dolayısıyla
toplam sayı, deste sayaçları, konu seçici, `openModules`/`autoPickModule` ve turlar
otomatik olarak dışlar. İşaretleme Durum panelindeki **Geçtiğim sınavlar** çip listesinden
yapılır; konu seçicideki `#tPass` düğmesi oraya götürür. `inToggles(q, withPassed)` ikinci
parametreyle geçilenleri de sayar — yalnız o listenin kendi sayıları için kullanılır.

> `inToggles`/`inScope` gibi ikinci parametre alan yüklemleri `filter()`'a **çıplak verme**;
> `Array.filter` ikinci argüman olarak indeksi geçirir ve süzgeç sessizce devre dışı kalır.
> Her zaman `filter(q => inToggles(q))` yaz.

Geçilen ders seçili kapsamdaysa `togglePassed` onu düşürür ve `autoPickModule()` ile yeni
modüle geçer. Hepsi geçilirse ana ekran "Hepsini geçtin" boş durumuna düşer — o durumda
`#mPick` ve `#tree` çizilmez, `buildTree` erken döner.

**Turlar kalıcıdır.** Her `start()` bir kayıt açar (`S.runs`, en yeni başta, `RUN_MAX`
tane tutulur). Her cevapta ve her soru geçişinde `saveRun()` çalışır; sekme gizlenince
`flush()` bekleyen yazmayı hemen diske indirir. Açılışta `S.runs[0]` bitmemişse uygulama
doğrudan o soruya döner — ana ekrana uğramaz. Soru ekranındaki **`‹ Ana ekran`**
(`#hb`, `.backb`) turu **kapatmaz**, ana ekrana döner; `Turu bitir` (`#quit`, `.go3`)
kapatır ve raporu çizer.

**Soru ekranındaki ağırlık sırası: Sonraki > gezinme takımı > Turu bitir.** Geri düğmesi
çerçeveli ve etiketli (`.backb`, dar ekranda etiket kalır, yerine deste adı gizlenir);
`Turu bitir` sessiz üçüncül (`.go3`: çerçevesiz, 12px, `--ink-3`) ama dokunma alanı
korunur. Kullanıcı tersini şikâyet etti — geri dönüşü görünmez, turu bitirmeyi göz
önünde bulan düzene geri dönme.

`.acts .go` **tek satırda kalmalı** (`white-space:nowrap`): "Anladım, devam" 375px'te
sarınca alt şerit 70px'ten 95px'e çıkıyor ve soruya kalan yer daralıyor. 420px altında
yazı 15px'e, `.navgrp`/`.go3` iç boşlukları birer punto küçülür. Bu ölçüleri değiştirirsen
375×812'de "Anladım, devam" ile yeniden ölç.

`openRun()` cevaplanmış turu öne alır, `dropEmptyRun()` (geri düğmesinde) hiç cevap
verilmemiş turu kayıttan düşürür: yeni açılıp bırakılan boş tur ana ekranda gerçek
yarım turun önüne geçmesin.

Bitmemiş tur artık hero'nun birincil düğmesidir; `.resume` şeridi yalnız "hepsini
geçtin" boş durumunda çizilir (hero orada başka iş yapıyor). Tüm turlar
`Geçmiş` akordeonunda listelenir (`hisRow`): biteni açmak raporu gösterir (`report(rec,
false)` — "Devam et" düğmesi yalnız `live` iken çizilir), bitmeyeni açmak `resumeRun()`
ile kaldığı yerden sürdürür. Biten turların `ids`/`missed` alanları silinir, geri
yüklenmezler. Hiç soru çözülmeden bırakılan turlar bir sonraki `start()`'ta atılır.

İlk ziyarette `randomName()` rastgele bir profil adı üretir ve profil kendiliğinden açılır;
giriş yoktur. Google ile giriş yapılırsa profil hesabın ad soyadına döner (aşağıya bak).
Ad Durum panelinden değiştirilir (`renameProfile` localStorage anahtarını taşır). Aralıklı tekrar
kutuları `BOX_MS`, takılma eşiği `LEECH`, yanlış defterinden çıkış `MASTER` sabitleriyle
ayarlanır. Kaynak `web/template.html`; `__DATA__` yer tutucusuna `build_web.py` veriyi
gömer. Değişiklikten sonra `python3 scripts/build_web.py` çalıştır.

Yedekleme metin kopyala/yapıştır üzerinden yapılır — artifact kum havuzunda dosya
indirme engelli. Dosya düğmeleri yalnızca `window.self === window.top` iken gösterilir.

## Şekiller

Şekil gerektiren sorular (`questions.needs_figure = 1`) için çizimler `figures/` altında
SVG olarak durur; `figures/index.json` soru id'sini çizim adına bağlar, birden çok soru
aynı çizimi paylaşabilir.

```bash
python3 scripts/make_figures.py    # figures/*.svg + index.json üretir
python3 scripts/check_figures.py   # figures/_kontrol.html — geriye doğru teyit sayfası
```

`make_figures.py` çizimlerin tek kaynağıdır — SVG dosyalarını elle düzenleme, betiği
düzelt. Çizim kuralı: **beyaz zemin, siyah çizgi, temel şekiller** (doğru, daire, elips,
üçgen, yay); gri yalnız zemin dolgusu gibi ayırt etmesi zorunlu yerlerde. Uygulamada
`.figbox` beyaz kalır, koyu temada basılı bir şekil gibi durur.

**Yeni çizim eklerken teyit zorunlu:** `check_figures.py` her çizimi sorusunun ve doğru
şıkkının yanına koyar; şekle bakıp cevabın çizimden okunabildiği doğrulanır. Çizimi
olmayan soru kalırsa betik hata verir, `build_web.py` de uyarı basar.

**Şekil süzgeci kaldırıldı.** Hepsi çizildiği için `hideFig` tercihi yok; şekil gerektiren
hiçbir soru gizlenmiyor. Eski kayıtlardaki `hideFig` `loadProfile`'da siliniyor. Çizimi
olmayan bir soru eklenirse kartta "şekil gerekli" rozeti çıkar — o zaman çizimini üret.

## Soru üretimi

Kullanıcı ders notu verdiğinde iş akışı:

1. Notu `notes/` altına koy, `python3 scripts/build_web.py` ile uygulamaya göm
2. `python3 scripts/topic_gap.py notes/<dosya>.md <ders>` ile boşlukları çıkar
3. Gerçekten soru gereken konulara karar ver (betik yalnızca aday listeler)
4. Soruları `data/<ders>_uretilmis_sorular.json` içine yaz — **`"origin": "uretilmis"`
   alanı zorunlu**, ID'ler mevcutlarla çakışmasın, doğru cevap ilk şık olsun
5. `python3 scripts/init_db.py && python3 scripts/build_web.py`

Üretilmiş sorular uygulamada "üretilmiş" etiketiyle görünür ve kapsam anahtarından
kapatılabilir; gerçek sınav sorularıyla asla karıştırılmaz.

**Üretilmiş sorular kendi bölümünde durur: "Ders Notundan Üretilmiş"** (İngilizcesi
"Generated from Course Notes", `data/en/_dersler.json`). Ders notu soruları ayrı
bölümde kalır: 070-06 / 070-07, 01-02 / 01-03, 090-B1…B4 / 090-U. Kod, konu seçicide ders
notu bölümlerinin **arkasına** düşecek biçimde seçilir (bölümler koda göre sıralanır;
090'da `-07` B'lerin önüne düşerdi, o yüzden `-U`). 090'da üretilmişler önce B1–B4'e
karışmıştı ve kullanıcı konu seçicide onları ayrı bulamadığını söyledi. Konuya göre
kimlik aralıkları dosyanın `id_convention` alanında yazılı. Seçim bölüm **koduyla**
saklandığı için (`F.pick`), yeni bölüm eklemek kayıtlı seçimleri bozmaz.

502 bu kurala henüz uymuyor: 118 üretilmiş soru, 25 SHGM örnek sorusuyla aynı GB-01…05
konu bölümlerinde. Kullanıcı yalnız 090'ı istedi; 502'ye dokunmadan önce sor.

**İki dil kuralı (her yeni soru dosyası için).** Uygulama iki dilli; her sorunun iki
karşılığı olmalı, yoksa seçili dil ne olursa olsun kaynak dilinde görünür ve kip içinde
dil karışır. Türkçe yazılmış ders notu/üretilmiş dosyaya dosya düzeyinde `"lang": "tr"`
koy, İngilizcesini `data/en/<dosya-adı>_01.json` (65'lik parçalar, `{"questions":
{"<id>": {"text", "options"}}}`) olarak yaz; İngilizce kaynaklı dosya için tersi
`data/tr/`. Yeni bölüm kodlarının diğer dildeki adını `data/en/_dersler.json` ya da
`data/tr/_dersler.json` içine ekle. `python3 scripts/check_tr.py` ikisini de doğrular —
"toplam N/N ✓" görmeden gönderme. Şıkların sırası kaynakla birebir aynı kalmalı; doğru
cevap ilk şık olduğu için kayan bir çeviri yanlış şıkkı doğru yapar.

## Bulut (Google girişi)

Firebase Auth + Firestore. Yapılandırma `web/firebase-config.json`, `build_web.py`
`__FIREBASE__` yer tutucusuna gömer; dosya yoksa `null` gömülür ve `Cloud.acik` false
kalır — uygulama yalnız `localStorage` ile çalışır. Kurulum `scripts/setup_firebase.sh`,
kurallar `firestore.rules`.

**`web/firebase-config.json` depoya girer ve herkese açıktır, bu doğrudur.** Firebase web
yapılandırması sır değildir; erişimi kurallar kısıtlar (`request.auth.uid == uid`). Bunu
"sızmış anahtar" sanıp gitignore'a ekleme — eklersen derleme bulutu kapatır.

**Her Firestore çağrısı `sureli()` ile sınırlanmalı (12 sn).** Sınır kaldırılırsa
`mesgul` bayrağı takılıp arayüz "Eşitleniyor…"da asılı kalır — bu bir kez yaşandı.
Söz iptal edilmez: zaman aşımından sonra da Firestore yazmayı kuyrukta tutar, sunucu
onaylayınca `gonder()` içindeki `soz.then` durumu kendiliğinden düzeltir. Bağlantı
`initializeFirestore(..., { experimentalAutoDetectLongPolling: true })` ile kurulur;
WebChannel'ın kurulup yanıt döndürmediği ağlarda XHR'a düşmesi için gerekiyor.

Arka plan eşitlemesi ekranı boşuna tazelememeli: `cek()` yalnız aktif profilde gerçek
bir değişiklik olduğunda `true` döner, `esitle()` `home()`'u yalnız o zaman çağırır.

**Gönderim tetikleyicileri eksiksiz olmalı.** `flush()` yalnız 4 sn'lik zamanlayıcı
kurar; sekme kapanırken o zamanlayıcı ateşlenmez. Bu yüzden `pagehide` ve
`visibilitychange`→hidden `Cloud.simdiGonder()` çağırır, çıkıştan önce bekleyen
gönderilir, profil değiştirme/ad değiştirme/sıfırlama bulutu da günceller. Bu
kancalardan birini kaldırırsan sessiz veri kaybı olur.

`Cloud.gonder(ad, veri)` profil adını dışarıdan alır: `switchProfile` eskisini `ME`
değişmeden yakalayıp yollar. `Sıfırla` bulut belgesini de siler — yoksa ilk eşitlemede
veri geri gelir.

**Giriş yapan hesap profili sahiplenir.** `onAuthStateChanged` içinde `bindAccount(u)`
çalışır: profil adı Google'daki **ad soyad** olur (yoksa e-postanın kullanıcı adı, 28
karakterde kesilir), avatar `u.photoURL` olur ve bundan sonraki her kayıt — çözülen
soru, ayar, tur, geçilen sınav — bu profile, yani hesaba yazılır.

- Misafirken çözülenler kaybolmaz: profil **yeniden adlandırılır** (`renameProfile`),
  veri olduğu gibi taşınır. Hesabın profili bu tarayıcıda zaten varsa ona geçilir ve
  misafir profili yerinde bırakılır.
- Girişteki yeniden adlandırma buluta **hemen yazmaz** (`renameProfile(…, true)`):
  hesabın belgesinde başka cihazın verisi olabilir, `setDoc` onu ezerdi. Ardından gelen
  `esitle()` önce çeker, kaynaştırır, sonra gönderir. Bu üçüncü parametreyi kaldırma.
**Giriş üst çubukta durur** (`#bLogin`, Google logolu "Giriş"), Durum panelinde
aranmaz; girince gizlenir. `paintCloud()` görünürlüğü yönetir.

Girişten sonra gelen bulut ilerlemesi ekranı tazeler: `esitle()` değişiklik varsa
`home()`'un yanında `refreshSheet()` de çağırır — açık Durum paneli eski sayılarla
kalmasın (kaydırma konumu korunur). Ayrıca `girisSonrasi` bayrağı ile bir kez
`reselectAfterSync()` çalışır: başka cihazda bitirilmiş bir modül seçiliyse en son
çalışılan ve soru kalan modüle geçer. İçinde iş kalan modüle ve elle kurulmuş çoklu
kapsama dokunmaz — seçim kullanıcınındır.

- Bağ uid başına `atpl.acct:<uid>` içinde durur. Girişten sonra adı elle değiştirirsen
  bağ yeni ada taşınır ve sonraki giriş adı geri almaz; profil değiştirirsen hesap
  artık o profile yazar.

**Profil resmi yerelde durur** (`atpl.pics`, ad → adres); buluta gönderilmez, çünkü her
cihaz kendi girişinde aynı adresi zaten alıyor. `avatar()` baş harfleri yazar ve resmi
üstüne serer; resim yüklenemezse `onerror` img'yi silip `pic` sınıfını kaldırır, baş
harfler geri gelir. Çıkışta resim düşer, ad ve veri yerelde kalır.

**Turlar zaman damgasına göre birleştirilmez, ilerlemeye göre birleşir** (`runIleri`):
önce cevaplanmış soru sayısı, eşitse biten kayıt, sonra konum, en son `tN`. Zaman damgası
ölçü alınınca şu oluyordu: açılışta yerel tur `resumeRun` → `step0` → `saveRun` ile
`tN`'sini tazeliyor, böylece başka cihazdaki gerçek ilerlemeyi yeniyor **ve onu buluta
geri yazarak siliyordu**. `runIleri`'yi tekrar `tN`'ye indirgeme.

Açılışta yerel tur hemen sürdürülür, bulut yanıtı sonra gelir; bu yüzden `esitle()`
değişiklik gördüğünde tur içindeysek `adoptRun()` çağırır: kayıt daha ileriyse
`resumeRun` ile o konuma geçilir, başka cihazda bitirilmişse ana ekrana dönülür.

Eşitleme çakışma çözmez, **kaynaştırır**: `mergeState(hedef, gelen)` kart bazında daha çok
görülmüşü, gün sayaçlarında en büyüğü alır. Geçilen sınavlar
`S.pAt` zaman damgasıyla son yazana gider — birleştirmek kaldırılan dersi geri getirirdi.
Ayarlar da bir tercih kümesidir, birleştirilemez: `S.prefAt` damgasıyla son kaydeden
kazanır (`savePref` damgayı basar). Buluttan daha yeni ayar gelirse `merge()` `applyPref()`
çağırıp `F`'i tazeler — `S.pref === F` bağı orada yeniden kurulur, koru.
`flush()` yerel yazmayı `flushLocal()` yapar, ardından `Cloud.schedule()` ile 4 saniye
gecikmeli gönderir; Firestore yazma kotasını düşük tutar.

Artifact'ta bulut çalışmaz (kum havuzu dış kaynağı engeller); `Cloud.init()` yakalar,
`acik` false olur, kutu hiç çizilmez. Bu bilinçli — tek dosya iki yerde de çalışsın diye.

**Google sağlayıcısını API'den açmaya çalışma, yolu yok.** Denendi: Identity Platform
`initializeAuth` faturalandırma istiyor (o ücretli GCIP), `admin/v2/.../config` PATCH/POST
yapılandırma yokken 404 veriyor, IdP oluşturma `client_id` istiyor ve OAuth istemcisi
üreten genel bir API yok. Konsoldaki **Get started → Google → Enable** tıklaması bu
istemciyi üretiyor; tek elle adım budur. Ondan **sonra** izinli alan listesi
`admin/v2/.../config?updateMask=authorizedDomains` ile güncellenebiliyor ve betik bunu
kendisi yapıyor. `CONFIGURATION_NOT_FOUND` hatası "API anahtarı bozuk" demek değildir,
"projede Authentication hiç açılmamış" demektir.

## Sunucu (isteğe bağlı)

Çok cihazlı senkron isteyene FastAPI sürümü duruyor; günlük kullanım için gerekli değil.

```bash
./run.sh                                   # http://127.0.0.1:8778
.venv/bin/python server/test_flow.py       # uçtan uca test (20 kontrol)
```

Değişiklikten sonra testleri çalıştır. Kritik davranışlar:

- **Doğru cevap istemciye gönderilmez.** `/api/tur/{id}/soru/{idx}` yanıtında doğruluk
  bilgisi olmamalı; test bunu kontrol ediyor. Bu kuralı bozacak bir alan ekleme.
- **Giriş zorunlu değil.** Siteye giren herkes otomatik misafir hesabı alır
  (`ensure_user` middleware). Hesap oluşturmak misafiri *yükseltir*, yeni satır açmaz —
  geçmiş korunur.
- **Yanlış defteri:** yanlış → deftere girer, **üst üste iki doğru** → düşer
  (`db.MASTER_STREAK`).
- Kullanıcılar birbirinin turunu göremez; her sorgu `user_id` ile kısıtlıdır.

## Yayın ve kimlik

Depo `ppltr/ppltr.github.io` altında herkese açık; site
**https://ppltr.github.io/** adresinde yayında.

Adres bilerek kısa: organizasyon `ppltr`, depo adı `ppltr.github.io` olduğu için path
boş kalıyor. **İkisinden birini değiştirirsen adres uzar ya da kırılır.** Organizasyon
2026-08-22'de `xmlparser`'dan `ppltr`'ye çevrildi (eski ad serbest bırakıldı). Deponun
`eski-site-2020` dalında 2020'den kalma XML editor sitesi duruyor, silme.

**Yayın otomatik:** Pages kaynağı GitHub Actions (`.github/workflows/pages.yml`).
`web/template.html`, `atpl.db`, `scripts/build_web.py` ya da `notes/` değişip main'e
gidince site kendiliğinden derlenir. Veri değiştiyse `./deploy.sh "mesaj"` kullan
(init_db + build_web + commit + push).

**Commit kimliği bilerek nötrdür:** `PPL Soru Bankası
<noreply@ppl-soru-bankasi.invalid>`. `.invalid` ayrılmış bir TLD olduğu için commit'ler
hiçbir GitHub hesabına bağlanmaz. Depo yerel `git config` ile bu kimliği kullanır —
global kimliğe düşürme, kişisel ad/eposta depoya girmesin. Örnek metinlerde de kişi adı
kullanma.

## Dil

Arayüz, kod yorumları ve commit mesajları Türkçe. Soru metinleri kaynaktaki dilinde
(çoğu İngilizce) bırakılır — sınavda öyle çıkıyor.
