# PPL Soru Bankası

SQLite tabanlı **PPL** soru bankası (ATPL TV'deki *PPL Turkey (English)* sınav
raporlarından çevrildi). Bankanın tamamı şu an PPL seviyesindedir; ATPL soruları
ileride eklenecek — `subjects.level` sütunu bunun için hazır (`ppl` / `atpl`). **2.514 soru, 10 ders** (226 tekrar işaretli → 2.288 benzersiz; 71'i ders notundan üretilmiş).

| Ders | Soru | Benzersiz | Bölüm |
|---|---|---|---|
| 050 \| Meteorology | 385 | 346 | 9 |
| 020 \| Aircraft General Knowledge | 347 | 325 | 24 |
| 501 \| Havacılığa Giriş | 252 | 251 | 3 |
| 040 \| Human Performance and Limitations | 251 | **210** | 9 |
| 060 \| Navigation | 245 | 231 | 14 |
| 080 \| Principles of Flight | 244 | **197** | 9 |
| 030 \| Flight Performance and Planning | 237 | 220 | 10 |
| 070 \| Operational Procedures | 193 | 183 | 7 |
| 090 \| Communications | 183 | **150** | 6 |
| 010 \| Air Law | 177 | 175 | 7 |

```
atpl.db                                 # veritabanı (script ile üretilir)
data/501_havaciliga_giris.json          # kaynak veri
data/070_operational_procedures.json
data/010_air_law.json
data/090_communications.json
data/020_aircraft_general_knowledge.json
data/030_flight_performance_and_planning.json
data/040_human_performance.json
data/050_meteorology.json
data/060_navigation.json
data/080_principles_of_flight.json
data/501_ders_notu_sorulari.json         # ders notu quiz soruları
data/070_ders_notu_sorulari.json         # 073 ders notu quiz soruları
data/501_uretilmis_sorular.json          # ders notundan üretilmiş (gerçek sınav sorusu değil)
data/070_uretilmis_sorular.json
data/_tekrarlar.json                     # elle doğrulanmış tekrar grupları
scripts/init_db.py                      # şema + içe aktarma
```

**Doğru cevap her soruda A şıkkıdır** — kaynak şıkları doğru cevap başta olacak
şekilde veriyor, bu sıra korunuyor.

## Kurulum / güncelleme

```bash
python3 scripts/init_db.py
```

Betik idempotenttir: JSON'u düzeltip tekrar çalıştırınca sorular güncellenir, çoğaltılmaz.

## Şema

| Tablo | Açıklama |
|---|---|
| `subjects` | Ders (`501` → Havacılığa Giriş) |
| `sections` | Ders bölümü (`01-01`) |
| `questions` | Soru; `id` = ATPL TV'deki soru ID'si, `explanation` kendi notların için boş, `flagged` kaynakta "Attention!" işaretli, `origin` = `banka`/`uretilmis`, `dup_of` = tekrarsa kanonik sorunun id'si, `needs_figure` = soru bir şekle atıf yapıyor |
| `options` | Şıklar; `ord` 1..5, `label` A..E, `is_correct` doğru cevap |
| `v_sorular` | Soru + doğru cevabı tek satırda veren görünüm |
| `questions_fts` | FTS5 tam metin arama |

`flagged = 1` olan 3 soru (14554, 15967, 16159) kaynakta "Attention!" ile işaretli —
kullanıcılar cevabı tartışmalı bulmuş. Bunlara körü körüne güvenme:

```bash
sqlite3 -box atpl.db "SELECT soru_id, soru, dogru_cevap FROM v_sorular WHERE soru_id IN (SELECT id FROM questions WHERE flagged=1);"
```

**Doğru cevap kuralı:** Kaynak rapor şıkları doğru cevap en başta olacak şekilde listeliyor. Bu yüzden her sorunun ilk şıkkı (`ord = 1`, `label = 'A'`) doğru kabul edildi. Bir soruda hata görürsen JSON'daki `options` sırasını düzelt ya da o soruya `"correct_index": 2` gibi bir alan ekleyip betiği tekrar çalıştır.

## Örnek sorgular

Bir sorunun tüm şıklarını görmek:

```bash
sqlite3 -box atpl.db "SELECT label, text, is_correct FROM options WHERE question_id=27142 ORDER BY ord;"
```

Rastgele 10 soruluk deneme (cevaplar gizli):

```bash
sqlite3 -box atpl.db "SELECT q.id, q.text, o.label, o.text FROM questions q JOIN options o ON o.question_id=q.id WHERE q.id IN (SELECT id FROM questions ORDER BY random() LIMIT 10) ORDER BY q.id, o.ord;"
```

Konu araması (tam metin):

```bash
sqlite3 -box atpl.db "SELECT q.id, q.text FROM questions_fts f JOIN questions q ON q.id=f.rowid WHERE questions_fts MATCH 'Annex';"
```

Doğru cevap listesi (cevap anahtarı):

```bash
sqlite3 -box atpl.db "SELECT soru_id, dogru_sik, dogru_cevap FROM v_sorular ORDER BY soru_id;"
```

## Çalışma notları

| Dosya | İçerik |
|---|---|
| [notes/501-ders-notlari.md](notes/501-ders-notlari.md) | 501 Havacılığa Giriş ders notları — 7 bölümün sınav odaklı özeti |
| [notes/501-ezber-listesi.md](notes/501-ezber-listesi.md) | 501 kısa ezber listesi — soru kelimesi → cevap |
| [notes/073-ders-notlari.md](notes/073-ders-notlari.md) | 073 Uçak Operasyonel Prosedürler ders notları — 070 bankasının ders karşılığı |
| [notes/070-cheat-sheet.md](notes/070-cheat-sheet.md) | 070 Operational Procedures özeti — sayılar, tanımlar, tuzaklar |
| [notes/annex-sifre.md](notes/annex-sifre.md) | ICAO Annex 1–19 rakam bağlama yöntemi |
| [notes/annex-kart-promptlari.md](notes/annex-kart-promptlari.md) | Annex kartlarının görüntü promptları |

## Annex ezber kartları

`cards/annex-01.png … annex-19.png` — her ICAO Annex için rakamın şeklini konuya
gömen görsel kart. `cards/00-kontak-sayfasi.png` hepsini tek sayfada gösterir.

Promptlar [notes/annex-kart-promptlari.md](notes/annex-kart-promptlari.md) içinde.
Yeniden üretmek için (yerel `grok` CLI'yi ve senin Grok kotanı kullanır):

```bash
python3 scripts/generate_cards.py            # eksik kartlar
python3 scripts/generate_cards.py --force 17 # tek kartı yeniden üret
```

Bir kart ~20 saniye. Rakam görünmüyorsa prompt'a "A giant numeral N ... clearly
readable" kalıbını ekleyip `--force` ile tekrar üret — ilk turda 1, 2, 6 ve 17'de
rakam çıkmamıştı, bu kalıpla düzeldi.

## Video kartlar

`videos/annex-01.mp4 … annex-19.mp4` — her kartın 6 saniyelik animasyonlu hali
(544×544, 24 fps, ~1–2 MB).

```bash
python3 scripts/generate_videos.py            # eksik videolar
python3 scripts/generate_videos.py --force 15 # tek videoyu yeniden üret
```

**Grok CLI'nin `image_to_video` aracını kullanma** — ZDR hesaplarında şu hatayı verir:

```
HTTP 400 invalid-argument:
"Zero Data Retention teams must provide output.upload_url for video generation."
```

Bunun yerine `~/.grok/bin/grok-image-to-video` script'i doğrudan
`https://api.x.ai/v1/videos/generations` API'sine gidiyor ve aynı hesapla sorunsuz
çalışıyor (yanıt `zdr=false` dönüyor). `scripts/generate_videos.py` bu script'i çağırır.
Video başına ~30 saniye.

### Tek dikey video (reel)

`videos/annex-reel.mp4` — 19 klibin tamamı sırayla, 1080×1920, 103 saniye, 31 MB.
Üstte "ANNEX N", altta Annex adı ve hatırlama çengeli, geçişlerde 0,6 sn crossfade.

```bash
python3 scripts/build_reel.py
```

Yazılar bilerek **birleştirmeden sonra** basılıyor. Önce her klibe yazıp sonra
crossfade yaparsan geçiş anında iki klibin yazısı üst üste binip hayalet gibi
görünüyor. Sonda basınca her yazı yalnızca kendi aralığında görünür
(`enable='between(t,…)'`), geçiş sırasında ikisi de gizlidir.

Türkçe karakterler için metin drawtext'e `textfile=` ile veriliyor; font
`Arial Bold.ttf` (macOS'ta ı, ğ, ş, ö, ü hepsini taşıyor).

### Hareket promptu yazarken

Kamera hareketi rakamı kırpıyor ya da bozuyor. İlk turda 1, 9, 14, 17'de rakam kadraj
dışında kaldı; 3, 5, 6, 11'de formu bozuldu; **15'te tabela "20" yazdı** — yani video
yanlış bilgi öğretir hale geldi. Çözüm, script'teki `HOLD` öneki:

> camera holds completely still, no zoom and no pan, *[rakam sabit kalacak cümlesi]*,
> only *[tek küçük hareket]*

Yeni video ürettiğinde **son kareyi mutlaka kontrol et** — rakam hâlâ doğru mu:

```bash
ffmpeg -ss 5.5 -i videos/annex-15.mp4 -frames:v 1 -y /tmp/son-kare.png
```

## Web sunucusu (kullanıcı girişli)

`server/` — çalışma sitesi. **Giriş zorunlu değil:** siteye girer girmez soru çözmeye
başlanır, ilerleme tarayıcıdaki oturuma bağlı olarak saklanır. Hesap oluşturmak isteğe
bağlıdır ve misafir geçmişini olduğu gibi taşır (başka cihazdan devam etmek için).
Kalıcı yanlış defteri, ders ve bölüm bazında istatistik, mobil uyumlu arayüz.

```bash
./run.sh          # http://127.0.0.1:8778
```

Kurulum, systemd/nginx örnekleri ve yedekleme: [server/README.md](server/README.md).
Uçtan uca test: `.venv/bin/python server/test_flow.py`.

Soru bankası (`atpl.db`) salt okunur kullanılır; kullanıcı verisi `server/app.db`
içinde durur, `scripts/init_db.py` çalıştırmak geçmişi etkilemez.

**Yanlış defteri kuralı:** yanlış cevaplanan soru deftere girer, **üst üste iki kez**
doğru cevaplanınca düşer. "Sadece yanlış defterim" seçeneğiyle yalnızca o sorulardan
tur açılabilir.

**Doğru cevap istemciye gönderilmez** — şıklar sunucuda karıştırılır, tarayıcı yalnızca
görünen sırayı bilir.

## Çalışma uygulaması (tek dosya)

`web/atpl-soru-bankasi.html` — 2.514 sorunun tamamını içeren tek dosyalık uygulama.
Sunucu istemez, dış bağımlılığı yok (yalnızca Google Fonts).

Artifact: https://claude.ai/code/artifact/5b35bb1b-5314-4199-a8a9-8f07589837ed

### Profil özeti

Ana ekranın en tepesinde, seçili modülden bağımsız olarak **profilin geneli** durur:

```
Mavi Yaklaşma                                    TÜM PPL BANKASI
▓▓▓░░░░░░░░░░░░░░░░░
186 / 2.265 soru görüldü   %99 başarı   2 tekrar zamanı   2 yanlış defteri   1 gün seri
```

Çubuk bankanın ne kadarını gördüğünü gösterir. Şeride tıklayınca ayrıntılı **Durum**
paneli açılır (ders bazında başarı, en zayıf bölümler, 45 günlük ısı haritası, yedek).

### Modül modül ilerleme

Ana ekran tek bir **modülün** (dersin) üstüne kuruludur — bütün bankayı tek seferde
açmaz. İlk girişte rastgele bir modül seçilir; kart o modülün adını, ilerleme çubuğunu
ve kalan soru sayısını gösterir:

```
ŞİMDİ ÇALIŞTIĞIN MODÜL              [Başka modül]
070 · Operational Procedures
▓▓▓▓▓░░░░░░░░░  12 / 183 soru görüldü · 171 kaldı
                     [Başla · 171 soru]
```

Modül bitince kart yeşile döner ve **"Sıradaki modüle geç"** çıkar. Başka modüllerde
tekrarı gelmiş soru varsa ayrı bir satır uyarır ("Diğer modüllerde 23 soru tekrar
bekliyor"), tek tıkla hepsine geçilir.

Deste sayıları (tekrar zamanı / yanlışlarım / hiç görmedim / yıldızlılar) seçili modüle
göre hesaplanır. Konular akordeonundan birden çok modül ya da modül içinden tek tek
bölüm de seçilebilir; o zaman kart "karma seçim" der.

Tur uzunluğu varsayılan olarak sınırsızdır (modülün tamamı); Ayarlar'dan 20/50/100 ile
kısaltılabilir. İstediğin an *Çık* dersin, ilerleme kayıtlı kalır.

### Kullanıcı adı ve profiller

Siteye ilk girişte **rastgele bir ad** verilir (*Serin Pist*, *Parlak Kartal* gibi) ve
profil kendiliğinden açılır — giriş, şifre, e-posta yok. Ad üst şeritte görünür; tıklayıp
**Durum** panelinden istediğin gibi değiştirirsin. Aynı cihazda birden çok profil
tutulabilir, her birinin ilerlemesi ayrıdır (`localStorage`'da `atpl.v2:<ad>`).

### Konu seçici

Ana ekrandaki **Konular** akordeonu varsayılan kapalıdır. İçinde her ders bir satır;
sağdaki `›` ile bölümleri açılır. Ders kutusu tüm dersi seçer, tek tek bölüm seçince
kutu yarım dolu (`◧`) görünür. Birden çok ders ve her dersten farklı bölümler aynı anda
seçilebilir. Rozette "2 ders · 8 bölüm" gibi özet ve kapsam sayısı anında güncellenir.

### Aralıklı tekrar

| Kutu | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Tekrar | 10 dk | 1 gün | 3 gün | 7 gün | 16 gün | 35 gün |

Doğru bildikçe soru ileri kutuya, yanlışta 0'a döner. 4+ yanlış yapılan sorular
"takıldıkların" listesine düşer.

### Tur akışı

Doğru cevapta soru kendiliğinden geçer (kısa bir "Doğru" onayıyla), yanlışta doğru cevap
gösterilir ve "Anladım, devam" beklenir. **Tur bitince yanlış yaptıkların yeniden sorulur**;
hepsini bilene kadar tur döner. Özet ekranı ilk denemedeki başarıyı gösterir.

Sorular da şıklar da her gösterimde karıştırılır.

### Profiller

Sunucu olmadığı için giriş yok; bunun yerine **Durum** panelindeki açılır listeden profil
seçilir. Aynı cihazda birden çok kişi ayrı ilerleme tutabilir. Kayıt
`localStorage`'da `atpl.v2:<profil>` anahtarında durur.

### Ders notları

Üst şeritteki **Konu** düğmesi `notes/` klasöründeki .md dosyalarını uygulama içinde
açar (tablolar, başlıklar, kalınlar dahil). Yeni not eklemek için dosyayı `notes/`
altına koyup `python3 scripts/build_web.py` çalıştırmak yeterli — dosya adının ilk üç
hanesi ders kodu sayılır (`073-` → 070, `annex-` → 010).

### Yedek ve taşıma

Durum panelindeki kutudan metni kopyala, öbür cihazda aynı kutuya yapıştırıp **Yükle**.
Birleştirme yapılır, iki cihazın emeği korunur. Statik sunucudan açtığında ayrıca dosya
indir/seç düğmeleri çıkar.

## Google ile giriş ve bulut yedeği

Kaldığın yerden başka cihazda devam etmek için Firebase (Google girişi + Firestore)
kullanılır. **Kendi sunucunu tutman gerekmez**, ücretsiz katman bu iş için fazlasıyla
yeterli. Kurulmadıysa uygulama bugünkü gibi yalnız `localStorage` ile çalışır — bulut
katmanı tümüyle kapalı kalır.

### Kurulum

```bash
npm i -g firebase-tools        # bir kez
./scripts/setup_firebase.sh    # projeyi sorar ya da yenisini açar
```

Betik şunları yapar: oturumu kontrol eder, projeyi açar/seçer, web uygulaması oluşturur,
`web/firebase-config.json` dosyasını yazar, Firestore veritabanını açar,
`firestore.rules` dosyasını yayımlar ve sitenin adresini izinli alanlara ekler. Var olan
bir projeyi kullanmak için:

```bash
./scripts/setup_firebase.sh <proje-id>
```

Yeniden çalıştırmak güvenlidir; var olanı bulur, üstüne yazmaz.

### Konsoldan yapılacak tek adım

**Google girişini açmak CLI'den yapılamıyor.** Firebase bu sırada projeye bir OAuth
istemcisi üretiyor ve bunun için tarayıcıda destek e-postası seçmen gerekiyor; bunu
yapan bir genel API yok. Bir kez:

> Firebase konsolu → Authentication → **Get started** → Google → **Enable** →
> *Public-facing name* ve *Support email* doldur → **Save**

Sonra betiği tekrar çalıştır — izinli alanı (`ppltr.github.io`) artık kendisi ekler:

```bash
./scripts/setup_firebase.sh <proje-id>
```

Adım atlanırsa uygulama giriş denemesinde ne yapılacağını yazar: "Google girişi Firebase
konsolunda açık değil" ya da "Bu adres Firebase'de izinli değil".

Sonra yapılandırmayı sayfaya göm ve yayına al:

```bash
python3 scripts/build_web.py     # "bulut açık" yazmalı
./deploy.sh "Google girişi"
```

### Nasıl çalışıyor

Durum panelinde **Google ile giriş yap** düğmesi çıkar. Girdikten sonra profilin
**tamamı** yedeklenir:

| Ne | Örnek |
| --- | --- |
| Aralıklı tekrar kartları | hangi soru hangi kutuda, ne zaman tekrar edilecek |
| Yanlış defteri | doğru/yanlış sayıları, üst üste doğru serisi |
| Yıldızlar | sonra bakılacak sorular |
| Günlük sayaçlar | seri ve son 45 gün ısı haritası |
| Tur geçmişi | biten turlar ve **yarım kalan tur** — başka cihazda kaldığın sorudan devam |
| Geçilen sınavlar | eledigin dersler |
| Ayarlar | deste, kapsam, tur uzunluğu, mod, sıra, ses, sohbet seçimi |

**Ne zaman gönderilir**

- Her kayıttan ~4 saniye sonra
- Sekme kapanırken ya da arka plana alınırken bekleyen değişiklik **hemen**
- Çıkış yapmadan önce
- Profil değiştirirken eskisi, ad değiştirirken yeni adla
- Gönderim başarısızsa "kirli" işaretlenir; bağlantı gelince ve sonraki kayıtta
  yeniden denenir

**Ne zaman çekilir**

- Girişte ve **Şimdi eşitle** düğmesinde
- Sekmeye dönüldüğünde (tur ortasında değilsen, en fazla 30 saniyede bir)

Çekme sonrası yerelle **kaynaştırılır**, sonra geri gönderilir — çakışma ekranı yoktur,
iki cihazın emeği birleşir. Her soruda "daha çok görülmüş" kayıt kazanır, gün sayaçları
en büyükte birleşir, turlar id'ye göre son dokunulanla gelir, geçilen sınavlar zaman
damgasıyla son karara göre belirlenir.

Kimlik satırındaki küçük nokta durumu söyler: yeşil yedeklendi, mor bekliyor,
kırmızı gönderilemedi. Durum panelinde aynısı yazıyla.

**Sıfırla** bulut kopyasını da siler; yoksa ilk eşitlemede her şey geri gelirdi.

Veri `users/{uid}/profiles/{profil}` altında, tek bir JSON metni alanında durur.
Birden çok profilin varsa hepsi ayrı belge olarak eşitlenir.

### Güvenlik

`web/firebase-config.json` **depoya girer ve herkese açıktır — bu normaldir.** Firebase
web yapılandırması bir kimlik bilgisi değil, projenin adresidir; Google böyle
tasarlamıştır. Erişimi `firestore.rules` kısıtlar:

```
match /users/{uid} { allow read, write: if request.auth.uid == uid; }
```

Yani giriş yapmayan hiçbir şey okuyamaz, giriş yapan da yalnız kendi verisini okur.
Kurallar ayrıca yazılan belgenin biçimini ve boyutunu doğrular.

> Artifact sürümünde bulut çalışmaz: Artifact kum havuzu dış kaynaklara ağ isteğini
> engeller. Katman sessizce kapanır, uygulama `localStorage` ile çalışmaya devam eder.
> Bulut yedeği için siteyi kullan.

## Mobil gezinme ve kalite kontrolleri

Durum, ders notları, inceleme kuyruğu ve düz metin panellerinde Geri/Kapat başlığı
her zaman görünür. Telefonun veya tarayıcının Geri düğmesi önce paneli kapatır;
ders notunda önce listeye döner. Panel kapanınca aynı soru, seçim ve sayfa konumu
korunur. Ayarlar'daki sabit Geri düğmesi bölümü kapatır; ayar değişiklikleri
otomatik kaydedilir.

Yayın öncesinde Chromium ve WebKit üzerinde mobil ekranlar, panelden çıkış,
Geri/İleri, klavye odağı, soru/süre korunması ve axe erişilebilirlik kuralları
otomatik kontrol edilir. Başarısız kontrol yayını durdurur.

```bash
npm ci
npx playwright install chromium webkit
python3 scripts/build_web.py
npm test
WEB_TEST_BROWSER=webkit npm test
```

Ekran görüntüleri için `MOBILE_QA_DIR=test-results` kullanılabilir. Bu testler
320–719 piksel genişlikleri ve yatay görünümü kapsar; gerçek telefon, ekran
okuyucu ve sanal klavye ile elle yapılacak incelemenin yerine geçmez.

SEO için açıklayıcı başlık/açıklama, canonical adres, paylaşım etiketleri,
WebApplication yapılandırılmış verisi, JavaScript öncesi okunabilir tanıtım,
`robots.txt` ve `sitemap.xml` bulunur. Soru ve kişisel ilerleme ekranları ayrı
indekslenebilir adresler oluşturmaz. Yazı tipleri ilk çizimi bekletmeden yüklenir.

Gezinme ve odak davranışı [WAI dialog rehberini](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/),
SEO düzenlemeleri [Google Search Central rehberini](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
izler. Otomatik kontrollerin geçmesi bütün cihazlarda kusursuzluk veya arama
sonuçlarında sıralama garantisi değildir.

## Yayın

**Canlı site: https://ppltr.github.io/**

GitHub Pages, `main` dalının `/docs` klasöründen yayımlar. `scripts/build_web.py` aynı
dosyayı iki yere yazar:

- `web/atpl-soru-bankasi.html` — yerel kullanım / Artifact
- `docs/index.html` — Pages'in yayımladığı dosya

**Yayın otomatiktir.** `web/template.html`, `atpl.db`, `scripts/build_web.py` ya da
`notes/` değişip `main`'e gidince GitHub Actions siteyi yeniden derleyip yayımlar
(`.github/workflows/pages.yml`). `docs/index.html`'i commit'lemek zorunda değilsin.

Veri değiştiysen bankayı da üretmek gerekir:

```bash
./deploy.sh "değişiklik açıklaması"
```

Bu betik `init_db.py` + `build_web.py` çalıştırır, commit'ler, gönderir; gerisini Actions
halleder (~1 dakika).

Tek dosya olduğu için Netlify, Vercel ya da herhangi bir statik sunucu da çalışır.

## Soru üretimi (hazırlık)

Ders notlarında geçip soru bankasında karşılığı olmayan konuları bulmak için:

```bash
python3 scripts/topic_gap.py notes/501-ders-notlari.md 501
```

Nottaki başlıklar, kalın terimler ve tablo satır etiketleri konu adayı sayılır; her aday
o dersin sorularında aranır. Hiç geçmeyenler ve yalnızca 1-2 soruda geçenler listelenir.
Betik soru üretmez, yalnızca boşluğu gösterir.

Üretilen sorular `data/<ders>_uretilmis_sorular.json` içine `"origin": "uretilmis"` ile
eklenir; uygulamada **üretilmiş** etiketiyle görünür ve istenirse kapsam anahtarından
kapatılabilir. Gerçek sınav sorularıyla karışmaz.

## Tekrar eden sorular

`data/_tekrarlar.json` elle doğrulanmış tekrar gruplarını tutar; her grupta ilk ID
kanonik, diğerleri `dup_of` ile ona bağlanır. Metin benzerliği ≥%60 olan tüm çiftler
tek tek incelendi. **Cevabı farklı olan benzer sorular bilerek tekrar sayılmadı** —
onlar sınavın en değerli tuzakları (ör. 15969/15970 gündüz-gece yakıtı,
15993/15998 yaralanma var/yok, 14343/14344 destination-location tabela renkleri).

Benzer çiftleri yeniden taramak için:

```bash
python3 scripts/find_duplicates.py
```

## Yeni ders eklemek

`data/` altına aynı formatta yeni bir JSON koy (`subject_code`, `subject_name`, `section_code`, `questions[]`) ve `python3 scripts/init_db.py` çalıştır.

## 2026-10-12 · Dış kaynak Air Law genişletmesi

Claude’un yarım kalan worktree çalışması denetlenip tamamlandı. **42 yeni benzersiz Air Law sorusu** (ilk derlemede 88'di; 2026-10-13 ders notu denetiminde 46'sı notlarda karşılığı olmadığı ya da aynı konuyu tekrarladığı için emekli edildi) iki dilde, doğru cevap ilk şık olacak şekilde eklendi; 2.934 mevcut sorunun kimliği/metni/şıkları aynen korundu. Kaynak soru metinleri topluca yayımlanmadı: eklenenler bağımsız anlatımlı, güncel birincil kuralla doğrulanmış uyarlamalardır.

824 kaynak adayı: **253 mevcut eşleşme**, **42 aktif yeni soru**, **238 kapsam dışı / aynı konu / notlarda yok**, **243 inceleme**. Kullanıcının ipuçlarından yazılan sorulardan TL sorumlusu, Code 3, kabotaj ve iki CPL yetki ayrımı kaldı; ditching ders notunda karşılığı olmadığı için emekli edildi. Mevcut ATPL sorusu 27032 yeni kopya yerine Air Law kapsamında ortak kullanılır.

### Kaynak bazında sonuç

"Yeni" sütunu kaynak sorusuna atanmış yeni temsilcileri sayar. Aynı yeni soruya başka kaynaktan verilen bağ "tekrar" sütunundadır. Mevcutler kanonik kimliğe bağlanır. Kaynak başına farklı yeni soru bağlantılarının sayısı JSON raporundaki `kaynak_yeni_benzersiz` alanındadır ve kaynaklar arasında toplanmaz.

| Kaynak | Taranan | Mevcut | Yeni | Yeni aday tekrarı | Kapsam dışı | İnceleme |
|---|---:|---:|---:|---:|---:|---:|
| [Linx Aviation — Air Law](https://linxaviation.rs/wp-content/uploads/2020/12/Air_law.pdf) | 150 | 59 | 48 | 7 | 0 | 36 |
| [Bangladesh CAA — Air Law (validation)](https://ops.caab.gov.bd/file-manager/air-law-validation.pdf) | 250 | 54 | 27 | 8 | 111 | 50 |
| [Sırbistan Sivil Havacılık Direktörlüğü (CAD) — PPL(A) Air Law teorik sınav soruları (Form CAD-PEL-OB-1001)](https://cad.gov.rs/upload/Vazduhoplovno%20osoblje/2022/Air%20law.pdf) | 79 | 30 | 0 | 32 | 4 | 13 |
| [Austro Control — ECQB-PPL(A) 10 Air Law (Aircademy/LPLUS özeti, v2015.4)](https://www.austrocontrol.at/jart/prj3/ac/data/uploads/PEL/Fragenkatalog/ECQB-PPL-A-10-ALW_EN.pdf) | 134 | 34 | 5 | 8 | 13 | 74 |
| [Traficom (Finlandiya) — LAPL/PPL question bank AIRLAW 010 (Rev. 1.8, 2018)](https://www.traficom.fi/files/media/file/PPL010ENG%2011102018.pdf) | 181 | 64 | 0 | 38 | 11 | 68 |
| [Son Yaklaşma — PPL Soruları / Hava Hukuku (ücretsiz örnek)](https://sonyaklasma.com/ppl-sorulari/hava-hukuku) | 10 | 10 | 0 | 0 | 0 | 0 |
| [Transport Canada — TP 13014E Sample Examination (Recreational Pilot Permit / Private Pilot Licence — Aeroplane)](https://www.tc.gc.ca/publications/EN/TP13014/PDF/HR/TP13014E.PDF) | 20 | 2 | 2 | 2 | 12 | 2 |

Kullanıcının verdiği aşağıdaki kaynaklar toplu bankaya aktarım kısıtı nedeniyle **taranmış sayılmadı**. Erişilebilir önizleme, toplu yeniden kullanım izni değildir. Kullanıcı ipuçları saklandı; korunan soru bankasının tamamı çıkarılmadı ve hiçbir erişim engeli aşılmadı. [Scribd şartları](https://support.scribd.com/hc/en-us/articles/210129326-Global-Terms-of-Use), [QuizVDS şartları](https://quizvds.it/en-en/termini-condizioni), [Furious yasal bildirim](https://www.furious-atpl.com/mcq-exam/pageplus_3-legal-notices), [PDFCoffee şartları](https://pdfcoffee.com/term).

| Kaynak | Taranan | Mevcut | Yeni | Durum |
|---|---:|---:|---:|---|
| [PPLHAVUZSONHALI](https://www.scribd.com/document/851963112/PPLHAVUZSONHALI-1) | 0 | 0 | 0 | Toplu aktarım izni yok |
| [PPL-Q-BANK-AL](https://www.scribd.com/document/446626932/PPL-Q-BANK-AL) | 0 | 0 | 0 | Toplu aktarım izni yok |
| [CAE Oxford Aviation Academy 010 Air Law](https://www.scribd.com/document/604806172/CAE-Oxford-Aviation-Academy-010-Air-Law) | 0 | 0 | 0 | Toplu aktarım izni yok |
| [PPL(A) Question Bank (Scribd)](https://www.scribd.com/document/676565250/PPL-a-Question-Bank) | 0 | 0 | 0 | Toplu aktarım izni yok |
| [02 Question Bank Topicwise 200Q](https://www.scribd.com/document/1066220026/02-Question-Bank-Topicwise-200Q) | 0 | 0 | 0 | Toplu aktarım izni yok |
| [010 Progress Check 2](https://www.scribd.com/document/774640527/010-PC2) | 0 | 0 | 0 | Toplu aktarım izni yok |
| [QuizVDS — ATPL Air Law](https://quizvds.it/en-en/quiz/atpl/air-law/306/refers) | 0 | 0 | 0 | Toplu aktarım izni yok |
| [Furious ATPL — MCQ exam](https://www.furious-atpl.com/mcq-exam/answer%2C1-training-professional) | 0 | 0 | 0 | Toplu aktarım izni yok |
| [1 Lahmacun İşaretsiz](https://www.scribd.com/document/856014115/1-Lahmacun-%C4%B0%C5%9Faretsiz) | 0 | 0 | 0 | Toplu aktarım izni yok |
| [GDH PPL(A) English Question Bank](https://pdfcoffee.com/gdh-ppl-a-question-bank-eng-pdf-free.html) | 0 | 0 | 0 | Toplu aktarım izni yok |
| [Dauntless GroundSchool ATPL test banks](https://www.dauntless-soft.com/PRODUCTS/GroundSchoolATPL/TestBanks/air_law_and_atc_procedures/010-01-01_the_convention_of_chicago/) | 0 | 0 | 0 | Toplu aktarım izni yok |

StudyLib ayrıca 403 erişim engeli nedeniyle taranmadı. CAAB’de cevap anahtarı yok; Linx’in ilk şık kuralı bazı sorularda yanlış. Bu yüzden hiçbiri doğrudan cevap otoritesi kabul edilmedi. Eski ulusal/JAR kuralları, eksik görseller, kapsam/cevap/izin belirsizlikleri referanslarıyla `inceleme_010.json` içinde; aktif soru/puanlama havuzuna girmez.

### Sınavda hatırlanan sorular

| Konu | Kimlik | İşaret ve eşleşme |
|---|---|---|
| kabotaj | 61078 | benzer_aday |
| icao-chicago | 61072 | benzer_aday |
| lisans-yetkileri | 61080, 61079, 27032, 14303 | benzer_aday |
| transition-tirmanis | 61035 | benzer_aday |
| tl-kim-belirler | 61002 | kullanici_dogruladi_yeniden_yazim |
| aip-bolumleri | 14384 | benzer_aday |
| aerodrome-code3 | 61001 | kullanici_dogruladi_yeniden_yazim |
| ditching | — (61081 emekli: notlarda yok) | benzer_aday |
| tora-tanimi | 14909 | kullanici_dogruladi_mevcut_esdeger |
| manyetik-rota-fl | — | kesin_soru_bulunamadi |

⭐ **Code 3: 61001**, **TL sorumlusu: 61002**, **TORA: 14909**. TL ve Code 3 kullanıcının doğruladığı soru tipinden yeniden yazıldı; TORA mevcut ters yönden tanım sorusunun eşdeğer kaydıdır. Birebir kaynak metni bulundu iddiası yoktur. TORA’nın asıl dersi 030 ve geçmişi korunur; 010 kapsamına aynı kimlikle de girer. Hiçbir işaret resmî SHGM çıkmış sorusu iddiası değildir. Diğer konular benzer adaydır. **Manyetik rota/IFR/non-RVSM sorusunun kesin derece, koşul ve metni bulunamadı**; 146° VFR → FL75 ile birleştirilmedi.

### Diğer dersler (2026-10-13)

020, 030, 040, 050, 060, 070, 080, 090 için Traficom (Finlandiya) ve Sırbistan CAD listelerinin tamamı, Transport
Canada örnek sınavının ilgili bölümleri ve Son Yaklaşma'nın ücretsiz örnekleri indirilip tek tek bankayla karşılaştırıldı.
080 Principles of Flight için ek olarak Austro Control'ün yayımladığı ECQB-PPL(A) 51 özeti (149 soru, işaretli kutudan
cevap anahtarı) tarandı: 80'i bankada aynı bilgiyle vardı, 63'ü notlarda yok ya da aynı konu, 1'i inceleme, 5'i yeni (kanat yüklemesi, girişim sürüklemesi, laminer→türbülanslı
geçiş noktası, windmilling pervane direnci, dönüşte hücum açısı/güç); geri kalanı bankada aynı bilgiyle ya da notlarda
yok. Her ek soru dersin `notes/` dosyasına bağlanabilmeli; bağlanamayan emekli edildi (Air Law 88 → 42, 050 → 0,
060 → 2). Ölçüt ve akış `CLAUDE.md` içinde ("Ek kaynak soruları"). Sonuç için `python3 scripts/kaynak_rapor.py`.

### Yeniden derleme ve test

```bash
python3 scripts/kaynak_derle.py 010 data/kaynaklar/decisions/root_special.json data/kaynaklar/decisions/caab_linx_audit.json data/kaynaklar/decisions/other_airlaw_audit.json data/kaynaklar/decisions/010_emekli.json
python3 scripts/check_tr.py
python3 scripts/init_db.py
python3 scripts/build_web.py
python3 scripts/test_kaynak_pipeline.py
python3 scripts/test_kaynak_derle.py
node scripts/test_kaynak_web.cjs
.venv/bin/python server/test_flow.py
```

`--kuru` veri yazmaz; ID kaydı kalıcıdır; doğrulamasız cevap, kimlik çakışması, aynı kök veya eski yeni-soru içeriğinin sessiz değişimi derlemeyi durdurur. İnceleme yalnız okunur panelde açılır. Mevcut soru ortak dersler için `also_subjects` ile bağlanır; çözüm yine aynı ID üzerinden tutulur. İlerleme veritabanı/localStorage/bulut kayıtlarına derleme betikleri dokunmaz.

23 Python regresyon testi, gerçek template işlevleriyle JS kontrolü, sunucu akış testi, EN/TR tamlığı ve 2.934 soru için SHA-256 kimlik/içerik kontrolü geçti. Tarayıcıda yıldız, açıklama/kaynak, yanlışların tekrar turu, yenileme ve geri/ileri ile aynı soruya dönüş doğrulandı. Yeni bankada 2.992 ham / 2.612 görünür benzersiz soru var; mevcut 380 tekrar bağlantısı değişmedi. `qa/airlaw-confirmed.jpg` yerel test profili görüntüsüdür.
