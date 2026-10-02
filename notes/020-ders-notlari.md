# 020 · Uçak Genel Bilgisi — ders notları

Kaynak: SHGM KDM, *Uçak Genel Bilgisi 1* (U 01 E UO 078), dijital eğitim içeriği. Slayt metinleri düzenlenerek
aktarıldı; videolar ve etkileşim kalıntıları (düğme/şekil etiketleri) atıldı. Bölüm sonu soruları
`data/020_ders_notu_sorulari.json` içindedir.

## BÖLÜM 1 · Pistonlu Motorlar

### 1.1 Motorun yapısı ve genel prensipleri

Motorlar ısı enerjisini mekanik enerjiye çeviren makinelerdir. Isı, yakıtın silindirlerin dışında ya da içinde yakılmasıyla
üretilir: **dıştan yanmalı** (buharlı tren: yakıt dışarıda yanar, buhar basıncı pistonları döndürür) ve **içten yanmalı**
(yakıt doğrudan silindirde yanar, ısı piston–biyel mekanizmasıyla krank miline iletilir). Havacılıkta genellikle **boxer
(zıt silindirli)** motorlar kullanılır: yer çekiminden etkilenmezler ve daha performanslı çalışırlar.

Pistonlu motorlar; silindir dizilimine (sıralı, V, boxer, W, H, zıt pistonlu), ateşlemeye (buji ile / sıkıştırma ile), yakıta
(benzin, dizel, LPG, doğalgaz), zamanlamaya (2, 4, 6 zamanlı), soğutmaya (hava / su) göre sınıflanır. İçten yanmalının diğer
ailesi **tepkili motorlardır** (turbofan, turbojet, turboprop, turboşaft, ramjet, scramjet…).

#### Dört zamanlı motor ve Otto döngüsü
- **ÜÖN (üst ölü nokta, TDC):** Pistonun silindirdeki en üst noktası. **AÖN (alt ölü nokta, BDC):** en alt noktası.
- **Silindir hacmi (swept volume):** AÖN ile ÜÖN arası hacim. **Yanma odası hacmi (clearance volume):** ÜÖN'nin üstünde kalan hacim. İkisinin toplamı **toplam hacim**.
- Piston ÜÖN'den AÖN'ye gidince krank mili **180°** döner; bir zaman = 180°, tam döngü **720°** (4 × 180°).
- Bir döngüde **krank mili 2 tur, eksantrik (kam) mili 1 tur** döner. Eksantrik mili krank milinin **yarı hızında** tahrik edilir, çünkü her valf döngüde yalnız bir kez (krank milinin iki devrinde bir) açılıp kapanır.
- Piston motorlarda yanma **sabit hacimde** olur; süreç aralıklıdır (intermittent).

| Zaman | Olan |
|---|---|
| **Emme** | Emme sübabı ÜÖN'den önce açılır; piston inerken yakıt-hava karışımı silindire dolar. Gaz momentumu nedeniyle sübabın kapanması AÖN'den sonraya (ÜÖN'den sonra basınçlar eşitlenene kadar) ertelenir. |
| **Sıkıştırma** | Emme sübabı kapanır, gaz sıkıştırılır (basınç ve ısı artar). Piston ÜÖN'ye ulaşmadan önce buji ateşler, alev yayılır. |
| **Yanma/güç (ateşleme)** | ÜÖN'de sıkıştırılmış karışım buji kıvılcımıyla yanar; basınç piston ÜÖN'yi geçerken zirve yapar. Yanma, piston AÖN'yi yaklaşık 10° geçince tamamlanır. Krank açısının 90°'sine kadar gazın enerjisinin çoğu mekanik enerjiye dönüşür. |
| **Egzoz** | Egzoz sübabı AÖN'den biraz önce açılır; artık basınç tahliyeyi başlatır (önemli enerji kaybı olmaz). Piston yukarı çıkıp kalan gazı dışarı iter; egzoz sübabı ÜÖN'den sonra gazlar tahliye olana dek açık kalır. |

**Sıkıştırma oranı** = (silindir hacmi + boşluk hacmi) / boşluk hacmi (toplam hacmin yanma hacmine oranı); genellikle yaklaşık 7:1 (şekil örneği 6:1).

**IHP formülü:** IHP = P·L·A·N·E / 33 000 — P ortalama etkin basınç, L strok (AÖN–ÜÖN mesafesi), A piston alanı, N silindir sayısı, E (zaman başına güç strokları, RPM'e bağlı) ve 33 000 foot-pound'u beygir gücüne çeviren sabit. Gösterge diyagramı yalnız motor geliştirme aşamasında kullanılır.

#### Dizel ve benzinli motor
| | Benzinli | Dizel |
|---|---|---|
| Silindire giren | Yakıt–hava karışımı | Yalnız hava |
| Ateşleme | Buji | Sıkışmış havaya enjektörle yakıt püskürtülür; buji yok (ısıtma bujisi var) |
| Sıkıştırma oranı | Daha düşük | Daha yüksek; daha sağlam, **daha ağır** motor |
| Isıl verim | %20–35 | **%30–50** (daha verimli) |
| Güç/ağırlık | Daha yüksek | Daha düşük |
| Gaz kolu | Gaz kelebeğiyle giren hava debisini ayarlar | Yakıt akışını ayarlar; gaz kelebeği ve mixture kolu yoktur |
| Yakıt | Daha yanıcı | Daha az yanıcı |

Enjeksiyonlu benzin motorlarında emme zamanında yalnız hava alınır, buji bulunmaz (ders metnindeki anlatım dizel döngüsüne karışmıştır).

#### Motor parçaları
- **Motor bloğu (karter):** Motorun etrafında kurulduğu çekirdek; genelde alüminyum alaşımı, krank milini yerleştirmek için iki yarım. Sıvı soğutmalıda silindir gömleklerinin etrafında soğutma sıvısı ceketi vardır.
- **Segmanlar:** Grafitli dökme demirden; kompresyon segmanı gaz sızmasını, yağ segmanı yağın yanma odasına geçmesini önler.
- **Biyel kolu:** Yanma kuvvetini krank miline iletir, doğrusal hareketi dairesel harekete çevirmeye yardım eder; **H kesitli** yüksek gerilimli çelikten. Pistona piston pimiyle (küçük uç), krank miline büyük uç yatağıyla bağlanır.
- **Krank mili:** Doğrusal hareketi dönmeye çevirir, torku pervaneye ve aksesuar dişlisine iletir. Muylular ana yataklarda desteklenir; krank pimleri muyludan **krank atımı** kadar kaydırılmıştır (strok = 2 × krank atımı). Eksantrik mili krank milinden tahrik edilir, **sübap zamanlamasından** sorumludur.
- **Silindir kapağı:** Alüminyum alaşımı, kanatçıklı (ısı dağıtımı); yanma odasını kapatır; sübapları, bujileri ve külbütörleri barındırır.
- **Sübaplar (valfler):** Valf kılavuzlarıyla yuvaya eş merkezli tutulur; yüz ve yuva birlikte "alıştırılır". Emme sübabı karışım akışını, egzoz sübabı atık gazları kontrol eder; gücü eksantrik milinden alır.
- **Sübap yayları:** Özel yay çeliği, çoğu zaman **iç içe iki yay**: güvenlik payı sağlar ve **sübap sıçramasını** (rezonans) önler.

### 1.2 Yakıt sistemleri ve karışım oluşumu

**İdeal yakıt:** Tüm koşullarda kolay akış, tam yanma, yüksek kalori değeri, zararsız yan ürün, düşük yangın tehlikesi, kolay çalıştırma, aşındırmama, yağlama.

- **Yakıt tankları:** Uçak yapısı içinde, yuvanın şekline uygun yakıt geçirmez hücreler. Sızıntı noktalarını azaltmak için kör tutturucular kullanılır; yapı, olası kaçağı **dış yüzeye** akıtacak şekilde düzenlenir (tehlikeli birikim olmasın).
- **Spesifikasyonlar:** Jet A-1 → DERD 2494; benzin (AVGAS) → DERD 2485 (AVGAS 100, 100LL, 80).
- **Oktan testi:** Test yakıtı özel test motorunda iki referans yakıtla kıyaslanır: **iso-oktan = 100** (patlamaya çok dirençli), **normal heptan = 0** (kolay patlar). %95 iso-oktan + %5 heptan karışımıyla aynı vuruntuyu veren yakıt 95 oktandır. Oktan = **vuruntu önleme değeri**.
- **Performans numarası:** AVGAS 100 → **100/130**; düşük sayı fakir, yüksek sayı zengin karışım vuruntu sınırıdır. Motorun tasarlandığından **düşük oktanlı yakıt asla kullanılmaz**; doğru oktan yoksa daha yüksek olan kullanılır.
- **Katkılar:** Oktanı artırmak için **TEL (tetraetil kurşun)** eklenirdi (100/130 için galon başına 2 ml); kurşun oksit uçucu değildir, egzoz valfi, yuvası ve buji elektrotlarını aşındırır. Bunu önlemek için **etilen dibromür** eklenir (uçucu kurşun bromür oluşur, egzozla atılır). Kurşunun sağlığa zararı yüzünden **100LL (low lead)** üretilmiştir.
- **Renkler:** **AVGAS 100LL mavi, AVGAS 100 yeşil, AVTUR (jet yakıtı) berrak/saman rengi.** İkmal ekipmanı ve boru hatları da buna göre işaretlenir.
- **Kirlenme:** En sık kirletici **sudur** (güç kaybı, hatta motor durması). Depolar tam doldurulunca nem dışarıda kalır; ikmalden sonra yakıt çökmeye bırakılır, ağır su damlacıkları dibe iner ve tahliye vanasından boşaltılır.
- **Drenaj:** Her tankın dibindeki tahliye vanası (quick-drain) yeterli yakıt akıtılarak boşaltılır, yakıt kapta incelenir. Tahliyeden sonra yangın tehlikesi olmadığından emin olunur; çok su varsa uçak **servis dışı** ilan edilir; vana tam kapanmalıdır.
- **Havalandırma (vent):** Her tankın öne bakan, genelde kanat altında bir havalandırma borusu vardır; atmosfer basıncını korur. Tıkalı/hasarlıysa ters basınç yakıt akışını bozar.
- **Yakıt filtresi (süzgeç):** Sistemin en alt noktasında (genelde motor bölmesi); hızlı boşaltmalıdır. Yakıt seçme valfiyle seçilen her tank için bir kez boşaltılır.
- **Yakıt göstergesi:** Şamandıra tipi sensörler yerde ve düz-sabit uçuş dışında güvenilmezdir; pilot uçuş öncesi kapağı açıp **görsel kontrol** yapar. **Depo seçme valfi** tankları sırayla kullanarak uçağı yanal dengede tutar.
- **Pompalar:** Elektrikli (takviye/yardımcı) pompa **mekanik pompa arızasında** devreye girer; POH'a göre **kalkışta, 1000 ft altında ve inişte** ve tank değiştirirken açık tutulur. Mekanik pompa motordan tahriklidir; basınç göstergesi elektrikli pompa kapalıyken mekanik pompa basıncını gösterir. **Yüksek kanatlı** (tanklar kanatta) uçaklarda yerçekimi akışı yeterli olabilir.
- **Hazırlama pompası (primer):** Çalıştırmadan önce giriş portlarına yakıt basar; kullanımdan sonra **kilitlenmelidir**, yoksa titreşimle açılıp karışımı aşırı zenginleştirir, motoru durdurabilir.

**Yakıt ikmali güvenliği:** Uçakta kimse kalmamalı; motor ve kontak kapalı; yangın söndürücü hazır; sigara yasak; **topraklama kabloları** statik kıvılcımı önler; gerekli rezervler dahil yeterli yakıt; doğru kalite yakıt; kapaklar sıkı (kanat üstündeki kapak düşük basınç bölgesindedir, gevşerse yakıt **sifonla** çekilir); günün ilk uçuşundan önce kirlilik kontrolü; sızıntı kontrolü.

#### Karbüratör ve enjeksiyon
- **Karbüratör** hava–yakıt karışımını **venturi boğazında Bernoulli prensibiyle** hazırlar: boğazda hız artar, statik basınç düşer, yakıt atomize olarak havaya karışır. **Gaz kelebeği** giren hava debisini (dolayısıyla yakıtı) belirler.
- **İdeal karışım 15:1 (kütlece hava:yakıt).** Aynı mixture ayarında yükselince karışım **zenginleşir**, alçalınca **fakirleşir**. İrtifada karışım yavaşça fakirleştirilir; RPM artar, RPM düşüşü görülene dek fakirleştirmeye devam edilip sonra biraz zenginleştirerek tavan RPM yakalanır.
- **EGT:** Fakir karışım yüksek EGT ve CHT; zengin karışım düşük EGT verir. İdeal karışım maksimum EGT'nin **biraz altında**; EGT yükseliyorsa karışım yoksullaştırılıyordur. Zengin karışım yakıtın soğutma etkisiyle motoru soğutur. **CHT** motorun aşırı ısınmasını gösterir; fakir karışım CHT'yi artırır, hemen zenginleştirilmelidir.
- **Mixture kolu:** İleri itmek karışımı zenginleştirir, geri çekmek fakirleştirir. Kalkış/tırmanışta ve sıcak havada zengin; seyirde yakıt ekonomisi için EGT/CHT izlenerek fakir.
- **Direkt (enjeksiyon) sistemi:** Düşük basınçlı **devamlı akışlı** tip: yakıt emme sübabına yakın püskürtülür. Avantajları: düşük çalışma basıncı, iyi yakıt dağılımı, **buzlanma sorunu olmaması**, zamanlama gerektirmeyen pompa. Bileşenler: yakıt pompaları, yakıt kontrol ünitesi, dağıtım manifold valfi, her silindir için nozul, yakıt basınç göstergesi. Gaz kolu ölçücü valfi motor devrine göre yakıt basıncını değiştirir; özel idle ayarı ve start için jikle gerekmez.
- **Karbüratör buzlanması:** En çok **−5 ile +20 °C**, **%50 ve üzeri bağıl nem** ve gaz **idle** konumunda olur; bu şartlarda **carb heat** açılır. Carb heat motora giren hava yoğunluğunu azaltır (performans kaybı), bu yüzden **kalkışta hiçbir koşulda açılmaz**. Buzlanma en çok venturi çıkışı/gaz kelebeği bölgesinde olur (genişleyen yapıda hız düşer).

### 1.3 Yağlama ve soğutma sistemleri

Yük, ısı ve hız arttıkça sürtünme ve aşınma artar; **yağlama** hareketli yüzeyleri ayırarak bunları azaltır.

**Yağın görevleri:** sürtünme/aşınma ve ısınmayı azaltmak, iç soğutma, titreşim/şok emme, motoru temizleme (partikül toplama), korozyonu önleme, motor hakkında bilgi verme (ikaz). **Ana parçalar:** yağ hatları, basınç pompası, filtre ve elekler, yağ haznesi, soğutucu, göstergeler; kuru karterli sistemde ayrıca depo ve boşaltma (scavenge) pompaları.

| | Islak karter | Kuru karter |
|---|---|---|
| Yağ nerede | Karterin içinde (krank mili yatağı) | Motordan bağımsız uzak depoda |
| Artı | Yapıyı basitleştirir | Islak sistemin sorunlarını çözer |
| Eksi | Eğik karter, **ters uçuş tehlikesi**, sıcak karter, kirlenen yağ | **Ağırlık** |

Islak karterde basınç pompası yağı filtreden geçirip **yağ galerisine** basar; krank mili ana yataklarını ve aksesuar tahriklerini yağlar.

- **Göstergeler:** Basınç, sıcaklık, miktar. Basınç ve sıcaklık göstergesi kokpitte **zorunludur**; miktar göstergesi yoksa uçuş öncesi seviye çubuğuyla bakılır. **Yağ basıncı** basınç pompası çıkışında ölçülür (tipik yeşil yay **50–90 psi**); motor çalışınca **30 saniye içinde** yükselmezse motor derhal durdurulur. Aşırı basınçta basınç tahliye valfi devreye girer. **Yağ sıcaklığı** pompa girişinde ölçülür (tipik yeşil yay **100–245 °F**); soğuk motorda hemen yükselmez, normaldir.
- **Viskozite (SAE / Saybolt Universal):** Sıvının iç sürtünmesinin ölçüsüdür; **sayı düştükçe yağ incelir**.
- **Hidrolikleşme (hydraulicing):** Radyal ve ters çevrilmiş motorlarda alt silindirlerde piston ile kapak arasında yağ birikmesi; marşta piston kırılması, biyel bükülmesi, silindir/krank mili hasarı. Önlem: **manyeto KAPALIyken** pervane elle çevrilerek motor döndürülür.
- **Arızalar:** Normal sıcaklıkta çok yüksek basınç → tahliye valfi ayarı bozuk (düşük sıcaklıkta yağ koyu olduğu için de olabilir); çok düşük basınç → valf ayarı, yataklarda aşınma boşluğu veya basınç pompası çıkışında sızıntı; ibrede **dalgalanma** → tahliye valfi yapışıyor veya yağ az; **basınç aniden sıfıra** düşerse pompa arızası ya da ciddi yağ kaybıdır, **motor derhal durdurulur**.

#### Hava ve sıvı soğutma
Hafif uçak benzin motorunun ısıl verimi yaklaşık %30'dur; enerjinin ~%70'i kaybolur (yaklaşık %40'ı egzozla, %30'u motor bileşenlerini ve yağı ısıtmakla). **Hava soğutma** daha hafif, basit, ucuzdur (hafif uçaklarda tercih edilir) ama soğutma performansı düşüktür. Bileşenler: **yangın duvarı, kaporta, cowl flap (kaporta klapesi/panjur) ve silindirler arası deflektörler (baffles)**. Cowl flap açıklığı hava akışını artırır; baffle'lar havayı silindirlerin çevresine yönlendirir. Verimi belirleyenler: **dış hava sıcaklığı (OAT)**, **hava akış hızı** (cowl flap), **soğutma kanatçıkları** (silindir başlarında yoğun, çünkü patlama orada olur).
**Sıvı soğutma** daha verimlidir, ısıyı daha iyi kontrol eder; **daha güçlü motorlu yüksek hızlı uçaklarda** kullanılır. Kapalı devre sıvı motor bloğundaki kanallarda dolaşır, ısıyı radyatör/ısı eşanjörüyle havaya verir.

**Yeterli soğutma için:** Uçuş öncesi kaporta hava giriş/çıkışının tıkalı olmadığını, bölmelerin ve kaportanın durumunu, varsa kapak/ızgara çalışmasını ve yağ seviyesini (yağ soğutmada da rol oynar) kontrol et. **Kalkıştaki gibi yüksek güç ve düşük hızda kaporta kanatları (cowl flap) açık seçilir**; tırmanma ve seyirde motor sıcaklığı optimumda tutulacak şekilde ayarlanır. Uzun tam güç tırmanışında yağ ve silindir kapağı sıcaklığı yakından izlenir; CHT aşırıysa motoru soğutacak uygun prosedür uygulanır.

### 1.4 Ateşleme sistemleri ve motor performansı

- **Bujiler** ateşlemeyi elektriksel yapar ve **manyetolardan** beslenir. Tüm pistonlu motorlarda **çift ateşleme** vardır: silindir başına **iki buji, ayrı iki manyeto**. Çift ateşleme arıza riskini azaltır, silindiri iki noktadan ateşleyerek yanma süresini kısaltır, güç ve verimi artırır; ateşleme piston ÜÖN'ye gelmeden hemen önce olur.
- **Buji kirlenmesi (fouling):** Buji uçlarının fazla yakıt, yağ veya karbonla kaplanması. Nedenleri: sürekli zengin karışım, tam zengin karışımla tırmanma, yanlış karışım, ilk çalıştırmadan önce fazla yakıt pompalama (excessive priming), sürekli düşük RPM, gazsız uzun alçalma (idle), motorun yağ yakması.
- **Erken ateşleme (pre-ignition):** Yanmanın buji ateşlemesinden **önce** başlaması; önceki döngüden kalan kıvılcım, aşırı sıcak nokta veya aşırı ısınma (yüksek CHT) neden olur.
- **Vuruntu (detonation):** Normal döngü dışında ani, kontrolsüz patlama (normal alev yerine kontrolsüz alev). Nedenleri: yanlış karışım oranı, yüksek EGT, **yanlış (düşük) oktanlı yakıt**, ateşleme zamanlamasının çok ileri olması, kendiliğinden tutuşma, yüksek basınç, **sabit hızlı pervanede düşük RPM–yüksek güç** ayarı.
- **Manyeto:** Motordan hareketini alan, **harici güç kaynağı gerektirmeyen** elektrik jeneratörüdür; dönen manyetik rotor primer sargıda enerji oluşturur, sekonder sargıya aktarılır ve yüksek gerilimli kıvılcım üretilir.
- **Manyeto kontrolü (run-up):** Motor maksimum RPM'inin yaklaşık %75'ine alınır (Cessna 172 için 1800 RPM). **Both** konumuna göre Left veya Right'ta düşüş **en çok 175 RPM**, Left ile Right arasındaki fark **en çok 50 RPM** olmalıdır.
- **Impulse coupling (impuls kaplini):** Marş sırasında manyeto dönüşünü yayla geçici hızlandırıp **gecikmeli (güçlü) kıvılcım** verir; motor ile manyeto arasındadır, genelde **yalnız sol manyetoya** takılır.
- **Performans:** İrtifa arttıkça yoğunluk, basınç ve sıcaklık değişir; karışım oranı ve RPM de değişir, performansı etkiler. **MAP (manifold absolute pressure):** Gaz kelebeği ile emme sübabı arasında karışım basıncını ölçer; piston motorlu uçak için performans göstergesidir. İrtifa arttıkça MAP azalır, motor gücü de azalır.
- **Süperşarj (kompresör):** Gücünü **motordan** alır (karbüratörlü motorda karbüratörden sonra yakıt/hava karışımını sıkıştırır). **Artı:** her devirde, düşük devirde de çalışır. **Eksi:** motor gücünün bir kısmını harcar.
- **Turboşarj:** Gücünü **egzoz gazlarından** alır (türbin + kompresör); yoğunluğu düşük havayı sıkıştırarak yoğunluğunu artırır. **Artı:** motordan güç çalmaz. **Eksi:** egzoz gazı artınca verimli olur, **alt devirde etkisiz**, ani gaz emrinde **turbo-lag** (gecikme); devri gelene dek motor atmosferik gibi çalışır.

### 1.5 Pervaneler ve motor gücü aktarımı

Pervane motorun mekanik enerjisini, havayı geriye hızlandırarak itkiye çevirir (**Newton'un 3. yasası**); burkulmuş bir kanat profilidir. Kokpitten bakınca **pervane saat yönünde dönüyorsa uçak sola sapar** (müzdevice etki / tork reaksiyonu); dengelemek için gaz açıldığında **sağ rudder** verilir.
- **Burkulmuş pal (blade twist):** Pal üzerindeki hava hızı uca doğru arttığı için, her noktada eşit hücum açısı ve düzgün itki dağılımı sağlamak üzere pal uca doğru burkulmuştur (pal açısı uca doğru azalır).
- **Sabit hatveli pervane:** Pal açısı değişmez, seyir hızında en verimli olacak şekilde sabitlenmiştir; krank miline/dişli kutusuna doğrudan bağlıdır; RPM motor devrine bağlıdır (gaz açılınca artar). Çalışma hücum açısı, bağıl hava akışı ile pal kordo hattı arasındaki açıdır.
- **Değişken hatveli pervane:** Uçuşta pal açısı ayarlanır; **RPM'i manifold basıncından bağımsız seçmeye** izin verir (gaz kolu + RPM kolu), en iyi verim, yakıt tasarrufu ve en az motor aşınması için. Pervane, iç **ince ve kalın hatve stopları** arasında çalışır.
- **Sabit hızlı (constant speed) pervane:** Değişken hatvelinin otomatiği: kontrol ünitesi (CSPU/governör) pal açısını değiştirerek **RPM'i sabit tutar**; **en geniş hız aralığında yüksek verim** verir. Mavi kolla ayarlanır: kol en ileride = en küçük pal açısı (fine), geriye çektikçe açı büyür, en geride = **feather**.

| Hatve durumu | Özellik / kullanım |
|---|---|
| **Fine (düşük açı)** | Çalıştırma, kalkış ve tırmanış; uçak atik, son hız düşük, drag yüksek; **windmilling** için de kullanılır. **Tek motorlu uçakta motor arızasında** pervane en ince hatveye getirilir (havanın palleri döndürüp motoru yeniden çalıştırmasına yardım eder). |
| **Coarse (büyük açı)** | Seyir ve yüksek hız; min. yakıt tüketimi, en yüksek son hız, atik değil. Açı büyüdükçe drag azalır. Düşük RPM–yüksek gaz "kazıklama" doğurabilir. |
| **Feather** | Teorik olarak en büyük açı; pal hava akışına paralel, **sürtünmenin (drag) en az olduğu** konum. **Çok motorlu uçakta arızalı motor feather edilir** (min. drag, min. asimetrik uçuş). |
| **Reverse (negatif itki)** | İnişte durmaya yardım için (genellikle turboprop); geriye itki sağlar. |

**Pervane verimliliği** = (itki × TAS) / (pervane torku × RPM). Sabit hatveli pervane düşük açıda sabitlenirse tırmanışta, biraz daha büyük açıda sabitlenirse seyirde verimlidir; **sabit hızlı pervane çok geniş hız bandında maksimum verimini korur.**

## BÖLÜM 2 · Alet ve Gösterge Sistemleri

### 2.1 Giriş ve temel prensipler
Sensörlerden, dış ortamdan ve yer istasyonlarından gelen bilgi kokpitte ilgili göstergelerle sunulur. Temel uçuş aletleri, motor aletleri ve haberleşme–seyir aletleri bordo panelinde bulunur. Kokpit; aletleri, bordo panelini, pedestal paneli, konsolları, lövye, gaz kolu, direksiyon-fren gibi sistemleri içerir; uçak tipine ve ergonomiye göre düzenlenir (yan yana iki kişilik, tek kişilik, ön-arka).
**Temel uçuş aletleri (6):** sürat saati, durum cayrosu (attitude), altimetre, varyometre, istikamet (heading) göstergesi, dönüş koordinatörü (turn and slip). Haberleşme/seyir aletleri hafif uçaklarda genelde panelin ortasında; **motor aletleri** temel uçuş aletlerinin sağında/solunda yer alır.

### 2.2 Sıcaklık algılama
Sıcaklık, atom/moleküllerin kinetik enerjisinin ölçüsüdür. **°C = (°F − 32) / 1,8**; Celsius 100 bölme, Fahrenheit 180 bölme (donma–kaynama noktası arası). Sıcaklık, sistemlerin limit içinde çalıştığını izlemek ve uçuş planlaması için gerekir. Motor durum göstergeleri: silindir başı sıcaklığı (CHT), yağ sıcaklığı, egzoz gaz sıcaklığı (EGT).

| Sensör | Prensip | Not |
|---|---|---|
| **Çift metal şerit (bimetal)** | Aktif ve pasif metalin farklı genleşmesi; şerit pasif bileşene doğru bükülür, ibreyi hareket ettirir. | Elektrik gerekmez; **uzaktan ölçüm için kullanılmaz**; −50 ile +400 °C. |
| **Değişken dirençli termometre** | Wheatstone köprüsünde pozitif sıcaklık katsayılı direnç (sıcaklık artınca direnç artar). | Genel olarak ~**150 °C**'ye kadar. |
| **Termokupil** | İki farklı metalin (chromel +, alumel −) birleşim yeri ısınınca **sıcak ve soğuk bağlantı arasında voltaj** doğar; dışarıdan elektrik gerekmez. | **1300 °C**'ye kadar; uzaktan gösterime uygun; pistonlu motorda **CHT** ölçümünde (ve EGT'de) kullanılır. |

### 2.3 Basınç gösterge sistemleri
**P = F / A**; birimler: N/m², Pascal (Pa), milibar (mb), psi, inHg. Sistemlerdeki hava (lastik) ve sıvı (yağ, hidrolik) basınçları emniyet için izlenir.

| Sensör | Özellik |
|---|---|
| **Diyafram** | Yarı esnek, oyuk yuvarlak metal; iki bölüm arasında bariyer, basınç farkıyla hareket eder; **düşük basınç** ölçer. |
| **Kapsül** | İki diyaframın birleşimi. **Basınç kaynağıyla temaslıysa basınç kapsülü** (sürat saati, varyometre); **temassızsa (kapalı) eneroid kapsül** (**altimetre**). Körüklü kapsül yakıt basıncı gibi yüksek/orta/düşük basınç ölçer. |
| **Burdon tüpü** | "C" şeklinde esnek boru; bir ucu sabit (basınç girişi), diğer ucu kapalı ve ibreyi çeviren dişliye bağlı; **yüksek basınç** ölçümünde. |
| **Katı hal sensörleri** | **Karbon diskli** (basınç diskleri sıkıştırır, direnç ve voltaj değişir) ve **piezoelektrik** (kristal sıkışınca voltaj üretir). |
| **Uzaktan gösterge** | Değer ölçülüp elektrik sinyaline çevrilerek kokpite gönderilir (sızıntı/yangın riskini kaldırır). |

### 2.4 Yakıt ve akış gösterge sistemleri
Hafif uçaklarda yakıt hacim birimiyle (litre/galon), büyük uçaklarda kütle birimiyle (kg/pound) izlenir. İlk uçaklarda şamandıraya bağlı görsel çubuk; modern hafif uçaklarda tankta **yüzer (şamandıra) sensör**: yoğunluğu yakıttan az şamandıra, kolla reostaya bağlıdır; yakıt azaldıkça direnç ve voltaj değişir. **Kapasitif sistemde** yakıt seviyesi düşünce dielektrik sabiti ve kapasite düşer; sıcaklık ve yoğunluk değişimi hata yaratır, bu yüzden **sıcaklık kompanzasyon devresi** bulunur. Mekanik float göstergeler basittir ama türbülans ve sarsıntıya duyarlıdır.
- **Akışmetre (flow meter):** Yakıtın motora gidiş hızını ölçer; motor giriş hattına yakın monte edilir. Bölme plakalı sensörde yakıt plakayı döndürür, açı senkro ile göstergeye aktarılır. **Pistonlu motorda hacimsel, jet motorda kütlesel** ölçülür.
- Göstergeler her tank için ayrı verilir; **total fuel** ve **usable fuel** (pompalarla alınabilen) gösterebilir; tank dibinde kalan kullanılamaz kısım **unusable fuel**'dir. Devre genelde DC ile çalışır, uzun kablolar elektromanyetik paraziti için korunur.

### 2.5 Pozisyon ve hareket aktarım sistemleri
Sensör değerleri mekanik, pnömatik, hidrolik, elektrik ve elektronik olarak göstergeye aktarılır. Mekanik aktarım artık az kullanılır; flap/valf/kontrol yüzeyi pozisyon bilgisinde kullanılmıştı. **Pnömatik** aktarımda pitot/statik basıncı borularla alete taşınır (altimetre, sürat saati).
- **Elektrik aktarım:** DC aktarım **desyn**, AC aktarım **senkro**. AC senkro (26 V AC, değişken transformatör prensibi; primer sargılı rotor, sekonder sargılı stator) iki tiptir: **tork senkro** (algıladığını aynen aktarır, açısal pozisyonlama; verici ve alıcıda 120° aralıklı üç sekonder sargı, seri bağlı) ve **servo senkro** (sinyali yükselteç ile güçlendirir; **daha ağır yükleri sürer**, ör. cayromanyetik göstergede cayroyu ayarlamak). Rotor–stator sistemin adı **selsyn**.
- **Dijital aktarım:** Sensör bilgisi veri yoluna (data bus) alınır, analog veri dijitale çevrilir; çok kabloyu azaltır. Standardı **ARINC** (Aeronautical Radio Incorporated) belirler (ör. **ARINC 429** data bus; otopilot, INS, FMS, flight director, EADI/EHSI bu yoldan haberleşir).
- **Takometre (RPM göstergesi):** Pistonlu motorda krank mili dakikadaki devri, gaz türbininde kompresör şaftı devridir. **Mekanik (manyetik) takometre** genelde tek motorlu pistonlu uçakta; esnek sürücü şaft, mıknatıs, alüminyum/bakır **sürükleme kabı (drag cup)** ve yay: dönen mıknatıs kapta **eddy akımı** oluşturur, tork yay gerilmesiyle dengelenir, devir arttıkça gösterge artar.

## BÖLÜM 3 · Aerodinamik Parametrelerin Ölçümü

### 3.1 Basınç ve sıcaklık ölçüm sistemleri
Uçuşlar çoğunlukla troposfer ve nadiren stratosferde olur; hava yoğunluğu sıcaklık, basınç, nem ve irtifaya göre değişir. Taşıma formülü L = ½ρV²SCL (ρ yoğunluk, V gerçek hız TAS, S kanat alanı, CL katsayı).

- **Statik basınç (Ps):** Atmosferi oluşturan gazların yerçekimiyle yarattığı basınç; üstteki atmosfer sütununun ağırlığıdır (P = F/A = W/A = mg/A). Yükseldikçe azalır. **Altimetre** statik basınç değişimini irtifaya kalibre eden göstergedir.
- **Dinamik basınç (Pd veya q):** Hareket eden akışkanın kinetik enerjisinden doğar: **q = ½ρV²**. **Hava sürat göstergesi** dinamik basınca göre çalışan, hıza kalibre göstergedir.
- **Toplam basınç:** **Pt = Ps + Pd**; Pd = Pt − Ps; Ps = Pt − Pd. Bu hesaplar yaklaşık **200 kt veya Mach 0,3'e** kadar hava **sıkıştırılamaz** varsayımıyla geçerlidir; üzerinde hava sıkışır, çarpma basıncı (impact pressure) toplam basıncı ve hesaplanan dinamik basıncı artırır — sürat saati okumasında hata.
- **Statik delikler (portlar):** Altimetre, sürat saati, varyometre ve Mach göstergesine (varsa ADC'ye) atmosfer statik basıncını verir. Gövdeyle **düz** yerleştirilir; hat su taşımasın diye uygun eğimlidir. Doğru bilgi için toz, böcek ve buzdan uzak olmalı; uçuş öncesi kontrol edilir.
- **Alternatif statik kaynak:** Basınçsız küçük uçaklarda tıkanmaya karşı **kabin içinde**; venturi etkisiyle mevcuttan düşük basınç okur, bu yüzden biraz hatalı değer verir (yüksek hücum açısında statik deliklerdeki anafor da gerçek basıncı etkiler).
- **Pitot tüpü (toplam basınç):** Ucu açık, boylamsal eksene paralel; **buzlanmaya karşı ısıtıcısı ve su tahliye hattı** vardır; sınır tabakasından uzak olması için gövdeden çıkıntılıdır (burun, kanat altı veya dikey stabilize). Sürat saatine ve (transonik/süpersonikte) Mach göstergesine toplam basıncı verir.
- **Pitot/statik başlık:** İkisi tek başlıkta; pitot borusuna dik yan statik delikler. **Pitot (toplam basınç) yalnız sürat saatini (ve Mach'ı) besler; statik basınç sürat saatini, altimetreyi, varyometreyi ve yüksek hızlı uçaklarda Mach göstergesini besler.** Uçuştan sonra başlık kılıfı takılmalıdır.
- **Sıcaklık ölçümü:** OAT (SAT) hesaplamalar, planlama ve sistemler için gerekir. Sıcaklık artınca yoğunluk ve taşıma düşer; aynı dinamik basınç için TAS artmalı, **kalkış-iniş mesafesi uzar**; yakıt tüketimini ve motor performansını etkiler, buzlanma taşımayı düşürüp sürüklemeyi artırır, **stall hızını yükseltir**. Çift metal şerit sensör genelde kanopide, güneş temasından korunmalı yerde; cıvalı kılcal boru sensör dış ortama maruz cıvanın genleşmesiyle Burdon sensör ve ibreyi oynatır.
- **Tıkanma ve sızıntı:** Altimetre statik deliği tıkanırsa en son basıncı gösterir (tıkanma irtifasının üzerine çıkınca **düşük**, alçalınca **fazla** okur). Statik hatta sızma olursa **basınçlı uçak kabin irtifasını** gösterir; **basınçsız uçakta venturi etkisiyle fazla irtifa** okunur.

### 3.2 Altimetre ve atmosfer modeli
Altimetre bağlanan basınç noktasını sıfır ft kabul edip dikey mesafeyi (genelde feet; 1 m ≈ 3,3 ft) gösterir: **QNH** ayarlıysa **irtifa (altitude)**, **QFE** ayarlıysa **yükseklik (height)**, **standart (1013,25) ayarlıysa uçuş seviyesi (flight level)**. Basınç–yükseklik ilişkisi doğrusal olmadığı için kalibrasyon zordur. Yüksek–alçak basınç sistemleri göstergeyi etkiler: 1020 mb'den 1004 mb'lik bölgeye ayarsız uçan uçağın altimetresi **gerçekte daha alçakta** olduğunu saklar (yüksekten alçak basınca = gerçek irtifa düşük). Sıcaklık da etkiler: sıcak bölgede kontürler (eş basınç eğrileri) genişler, gösterge aynı irtifayı (ör. 700 hPa = 10 000 ft) gösterse de **gerçek irtifa yüksektir**; soğuk bölgede **gerçek irtifa düşüktür**. Bu sapmaları düzeltmek için ICAO **ISA** (standart atmosfer) tanımlanmıştır.

**Kalibrasyon:** Üreticiler ISA tablosuyla kalibre eder; basınç–irtifa doğrusal değildir, bu dinamik tasarımlı eneroid kapsüller ve değişken büyütme koluyla doğrusal okumaya çevrilir. **ISA'da MSL'den 11 km'ye kadar 1 hPa (mb) basınç değişimi ≈ 27 ft** (yükselirken 1 hPa düşüş = 27 ft artış; formül: 96 × T/P = 96 × 288/1013,25 ≈ 27).

#### QFE, QNH, standart ayar
| Ayar | Anlamı | Altimetre ne okur |
|---|---|---|
| **QFE** (Q Field Elevation) | Meydanda o an okunan basınç. | Meydanda yerde **0 ft**; havada meydandan dikey mesafe = **yükseklik (height)**. Meydan turlarında kullanılır. |
| **QNH** | Meydan basıncının (QFE) **ortalama deniz seviyesine (MSL) indirgenmiş** hali. | MSL'den dikey mesafe = **irtifa (altitude)**. Meydanda QNH bağlıysa okunan **meydan rakımı (elevation)**'dır. Haritalardaki tüm yükseklikler MSL'dedir; manialardan geçişte en uygun ayar QNH'dir. QNH günlük değiştiği için METAR ve kuleden teyit edilip güncellenmelidir. |
| **SPS / QNE = 1013,25 hPa (29,92 inHg)** | Standart basınç ayarı. | **Uçuş seviyesi (flight level)**, yani **basınç irtifası**. Geçiş irtifasında bağlanır; arazi yüksekliği dikkate alınmaz, bu yüzden uçuş seviyesinin arazinin üstünde olduğundan emin olunmalıdır. Bölgedeki QNH 1013'ten büyükse QNH irtifası basınç irtifasından büyük olur (mania kleransı artar); QNH 1013'ten küçükse kleransı düşer. |

*Örnek (ders):* Meydan rakımı 540 ft, QFE 990 hPa → 540/27 = 20 hPa → **QNH = 990 + 20 = 1010 hPa**.

#### Yoğunluk irtifası, gerçek irtifa
- **Basınç irtifası:** 1013,25 hPa (29,92 inHg) noktasından okunan irtifa (SPS).
- **Yoğunluk irtifası (density altitude):** **Sıcaklık için düzeltilmiş basınç irtifası**; altimetrede gösterilmez. Sıcaklık ISA'daysa basınç irtifasına eşittir (ISA sapması sıfır). **DA ≈ basınç irtifası + 120 × ISA sapması.** *Örnek:* basınç irtifası 6000 ft, 30 °C. 6000 ft'te ISA = 15 − 2×6 = 3 °C → sapma +27 → DA = 6000 + 27×120 = **9240 ft**. Sıcaklık artınca yoğunluk irtifası artar; aynı dinamik basıncı elde etmek için kalkış koşusu ve pist mesafesi uzar.
- **Gerçek irtifa (true altitude):** MSL'den gerçek dikey mesafe, mania kleransı buna göre belirlenir; altimetrede gösterilemez. 1 °C sapma hava sütun kalınlığını **%0,4** değiştirir. **TA = gösterge irtifası + (ISA sapması × 4/1000 × gösterge irtifası)** (4 ft/1000 ft/°C). *Örnek:* QNH ayarlı, 10 000 ft, ISA −10 °C → TA = 10 000 − 400 = **9600 ft**; 500 ft'lik meydandan yükseklik = 9100 ft.
- **Yükseklik (height):** Belirlenmiş bir noktadan dikey mesafe. **İrtifa (altitude):** MSL'den dikey mesafe; meydanın deniz seviyesinden yüksekliği **elevation (rakım)**. **Seyir seviyesi:** Seyir kısmında dikey konumu tanımlayan genel terim (QNH/SPS/QFE'ye göre).
- **Geçiş irtifası (transition altitude), geçiş seviyesi (transition level), geçiş tabakası (transition layer):** **Geçiş seviyesi geçiş irtifasının üzerindeki en düşük uçuş seviyesidir**; ikisi arasındaki boşluk **geçiş tabakasıdır** (her ülke kalınlığını belirler). Tabakada **tırmanışta dikey konum uçuş seviyesiyle, alçalışta irtifayla** ifade edilir. Geçiş irtifasında 1013 bağlanır; geçiş seviyesi altında QNH ile uçulur, seviye kule (ATC) tarafından bildirilir.

#### Altimetre tipleri
- **Basit altimetre:** Koruma kabı, statik giriş, kısmi havalı hava geçirmez **eneroid kapsül**, yaprak yay, mekanik bağlantı, ibre; sıcaklık telafisi vardır. Yükselince kapsül genişler, alçalınca daralır.
- **Hassas altimetre:** 2–3 eneroid kapsül, sürtünmeyi azaltılmış bağlantı, **titreşim cihazı**; ayar düğmesiyle QNH/QFE/1013 girilir. Yerde duran uçakta günlük basınç değişimiyle ibre oynar ama basınç penceresi değişmez (pilot ayarlarsa değişir). Çalışma aralığı **0–80 000 ft**.
- **Servo destekli altimetre:** Mekanik sürtünmesiz, çok hassas; **servo motor** ibreyi döndürür; dijital/analog; irtifa bilgisi **transpondere ve ADC'ye** gider; **0–100 000 ft**.
- **Altimetre hataları:** Alet hatası; **pozisyon/basınç hatası** (statik delikler yetersiz basınç alır; hız ve hücum açısı arttıkça büyür); **zaman gecikmesi** (**tırmanışta düşük, alçalışta fazla okur**); **manevra kaynaklı hata** (pitch değişiminde geçici dalgalanma); **barometrik hata** (basınç değişince yeniden ayar yapılmamışsa); **sıcaklık hatası** (ISA dışı sıcaklıkta sütun kalınlığı %0,4/°C değişir).

### 3.3 Hava sürat göstergesi (ASI) ve hataları
ASI **dinamik basıncı** ölçer ve hıza kalibre eder; koruma kabı, statik hat, pitot hattı, basınç kapsülü, mekanik bağlantı, ibre. Birim knot (**1 NM = 1,852 km, 1 kt = 1,852 km/s**). *Sürat skaler, hız vektöreldir (yön+şiddet).*
**Çalışma:** Pitot toplam basıncı (Pt = Pd + Ps) basınç kapsülüne gelir; statik basınç koruma kabına gelir. Kapsül ve kap içindeki statik basınç birbirini dengeler, kapsüle yalnız **dinamik basınç** etki eder; kapsül şişer, ibre IAS gösterir.

| Sürat | Düzeltme |
|---|---|
| **IAS** (Indicated) | Göstergedeki okuma. |
| **CAS** (Calibrated) | IAS ± alet ve pozisyon/basınç hataları. |
| **EAS** (Equivalent) | CAS ± **sıkıştırılabilirlik** hatası (EAS = CAS + compressibility). |
| **TAS** (True) | EAS ± **yoğunluk** hatası. Sıkışma yoksa TAS = CAS ± yoğunluk hatası. |

(Hatırlatma cümlesi: **I-C-E-T**: Instrument/position → Compressibility → Density.) IAS'tan TAS'a çevirme uçuş bilgisayarı veya **ADC** ile yapılır (örnek: FL300, CAS 400, SAT −52 °C → TAS ≈ 641 kt); tahmini TAS ≈ CAS + (irtifa/1000 × 1,75 × CAS/100).
- **Alet hatası:** Sürat saati ISA'ya (1013 mb, MSL, 15 °C, 1,225 kg/m³) kalibredir. **Yoğunluk hatası:** q = ½ρV² olduğu için ISA dışı yoğunluk dinamik basıncı değiştirir. **Sıkıştırılabilirlik hatası:** 0,3 Mach / 200 kt üzerinde pitot önündeki hava sıkışır, basınç gerçek dinamik basınçtan **fazla** olur → ASI **fazla okur**; yüksek irtifa ve yüksek hızda artar. **Pozisyon/basınç hatası:** statik ve pitot konumu, hız, hücum açısı.
- **Pitot tıkanması (genelde buz):** ASI **altimetre gibi davranır**. Düz uçuşta tıkanırsa sürat sabit kalır, gaz değişimine tepki vermez. **Tırmanışta fazla okur (over-read), alçalışta düşük okur (under-read).**
- **Statik hat tıkanması:** Düz uçuşta doğru gösterir ama gaz değişiminde ilgisiz; **tırmanışta düşük okur (under-read), alçalışta fazla okur (over-read).**
- **Sızıntılar:** Pitot hattında sızıntı → düşük okur. Statik hatta sızıntı ve basınçsız uçak → **fazla okur**; basınçlı uçakta kabin basıncına göre okur.

### 3.4 Dikey sürat göstergesi (VSI / varyometre)
Dikey hızı **ft/dk** cinsinden gösterir; **basınç değişim oranını** algılar. Düz uçuşta sıfır gösterir. Parçalar: koruyucu kap, statik hat girişi, **kılcal (boğumlu) ölçme ünitesi**, basınç kapsülü. Statik basıncın bir kısmı doğrudan kapsüle, bir kısmı kılcal üniteden geçerek kaba girer; **tırmanışta kaptaki basınç kapsülündekinden fazladır, alçalışta kapsül basıncı kaptakinden fazladır** → tırmanış/alçalış varyosu.
- **Hatalar:** Alet hatası (tornavidayla sıfırlanabilir); pozisyon/basınç hatası (ani hız değişimi, ör. kalkış ivmelenmesi); manevra kaynaklı hata; **zaman gecikmesi** (uzun tırmanış/alçalışta, kararlı fark oluşumu birkaç saniye alır).
- **Statik delik tıkanması:** Tırmanış/alçalışta basınçlar eşitlenir, varyo bir süre sonra sıfıra döner; düz uçuşta tıkanırsa tırmanışta/alçalışta hep sıfır gösterir.
- **IVSI (anlık VSI):** Gecikmeyi gidermek için normal varyometreye **akselerometre** eklenmiştir.

## BÖLÜM 4 · Uçak Gövdesi ve Yapısal Elemanlar

### 4.1 Uçağa etki eden kuvvetler
Temel gövde parçaları: gövde, kanatlar, kuyruk tertibatı (dikey stabilize + yön dümeni, yatay stabilize + irtifa dümeni), uçuş kontrolleri, iniş takımı, motor ve gondollar.

| Yük | Tanım |
|---|---|
| **Gerilim (çekme)** | Yapısal elemanı esnetmeye zorlar; bağlar buna karşı koyacak şekilde tasarlanır. |
| **Sıkıştırma (basma)** | Elemanları kısaltma eğilimi; takoz/destek bu yüklere direnir. |
| **Kesme (shear)** | Malzemenin bir yüzünü bitişik yüz üzerinde kaydırma eğilimi; **perçinli bağlantılar** buna göre tasarlanır. |
| **Bükülme (bending)** | Dış kenarda gerilim, iç kenarda sıkıştırma, yapı boyunca kesme. |
| **Burulma (torsion)** | Dış kenarda gerilim, merkezde sıkıştırma, boyunca kesme birleşik yükü. |
| **Burkulma (buckling)** | İnce sac malzemenin uçlarından basma kuvvetine maruz kalınca. |

Pervaneli uçak kalkışta pervaneler sağa dönüyorsa gövde **sola dönmeye çalışır** (burulma); kanatlar düz kalmak için sıkışma-gerilme yüküne girer. Yükler tasarım değerini aşmazsa malzeme eski haline döner; aşarsa **kalıcı deformasyon** olur.
- **Limit load:** Üreticinin belirttiği normal yapısal dayanım. **Ultimate load (son dayanma yükü):** Kısa süreli dayanılabilen yük = **limit yük × 1,5** (güvenlik katsayısı = 1,5). Uzun sürerse yapısal hasar oluşur.
- **Yorgunluk (fatigue):** Çok tekrarlanan yükler sonrası parçanın yorulup kırılması. Bakımlar bu sınır yüklerine göre yapılır. **Aşırı yük altında kalmış uçak sonraki uçuştan önce yetkili teknisyen/bakım mühendisi tarafından muayene edilmelidir.**

### 4.2 Bakım ve uçuşa elverişlilik
**Uçuşa elverişlilik = emniyetli uçuş:** Hava aracı ve parçalarının tipine göre onaylanmış haline uygun olması. Devamlılığı yetkili bakım kuruluşlarıyla sağlanır. **Planlı bakım** (önleyici; tip onayına göre belirlenen aralıklarla) ve **plansız bakım** (düzeltici; uçuşa elverişsizlik durumunda).
| Bakım türü | Açıklama |
|---|---|
| **Hard-time** | Üretici önerisiyle belirli aralıkta (saat/mil), parça sağlam olsa bile **değiştirme**. |
| **On-condition** | Periyodik inceleme/kontrol; ünitenin hizmette kalıp kalamayacağı belirlenir, **arızadan önce** hizmetten çıkarılır. |
| **Damage tolerance** | Yapının katastrofik arıza olmadan belirli zayıflamaya dayanabilmesi; pilot, kabin ekibi, yolcu, bakım ekibi tespit edebilir; **arıza gözlenince** değiştirilir/onarılır. |
Uçuşa elverişlilik şartlarında belirtilen bakım sürelerinden sapma, ilgili bakım tamamlanana kadar **uçuşa elverişlilik sertifikasını geçersiz kılar**; sertifikadaki bakım planıyla çakışmayan işlemler geçerliliği etkilemez.

### 4.3 Gövde ve yapısal elemanlar
Gövde uçağın ana yapısı ve yük taşıyıcı kısmıdır: ekip, yolcu ve yükü taşır, kontrol donanımına yer verir, ana bölümlere gelen kuvvetleri aktarır; basınçlı uçakta iç-dış basınç farkını karşılar. Deniz uçağı gövdesi sudan kalkış-inişe uygun; savaş uçağı gövdesi yalnız kanat, motor ve pilot kabinini toplar (min. sürtünme); büyük yolcu uçağı gövdesi büyük silindir, basınç farkına dayanıklı.

| Gövde tipi | Özellik |
|---|---|
| **İskelet/karkas (truss)** | Hafif çelik boruların **üçgenleme ve kaynakla** bağlanmasıyla kafes kiriş; üzeri alüminyum veya kumaşla kaplanır (kaplama yük taşımaz). Kolay üretim, düşük maliyet, kolay bakım; **köşeli olduğu için sürükleme fazla**. Kabin basınçlandırması olmayan hafif ve basit uçaklarda. |
| **Monokok (monocoque)** | "Tek kabuk": yükleri hafif iç çerçeveler/formerlarla gerilmiş **kaplama** taşır (gerilimli yüzey). Yekpare; küçük hasar bile yapıyı ciddi zayıflatır; bakımı zor ve maliyetli. |
| **Yarı monokok (semi-monocoque)** | **En yaygın** tip. Monokoka ek olarak gövde boyunca **stringer**'lar, çerçeve ve formerlara dik bağlanır; kaplama perçin/kaynakla birleştirilir; birleşik yüklere dayanıklıdır, yük paylaşımı kaplama ile yapılır. |

> Ders metninde: Monokok başlıklı bir slaytta iskelet/karkas özellikleri sayılıyor ve karkas için "kabin basınçlı olmayan hafif uçaklarda" ifadesi monokoka yazılmış; yukarıda karkas ve monokok özellikleri ayrılarak verildi.

- **Bulkhead:** Kuyruk veya motor tarafında gövdeyi bölmeler; formerlar gibidir, kontrol kabloları, hortum ve elektrik kabloları belirli açıklıklardan geçer; **motor tarafındaki bulkhead yangın bariyeri** olarak yangının kokpite/kabine geçmesini engeller.
- **Kapılar:** Yana veya üste açılabilir (menteşe konumuna göre). **Basınçlı uçakta** basınç/hava dengesi için pimlerle gövdeye kilitlenir; basınçsız uçakta normal menteşe-kilit sistemi, uçuşta etrafı görecek cam ve sızdırmazlık için kapı fitilleri vardır.
- **Zemin:** Çapraz kirişler yolcu/kargo tabanını destekler; zemin panelleri sandviç veya **bal peteği** malzemedir, üstte aşınmaya karşı yüzey koruyucu bulunur. Hızlı dekompresyonda döşemenin bozulmasını önlemek için basıncı eşitleyen **zemin havalandırma panelleri** otomatik açılır.
- **Kokpit camları (basınçlı uçak):** İç basınca ve **kuş çarpmasına** dayanmalıdır: güçlendirilmiş cam tabakaları arasında **şeffaf naylon levha**; en dış cam altında elektrik iletken şeffaf kaplama camı **ısıtır** (buz önler, esnemeyle kuş çarpmasının ani yükünü yumuşatır). Ön camın görüş açısı her pilota manevralar için yeterli, engelsiz görüş sağlamalıdır; hafif uçakta ön camlar genelde **plexiglas**.
- **Yolcu camları:** Hava geçirmez conta arasında **iki plastik tabaka** ve metal çerçeve; **iç ve dış panel her biri tek başına kabin basıncına dayanır** (biri bozulursa diğeri tutar, fail-safe); buğu önleyici sistem vardır, **ısıtma yoktur**; üç parçadan oluşur.

### 4.4 Kanatlar ve kuyruk yapısı
- Kanat; kaldırma üretir, yakıt deposu, kanatçık, flap ve bazı uçaklarda motorları taşır. Önü **hücum kenarı**, arkası **firar kenarı**, kamburlu kesit **airfoil**.
- **Spar:** Birden fazla yöndeki yüklere karşı direnci sağlayan temel eleman; **kanadı gövdeye bağlayan ana yük taşıyıcıdır** (yerde ağırlıktan doğan eğilme gerilimini, havada yukarı/geriye kuvvetleri karşılar). Ön ve arka spar arası genelde **yakıt deposudur**. **Rib (kaburga):** Kanat profiline **şekil verir**, gövdeye paralel dizilir. **Stringer:** Kanat boyunca yapısal destek (çıtalar). Spar + rib + stringer + yüzey kaplaması birleşik yüklere dayanır ve rijitliği artırır.
- **Kanat çeşitleri:** Kanat sayısı: **monoplane** (tek), **biplane** (çift), **triplane** (üç). Bağlantı: **cantilever (ankastre, tek noktadan bağlı, dış destek yok)** ve **non-cantilever (destekli)**.
  - **Çift kanat (biplane):** Kafes kiriş üzerine bez kaplı, **200 kt'ı aşmayan** yapılar; alt ve üst kanat kirişlerle bağlıdır, eğilme ve burulma momentine daha az maruz kalır.
  - **Destekli tek kanat (braced monoplane):** Düşük hızlarda; gövdeye tek noktadan bağlanıp dışarıdan çapraz kiriş/dikmelerle desteklenir (eğilme momentine çok dayanıklı).
  - **Cantilever monoplane:** Modern uçakların büyük çoğunluğu; gövdeye tek noktadan bağlanır, bu nokta havada lift ve drag kuvvetlerini, yerde kendi ağırlığını taşır.
- **Kanat şekline göre:** üçgen (delta), geriye ok açılı, öne ok açılı, elips şekilli, değişken açılı, hücum ve firar kenarı geriye açılı vb. **Gövdeye bağlantıya göre:** alttan (low), ortadan (mid), üstten (high) kanat.
- **Kanat açısına göre:** **Dihedral** kanat → stabilite yüksek, manevra (controllability) düşük. **Anhedral (negatif dihedral)** → stabilite düşük, manevra yüksek.

### 4.5 Kontrol yüzeyleri ve kuyruk
| Yüzey | Eksen/Hareket | Kumanda |
|---|---|---|
| İrtifa dümeni (elevator) | **Pitch** | Lövye: **geri çekince elevator yukarı**, burun yukarı; ileri itince aşağı. |
| İstikamet dümeni (rudder) | **Yaw** | Pedallar: sağ pedalın ileri hareketi rudder'ı sağa çevirir, uçak sağa döner. |
| Kanatçık (aileron) | **Roll** | Lövye: sağa çevirince **sağ kanatçık yukarı (spoiler etkisi, lift azalır), sol kanatçık aşağı (flap etkisi, lift artar)** → sağa yatış. |

- **Eksenler:** Boylamsal eksende roll (aileron), yanal (yatay) eksende pitch (elevator), dikey eksende yaw (rudder).
- **Flutter** kontrol yüzeylerinde dengesizlikte oluşan, kontrolsüz osilasyondur (kaza riski); önlemek için **ağırlık dengeleme**. **Kontrol kilitleri** yüzeyleri rüzgârın hasarından korur; **"Remove Before Flight" uyarı bayrağı** asılır.
- **Kuyruk (empennage):** Yatay ve dikey stabilize ile bağlı kumanda yüzeyleri. **Dikey stabilize** sapma hareketlerini azaltır, doğrultu kararlılığı sağlar (firar kenarında rudder); **yatay stabilize** pitch hareketini azaltır, boylamsal kararlılık sağlar (firar kenarında elevator). Bazı uçaklarda elevator yerine **komple hareketli yatay stabilize** (stabilator) bulunur.

## BÖLÜM 5 · Uçak Sistemleri

### 5.1 Hidromekanik sistemler
Hidrolik, büyük/uzak aksamların çalıştırılmasında güç aktarır (ör. ana iniş takımı freni); **sıvıların sıkıştırılamaması** prensibiyle çalışır.

| Avantajlar | Dezavantajlar |
|---|---|
| Küçük hacimle büyük kuvvet/moment; kademesiz hız-kuvvet ayarı; yön çabuk değişir; valflerle aşırı yük korumasi; hassas kontrol; kendini yağlar ve soğutur; uzun ömürlü, ekonomik, titreşimsiz, gürültüsüz | Çevre kirliliği; elemanlar pahalı; yüksek basınç tehlikesi (**3000 psi**); sistem ve yağ **kirlenmesi (contamination)**; sıcağa/soğuğa duyarlı |

- **Hidrostatik basınç:** Kaptaki sıvı basıncı yalnız sıvı yüksekliğine bağlıdır; farklı kaplarda eşit yükseklik = eşit basınç.
- **Pascal kanunu / basınç oluşumu:** Hidrolik basınç **sıvının sıkıştırılmasıyla** oluşur; pompa basınç değil akış sağlar. Ucu açık borudan basınç doğmaz, ucu tıkanınca basınç oluşur. **Kuvvet = basınç × alan.**
- **Açık sistem:** Kullanılmadıkça sıvı depoya döner, motor/pompa sürekli çalışır. **Kapalı sistem:** Pompa yük altında değildir, basınç kontrol vanasına kadar tutulur ve gerektiğinde sisteme verilir.
- **Hidrolik sıvılar:** **Mineral bazlı** (klasik, en eski) ve **sentetik bazlı** (modern; çoğu havayolu uçağında **phosphate ester**, tutuşma ~250 °C). **Farklı tip sıvılar karıştırılmaz** (bileşen hasarı, conta sızıntısı); cilt/göz tahriş eder. İstenen özellikler: nispeten sıkıştırılamaz, iyi yağlama, yüksek kaynama/düşük donma noktası (≈ −70…+80 °C), parlama noktası 100 °C üzeri, yanmaz, kimyasal olarak etkisiz, köpürmez, paslandırmaz.
- **Contalar** sızıntıyı önler (statik conta, salmastra, rondela). **Depo:** Sıvıyı depolar; pompa girişinde pozitif basınç ve yüksek irtifada hava kabarcığı oluşmaması için çoğunlukla **basınçlandırılır** (motor kompresöründen veya kabin basıncından). **Filtreler** emme ve basınç hatlarında (pompanın iki yanında, dönüş hattında); pompayı, contaları ve çalışan yüzeyleri korur.
- **Pompalar:** El, motor, elektrik motoru, basınçlı hava türbini (ATM), hava türbini (**RAT/Hydrat**), hidrolik motorlu **PTU (güç aktarım ünitesi)**; küçük uçaklarda daha basit.

### 5.2 İniş takımı, lastik ve frenler
Toplanabilir iniş takımları performansı artırır, sürtünmeyi azaltır; çoğunlukla **hidrolikle**, bazen pnömatik/elektrikle toplanır; bazı örneklerde hidrolik yalnız toplar, açılma yerçekimi ve hava akımıyla olur. Açıkken dikmeyi **mekanik kilit** sabitler; konum bilgisini kokpite gönderen sensörler ve **yerde iniş takımının toplanmasını engelleyen güvenlik sistemi** vardır.
- **Lastik:** Dubleks tip: iç kısım basınçlı hava (şoku emer, ağırlığı taşır); dış koruyucu kısım iç lastiği korur, şekli sürdürür, frenlemeyi iletir, aşınma yüzeyi sağlar. Bölgeler: **taç, omuz, yanak, topuk (bead)**; sırt deseni genelde **ribbed**. **Sarım sayısı (ply rating) gerçek kat sayısı değil dayanıklılık sırasıdır** (PR16 / "16 PLY RATING" yanakta işaretli); yanakta ebat (inç) ve **hız değeri** da bulunur. Lastik üzerindeki **yeşil veya gri noktalar** basınç dengesi/tığ deliklerinin konumunu gösterir.
- **Bakım:** Aşırı ısı, nem, güneş, yağ/yakıt/hidrolik sıvıdan korunur; temas olursa hemen bezle silinir; park halindeyken sıvı boşaltırken lastiğe koruyucu kılıf takılır.
- **Kayma (creep):** Lastiğin jant üzerinde sürünmesi normaldir, yerine oturunca durmalıdır; fazla ve sürekli kayma patlamaya götürür. Doğru basınç kaymayı azaltır; dudak bitişine **kayma işareti** çizilir. **Limit:** dış çapı 24 inç'e kadar lastiklerde **1 inç**, 24 inçten büyüklerde **1½ inç**; aşılırsa lastik sökülüp supap kontrol edilir.
- **Hasarlar:** Kesik (derinlik kata kadar inmişse değiştir), **meme (bulge/kaplama kırılması → değiştir)**, dişler arasında yabancı madde (ayıkla), aşınma: kanal/bağ çizgilerinde **%25**'e (düz tabanlıda kaplama bezine) aşınmışsa kullanılmaz.
- **Suda kayma (hydroplaning) hızı:** **9√P (kt; P psi)** veya 34√P (P kg/cm²); lastik havası ne kadar yüksekse o kadar yüksek hızda kayma başlar. Diş derinliğinin korunması kaymayı azaltır.
- **Frenler:** Kinetik enerjiyi **ısı enerjisine** çevirir; ısı uçak boyutuyla doğru orantılıdır. Frenleme yangını için en uygun söndürücü **kuru toz**. Çoğu uçakta **hidrolik disk fren** (el freni/pedal → hidrolik basınç kaliper pistonunu itip balataları diske bastırır). Disk **çelik** veya **karbonfiber** (karbon daha hafif, geç ısınır, daha dayanıklı).

### 5.3 Uçuş kontrol sistemleri
Birincil kontroller aileron/elevator/rudder (B4.5). Elevator aşağı akım etkisiyle burnu yukarı/aşağı iter; sağ pedal ileri = rudder sağa.
- **İkincil kontroller (yüksek taşıma araçları):** flap, slot, slat, trim.
  - **Flap:** Düşük hızda daha fazla kaldırma; firar kenarı flapı menteşeyle aşağı inerek kamburluğu artırır; hücum kenarı flapı (Krueger) benzer prensiple. **Kamburluk artınca lift ve drag artar ama lift sürtünmeden fazla artar.**
  - **Slot:** Hücum kenarında **sabit** boşluk; ek kaldırma sağlar, yüksek hızda çok drag yarattığı için **yüksek hızlı uçaklarda tercih edilmez**. **Slat:** Açılıp kapanabilen slot; açılınca **CL'yi ve kritik hücum açısını (critical AOA) artırır**.
  - **Trim:** Pilotun sürekli kuvvet uygulamasını önler; **fletner tab** menteşe hattının arkasında; ağırlık merkezi kayması (çift motorda bir motorun arızası, yakıt dengesizliği) trimle dengelenir; **bazı trim tab'lar uçuşta ayarlanamaz**, yerde mühendis/teknisyen ayarlar.
- **Çalıştırma biçimi:** **Mekanik** (kablo, halat, rot, kol, zincir), **hidrolik** (valfler mekanik kumandalı olabilir), **elektrik** (fly-by-wire; kumanda hareketi sinyal gönderir).
- **Reversible (geri beslemeli):** Manuel/mekanik sistem; pilotun kuvveti yüzeye, yüzeye gelen rüzgâr kuvveti de kumandalara iletilir; **pilot yüzeydeki yükü hisseder**.
- **Irreversible (geri beslemesiz, güçlendirilmiş):** Geniş yüzey veya yüksek hızda yükü azaltmak için hidrolik/elektrik güç; **pilot geri kuvveti hissetmez** (hareket yalnız ileri gider).

### 5.4 Buzlanma ve koruma sistemleri
Buz havanın uçağa ilk çarptığı yerlerde başlar. **Anti-icing:** Buz oluşumunu **başlamadan önleyen**, sürekli ısı/sıvı uygulaması. **De-icing:** Oluşmuş buzu **temizleyen**, ısı/sıvı/mekanik çabanın **aralıklı** uygulanması. Büyük uçaklarda çoklu sistemler kokpit anahtarlarıyla çalıştırılır; **otomatik buz dedektörleri** ekibi uyarır.
| Tip | Çalışma |
|---|---|
| **Pnömatik (boot)** | Kanat hücum kenarında genişleyen/şişen kauçuk kaplama; hava basıncıyla şişince buzu kırar. **Piston motorlu uçaklarda yaygın.** |
| **Termal** | Elektrikli rezistans, yağlı veya havalı ısıtma. **Jet uçaklarda sıcak hava** sistemleri; pitot, ön cam ve bazı sensörlerde **elektrik**. |
| **Sıvı** | Donma noktasını düşüren sıvı püskürtme/kaplama (de-icing). |
- Hafif uçaklarda tavan limiti nedeniyle buzlanma beklenmez ama bazı uçaklarda **ön cam elektrikle ısıtılır** (cam tabakaları arasındaki tel, direnç ısısı). **Pitot tüpü, statik portlar ve AOA sensörleri** buz korumasına dahildir; pitot buzlanırsa hız göstergesi hatalı olur, bu yüzden **pitot ısıtması kalkıştan önce test edilir**. Motor girişinde buzlanma verimi düşürür, **compressor stall** riski doğurur.

### 5.5 Yakıt ve enerji sistemleri
- **İdeal yakıt:** İyi yağlama, yüksek kalori değeri, **düşük viskozite**, uzun depolanabilme ve soğuğa dayanıklılık, korozyon yapmama, iyi yanma, havayla kolay karışma.
- **Yakıt tankları** kanat köklerine yakın; kapaklar basınç belli seviyeyi aşarsa otomatik açılır. **Basınçsız tanklarda yakıtın üzerinde tank kapasitesinin %2'si kadar boşluk** bırakılır; hava **havalandırma borularıyla (vent pipes)** sağlanır, iki depo birbirine boruyla bağlıdır. **Vapour lock:** Yakıt hatlarında oluşan buhar baloncuğunun yakıt akışını tıkaması; yakıtın basınçlandırılarak gönderilmesi ve vent sistemi önler.
- **Pompalar:** Motor tahrikli (engine-driven, motor dönerken çalışır) ve elektrikli (kokpitten seçilir). **Selektör valf** hangi depodan çekileceğini belirler. **Drain** her günün ilk uçuşundan önce, uzun bekleme sonrası ve yakıt alındıktan sonra yapılmalıdır.
- **İkmal öncesi:** Uçağın **grounding**'i, tankerin grounding'i ve uçakla tanker arasında **bonding** yapılır; **single pole** sistemde uçak yer kabul edilip topraklanır (ağırlık tasarrufu). Seviyeye ulaşınca **otomatik kapatma valfi** akışı keser.

### 5.6 Elektrik temelleri
- **Doğru akım (DC):** Tek yönlü akım; sabit gerilim; artı ve eksi terminal. Yoğunluk zamanla değişebilir, yön değişmez.
- **Voltaj (gerilim):** İletkenin iki ucu arasındaki **potansiyel farkı**; elektronları hareket ettirip akımı sağlayan kuvvet.
- **Akım:** Devredeki noktadan geçen elektron/yük miktarı; birim **amper**.
- **Akımın etkileri:** ısıtma, manyetik, kimyasal.
- **Direnç:** Akıma karşı koyma. Etkileyenler: **maddenin cinsi** (gümüş bakırdan iyi iletken), **uzunluk** (uzun kablo = fazla direnç), **kesit alanı** (kalın kablo = az direnç), **sıcaklık** (direnç sıcaklıkla artıyorsa pozitif sıcaklık katsayısı, PTC; sembol α).
- **NTC (negatif sıcaklık katsayısı):** Direnç sıcaklıkla **azalıyorsa** NTC'dir; **termistörler** uçak sistemlerinde sıcaklık ölçümünde kullanılır.
- **Ohm kanunu: V = I × R.** Direnç sabitken gerilim artarsa akım artar (doğru orantı); gerilim sabitken direnç artarsa akım azalır (ters orantı). Geçerli olması için **sıcaklık sabit** olmalıdır.
- **Güç:** İşin yapılma hızıdır, birimi **watt**. **W = V × I = I² × R.**

### 5.7 Elektrik üretimi ve dağıtımı
**DC üretimi:** DC jeneratör (motor döndürür), **alternatör + redresör** (AC üretilir, doğrultularak DC'ye çevrilir; modern uçaklarda yaygın), **batarya/akümülatör** (acil durum). Tasarım güvenilirlik, verimlilik ve güvenlik içindir. **Bozulmalar:** aşırı yük (ısınma), kısa devre (hasar, yangın riski), voltaj düşüklüğü/artışı. **İzleme:** güç yönetim panelleri (voltaj, akım, sistem sağlığı), uyarı/alarm sistemleri, otomatik izleme.

**AC üretimi:** **Jeneratörler** (ana AC kaynağı), **invertörler** (DC → AC), **APU** ve yer destek ekipmanı (yerdeyken/ana motorlar çalışmazken). **Tasarım:** genellikle **üç fazlı**; **frekans 400 Hz** (jeneratör ve ekipman daha hafif/küçük); voltaj genellikle **115/200 VAC**. Bozulmalar: aşırı yük, kısa devre, voltaj ve frekans sapması. İzleme: AC güç panelleri (voltaj, akım, frekans), uyarı sistemleri.

**Dağıtım:**
- **Bara (bus bar):** Enerjiyi birden fazla devreye dağıtan merkezî noktadır; tipik olarak **ana bara (main)**, **acil bara (emergency)** ve bazen **yardımcı bara (auxiliary)**.
- **Ortak topraklama (common ground):** Tüm bileşenler aynı topraklama noktasına bağlanır (genellikle **uçağın metal gövdesi**); potansiyel farkını ve çarpılma riskini azaltır, yıldırım/statik birikimine karşı koruma sağlar.
- **Öncelik:** Güç sınırlıyken veya arızada **uçuş kontrol sistemleri ve aviyonik** en yüksek önceliğe sahiptir.

**Modern uçaklar neden AC tercih eder:** AC jeneratör daha basit ve sağlam; güç/ağırlık oranı daha iyi; **transformatörle** gerilim neredeyse **%100 verimle** yükseltilip düşürülür; gerekli DC voltajı **TRU (transformatör-doğrultucu)** ile kolayca elde edilir; sabit frekanslı üç fazlı AC motorlar DC motordan basit, sağlam, verimli; **komütasyon sorunu yoktur** (özellikle yüksek irtifada güvenilir); yüksek voltajlı AC daha az kablo ağırlığı gerektirir.

**Bileşenler:**
- **Anahtarlar:** Akımı açıp kapatır (manuel, otomatik/sensör kontrollü, basmalı).
- **Devre kesiciler (circuit breaker):** Aşırı akımda devreyi **otomatik keser**; çalışma prensibi **termal, manyetik, hidromanyetik**; kokpitte devre kesici panelinden izlenir.
- **Röle:** Düşük güçlü kontrol sinyaliyle yüksek güçlü devreyi açıp kapatan elektrikli anahtar; **elektromekanik** (fiziksel kontak) ve **katı hal röle (SSR)** (yarı iletken).

### 5.8 Alternatif akım ve devreler
- **AC:** Yönü ve şiddeti zamanla değişen akım; dalga biçimleri: kare, dikdörtgen, üçgen, **sinüsoidal**.
- **Periyot (T):** Bir saykılın süresi, birimi **saniye**. **Frekans (f):** Saniyedeki periyot sayısı, birimi **Hz**; f = 1/T. AC sistemlerde kaynak AC jeneratör (**alternatör**).
- **Seri devre:** Toplam direnç **toplanır** (RT = R1 + R2 + R3); bir direncin bozulması tüm devreyi keser; dirençler ayrı kontrol edilemez. Örnek: 4 + 6 + 10 = 20 Ω, 12 V → I = 12/20 = **0,6 A**.
- **Paralel devre:** Her direnç ayrı kontrol edilir, **her birinde aynı voltaj** vardır, **biri bozulunca diğerleri etkilenmez**; **uçaklarda çoğu bağlantı paralel**. 1/RT = 1/R1 + 1/R2 + 1/R3. Örnek: 1/4 + 1/6 + 1/10 = 31/60 → RT ≈ **1,94 Ω**, I = 12/1,94 ≈ 6 A.
  > Ders metninde: Slaytta paralel örnek "V = 12/1,94" diye yazılmış; I = V/R olduğundan ifade "I = 12/1,94" olmalıdır (sonuç ≈ 6 A).
- **Karışık devre:** Önce paralel dirençler hesaplanır, sonra seri dirençle toplanır.

### 5.9 Statik elektrik ve yıldırım
- Statik elektrik iki yüzeyin teması ve ayrılmasıyla elektron transferinden doğar; uçak–hava **sürtünmesiyle** birikir, aviyonikte **parazit** ve hatalı okuma yapar. Potansiyel farkı yeterince artınca **ani statik deşarj** olur.
- **Statik deşarj cihazları (static wicks):** Kanat uçları, kuyruk gibi arka kısımlarda, yüksek iletkenli malzemeden; birikmiş yükü atmosfere kontrollü boşaltır. Ek koruma: iletken malzemeler, özel kablo yalıtımı.
- **Yıldırım:** Statik elektriğin bir biçimidir; gövde iletken malzemeyle donatılarak yıldırımı güvenle yönlendirip uçak dışına aktarır; elektronik sistemleri ve yolcuları korur.

### 5.10 Güç depolama ve yedek sistemler
- **Bataryalar** acil durumda güç kaynağıdır; ana kaynaklar arızalandığında acil aydınlatma, aviyonik, uçuş enstrümanları ve kritik iletişimi besler. Şarjda elektrik enerjisini **kimyasal enerji** olarak depolar, deşarjda geri verir.
- **Ana (primary) hücre:** İki elektrot + elektrolit; tam yükte potansiyel fark **≈ 1,5 V**; **şarj edilemez** (ör. kuru hücre: karbon çubuk (+), çinko kap (−)). **İkincil (secondary) hücre:** Ters yönlü şarj akımıyla kimyasal enerji yeniden oluşturulur; tekrar şarj edilebilir.
- **Kapasite = akım × süre (Ah).** **Seri** bağlamada toplam voltaj hücre voltajlarının toplamıdır, kapasite tek hücrenin kapasitesidir; **paralel** bağlamada voltaj tek hücrenin voltajı, kapasite toplamdır.
- **Akü tipleri:** **Kurşun-asit**, **nikel-kadmiyum (Ni-Cd)**, **lityum-iyon (Li-ion)**.

### 5.11 İniş takımı (yapı)
- **İşlevleri:** Yerde taksi manevrası, uçağın/pervanenin/kontrol yüzeylerinin yerden yüksekliği, inişte **şok enerjisini emmek**. Sabit veya toplanabilir; ana takım + burun veya kuyruk tekeri.
- **Sabit takım türleri:** **Çelik yaylı** (genellikle ana takım), **kauçuk kordon/lif** darbe emicili, **oleo-pnömatik** (yağlı-havalı) dikme.
- **Burun takımı:** Ana takımdan hafiftir; sıkıştırma-basma yüküne maruz kalır; çekme/itme sırasında **kesme yüküne** dayanmalıdır; yerde serbestçe yönlendirilir. Sabit takımlarda hem oleo dikmeyi korumak hem aerodinamik için **fairing** kullanılabilir.
- **Burun tekeri yönlendirme:** Bağımsız direksiyon (tiller) veya **dümen pedalları** ile. **Shimmy (titreşim):** Eşit olmayan lastik basıncı, esneklik, aşınmış rulmanlar yüzünden oluşur; **titreşim sönümleyiciler (shimmy damper)** eklenir.

## BÖLÜM 6 · Manyetizma ve Direkt Okumalı Pusula

### 6.1 Manyetizma ve Dünya'nın manyetik alanı
- Sulu pusula **manyetik kuzeye** göre yön verir; bazı uçaklarda ana, bazılarında yardımcı göstergedir.
- **Mıknatıs:** Demir, kobalt, nikeli çeker; alüminyum/bakıra etki etmez. Daima **iki kutbu** vardır (bölünse de). Serbest asılınca kuzeyi arayan uç **kuzey (kırmızı) kutup**, güneyi arayan **güney (mavi) kutup**. **Aynı kutuplar iter, farklı kutuplar çeker**; kuvvet mesafenin karesiyle ters orantılıdır. Kutupları birleştiren hat **manyetik eksen**.
- **Akı (kuvvet) çizgileri:** Mıknatısın dışında kuzeyden güneye, içinde güneyden kuzeye akar; **birbirini asla kesmez**. Akı birimi **Weber (Wb)**. **Geçirgenlik (permeability):** Manyetik akının bir malzemeye indüklenme kolaylığı.
- **Madde türleri:** **Ferromanyetik** (demir, kobalt, nikel; kolay mıknatıslanır), **paramanyetik** (alüminyum, platin, manganez; akıyı hafifçe çeker, alan kalkınca özelliği hemen kaybeder), **diyamanyetik** (bakır, bizmut; akıyı hafifçe iter). **Sert demir** (kobalt, tungsten) zor mıknatıslanır, **kalıcı** mıknatıs olur; **yumuşak demir** (saf demir) kolay mıknatıslanır, **geçici** mıknatıstır.
- **Mıknatıslama yöntemleri:** Mıknatısı demir üzerinde **tek yönde sürtmek**; demiri alanın kuvvet çizgisi boyunca **çekiçlemek/titreştirmek**; etrafına sarılı bobinden **DC** geçirmek (röle ve selenoidin temeli).
- **Mıknatıslığı gidermek:** Alana **dik** çekiçlemek/titreştirmek, yaklaşık **900 °C**'ye ısıtmak, bobine **AC** uygulamak (yön sürekli değişir, mıknatıslanma olmaz).

### 6.2 Dünyasal manyetizma
- Dünya, merkezinden geçen varsayımsal bir mıknatıs bar gibidir; ekseni coğrafik eksenden **ayrıdır**. Barın **güney kutbu coğrafik kuzeyde, kuzey kutbu coğrafik güneydedir**. Akı çizgileri kutuplara yaklaştıkça eğilir, kutuplarda yüzeye 90°; çizgilerin yüzeye paralel (0°) olduğu yere **manyetik ekvator** denir.
- **Manyetik meridyen:** Dünya manyetik alanının yatay bileşeninin yönü; sulu pusula bunu izler. Pusula manyetik kuzeyi bulur.
- **Varyasyon (variation):** Coğrafik (gerçek) meridyenle manyetik meridyen arasındaki açı; **MN gerçek kuzeyin batısındaysa W, doğusundaysa E**. Değerler 0°–180° aralığındadır. Eş varyasyon çizgileri **izogonal**; sıfır olanı **agonal**. **Varyasyonun yönü uçuş başına değil**, uçağın bulunduğu yerde gerçek kuzeye bakıp manyetik meridyenin hangi tarafta kaldığına göre belirlenir.
- **Baş hesabı:** **Varyasyon batılıysa eklenir, doğuluysa çıkarılır** (TH → MH). Örnek: 286°T, 4°W → 290°M; 090°T, 6°E → 084°M. Kural: **"West: manyetik en büyük; East: manyetik en küçük."** (Varyasyon batı → manyetik > gerçek.)
- **Manyetik batma (dip/inclination):** Akı çizgileri yatay (H) ve dikey (Z) bileşene ayrılır; yatay bileşen ile toplam akı çizgisi arasındaki açıdır. **Yalnız manyetik ekvatorda yatay** (0°). Kutuplara gidildikçe batma artar, yatay bileşen azalır; **H bileşeni ≈ 6 µT veya altındaysa** sulu pusula kuzeyi bulamaz ve güvenilmezdir.

### 6.3 Uçağın manyetik alanı ve sapma
- **Sapma/deviasyon (deviation):** Uçaktaki demir metaller, mıknatıslanmış parçalar ve akım taşıyan iletkenler pusulayı manyetik meridyenden saptırır; **manyetik meridyen ile pusulanın gösterdiği yön arasındaki açıdır**. **Şiddeti uçuş başına bağlıdır.** Pusula ibresi doğuya sapmışsa **E (sağ)**, batıya sapmışsa **W (sol)**.
- **Zincir:** Harita gerçek kuzeye göre → TH; pusula manyetik kuzeye → MH; ek olarak deviasyonla **Compass Heading (CH)**. **T →(± varyasyon)→ M →(± deviasyon)→ C.** Örnek: TH 115°, varyasyon 4°E → MH 111°; deviasyon 10°W → CH 121°.
- **Uçak mıknatıslığı:** **Sert demir** malzemeler (kalıcı; imalat/bakımdaki çekiçleme, uzun süre aynı başta durma vb. sebep olur); **yumuşak demir** malzemeler (geçici; dünya alanı ve uçaktaki elektromanyetik alanlarca indüklenir; manyetik enlem, uçuş başı ve coğrafi konuma bağlıdır).
- **Pusula kalibrasyonu (compass swing):** Etkilerden uzak, işaretli bir meydanda **30°'lik aralıklarla** başlar, pusula okumaları ile referans değerler karşılaştırılır. Sert demir sapmaları üç eksende: boylamsal **P**, yanal **Q**, dikey **R**; yumuşak demir etkileri yatay **H** ve dikey **Z** düzlemde. Sonuç **kalibrasyon kartına** ("Steer for…", "calibrated with radio on") yazılır.
- **Compass swing gerektiren durumlar:** Uzun süreli yoğun statik ortamda uçuş veya **yıldırım çarpması**; önemli bakım; yeni uçak; periyodik bakım zamanı; uçakta mıknatıslı malzeme değişimi; pusula doğruluğundan şüphe; ciddi şok; aynı başta uzun süre park; demir malzeme taşınması; manyetik enlemin çok değişmesi.

### 6.4 Direkt okumalı manyetik pusula
- İki temel tip: **dikey kart** ve **grid halka**; derste anlatılan **E tipi** pusula.
- **E tipi bileşenleri:** Dairevi mıknatıs, pusula gülü (kart), **denge noktası iğne** (iridyum uç), **sıcaklık telafi edici körük** (sıvı genleşmesi), plastik kase, **B ve C katsayısını düzelten mekanik ayar vidası ve dişlisi**, cam üzerinde **lubber line**.
- **Yataylık (horizontality):** Mıknatıs **sarkaç yapı ve kayan denge noktasıyla** yatay tutulur; dengeleme **en fazla 20°** batma açısına kadar yeter. **~70° manyetik enlemden sonra** pusula güvensizdir.
- **Duyarlılık (sensitivity):** Mıknatısın yön için izlediği toplam alanın **H bileşenini** algılayabilme özelliği; kutuplara doğru azalır; kutup kuvveti güçlendirilerek artırılabilir.
- **Periyodiklik (aperiodicity):** Dönüşten sonra pusulanın **manyetik kuzeyi ne kadar hızlı yeniden yakaladığı** (osilasyonun azlığı). Yöntemler: kaseye **sönümleyici sıvı** koymak; uzun mıknatıs yerine **kısa/yuvarlak veya yan yana kısa mıknatıslar**; sarkacı kısa tutmak.

### 6.5 Manyetik pusula hataları
Sarkaç yapı (yataylık için) ve sıvı girdabı; denge noktası (pivot) yüksek enlemlerde bulunulan yarımküredeki kutba doğru kayar. Sonuç: **doğuya/batıya** hızlanma-yavaşlamada ve **dönüşlerde** hata.
- **Hızlanma/yavaşlama hatası (kuzey yarımküre):** Yalnız **90° (doğu) ve 270° (batı)** başlarda olur. **Hızlanınca pusula kuzeye doğru dönüyormuş gibi** gösterir, **yavaşlayınca güneye doğru** ("ANDS": Accelerate North, Decelerate South). Örnek: 270°M'de hızlanma → okuma artar (sağa dönüş gibi); yavaşlama → okuma azalır. 090°M'de hızlanma → okuma azalır; yavaşlama → artar. Atalet etkisi **C.G**'den, hızlanma kuvveti **denge noktasından** etkir, Z bileşeni etrafında moment oluşur. **Kuzey ve güney başlarda** C.G ile denge noktası aynı eksen üzerinde olduğundan **hata yoktur**.
- **Dönüş hatası:** **Kuzeye ve güneye dönüşlerde en büyük**, **doğuya ve batıya dönüşlerde yoktur** (merkezkaç kuvveti de C.G'den, merkezcil kuvvet denge noktasından etkir).
  - **Kuzeyden dönüşler (sağa/sola):** Uçak dönüş hızı pusuladan fazla; pusula **gecikmeli (undershoot)** gösterir → hedef başa **erken** çıkılmalıdır.
  - **Güneyden dönüşler:** Pusula **erken (overshoot)** gösterir → **geç** çıkılmalıdır.
  - Kural: **UNOS — Undershoot North, Overshoot South.** Hata miktarı enlemle artar.

## BÖLÜM 7 · Cayroskopik (Jiroskopik) Aletler

### 7.1 Temel prensipler
- Cayro (jiroskop) rotorunun dönüşünden doğan **atalet (eylemsizlik)** özelliğinden yararlanan aletler: **dönüş göstergesi (rate of turn)**, **suni ufuk (AI)**, **istikamet cayrosu (DGI)**, **dönüş koordinatörü**.
- **Hareket:** Doğrusal, dairesel (cayro rotoru), eğrisel (atılan top mermisi). **Momentum:** Çizgisel **P = m·V**; **açısal momentum L = I·ω** (I = m·r², eylemsizlik momenti); vektörel, yönü dönüş düzlemine diktir.
- **Newton:** Net kuvvet yoksa duran durur, sabit hızlı giden devam eder (atalet); **F = dP/dt = m·a**.
- **Cayroskopik hadise:** Dönen cisim açısal momentuma ve ataletine sahiptir, bu ona **denge** verir (topaç dönerken devrilmez).
- **Cayro özellikleri:** **Sabitlik (rigidity)** ve **devinim (precession, uygulanan kuvvetin dönüş yönünde 90° sonra etki etmesi)**. Sabitlik; rotor kütlesi, dönüş hızı ve kütlenin yarıçapa dağılımıyla artar.

### 7.2 Cayro çeşitleri ve tahrik
- **Uzay cayrosu (free-space gyro):** Üç düzlemde serbest, hiçbir dış kontrole bağlı değil; ekseni uzayda korur; uzay mekiği ve **INS**.
- **Bağlı cayrolar (tied gyro):** Ekseni başka bir unsurla muhafaza edilir; **dünya cayrosu (earth gyro)** — yerçekimini kontrol kuvveti sayar (dikey cayro). **Oran cayrosu (rate gyro):** **Tek derece özgürlük**, tek yalpa halkası, devinim **yayla** kısıtlanır, düzleminde en fazla 90° döner. Devinim **sıvı** ile kısıtlanırsa **oran entegreli cayro (rate integrating gyro)**; INS'te kullanılır, servo motor sinyali bilgisayarda zamana göre integre edilir.
- **Hava (pnömatik) tahrik:** Motorla çalışan **vakum pompası** emme basıncı oluşturur; hava filtreden geçip jetle rotor üzerinden akar; emme basıncı limit içinde olmalıdır (yetersizse rotor yavaş döner, gösterim bozulur). Durum göstergesi için yaklaşık **4 inç cıva**.
- **Elektrik tahrik:** Fırçasız **asenkron AC motor**; statora üç fazlı AC → dönen manyetik alan; rotor hızı alan hızından yaklaşık **%8 düşük**. Daha yüksek devir (**~22 500 RPM**) → daha yüksek sabitlik.

### 7.3 Cayro sapması (wander)
- **Gerçek sapma (real wander):** İmalat hatası, aşınma, dengesiz rotor/gimbal, rulman sürtünmesi; **drift ve topple** doğurabilir. **Göreceli sapma (apparent wander):** Dünya'nın dönüşü (**earth rate**) ve cayronun taşınması; rotor uzayda ekseni korur, gözlemciye göre değişir.
- **Sürüklenme (drift):** Yatay eksenli cayro ekseninin **yatay düzlemde** (azimutta) sapması. **Devrilme (topple):** **Dikey düzlemde** sapma. **İstikamet cayrosu** (yatay eksenli) ikisine de maruz kalır; **suni ufuk** (dikey eksenli) yalnız **devrilme**.
- **Dünya dönüşü:** 360°/24 sa = **15°/saat**.
  - Meridyene paralel eksen: **Drift = 15° × sin(enlem) / saat** → ekvatorda 0°, kutupta 15°/saat (6 saatte 90°). Kuzey yarımkürede dünya batıdan doğuya döndüğünden uçak başı **küçülür** (görünür).
  - Ekvatora paralel (yatay) eksen: **Topple = 15° × cos(enlem) / saat** → ekvatorda 15°, kutuplarda 0°.
  - **Taşıma sapması (transport wander):** Ekvatorda meridyene paralel cayro kuzey kutbuna taşınırsa ekseni yatayken dikeye döner; sapma uçağın yer değiştirmesinden kaynaklanır.

### 7.4 Dönüş göstergesi ve kayış göstergesi
- **Dönüş göstergesi:** Ibre ile dönüş **yönü ve oranı**. Yapı: elektrik/hava tahrikli rotor, **tek derece özgürlük veren gimbal**, kısıtlayıcı **yaylar**, gösterge, **kırmızı ihbar bayrağı**. Rotor ekseni **yanal eksene paralel (yatay eksenli)**; dikey (yaw) eksendeki dönüşü algılar; gimbal ve yaylar kuvveti **orantılı** gösterir. Düz uçuşta ibre ortadadır.
- **Rate one:** Saniyede **3°** = tam tur **2 dakika** (360/3 = 120 sn); doğru gösterim **yalnız koordineli dönüşte**.
- **Hataları:** Gerçek sapma azdır; göreceli sapma hatası yaylarla bertaraf edilir. Hava tahrikli alette **yetersiz vakum → düşük dönüş oranı** okuması, **fazla vakum → fazla oran**. Yerde taksi sırasında sağa dönüşte ibre sağa, top (ball) sola gitmeli, solda tersi; dönüş yokken ibre ortada olmalıdır.
- **Kayış göstergesi (slip/skid):** Dönüşün **dengeli olup olmadığını** gösterir; sıvı dolu fosforlu ark cam tüp içinde **sarkaç top**, ortada iki çizgi; sıvı motor titreşimini sönümler. Top **göreceli dikeyi** (yerçekimi + merkezkaç bileşkesi) gösterir.
  - **Skid (savruluş):** Gerekenden **az yatışla** dönüşte merkezkaç baskın, top dönüşün **dışına** gider.
  - **Slip (kayış):** **Fazla yatışta** top dönüşün **içine** gider. Sürat arttıkça uygun yatış açısı artar: **Yatış ≈ (TAS/10) + 7** (150 kt → 22°). Yerde top iki çizgi arasında olmalı.
- **Dönüş koordinatörü:** Dönüş oranına ek olarak **yatış oranını** da gösterir, küçük uçaklarda yaygın; cayro **uzunluk eksenine 30° açıyla** yerleştirilmiştir, hem yaw hem roll hareketini algılar; ibre yerine **uçak sembolü** vardır, kayış göstergesi üzerindedir; **yunuslama (pitch) algılamaz**; elektrikle ≈6000 RPM; 3°/sn ile 2 dakikada tam tur.

### 7.5 Durum göstergesi (suni ufuk) ve hataları
- Pitch ve roll durumunu gösterir; **dikey eksenli rotor, iki gimbal (iki derece özgürlük), yer cayrosu**. Hava tahrikli: ≈**15 000 RPM**, ≈4 inç Hg emme; elektrikli: **≈22 500 RPM**.
- **Dış gimbal** uzunluk ekseninde, yaklaşık **±110°** yatışı; **iç gimbal** yanal eksende **yaklaşık ±55°** yunuslama; iç gimbalın **rehber pimi** yatay bar koluna iletir. **Sabit uçak sembolü** camın arkasında, hareket eden **resim plaka** gökyüzü/yeri gösterir; **hızlı dikleştirme (fast erection) düğmesi** vardır. Alet cayro sabit kalır, **uçak cayronun etrafında döner**.
- **Dikleştirme (erection) sistemi (hava tahrikli):** **Dört sarkaç kanatçık/yarık**; cayro dikken eşit hava çıkar, devrilince biri kapanıp biri açılır, oluşan reaksiyon **devinim kuralıyla 90° sonra** düzeltici tork verir.
- **İvmelenme (kalkış) hataları (hava tahrikli):** Düzeltme sistemi göreceli dikeye göre dikleştirir. **Kalkışta yunuslama hatası:** olmayan bir **burun yukarı** izlenimi (yanlış climb göstergesi). **Kalkışta yatış hatası:** ağırlık merkezi denge noktasının altında olduğundan devinimle **yatış hatası** (örnekte saat yönünün tersi dönen rotor için **sağa yatış**). Hata kalkıştaki ivmelenmede oluşur.
- **Dönüş hataları:** Dönüşte merkezkaç kuvveti kanatçık sistemini yanlış açar/kapar → **yunuslama ve yatış hataları**; hata dönüş oranı, hız ve yataylığa bağlıdır; **360°'lik tam dönüş sonunda hatalar normale döner**, en büyük yaklaşık 180°–270° civarı.
- **Elektrikli durum göstergesi:** Rotor ~22 000–22 500 RPM, sabitlik çok yüksek; dikleştirme **cıvalı seviyeleme sensörleri + tork motorları** ile (sensör sinyali tork motoruna, devinimle 90° sonra düzeltir). **Kapama anahtarları** ivmelenme (**≈0,18 G**) ve **10°'den fazla yatışta** sensör girdisini keser; ağırlık merkezi denge noktasına yakındır → ivmelenme hatası az. **Hızlı dikleştirme:** normal düzeltme **dakikada ≈4°**, hızlı düzeltme **≈120°/dk** (20 V → 115 V); aşırı ısınma nedeniyle **15 saniyeden fazla** kullanılmaz.

### 7.6 Dikey cayro ünitesi ve istikamet cayrosu
- **Dikey (uzak) cayro ünitesi:** Aviyonik bölgesinde; durum bilgisini **senkro** ile aletlere gönderir; platform üç oran cayrosuyla yatay tutulur. **Avantaj:** göreceli hata yok, manuel düzeltme gerekmez, güvenilir, dijital açısal bilgi otopilot/FMS'e gider. **Dezavantaj:** **elektriğe bağımlı**.
- **İstikamet cayrosu (DGI):** Sabitlikten yararlanarak **kararlı istikamet referansı** verir; **manyetik değildir**, uçak manyetizmasından ve dünya alanından etkilenmez. Yatay eksenli, **iki derece özgürlüklü**; rotor ekseni dış gimbal ekseniyle 90°. **Devrilme** hava tahrikli düzeltme sistemiyle ya da **caging** (çekerek) giderilir; **sürüklenme (drift) otomatik düzeltilmez**, **istikamet ayar düğmesiyle** elle düzeltilir; uçuşta **yaklaşık 30 dakikada bir sulu pusula ile kontrol edilip ayarlanır**.
- **Göstergesi:** Dikey gösterimli pusula gülü veya yatay gösterimli; **üç rakamlı baş iki rakamla** gösterilir (330° → 33), kısa çizgi 5°, uzun çizgi 10°, her 30°'de rakam (N, 3, 6, E, 12, 15, S, 21, 24, W, 30, 33).
- **Hava tahrikli DGI düzeltmesi:** Jet hava dış gimbaldeki yarıklı rotoru döndürür; yatışta jet iki bileşene ayrılır, devinimle **kaba ayar**; **düzeltme kaması** ise rotor tam dik değilse eşitsiz reaksiyonla **ince ayar** yapar.

### 7.7 DGI hataları ve toplam sürükleme
- DGI'da **gerçek (imalat, aşınma)** ve **göreceli (dünya dönüşü, taşıma)** sapma vardır; eksen **drift** veya **topple** yapar. **Kuzey yarımkürede göreceli sapma istikameti azaltır** (mevcut istikametten çıkarılır); güney yarımkürede tersi.
- **Enlem somunu (latitude nut, LN):** İç gimbala takılır; dünyanın dönüşünden doğan göreceli sapmayı, **ters yönde yapay (gerçek) bir sapma** oluşturarak dengeler; belirli bir enlem için ayarlanır (**15° × sin(enlem)/saat**). 
- **Taşıma sapması (transport wander):** Dünya batıdan doğuya döndüğünden **doğuya uçuşta** GS dünya dönüşüne **eklenir**, **batıya uçuşta çıkarılır**; büyüklüğü **GS/60 × tan(enlem)** (°/saat) → **sürat ve enleme bağlıdır**.
- **Toplam sürükleme: TD = RW + ER + LN + TW** (gerçek sapma + dünya dönüşü + enlem somunu + taşıma). Kuzey yarımkürede ER negatif, LN pozitif (güney yarımkürede tersi).
  - Örnek (slayt): 130 kt GS, 080° baş, 30° enlem, enlem somunu 45°'ye ayarlı, ideal cayro, 1,5 saat: **ER = −1,5 × 15 × sin30° = −11,25°**, **LN = +15 × sin45° × 1,5 ≈ +15,9°** (slaytta saatlik değer 10,6° verilmiş), TW ayrıca eklenir.
  > Ders metninde: Slaytta LN için yalnız saatlik değer (+10,6°) yazılmış, 1,5 saatle çarpılmamış ve örnek sonucu tamamlanmamış; hesap sürükleme formülünün her terimini süreyle çarpmayı gerektirir.

## BÖLÜM 8 · İletişim, Uyarı ve Yakınlık Sistemleri

### 8.1 Haberleşme sistemleri
| Sistem | Özellik |
|---|---|
| **HF (3–30 MHz)** | **Yer dalgası** (dünyanın eğriliğini izler) ve **gök dalgası** (**iyonosferden yansır**); **görüş hattı gerekmez**, engele takılmaz, çok düşük güç; **kutup rotalarında** VHF/SATCOM kapsama dışındayken kullanılır. Kalite **kutup ışıkları ve güneş patlamalarına, mevsime, günün saatine (şafak/alacakaranlık)** bağlıdır. |
| **VHF (30–300 MHz)** | **Görüş hattı gerekir**; iyonosferden yansımaz, dünyanın eğriliğini izlemez, engeli geçemez; menzil alıcı ve vericinin **irtifasına** bağlıdır. **108,0–117,95 MHz seyrüsefer, 117,975–137,0 MHz sesli iletişim.** |
| **SATCOM** | Uydu **röle** görevi yapar; yüksek sinyal kalitesi, ses ve veri, uzun mesafe, yer engellerinden etkilenmez. Uydular **ekvator üzerinde yerleşik (jeostasyoner)**, dünyayla aynı açısal hızda; **kutup bölgelerinde** görüş dışında kalır, kapsama alanı dışında kullanılamaz; VHF gibi görüş hattı gerekir. |
- Hafif ve küçük uçaklarda bile **yedekli VHF** iletişim sistemi bulunmalıdır.

### 8.2 Uçuş ihbar ve uyarı sistemleri
- **Amaç:** Normal uçuş şartları dışındaki durumları bildirip **durumsal farkındalığı** artırmak: motor/sistem arızaları, aerodinamik limit aşımları (**irtifa alarmı, aşırı hız, stol**), harici tehlikeler (**GPWS** yere yaklaşma, **TCAS** çarpışmadan kaçınma).
- **Alarm (alert):** görsel **veya** işitsel; **İhbar (warning):** görsel **ve** işitsel birlikte.
- **Sunum:** **Görsel** (ışık, bayrak, master caution/warning lambaları), **işitsel** (sentetik insan sesi: "fire", "climb", "traffic"…; ya da üretilmiş ses), **duyusal** (kumanda sarsıntısı = **stick shaker**, lövye bastırma = **stick pusher**).
- **Renkler:** **Kırmızı = ihbar (warning)**, **sarı/kehribar = dikkat (caution)** ve **tavsiye (advisory)**.
- **Stol ihbar sistemi:** Stol, hücum açısı (AOA) kritik değeri aşınca taşıma kaybıdır. **Düz kanatta kritik AOA ≈ 12°–18°**, **oklu veya delta kanatta 30°–40°**. Küçük uçakta hücum kenarında **menteşeli kanatçıklı sensör** (AOA artınca sapar → ses ve lamba); büyük/performanslı uçaklarda **AOA (alfa) sensörü**. İhbar stol durumu geçene kadar sürmelidir.

## BÖLÜM 9 · Göstergeler, Entegre Cihazlar, Elektronik Ekranlar

- **Gösterge türleri:** İbreli saat tipi, **CRT**, **LCD**, **LED**, **cam kokpit (glass cockpit)**.
- **Ölçüm aralığı:** İyi ölçeklendirilmeli, uçak limitlerine uygun olmalı (limit sürat kadranda belirtilir). Çok geniş aralık için **ikinci ibre**; doğrusal olmayan ölçek, belirli bölgede hassasiyeti artırır.
- **Ergonomi:** İnsan-makine ilişkisi; aletler okunabilir, hızlı ulaşılır yerde olmalıdır. Uçuş aletleri **"temel altı" (basic six)** ve **"temel T"** düzeninde, pilotun hemen göreceği yere yerleşir; cam kokpitte de aynı mantık kullanılır.
- **Okunabilirlik:** İndeks ve ölçek pilot göz hattında olmalıdır, aksi hâlde **paralaks** okuma hatası olur (sulu pusulada lubber line). Çok ibreli **altimetre** algı sorunu yaratabilir.
- **İçten dışa (inside-out):** Uçak figürü sabit, ufuk/resim plaka hareketli (durum cayrosu) → **algıyı artırır**; **dıştan içe (outside-in):** uçak figürü hareketli, ufuk sabit → algıyı düşürür.
- **Renkler:** Klasik: **yeşil normal**, **sarı/amber dikkat**, **kırmızı ihbar/emniyetsiz**. Gelişmiş uçaklarda ek olarak **beyaz (mevcut durum)** ve **mavi (geçici durum)**.
- **Mekanik göstergeler:** Dişli, kol ve bağlantılarla ibre (altimetre, VSI, hız göstergesi). **Elektrik göstergeler:** hareketli bobin ve oran ölçer (aslında **voltmetre**), **senkro/selsyn**, **servo** (servo altimetre basıncı elektrik sinyale çevirir).
- **Elektronik göstergeler:** **7 segmentli** (yalnız rakam, her segmentte LED), **5×7 nokta matriks** (harf, rakam), **CRT** (elektron tabancası, vakum tüpü, floresan ekran), **LCD** (nematik sıvı kristal, voltajla yapısı değişir, oda sıcaklığında sıvı).
- **Dijital:** **EFIS** / glass cockpit; **PFD** (irtifa, hız, yön, tırmanma oranı: temel uçuş bilgisi), **MFD** (seyrüsefer, motor parametreleri, sistem durumu). Hibrit (analog + dijital) yaygın. Arızada gösterge **"flag"** veya **"warning"** verir; renk kodu, sesli uyarı ve simgeler dikkati kritik bilgiye yönlendirir.
