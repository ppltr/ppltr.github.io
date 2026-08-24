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

Sınav soruları kaynakta İngilizcedir ve **varsayılan dil İngilizcedir** — sınavda öyle
çıkıyor. Türkçesi `data/tr/*.json` içinde ayrı durur; kaynak dosyalara dokunulmaz.

```json
{ "questions": { "14227": { "text": "Soru?", "options": ["Şık 1", "Şık 2"] } } }
```

- **Şıklar sırayla eşlenir.** Kaynakta doğru cevap ilk şıktır; çeviri aynı sırayı
  taşımak zorundadır. Sayı tutmazsa `init_db.py` ve `check_tr.py` derlemeyi durdurur —
  sıra kayarsa yanlış şık doğru diye işaretlenirdi.
- Çevirisi olmayan soru Türkçe kipte de **İngilizce görünür**; yarım çeviri yüzünden
  soru kaybolmaz.
- Kaynağı zaten Türkçe olan dosyalar (501, 502, ders notu soruları) dosya düzeyinde
  `"lang": "tr"` taşır. Bunlar çeviri kapsamı dışıdır, "çevrilmedi" diye sayılmazlar.
- Ders/bölüm adları `data/tr/_dersler.json` içinde; karşılığı olmayan İngilizce kalır.

Çeviri eklendikten sonra:

```bash
python3 scripts/check_tr.py            # şık sayısı, boş/çevrilmemiş metin, çift id
python3 scripts/init_db.py && python3 scripts/build_web.py
```

Uygulamada tercih `F.lang` (`'en'` varsayılan), Ayarlar'daki **Soru dili** satırından
seçilir ve `S.pref` içinde saklanıp cihazlar arasında eşitlenir. Metin seçimi tek yerden
geçer: `qText(q)` / `qOpts(q)` / `subjName(s)` / `secName(sc)`. Soru metnini doğrudan
`q[3]`, şıkları `q[4]` diye okuma — dil süzgeci devre dışı kalır.

**İlerleme dilden bağımsızdır.** Kayıt soru **id'sine** bağlı; dili değiştirmek
çözülmüşleri sıfırlamaz ve aynı soruyu iki dilde iki kez sormaz. Şık dizilerinin uzunluğu
iki dilde aynı olduğu için tur ortasında dil değiştirmek cevap konumlarını da bozmaz.

Dışa aktarımda çeviri, soru satırının **10. ve 11. alanları**dır (`q[10]` metin,
`q[11]` şıklar) ve yalnız çevirisi olan satırda bulunur — çevirisiz sorular bugünküyle
aynı boyutta kalır.

## Tekrar grupları

`data/_tekrarlar.json` içinde her grubun ilk id'si kanonik, diğerleri `dup_of` ile
ona bağlanır. **Cevabı farklı olan benzer sorular tekrar sayılmaz** — onlar sınavın
en değerli tuzakları (ör. 15613 METAR'da true north / 15666 ATIS'te magnetic north).
Yeni ders eklerken hem metin benzerliğini hem de "cevabı aynı ama metni farklı"
çiftleri tara; karar insana ait.

## Çalışma uygulaması (`web/`)

Asıl kullanılan sürüm bu: tek dosya, sunucusuz, `localStorage` tabanlı.

Varsayılanlar `DEFAULTS` sabitinde: `deck:'new'` (çözülmemişler), `count:0` (sınırsız tur).
`pick` ilk açılışta `autoPickModule()` ile **rastgele bir modüle** ayarlanır.

**Ana ekran modül odaklıdır** — kullanıcı bütün bankayı tek düğmede açan bir akış
istemedi. Kart hangi modülde olunduğunu, ilerlemeyi ve kalan soruyu yazar; "Başla" o
modülü açar. Modül bitince "Sıradaki modüle geç" çıkar. Bunu bozup "Başla · 2265 soru"
gibi bir düğmeye dönme.

Ekran üç katmandır ve bu sırayı koru: (1) `.idline` — avatar + ad + toplam istatistik,
tek satır, dokunulunca Durum paneli; (2) `.hero` — ilerleme halkası (`ringSvg`) + modül
kutusu + **tek** birincil düğme; (3) `.chiprow` — deste çipleri, sayısı sıfır olan deste
hiç çizilmez. İlk ziyarette (`G.seen === 0`) hero "Hoş geldin" sürümüne düşer ve çip
satırı gizlenir. Ana ekranı sayı yığınına çevirme — kullanıcı tek birincil eylem istedi.

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

**Klavye:** `A`–`E` ve `1`–`5` cevaplar, `←` `→` soru değiştirir, `Home`/`End` başa ve
sona gider, `Enter` devam eder, `S` yıldızlar, `Esc` açık paneli kapatır.

**Gezinme paneli** soru sayacına (`#navBtn`) dokununca açılır (`navOpen`, çizimler arası
korunur): ilk/önceki/sonraki/son düğmeleri, numara kutusu ve "Git". Kapalıyken hiç yer
kaplamaz — kullanıcı kontrollerin arayüzü işgal etmesini istemedi, kalıcı bir gezinme
çubuğu ekleme.

**Soruyu yapay zekâya sorma.** Kart başlığındaki `Sor` düğmesi (`askBtn`) soruyu,
gördüğün sıradaki şıkları, doğru cevabı ve verdiğin cevabı düz metne çevirip
(`askText`) panoya kopyalar ve seçilen sohbeti yeni sekmede açar. Düğme gerçek bir
`<a target="_blank">`; `window.open` sandbox'ta engellenebiliyor. Sağlayıcı `AI`
sözlüğünde, seçim `F.ai` ile Ayarlar'dan yapılır.

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
doğrudan o soruya döner — ana ekrana uğramaz. Soru ekranındaki `‹` (`#hb`) turu
**kapatmaz**, ana ekrana döner; `Turu bitir` (`#quit`) kapatır ve raporu çizer.

Ana ekranda bitmemiş tur varsa kimlik satırının altında `.resume` şeridi çıkar. Tüm turlar
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
- Bağ uid başına `atpl.acct:<uid>` içinde durur. Girişten sonra adı elle değiştirirsen
  bağ yeni ada taşınır ve sonraki giriş adı geri almaz; profil değiştirirsen hesap
  artık o profile yazar.

**Profil resmi yerelde durur** (`atpl.pics`, ad → adres); buluta gönderilmez, çünkü her
cihaz kendi girişinde aynı adresi zaten alıyor. `avatar()` baş harfleri yazar ve resmi
üstüne serer; resim yüklenemezse `onerror` img'yi silip `pic` sınıfını kaldırır, baş
harfler geri gelir. Çıkışta resim düşer, ad ve veri yerelde kalır.

Eşitleme çakışma çözmez, **kaynaştırır**: `mergeState(hedef, gelen)` kart bazında daha çok
görülmüşü, gün sayaçlarında en büyüğü, turlarda son dokunulanı alır. Geçilen sınavlar
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
