#!/usr/bin/env python3
"""data/tr/ ve data/en/ altındaki çevirileri kaynakla karşılaştırıp doğrular.

Her sorunun iki dilde de karşılığı olmalı: kaynağı İngilizce olanın Türkçesi
data/tr/ içinde, kaynağı Türkçe olanın İngilizcesi data/en/ içinde. Eksik varsa
uygulamada o soru, seçili dil ne olursa olsun kaynak dilinde görünür — yani kip
içinde dil karışır. Bu betik tam da onu yakalar.

    python3 scripts/check_tr.py            # iki dili de kontrol et, kapsamı yaz
    python3 scripts/check_tr.py data/tr/010_air_law_01.json   # tek dosya

Kontroller:
  * JSON düzgün mü, id'ler bankada var mı, aynı id iki dosyada mı
  * şık sayısı kaynakla birebir aynı mı  (doğru cevap ilk şıktır — sıra kayarsa
    yanlış şık doğru diye işaretlenir, o yüzden bu ölümcül hatadır)
  * boş metin, çevrilmeden bırakılmış (kaynakla birebir aynı) metin
  * Türkçe karakter hiç geçmeyen uzun çeviriler (şüpheli, uyarı)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TR = DATA / "tr"
EN = DATA / "en"

# Kısaltma/kod ağırlıklı kısa şıklar Türkçe karakter içermeyebilir, uyarma
TR_HARF = re.compile(r"[çğıöşüÇĞİÖŞÜ]")


def kaynak(dil: str) -> dict:
    """id → (soru metni, şıklar, dosya).

    `dil='tr'` → çevrilmesi gereken (kaynağı İngilizce) sorular.
    `dil='en'` → çevrilmesi gereken (kaynağı Türkçe) sorular: 501, 502, ders notu.
    """
    out = {}
    for f in sorted(DATA.glob("*.json")):
        if f.name.startswith("_"):
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        dosya_tr = d.get("lang") == "tr"
        for q in d.get("questions", []):
            soru_tr = dosya_tr or q.get("lang") == "tr"
            # Kaynağı Türkçe olan sorunun Türkçeye, İngilizce olanın İngilizceye
            # çevrilmesine gerek yok — zaten o dilde
            if (dil == "tr") == soru_tr:
                continue
            out[q["id"]] = (q["text"], q["options"], f.name)
    return out


def denetle(dil: str, klasor: Path, paths: list) -> tuple[list, list, dict, dict]:
    src = kaynak(dil)
    hata, uyari, gorulen = [], [], {}
    for p in paths:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            hata.append(f"{p.name}: bozuk JSON — {e}")
            continue
        qs = d.get("questions")
        if not isinstance(qs, dict):
            hata.append(f"{p.name}: 'questions' bir sözlük değil")
            continue
        for sid, tr in qs.items():
            if not sid.isdigit():
                hata.append(f"{p.name}: sayı olmayan id anahtarı: {sid!r}")
                continue
            qid = int(sid)
            if qid not in src:
                hata.append(f"{p.name}: {qid} bankada yok")
                continue
            if qid in gorulen:
                hata.append(f"{p.name}: {qid} zaten {gorulen[qid]} içinde çevrilmiş")
                continue
            gorulen[qid] = p.name
            stext, sopts, _ = src[qid]
            ttext, topts = tr.get("text", ""), tr.get("options", [])
            if not isinstance(topts, list) or len(topts) != len(sopts):
                hata.append(f"{p.name}: {qid}: {len(topts) if isinstance(topts, list) else '?'} şık "
                            f"çevrilmiş, kaynakta {len(sopts)} şık var")
                continue
            if not ttext.strip() or any(not str(t).strip() for t in topts):
                hata.append(f"{p.name}: {qid}: boş çeviri")
                continue
            if ttext.strip() == stext.strip():
                uyari.append(f"{p.name}: {qid}: soru metni kaynakla birebir aynı")
            # Bu sezgi yalnız Türkçe yönü için anlamlı; İngilizce çeviride
            # Türkçe karakter olmaması normaldir
            if dil == "tr" and len(ttext) > 60 and \
                    not TR_HARF.search(ttext + " ".join(map(str, topts))):
                uyari.append(f"{p.name}: {qid}: hiç Türkçe karakter yok, çevrilmemiş olabilir")

    ders = {}
    for qid, (_, _, f) in src.items():
        kod = f[:3]
        d = ders.setdefault(kod, [0, 0])
        d[0] += 1
        if qid in gorulen:
            d[1] += 1
    return hata, uyari, gorulen, {"ders": ders, "src": src}


def main() -> None:
    arg = [Path(p) for p in sys.argv[1:]]
    isler = []
    if arg:
        for p in arg:
            isler.append(("en" if p.parent.name == "en" else "tr", p))
    else:
        isler = [("tr", None), ("en", None)]

    toplam_hata = 0


    for dil in ("tr", "en"):
        paths = [p for d, p in isler if d == dil and p is not None]
        if arg and not paths:
            continue
        klasor = TR if dil == "tr" else EN
        if not paths:
            paths = sorted(f for f in klasor.glob("*.json") if not f.name.startswith("_"))
        hata, uyari, gorulen, ek = denetle(dil, klasor, paths)
        etiket = "Türkçe (data/tr)" if dil == "tr" else "İngilizce (data/en)"
        print(f"\n{etiket} — ders  çevrili/toplam")
        for kod in sorted(ek["ders"]):
            t, c = ek["ders"][kod]
            print(f"  {kod}   {c:5d}/{t:<5d} {'✓' if c == t else ''}")
        print(f"  toplam {len(gorulen)}/{len(ek['src'])}")
        for u in uyari:
            print("uyarı:", u, file=sys.stderr)
        for h in hata:
            print("HATA:", h, file=sys.stderr)
        toplam_hata += len(hata)
    if toplam_hata:
        sys.exit(f"\n{toplam_hata} hata — düzeltilmeden init_db.py çalıştırma")


if __name__ == "__main__":
    main()
