#!/usr/bin/env python3
"""Ham dosyaların üst verisinden data/kaynaklar/_kaynaklar.json kaydını günceller.

    python3 scripts/kaynak_kayit.py

Her ham dosya (data/kaynaklar/_ham/<kaynak>__<ders>.json) için kaynak kaydına şunlar işlenir:
  erisim          acik | kismi | engelli  (dosyalardan en iyisi; hiç dosya yoksa mevcut kalır)
  erisim_notu     son görülen erişim açıklaması (kısa)
  kullanim_notu   robots.txt / kullanım şartı / telif notu
  taranan         { ders: {"sayi": N, "kapsam": "PDF s.1-24", "url": "..."} }
Kayıtta olmayan kaynak id'si (ör. x-cad-rs) ham dosyanın `kaynak_meta` ya da `kaynak_adi`
alanından, o da yoksa dosya adından oluşturulur. Sayılar (bizde var / yeni / elenen) burada
değil, scripts/kaynak_rapor.py içinde eşleşme kayıtlarından türetilir.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HAM = ROOT / "data" / "kaynaklar" / "_ham"
REG = ROOT / "data" / "kaynaklar" / "_kaynaklar.json"
SIRA = {"engelli": 0, "kismi": 1, "acik": 2}


def main() -> None:
    reg = json.loads(REG.read_text(encoding="utf-8"))
    by_id = {k["id"]: k for k in reg["kaynaklar"]}
    toplam = {}
    for p in sorted(HAM.glob("*__*.json")):
        if p.name.startswith("_"):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        kid, ders = d["kaynak"], d["ders"]
        k = by_id.get(kid)
        if k is None:
            k = {"id": kid, "ad": d.get("kaynak_adi") or kid, "url": d["url"], "tur": "web"}
            reg["kaynaklar"].append(k)
            by_id[kid] = k
        if SIRA[d["erisim"]] >= SIRA.get(k.get("erisim", "engelli"), 0) or "erisim" not in k:
            k["erisim"] = d["erisim"]
        if d.get("erisim_notu"):
            k["erisim_notu"] = d["erisim_notu"][:700]
        if d.get("kullanim_notu"):
            k["kullanim_notu"] = d["kullanim_notu"][:700]
        k.setdefault("taranan", {})[ders] = {
            "sayi": len(d["sorular"]), "gorulen": d.get("toplam_gorulen", len(d["sorular"])),
            "kapsam": d.get("taranan", ""), "url": d["url"]}
        toplam[kid] = toplam.get(kid, 0) + len(d["sorular"])
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k in reg["kaynaklar"]:
        print(f"{k['id']:28s} {k.get('erisim', '?'):8s} {toplam.get(k['id'], 0):5d} soru")


if __name__ == "__main__":
    main()
