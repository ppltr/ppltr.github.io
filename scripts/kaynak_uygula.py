#!/usr/bin/env python3
"""Karar iş akışının sonucunu depoya işler: yeni sorular, kaynak notları, eşleşme kaydı.

    python3 scripts/kaynak_uygula.py 010 <sonuc.json> [--ceviri-inceleme <json>] [--kuru]

Girdi `sonuc.json`: scripts/kaynak_esle.py'nin kümelerini (data/kaynaklar/_ham/_esleme_<ders>.json)
karara bağlayan iş akışının çıktısı (`kabul`, `nihai_kararlar`, `inceleme_kuyrugu`, `ipucu`,
`tekrar_gruplari`, ...). Betik yalnız VERİYİ yazar; kararı vermez.
Her kabulde `dogru_dogrulandi: true`, `dayanak` ve `dogru_url` (özgün soruda `url`)
zorunludur. Kaynak anahtarından farklı cevap için ayrıca `anahtar_duzeltildi: true`
gerekir. Metin benzerliği cevabı seçemez. Yeni işler için kaynak_derle.py kullanılır.

Yazılanlar (hepsi idempotent; kimlikler `eslesme_<ders>.json` içinde kalıcıdır):
  data/<ders>_ek_kaynak_sorulari.json       yalnız doğrulanmış yeni sorular (origin "ek")
  data/tr/<ders>_ek_kaynak_sorulari_01.json Türkçe çeviri (şık sırası kaynakla aynı)
  data/_kaynak_notlari.json                 soru başına kaynak, kısa açıklama (TR/EN), ⭐/aday işareti
  data/kaynaklar/eslesme_<ders>.json        her ham sorunun akıbeti (metin yok): bizde var / yeni / elendi / inceleme
  data/kaynaklar/inceleme_<ders>.json       inceleme kuyruğunun tamamı (aktif teste girmez)

Mevcut soru kimlikleri ve içerikleri ASLA değiştirilmez; yalnız `_kaynak_notlari.json`'a kaynak
bilgisi eklenir. Yeni sorular kendi kimlik bandında açılır (010 → 61001+).
"""

import json
import os
import re
import sqlite3
import sys
import tempfile
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
HAM = DATA / "kaynaklar" / "_ham"
DB = ROOT / "atpl.db"
BANT = {"010": 61000, "020": 62000, "030": 63000, "050": 65000, "060": 66000, "080": 68000}
REF_KAYNAK = "ref-icao-easa"        # özgün yazılan sorular için resmî metin atfı


def norm(t: str) -> str:
    # Sayı ve işaretler cevapta anlam taşır (+3 / -3; <180 / >180).
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", t or "")).strip().casefold()


def dogru_sirasi(k: dict, raw: dict) -> list:
    """Yalnız doğrulanmış ve kaynak şıkkıyla tam eşleşen cevabı ilk sıraya taşır."""
    if k.get("dogru_dogrulandi") is not True or not k.get("dayanak") or not re.match(
            r"^https?://", k.get("dogru_url") or k.get("url") or ""):
        raise ValueError(f"{k.get('kume')}: doğrulanmış cevap, dayanak ve doğrulama URL'si gerekli")
    opts = raw["siklar"]
    matches = [i for i, option in enumerate(opts) if norm(option) == norm(k["siklar"][0])]
    if len(matches) != 1:
        raise ValueError(f"{k.get('kume')}: cevap kaynak şıkkıyla tek ve tam eşleşmiyor; tahmin edilmedi")
    d = matches[0]
    if raw.get("dogru") is not None and raw["dogru"] != d and k.get("anahtar_duzeltildi") is not True:
        raise ValueError(f"{k.get('kume')}: kaynak anahtarıyla çelişki; açık düzeltme kararı gerekli")
    return [opts[d]] + [s for i, s in enumerate(opts) if i != d]


def yukle_json(p: Path, varsayilan=None):
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return varsayilan


def yaz_json(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{p.name}.", dir=p.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")
        os.replace(name, p)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def ham_yukle(ders: str) -> dict:
    out = {}
    for p in sorted(HAM.glob(f"*__{ders}.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("erisim") == "engelli":
            if d.get("sorular"):
                raise ValueError(f"{p}: erişim engelli kaynak soru içeremez")
            continue
        for i, q in enumerate(d["sorular"]):
            out[f"{d['kaynak']}__{d['ders']}#{i}"] = {**q, "kaynak": d["kaynak"], "url_dosya": d["url"], "i": i}
    return out


def var_kumeleri(esleme: dict) -> dict:
    """Karar iş akışının kurduğu 'V' kümelerini yeniden üretir (bank_id'ye göre, artan sırayla)."""
    gruplar = defaultdict(list)
    for v in esleme["var"]:
        gruplar[v["bank_id"]].append(v["k"])
    return {f"{esleme['ders']}-V{i:04d}": {"k": ks, "bank_id": bid}
            for i, (bid, ks) in enumerate(sorted(gruplar.items()), 1)}


def kanonik(conn, bid: int) -> int:
    seen = set()
    while bid not in seen:
        seen.add(bid)
        r = conn.execute("SELECT dup_of FROM questions WHERE id = ?", (bid,)).fetchone()
        if r is None:
            raise ValueError(f"bank_id {bid} bankada yok")
        if not r[0]:
            return bid
        bid = r[0]
    raise ValueError(f"tekrar zincirinde döngü: {bid}")


def kaynak_girdisi(q: dict) -> dict:
    g = {"k": q["kaynak"], "no": str(q.get("no", ""))}
    if q.get("sayfa"):
        g["sayfa"] = str(q["sayfa"])
    g["url"] = q.get("url") or q["url_dosya"]
    return g


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    ders, sonuc_yol = args[0], Path(args[1])
    kuru = "--kuru" in args
    cev_inc = {}
    if "--ceviri-inceleme" in args:
        cev_inc = json.loads(Path(args[args.index("--ceviri-inceleme") + 1]).read_text(encoding="utf-8"))
    sonuc = json.loads(sonuc_yol.read_text(encoding="utf-8"))
    esleme = json.loads((HAM / f"_esleme_{ders}.json").read_text(encoding="utf-8"))
    ham = ham_yukle(ders)
    kumeler = {k["kume"]: k for k in esleme["kumeler"]}
    for kid, v in var_kumeleri(esleme).items():
        kumeler[kid] = {"kume": kid, "uyeler": [{"k": k} for k in v["k"]], "_var_bank": v["bank_id"]}

    conn = sqlite3.connect(DB)
    bolum_ad = dict(conn.execute(
        "SELECT code, name FROM sections WHERE subject_code = ?", (ders,)).fetchall())
    ders_ad = conn.execute("SELECT name FROM subjects WHERE code = ?", (ders,)).fetchone()[0]
    mevcut_idler = {r[0] for r in conn.execute("SELECT id FROM questions")}

    kayit_yol = DATA / "kaynaklar" / f"eslesme_{ders}.json"
    kayit = yukle_json(kayit_yol, {"ders": ders, "yeni": {}, "ham": {}})
    notlar_yol = DATA / "_kaynak_notlari.json"
    notlar = yukle_json(notlar_yol, {"_aciklama": "", "notlar": {}})
    notlar["_aciklama"] = (
        "Soru başına kaynak bağı (src), kısa açıklama (tr/en) ve işaret. isaret: 'dogrulanmis' = kullanıcı bu "
        "sorunun sınavda karşılaştığı soruyla eşleştiğini doğruladı (⭐); 'aday' = hatırlanan konuya benzer aday, "
        "kesin metin eşleşmesi yok. Hiçbiri resmî SHGM çıkmış sorusu olarak sunulmaz. scripts/kaynak_uygula.py yazar.")
    N = notlar["notlar"]

    def not_ac(qid: int) -> dict:
        return N.setdefault(str(qid), {"src": []})

    def src_ekle(qid: int, girdiler: list) -> None:
        n = not_ac(qid)
        n.setdefault("src", [])
        var = {(s["k"], s.get("no", ""), s.get("sayfa", ""), s.get("url", "")) for s in n["src"]}
        for g in girdiler:
            key = (g["k"], g.get("no", ""), g.get("sayfa", ""), g.get("url", ""))
            if key not in var:
                n["src"].append(g)
                var.add(key)

    # ── kimlik tahsisi (kalıcı) ──────────────────────────────────────────
    yeni_map = kayit["yeni"]            # anahtar → id
    sonraki = max([BANT[ders]] + [int(v) for v in yeni_map.values()])

    def kimlik(anahtar: str) -> int:
        nonlocal sonraki
        if anahtar not in yeni_map:
            sonraki += 1
            if sonraki > BANT[ders] + 999:
                sys.exit(f"hata: {ders} kimlik bandı doldu; yeni bant tanımlanmalı")
            if sonraki in mevcut_idler:
                sys.exit(f"hata: {sonraki} kimliği bankada zaten var")
            yeni_map[anahtar] = sonraki
        return int(yeni_map[anahtar])

    kabul = {k["kume"]: k for k in sonuc["kabul"]}
    nihai = {k["kume"]: k for k in sonuc["nihai_kararlar"]}
    tekrar_grup = {}                    # at → tut (yeniler arası tekrar)
    for g in sonuc.get("tekrar_gruplari", []):
        for a in g["at"]:
            tekrar_grup[a] = g["tut"]

    onceki = yukle_json(DATA / f"{ders}_ek_kaynak_sorulari.json", {"questions": []})
    sorular = list(onceki["questions"])
    onceki_by_id = {q["id"]: q for q in sorular}
    tr_cevirileri = yukle_json(DATA / "tr" / f"{ders}_ek_kaynak_sorulari_01.json", {"questions": {}})["questions"]
    kume_id = {}                        # kume → yeni soru id
    def ek_soru(kume: str, metin: str, siklar_dogru_ilk: list, bolum: str, anahtar: str,
                inceleme: str = "", tr: dict | None = None) -> int:
        qid = kimlik(anahtar)
        kume_id[kume] = qid
        q = {"id": qid, "section": bolum, "text": metin, "options": siklar_dogru_ilk}
        if inceleme:
            q["inceleme"] = True
            q["inceleme_nedeni"] = inceleme
        if qid in onceki_by_id:
            old = onceki_by_id[qid]
            if old["text"] != metin or old["options"] != siklar_dogru_ilk:
                raise ValueError(f"{qid}: aynı kimliğe farklı soru yüklenemez; yeni kimlik gerekli")
            sorular[sorular.index(old)] = q
        else:
            if qid in mevcut_idler:
                raise ValueError(f"{qid}: mevcut soru kimliği yeniden kullanılamaz")
            sorular.append(q)
        onceki_by_id[qid] = q
        if tr:
            tr_cevirileri[str(qid)] = {"text": tr["tr_metin"], "options": tr["tr_siklar"]}
        return qid

    # ── kabul edilen yeni sorular ────────────────────────────────────────
    for kume, k in sorted(kabul.items()):
        yz = k.get("yazi")
        if not yz:
            raise ValueError(f"{kume}: Türkçe çeviri yok; hiçbir dosya yazılmadı")
        if any(not yz.get(field) for field in ("tr_metin", "tr_siklar", "aciklama_tr", "aciklama_en")):
            raise ValueError(f"{kume}: çeviri veya kısa açıklama eksik")
        if k.get("ozgun"):
            if k.get("dogru_dogrulandi") is not True or not k.get("dayanak") or not re.match(r"^https?://", k.get("url") or ""):
                raise ValueError(f"{kume}: özgün soru için doğrulanmış cevap ve URL'li dayanak gerekli")
            metin, sk, anahtar = k["metin"], k["siklar"], kume
            src = [{"k": REF_KAYNAK, "no": "", "sayfa": (k.get("dayanak") or "")[:160], "url": k.get("url") or ""}]
        else:
            r = ham[k["temsilci_k"]]
            metin = r["metin"]                       # birebir kaynak metni (ajan kopyası değil)
            kaynak_sk = r["siklar"]
            sk = dogru_sirasi(k, r)
            anahtar = k["temsilci_k"]
            if len(sk) != len(yz["tr_siklar"]):
                sys.exit(f"hata: {kume}: çeviri şık sayısı tutmuyor")
            src = []
            for u in kumeler[kume]["uyeler"]:
                src.append(kaynak_girdisi(ham[u["k"]]))
        qid = ek_soru(kume, metin, sk, k["bolum"], anahtar, tr=yz)
        n = not_ac(qid)
        n["tr"], n["en"] = yz["aciklama_tr"], yz["aciklama_en"]
        src_ekle(qid, src)

    # ── inceleme kuyruğu ─────────────────────────────────────────────────
    kuyruk = []
    for it in sonuc.get("inceleme_kuyrugu", []):
        kume = it["kume"]
        if kume in kabul or kume in tekrar_grup:
            continue
        kayit_k = {"kume": kume, "neden": it.get("inceleme_nedeni") or it.get("gerekce"),
                   "metin": it.get("metin"), "siklar": it.get("siklar"), "dogru_index": it.get("dogru_index"),
                   "bolum": it.get("bolum"), "dayanak": it.get("dayanak"),
                   "kaynaklar": [kaynak_girdisi(ham[u["k"]]) for u in kumeler.get(kume, {}).get("uyeler", []) if u["k"] in ham]}
        kuyruk.append(kayit_k)
        # Tahmini cevap ve çeviri, adayları aktif banka kaydına dönüştürmez.

    # ── mevcut sorulara kaynak bilgisi (var / tekrar) ────────────────────
    for kume, kr in nihai.items():
        c = kumeler.get(kume)
        if not c:
            continue
        hedef = None
        if kr["karar"] == "var" and kr.get("bank_id"):
            hedef = kanonik(conn, int(kr["bank_id"]))
        elif kr["karar"] == "elendi" and kr.get("elenme_nedeni") == "tekrar" and kr.get("bank_id"):
            hedef = kanonik(conn, int(kr["bank_id"]))
        if hedef:
            if hedef not in mevcut_idler:
                print(f"uyarı: {kume}: bank_id {hedef} bankada yok", file=sys.stderr)
                continue
            src_ekle(hedef, [kaynak_girdisi(ham[u["k"]]) for u in c["uyeler"] if u["k"] in ham])
    # yeniler arası tekrar: elenen kümenin kaynakları tutulan yeni soruya eklenir
    for at, tut in tekrar_grup.items():
        c = kumeler.get(at)
        if not c:
            continue
        if str(tut).startswith("BANKA:"):
            hedef = kanonik(conn, int(str(tut).split(":")[1]))
            src_ekle(hedef, [kaynak_girdisi(ham[u["k"]]) for u in c["uyeler"] if u["k"] in ham])
        elif tut in kume_id:
            src_ekle(kume_id[tut], [kaynak_girdisi(ham[u["k"]]) for u in c["uyeler"] if u["k"] in ham])

    # ── ipucu işaretleri ─────────────────────────────────────────────────
    for h in sonuc.get("ipucu", []):
        for m in h.get("mevcut_isaret", []):
            bid = kanonik(conn, int(m["bank_id"]))
            n = not_ac(bid)
            if n.get("isaret") != "dogrulanmis":
                n["isaret"] = m["isaret"]
        for m in h.get("kume_isaret", []):
            qid = kume_id.get(m["kume"])
            if qid is None and m["kume"] in tekrar_grup:
                qid = kume_id.get(tekrar_grup[m["kume"]])
            if qid is not None:
                n = not_ac(qid)
                if n.get("isaret") != "dogrulanmis":
                    n["isaret"] = m["isaret"]
    for k in kabul.values():
        if k.get("ozgun") and k["kume"] in kume_id and k.get("isaret"):
            n = not_ac(kume_id[k["kume"]])
            if n.get("isaret") != "dogrulanmis":
                n["isaret"] = k["isaret"]

    # ── ham soru akıbeti (metinsiz) ──────────────────────────────────────
    ham_kayit = kayit["ham"]
    for kume, c in kumeler.items():
        kr = nihai.get(kume)
        for u in c["uyeler"]:
            k = u["k"]
            if k not in ham:
                continue
            r = ham[k]
            if kume in kume_id and kume in kabul:
                sn = {"sonuc": "yeni", "id": kume_id[kume]}
            elif kume in kume_id:
                sn = {"sonuc": "inceleme", "id": kume_id[kume]}
            elif kume in tekrar_grup:
                tut = tekrar_grup[kume]
                hedef = int(str(tut).split(":")[1]) if str(tut).startswith("BANKA:") else kume_id.get(tut)
                sn = {"sonuc": "var" if str(tut).startswith("BANKA:") else "yeni_tekrar", "id": hedef}
            elif kr is None:
                sn = {"sonuc": "karar_yok"}
            elif kr["karar"] == "var" or (kr["karar"] == "elendi" and kr.get("elenme_nedeni") == "tekrar"):
                sn = {"sonuc": "var", "id": kanonik(conn, int(kr["bank_id"])) if kr.get("bank_id") else None}
            elif kr["karar"] == "elendi":
                sn = {"sonuc": "elendi", "neden": kr.get("elenme_nedeni") or "ppl_disi"}
            elif kr["karar"] == "inceleme":
                sn = {"sonuc": "inceleme", "neden": kr.get("inceleme_nedeni", "")[:140]}
            else:
                sn = {"sonuc": "yeni_elendi", "neden": "çeviri/doğrulama aşamasında düştü"}
            sn.update({"kaynak": r["kaynak"], "no": str(r.get("no", "")), "sayfa": str(r.get("sayfa") or "")})
            if kr and kr.get("gerekce"):
                sn["gerekce"] = kr["gerekce"][:200]
            ham_kayit[k] = sn
    kayit["yeni"] = yeni_map

    # ── dosyaları yaz ────────────────────────────────────────────────────
    sorular.sort(key=lambda q: q["id"])
    soru_dosya = {
        "subject_code": ders, "subject_name": ders_ad, "origin": "ek",
        "source": "Ek kaynaklar: dış PPL soru listeleri ve resmî metinler (ayrıntı: data/_kaynak_notlari.json, "
                  "data/kaynaklar/_kaynaklar.json). SHGM çıkmış sorusu değildir.",
        "id_convention": f"{BANT[ders] + 1}–{BANT[ders] + 999}: ek kaynak sorular; kimlikler "
                         f"data/kaynaklar/eslesme_{ders}.json içinde kalıcıdır, emekli kimlik yeniden kullanılmaz.",
        "sections": bolum_ad,
        "questions": sorular,
    }
    print(f"{ders}: {len(sorular)} soru yazılacak "
          f"({sum(1 for q in sorular if q.get('inceleme'))} inceleme), {len(N)} notlu soru, "
          f"{len(kuyruk)} inceleme kuyruğu kaydı")
    if kuru:
        return
    yaz_json(DATA / "kaynaklar" / f"inceleme_{ders}.json", {"ders": ders, "kuyruk": kuyruk})
    yaz_json(DATA / f"{ders}_ek_kaynak_sorulari.json", soru_dosya)
    yaz_json(DATA / "tr" / f"{ders}_ek_kaynak_sorulari_01.json", {"questions": tr_cevirileri})
    for q in notlar["notlar"].values():
        q["src"].sort(key=lambda s: (s["k"], s.get("no", "")))
    notlar["notlar"] = dict(sorted(N.items(), key=lambda kv: int(kv[0])))
    yaz_json(notlar_yol, notlar)
    yaz_json(kayit_yol, kayit)


if __name__ == "__main__":
    main()
