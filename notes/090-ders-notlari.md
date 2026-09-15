# 090 | Haberleşme — Ders Notları

Kaynak: SHGM eğitim portalı, Haberleşme dersi (B1–B4). Metin ders materyalinden derlenmiştir.

---

## B1 — Terimler, kısaltmalar ve meydan hava durumu

### Temel tanımlar

**Hava trafiği (air traffic):** bir meydanın manevra sahası üzerindeki ve uçuştaki bütün
hava araçları.

**Hava trafik kontrol müsaadesi (ATC clearance):** hava trafik kontrol ünitesinin bir hava
aracına belirli şartlar altında uçma yetkisi vermesi. Uygun yerlerde kısaca **müsaade**
denir; başına uçuşun ilgili parçasını belirtmek üzere **taksi, kalkış, yol, yaklaşma,
iniş** kelimeleri gelebilir.

**Hava trafik kontrol hizmeti:** hava araçları arasında çarpışmaları önlemek, manevra
sahasındaki hava araçları ile manialar arasında düzenli bir trafik akışını sürdürmek ve
hızlandırmak amacıyla yapılan hizmet.

**Karşılıksız yayın (blind transmission):** iki yönlü iletişimin kurulamadığı, ancak
aranan istasyonun yayını alabileceğine inanıldığı durumlarda tek taraflı yapılan gönderme.

**Pist görüş mesafesi (RVR):** pist merkez hattı üzerindeki uçağın pilotunun pist
işaretlerini, pisti belirleyen ışıkları veya merkez hattını görebilme uzaklığı.

### Çalışma saati kısaltmaları

| Kısaltma | Anlamı |
| --- | --- |
| **H24** | Gündüz ve gece boyunca sürekli hizmet |
| **HJ** | Gündoğumundan günbatımına |
| **HN** | Günbatımından gündoğumuna |
| **HX** | Belirli bir çalışma saati yok |
| **HO** | Operasyonel ihtiyaca göre |

### Q kodları

**QDM:** bir istasyona uçmak için kullanılan **manyetik yön**. Rüzgâr yoksa QDM, VDF
istasyonuna ulaşmak için uçulacak rotadır; rüzgâr varsa uçma istikametini bulmak için
QDM'ye rüzgâr düzeltme açısı uygulanır.

**QFE:** meydan referans noktası üzerindeki **yükseklik** (height) — altimetre pistte sıfır
gösterir. **QNH:** ortalama deniz seviyesinden **irtifa** (altitude).

### Mesaj kategorileri

- **Distress mesajı:** hava aracının ciddi veya yakın tehlike içinde olduğunu bildirir
- **Urgency mesajı:** hava aracının, başka bir aracın ya da uçaktaki bir kişinin emniyetiyle
  ilgilidir
- İstikametle ilgili haberleşme mesajları (yön bulma)
- Uçuş emniyetiyle ilgili pilota verilen mesajlar
- Meteorolojik mesajlar
- Uçuş düzenleme mesajları (yer ve bakım hizmetleri)

### Meydan hava durumu

Havadaki pilot meydan hava bilgisini genellikle **yaklaşma kontrol** frekansından, ilgili
Hava Trafik Hizmet Biriminden ister. Bilgi kullanılan pisti de kapsıyorsa **QNH ile
birlikte pist istikameti tekrar edilir**.

### ATIS

Otomatik Terminal Bilgi Hizmeti; meydanın çalışma saatleri boyunca **sürekli** yayınlanan
güncel meydan bilgileri. Ayrılmış bir frekansı yoksa **VOR tanıtma ses kanalından**
yayınlanabilir.

- Her yeni yayın öncekinin yerini alır ve **sıralı alfabetik kodla** tanımlanır
  (ALPHA → BRAVO …)
- Pilot, ATC ile **ilk temasta** aldığı bilginin kodunu söyler; kontrolör böylece doğru
  bilgiye sahip olduğunu doğrular
- İçerik: havalimanı adı, saat, alfabetik kod, kullanılan pist(ler), rüzgâr yönü ve hızı,
  görüş mesafesi, diğer hava şartları

### VOLMET

Meteorolojik rapor ve tahminlerin **HF veya VHF** üzerinden yerden havaya otomatik
iletimi. ATIS **tek** havalimanı için, VOLMET **civardaki birkaç** havalimanı için bilgi
verir — varış ve alternatif meydanlar birlikte planlanır. 2 saat içinde beklenen hava
olayı yoksa **NOSIG** geçer.

### CAVOK

- Görüş **10 km** ve üzeri
- **5000 ft** altında veya **MSA** altında bulut yok
- Kümülonimbus yok
- Önemli hava olayı yok

### Pist görüş mesafesi (RVR)

Kalkış ve iniş hesapları için ölçülür; doğrudan gözlem ya da ölçüm cihazıyla. Pist boyunca
**üç nokta:** **touchdown zone, midpoint, stop end**. Değerler **metre** cinsinden
sıralanır, **fonetik alfabeyle okunmaz**, **readback gerekmez**.

### Pist yüzey durumu ve frenleme

Kar, buz, su performansı etkiler; durum ATIS'te kısaltılmış ifadelerle bildirilir ya da
kontrolörden alınır. Genellikle pistin başından sonuna kadar verilir. **Kuru (dry) veya
nemli (damp) oluş belirtilmez** — başka bir şey söylenmediyse böyle anlaşılır. Kar ya da
buz varsa **fren performansı** raporu da verilir: pist sürtünme katsayısı hesaplanır,
**düşükten yükseğe** kategorilenir.

---

## B2 — Standart ifadeler ve çağrı adları

### Harf, rakam ve zaman

- Harfler ICAO **fonetik alfabesiyle** söylenir
- Tek haneli sayılar olduğu gibi; **çok haneli sayılar rakam rakam** söylenir
  (53 148 → beş üç bir dört sekiz)
- Harf–rakam kombinasyonları ayrı ayrı: TK 9876 → Türk Hava Yolları dokuz sekiz yedi altı
- Zaman **UTC** (GMT, Zulu), 24 saat. Karışıklık ihtimali yoksa **yalnız dakika**
  söylenir; varsa saat ve dakika birlikte

### Vericiyi kullanma tekniği

- Kulaklık kulağa tam oturmalı; mikrofon dudaklara **ne çok uzak** (ses zayıflar, kokpit
  gürültüsü girer) **ne çok yakın** (ses bozulur)
- Frekans değiştirince göndermeden önce **yaklaşık 5 saniye dinle**
- Normal ses tonu, mırıldanmadan ve bağırmadan, tereddütsüz
- Konuşma hızı **dakikada 100 kelime**; yazılacak bilgi aktarırken daha yavaş
- Konuşma düğmesine konuşmadan **önce** bas, bitirene kadar **bırakma** — en sık hata
  erken bırakmaktır
- Sayılardan önce ve sonra küçük duraklama anlaşılırlığı artırır; sık kullanılan anlaşılır
  kısaltmalar hecelenmez
- Uzun mesajda ara sıra boşluk bırak: frekans boş mu, tekrar gerekiyor mu kontrol edilir

### Çağrı adları

İlk temasta yer istasyonunun ve hava aracının **tam çağrı adı** kullanılır. Kısaltmayı
**önce yer istasyonu** yapar, ancak ondan sonra kısaltılmış ad kullanılabilir. Yer
istasyonu = **istasyon adı + hizmet türünü belirten son ek** (Tower, Ground, Approach…).

| Tip | Çağrı adı | Kısaltması |
| --- | --- | --- |
| **1** | ICAO tescil işareti (TC-ABC) | İlk karakter + son iki karakter (T-BC) |
| **2** | Operatör telsiz tanımlayıcısı + tescilin son 4 karakteri | Tanımlayıcı + son 2 karakter |
| **3** | Operatör telsiz tanımlayıcısı + uçuş numarası (Turkish 1234) | **Kısaltılmaz** |

### Haberleşmenin devri

ATC kontrolündeki uçaktan frekans değiştirmesi istenebilir. Uçak kendi isteğiyle frekans
değiştirecekse önce ilgili **ATC biriminden müsaade** alır.

### Telsiz kontrolü

Uçuş başında, genellikle taksiden önce, telsizden şüphe varsa radyo kontrolü yapılır.
Çağrı sırası: **aranan istasyonun çağrı adı → uçak çağrı adı → "Radio check" → kullanılan
frekans.** Yanıt: **uçağın çağrı adı → yanıt veren istasyonun çağrı adı → duyma seviyesi.**

### Readback — kelimesi kelimesine tekrar edilecekler

Uçuş emniyetini doğrudan etkileyen müsaade ve mesajlar pilot tarafından **kelimesi
kelimesine** tekrar edilir; bu, müsaadenin doğru uçağa verildiğini de teyit eder:

ATC yol müsaadeleri · piste giriş · kalkış · iniş · bekleme · pisti kat etme · pist
üzerinde geri dönüş · kullanılan pist · altimetre · transponder kodu · irtifa ve seviye
talimatları · uçuş başı talimatları · hız talimatları · frekans değişikliği · taksi
talimatı · yaklaşma müsaadesi.

**Wilco:** talimatı anladım ve uygulayacağım. **Roger:** son yayınını aldım (talimat
tekrarı yerine geçmez).

### Trafik bilgisi sırası

Kesişen trafik: **12'li saat düzenine göre pozisyon → mesafe → istikamet → biliniyorsa
irtifa ve sürat.**

---

## B3 — Telsiz arızası, acil durumlar ve VHF esasları

### Telsiz arızası

Nadirdir; ekipmanın tam/kısmi arızası ya da **insan hatası** (ses kısık, yanlış frekans).

**Fiziki kontroller:** doğru frekans · ses seviyesi yeterli · **squelch** gereğinden
yüksek değil · mikrofon ve kulaklık jakları tam oturmuş · istasyonun **çalışma saatleri**.

**Sinyal menzili:** yüksekliğin (ft) karekökü × **1,25** ≈ NM; ya da uçuş seviyesinin
karekökü × **12**.

**Sıra:** başka bir ATC biriminin frekansı (Kule, Yaklaşma, Yer) → rota üzerindeki başka
bir istasyon → rota üzerindeki **diğer uçaklar**.

### Distress ve urgency

| | Distress | Urgency |
| --- | --- | --- |
| Tanım | Ciddi ve/veya yakın tehlike, **dışarıdan acil yardım gerekir** | Uçağın, başka aracın ya da bir kişinin emniyeti tehdit altında, **acil yardım gerekmez** |
| Sinyal | **MAYDAY** ×3 | **PAN PAN** ×3 |

- Urgency mesajı mevcut frekanstan verilir; diğer trafikler kesmez; karşılık alamayan bir
  urgency/distress mesajını duyan pilot anladığını bildirip yer istasyonuna **iletir**
- Distress çağrısından önce transponder **7700**; çağrı **kullanımdaki frekanstan** yapılır
  ve başka frekansın daha etkili olacağı söylenmedikçe orada kalınır
- **121,5 MHz** uluslararası acil durum frekansı; **her mesaja karşı önceliklidir**
- Sessizlik: yönlendiren istasyon **"Stop transmitting, Mayday"**; tehlike geçince pilot
  **"cancel distress"**; istasyon sessizliği **"distress traffic ended"** ile bitirir
- Kaçırılma: transponder **7500**; şahit olan istasyon ilgili birimleri haberdar eder

### ELT frekansları

| Frekans | Kullanım |
| --- | --- |
| **121,5 MHz** | Sivil havacılık |
| **243 MHz** | Askerî havacılık |
| **406 MHz** | Arama-kurtarma tespiti |

### Radyo dalgası ve modülasyon

Elektromanyetik dalga, ışık hızında; frekans birimi **Hz**. Sesli haberleşme bantları
**VHF ve HF**. Modülasyon türleri **AM** ve **FM**; havacılıkta **her zaman AM**.

### Hava bandı

VHF bandı 30–300 MHz'dir; havacılıkta kullanılan bölüm **hava bandı (airband)**:
**108–136,975 MHz** (108–117,975 seyrüsefer, **118–136,975 haberleşme**). Haberleşme
bandı **ICAO Annex 10 Volume V** ile düzenlenir.

### Yayılım ve menzil

Radyo dalgası **açık görüş hattı** (line of sight) ile yayılır. Etkileyenler: verici gücü,
verici ve alıcı yükseklikleri, çevredeki engeller, atmosferden/yerden yansıyan dalgalar.

**Azami menzil (NM) = 1,25 × (√h_verici + √h_alıcı)** — yükseklikler feet.

### Kanal aralığı

Tarihsel sıra **100 kHz → 50 kHz → 25 kHz → 8,33 kHz** (25 kHz'lik dilim üçe bölündü).
25 kHz radyoda frekans **5 veya 6** basamak; 8,33 kHz radyoda **6 basamak** zorunlu.

### Parazit ve antenler

Bulutta uçan uçak sürtünmeyle **statik elektrik** yükü biriktirir; yanlış konumlanmış
metal parçalar voltaj değişimine, titreşim ve kontrol yüzeyi hareketi alıcıda cızırtıya
yol açar; pilot frekansın kullanılamadığını bildirir. Antenler **küçük uçakta üstte, büyük
uçakta kuyrukta dikey stabilizatörde**.

### Kule ışık işaretleri

| İşaret | Havadaki uçağa | Yerdeki uçağa |
| --- | --- | --- |
| Sabit yeşil | İniş serbest | Kalkış serbest |
| Kesik yeşil | İniş için geri dön | Taksi serbest |
| Sabit kırmızı | Diğer uçağa yol ver, tura devam et | Dur |
| Kesik kırmızı | Meydan emniyetsiz, inme | Kullanılan iniş sahasından çık |
| Kesik beyaz | İn ve apron'a git | Meydandaki başlangıç noktasına dön |

---

## B4 — VHF prensipleri ve frekans yönetimi

### VHF'nin karakteri

- **Line of sight:** verici–alıcı arasında doğrudan görüş hattı gerekir; menzil çoğunlukla
  **irtifaya** bağlıdır, yer eğriliği ve dağlar kısıtlar
- HF'ye göre gürültüsüz ve kararlı: **iyonosferik yansımayla uğraşmaz**; kısa/orta menzilde
  tercih sebebi
- 30 000 ft'te tipik menzil **~200 NM**
- Atmosferde az kırıldığı için yönlü yayılır; yer istasyonları yüksek arazide ya da kule
  tepesinde
- Mikrofon **2–3 cm** mesafede, sabit ton; konuşmadan önce **1 saniye** bekle; bir frekansta
  aynı anda **tek kişi** konuşur

### Modülasyon ve kanal aralığı

VHF'de **AM**; aynı frekansta birden fazla istasyon yayına girebilir, parazit oluşabilir.
Bunu azaltmak için **8,33 kHz** kanal aralığı — 25 kHz'e göre **üç kat** kanal.
**Avrupa hava sahasında zorunlu.**

### Avantaj ve dezavantaj

Avantaj: yüksek netlik, düşük gürültü, kolay anten uyumu, doğrudan iletişim; ses dışında
**dijital veri** de taşır (**ACARS** bazı durumlarda VHF kullanır). Dezavantaj: uzun
menzilde zayıflar, dağlık alanda **kör bölge**; bu yüzden radar kapsamasıyla planlanır.

### Frekans tahsisi

- Hava bandı **118,000–137,000 MHz**, ICAO **Annex 10 Volume V**
- Ulusal otoriteler ICAO bölgesel planlarına uyar → ülke içi ve uluslararası çakışma önlenir
- Aynı frekansı kullanan iki istasyon arasında en az **150–200 NM**; dağlık bölgede
  **repeater**
- Uçak antenleri gövdenin **üst ve alt** kısmında; büyük uçaklarda birden fazla VHF telsiz
  (biri bozulursa diğeri yedek)

### Atmosfer ve parazit türleri

Sıcaklık terselmesi veya yoğun nem sinyali zayıflatır, parazit/yankı olur; pilot **"Say
again"** der ve sinyal kalitesini rapor eder.

- **Co-channel interference:** aynı frekansta iki istasyonun aynı anda konuşması
- **Adjacent channel interference:** yakın frekanstaki yayınların karışması

Tahsiste yalnız merkez frekans değil **yan bant genişliği** de hesaba katılır.

### Acil durum frekansları

**121,500 MHz** dünya genelinde distress frekansı; tehlike çağrısında ve haberleşme
kaybında **dinlenmek zorundadır**. **123,100 MHz** arama-kurtarma operasyonlarında.

### Frekansların kademelendirilmesi

Bölgesel, yerel ve yaklaşma sahaları arasında kademeli paylaşım. Tipik uçuş sırası:
**GROUND → TOWER → DEPARTURE → ENROUTE → APPROACH → TOWER → GROUND.** Her değişim
**"contact"** ya da **"monitor"** talimatıyla.

### Haberleşme güvenliği

Yetkisiz yayınların engellenmesi, parazit kaynaklarının tespiti, düzenli bakım; bazı
ülkelerde ulusal frekans denetleme birimleri sürekli spektrum tarar. Frekans planlaması
teknik görevin ötesinde emniyetin sürekliliği için stratejik sorumluluktur.
