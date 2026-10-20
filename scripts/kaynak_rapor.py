#!/usr/bin/env python3
"""Ek soru çalışmasının özet tablolarını rapor_<ders>.json dosyalarından üretir.

    python3 scripts/kaynak_rapor.py            # Markdown tablolar
    python3 scripts/kaynak_rapor.py --json     # makine okunur

Ders başına: taranan kaynak sorusu, bankada zaten olan, EKLENEN (benzersiz yeni soru), aynı konu zaten
işlendiği / kapsam dışı olduğu için eklenmeyen, inceleme kuyruğunda bekleyen. Kaynak başına aynı sayılar.
Taranamayan (erişim/izin) kaynaklar ayrıca listelenir.
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KD = ROOT / "data" / "kaynaklar"
AD = {"010": "Air Law", "020": "Aircraft General Knowledge", "030": "Flight Performance and Planning",
      "040": "Human Performance", "050": "Meteorology", "060": "Navigation", "070": "Operational Procedures",
      "080": "Principles of Flight", "090": "Communications"}


def yukle() -> tuple[dict, dict]:
    ders, kaynak = {}, defaultdict(Counter)
    for p in sorted(KD.glob("rapor_*.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        d = r["ders"]
        say = Counter()
        for sid, c in r["kaynaklar"].items():
            for durum, n in c.items():
                say[durum] += n
                kaynak[sid][durum] += n
        ders[d] = {"taranan": r["taranan"], "yeni": r["yeni_benzersiz"], "mevcut": say["existing"],
                   "disi": say["out_of_scope"], "inceleme": say["review"],
                   "yeni_kume": say["new"] + say["duplicate_new"]}
        for sid, n in r.get("kaynak_yeni_benzersiz", {}).items():
            kaynak[sid]["yeni_benzersiz"] += n
        for sid, c in r["kaynaklar"].items():
            kaynak[sid]["taranan"] += sum(c.values())
    return ders, kaynak


def main() -> None:
    ders, kaynak = yukle()
    reg = {k["id"]: k for k in json.loads((KD / "_kaynaklar.json").read_text(encoding="utf-8"))["kaynaklar"]}
    if "--json" in sys.argv:
        print(json.dumps({"ders": ders, "kaynak": {k: dict(v) for k, v in kaynak.items()}}, ensure_ascii=False, indent=1))
        return
    print("| Ders | Taranan | Bankada var | **Eklenen** | Eklenmeyen (aynı konu / kapsam dışı) | İnceleme |")
    print("|---|---:|---:|---:|---:|---:|")
    top = Counter()
    for d in sorted(ders):
        x = ders[d]
        print(f"| {d} · {AD.get(d, d)} | {x['taranan']} | {x['mevcut']} | **{x['yeni']}** | {x['disi']} | {x['inceleme']} |")
        for k in ("taranan", "mevcut", "yeni", "disi", "inceleme"):
            top[k] += x[k]
    print(f"| **Toplam** | {top['taranan']} | {top['mevcut']} | **{top['yeni']}** | {top['disi']} | {top['inceleme']} |")
    print()
    print("| Kaynak | Taranan | Bankada var | Eklenen soruya bağlı | Eklenmeyen | İnceleme |")
    print("|---|---:|---:|---:|---:|---:|")
    for sid, c in sorted(kaynak.items(), key=lambda kv: -kv[1]["taranan"]):
        ad = reg.get(sid, {}).get("ad", sid)
        yeni = c["new"] + c["duplicate_new"]
        print(f"| {ad} | {c['taranan']} | {c['existing']} | {yeni} | {c['out_of_scope']} | {c['review']} |")
    taranmayan = [k for k in reg.values() if k.get("erisim") == "engelli"]
    if taranmayan:
        print()
        print("Taranmayan kaynaklar (erişim/izin):", ", ".join(k["ad"] for k in taranmayan))


if __name__ == "__main__":
    main()
