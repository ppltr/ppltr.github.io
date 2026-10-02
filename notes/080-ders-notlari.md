# 080 · Uçuş Prensipleri — ders notları

Kaynak: SHGM KDM, *Uçak Uçuş Prensipleri 1* (U 01 E UO 071), dijital eğitim içeriği. Slayt metinleri
düzenlenerek aktarıldı; videolar ve etkileşim kalıntıları (düğme etiketleri, şekil yazıları) atıldı.
Bölüm sonu soruları `data/080_ders_notu_sorulari.json` içindedir.

## BÖLÜM 1 · Temel Kavramlar, Kanunlar ve Tanımlar

### B1.1 Tanımlar

#### Terimler sözlüğü

| Terim | Anlamı |
|---|---|
| Aerofoil | Kanat profili. Kanadın kesit geometrisi; hava içinde hareket ederken taşıma kuvveti üretmek üzere şekillendirilmiş yapı. |
| Amplitude | Titreşim genliği, genişlik, salınım. |
| Attitude | Ufka göre uçak burnunun burun aşağı veya burun yukarı yönelimi. |
| Boundary Layer | Sınır tabakası. Akışkanın viskozite etkilerinin baskın olduğu, yüzeye bitişik hava tabakası. |
| Buffeting | Uçaktan dağılan türbülanslı akışın uçağın herhangi bir parçasında yarattığı düzensiz titreşim. |
| Convergent | Birbirine yakınlaşan, birleşen. |
| Divergent | Birbirinden uzaklaşan, ayrılan. |
| Equilibrium | Denge. Cisme etki eden kuvvet veya momentlerin toplamının sıfır olması. |
| Flight Path | Uçağın havada izlediği yol. |
| Laminar Flow | Yüzeye paralel, bitişik hava akışı; hava akışı birbirine karışmaz, sabit düzende hareket eder. |
| Load Factor | Yük katsayısı. Taşıma kuvvetinin ağırlığa oranı: n = L/W. |
| Pitot Tube | Hava akımı istikametine göre ucu açık olan, toplam ve statik basınç farkından hızı ölçen alet. |
| Relative airflow (relative wind, free stream flow) | Göreceli hava akımı / göreceli rüzgâr / serbest hava akımı. Uçak sabit hızla ilerlerken karşılaştığı rüzgârın hızı ve yönü; uçuş hattına paralel ve ters yönde etkir. |
| Separation | Hava akımının temas ettiği yüzeyden ayrılması, kopması. |
| Stability | Kararlılık. Dengesi bozulan uçağın pilot müdahalesi olmadan denge konumuna dönme eğilimi. |
| Stagnation Point | Durma noktası. Hava akımının kanat hücum kenarında ikiye bölündüğü ve hızının sıfıra düştüğü nokta. |
| Static Vent | Statik basıncı ölçmek için gövdede plaka üzerine yerleştirilen küçük delik. |
| Throat | Kanal kesit alanının en küçük olduğu yer (boğaz). |
| Turbulent Flow | Hava akışının hızlanıp dağılmasıyla oluşan düzensiz akım. |
| Viscosity | Akmaya karşı direncin ölçüsü; yüksek viskoziteli akışkan daha zor akar. |
| True Airspeed (TAS, V) | Gerçek hava hızı; genelde knot cinsinden, uçağın havaya göre hızı. |

#### Kütle ve ağırlık
- **Kütle (mass):** Cismin içerdiği madde miktarı; yerçekiminden bağımsızdır.
- **Ağırlık (weight):** Bir kütleye yerçekiminin uyguladığı kuvvet; yerçekimine bağlıdır.

#### Kuvvet
**F = m·a** — F kuvvet (Newton, N), m kütle (kg), a ivme (m/s²). 1 N = 1 kg·m/s². Kuvvet, cismin hareketini veya
şeklini değiştirecek etkidir; ivmeyle doğru orantılıdır.

#### Ağırlık merkezi (CG)
Ağırlık CG boyunca etkir. Dönme CG etrafında olur ve uçağın eksenleri CG'den geçer. Uçağın kararlı ve
kontrol edilebilir olması için CG ön ve arka limitler içinde olmalıdır.

#### İş ve güç
- **İş = kuvvet × yol** (Nm = joule, J). Örnek: 10 N'luk kuvvet cismi 2 m hareket ettirirse 20 J iş yapılmıştır.
- **Güç = iş / zaman** (watt = J/s). Aynı iş 5 saniyede yapılırsa güç 4 J/s'dir.

#### Enerji ve kinetik enerji
Cisim iş yapabiliyorsa enerjiye sahiptir; birimi işle aynı (joule). **Kinetik enerji** hareket halindeki cismin
enerjisidir; kütleye ve hıza bağlıdır, hız arttıkça artar.

#### Newton yasaları
1. **Birinci (inertia/eylemsizlik):** Net kuvvet uygulanmadıkça cisim hareketsiz kalır ya da sabit hızla doğrusal hareketine devam eder.
2. **İkinci (kuvvet–momentum):** Cisim, etki eden kuvvet yönünde ivmelenir; ivme kuvvetle doğru orantılıdır. 1 kg'lık cisme 1 N etki ederse 1 m/s² ivme kazanır.
3. **Üçüncü (etki–tepki):** Her etkiye eşit ve zıt bir tepki vardır.

#### Süreklilik denklemi
Venturi borusundan geçen hava kütlesi sabittir: giren kütle = çıkan kütle (ρ₁A₁V₁ = ρ₂A₂V₂). 0,3 Mach'ın altında
hava sıkıştırılamaz sayılır, yoğunluk değişimi önemsizdir; bu durumda **A₁V₁ = A₂V₂**: hız kesit alanıyla ters
orantılıdır — alan daralınca hız artar, genişleyince azalır.

#### Bernoulli prensibi
Enerjinin korunumuna dayanır: akışkanın hızının arttığı yerde basınç düşer. Akışkan enerjisinin üç bileşeni:
**statik basınç, dinamik basınç, toplam basınç**.

#### Venturi boyunca sesaltı sıkıştırılamaz akış
Kütle akısı (debi) = yoğunluk × hava sürati × kesit alanı. Venturide bozulmamış akış → daralan bölüm → boğaz
(daralma noktası) → genişleyen bölüm sırasıyla izlenir.

#### Yoğunluk
Birim hacme düşen kütle: **ρ = m / V** (kg/m³). Basınç, sıcaklık ve nemle değişir; uçak performansını önemli
ölçüde etkiler.

#### IAS ve TAS
- **IAS (Indicated Airspeed):** Hız göstergesinde okunan, pitot-statik sistemin ölçtüğü hız. İrtifa, sıcaklık ve alet hatalarını hesaba katmaz.
- **TAS (True Airspeed):** Hava yoğunluğu değişimini hesaba katan gerçek hız. Gösterge standart deniz seviyesi yoğunluğuna (1,225 kg/m³) göre kalibredir; uçak bu yoğunlukta uçarsa IAS = TAS olur.

### B1.2 Hava akışı

#### Aerodinamik yükler ve akış
Taşıma ve sürükleme, hava akışının etkisiyle oluşur. Uçağın havada hareket etmesi ya da havanın sabit uçağın
etrafından akması fark etmez; sonuç aynıdır. Hava akımı atmosferdeki moleküllerin belirli hız ve yönde hareketidir;
yoğunluk, sıcaklık, basınç ve nemle ilişkilidir. İki ana tür: **laminer** (düzgün, paralel yollar) ve
**türbülanslı** (düzensiz, girdaplı). Akım çizgileri havanın kanat çevresinde nasıl yönlendiğini gösterir.

| Model | Ne gösterir |
|---|---|
| İki boyutlu akış | Kanat kesiti etrafındaki kuvvetler. Akışın kanat üstündeki düşük basınca yönelmesine **upwash**, kanadı geçtikten sonra eski durumuna dönmesine **downwash** denir. |
| Üç boyutlu akış | Basınç farkından doğan kanat ucu vortexleri ve indüklenmiş sürüklemeyle taşımanın kanat açıklığı boyunca dağılımı. |

#### Kanat terminolojisi
- **Kordo / veter (chord):** Hücum ve firar kenarı arasında kordo hattı boyunca mesafe.
- **Kordo hattı:** Hücum kenarını firar kenarına bağlayan düz hat.
- **Kalınlık–kordo oranı:** Kanat kalınlığının kordo uzunluğuna oranı.
- **Bombe (kamburluk):** Kanadın eğimi. **Bombe hattı:** Hücum–firar kenarını birleştiren, üst ve alt yüzeye eşit uzaklıktaki hat. **Maksimum bombe:** Kordo hattı ile bombe hattı arasındaki en büyük mesafe.

#### Yüzeye etki eden kuvvetler
- **Hücum açısı (AOA):** Kordo hattı ile göreceli rüzgâr arasındaki açı.
- **Taşıma (lift):** Bağıl harekete **dik** aerodinamik kuvvet.
- **Sürükleme (drag):** Bağıl harekete **paralel** ve hareket yönüne zıt kuvvet.
- **Basınç merkezi (CP):** Taşıma kuvvetinin etki ettiği kabul edilen nokta.

#### Kanat geometrisi
| Terim | Tanım |
|---|---|
| Wing area (S) | Kanatların toplam yüzey alanı. |
| Wing span (b) | Bir kanat ucundan diğerine mesafe (açıklık). |
| Average chord (c) | Kanat açıklığı boyunca ortalama genişlik. |
| Aspect ratio (AR) | Kanat açıklığının ortalama kordoya oranı; uzun dar kanatta yüksek, kısa geniş kanatta düşük. |
| Tip chord / root chord | Kanat ucu / kanat kökü kordo uzunluğu. |
| Taper ratio | Uç kordonun kök kordona oranı. |
| Wing planform | Kanadın yukarıdan bakışta plan şekli. |

## BÖLÜM 2 · Aerodinamik Etkiler ve Stall

### B2.1 Kanat üzerinde hava akımı ve basınç dağılımı
İki boyutlu akışta kanat profili kesit gibi gösterilir; akış çizgileri, basınçlar ve kuvvetler incelenir.
**Downwash** akışın kanat arkasında aşağı yönlü akışıdır; **upwash** kanadın önünde akışın yukarı yönlü akışıdır.

- **Durma noktası (stagnation point):** Hava akışının kanada çarpıp hızının sıfıra düştüğü, akışın üst ve alt yüzeye ayrıldığı nokta. Hücum açısı değişince yeri değişir: pozitif kamburluklu kanatta 0° AOA'da hücum kenarının altındadır; AOA kritik (stall) açıya doğru arttıkça aşağı doğru hareket eder.
- **Basınç dağılımı:** Hücum kenarı yakınında basınç yüksektir (durma noktası). Hava üst yüzeyde geriye aktıkça basınç düşer; kamburluk nedeniyle üst yüzeydeki düşüş daha fazladır ve taşımayı oluşturur. Firar kenarına doğru hız azaldıkça basınç artar → **ters basınç gradyanı** (basıncın akış yönünde artması). Kritik hücum açısı (yaklaşık 16°) aşılınca üst yüzey ayrılmış akışla kaplanır, ters gradyan akışın yüzeyi izlemesini önler ve kanat stall olur.
- **CG ve CP:** CG uçağın ağırlıklarının toplandığı yer; CP kanat üzerindeki basınçların toplandığı ve kaldırmanın etki ettiği yer. Genellikle farklı yerlerdedir; aralarındaki ilişki uçak dengesi için çok önemlidir.
- **Taşıma – AOA:** Eğri, **CLmax** tepe değerine kadar AOA ile kademeli artar. Bu açıyı aşınca stall başlar ve taşıma azalır (stall açısı). Eğrinin şekli kanat profiline bağlıdır.
- **İndüklenmiş sürükleme ve hız:** Taşıma üretirken kanat ucu girdaplarının yarattığı direnç; downwash taşımanın bir kısmını geriye yönlendirir. AOA arttıkça ve kanat geniş-kısa olunca artar. Etkileri: yakıt tüketimi artar, düşük hızlarda performans kaybı belirginleşir. Çözümler: **winglet**'ler (vortex etkisini azaltır), uzun ve dar kanatlar.

### B2.2 Taşıma kuvveti katsayısı (CL) ve formülü
Taşıma, havanın **yoğunluğu (ρ)** ve **hızı (V)** ile kanadın **alanı (S)** ve **taşıma katsayısına (CL)** bağlıdır:

**L = ½ · ρ · V² · S · CL**   (½ρV² havanın dinamik basıncıdır)

CL kanat şekli ve hücum açısına bağlıdır; kanadın akışı ne kadar verimli kullandığını gösterir.

| Etken | Taşımaya etkisi |
|---|---|
| Hava yoğunluğu | Doğru orantılı. İrtifa arttıkça yoğunluk azalır, taşıma düşer. |
| Hız | **Hızın karesiyle** doğru orantılı. |
| Kanat alanı | Doğru orantılı. |
| CL | Şekil ve hücum açısına bağlı; AOA ile CLmax'a kadar artar, sonra stall nedeniyle azalır. Flap açmak şekli değiştirerek CL'yi etkiler. |

Faktörlerden birinin artması taşımayı artırır; taşıma sabit tutulacaksa faktörler birbirini dengelemelidir.

**Sürükleme:** D = ½ · ρ · V² · S · CD. CD cismin şekline, yüzey özelliklerine ve diğer aerodinamik etkenlere bağlı boyutsuz bir değerdir. Taşıma ve sürükleme katsayıları, farklı şekil ve boyuttaki cisimlerin aerodinamik performansını karşılaştırmayı kolaylaştıran boyutsuz parametrelerdir.

### B2.3 Kanat ucu vortexleri, indüklenmiş sürükleme ve yer etkisi
- **Üç boyutlu akış:** Kanat alt ve üst yüzeyi arasındaki basınç farkı, kanat uçlarında havanın dışarı yönlenmesine ve girdap (vortex) oluşmasına yol açar.
- **Sürükleme:** Uçağın hareket yönüne zıt aerodinamik kuvvet (arabadan dışarı uzatılan elin hissettiği direnç gibi).
- **Parazit sürükleme:** Şekil, biçim ve yüzey özelliklerinden doğar; hızın karesiyle artar. Bileşenleri: yüzey sürtünme, şekil/basınç ve girişim sürüklemesi.
- **İndüklenmiş sürükleme:** Taşıma üretimiyle ilişkili, kanat ucu vortekslerinin yukarı-aşağı hava akımını saptırmasından doğar.
- **Vortekslerin hücum açısına etkisi:** Kanat ucu vorteksleri açıklık boyunca taşıma dağılımını değiştirir; artan downwash dış bölümlerde **etkin hücum açısını azaltır, indüklenmiş hücum açısını artırır**.
- **İndüklenmiş hücum açısı (αi):** Vorteksler göreceli akışı aşağı saptırır; etkin akış (effective airflow) kanada bu sapmış halde gelir. Taşıma geriye eğilir; bu geriye eğimin serbest akım doğrultusundaki bileşeni **indüklenmiş sürüklemedir (Di)**. αe etkin, αi indüklenmiş hücum açısıdır.
- **İndüklenmiş sürükleme ve hız:** Düz uçuşu korumak için hız azaldıkça AOA artar → vortex güçlenir → taşıma daha çok geriye eğilir → indüklenmiş sürükleme artar. Akışın açısal sapması hem girdap şiddetine hem TAS'a bağlıdır.
- **Kanat ucu vortexleri:** Alt-üst basınç farkı kanat boyunca akışla birleşince oluşur; yüksek AOA'da daha güçlüdür. Kanat arkasında vortex etrafındaki dolaşım **downwash** (aşağı akış), kanat uçlarının yakınında **upwash** (yukarı akış) yaratır.

#### Kuyruk türbülansı (wake turbulence)
Taşıma üretiminin doğal sonucudur; takip eden uçaklar için risk oluşturur.
- **Nedeni:** Kanat ucu vorteksleri. Kalkışta **rotasyonla (burun tekerleği kalkınca) başlar**, inişte burun tekerleği yere değene kadar sürer; yüksek taşıma üretilen safhalarda şiddetlenir.
- **Dağılımı:** Vorteksler uçak ilerledikçe kanat uçlarından dışarı ve aşağı doğru uzanır.
- **Süresi:** Atmosfer koşullarına bağlıdır; durağan atmosferde daha uzun sürer.
- **Kaçınma:** Otoriteler uçaklar arası minimum ayırma standartları koyar.

#### Yer etkisi (ground effect)
Uçak yere kanat açıklığının **yarısından daha yakın** uçarken taşıma ve sürükleme değişir. Yer yakınında kanat ucu vorteksleri ve **indüklenmiş sürükleme azalır**; yukarı akış sınırlandığı için etkin hücum açısı artar, taşıma ve aerodinamik performans artar.
- **Yer etkisine girerken** (yükseklik < açıklığın yarısı): taşıma artar, kabarma hissi olabilir; palye (float) nedeniyle iniş mesafesi uzayabilir. Aşağı akımdaki azalma kuyruktaki aşağı yükü (download) azaltır ve **burun aşağı yunuslama momenti** doğurur.
- **Yer etkisinden çıkarken** (yükseklik > açıklığın yarısı): aşağı akım artar → indüklenmiş sürükleme artar, taşıma azalır; yunuslama açısı değişebilir, tırmanma performansı düşer.

### B2.4 Toplam ve parazit sürükleme türleri
**Parazit sürükleme (sıfır taşıma sürüklemesi)** taşıma üretmeyen yüzeylerden (gövde, iniş takımı, antenler, motor gondolları) doğar ve üç bileşene ayrılır:

| Tür | Nedeni |
|---|---|
| Şekil/basınç sürüklemesi (form drag) | Cismin biçimi; akışın yüzeyden ayrılıp arkada türbülans yaratması ve hücum-firar kenarı basınç farkı. Akış yüzeyden ne kadar erken ayrılırsa o kadar büyük. |
| Girişim sürüklemesi (interference drag) | Kanat–gövde gibi kesişim bölgelerinde bir bileşenin akışının diğerini engellemesi. Hız arttıkça artar; konfigürasyon değişimi etkiler. |
| Yüzey sürtünme sürüklemesi (skin friction drag) | Yüzeyle hava molekülleri arasındaki sürtünme; yüzey pürüzlülüğü, viskozite, kirlenme ve doku etkiler. Laminer sınır tabaka → geçiş noktası → türbülanslı sınır tabaka. |

**Toplam sürükleme = parazit + indüklenmiş sürükleme.**
- Düşük hızlarda indüklenmiş sürükleme baskındır; hız arttıkça azalır, parazit sürükleme (∝ V²) artar.
- Toplam sürükleme hız arttıkça önce azalır, sonra artar. **Parazit ve indüklenmiş sürüklemenin eşit olduğu hızda toplam sürükleme minimumdur (Vmd)** — "minimum sürükleme hızı", L/Dmax'a karşılık gelir; optimum hücum açısı yaklaşık 4°'dir.
- Bu hızda kanat minimum sürükleme için maksimum taşıma üretir ("ekonomik/en verimli hız").
- Doğru sürükleme yönetimi yakıt ekonomisi ve performans için kritiktir.

### B2.5 Stall, stall hızı ve özel fenomenler
**Stall:** Taşımanın uçağın ağırlığını taşıyamayacak kadar azalması. Hücum açısı **kritik hücum açısını** (tipik olarak yaklaşık 15°) aştığında olur. (*Ders metninde:* B2.1'de aynı açı yaklaşık 16° olarak geçer.)
Normal uçuşta üst yüzeyde hız artar/basınç düşer, alt yüzeyde hız azalır/basınç artar. Kritik AOA'ya yaklaşırken üst yüzeyde akış yavaşlar, basınç artar ve **akım ayrılması (separation)** olur → taşıma düşer, uçak düşmeye başlar. Düşük irtifada pilota çok az tepki süresi bırakır; stall manevraları eğitimde tanıma ve doğru tepki için zorunludur.

#### Stall hızını etkileyenler
| Faktör | Etki |
|---|---|
| Kanat şekli | Daha geniş ve düz kanatlarda stall hızı daha yüksek. |
| Ağırlık | Ağır uçakta stall hızı daha yüksek. |
| CG konumu | CG ileri → burun aşağı moment artar, kuyrukta daha fazla negatif kuvvet gerekir, toplam taşıma ihtiyacı artar → **stall hızı yükselir**. |
| Hava koşulları | Düşük sıcaklık ve yüksek irtifada yoğunluk azalır → TAS cinsinden stall hızı yüksek. IAS cinsinden düşük irtifada etkilenmez; yüksek irtifada Mach/sıkışabilirlik etkisi stall hızını artırır. |
| Diğer | Kanat yüklemesi (W/S), yüzey sürtünmesi. |

Stall hızı en düşük kalkış/iniş, tırmanma ve seyir hızlarını belirler; minimum güvenli hızlar buna referansla tespit edilir. Pilot stall hızının altında uçmaktan kaçınmalıdır.

**Kanat uzunlamasına (kısmi) stall:** Kanadın yalnızca bir kısmının stall'a girmesi; kritik AOA tüm kanatta aynı anda aşılmaz. En yaygın nedeni kanatlara eşit olmayan yük dağılımıdır. Önlemi: eşit yük dağılımı, stall hızına yakın uçarken AOA'nın titizlikle kontrolü, doğru motor yönetimi ve koordineli kumanda.

#### Stall uyarısı
Uyarı sistemleri AOA ve hızı sürekli izler; AOA kritik değere yaklaşınca veya hız stall hızının altına düşünce devreye girer.
- **Stall uyarı lambası:** Kokpitte yanar.
- **Stall uyarı sesi:** Karakteristik ses sinyali.
- **Lövye titretici (stick shaker):** Kumandayı titreterek fiziksel uyarı verir.
- **Lövye itici (stick pusher):** Bazı uçaklarda kontrol kolunu ileri iterek burnu otomatik aşağı indirir.
Küçük uçaklarda basit lamba/sesli ikaz, büyük yolcu uçaklarında çoklu sensörlü otomatik sistemler bulunur. Sistem bileşenleri: hücum açısı probu, kanatçık (vane), flap konum vericisi, karıştırıcı ünite, kumanda sarsıcı motoru.

#### Stall'ın özel belirtileri
- **Akım ayrılması:** Kritik AOA'da üst yüzey akışının yüzeyden kopması.
- **Titreme (buffet):** Stall'a yaklaşırken kanattan ayrılan dağınık akış yatay kuyruğa gider; kuyruğun burun yukarı momentinde sık ve şiddetli dalgalanma yaratır, uçak belirgin titrer.
- **Burnun aşağı düşmesi:** Stall'a girerken taşımanın azalmasının doğal sonucu.
Bu belirtiler pilotun stall'ı erken fark etmesine yardım eder; uyarı sistemleri etkin kullanılmalıdır.

## BÖLÜM 3 · Kaldırma Artırımı, Sınır Tabaka, Özel Durumlar

### B3.1 CL artırımı, sınır tabaka ve kirlenme
CL, hücum açısıyla artar; kritik AOA'ya ulaşınca düşmeye başlar. **CL'yi artırmak** stall hızını düşürür, uçağın daha düşük hızda uçmasına ve manevra kabiliyetine yardım eder. Yöntemler: firar kenarına hareketli yüzey (flap), hücum kenarına yardımcı yüzey eklemek ve kanat profilini seçmek.

- **Kanat profilinin değiştirilmesi:** Üst yüzey daha eğimli/kamburluklu (venturi etkisini artırmak için), alt yüzey daha az kamburluklu veya düz yapılırsa CL artar. Kalın ve çok kamburluklu profiller yüksek CL verir ama **kritik Mach sayısı düşük** ve sürükleme yüksektir; bu yüzden yüksek hızlı uçaklarda tercih edilmez. Yüksek kritik Mach sayısı (şok dalgasız ya da zayıf şoklu uçuş) için havanın kanat çevresinde çok hızlandırılmaması gerekir: yolcu ve özellikle savaş uçaklarında **daha az kamburluklu, ince profiller** kullanılır.
- **Sınır tabaka:** Katı yüzeye yaklaşan havanın viskozite nedeniyle yüzeye yapıştığı ince tabaka. Profil şekli sınır tabakanın kalınlığını ve davranışını belirler; performansı etkileyen önemli bir faktördür.
- **Buz ve kirlenme:** Buzlanma en yaygın kirlenme türüdür (kanat, kuyruk ve diğer yüzeylerde). Kırağı, kar, yağmur, kuş pisliği, toz da yüzeyi pürüzlendirir; **taşımayı azaltır, sürüklemeyi artırır**, kontrolü zorlaştırır ve stall'a neden olabilir.
- **Önlemler:** Anti-icing / de-icing sistemleri (kimyasal püskürtme), ısıtma sistemleri, buz tutmayı zorlaştıran dış yüzey tasarımı ve pilotun yüzeyi düzenli kontrolü.

### B3.2 Kaldırma artırıcı cihazlar (flap ve slat)
Düşük hızlarda daha fazla kaldırma sağlayan, özellikle kalkış-iniş için kullanılan hareketli yüzeyler. **Arka kenar cihazları = flap; ön kenar cihazları = slat / leading-edge device.** Bazı uçaklarda sabit ön kenar açıklıkları (**slot**) aynı işi görür.

| Cihaz | Görevi |
|---|---|
| Flap (arka kenar) | Kanadın eğriliğini ve yüzey alanını artırır; efektif hücum açısı artar, **stall hızı düşer**. Kalkışta taşımayı artırıp daha kısa pistten kalkış sağlar; inişte taşıma ve sürüklemeyi artırıp daha düşük hızla inişe, kısa iniş mesafesine izin verir. |
| Slat / Krueger (ön kenar) | Kanadın ön kenarında açılır; akımın üst yüzeyden ayrılmadan ilerlemesini sağlar, daha yüksek AOA'da bile akımın yapışık kalmasına yardım eder. Kalkış ve inişte taşımayı artırır. |
| Flaperon | Arka kenarda, aviyonikle gerektiğinde flap gerektiğinde kanatçık (aileron) olarak çalışan yüzey. |

**Flap tipleri:** plain, split, slotted ve **fowler** (hem geri kayar hem aşağı iner; kanat alanını ve eğriliğini artırır — en etkili alan artırıcı tip).

## BÖLÜM 4 · Düz Yatay Uçuşta Denge ve Stabilite

### B4.1 Statik stabilite ve denge prensipleri
Statik kararlılığın ön koşulu, düzgün uçuşta küçük bir bozunumdan sonra uçağın **kendiliğinden dengeye dönme** yeteneğidir. Bu; CG, taşıma (L) ve aerodinamik merkez (AC) konumları arasındaki ilişkiye dayanır. Kanatların konumu/boyutu/şekli, kuyruk yüzeylerinin boyutu ve konumu, ağırlık dağılımı kararlılığı etkiler.

- **Kural:** CG, aerodinamik merkezin (**neutral point, NP**) **önünde** olmalıdır. CG NP'nin arkasındaysa, burun aşağı bir bozunumdan sonra uçak daha da aşağı eğilir; pilot sürekli düzeltmek zorunda kalır, uçuş tehlikeli olur.
- **Denge:** Düz uçuşta ağırlık merkezi, taşıma merkezi ve sürükleme merkezi aynı eksendedir. Denge üç eksende incelenir:

| Denge | Eksen | Önlediği hareket |
|---|---|---|
| Boylamsal (longitudinal) | Yanal (yatay) eksen | Burnun aşağı/yukarı (pitch) hareketi |
| Yanal (lateral) | Boylamsal eksen | Sağa/sola yatış (roll) |
| Yönsel (directional) | Dikey eksen | Sağa/sola sapma (yaw) |

| CG konumu | Statik boylamsal kararlılık |
|---|---|
| NP'nin önünde | Pozitif |
| NP'de | Nötr |
| NP'nin arkasında | Negatif |

> Ders metninde: Boylamsal dengenin "yatay eksen etrafında" ve "burun aşağı veya yukarı **yuvarlanma**" diye anlatıldığı yer var; pitch hareketi yanal eksen etrafındadır, "yuvarlanma" roll'dür. Doğru eşleşme: pitch = yanal eksen, roll = boylamsal eksen, yaw = normal (dikey) eksen.

**Dengeyi sağlayan öğeler:** Kanat tasarımı (şekil ve boyut taşıma merkezini belirler), ağırlık merkezinin konumu, kuyruk yüzeyleri. Yatay dengeleyici (horizontal stabiliser) burun aşağı/yukarı bozunumlarda ters yönlü moment üretip toparlama sağlar.

### B4.2 Kanat, kuyruk ve kontrol yüzeyleri
Kontrol yüzeyleri uçağın hareketlerini kontrol eden hareketli yüzeylerdir; temel üçü:

| Yüzey | Yeri | Görevi |
|---|---|---|
| Kanatçık (aileron) | Kanat uçlarına yakın | Yuvarlanmayı (roll) kontrol eder. |
| İrtifa dümeni (elevator) | Yatay kuyruğun arkası | Yunuslamayı (pitch) kontrol eder. Kolu çekince elevator yukarı döner → yatay kuyruk daha çok negatif (aşağı) kuvvet → daha fazla burun yukarı moment, uçak irtifa kazanır. Kolu itince tersi. |
| Yön dümeni (rudder) | Dikey kuyruğun arkası | Sapmayı (yaw) kontrol eder. |

> Ders metninde: İrtifa dümeni "yatış açısını" kontrol eder diye yazılmış, doğrusu **yunuslama (pitch)**; yön dümeni ve kanatçık için "ters yönde hareket" ifadeleri de belirsizdir. Pedal/lövye karşılıkları için B5'e bakın.

**Flap, slat, spoiler:** Flap arka kenardadır, kamburluğu artırıp stall hızını düşürür, iniş-kalkışta kullanılır. Slat ön kenarda taşımayı artıran yüzeydir (*ders metninde "hızı düşürmeye yardım eder" diye geçer; asıl işlevi stall hızını/AOA sınırını iyileştirmektir*). **Spoiler** kanat (veya kuyruk) üstünde taşımayı azaltan yüzeydir: yaklaşmada az açılarak hız keser, **teker koyduktan sonra tam açılarak** sürüklemeyi artırır ve durmayı kolaylaştırır.

### B4.3 Balast, ağırlık dağılımı, trim ve kararlılık türleri
**Ağırlık ayarı / balast:** CG konumunu değiştirmek için ağırlık eklemek-çıkarmak veya ağırlığı yeniden dağıtmak (ör. yakıt tanklarının konumu). Nedenleri: uçağın belirli bir CG gereksinimini karşılamak, performansı ve dengeyi iyileştirmek. CG optimum yerin gerisindeyse uçak gerektiğinden az kararlı olur. (Şekilde: neutral point ile CG arasındaki mesafe **statik pay**.)

#### Statik ve dinamik boylamsal kararlılık
- **Statik:** Küçük bir bozunumdan sonra uçağın **kendiliğinden dengeye dönme eğilimi**; ön koşul CG'nin NP önünde olması. Burun yukarı bozunumda AOA artar, kanat ve kuyruktaki ek taşımaların CG etrafındaki net momenti toparlayıcı olur.
- **Dinamik:** Bozunumdan sonra salınımların **sönüp sönmediği**.

| Dinamik kararlılık | Salınım |
|---|---|
| Pozitif | Azalarak yok olur. |
| Nötr | Sabit genlikte kalır; kontrol girdisi olmadan düz uçuşa dönmez (ideal değil). |
| Negatif | Artar, kontrol edilemez hale gelebilir (çok tehlikeli). |

#### Yatış ve yön kararlılığı
- **Statik yön kararlılığı:** Sapma bozunumundan sonra kendiliğinden düzgün yola dönme; **dikey kuyruk (dikey stabilize)** sağlar. Pozitifte dönüş vardır; nötrde sapma açısında kalır; negatifte sapma artar (tasarımda önlenir).
- **Statik yatış (yanal) kararlılığı:** Yuvarlanma bozunumundan sonra kendiliğinden yatay konuma dönme; **kanatların dihedral açısı** pozitif yanal kararlılığa katkı yapar.
- Dinamik yön ve yatış kararlılığı da salınımların sönmesine (pozitif), sabit kalmasına (nötr), artmasına (negatif) göre sınıflanır. Negatif dinamik yatış kararlılığı spiral dalışa götürür.

#### Dutch roll ve spiral dalış
| Bozunum | Ne zaman | Düzeltme |
|---|---|---|
| **Dutch roll** | Dinamik yatış kararlılığı **aşırı**, dinamik yön kararlılığı **zayıf** | Pilotun düzeltme girişimi bozunumu artırabilir; **yaw damper** ile sönümlenir. Yaw damper yoksa/arızalıysa hız ve irtifa azaltılır. |
| **Spiral dive** | Dinamik yatış kararlılığı **zayıf**, dinamik yön kararlılığı **aşırı** | Küçük yuvarlanma ve sapmada güçlü yön kararlılığı uçağı hizaya sokmaya çalışır ama zayıf yanal kararlılık yatışı düzeltemez; dış kanat daha çok hız ve taşıma kazanır, yatış artar, uçak spiral dalışa girer. Çıkış: gücü rölantiye almak, aileronları nötre getirmek (aileron spirali artırabilir), yön dümeniyle ters yuvarlanma başlatmak ve sonra düzeltmek; irtifa dümenini aşağı çevirerek stall'dan çıkmak. |

## BÖLÜM 5 · Kontrol

### B5.1 Uçuş kontrolünün temelleri ve yunuslama kontrolü
Uçak, ağırlık merkezinden geçen ve birbirine dik **üç eksen** etrafında hareket eder:

| Eksen | Hareket | Kontrol yüzeyi |
|---|---|---|
| Boylamsal (uzunlamasına) | Yuvarlanma (roll) | Kanatçık |
| Yanal | Yunuslama (pitch) | İrtifa dümeni |
| Normal (dikey) | Sapma (yaw) | Yön dümeni |

- **Hücum açısı:** Kordo hattı ile göreceli hava akışı arasındaki açı. Hava yüzeye tutunduğu sürece AOA büyüdükçe taşıma artar; kritik değer aşılırsa akış ayrılır, taşıma kaybolur, stall olur. Pilot AOA'yı kontrol altında tutmalıdır.
- **Pitch kontrolü:** Yatay stabilizeye monte irtifa dümeni, lövyeye bağlıdır. Lövye ileri → elevator aşağı → kuyrukta yukarı yönlü kuvvet → **burun aşağı**. Lövye geri → elevator yukarı → **burun yukarı**.
- **Downwash etkisi:** Kanattan aşağı yönlenen akış yatay stabilize üzerinde kuvvet yaratır ve taşımanın CG etrafında oluşturduğu momenti dengeler; elevator bu kuvveti artırıp azaltarak yunuslama momenti üretir.
- **CG konumunun etkisi:** CG limitleri üretici tarafından belirlenir; yüklemede kontrol edilmelidir (yakıt tüketimi, yolcu/mürettebat yer değiştirmesi, iniş takımı hareketi CG'yi kaydırır; etkiler trimle düzeltilir). 
  - CG **ilerideyse** burun aşağı eğilim, kararlılık yüksek, kontrol kabiliyeti düşük (pitch için daha çok kuvvet gerekir).
  - CG **gerideyse** burun yukarı eğilim, kararlılık düşük, kontrol kabiliyeti yüksek.

### B5.2 Yuvarlanma ve sapma kontrolü
- **Yuvarlanma (roll):** Lövye sola yatırılınca sol kanatçık yukarı (taşıma azalır), sağ kanatçık aşağı (taşıma artar) → uçak sola yatar; sağa için tersi.
- **Ters sapma (adverse yaw):** Uçağın dönmek istediği yönün tersine sapma eğilimi. Dönüşte dış kanat daha fazla taşıma ve sürükleme üretir; sürükleme farkı burnu dönüş yönünün tersine çevirir. Pilot rudder ile dengeler.
- **Ters sapmayı önleme yöntemleri:**
  - **Differential aileron:** Yukarı giden kanatçık daha büyük, aşağı giden daha küçük açıyla hareket eder.
  - **Frise aileron:** Yukarı giden kanatçık alt kenarını hava akımına sokup ekstra sürükleme yaratır.
  - **Roll control spoiler:** Dönüşte taşımayı azaltır, sürükleme ekler.
  - **Aileron–rudder coupling:** Kanatçık hareketiyle rudder senkron çalışır.
- **Kontrol kuvvetlerini azaltma (aerodynamic balance):** Kontrol yüzeyi menteşeyle bağlıdır; manuel kontrolde yüzey sapınca oluşan aerodinamik kuvvet yüzeyin açısını küçültecek **menteşe momenti (hinge moment)** üretir ve pilotun kuvvetini artırır. Menteşe momentini azaltan yöntemler: **horn balance, inset hinge, internal balance, balance tab**.
- **Sapma (yaw) kontrolü:** Dikey eksen etrafında dönme, rudder ile kontrol edilir. Sağ pedal → burun sağa, sol pedal → burun sola. Ters sapma rudder ile karşılanmazsa uçak koordinasyonsuz dönüşe girer; bu yüzden dönüşlerde aileron ve rudder uyumlu kullanılır.

### B5.3 Kütle dengesi, ikincil kontrol yüzeyleri ve trim
- **Flutter:** Kontrol yüzeyinin ağırlığı ve üzerindeki aerodinamik kuvvetin yüzeyde yarattığı burulma/bükülme momentlerinin neden olduğu **salınımlar**. Önlenmezse genliği artar ve yüzeyde yapısal hasara yol açar.
- **Control mass balance:** Salınımı önlemek ya da daha yüksek hızlara ötelemek için yüzeyin **ağırlık merkezini menteşeye yaklaştırmak** (burulma etkisini, dolayısıyla flutter riskini azaltır).

#### İkincil kontrol yüzeyleri (yüksek taşıma araçları)
Düşük hızlarda taşıma katsayısını artırır; kalkış ve iniş fazlarında kullanılır. **Hücum kenarı flapları kritik hücum açısını artırır; firar kenarı flapları kamburluğu artırıp taşıma katsayısını yükseltir.** Hafif uçaklarda genelde **plain**, nakliye uçaklarında hem CL'yi hem yüzey alanını artırdığı için **fowler** flap kullanılır.
- **Düşük flap derecelerinde** taşıma, sürüklemeye göre daha çok artar → kalkışta düşük flap.
- **Yüksek flap derecelerinde** sürükleme taşımadan daha çok artar → inişte yüksek flap.

| Flap | Çalışması | Artı | Eksi |
|---|---|---|---|
| Fowler | Hem aşağı döner hem arkaya kayar; kanat alanını artırır. Büyük yolcu uçakları. | En yüksek kaldırma, çok düşük stall hızı | Mekanik karmaşıklık, bakım maliyeti, ağırlık |
| Slotted | Kanat ile flap arasında boşluk; geçen hava akışı kaldırmayı artırır. Ticari ve orta ölçekli uçaklar. | Akışı düzenler, verimli L/D | Karmaşık mekanizma, bakım maliyeti |
| Split | Kanadın alt yüzeyinden ayrılarak açılır; çok sürükleme. Askeri ve kısa iniş-kalkış uçakları. | İnişte yüksek sürükleme gereken yerde etkili, basit ve güvenilir | Yakıt verimini düşürür, L/D düşük |
| Plain | Basit menteşeli arka kenar flabı; kamburluğu artırır. Küçük eğitim ve eski uçaklar. | Basit, ucuz, dayanıklı | Sürüklemeyi çok artırır, L/D düşük |

#### Trim
Trim, pilotun lövyeye uygulaması gereken kuvveti azaltır; uçağı sürekli kumanda uygulamadan istenen konumda tutar, yorgunluğu azaltır ve yakıt verimini korur (trimsiz uçakta sürekli kontrol gerekir). Kontrol yüzeyinin arkasındaki küçük **flettner (trim) tab** ile yapılır:
- **Sabit trim tab:** Aileron ve rudder'da; **yerde** ayarlanır, yalnızca yetkili mühendis/teknisyen yapabilir.
- **Ayarlanabilir trim tab:** Elevatörde; uçuşta pilotun **trim tekerleğiyle** kontrol edilir.
- **Rudder trim:** Yan rüzgâr veya motor asimetrisinde sapma momentini düzeltir. **Aileron trim:** Uzun süreli yuvarlanma eğilimini dengeler.
- Mekanik, elektrikli veya hidrolik sistemlerle ayarlanır; otomatik uçuşta **autotrim** elektronik ayar yapar.
- Kütle dengesinin yanlış ayarı kontrol yüzeylerinde gecikmeli tepki veya aşırı hassasiyet doğurabilir.

## BÖLÜM 6 · Sınırlamalar

### B6.1 İşletme sınırlamaları (hızlar)
Flutter ve control mass balance için B5.3'e bakın. Yapısal bütünlüğü korumak için tanımlı hız sınırları:

| Hız | Anlamı |
|---|---|
| **Vfe** | Flapların açık halde kullanılabileceği **maksimum güvenli hız** (maksimum flap açma sürati). Flap derecesine göre sınırlanır: **düşük flap (take-off) için yüksek, yüksek flap (landing) için düşük değer.** |
| **Vs0** | **İniş konfigürasyonundaki** (tam flap) stall hızı. |
| **Vs1** | **Temiz konfigürasyon** (flaplar toplu) stall hızı. |
| **Vno** | **Maksimum normal operasyon hızı.** Üzerinde, özellikle hamleli rüzgârda yapısal hasar riski vardır. |
| **Vne** | **Asla aşılmaması gereken hız**; maksimum operasyon hızı. |

**Hız göstergesi renk işaretleri (analog):**

| İşaret | Aralık |
|---|---|
| **Beyaz yay** | Flapların çalıştırılabileceği aralık: alt limit **Vs0**, üst limit **Vfe** (iniş konfigürasyonu). |
| **Yeşil yay** | Normal operasyon: alt limit **Vs1**, üst limit **Vno**. |
| **Sarı yay** | Dikkat aralığı (caution range): alt limit **Vno**, üst limit **Vne**. |
| **Kırmızı çizgi** | **Vne** — asla aşılmayacak hız. |

### B6.2 Manevra limitleri (manoeuvring envelope)
**Manoeuvring envelope (V–n diyagramı / manevra zarfı)**, uçağın belirli uçuş koşullarında güvenle manevra yapabileceği sınırları tanımlar; hız (EAS) ve **yük faktörü (n)** eksenlerinde grafik/tablo olarak gösterilir. Aerodinamik performans, yükseklik, hız ve ağırlıkla etkileşir. Diyagramda **pozitif ve negatif limit yük faktörü**, **nihai yük faktörü**, **kalıcı yapısal deformasyon** ve **yapısal arıza** bölgeleri ile Vs1g ve Va (manevra hızı) noktaları bulunur.

- **Kritik manevra durumları:** Sınırların zorlandığı/aşıldığı durumlar — yüksek hız, düşük irtifa, ani manevralar. Stratejiler: hız kontrolü (maksimum hız sınırlarını aşmamak), irtifa yönetimi (düşük irtifada ani irtifa kaybını önlemek), ani manevrada hassas ve hızlı kontrol.
- **Uçak türüne göre zarflar:** Yüksek performanslı savaş uçaklarında yüksek hız ve yüksek g; yolcu uçaklarında yüksek irtifa, düşük hız, uzun menzil; helikopterlerde düşük hız/irtifada manevra; İHA'larda göreve göre optimize.
- **Pilot eğitimi ve güvenlik:** Pilotlar zarfın temel prensiplerini öğrenir; sertifikasyonda uçak belirli zarf kriterlerini karşılamadan onaylanamaz; zarfa uyumla ilgili olaylar güvenlik standartlarını iyileştirir.

#### Manevra yük diyagramı (MLD)
Uçağın güvenle manevra yapabileceği sınırları gösteren grafik (EAS – yük faktörü; Vs1g ve Va noktaları). Bileşenleri: **limit manevra yük faktörü (n_lim)** — aerodinamik ve yapısal sınırların birleşimi, uçağın maksimum dayanma faktörü; **kritik motor kaybı manevra yük faktörü (n_eng-out)** — özellikle tek motorlu uçaklarda önemli; **pozitif manevra yük faktörü (n_pos)**. MLD'nin pilot eğitiminde rolü: manevra güvenliği, simülasyon ve eğitim uçuşları; güvenlikte rolü: sertifikasyon ve olay analizi.

#### Kütlenin etkisi
Kütle (yakıt, ekipman, yük toplamı) menzili, hızı, manevra kabiliyetini ve taşıma kapasitesini belirler; kütle arttıkça menzil ve yakıt verimi düşer. MLD'de kütle, **limit manevra yük faktörlerini ve diğer kritik noktaları etkiler**; ders notuna göre **kütle arttıkça limit manevra yük faktörleri artar** (daha ağır uçak daha yüksek limit manevra yük faktörlerine dayanabilir). Ağır uçak daha yavaş tepki verir, manevra kabiliyeti düşer; özellikle düşük hızlarda dikkat gerekir. Kütle merkezi denge ve stabiliteyi kritik biçimde etkiler; hafif malzemeler, tasarım yenilikleri ve elektrikli hava ulaşımı kütle azaltımına katkı verir.

### B6.3 Rüzgâr limitleri (gust envelope)
**Gust envelope / Gust Load Diagram (GLD):** Uçağın belirli rüzgâr (gust) koşullarında nasıl tepki vereceğini gösteren grafik; aerodinamik sınırlar ve yapısal dayanıklılığı değerlendirmek için kullanılır. **Pozitif gust** uçağın ani yükselişine ve akım dalgalanmasına, **negatif gust** ani düşüşe yol açar. Diyagramda hız (V), Va (manevra hızı), Vno, Vne, pozitif/negatif limit yük faktörü yer alır. Etkileyenler: yapısal özellikler, aerodinamik tasarım, ağırlık ve dağılımı, pilotun kontrolü, rüzgârın hızı/yönü/dalgalanması, uçuş hızı ve irtifa. Gust envelope tasarımda ve sertifikasyonda kullanılır.

| | MLD (Manevra yük diyagramı) | GLD (Rüzgâr yük diyagramı) |
|---|---|---|
| Neyi gösterir | Güvenli manevra sınırları, limit manevra yük faktörleri | Rüzgâr değişimlerine tepki; rüzgârın yarattığı dinamik yükler |
| Odak | Uçağın kendi ağırlığı ve manevra yükleri | Rüzgârın neden olduğu dinamik yüklemeler (gust yük faktörleri) |
| Kullanım | Pilot eğitimi, sertifikasyon | Tasarım ve sertifikasyonda dayanıklılık değerlendirmesi |

## BÖLÜM 7 · Pervaneler

### B7.1 Hatve ve pervane çeşitleri
**Hatve (pitch) = pal/bıçak açısı (blade angle).** Bıçağın hücum açısı (blade AOA) TAS ve RPM'e bağlıdır: **sabit TAS'ta RPM artarsa blade AOA artar; sabit RPM'de TAS artarsa blade AOA azalır.**

| Tür | Özellik |
|---|---|
| **Fine pitch (küçük hatve açısı)** | Düşük hızlarda (kalkış, tırmanış) verimli; pervane havayı daha hızlı "ısırır", uçak kısa mesafede kalkar, dik tırmanır. İnce hatve = tırmanma pervanesi. |
| **Coarse pitch (büyük hatve açısı)** | Yüksek hızlarda (seyir) verimli; uygun hücum açısını koruyup az sürtünmeyle gücü itkiye çevirir, yakıt tüketimini azaltır, menzili artırır. Kalın hatve = seyir pervanesi. |
| **Sabit hatveli** | Yalnızca **bir TAS değerinde** verimli. |
| **Değişken hatveli (constant speed)** | Bıçak AOA'sı optimum tutulur; daha geniş hız aralığında verimli, daha az sürtünme ve yakıt tüketimi. |

Pervane verimliliği T/O, tırmanma ve seyirde farklı hatvelerde farklı TAS'ta tepe yapar; bu yüzden değişken hatve avantaj sağlar. Pal profili düşük direnç ve yüksek itki vermelidir; pervaneler alaşımlı metal, kompozit veya ahşaptan yapılır (hafiflik, dayanıklılık, maliyet).

### B7.2 İtki üretimi, pitch ve pal bükümü
**Motor torkunun itkiye dönüşmesi:** İçten yanmalı motorda yakıtın yanması pistonları döndürür; tork genelde dişli kutusuyla pervaneye iletilir (motorun yüksek devri pervanenin daha düşük devrine uyarlanır). Pervane dönen hareketle hava akımının hızını ve yönünü değiştirir; **Newton'un üçüncü yasasına göre** eşit ve zıt **itki (thrust)** doğar. İtki, palin havayı geriye itmesiyle oluşur. Pervane açı ayarı, uçağın hızını ve performansını kontrol etmede önemlidir; motor hızı pilot veya otomatik sistemlerle düzenlenir. Jet motorlarda hızlı hava çıkışı ve **itme vektörü kontrolü** kullanılır.

**Pitch ölçümü (uçak):** Pitch, yanal eksen etrafında burnun yukarı/aşağı hareketidir; yatay stabilize ve elevatör kontrol eder. Pitch açısı, ufuk çizgisi ile uçak ekseni arasındaki açıdır; uçuş yolu açısı ve hücum açısından farklıdır (*pitch açısı = uçuş yolu açısı + hücum açısı*, sakin havada). Pitch kontrolü stabilite ve irtifa değişimi için kritiktir; modern uçaklarda otopilot yapar.

> Ders metninde: "Pitch'in uçuş performansına etkisi" slaytında pitch'in "uçağın yatay düzlemde hareket etmesini sağladığı" söylenir; pitch hareketi dikey düzlemdedir (burun yukarı-aşağı).

**Blade twist (pal bükümü):** Pervanenin kökten uca değişen açısal eğimi; hava akımıyla etkileşimde optimum performans için tasarlanır. Amaç **aerodinamik verimliliği artırmak**: direnç ve itme dengesini optimize eder, itmeyi pal boyunca homojen dağıtır, stabiliteyi ve kontrolü iyileştirir; ayarlanabilir twist farklı hız ve irtifalara uyum sağlar.

> Ders metninde: "geniş pal kökü genellikle daha düşük eğime, uç kısım daha fazla eğime sahiptir" yazılıdır. Genel kural bunun tersidir: pal açısı kökte büyük, uca doğru küçüktür (uç daha hızlı döndüğü için). Soru bankasında yalnızca blade twist'in *amacı* sorulur (aerodinamik verim).

### B7.3 Motor arızası ve windmilling
- **Motor arızasının nedenleri:** Yakıt yetersizliği (sistem arızası, planlama hatası, kontaminasyon); mekanik arızalar (piston, silindir, krank mili — aşınma, imalat hatası, bakım eksikliği); ateşleme sistemi sorunları (kirli bujiler, manyeto, zamanlama); yağ sistemi problemleri (yetersiz yağlama, sızıntı, pompa arızası, kontaminasyon).
- **Etkileri:** Anında itki kaybı (irtifa ve hız koruyamama), manevra kabiliyetinde azalma (özellikle kalkış-inişte), titreşim ve anormal ses.
- **Pilot önceliği:** Uçağın kontrolünü elinde tutmak (aviate), uygun iniş sahası seçmek (navigate), acil durumu bildirmek (communicate). Acil durum kontrol listeleri, sorun giderme (yakıt kontrolü, motoru yeniden başlatma, ateşleme), zorunlu iniş prosedürü, ATC'ye acil durum ilanı.
- **Yel değirmeni sürüklemesi (windmilling drag):** Motor devre dışı kalınca pervanenin rüzgârla dönmesi ve bunun yarattığı dirençtir. Normalde itki üreten pervane **direnç** üretir; uçak yavaşlar ve itme tersine dönebilir (kontrol zorluğu, performans düşüşü). Otorotasyonda iniş açısını ve hızı etkiler; pilot motoru yeniden başlatma girişimleriyle windmilling drag'i azaltmaya çalışır. Havada kalış süresini kısaltır, yakıt ekonomisini bozar; modern sistemler ve yeni pervane tasarımları windmilling drag'i azaltmayı hedefler.

### B7.4 Pervanenin yarattığı momentler
Pervane çalışması uçakta dönme momentleri doğurur. Aerodinamik moment kaynakları: **diferansiyel itme** ile **P-faktör (güç etkisi)**. Diferansiyel itme yan (lateral) stabiliteyi etkileyebilir; P-faktör yaw hareketini etkiler. İtme ileri hareket, yuvarlanma momenti (rolling moment) yatma hareketi doğurur; pervane pitch momentini de etkiler. Pilotlar bu momentleri yönetmeyi öğrenir; ayarlanabilir pervane tasarımları ve otomatik pervane kontrolü iş yükünü azaltır.

| Etki | Ne | Yönetim |
|---|---|---|
| **Tork reaksiyonu (torque reaction)** | Pervanenin dönmesine karşılık, motorun gövde (karoser) üzerinde oluşturduğu **zıt yönlü tork**; uçağı dönüş yönünün tersine yatırmaya eğilimli. Tek motorlu uçakta daha belirgin; dönüş ve manevralarda artabilir. | Düz uçuşta **kontrol yüzeyleriyle** (aileron, yatay stabilize) dengelenir. **Ters yönde dönen pervaneler** etkiyi ortadan kaldırır; çok motorlu uçakta motorların torkları birbirini dengeleyebilir. |
| **Asimetrik kayma etkisi (asymmetric slipstream)** | Pervanenin döndürdüğü helisel kayma akımının **kuyruk bölgesine** (dikey/yatay stabilize) çarpması; uçağı sağa veya sola savurur (yawing). Düz uçuşta ve minimum güçte daha az belirgindir; dönüş ve manevralarda artabilir. Güç artınca slipstream artar: **pervanesi saat yönünde dönen uçak güç artışında sola yaw yapar**, güç azalınca sağa. | Kontrol yüzeyleri (rudder) ile dengelenir. |
| **Asimetrik pal etkisi (asymmetric blade effect, P-faktör)** | Pervane diskinin farklı bölgelerindeki palların farklı aerodinamik etkisi; **düşük hızlarda, özellikle iniş ve kalkışta** belirginleşir; yawing momentini artırır. | Ayarlanabilir pervane tasarımları, otomatik sistemler; kontrol yüzeyleriyle dengelenir. Çok motorlu uçaklarda motorlar etkiyi biraz dengeler. |

*Ek bilgi (ders metninde yok):* P-faktörde pervane ekseni hava akımıyla açı yaparsa (yüksek burun açısı, düşük hız, yüksek güç) alçalan palın hücum açısı ve itkisi yükselen paldan büyük olur; sapma momenti buradan doğar.

## BÖLÜM 8 · Uçuş Mekaniği

### B8.1 Uçağa etki eden kuvvetler ve uçuş durumları
Dört temel kuvvet: **ağırlık, taşıma, itki, sürükleme**.

| Kuvvet | Özellik |
|---|---|
| Ağırlık (W) | Kütle × yerçekimi ivmesi; **CG'den** aşağı etki eder. Yakıt tüketimi veya kargo düzeni CG'yi az da olsa değiştirir. |
| Sürükleme (D) | İleri harekete karşı hava direnci; uçuş yönünün tersine. Hız arttıkça genelde artar (özellikle parazit). |
| İtki (T) | Hareket yönünde ileri doğru hızlanma/hız koruma sağlayan kuvvet; motor ekseninden etki eder. Hız ve tırmanma kabiliyeti itkiye bağlıdır. |
| Taşıma (L) | Kanat üzerinde Bernoulli ve basınç farklarıyla oluşan yukarı kuvvet; **basınç merkezinden (CP)** etki eder. Profil şekli, AOA ve hava hızına bağlıdır; flap/slat ile kontrol edilir. |

**Beş temel uçuş durumu:** düz yatay istikrarlı uçuş, düz istikrarlı tırmanış, düz istikrarlı alçalış (iniş), düz istikrarlı süzülme, stabil koordineli dönüş.

### B8.2 Düz yatay, tırmanış, alçalış ve süzülme
#### Düz yatay istikrarlı uçuş (straight and level)
Sabit hız ve sabit irtifada düz ilerleme; **L = W, T = D**; kuvvetler ve momentler dengededir (ivme yoktur). Kuvvetler farklı noktalardan etki ettiği için hem kuvvetler hem momentler birbirini sıfırlamalıdır. Düşük hızlarda düz yatay uçuş mümkün değildir (stall); güç-hız eğrisinde **minimum güç hızı** vardır, düşük seyirde ve yüksek seyirde yüksek güç gerekir.
- Sapmayı önlemek için aileronlarla kanatlar düz tutulur, gerekli rudder basıncı uygulanır; uçağın yatmasına izin verilirse alt kanat yönünde dönmeye başlar.
- Güç artarsa slipstream artar → pervanesi saat yönünde dönen uçak **sola yaw** yapar; güç azalınca sağa.
- Sabit irtifa için güç değişince elevator ile pitch tutulur, istenen hıza gelince trimlenir.
- Göstergeler: sabit airspeed, düz attitude, sabit altimetre ve heading, VSI sıfır, koordinatör topu merkezde.
- **Attitude + Power = Performance.** Lift sabit tutulurken hız artınca AOA azaltılır, hız azalınca AOA artırılır (CL hızın karesiyle ters orantılı).

#### Kuvvet çiftleri ve kuyruk
- CG'nin **arkasından** etki eden lift **burun aşağı**, CG'nin **önünden** etki eden lift **burun yukarı** moment yapar.
- Drag çizgisinin **altından** etki eden thrust **burun yukarı**, **üstünden** etki eden thrust **burun aşağı** moment yapar. Çoğu uçakta motor arızasında lift–weight çiftinin toplamı burnu aşağı çevirir ve uçak süzülmeye başlar; güç eklenince burun kalkar, tırmanış başlar.
- **Tailplane:** İstenmeyen pitch momentlerini dengelemek için CG'den uzak, uzun moment koluyla yerleştirilir; bazı uçaklarda konumu ayarlanabilir. Dengeleme kuvveti drag artışına yol açar: **trim drag**.

#### Düz istikrarlı tırmanış
Yatay uçuş için gerekenden fazla itki gücü potansiyel enerjiye dönüşür. Sabit hızda tırmanırken kuvvetler dengelidir (ağırlığın W·sin/W·cos bileşenleri); **thrust daima drag'den büyük, lift daima weight'ten küçüktür**. Tırmanış açısı arttıkça gereken lift azalır, gereken thrust artar.
- **Vx (maksimum tırmanış açısı hızı):** En kısa yatay mesafede en fazla irtifa; nispeten **düşük hızdadır**, engel aşmak için uygundur.
- **Vy (maksimum tırmanış oranı hızı):** **En kısa zamanda** en fazla irtifa; Vx'ten **daha yüksek hızdadır**, açı daha dardır.

#### Düz istikrarlı alçalış
Ağırlığın uçuş yolu boyunca bileşeni itkiyle birlikte uçağı hızlandırır; sabit hava hızı için thrust, drag'e karşı gelene kadar azaltılır. Alçalışta **L < W** ve **T < D** (W·sin(descent) uçuş yolu boyunca).

#### Düz istikrarlı süzülme (itki sıfır)
Motor çalışmıyorsa thrust bileşeni sıfırdır; ağırlığın uçuş yolu boyunca bileşeni drag'i dengeler. **Minimum süzülme açısı → maksimum süzülme mesafesi**; en iyi süzülme **minimum drag hızında** (L/D en yüksek) elde edilir; başka hızda L/D düşer, süzülme açısı artar, mesafe azalır.
- **Kütle yalnızca süzülme hızını ve süresini etkiler**, mesafeyi etkilemez: L/D oranı kütleden bağımsızdır, L ve D aynı oranda artar. (5 tonluk ve 6 tonluk uçak aynı mesafeye süzülür; 6 tonluk daha hızlı gider, havada kalma süresi farklıdır.)
- **Rüzgâr:** Headwind/tailwind yatay hızı (yere göre mesafeyi) etkiler, dikey hızı etkilemediği için **süreyi (duration) etkilemez**.
- En iyi süzülme hızı uçuş el kitabında AUW'ye göre verilir.

### B8.3 Stabil koordineli dönüş
Yatış açısı (bank angle), yük faktörü, dönüş yarıçapı ve dönüş oranı (rate of turn) dikkate alınır. Uçak yatınca toplam lift vektörü yana kayar:
- **Lift'in dikey bileşeni (L·cos φ) ağırlığı taşır:** L·cos φ = W.
- **Lift'in yatay bileşeni (L·sin φ) merkezcil kuvvettir** (centripetal) ve merkezkaç kuvvetini (centrifugal) dengeleyip dönüşü sağlar.
- Toplam lift aynı kalsaydı ağırlığı taşıyan bileşen azalır, hücum açısı artırılmazsa irtifa kaybedilir. Sabit irtifada dönmek için lift, dolayısıyla **yük faktörü ve AOA/thrust artırılmalıdır**; yatış büyüdükçe gereken lift artar.
- **Thrust = drag** (sabit hız ve irtifa için) — ancak bu drag düz uçuştakine eşit değildir (daha büyüktür).
- 45° yatışta dikey ve yatay bileşenler eşittir.
- Lift ihtiyacı arttığı için load factor ve **indüklenmiş sürükleme artar**.

**Yük faktörü (load factor, n):** Lift / Weight; birimi **g**. Koordineli yatışlı dönüşte **n = 1 / cos(yatış açısı)**. Örnek: 60° yatışta n = 2 → uçak 2 g'ye maruz kalır, kütlesi artmasa da ağırlığı iki katına çıkmış gibi olur (toplam lift = 2 × W).

**Dönüş yarıçapı:** TAS ve yatış açısına bağlıdır, **kütleden bağımsızdır** (r = V² / (g·tan φ)). Merkezcil ivme a = V²/r.

**Kanat yüklemesi (wing loading):** AUW / kanat alanı (N/m²). AUW seyir koşullarında uçağın ağırlığıdır, yakıt yanınca değişir. Kanat yüklemesi yüksekse indüklenmiş sürükleme çok yüksek, düşükse çok düşüktür.

**Dönüşte stall hızı:** Stall hızı yük faktörüyle artar: **Vs(dönüş) = Vs(normal) × √n**. Örnek: normal stall hızı 60 kt, 60° yatış (n = 2) → 60 × √2 ≈ 85 kt. Yatışa göre stall hızı artışı: 30° ≈ %7, 45° ≈ %19, 60° ≈ %41.

**Flap ve irtifa etkisi:** Düşük hızlarda veya kötü görüşte dönüş manevrası yaparken flapları kalkış ayarına getirmek avantajlıdır (CL artar, toplam taşıma kapasitesi yükselir). İrtifa arttıkça sabit IAS'ta TAS artar ve itki gücü azalır; bu yüzden herhangi bir yatışta **minimum dönüş yarıçapı artar**, stall hızı üzerindeki marj azalır.

**Dönüş oranı (rate of turn):** Dönüşün ne kadar sürdüğünün ölçüsü, derece/saniye. **Standart dönüş (rate-1) = 3°/s** (180° için 1 dakika, 360° için 2 dakika). Rate-1 yatış açısı, dönüş yarıçapı ve hızla ilişkilidir; sabit yük faktöründe hız arttıkça yarıçap büyür, aynı hızda yatış arttıkça dönüş oranı yükselir.
