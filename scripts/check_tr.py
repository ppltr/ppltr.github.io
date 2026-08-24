#!/usr/bin/env python3
"""data/tr/ altındaki Türkçe çevirileri kaynakla karşılaştırıp doğrular.

    python3 scripts/check_tr.py            # hepsini kontrol et, kapsamı yaz
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

# Kısaltma/kod ağırlıklı kısa şıklar Türkçe karakter içermeyebilir, uyarma
TR_HARF = re.compile(r"[çğıöşüÇĞİÖŞÜ]")


def kaynak() -> dict:
    """id → (soru metni, şıklar, dosya). Kaynağı zaten Türkçe olan dosyalar
    (`"lang": "tr"`) çeviri kapsamı dışıdır — 501, 502, ders notu soruları."""
    out = {}
    for f in sorted(DATA.glob("*.json")):
        if f.name.startswith("_"):
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("lang") == "tr":
            continue
        for q in d.get("questions", []):
            if q.get("lang") == "tr":
                continue
            out[q["id"]] = (q["text"], q["options"], f.name)
    return out


def main() -> None:
    src = kaynak()
    paths = [Path(p) for p in sys.argv[1:]] or sorted(
        f for f in TR.glob("*.json") if not f.name.startswith("_"))

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
            if len(ttext) > 60 and not TR_HARF.search(ttext + " ".join(map(str, topts))):
                uyari.append(f"{p.name}: {qid}: hiç Türkçe karakter yok, çevrilmemiş olabilir")

    # Kapsam
    ders = {}
    for qid, (_, _, f) in src.items():
        kod = f[:3]
        d = ders.setdefault(kod, [0, 0])
        d[0] += 1
        if qid in gorulen:
            d[1] += 1
    print("ders  çevrili/toplam")
    for kod in sorted(ders):
        t, c = ders[kod]
        print(f"  {kod}   {c:5d}/{t:<5d} {'✓' if c == t else ''}")
    print(f"toplam {len(gorulen)}/{len(src)}")

    for u in uyari:
        print("uyarı:", u, file=sys.stderr)
    for h in hata:
        print("HATA:", h, file=sys.stderr)
    if hata:
        sys.exit(f"\n{len(hata)} hata — düzeltilmeden init_db.py çalıştırma")


if __name__ == "__main__":
    main()
