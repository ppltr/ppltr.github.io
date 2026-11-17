# 020 zayıf konular çalışma bankası

Kullanıcının 2026-11-17 Uçak Genel Bilgisi sınavında yanlış yapmış olabileceği konuların (altimetre/hPa,
manyeto, elektrik/voltaj, yakıt/100LL, statik elektrik, birimler) bütün bankadan toplanmış sorusu.
Bankadan ayrı, tek dosyalık bir çalışma sayfası: `calisma/020-zayif-konular.html`.

```bash
python3 scripts/zayif_konular/topla.py /tmp/zk.json
python3 scripts/zayif_konular/uret.py /tmp/zk.json calisma/020-zayif-konular.html scripts/zayif_konular/sablon.html
```

`uret.py` içindeki `DROP` konu dışı eşleşmeleri (pitot, kızdırma bujisi, kütle hesabı…) eler, `MOVE` soruyu
doğru konuya taşır. Doğru cevap verideki ilk şıktır; sayfa şıkları karıştırır.
