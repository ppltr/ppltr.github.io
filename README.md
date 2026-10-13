# PPL Soru Bankası

SQLite tabanlı **PPL** çalışma uygulaması. İlk banka ATPL TV'deki *PPL Turkey (English)* sınav raporlarından çevrildi; ders notları ve kaynak taramalarından doğrulanmış, bağımsız yazılmış alıştırmalarla genişletildi. **3.572 kayıt, 11 ders; 383 tekrar bağlantısı çıkarılınca 3.189 benzersiz kayıt (varsayılan çalışma kapsamı 3.182 soru).** 233 kayıt ders notlarından, 638 kayıt ek kaynak çalışmalarından gelir.

Aşağıdaki sayılar sorunun ana dersine göre fiziksel kayıt sayılarıdır. Ortak konular aynı soru kimliğiyle birden fazla derste gösterilebilir; bu bağlar toplam soru sayısını artırmaz.

| Ders | Kayıt | Benzersiz | Bölüm |
|---|---:|---:|---:|
| 010 · Air Law | 285 | 256 | 15 |
| 020 · Aircraft General Knowledge | 500 | 439 | 34 |
| 030 · Flight Performance and Planning | 307 | 274 | 15 |
| 040 · Human Performance and Limitations | 384 | 341 | 18 |
| 050 · Meteorology | 538 | 475 | 20 |
| 060 · Navigation | 330 | 300 | 24 |
| 070 · Operational Procedures | 237 | 227 | 8 |
| 080 · Principles of Flight | 306 | 242 | 20 |
| 090 · Communications | 290 | 241 | 13 |
| 501 · Havacılığa Giriş | 252 | 251 | 3 |
| 502 · Güvenlik Bilinci | 143 | 143 | 5 |

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

Claude’un yarım kalan worktree çalışması denetlenip tamamlandı. **88 yeni benzersiz Air Law sorusu** iki dilde, doğru cevap ilk şık olacak şekilde eklendi; 2.934 mevcut sorunun kimliği/metni/şıkları aynen korundu. Kaynak soru metinleri topluca yayımlanmadı: eklenenler bağımsız anlatımlı, güncel birincil kuralla doğrulanmış uyarlamalardır.

824 kaynak adayı: **253 mevcut eşleşme**, **82 kabul edilen yeni kaynak türü**, **95 yeni aday tekrarı**, **151 PPL kapsamı dışı**, **243 inceleme**. Ayrıca kullanıcının ipuçları ve resmî kurallardan bağımsız yazılan 6 soru: TL sorumlusu, Code 3, kabotaj, ditching ve iki CPL yetki ayrımı. Sonuç 82 + 6 = 88. Mevcut ATPL sorusu 27032 yeni kopya yerine Air Law kapsamında ortak kullanılır.

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
| transition-tirmanis | 61060, 61035 | benzer_aday |
| tl-kim-belirler | 61002 | kullanici_dogruladi_yeniden_yazim |
| aip-bolumleri | 14384 | benzer_aday |
| aerodrome-code3 | 61001 | kullanici_dogruladi_yeniden_yazim |
| ditching | 61081 | benzer_aday |
| tora-tanimi | 14909 | kullanici_dogruladi_mevcut_esdeger |
| manyetik-rota-fl | — | kesin_soru_bulunamadi |

⭐ **Code 3: 61001**, **TL sorumlusu: 61002**, **TORA: 14909**. TL ve Code 3 kullanıcının doğruladığı soru tipinden yeniden yazıldı; TORA mevcut ters yönden tanım sorusunun eşdeğer kaydıdır. Birebir kaynak metni bulundu iddiası yoktur. TORA’nın asıl dersi 030 ve geçmişi korunur; 010 kapsamına aynı kimlikle de girer. Hiçbir işaret resmî SHGM çıkmış sorusu iddiası değildir. Diğer konular benzer adaydır. **Manyetik rota/IFR/non-RVSM sorusunun kesin derece, koşul ve metni bulunamadı**; 146° VFR → FL75 ile birleştirilmedi.

### Diğer dersler: yalnız ekleme önerileri

130 aday (Transport Canada TP13014, soru 21–100: 80; Son Yaklaşma’nın her dersten 10 yerel örneği: 50) incelendi. Bu kaynakların tüm bankalarına ilişkin tahmin değildir. Kaynak anahtarı bulunan adaylar için de aktif eklemeden önce modern teknik dayanak, şekil ve ülke koşulları tamamlanmalıdır. Bu derslere yeni aktif soru eklenmedi.

| Ders | Olası benzersiz yeni tür |
|---|---:|
| Navigation | 0 |
| Flight Performance | 1 |
| Aircraft General Knowledge | 5 |
| Meteorology | 10 |
| Principles of Flight | 2 |

Toplam **18**; ikinci denetimde dört tekrar elendi. Navigation’daki 0, bankanın tamamında hiçbir eksik olmadığı anlamına gelmez: taranan örneklerin yeni türleri eski/eksik harita koşulları nedeniyle incelemededir. Aday başına kaynak, soru/sayfa, yakın mevcut kimlik ve ayrım gerekçesi `decisions/subject_proposals.json` içindedir.

### Yeniden derleme ve test

```bash
python3 scripts/kaynak_derle.py 010 data/kaynaklar/decisions/root_special.json data/kaynaklar/decisions/caab_linx_audit.json data/kaynaklar/decisions/other_airlaw_audit.json
python3 scripts/check_tr.py
python3 scripts/init_db.py
python3 scripts/build_web.py
python3 scripts/test_kaynak_pipeline.py
python3 scripts/test_kaynak_derle.py
node scripts/test_kaynak_web.cjs
.venv/bin/python server/test_flow.py
```

`--kuru` veri yazmaz; ID kaydı kalıcıdır; doğrulamasız cevap, kimlik çakışması, aynı kök veya eski yeni-soru içeriğinin sessiz değişimi derlemeyi durdurur. İnceleme yalnız okunur panelde açılır. Mevcut soru ortak dersler için `also_subjects` ile bağlanır; çözüm yine aynı ID üzerinden tutulur. İlerleme veritabanı/localStorage/bulut kayıtlarına derleme betikleri dokunmaz.

23 Python regresyon testi, gerçek template işlevleriyle JS kontrolü, sunucu akış testi, EN/TR tamlığı ve 2.934 soru için SHA-256 kimlik/içerik kontrolü geçti. Tarayıcıda yıldız, açıklama/kaynak, yanlışların tekrar turu, yenileme ve geri/ileri ile aynı soruya dönüş doğrulandı. Yeni bankada 3.022 ham / 2.642 görünür benzersiz soru var; mevcut 380 tekrar bağlantısı değişmedi. `qa/airlaw-confirmed.jpg` yerel test profili görüntüsüdür.

## 2026-10-12 · Diğer PPL derslerinde tamamlanan eklemeler

Aynı kaynak ailesinden **29 yeni benzersiz soru** eklendi. İki dil, makul çeldiriciler, kısa açıklama ve birincil cevap dayanağı birlikte denetlendi. Mevcut 3.022 kimlik korundu; silme veya yeniden ID kullanma yok. Toplam 3.051 ham / 2.671 görünür benzersiz soru oldu. İlk 18-aday kaydı tarihsel ön elemedir; yeni sayılar ayrıntılı içerik ve grafik denetiminin sonucudur.

| Ders | Yeni | Gerçek kaynak adayı | İnceleme |
|---|---:|---:|---:|
| Aircraft General Knowledge | 7 | 21 | 0 |
| Flight Performance | 2 | 16 | 0 |
| Human Performance | 3 | 5 | 1 |
| Meteorology | 11 | 41 | 0 |
| Navigation | 3 | 23 | 8 |
| Operational Procedures | 1 | 2 | 0 |
| Principles of Flight | 2 | 16 | 1 |

130 gerçek kaynak adayı: TC örneğinin 21–100 numaralı tüm 80 sorusu ve Son Yaklaşma’nın 50 önceden elde edilmiş açık örneği. 124 kayıt derslere işlendi; kalan 6 TC kaydı Kanada’ya özgü meydan/hukuk şartları nedeniyle kapsam dışı tutuldu. Bu sayılar ek bir bankanın bütününe ilişkin tahmin değildir.

| Kaynak | Gerçek aday | Mevcut | Yeni kaynak türü | İnceleme | Kapsam dışı |
|---|---:|---:|---:|---:|---:|
| x-tc-tp13014 | 80 | 37 | 24 | 9 | 10 |
| x-sonyaklasma | 50 | 49 | 0 | 1 | 0 |

**24 kabul edilen kaynak türü + 5 ayrı, koşulları açık bağımsız alıştırma = 29.** Ayrı alıştırmalar: VOR FROM, tırmanış ek süresi, track/heading/course, ICAO Qxxxx/hPa ve boş alan miyopisi tanımı. Bunlar eski haritaların veya yerel kodların özgün cevaplarının doğrulandığı anlamına gelmez. Eski Toronto VNC’ye bağlı sorular ve TC’nin eski sayısal miyopi cevabı referanslarıyla incelemede kaldı; cevap tahmini aktif bankaya yazılmadı.

Transport Canada’nın yayımladığı [TP13014](https://tc.canada.ca/en/aviation/publications/civil-aviation-sample-examination-recreational-pilot-permit-private-pilot-licence-aeroplane-tp-13014) kamuya açık ticari olmayan yeniden kullanım iznini açıkça verir. Son Yaklaşma’nın korumalı metinleri aktarılmadı; mevcut sorulara kaynak ipucu bağlandı ve track sorusu FAA teknik tanımlarından bağımsız yazıldı. Önceki Scribd/QuizVDS/Furious/PDFCoffee/Dauntless toplu aktarım kısıtları korunur. Traficom’un coğrafi veri lisansı sınav bankasına uygulanmış sayılmadı; CAD belgesinin üçüncü taraf hakları kesinleşmedi. Bu geniş bankalar bu turda kapak/erişim/izin kontrolünden öte taranmış sayılmadı.

İkinci hakem denetimi: TC67’nin mevcut 15414 ile aynı düşük→yüksek QNH koşulu yeniden sorulmadı; yer etkisi ve stagnation soruları mevcut16168/16126’ya bağlandı; METAR tavanı mevcut 61085’e ortak ders bağıyla taşındı. TC89 Türkçe toplam yakıt payı belirsizliği ve TC58’in cevabı veren sıfatları düzeltildi. Alkol/irtifa sorusunun ilgisiz yanlış şıkları daha yakın fizik/etki yanılgılarıyla değiştirildi.

Sayısal örnekler ayrı doğrulandı: tabloya özgü kalkış 2.063 ft, iki kalkış payıyla yakıt 17 US gal, tırmanış ek paylı uçuş 75 dakika, ara seviye rüzgâr 24 kt, negatif sıcaklık–çiy noktası farkı 5°C. Bunlar senaryonun verdiği model ve katsayılardır; evrensel AFM/POH veya yakıt rezerv kuralları değildir.

Yeni meteoroloji çizimi 65009 sorusuna bağlandı; web ve sunucu sürümlerinde gösterilir. Tarih/UTC, kuzey ve sabit referanslar görsel olarak denetlendi. SVG erişilebilir açıklaması yorumlanmış doğru yönü yazmaz, aynı konum verilerini verir. Görsel QA: `qa/other-subjects.jpg`.

**Önceki Air Law’dan 61035 ve 61084**, tespit edilen koşul/kök sorunları için aynı ID ile düzeltildi. Geçiş tabakası içindeki tırmanışta FL / alçalışta irtifa ayrımı ve TA < 10.000 ft iken FL100 eşiği açık yazıldı. Düzeltme eski/yeni içerik hashleri ve gerekçesiyle `data/kaynaklar/duzeltmeler.json` içindedir; eski 2.934 banka sorusuna dokunulmadı.

Kontroller: 28 Python regresyon testi, JS kapsam/kimlik/inceleme ayrımı, tam EN/TR ve şekil kontrolü, SQLite bütünlüğü, bütün 8 ders derlemesinin tekrarlı çalıştırmada aynı veri vermesi, eski kimlik/hash koruması, sunucu akış ve grafik/API testi geçti. Browser’da grafikli soru ve dil seçimi görüldü; yenileme aynı soruya döndü. Kullanıcı verisi/localStorage/bulut geçmişine taşıma/sıfırlama yapılmadı.

Yeniden derleme:

```bash
python3 scripts/kaynak_derle.py 010 data/kaynaklar/decisions/root_special.json data/kaynaklar/decisions/caab_linx_audit.json data/kaynaklar/decisions/other_airlaw_audit.json
for ders in 020 030 040 050 060 070 080; do
  python3 scripts/kaynak_derle.py "$ders" "data/kaynaklar/decisions/other_subjects_${ders}.json"
done
python3 scripts/check_tr.py
python3 scripts/init_db.py
python3 scripts/build_web.py
```

## 2026-10-13 · Diğer PPL derslerinde tam kaynak taraması

**521 yeni benzersiz soru eklendi.** Bu sayı 12 Ekim'deki 29 soruya ilavedir; önceki Air Law 88 kaydı da bu yeni sayıya dahil değildir. Önceki 3.051 sorunun kimlik ve soru içeriği aynen korundu. Son durum 3.572 ham / 3.192 görünür benzersiz kayıttır.

Bu tur önceki sınırlı örneklemeyi genişletir: normal erişimle incelenebilen yayımlanmış PDF'lerin 020–090 bölümleri baştan sona işlendi. **8.647 gerçek kaynak soru satırı** incelendi. Aynı sorunun farklı bankalarda tekrarlanması taranan satır sayısına dahildir; eklenen benzersiz kayıt sayısına dahil değildir. Bu sayı bütün güncel SHGM/PPL sınav bankasının kesin eksik sayısı olarak yorumlanamaz.

| Ders | Taranan kaynak satırı | Bu tur eklenen benzersiz kayıt |
|---|---:|---:|
| 020 · Aircraft General Knowledge | 1804 | **106** |
| 030 · Flight Performance and Planning | 1177 | **48** |
| 040 · Human Performance | 1394 | **96** |
| 050 · Meteorology | 1318 | **116** |
| 060 · Navigation | 1481 | **57** |
| 070 · Operational Procedures | 442 | **43** |
| 080 · Principles of Flight | 607 | **30** |
| 090 · Communications | 424 | **25** |
| **Toplam** | **8.647** | **521** |

### Kaynak kapsamı ve sayım

Traficom, Serbia CAD ve Austro'nun yayımlanmış bölümlerinde toplam 3.244; CAAB'nin açık AGK, CPL composite ve ATPL composite dosyalarında 4.203; Linx'in diğer sekiz dersinde 1.200 soru satırı incelendi. Austro belgeleri tarihsel yayımlanmış alt kümedir; güncel ticari AirCademy bankasının tamamına erişildiği iddia edilmez.

4.142 kaynak satırı başlangıçtaki bankaya, 1.624 satır bu tur kabul edilen yeni soru tiplerine bağlandı. 1.537 satır belirsizlik, eski/eksik şekil veya doğrulanamayan koşullar nedeniyle incelemede; 1.344 satır PPL kapsamı dışında tutuldu. İnceleme ve kapsam dışı kayıtlar aktif teste alınmadı. Ayrıntılı karar/gerekçe ve kimlik bağları `data/kaynaklar/decisions/full*.json`, makine tarafından yeniden üretilen sonuç `data/kaynaklar/rapor_tam_tarama_20261013.json` içindedir.

Aşağıdaki “İlk kaynakla eklenen” sütunu her yeni kaydı yalnız ilk kaynak URL'sine sayar; toplamı 521'dir. “Yeni tipe bağlanan” kaynak satırı sayısıdır, benzersiz yeni soru sayısı değildir. Fintraffic uçuş planı formu soru bankası değildir; soru taramasına 0 sayılmış, Z uçuş kuralları alıştırmasının birincil dayanağı olarak kullanılmıştır.

| Kaynak / yayımlanmış dosya | Taranan | Başlangıçta mevcut | Yeni tipe bağlanan | İlk kaynakla eklenen | İnceleme | Kapsam dışı |
|---|---:|---:|---:|---:|---:|---:|
| [ref-fpl-fintraffic](https://www.ais.fi/sites/default/files/2023-11/Instructions%20for%20completing%20the%20FPL%2005NOV20_1.pdf) | 0 | 0 | 0 | 1 | 0 | 0 |
| [x-austro-020](https://www.austrocontrol.at/jart/prj3/ac/data/uploads/PEL/Fragenkatalog/ECQB-PPL-A-80-AGK_EN.pdf) | 162 | 107 | 27 | 19 | 27 | 1 |
| [x-austro-030](https://www.austrocontrol.at/jart/prj3/ac/data/uploads/PEL/Fragenkatalog/ECQB-PPL-A-70-FPP_EN.pdf) | 112 | 51 | 42 | 15 | 19 | 0 |
| [x-austro-040](https://www.austrocontrol.at/jart/prj3/ac/data/uploads/PEL/Fragenkatalog/ECQB-PPL-A-20-HPL_EN.pdf) | 76 | 43 | 15 | 12 | 18 | 0 |
| [x-austro-050](https://www.austrocontrol.at/jart/prj3/ac/data/uploads/PEL/Fragenkatalog/ECQB-PPL-A-30-MET_EN.pdf) | 130 | 75 | 44 | 29 | 11 | 0 |
| [x-austro-060](https://www.austrocontrol.at/jart/prj3/ac/data/uploads/PEL/Fragenkatalog/ECQB-PPL-A-90-NAV_EN.pdf) | 225 | 147 | 43 | 20 | 34 | 1 |
| [x-austro-070](https://www.austrocontrol.at/jart/prj3/ac/data/uploads/PEL/Fragenkatalog/ECQB-PPL-A-60-OPR_EN.pdf) | 57 | 12 | 18 | 10 | 27 | 0 |
| [x-austro-080](https://www.austrocontrol.at/jart/prj3/ac/data/uploads/PEL/Fragenkatalog/ECQB-PPL-A-51-PFA_EN.pdf) | 149 | 112 | 23 | 12 | 14 | 0 |
| [x-caab-agk-020, x-caab-agk-080](https://ops.caab.gov.bd/file-manager/cpl-ir--agk-29072019.pdf) | 1200 | 131 | 93 | 54 | 394 | 582 |
| [x-caab-atpl-030, x-caab-atpl-040, x-caab-atpl-050, x-caab-atpl-060](https://ops.caab.gov.bd/file-manager/atplcomposit.pdf) | 1503 | 559 | 326 | 57 | 229 | 389 |
| [x-caab-cpl-030, x-caab-cpl-040, x-caab-cpl-050, x-caab-cpl-060](https://ops.caab.gov.bd/file-manager/cpl-comp-17-dec18.pdf) | 1500 | 575 | 363 | 98 | 224 | 338 |
| [x-cad-020](https://cad.gov.rs/upload/Vazduhoplovno%20osoblje/2022/Aircraft%20%20general%20knowledge.pdf) | 150 | 101 | 22 | 0 | 27 | 0 |
| [x-cad-030](https://cad.gov.rs/upload/Vazduhoplovno%20osoblje/2022/Flight%20performance%20and%20planning.pdf) | 148 | 109 | 13 | 10 | 26 | 0 |
| [x-cad-040](https://cad.gov.rs/upload/Vazduhoplovno%20osoblje/2022/Human%20performance.pdf) | 150 | 88 | 28 | 0 | 34 | 0 |
| [x-cad-050](https://cad.gov.rs/upload/Vazduhoplovno%20osoblje/2022/Metheorology.pdf) | 150 | 99 | 26 | 6 | 22 | 3 |
| [x-cad-060](https://cad.gov.rs/upload/Vazduhoplovno%20osoblje/2022/Navigation.pdf) | 138 | 103 | 16 | 10 | 19 | 0 |
| [x-cad-070](https://cad.gov.rs/upload/Vazduhoplovno%20osoblje/2022/Operational%20procedures.pdf) | 150 | 52 | 35 | 19 | 63 | 0 |
| [x-cad-080](https://cad.gov.rs/upload/Vazduhoplovno%20osoblje/2022/Principles%20of%20flight.pdf) | 150 | 129 | 16 | 8 | 5 | 0 |
| [x-cad-090](https://cad.gov.rs/upload/Vazduhoplovno%20osoblje/2022/Communications.pdf) | 137 | 85 | 29 | 1 | 22 | 1 |
| [x-linx-020](https://linxaviation.rs/wp-content/uploads/2020/12/Aircraft_general_knowledge.pdf) | 150 | 101 | 22 | 0 | 27 | 0 |
| [x-linx-030](https://linxaviation.rs/wp-content/uploads/2020/12/Flight_performance_and_planning.pdf) | 150 | 111 | 30 | 0 | 9 | 0 |
| [x-linx-040](https://linxaviation.rs/wp-content/uploads/2020/12/Human_performance.pdf) | 150 | 80 | 30 | 2 | 40 | 0 |
| [x-linx-050](https://linxaviation.rs/wp-content/uploads/2020/12/Meteorology.pdf) | 150 | 97 | 27 | 1 | 23 | 3 |
| [x-linx-060](https://linxaviation.rs/wp-content/uploads/2020/12/Navigation.pdf) | 150 | 107 | 32 | 2 | 11 | 0 |
| [x-linx-070](https://linxaviation.rs/wp-content/uploads/2020/12/Operational_procedures.pdf) | 150 | 52 | 36 | 0 | 62 | 0 |
| [x-linx-080](https://linxaviation.rs/wp-content/uploads/2020/12/Principles_of_flight.pdf) | 150 | 126 | 17 | 1 | 7 | 0 |
| [x-linx-090](https://linxaviation.rs/wp-content/uploads/2020/12/Communications.pdf) | 150 | 97 | 29 | 0 | 23 | 1 |
| [x-traficom-020](https://www.traficom.fi/sites/default/files/media/file/PPL020ENG%2011102018.pdf) | 159 | 114 | 28 | 27 | 17 | 0 |
| [x-traficom-030](https://www.traficom.fi/sites/default/files/media/file/PPL030ENG%2011102018.pdf) | 165 | 113 | 33 | 3 | 10 | 9 |
| [x-traficom-040](https://www.traficom.fi/sites/default/files/media/file/PPL040ENG%2011102018.pdf) | 159 | 99 | 31 | 26 | 29 | 0 |
| [x-traficom-050](https://www.traficom.fi/sites/default/files/media/file/PPL050ENG%2011102018.pdf) | 144 | 106 | 25 | 24 | 12 | 1 |
| [x-traficom-060](https://www.traficom.fi/sites/default/files/media/file/32088-PPL060ENG.pdf) | 170 | 127 | 31 | 3 | 11 | 1 |
| [x-traficom-070](https://www.traficom.fi/sites/default/files/media/file/PPL070ENG%2001062018.pdf) | 85 | 28 | 30 | 21 | 23 | 4 |
| [x-traficom-080](https://www.traficom.fi/sites/default/files/media/file/PPL080ENG%2011102018.pdf) | 141 | 113 | 13 | 6 | 5 | 10 |
| [x-traficom-090](https://www.traficom.fi/sites/default/files/media/file/PPL090ENG%2001062018.pdf) | 137 | 93 | 31 | 24 | 13 | 0 |
| **Toplam** | 8647 | 4142 | 1624 | 521 | 1537 | 1344 |

Önceki Scribd, QuizVDS, Furious, PDFCoffee, Dauntless ve Son Yaklaşma erişim/toplu aktarım sınırlamaları kaynak envanterinde korunur; kapalı içerik yeni baştan sona taramaya sayılmadı. Austro'nun İngilizce Communications dosyası bulunamadı (404; 0 soru). CAAB ATPL-FOOL ZIP dosyası normal erişimde zaman aşımı ve SSL sertifika doğrulama hatası verdi (0 soru); erişim engeli veya sertifika doğrulaması aşılmadı.

### İçerik, tekrar ve cevap denetimi

Kaynakların korumalı soru kökleri, seçenekleri ve şekilleri toplu olarak yayımlanmadı. PPL açısından gerekli farklı bilgi/koşullar bağımsız soru ifadeleriyle yazıldı. Her yeni kayıt İngilizce ve Türkçe dört seçenek, kısa iki dilli açıklama, kaynak URL'si ve varsa sayfa/soru numarası, ayrıca cevap doğrulaması için birincil dokümanın bölüm bağlantısını içerir. Sayısal örnekler verilen senaryo ve birimlerle kontrol edildi. Yeni Türkçe kayıtlardaki ondalık ve cümle boşlukları da son yazım denetiminde düzeltildi; değerler ve seçenek sırası korunur. Yeni kaynaklı soruların doğru cevabı JSON'da ilk seçenektir; uygulama seçenekleri karıştırır.

Konu benzerliği tek başına tekrar sayılmadı. Açık/kapalı pitot tahliyesi, kuzey/güney yarımküre pusula hataları, sabit hatveli/sabit devirli pervane, IFR/VFR ve farklı uçuş koşulları ayrı tutuldu. Beyaz yayın VS0 ve yeşil yayın VS1 alt sınırları iki ayrı kimliktir; bunları birlikte soran üçüncü tekrar eklenmedi. Kaynağın bir satırı iki ayrı koşulu içeriyorsa iki mevcut kimliğe kaynak bağı eklenebilir; çözüm kimlikleri birleştirilmez. Ortak dersler `also_subjects` ile aynı ID'yi kullanır.

İkinci içerik denetiminde yalnız yeni taslaklardan 11 tekrar elendi. Bunlar ve kısa gerekçeleri sonuç raporunun `ikincil_incelemede_elenen` alanında kayıtlıdır: düşük RPM'de buji kirlenmesi, karşılıklı yatay motor, batarya/starter, ana taşıyıcı yapı, oktan/detonasyon, altimetre basınç referansı, master kapalıyken elle pervane tehlikesi, motor arızasında önce uçuş kontrolü, ASI alt sınırlarının birleşik tekrarı, hafif yan rüzgârda vorteks ve alçalışta karışımın fakirleşmesi. Mevcut banka sorusu silinmedi veya azaltılmadı.

VASI'nin iki sırası ile PAPI'nin dört birimi ayrı doğrulandı. VASI'de yakın beyaz/uzak kırmızı doğru süzülüş hattıdır; ikisi kırmızı hattın altı, ikisi beyaz hattın üstüdür. Sağ yönlü yer oku sağ trafik dönüşünü belirtir. Üç yeni sorunun yanlış alt bölüm etiketi metin/seçenek/ID korunarak düzeltildi; eski/yeni hash ve neden `data/kaynaklar/duzeltmeler.json` içindedir.

Kullanıcının doğruladığı Air Law yıldızları **61001 (Code 3), 61002 (Transition Level'ı kim belirler), 14909 (TORA)** olarak korundu. Diğer hatırlanan konular benzer aday etiketinde kalır; hatırlanmayan manyetik derece ve sınavdaki tam soru metni kesinleştirilmiş sayılmadı. Hiçbir kayıt resmî SHGM çıkmış sorusu diye sunulmaz.

### Tekrarlanabilir derleme ve doğrulama

Son tam taramayı üretmek için aşağıdaki komutları kullanın. Önceki tarihli dar örneklem komutları bu turun manifestlerini kapsamaz.

```bash
python3 scripts/tam_tarama.py --derle --rapor
python3 scripts/make_figures.py
python3 scripts/check_tr.py
python3 scripts/init_db.py
python3 scripts/check_figures.py
python3 scripts/build_web.py
python3 -m unittest discover -s scripts -p 'test_kaynak*.py'
node scripts/test_kaynak_web.cjs
.venv/bin/python server/test_flow.py
```

`tam_tarama.py` yayımlanmış dosyaların gerçek satır sayılarını ve başlangıçtaki 3.051 soru hashini kontrol eder; eksik manifesti tam tarama saymaz. Aynı kaynak/koşulun çapraz ders bağları gerçek tahsis edilmiş ID'ler üzerinden çözülür. Yeniden derleme veri JSON'larında değişiklik üretmez. Eksik doğrulama, yanlış kimlik, habersiz içerik değişimi veya aynı kimliğin yeniden kullanımı derlemeyi durdurur. Açık gerekçeli alt bölüm düzeltmesinde de soru kimliği korunur.

33 Python regresyon testi, JS kapsam/kimlik/inceleme ayrımı, sunucu kullanıcı/çözüm/geçmiş akışı ve grafik API testi geçti. Her 3.572 kaydın iki dili tamdır; şekil isteyen 40 sorunun tamamı 32 üretilmiş çizime bağlanır. SQLite bütünlük ve yabancı anahtar kontrolleri temizdir. Mevcut 380 tekrar bağı ve kullanıcı geçmiş veritabanı değişmedi. Tarayıcıda eski çalışma oturumunun aynı ID/zamanla açılması, ayrı QA profilinde yeni grafikli sorunun iki dili, cevap/açıklama/kaynak ve tekrar turu doğrulandı. `qa/full-subject-expansion-tr.jpg` yeni soru ekranıdır.

Yerel SQLite, bağımsız HTML ve GitHub Pages için `docs/index.html` yeniden üretildi. Çalışma yerel `codex/ppl-airlaw-expansion` dalındadır.

## 2026-10-13 · Air Law hızlı tekrar ve kapsam düzeltmesi

Air Law'daki 88 yeni kayıt ve diğer derslerden bağlanan 27 yeni kayıt (115) yeniden incelendi. Sollama/tırmanış 61020 → 14264, acil durum safhaları 61025 → 15988 ve kemer brifingi 61076 → 16050 aynı bilgiyi tekrar sınadığı için yeni tekrar bağlantılarıyla gizlenir. Kanonik kayıtlar gerekli Air Law kaynak/ders bağlarını taşır. Hiçbir soru, seçenek, ID veya çözüm geçmişi silinmedi; mevcut 3.572 soru nesnesinin hashleri korundu.

15 ikincil/idari ayrıntı ve kısa önleme telsiz kalıbı alıştırması `data/_calisma_kapsami.json` ile Air Law'da tamamlayıcı olarak etiketlendi. **Ayarlar → Air Law: tamamlayıcı ayrıntılar** varsayılan kapalıdır. Açılınca yeniden görünürler. Başka derslerde kullanılan ortak sorular kendi derslerinde kalır; farklı koşul/istisna öğreten temel sorular keyfî kotayla çıkarılmadı.

Air Law'da tekrarlar gizliyken 311 yerine **295 ana kapsam sorusu**, tamamlayıcılar da açılırsa **310** soru bulunur. Ana kapsamdaki yeni ek/ortak kayıt 97'dir. Kullanıcının “hiç görmedim” sayısı kişisel geçmişine bağlıdır; bu toplamlar kişisel çözülmemiş sayısı değildir. Üç doğrulanmış sınav işareti 61001, 61002 ve 14909 ana kapsamda kalır. Tam karar listesi `data/kaynaklar/rapor_airlaw_hizli_20261013.json` içindedir.

Yarım kalan tur geri açıldığında güncel tekrar/kapsam filtreleri uygulanır. Çıkarılan sorular yüzünden eski indeks kayarak çözülmemiş bir soruyu atlamaz; kayıtlı cevap geçmişi korunur. 35 Python testi ve JS kapsam/tur devamı kontrolleri geçti.

## 2026-10-13 · Konuşmadaki sınav konularına odaklı son düzenleme

Kullanıcının paylaştığı 994 satırlık konuşma esas alındı. Air Law'daki yeni yayın kapsamı yalnız kabotaj, Chicago/ICAO, lisans yetkileri, transition, AIP, Code 3, ditching, TORA ve hatırlanan IFR/non-RVSM konusu olarak daraltıldı. Önceki 88 kayıttan bu konuları karşılamayan 76 kayıt yayın paketinden çıkarıldı; yerel kayıtlar ve kimlikleri tutuldu. Yeni ATPL çok pilotlu ticari uçak kaptanlığı, tırmanışta TA ve NON-RVSM örneği üç bağımsız aday olarak eklendi.

Üstte **Sınavda hatırladığın konular → Bu konuları çalış · 16 soru** düğmesi vardır. Bu grup önceden çözülmüş AIP/PPL/TORA sorularını da aynı kimlikleriyle gösterir; “hiç görmedim” filtresi bu tekrar çalışmayı engellemez. **Kısa konu anlatımı** doğrudan `notes/010-sinavda-hatirlanan-konular.md` notunu açar.

TORA'nın mevcut14909 kimliği, kullanıcı hatırlamasındaki gibi TORA soru kökünde parantez içinde olacak şekilde tanım sorusu olarak sunulur. AIP14384 seçeneklerinde GEN/ENR/AD'nin açık adları bulunur. CPL PIC/co-pilot kayıtları lisans seçenekleriyle gösterilir. Gösterim varyantları yerel soru nesnelerini değiştirmez, ilk doğru seçeneği ve geçmiş kimliğini korur.

Yalnız üç yıldızlı eşleşme doğrulanmış olarak kalır. Diğer hatırlanan konular/koşullar benzer adaydır; özellikle IFR/non-RVSM örneğindeki200° kesin sınav derecesi değildir. Hiçbir soru resmî SHGM çıkmış sorusu olarak sunulmaz. Kullanıcının zaman isteğiyle test paketi çalıştırılmadı; kaynak dayanakları incelendi, banka/HTML üretildi ve GitHub Pages'e gönderildi.

Air Law kaynak derlemesinde üç önceki tekrar kararının mevcut kanonik kayıtlar üzerinden çözülmesi ve yeni konu dosyasının dahil edilmesi için:

```bash
python3 scripts/kaynak_derle.py 010 data/kaynaklar/decisions/root_special.json data/kaynaklar/decisions/caab_linx_audit.json data/kaynaklar/decisions/other_airlaw_audit.json data/kaynaklar/decisions/exam_focus_010_20261013.json
python3 scripts/init_db.py
python3 scripts/build_web.py
```
