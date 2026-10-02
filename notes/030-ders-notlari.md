# 030 · Uçuş Performansı ve Planlama — ders notları

Kaynak: SHGM KDM platformu, *Uçak Uçuş Performansı ve Planlama 1* (U 01 E UO 075). Bölüm sonu soruları `data/030_ders_notu_sorulari.json` dosyasındadır.

## BÖLÜM 1 · Ağırlık ve Denge

### 1.1 Temel kavramlar
- **Ağırlık merkezi (CG):** Uçağın dengede durduğu noktadır; yük dağılımıyla değişir. **CG limitleri**, uçağın emniyetle uçabileceği ön ve arka sınırlardır. Kütle ve CG üretici tarafından hesaplanır, onaylı uçuş/işletim el kitabındaki prosedürlere göre belgelenir; pilot verilen **ağırlık sınırlamalarına (mass limitations)** uymakla yükümlüdür.
- **Boş ağırlık (BEM, Basic Empty Mass):** İlk tartımda bulunan tam boş ağırlık. İçine girenler: **kullanılamayan yakıt, motor ve yardımcı ünitelerin yağları, hidrolik sıvı, yangın söndürücüler, acil oksijen sistemi, elektronik cihazlar**.
- **Değişken yük (VL, Variable Load):** Uçuş ekibi (pilot + kabin) ve bagajları, yolcu ikramları ve sökülebilir servis ekipmanı (uçuş uzunluğuna göre değişir), içme suyu ve temizlik malzemeleri, lavabo kimyasalları.
- **Trafik yükü (TL, Traffic Load):** Yolcu, bagaj, kargo ve ticari olmayan yükün toplamı. **Payload (faydalı yük):** Trafik yükünün **para kazandıran** kısmı.
- **Kütle zinciri:** BEM (+ özel/isteğe bağlı ekipman, değişken yük, mürettebat vb.; **yakıt dahil değil**) = **DOM**; DOM + trafik yükü = **ZFM** (sıfır yakıt kütlesi); ZFM + kalkış yakıtı = **TOM** (kalkış kütlesi); TOM − yolculuk yakıtı = **LM** (iniş kütlesi). **Rampa (blok) kütlesi** = tanklardaki tüm yakıt dahil; taksi yakıtı yakıldıktan sonra TOM'a düşer. İlgili kütle tanımı için **maksimum (sertifikalı) yapısal kütle sınırı** vardır; uçak **maksimum yük faktörü +2,5 g** için hesaplanmıştır. Tek kütle değişikliği nedeniyle fark her zaman **yakıt tüketimidir**.

### 1.2 Yakıt türleri ve hesabı
| Yakıt | Tanım |
|---|---|
| **Start/Run-up/Taxi fuel** | Kalkıştan önce kullanılan: APU, motor çalıştırma, taksi. |
| **Trip fuel** | Kalkıştaki fren bırakmadan varışta teker koymaya kadar gereken yakıt (kalkış, tırmanış, seyir, alçalma, yaklaşma, iniş). |
| **Contingency fuel** | Rüzgâr, rota değişikliği, ATC kısıtlaması gibi sapmalar için; **trip yakıtının %5'i** veya varış meydanı üzerinde **1500 ft (AGL+1500) 5 dk bekleme** yakıtından **hangisi büyükse**. |
| **Alternate fuel** | Varışta pas geçme noktasından yedek meydanda inişe kadar; iki yedek varsa **daha fazla yakıt gerektiren** alternatife göre. |
| **Final reserve (holding)** | Yedek meydandaki beklenmedik olaylar için; **gaz türbinli 30 dk, pistonlu 45 dk** bekleme (AGL+1500 ft). |
| **Additional fuel** | Şirket gereksinimleri için (alternatifsiz uzak bölge, ETOPS); fiyat farkı varsa ekonomik nedenle de eklenebilir. |
| **Extra fuel** | Kaptan ve/veya dispatcher'ın **takdirine** bağlı. |
| **Ramp/Block fuel** | Uçağa konan toplam yakıt. |
- **Rampa yakıtı = taksi + trip + contingency + alternate + final reserve + additional + extra.**
- **Ramp − Taxi = Take-off fuel; Take-off + Taxi = Ramp; Take-off − Trip = Landing fuel; Landing + Trip = Take-off.**

### 1.3 Ağırlık merkezi ve referans noktası (datum)
- **Datum:** İmalatçının belirlediği, tüm CG ölçümlerinin ve CG limitlerinin dayandığı sabit nokta.
- **Kol (arm):** Bir kütlenin ağırlık merkezinin **datuma uzaklığı**; kol uzadıkça moment artar. **Datumun önündeki kol negatif, arkasındaki pozitiftir.**
- **Moment = kütle × kol** (M × d). **Toplam moment** = Σ(Mᵢ × dᵢ); **CG = toplam moment / toplam kütle**. Terazi mantığı: iki tarafın kütle × kol çarpımları eşitse denge sağlanır.
- **Yük kaydırma/ekleme/çıkarma:** m = taşınan yük, M = uçağın toplam kütlesi, d = CG'nin kayma mesafesi, D = m'nin kaydırıldığı mesafe → **d = m × D / M** (kaydırmada).
- **CG'yi değiştiren etkenler (uzunlamasına):** yakıt tüketimi, flap açma/kapama, iniş takımı açma/kapama, kargo hareketi, yolcu ve ekip hareketi.
- **CG ön limitin önündeyse (burun ağır):** **Stabilite artar, kumanda kontrolü azalır.** Kalkışta rotasyon için daha fazla elevator sapması gerekir (geç kalkış); **trim drag artar**, aynı sürat için daha fazla güç/yakıt → **menzil ve havada kalış süresi azalır**; tailplane downforce arttığından efektif ağırlık artar → **stall sürati artar**; son yaklaşmada burun düşmesini önlemek için sürat yüksek tutulur → iniş sürati ve mesafesi artar; tırmanma açısı ve oranı düşer.
- **CG arka limitin arkasındaysa (burun hafif):** **Stabilite azalır, kumanda kontrolü artar.** Daha az elevator sapması, **trim drag azalır**, güç/yakıt azalır → **menzil ve havada kalış süresi artar**; tailplane downforce azalır; yaklaşma ve iniş sürati düşer, iniş mesafesi azalır; **rudder kolu kısaldığı için rudder verimi düşer, spinden çıkış zorlaşır**.

## BÖLÜM 2 · Performans

### 2.1 Basınç ve atmosfer
- **Basınç = kuvvet / alan**; birim N/m² = **Pascal (Pa)**; 1 bar = 100 000 Pa, 1 psi = 6894,8 Pa. İki tür: **statik** ve **dinamik**; toplam basınç = statik + dinamik.
- **Statik basınç:** Atmosferin nesneye **her yönden eşit** uyguladığı basınç; irtifa arttıkça üstteki hava kütlesi azaldığından düşer. **Dinamik basınç:** Nesne ile hava arasında **göreceli hareket** olunca, yalnızca hareket yönünde oluşur; **hız ve yoğunlukla artar**. **Toplam basınç:** Alçak hızda (subsonic) gövde etrafında sabittir; hız artarsa dinamik basınç artar, **statik basınç azalır** (kanat üstünde olan budur, lift buradan doğar).
- **ISA (ICAO Doc 7488):** Atmosfer **tamamen kuru**; deniz seviyesi basıncı **1013,25 hPa (29,92 inHg)**; deniz seviyesi sıcaklığı **15 °C**; **tropopoz 36 000 ft**; sıcaklık düşüş oranı **1,98 °C ≈ 2 °C / 1000 ft**; deniz seviyesinde yoğunluk **1,2250 kg/m³**; tropopozda sıcaklık **−56,5 °C**. **ISA sapması:** gerçek dış sıcaklık ile ISA sıcaklığı arasındaki fark (+/−), performans hesaplarında kullanılır.
  > Ders metninde: ISA sapması "15 − (1,98 × FL/1000)" olarak yazılmış; bu formül ISA **sıcaklığını** verir, sapma = OAT − ISA sıcaklığıdır.
- **Yoğunluk irtifası (DA):** Standart olmayan sıcaklık için basınç irtifasının düzeltilmiş hâli; atmosfer yoğunluğunun ISA'ya oranla irtifa cinsinden ifadesi. Yoğunluğu basınç, sıcaklık ve **nem** belirler. **Yoğunluk azalırsa:** motor gücü/itme azalır, hızlanma azalır, **kalkış mesafesi uzar**; belirli bir IAS için **TAS artar** (ör. 120 kt IAS ≈ 130 kt TAS) → daha uzun mesafe; tırmanma açısı ve oranı düşer, screen height'a ulaşmak daha uzun yatay mesafe ister. Performans yoğunluk irtifasıyla **ters orantılıdır**; sıcak ve nemli hava dikkate alınmalıdır. **Standart şartlarda basınç irtifası = yoğunluk irtifası; OAT standardın üzerindeyse yoğunluk irtifası artar.**

### 2.2 Altimetre ve irtifalar
- **Kollsman penceresi:** Altimetreye basınç girilen pencere; girilen değer altimetrenin sıfır noktasını belirler. 1013 girilirse standarda göre yükseklik gösterir.
- **QFE:** Meydandaki gerçek basınç; ayarlanınca apronda altimetre **sıfır** gösterir (**height, AGL**). **QNH:** QFE'nin ISA'ya göre deniz seviyesine indirgenmiş hâli; apronda **meydan irtifasını** gösterir (**altitude, MSL**). **QNE (STD):** 1013,25 hPa / 29,92 inHg; **uçuş seviyesi (FL)** olarak basınç irtifasını gösterir.
  > Ders metninde: Kısaltmaların açılımı ("Qualified Natural Horizon/Earth/Field Elevation") resmî tanım değildir; Q kodlarının resmî açılımı yoktur, yalnız anlamları vardır.
- **Geçiş irtifası (transition altitude):** Bu irtifada ve altında dikey konum **irtifa (altitude)**. **Geçiş seviyesi (transition level):** Bu seviyede ve üzerinde **FL**; kullanılabilir **en alçak** uçuş seviyesi. **Geçiş tabakası:** İkisi arasındaki hava sahası; **bu tabakada düz uçuş yapılmaz**.
- **İrtifa çeşitleri (4):** **Indicated** (altimetreden okunan), **pressure altitude** (1013,25 girilince; PA = FL), **density altitude** (sıcaklıkla düzeltilmiş basınç irtifası; performans için), **true altitude** (deniz seviyesine göre gerçek).

### 2.3 Hava hızları
**IAS → CAS → EAS → TAS → GS:**
| Hız | Tanım ve düzeltme |
|---|---|
| **IAS** | Sürat saatinde okunan; gerçek hız değil, **dinamik basınç göstergesi** (pitot toplam basıncı kapsül içine, statik basınç dışına). |
| **CAS** | **IAS + alet ve pozisyon hatası.** Hata düşük hızlarda en büyük, seyir hızında en küçük. ADC'li modern uçaklar CAS gösterir. **Deniz seviyesi, ISA: CAS = TAS.** |
| **EAS** | **CAS + sıkışabilirlik hatası.** Yüksek hızda (**Mach 0,3'ten sonra**, 300 KTAS üstünde) önündeki hava sıkışır; CAS, EAS'den çok az büyüktür. **Deniz seviyesi ISA: EAS = CAS.** IAS, CAS, EAS dinamik basınç ölçüleridir; **EAS en doğrusudur**. |
| **TAS** | **EAS + hava yoğunluğu hatası**; **TAS = EAS / √σ** (σ = bağıl yoğunluk). Yoğunluk azalırsa (tırmanış) **TAS artar**; yoğunluk artışı veya sıcaklık azalışı TAS'ı düşürür. |
| **GS** | **TAS ± rüzgâr bileşeni** (kafa/kuyruk); uçağın yer üzerindeki izdüşüm hızı. |
- **Hata zinciri:** IAS–CAS: alet ve pozisyon; CAS–EAS: sıkışabilirlik; EAS–TAS: yoğunluk; TAS–GS: rüzgâr. **Havadaki mesafe TAS (NAM), yerdeki mesafe GS (NGM) ile**: NAM/TAS = NGM/GS.
- **Sürat saati renkleri:** **Kırmızı çizgi** = **VNE** (asla aşılmamalı); **sarı ark** = VNO–VNE (ihtiyat, yalnız sakin havada); **yeşil ark** = **VS1 (flapsız stall) – VNO** (normal işletme); **beyaz ark** = **VS0 (full flap stall) – VFE** (flap kullanım aralığı).

### 2.4 Kuvvetler, sürükleme ve güç
- **Dört kuvvet:** itme (thrust), kaldırma (lift), sürüklenme (drag), ağırlık (weight). Düz uçuşta itme > sürükleme → hızlanır; sürükleme > itme → yavaşlar.
- **Sürükleme:** Göreceli hava akışına paralel bileşen; **parazit sürükleme** + **indüklenmiş sürükleme** = toplam. **Ağır uçak:** Her sürat için indüklenmiş sürükleme daha fazla → toplam sürükleme daha fazla; **parazit değişmez**; **VMD daha yüksek sürat**. **Kirli konfigürasyon** (flap, iniş takımı açık): **parazit sürükleme artar, indüklenmiş değişmez**, her sürat için toplam sürükleme artar, gerekli itme artar; **VMD daha düşük sürat**.
- **İtme:** Kütlesi olan havanın arkaya hızlandırılmasıyla oluşur (pervane/jet); T = m(V_J − V_V). **Takat (güç)** uçak hızı arttıkça, irtifa arttıkça ve sıcaklık arttıkça **azalır**.
- **Gerekli güç:** **VMP (minimum güç/maks. havada kalış hızı) ≈ 0,76 VMD**; toplam sürükleme eğrisinin teğet noktası = VMD; güç eğrisi teğeti ≈ **1,32 VMD**.
  > Ders metninde: Slaytta VMP/VMD ilişkisi karışık anlatılmış ("teğet noktası 1,32 VMD" güç eğrisi için geçerlidir); kanonik ilişki VMP ≈ 0,76 VMD, **VMD ≈ 1,32 VMP**'dir.

### 2.5 Performans sınıfları
- **Sınıf A (JAR-25):** **10 ve üzeri yolcu** kapasiteli veya **5700 kg üzeri** tüm **çok motorlu jet ve çok motorlu turboprop**; en sıkı performans kriterleri.
- **Sınıf B (JAR-23):** **9 veya daha az yolcu** ve **5700 kg altı** **pervaneli** (tek veya çift motorlu) uçaklar; kriterler A'dan hafiftir. B sınıfı ticari kullanımda **gün batımından sonra, IMC'de ve güvenli zorunlu iniş yolu yoksa** uçurulamaz. Kalkış değerlendirmesinde (a) mevcut meydan mesafesinde kalkış, (b) kalkıştan sonra yeterli eğimde tırmanma gerekir; **tek motorlu B sınıfında obstacle clearance gösterilmesi gerekmez**.
- **Sınıf C:** 10 ve üzeri yolcu veya 5700 kg üzeri **çok motorlu pistonlu pervaneli** uçaklar.

### 2.6 Pist uzunluk parametreleri (deklare mesafeler)
- **TORA:** Kalkış koşusu için yeterli mevcut pist uzunluğu; normalde kaplamalı pist uzunluğuna eşit.
- **Stopway:** Yalnızca durmada kullanılabilen, pistle aynı özellikte (en az pist genişliğinde, orta hat merkezli) uzantı; uçak ağırlığını taşıyabilmelidir (taşıyorsa ASDA'ya katılır).
- **ASDA (Accelerate-Stop Distance Available):** **TORA + stopway**; acil duruş noktasına kadar mesafe (EMDA). **Balanced field:** Motor arızasında gereken minimum alan.
- **Clearway:** Pist sonundan başlayan, uçağın ilk tırmanışı için hazırlanmış engelsiz saha; **genişliği en az 152 m (500 ft)**; su veya normal yüzey olabilir.
- **TODA (Take-off Distance Available):** **TORA + clearway**; clearway pist uzunluğunun **%50'sinden fazla olamaz** (TODA ≤ **1,5 × TORA**).
- **Gerekli mesafeler:** **Kalkış koşusu (take-off roll)** = kalkış noktasından yerden kesilmeye; **havalanma mesafesi (airborne distance)** = yerden kesilmeden **screen height**'a; toplamı **kalkış mesafesi (take-off distance)**. **Screen height: Sınıf A için 35 ft, Sınıf B için 50 ft.** Gerekli mesafeler mevcut mesafeleri aşmamalıdır. Kalkış mesafesi formülündeki V **gerçek yer hızıdır (TGS)**: yoğunluğun IAS→TAS etkisi ve rüzgârın TAS→TGS etkisi hesaba katılır. Screen height'ta ulaşılacak kalkış emniyet hızı stall ve minimum kontrol hızının üzerinde güvenli marj sağlamalıdır.

### 2.7 Kalkış hızları ve stall
| Hız | Anlam |
|---|---|
| **VS** | Stall hızı; iniş konfigürasyonunda **VS0**. |
| **V1** | **Karar hızı**: bu hıza kadar arızada kalkış **durdurulur**, ötesinde devam edilir. **Kuru pistte daha yüksek**, ıslak pistte (durma mesafesi yaklaşık **%15** artar) **daha düşük**. |
| **VR (rotate)** | Pilotun burun tekerini yerden kaldırmaya (rotasyon) başladığı hız. |
| **VMU** | Minimum unstick; uçağın yerden güvenle ayrılabildiği **en düşük hız**. |
| **VLOF** | Yerden kesilme hızı (tip, ağırlık, irtifa, pist ve hava koşuluna bağlı). |
| **VMBE** | Maksimum fren enerji hızı: frenlerin enerji sınırı. |
| **VEF** | Kritik motorun arızalandığı varsayılan hız. |
| **V2** | Kalkış emniyet hızı: bir motor arızalıyken güvenle tırmanılan hız (flap konumuna bağlı); **V2min** minimum kalkış emniyet hızı. |
| **V3** | Tüm motorlar çalışırken sabit ilk tırmanma hızı (slaytta "flap toplama hızı" olarak da geçer). |
| **VMC** | Çok motorlu uçakta bir motor çalışmazken **yön kontrolünün** sürdürülebildiği minimum hız. **VMCG:** Kalkış koşusunda kritik motor arızasında yalnız aerodinamik kumandalarla yön kontrolünün sağlandığı minimum kalibre hız; **VMCG ≤ V1**. **VMCL:** İniş yaklaşmasında minimum kontrol hızı. |
- **Stall:** Hücum açısı kritik değeri aşınca (hız düşük veya hücum açısı fazla) kanat üstündeki akımın bozulup **kaldırmanın düşmesi**; ileri gidiş durur, hızlı irtifa kaybı başlar; kalkışta kurtulma şansı çok azdır.
  > Ders metninde: Stall "uçağın sağa veya sola yatması" ve "güç artırılıp burun indirilirse kurtulur" biçiminde anlatılmış; stall tanım olarak **kritik hücum açısının aşılmasıdır**, kurtarma burun indirerek hücum açısını azaltmaktır (güç yardımcıdır).
- **Stall hızını etkileyenler:** **Ağırlık ↑ → ↑; irtifa ↑ → ↑** (yoğunluk düşer); **sıcaklık ↑ → ↑**; **flap açılınca ↓** (CLmax artar).

### 2.8 Kalkış performansını etkileyen faktörler
Genel zincir: **Kütle ↑ → atalet ↑ → ivme ↓ → kalkış mesafesi ↑.**
- **Kütle:** (1) Ataletin artması ivmeyi azaltır; (2) tekerlek yükü ve **tekerlek sürüklemesi** artar; (3) daha büyük ağırlık için daha fazla lift gerekir → **kalkış emniyet hızı artar**; (4) ilk **tırmanış açısı azalır**, screen height'a ulaşmak daha uzun yatay mesafe ister.
- **Hava yoğunluğu:** Yoğunluk, basınç, sıcaklık ve nemle belirlenir. **Yoğunluk ↓ → güç/itme ↓ → tırmanış açısı ↓ → kalkış mesafesi ↑**; ayrıca aynı lift için hız artmalıdır. İrtifa arttıkça basınç ve yoğunluk azalır.
- **Rüzgâr:** **Kafa rüzgârı** gerekli yer hızını düşürür, ilk tırmanış açısını artırır → **kalkış mesafesi azalır** (20 kt kafa rüzgârı, 120 kt TAS → 100 kt yer hızı); **arka rüzgâr** tersini yapar. **Yönetmelik: kafa rüzgârı bileşeninin en fazla %50'si, arka rüzgâr bileşeninin en az %150'si hesaba katılır** (rapor edilen rüzgâr değişimine karşı güvenlik). **90° yan rüzgârda** mesafe sıfır rüzgârdakiyle aynıdır.
- **Pist yüzeyi:** Kuru pistte bile yuvarlanma direnci vardır. Kar, sulu kar, durgun su → sıvı direnci ve çarpma; sürükleme **suda kayma (hydroplaning) hızına** kadar artar, ötesinde azalır. Kontaminasyon **kalkış mesafesini uzatır**; kalkış iptalinde (RTO) fren sürtünme katsayısı ciddi düşer, fren basıncı düşürülmelidir → **durma mesafesi çok artar**.
- **Pist eğimi:** Ağırlığın uzunlamasına bileşeni **W × sin(eğim)**; **yokuş aşağı → kalkış mesafesi azalır; yokuş yukarı → artar** ("weight apparent thrust/drag").
- **Gövde kirliliği (kar, buz, don):** Sürükleme ↑, lift ↓, ağırlık ↑ → kalkış mesafesi artar; kalkışta uçak buz ve kardan **arındırılmış** olmalıdır.
- **Flap ayarı:** Optimum artış **CLmax'ı artırır**, stall ve kalkış hızını düşürür → **kalkış mesafesi azalır**; optimumun ötesinde sürükleme fazla → mesafe tekrar artar. **Flap açısı arttıkça tırmanış gradyanı azalır** → gerekli gradyan için izin verilen maksimum kütle düşer. **Düşük flap:** daha uzun kalkış mesafesi, **daha dik tırmanış**; **yüksek flap:** daha kısa mesafe, daha yatık tırmanış. Engel varsa ve TODA, TODR'dan büyükse en kısa mesafeyi veren flap en yüksek kalkış kütlesini vermeyebilir; **sıcak ve yüksek irtifada** daha düşük flap ile daha büyük kütle elde edilebilir.

### 2.9 Tırmanış
- **Dengeli tırmanış:** **L = W·cosθ; T = D + W·sinθ**; tırmanışta **W > L'nin dikey bileşeni, T > D**.
- **Tırmanış oranı (ROC):** Dikey sürat (ft/dk, VSI'dan okunur).
- **VX (best angle):** En büyük tırmanış **açısı**; belirli irtifaya **en kısa yer mesafesinde** ulaşılır; **engel aşmak** için kullanılır. **VY (best rate):** En büyük tırmanış **oranı**; belirli irtifaya **en kısa sürede** ulaşılır; gürültü azaltma ve hava sahasını çabuk terk için. VY, VX'e göre daha yatık ama daha hızlı tırmanıştır.
- **Mutlak tavan:** ROC = **0 fpm**. **Servis tavanı:** ROC **100 fpm**'e düştüğü irtifa.
- **Rüzgâr:** Kafa rüzgârı yer üzerindeki tırmanış gradyanını (uçuş yolu açısını) **artırır**; arka rüzgâr azaltır. Sabit güçte tırmanışta ROC ve AOC irtifayla azalır.
- **CLTOM (climb limited take-off mass):** Tırmanış gradyanı fazla itme/ağırlık oranına bağlıdır; faktörler **kütle, yükseklik, sıcaklık**. **Basınç irtifası ↑ → CLTOM ↓; sıcaklık ↑ → ↓; yüksek flap → ↓. Rüzgâr, pist eğimi ve pist yüzeyi CLTOM'u etkilemez.**
- **OLTOM (obstacle limited take-off mass):** Basınç irtifası ↑ → ↓; sıcaklık ↑ → ↓; yüksek flap → ↓; **arka rüzgâr OLTOM'u azaltır**; pist eğimi ve yüzeyi etkilemez.

### 2.10 Seyir, menzil, havada kalış
- **Düz seyirde** itme = sürükleme, lift = ağırlık. **En yüksek düz uçuş hızı:** sürükleme eğrisinin mevcut en yüksek itme çizgisiyle kesiştiği hız.
- **Menzil (range):** Mevcut yakıtla uçulabilen **maksimum yatay mesafe** (NM); **en uzun menzil VMD'de**. **CG ön limite yakınsa drag artar, menzil azalır; arka limite yakınsa drag azalır, menzil artar.** Kütle artarsa aynı AOA için TAS ve gerekli güç artar, yakıt tüketimi artar, menzil azalır. **Kafa rüzgârı yer menzilini azaltır, arka rüzgâr artırır.**
- **Havada kalış süresi (endurance):** Mevcut yakıtla (veya süzülüşte) havada kalınabilecek süre; **en uzun endurance VMP'de**. CG öne yakınsa endurance azalır, arkaya yakınsa artar; **hafif uçak ağıra göre daha uzun** kalır. **Rüzgârın endurance'a etkisi yoktur** (yatay hareketle ilgisi yok).

### 2.11 Alçalma, süzülüş, iniş
- **Dengeli alçalış:** **L = W·cosθ; D = T + W·sinθ.** **Süzülüş**, alçalıştan **itmenin olmamasıyla** farklıdır. Alçalma oranı dikey süratle (fpm) ifade edilir.
- **Rüzgâr alçalma oranına ve süresine etki etmez**; yere göre alçalış açısını etkiler: **arka rüzgâr açıyı küçültür, kafa rüzgârı büyütür.**
- **En iyi süzülüş:** **L/D max ↔ VMD ↔ optimum AOA (~4°)**; en uzun süzülüş mesafesi **best glide speed**'de. Temiz konfigürasyonda süzülüş mesafesi artar; flap L/D'yi bozar. **Kütle süzülüş mesafesini etkilemez** (L/D ağırlıktan bağımsız); ağır uçak daha hızlı süzülür ve daha az havada kalır. Arka rüzgâr mesafeyi artırır, kafa rüzgârı azaltır.
- **İniş mesafesi (landing distance):** Pist eşiği üzerinde **screen height 50 ft**'ten tamamen durmaya kadar; hava ve iniş rulesi bölümleri. 50 ft'te sürat **VREF** olmalı (üstü mesafeyi artırır, altı stall yakınlığı nedeniyle risklidir).
- **İniş mesafesini etkileyenler:** iniş ağırlığı (↑ → mesafe ↑), yoğunluk/yüksek irtifa/sıcaklık/nem (mesafe ↑), **arka rüzgâr ↑ / kafa rüzgârı ↓**, pist eğimi (**aşağı eğim mesafeyi artırır; %1 aşağı eğim ≈ %5 artış**), pist yüzeyi (su, buz, kar, çim → artar), **flap** (yüksek CL, düşük iniş hızı → mesafe kısalır).

## BÖLÜM 3 · Uçuş Planlama ve İzleme

### 3.1 VFR ve hava sahası
- **VMC:** VFR için ICAO genel VMC minimumları sağlanmalıdır. **Türkiye'de gün batımından gün doğumuna VFR uçuşa müsaade edilmez.**
- **Hava sahası sınıfları (ders metni):** **A:** en yoğun trafik, **VFR'ye kapalı**. **B:** çok yüksek hava sahaları, IFR ve VFR'ye açık. **C:** yüksek hava sahaları; VFR ilgili ATS ile temas koşuluyla özel şartlarda. **D:** daha az yoğun; birçok CTR/CTA ve **ATZ** bu sınıftadır. **E:** D'ye benzer, ancak **VFR için ATC izni gerekmez**, daha kısıtlı trafik bilgisi.
  > Ders metninde: "Türkiye'de hava sahası sınıflandırması olmadığı için" ibaresi A–E sınıflarının genel (ICAO) tanımlarının verilmesini gerekçelendiriyor.
- **ATIS:** Yoğun meydanlarda rutin varış/ayrılış bilgisini belirli frekansta sürekli yayınlar; meydana yaklaşan uçak **ilk temasta ATIS kod harfini** bildirir; ayrılan uçak normalde bildirmek zorunda değildir ama son bilgiyi aldığını teyit etmelidir. Değişimde ATIS güncellenir.
- **Harita:** Plotter ile mesafe/rota ölçülür; manyetik kuzey haritada **küçük mavi oklarla** gösterilir.
- **Seyir irtifaları:** **IFR tam irtifalarda, VFR +500'lü irtifalarda**. **Doğuya (000°–179°) tek +500; batıya (180°–359°) çift +500** irtifalar.

### 3.2 Meteorolojik raporlar
- **METAR:** Havacılık amaçlı mutad hava raporu; **yarım saat aralıklarla**.
- **SPECI:** İki METAR arasında havacılığı etkileyen **önemli değişiklikte**, METAR kodlamasıyla aynı özel rapor.
- **TAF:** Meydan hava tahmini (yer rüzgârı, görüş, hava olayı, bulut); **9, 18 veya 24 saatlik** aralıklarla yayımlanır.

### 3.3 Yakıt planlaması
- Gerekli yakıt: havada harcanacak (tırmanış/alçalma dahil) + her iki meydanda yerde harcanan + bekleme + yedek meydan yakıtı + rezerv; hesapta **rüzgâr, gecikmeler, hava tahmini, tahmin edilemeyen olaylar** dikkate alınır. Ramp fuel ve yakıt türleri B1.2'deki gibidir (contingency %5 trip veya 5 dk; final reserve türbin 30, piston 45 dk @ 1500 ft).

### 3.4 Havacılık yayınları
- **AIP:** Her ülkenin otoritesi (Türkiye'de **SHGM ve DHMİ**) ICAO ile uyumlu yayımlar; bölümleri **GEN** (genel: ICAO farklılıkları, meteoroloji, arama kurtarma), **ENR** (rota: kısıtlı hava sahaları, seyrüsefer yardımcıları), **AD** (meydanlar: veriler, gün doğumu/batımı, yaklaşma); ayrıca **SUP** (ilaveler) ve **AMDT** (düzeltmeler).
- **AIC:** AIP'de olmayan, **NOTAM gerektirmeyen** bilgiler. **NOTAM:** Hizmet, yöntem, tehlike veya değişikliği bildirir; ICAO formatında; Türkiye'de **uluslararası dağıtım A, B, C, S serileri; iç dağıtım E, G, H, M serileri**. **Yasak bölge (P):** askerî zorunluluk; **kısıtlı bölge (R):** kamu güvenliği; **tehlikeli bölge (D):** uçuşa risk oluşturan faaliyet.

### 3.5 Uçuş planı
- Her uçuştan önce doldurulup **ilgili AIS birimine** verilir ve onay alınır; planı olmayan uçuşa izin verilmez; planlar Türkiye'de **3 ay saklanır**.
- **Zamanlama:** IFR veya VFR plan, tahmini kalkıştan **en az 30 dk önce** AIS'e ulaşmalı. Tahmini kalkış (block-off) gecikmesinde iptal: **VFR 1 saat, IFR kontrollü hava sahasında 30 dk, kontrolsüzde 60 dk**. Süre dolmadan telefonla uzatma: **VFR 1 saat, IFR 30 dk**. Plan **büyük harfle**, tüm zamanlar **Zulu (UTC)**.
- **Münferit** plan her uçuş için ayrıdır (formasyon ve ara duraklı uçuş da münferit). **Sürekli uçuş planı (RPL):** ticari havayolu usulü; aynı işleticinin **en az 10 IFR uçuşu** için, ilk uçuştan **en az 2 hafta önce** sunulur.
- **Çağrı adı:** **7 karakteri geçemez**, boşluk/tire kullanılmaz (TK514, AFHA21, TC-GDA).
- **Uçuş kuralları:** **I** (IFR), **V** (VFR), **Y** (önce IFR), **Z** (önce VFR). **Uçuş tipi:** **S** tarifeli, **N** tarifesiz ticari, **G** genel havacılık, **M** askerî, **X** diğer.
- **Uçak sayısı:** tek uçaksa "01" veya boş. **Uçak tipi:** ICAO kodu (C172); kodu yoksa **ZZZZ** (ayrıntı Item 18'de).
- **Wake türbülans kategorisi:** **H (Heavy): MTOW 136 000 kg ve üzeri; M (Medium): 7000 kg üzeri, 136 000 kg altı.**
  > Ders metninde: "Türbülans kategorileri ağır ve orta olmak üzere iki tanedir" denmiş; ICAO'da ayrıca **L (Light, ≤7000 kg)** ve J (Super) vardır.
- **Ekipman:** Standart: VHF RTF, ADF, VOR, ILS; uçaktaki ekipmanın çalışır olduğu kabul edilir; farklı kombinasyonlar belirtilir.
- **Hız/seviye değişim noktası:** **TAS'ta %5 veya daha fazla ya da Mach 0,01 veya daha fazla** değişimde belirtilir; eğik çizgiyle (/) yeni hız, sonra yeni seviye.
- **Rota:** VFR'de koordinat ve seyrüsefer yardımcıları; **DCT** = "Direct To".
- **Varış meydanı:** 4 harfli ICAO kodu; yoksa **ZZZZ** (ad Item 18'de). **Total EET:** **IFR'de kalkıştan varış meydanının IAF noktasına** süre; **VFR'de kalkıştan varış meydanına** toplam tahmini süre.

## BÖLÜM 4 · Ağırlık Limitleri ve Dönüşüm Örnekleri

### 4.1 Yapısal ve performans limitleri
- **Dört yapısal limit:** **MSRM** (maks. yapısal taksi/rampa), **MSTOM** (kalkış), **MSLM** (iniş), **MZFM** (maks. sıfır yakıt kütlesi; yakıt hariç izin verilen maksimum, kanat depoları boşken gövdenin taşıyabileceği; **kanat kökünde büyük eğilme momenti** oluşmasın diye).
- **Performans limitleri:** Meydan irtifası ve sıcaklık (yoğunluk), pist uzunluğu, çevre arazi yapısı. **PLTOM** (kalkış meydanı limitli), **PLLM** (iniş meydanı limitli).
- **Düzenlenmiş kütleler:** **RTOM = MSTOM ve PLTOM'un küçüğü** (= **MATOM**); **RLM = MSLM ve PLLM'nin küçüğü** (= **MALM**).
- **Maksimum kalkış kütlesi (MTOM):** **RTOM, RLM + trip fuel, MZFM + take-off fuel** üçünden **en küçüğü**. ZFM'ye TOF eklenirken **taksi yakıtı dahil edilmez**. Örnek: MSTOM 78 000, MSLM 71 500, MZFM 63 000, PLTOM 85 000, PLLM 67 000, TOF 13 800, trip 5 200 → RTOM = min(78 000; 85 000) = **78 000**; RLM = 67 000 + 5 200 = **72 200**; MZFM = 63 000 + 13 800 = **76 800** → **MTOM = 72 200 kg**.

### 4.2 Birim dönüşümleri (ICAO Annex 5)
- **Kütle = hacim × yoğunluk**; ISA deniz seviyesi yoğunluğu 1225 g/m³ (1,225 kg/m³).
- **1 m = 3,28 ft; 1 NM = 1852 m; 1 US galon = 3,785 L; 1 Imp galon = 4,546 L; 1 kg = 2,205 lb.** Litre ↔ kg: **litre × SG = kg** (SG = özgül ağırlık); lb ↔ kg: ÷/× 2,205.
  > Ders metninde: Slaytta "İngiliz galonu ↔ litre ×1,2/÷1,2" yazılmış; bu ABD galonu ile İngiliz galonu arasındaki yaklaşık dönüşümdür (1 Imp = 1,2 US). Doğrudan litreye dönüşüm için 4,546 kullanılır.

### 4.3 Temel boş kütle için CG
- Uçak üç tekerlek noktasından tartılır; **kütle × kol = moment**, toplam moment / toplam kütle = **CG**. Örnek (lb): burun tekeri 500 × (−20) = −10 000; sol ana 2000 × +30 = +60 000; sağ ana 2000 × +30 = +60 000 → toplam **4500 lb, +110 000 moment → CG = 24,4 inç datumun gerisinde** (moment pozitif olduğundan).

### 4.4 Yüklü kütle ve yük kartı
- Büyük yolcu uçaklarında CG, **kalkış** ve **sıfır yakıt** kütlesinde belirlenir (ikisi limit içindeyse uçuş boyunca limit içindedir). Bazı uçaklarda iniş takımı güç çeviricileri kütleyi ölçüp FMS'e gönderir.
- **Prosedür:** Kütle sütununa BEM (hafif uçak) veya **DOM ve DOI (dry operating index)** (büyük uçak) girilir; tüm kütleler eklenerek **ZFM ve TOM**'a ulaşılır (limit kontrolü); kol sütununa datumdan uzaklık yazılır (**datumun gerisi pozitif, önü negatif**); moment = kütle × kol (**pozitif kütle × negatif kol = negatif moment**); momentler toplanır; **CG = toplam moment / toplam kütle**; sonuç ön ve arka limit içinde olmalıdır.
- **Yük kartı:** Her uçuştan önce doldurulur; uçak kaydı/tipi, uçuş numarası, kaptan ve kartı dolduran kişi, DOM ve CG, kalkış ve trip yakıtı, diğer harcanan malzemeler, trafik yükü, kalkış/iniş/sıfır yakıt kütleleri, yük dağılımı, CG ve limitler yer alır.
- **Örnek 1 (tek motorlu piston):** BEM 2415 lb + ön koltuk 340 + arka koltuk 340 + bagaj 200 = **ZFM 3295 lb**; yakıt ekleyince **rampa 3655 lb**; **TOM = rampa − çalıştırma/taksi yakıtı = 3655 − 13 = 3642 lb**. Momentler: ZFM 284 286; rampa 311 286; TOM 310 286 → **TOM CG = 310 290 / 3642 ≈ 85,2 inç (datumun gerisinde)**. İniş: yolculuk yakıtı 240 lb → **iniş kütlesi 3642 − 240 = 3402 lb**; iniş momenti = 310 286 − (240 × 75) = 292 286. ZFM'de CG limit içindeyse iniş CG'sini hesaplamak normalde gerekmez; hafif uçakta iniş momenti iniş kütlesine bölünür.
- **Örnek 2:** Yakıt 7 US gal/sa, yağ 1 quart/sa; kalkış kütlesi 2055 lb, momenti +895 → **kalkış CG ≈ +0,435 inç**. 1,5 saatlik uçuşta yakıt **63 lb**, yağ **2,8 lb** → iniş kütlesi 2055 − 63 − 2,8 = **1989,2 lb**; iniş momenti = 895 − (63 × 2) − (2,8 × −48) ≈ **+903** → **iniş CG ≈ +0,454 inç** (limitler: datumun 2 inç önü – 6 inç gerisi, ikisi de limit içinde).
  > Ders metninde: Çözümde "30 saatlik uçuş" yazılmış; hesaplar **1,5 saatlik** (01.30) uçuşa göredir.

### 4.5 MAC ve CG'nin yeniden konumlandırılması
- **MAC (ortalama aerodinamik kord):** Kanadın geometrik olarak hücum ve firar kenarlarını birleştiren çizgi; **uzunluğu ve datumdan uzaklığı sabit**; büyük uçaklarda **CG, MAC yüzdesi** olarak verilir. **LeMAC** hücum kenarı, **TeMAC** firar kenarı. "%25 MAC", CG'nin hücum kenarından MAC uzunluğunun dörtte biri kadar gerisinde olduğunu gösterir.
- **%MAC = (CG − LeMAC) / MAC uzunluğu × 100.** Örnek: MAC 152 inç, LeMAC datumun 40 inç gerisinde, CG 66 inç gerisinde → (66 − 40)/152 × 100 = **%17,1**.
- **CG limit dışındaysa** yük **yer değiştirilir** veya **kütle eklenir/çıkarılır**. Formül (yer değiştirme): **m / M = d / D** (m taşınan kütle, M uçağın toplam kütlesi, d CG'nin kayma miktarı, D yükün taşındığı mesafe).
  - **Yükün yerini değiştirme:** 4451 lb uçak, CG +92, 200 lb yük arka koltuktan (157,5) ön koltuğa (85,5) → D = 72 in → d = 200 × 72 / 4451 ≈ **3,24 in öne**, yeni CG **+88,76 in**.
  - **Kütle ekleme:** Etkisi iki yönlüdür: momenti ve brüt ağırlığı değiştirir. Örnek: 185 lb ikinci pilot ön koltuğa (85,5) → CG +92'den **+91,74 in**'e kayar (d = 185 × 6,5 / 4636 ≈ 0,26 in). Hedef CG'ye ulaşmak için eklenecek kütle: M = 10 000 kg, CG 8 ft, hedef 13 ft, arka ambar 20 ft → **7142,86 kg** arka ambara eklenmelidir.
  - **Kütle çıkarma:** Ağırlığın alındığı yerin tersi yönüne CG kayar. Örnek: ön ambardan (5 ft) çıkarılacak kütle (hedef CG 13 ft) → **6250 kg**. 294 lb arka koltuk yolcusu inerse CG **92 → 87,37 in** (≈ 4,63 in öne).
  - Başka bir örnekte CG'yi güvenli bölgeye almak için **333,333 kg** kargonun yer değiştirilmesi gerektiği hesaplanmıştır.

### 4.6 Grafik yöntemler, yükleme limitleri ve underload
- **Zarf (envelope):** Kütle ve CG, grafik üzerinde **zarfın içinde (veya üzerinde)** olmalıdır; **kütle her zaman dikey eksendedir**. Yatay eksen: CG konumu (in/m/cm), CG momenti veya **%MAC**. Referans: CAP 696 (SEP1, MEP1, MRJT1 örnekleri); SEP için "ağırlık merkezi zarfı" dikey eksende lb, yatay eksende inç.
- **Yükleme limitleri:** **Doğrusal (running/linear) yük limiti** gövdeyi aşırı yükten korur (kg/inç). **Alan (area) yük limiti** döşeme panellerini korur (kg/m² veya lb/ft²): **düzgün dağılımlı (UD)** ve **yoğunlaşmış** yük. **Tek kompartman ve toplam kompartman limitleri** ile doğrusal limitler aşılamaz; yük UD limitini aşıyorsa **yük dağıtıcılar (kalas)** ile geniş alana yayılır. "Moving load" zeminde izin verilen toplam kütle, "fixed load" zeminin belirli bölümüne konabilecek maksimum yüktür.
- **TOM = DOM + yakıt + trafik yükü.**
- **Underload** (son dakika yük/yakıt değişiklikleri için): **Structural limited traffic load = MZFM − DOM**; **take-off limited traffic load = RTOM − DOM − take-off fuel**; **landing limited traffic load = RLM − DOM − kalan yakıt**; **en küçüğü** trafik yükü sınırıdır. İzin verilen kalkış kütlesi **RTOM, MZFM + take-off fuel, RLM + trip fuel**'in altında olmalıdır. Zorunlu yakıtlar: start-up/taxi, trip, contingency (trip'in %5'i), alternate (SEP1 için en uzak alternatife **45 dk**), final reserve (SEP1 için alternatif üstü **2000 ft ve 45 dk**).
