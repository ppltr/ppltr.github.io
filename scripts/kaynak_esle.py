#!/usr/bin/env python3
"""Ham kaynak sorularını bankayla eşleştirir ve bizde olmayanları kümeler.

    python3 scripts/kaynak_esle.py 010            # data/kaynaklar/_ham/*__010.json
    python3 scripts/kaynak_esle.py 010 --diger    # 010 dosyalarına ek: başka derslerde çıkmış TORA gibi
                                                  # soruları da bütün banka karşısında ara (varsayılan zaten bütün banka)
    python3 scripts/kaynak_esle.py 060

Çıktı: data/kaynaklar/_ham/_esleme_<ders>.json   (gitignore'da — soru metni içerir)

Her ham soru, bankadaki (TÜM derslerdeki) sorularla karşılaştırılır; kaynak İngilizce ise
bankanın İngilizce metniyle (kaynağı Türkçe olan banka sorularında `text_en`).

Sınıflar (otomatik, KARAR DEĞİL — belirsizleri insan/ajan okur):
  var         soru kökü ≥%80 benzer ve cevap aynı           → mevcut soruya yeni kaynak bilgisi eklenir
  ters_cevap  soru kökü ≥%80 benzer ama cevap FARKLI        → çelişki; elle bakılır (eski/çelişkili cevap olabilir)
  aday        kısmen benzer (koşul farkı, ters yönden sorma, cevabı aynı kök farklı)
  yok         bankada benzeri yok

`yok` + `aday` + `ters_cevap` kaynaklar arası kümelenir: aynı soru üç kaynakta geçiyorsa tek küme.
"""

import json
import re
import sqlite3
import sys
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "atpl.db"
HAM = ROOT / "data" / "kaynaklar" / "_ham"

STOP = {
    "the", "a", "an", "of", "to", "in", "is", "are", "and", "or", "for", "on", "at", "by", "be",
    "with", "that", "this", "it", "as", "from", "which", "what", "following", "statements",
    "statement", "correct", "true", "false", "following", "one", "all", "any", "should", "shall",
    "will", "can", "may", "must", "has", "have", "been", "was", "were", "when", "than", "then",
    "its", "their", "yes", "if", "do", "does", "who", "whom", "where",
}


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", (t or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.replace("&", " and ")
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s.]", " ", t)).strip()


def toks(t: str) -> set:
    # sayılar (1200, 3.5, 075) ayırt edicidir — durdurma sözcüğü sayılmaz
    return {w for w in norm(t).replace(".", " ").split() if w not in STOP and len(w) > 0}


def jac(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def seq(a: str, b: str) -> float:
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def benzerlik(a: str, b: str) -> float:
    """Jaccard ile sıra duyarlı oranın karışımı; kısa cevaplarda sıra, uzun köklerde küme baskın."""
    return 0.5 * jac(toks(a), toks(b)) + 0.5 * seq(a, b)


def bank_yukle() -> list:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    out = []
    for q in conn.execute(
            "SELECT id, subject_code, lang, text, text_en, text_tr, dup_of, origin FROM questions"):
        opts = conn.execute(
            "SELECT text, text_en, text_tr, is_correct FROM options WHERE question_id = ? ORDER BY ord",
            (q["id"],)).fetchall()
        for dil in ("en", "tr"):
            # o dildeki metin: kaynak dil ise `text`, değilse çeviri
            if q["lang"] == dil:
                metin, sik = q["text"], [o["text"] for o in opts]
            else:
                metin = q["text_" + dil]
                sik = [o["text_" + dil] for o in opts]
            if not metin or not all(sik):
                continue
            out.append({"id": q["id"], "ders": q["subject_code"], "dil": dil, "metin": metin,
                        "siklar": sik, "dogru": sik[0], "dup_of": q["dup_of"], "origin": q["origin"],
                        "tk": toks(metin), "ak": toks(sik[0]),
                        "ok": toks(" ".join(sik))})
    conn.close()
    return out


def ham_yukle(ders: str) -> list:
    out = []
    for p in sorted(HAM.glob(f"*__{ders}.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("erisim") == "engelli":
            continue
        for i, q in enumerate(d["sorular"]):
            dg = q.get("dogru")
            out.append({"k": f"{d['kaynak']}__{d['ders']}#{i}", "kaynak": d["kaynak"], "ders": d["ders"],
                        "dil": d.get("dil", "en"), "no": q.get("no"), "sayfa": q.get("sayfa"),
                        "bolum": q.get("bolum"), "url": q.get("url") or d["url"],
                        "metin": q["metin"], "siklar": q["siklar"], "dogru": dg,
                        "dogru_metin": q["siklar"][dg] if dg is not None else None})
    return out


def en_iyiler(r: dict, bank: list, idx: dict, n: int = 3) -> list:
    rt, rok = toks(r["metin"]), toks(" ".join(r["siklar"]))
    adaylar = defaultdict(int)
    for w in rt | rok:
        for j in idx.get(w, ()):
            adaylar[j] += 1
    sirali = sorted(adaylar, key=lambda j: -adaylar[j])[:60]
    sonuc = []
    for j in sirali:
        b = bank[j]
        if b["dil"] != r["dil"]:
            continue
        st = 0.5 * jac(rt, b["tk"]) + 0.5 * seq(r["metin"], b["metin"])
        # cevap karşılaştırması: kaynağın anahtarı varsa onunla, yoksa bankanın doğrusu ham şıklar arasında mı
        if r["dogru_metin"] is not None:
            ad = benzerlik(r["dogru_metin"], b["dogru"])
        else:
            ad = max(benzerlik(s, b["dogru"]) for s in r["siklar"])
        bank_dogru_ham_siklarda = max(benzerlik(s, b["dogru"]) for s in r["siklar"])
        sik_kumesi = jac(rok, b["ok"])
        sonuc.append({"id": b["id"], "ders": b["ders"], "dup_of": b["dup_of"], "stem": round(st, 2),
                      "ans": round(ad, 2), "bank_cevap_sikta": round(bank_dogru_ham_siklarda, 2),
                      "opts": round(sik_kumesi, 2), "metin": b["metin"], "dogru": b["dogru"]})
    sonuc.sort(key=lambda x: -(x["stem"] + 0.3 * x["opts"] + 0.2 * x["ans"]))
    return sonuc[:n]


def siniflandir(r: dict, nb: list) -> str:
    if not nb:
        return "yok"
    b = nb[0]
    anahtarli = r["dogru_metin"] is not None
    if b["stem"] >= 0.80:
        if anahtarli:
            if b["ans"] >= 0.60:
                return "var"
            # kök aynı, kaynağın anahtarı bankanınkinden farklı: bankanın doğrusu ham şıklar arasındaysa
            # AYNI soru için çelişen cevap (eski/yanlış anahtar ya da bizdeki hata); değilse şıklar da
            # farklıdır, başka bir koşulu soran soru olabilir
            return "ters_cevap" if b["bank_cevap_sikta"] >= 0.80 else "aday"
        # Bankanın cevabının şıklarda bulunması, kaynağın cevap anahtarı değildir.
        return "aday"
    # kök farklı yazılmış ama cevap + şık kümesi aynı: ters yönden sorma ya da yeniden ifade
    if b["stem"] >= 0.50 or (b["stem"] >= 0.30 and b["opts"] >= 0.60) or \
            (b["stem"] >= 0.35 and b["ans"] >= 0.85 and anahtarli):
        return "aday"
    return "yok"


def kumele(items: list) -> list:
    """bankada olmayan/belirsiz kalemleri kaynaklar arası kümeler (bağlı bileşenler)."""
    n = len(items)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tk = [toks(i["metin"]) for i in items]
    ok = [toks(" ".join(i["siklar"])) for i in items]
    inv = defaultdict(list)
    for j, t in enumerate(tk):
        for w in t:
            inv[w].append(j)
    for i in range(n):
        say = defaultdict(int)
        for w in tk[i]:
            for j in inv[w]:
                if j > i:
                    say[j] += 1
        for j in say:
            if items[i]["dil"] != items[j]["dil"]:
                continue
            st = 0.5 * jac(tk[i], tk[j]) + 0.5 * seq(items[i]["metin"], items[j]["metin"])
            if st < 0.72:
                continue
            ci, cj = items[i]["dogru_metin"], items[j]["dogru_metin"]
            if ci is not None and cj is not None:
                ans = benzerlik(ci, cj)
            else:
                ans = jac(ok[i], ok[j])
            # Aynı şıklar çelişen anahtarları veya farklı koşulları gizleyemez.
            if ci is not None and cj is not None and ans < 0.8:
                continue
            critical = {"ifr", "vfr", "rvsm", "non", "pic", "pilot", "copilot", "cpl", "ppl", "atpl", "not", "no", "climb", "climbing", "descent", "descending"}
            if (tk[i] & critical) != (tk[j] & critical):
                continue
            nums = lambda t: {w for w in t if any(c.isdigit() for c in w)}
            if nums(tk[i]) != nums(tk[j]):
                continue
            if ans >= 0.8 or (ci is None and cj is None and jac(ok[i], ok[j]) >= 0.9):
                parent[find(i)] = find(j)
    gruplar = defaultdict(list)
    for i in range(n):
        gruplar[find(i)].append(i)
    return [sorted(g) for g in gruplar.values()]


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ders = sys.argv[1]
    bank = bank_yukle()
    idx = defaultdict(list)
    for j, b in enumerate(bank):
        for w in b["tk"] | b["ok"]:
            idx[w].append(j)
    ham = ham_yukle(ders)
    if not ham:
        sys.exit(f"{ders}: ham soru yok ({HAM})")

    sonuc, sayac = [], defaultdict(lambda: defaultdict(int))
    for r in ham:
        nb = en_iyiler(r, bank, idx)
        r["sinif"] = siniflandir(r, nb)
        r["komsular"] = nb
        sayac[r["kaynak"]][r["sinif"]] += 1
        sonuc.append(r)

    bekleyen = [r for r in sonuc if r["sinif"] != "var"]
    kumeler = []
    for g in kumele(bekleyen):
        uyeler = [bekleyen[i] for i in g]
        # temsilci: anahtarlı olan, sonra en uzun şık metinli
        temsil = sorted(uyeler, key=lambda r: (r["dogru"] is None, -len(r["metin"])))[0]
        komsu = {}
        for u in uyeler:
            for nb in u["komsular"]:
                if nb["id"] not in komsu or nb["stem"] > komsu[nb["id"]]["stem"]:
                    komsu[nb["id"]] = nb
        kumeler.append({
            "kume": None,
            "siniflar": sorted({u["sinif"] for u in uyeler}),
            "uyeler": [{k: u[k] for k in ("k", "kaynak", "no", "sayfa", "bolum", "url", "metin", "siklar",
                                          "dogru", "dogru_metin", "sinif")} for u in uyeler],
            "temsilci": temsil["k"],
            "komsular": sorted(komsu.values(), key=lambda x: -x["stem"])[:5],
        })
    kumeler.sort(key=lambda c: (c["siniflar"] != ["yok"], c["uyeler"][0]["metin"]))
    for i, c in enumerate(kumeler, 1):
        c["kume"] = f"{ders}-K{i:04d}"

    var = [{"k": r["k"], "kaynak": r["kaynak"], "no": r["no"], "sayfa": r["sayfa"], "url": r["url"],
            "bank_id": r["komsular"][0]["id"], "stem": r["komsular"][0]["stem"],
            "ans": r["komsular"][0]["ans"], "bank_ders": r["komsular"][0]["ders"],
            "metin": r["metin"], "siklar": r["siklar"], "dogru": r["dogru"],
            "bank_metin": r["komsular"][0]["metin"], "bank_dogru": r["komsular"][0]["dogru"]}
           for r in sonuc if r["sinif"] == "var"]
    out = {"ders": ders, "sayac": {k: dict(v) for k, v in sayac.items()},
           "var": var, "kumeler": kumeler}
    path = HAM / f"_esleme_{ders}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{ders}: {len(ham)} ham soru → {len(var)} bizde var, {len(bekleyen)} bekleyen → {len(kumeler)} küme")
    print(f"{'kaynak':20s} {'toplam':>7s} {'var':>5s} {'ters':>5s} {'aday':>5s} {'yok':>5s}")
    for k, v in sorted(sayac.items()):
        print(f"{k:20s} {sum(v.values()):7d} {v['var']:5d} {v['ters_cevap']:5d} {v['aday']:5d} {v['yok']:5d}")
    print(path)


if __name__ == "__main__":
    main()
