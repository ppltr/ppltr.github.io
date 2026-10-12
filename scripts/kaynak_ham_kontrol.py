#!/usr/bin/env python3
"""Dış kaynaklardan çekilmiş ham soru dosyalarını doğrular.

    python3 scripts/kaynak_ham_kontrol.py                 # data/kaynaklar/_ham/*.json
    python3 scripts/kaynak_ham_kontrol.py data/kaynaklar/_ham/gdh-ppla__010.json

Ham dosya: data/kaynaklar/_ham/<kaynak>__<ders>.json  (gitignore'da — üçüncü tarafın
soru bankasının tamamını depoya koymuyoruz; depoya yalnız eşleşme kaydı ve eklenen
yeni sorular girer).

    {
      "kaynak": "gdh-ppla",              # data/kaynaklar/_kaynaklar.json içindeki id
      "ders": "010",                     # 010 020 030 040 050 060 070 080 090 diger
      "url": "https://...",              # soruların alındığı tam adres
      "erisim": "acik" | "kismi" | "engelli",
      "erisim_notu": "...",
      "kullanim_notu": "robots.txt / kullanım şartı / telif notu",
      "taranan": "PDF s.1-45",           # ne kadarı okundu
      "toplam_gorulen": 180,             # kaynakta görülen soru sayısı (ayrıştırılamayanlar dahil)
      "sorular": [
        {"no": "12", "sayfa": "4", "bolum": "...", "url": "...",   # url: soruya özel adres varsa
         "metin": "...", "siklar": ["...", "..."],
         "dogru": 1,                     # siklar içinde 0 tabanlı indeks; kaynakta anahtar yoksa null
         "dogru_dayanak": "kaynak" | "yok",
         "not": ""}
      ]
    }

Kural: `dogru` yalnız kaynağın KENDİ cevap anahtarından gelir. Tahmin edilmez; anahtar yoksa
null ve `dogru_dayanak: "yok"`. Metin ve şıklar kaynaktaki gibi, birebir (yazım kusurları dahil).
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HAM = ROOT / "data" / "kaynaklar" / "_ham"
DERSLER = {"010", "020", "030", "040", "050", "060", "070", "080", "090", "diger"}
ERISIM = {"acik", "kismi", "engelli"}


def kontrol(p: Path) -> tuple[list, list, int]:
    hata, uyari = [], []
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{p.name}: bozuk JSON — {e}"], [], 0
    for k in ("kaynak", "ders", "url", "erisim", "sorular"):
        if k not in d:
            hata.append(f"{p.name}: '{k}' alanı yok")
    if hata:
        return hata, uyari, 0
    if p.name != f"{d['kaynak']}__{d['ders']}.json":
        hata.append(f"{p.name}: dosya adı '<kaynak>__<ders>.json' olmalı")
    if d["ders"] not in DERSLER:
        hata.append(f"{p.name}: bilinmeyen ders {d['ders']!r}")
    if d["erisim"] not in ERISIM:
        hata.append(f"{p.name}: erisim {d['erisim']!r} geçersiz")
    if d["erisim"] == "engelli" and d["sorular"]:
        hata.append(f"{p.name}: erişim engelli ama soru var — erişemediğin kaynağı taranmış sayma")
    if d["erisim"] != "engelli" and not d.get("taranan"):
        uyari.append(f"{p.name}: 'taranan' (ne kadarı okundu) boş")
    gorulen = d.get("toplam_gorulen")
    qs = d["sorular"]
    if not isinstance(qs, list) or any(not isinstance(q, dict) for q in qs):
        return hata + [f"{p.name}: sorular nesne listesi olmalı"], uyari, 0
    if isinstance(gorulen, int) and gorulen < len(qs):
        hata.append(f"{p.name}: toplam_gorulen {gorulen} < ayrıştırılan {len(qs)}")
    seen = set()
    for i, q in enumerate(qs):
        ad = f"{p.name}[{i}] no={q.get('no')!r}"
        if not str(q.get("metin", "")).strip():
            hata.append(f"{ad}: boş metin")
        sk = q.get("siklar")
        if not isinstance(sk, list) or not 2 <= len(sk) <= 5 or any(
                not isinstance(s, str) or not s.strip() for s in sk):
            hata.append(f"{ad}: şıklar 2-5 dolu metin olmalı ({sk if not isinstance(sk, list) else len(sk)})")
            continue
        dg = q.get("dogru")
        if dg is not None and not (type(dg) is int and 0 <= dg < len(sk)):
            hata.append(f"{ad}: dogru={dg!r} şık aralığında değil")
        if dg is None and q.get("dogru_dayanak") not in (None, "yok"):
            hata.append(f"{ad}: dogru boş ama dogru_dayanak={q.get('dogru_dayanak')!r}")
        if dg is not None and q.get("dogru_dayanak") != "kaynak":
            hata.append(f"{ad}: dogru dolu ama dogru_dayanak 'kaynak' değil — cevabı tahmin etme")
        key = (str(q.get("no", "")), q["metin"].strip()[:80])
        if key in seen:
            uyari.append(f"{ad}: aynı no+metin iki kez")
        seen.add(key)
        if len(set(map(str.strip, sk))) < len(sk):
            uyari.append(f"{ad}: aynı metinli şıklar var")
    return hata, uyari, len(qs)


def main() -> None:
    paths = [Path(a) for a in sys.argv[1:]] or sorted(HAM.glob("*__*.json"))
    top_hata = 0
    for p in paths:
        hata, uyari, n = kontrol(p)
        durum = "✓" if not hata else "HATA"
        print(f"{p.name}: {n} soru {durum}")
        for u in uyari[:15]:
            print("  uyarı:", u)
        for h in hata[:30]:
            print("  HATA:", h)
        top_hata += len(hata)
    if top_hata:
        sys.exit(f"{top_hata} hata")


if __name__ == "__main__":
    main()
