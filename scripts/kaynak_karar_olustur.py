#!/usr/bin/env python3
"""Ek soru seçimi için gözden geçirme araçları ve karar dosyası üretici.

    python3 scripts/kaynak_karar_olustur.py liste 080 [a b] [--ust 0.70] [--filtre regex]
    python3 scripts/kaynak_karar_olustur.py ara   "regex" [ders]
    python3 scripts/kaynak_karar_olustur.py acik  080 data/kaynaklar/decisions/080_secim.json   # kararı olmayanlar
    python3 scripts/kaynak_karar_olustur.py uret  080 data/kaynaklar/decisions/080_secim.json

Akış (her ders için):
  1. python3 scripts/kaynak_ayristir.py …          ham soru dosyaları  (data/kaynaklar/_ham, gitignore'da)
  2. python3 scripts/kaynak_esle.py 080            bankayla eşleştirme + kümeler
  3. … liste 080                                   adayları EN YAKIN banka soruları ile yan yana okur
  4. … ara "regex"                                 bankada kavramın başka biçimde sorulup sorulmadığına bakar
  5. seçim dosyasını yaz (yeni / inceleme / disi / var)
  6. … uret 080 <secim.json>                       data/kaynaklar/decisions/<ders>_ek.json
  7. python3 scripts/kaynak_derle.py 080 data/kaynaklar/decisions/080_ek.json

Seçim dosyası (üye etiketi: TR#12 = Traficom, CAD#29 = Sırbistan CAD, TC#22 = Transport Canada, SY#3 = Son Yaklaşma):
  {"ders": "080",
   "yeni":     [{"uye": "CAD#29", "text": "...", "options": ["doğru", "…"], "tr_text": "...", "tr_options": [...],
                 "explanation_tr": "...", "explanation_en": "...", "answer_verification": [{"url": "https://…", "section": "…"}]}],
   "inceleme": {"CAD#119": "neden"},   "disi": {"CAD#136": "neden"},   "var": {"TR#5": 16068}}

`uret`, hiçbir karar verilmemiş ve otomatik sınıflanamayan küme kalırsa DURUR: her ham soru ya mevcut
bir soruyla eşleşmeli, ya seçilmeli, ya da gerekçeyle elenmeli. Otomatik kurallar yalnız kesin olanları
sınıflar (aynı soru + aynı şıklar; helikopter; şekil/ek gerektiren).
"""

import collections
import json
import math
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "atpl.db"
HAM = ROOT / "data" / "kaynaklar" / "_ham"
KISA = {"TR": "x-traficom-lapl-ppl", "CAD": "x-cad-rs", "SY": "x-sonyaklasma", "TC": "x-tc-tp13014",
        "AU": "x-austrocontrol-ecqb-ppl"}
TERS = {v: k for k, v in KISA.items()}
STOP = set("the a an of to in is are and or for on at by be with that this it as from which what following statement "
           "correct true false one all any should shall will can may must has have been was were when than then its "
           "their not no yes if do does who where during upon into also only".split())
HELI = re.compile(r"\b(helicopter|rotor|collective|cyclic|swash|autorotation|blade tip|retreating blade|tail rotor|"
                  r"coriolis force)\b", re.I)
SEKIL = re.compile(r"(see fig|refer to the appendix|\(see (lapl|fig)|LAPL/PPL 0\d0-\d|Appendix|VNC|"
                   r"WEATHER SYNOPSIS|Refer to the VNC)", re.I)


def toks(t):
    t = re.sub(r"[^a-z0-9.°%+\- ]", " ", (t or "").lower())
    out = []
    for w in t.split():
        w = w.strip(".-")
        if w and w not in STOP:
            out.append(w)
    return out


def vec(stem, ans, opts):
    c = collections.Counter()
    for w in toks(stem):
        c[w] += 1.0
    for w in toks(ans):
        c[w] += 1.5
    for w in toks(opts):
        c[w] += 0.3
    return c


class Banka:
    def __init__(self):
        conn = sqlite3.connect(DB)
        self.q = []
        for qid, sc, dup, lang, t, ten in conn.execute(
                "select id,subject_code,dup_of,lang,text,text_en from questions"):
            en = t if lang == "en" else ten
            if not en:
                continue
            o = [(x[0] if lang == "en" else x[1]) for x in conn.execute(
                "select text,text_en from options where question_id=? order by ord", (qid,))]
            if any(v is None for v in o):
                continue
            self.q.append({"id": qid, "ders": sc, "dup": dup, "t": en, "o": o, "ans": o[0]})
        conn.close()
        docs = [vec(b["t"], b["ans"], " ".join(b["o"])) for b in self.q]
        df = collections.Counter()
        for d in docs:
            df.update(d.keys())
        self.N = len(docs)
        self.idf = {w: math.log((self.N + 1) / (c + 0.5)) for w, c in df.items()}
        self.v = [self.norm(d) for d in docs]
        self.inv = collections.defaultdict(list)
        for i, v in enumerate(self.v):
            for w in v:
                self.inv[w].append(i)
        self.opt_tokens = [set(toks(" ".join(b["o"]))) for b in self.q]

    def norm(self, d):
        v = {w: c * self.idf.get(w, math.log(self.N + 1)) for w, c in d.items()}
        n = math.sqrt(sum(x * x for x in v.values())) or 1
        return {w: x / n for w, x in v.items()}

    def komsular(self, stem, ans, opts, k=3):
        v = self.norm(vec(stem, ans, opts))
        sc = collections.Counter()
        for w, x in v.items():
            for i in self.inv.get(w, ()):
                sc[i] += x * self.v[i][w]
        ot = set(toks(opts))
        out = []
        for i, s in sc.most_common(k):
            bt = self.opt_tokens[i]
            oj = len(ot & bt) / len(ot | bt) if ot and bt else 0.0
            out.append((s, oj, self.q[i]))
        return out

    def kanonik(self, qid):
        for b in self.q:
            if b["id"] == qid:
                return b["dup"] or qid
        return qid


def etiket(m):
    return f"{TERS.get(m['kaynak'], m['kaynak'])}#{m['no']}"


def kumeleri_yukle(ders):
    d = json.loads((HAM / f"_esleme_{ders}.json").read_text(encoding="utf-8"))
    return d


def ust_uye(k):
    return sorted(k["uyeler"], key=lambda m: (m["dogru"] is None, m["kaynak"] != "x-cad-rs"))[0]


def liste(ders, a, b, ust, filtre):
    bank = Banka()
    d = kumeleri_yukle(ders)
    for i, k in enumerate(d["kumeler"][a:b], a):
        u = ust_uye(k)
        key = u["siklar"][u["dogru"]] if u["dogru"] is not None else None
        nb = bank.komsular(u["metin"], key or "", " ".join(u["siklar"]))
        if nb and nb[0][0] >= ust:
            continue
        if filtre and not re.search(filtre, u["metin"] + " " + " ".join(u["siklar"]), re.I):
            continue
        src = ",".join(etiket(m) for m in k["uyeler"])
        opts = " | ".join(f"{'abcde'[j]}){s[:60]}" for j, s in enumerate(u["siklar"]))
        print(f"{i:04d} {src} {('[anahtar:' + key[:40] + '] ') if key else ''}S: {u['metin'][:200]}\n   {opts}")
        for s, oj, bq in nb:
            if s >= 0.28:
                print(f"   ~{bq['id']}({bq['ders']}){'d' if bq['dup'] else ''} {s:.2f}/{oj:.2f}: "
                      f"{bq['t'][:90]} => {bq['ans'][:60]}")


def ara(pat, ders=None):
    conn = sqlite3.connect(DB)
    rx = re.compile(pat, re.I)
    n = 0
    for qid, sc, dup, lang, t, ten in conn.execute(
            "select id,subject_code,dup_of,lang,text,text_en from questions order by id"):
        if ders and sc != ders:
            continue
        en = t if lang == "en" else (ten or t)
        o = [(x[0] if lang == "en" else (x[1] or x[0])) for x in conn.execute(
            "select text,text_en from options where question_id=? order by ord", (qid,))]
        if rx.search(en + " " + " ".join(o)):
            print(f"{qid}({sc}){'d' if dup else ''} {en[:140]} => {o[0][:70]}")
            n += 1
    print(f"-- {n} eşleşme")


def uret(ders, secim_yol, acik_mod=False, acik_ust=0.0):
    secim = json.loads(Path(secim_yol).read_text(encoding="utf-8"))
    bank = Banka()
    esl = kumeleri_yukle(ders)
    ham = {}
    for p in HAM.glob(f"*__{ders}.json"):
        dd = json.loads(p.read_text(encoding="utf-8"))
        for i, q in enumerate(dd["sorular"]):
            ham[f"{dd['kaynak']}__{dd['ders']}#{i}"] = {**q, "kaynak": dd["kaynak"], "url": dd["url"]}
    # üye etiketi → küme
    etiket_kume, kumeler = {}, []
    for k in esl["kumeler"]:
        kumeler.append(k)
        for m in k["uyeler"]:
            etiket_kume[etiket(m)] = k
    var_kume = collections.defaultdict(list)       # bank_id → ham üyeler (matcher 'var')
    for v in esl["var"]:
        var_kume[v["bank_id"]].append(v)

    def kume_bul(tag):
        if tag not in etiket_kume:
            sys.exit(f"hata: {tag} hiçbir kümede yok")
        return etiket_kume[tag]

    adaylar, kararlar, islenen = [], [], set()

    def karar(m, status, reason, **ek):
        key = f"{m['kaynak']}:{m['no']}"
        if key in islenen:
            return
        islenen.add(key)
        url = m.get("url") or ham.get(m.get("k", ""), {}).get("url", "")
        kararlar.append({"source": m["kaynak"], "no": str(m["no"]), "page": str(m.get("sayfa") or ""),
                         "url": url, "key": key, "status": status, "reason": reason, **ek})

    # 1) seçilen yeni sorular
    for y in secim.get("yeni", []):
        k = kume_bul(y["uye"])
        temsil = next(m for m in k["uyeler"] if etiket(m) == y["uye"])
        tkey = f"{temsil['kaynak']}:{temsil['no']}"
        adaylar.append({
            "key": tkey, "section": y.get("bolum") or secim.get("bolum") or f"{ders}-EK",
            "text": y["text"], "options": y["options"], "tr_text": y["tr_text"], "tr_options": y["tr_options"],
            "explanation_en": y["explanation_en"], "explanation_tr": y["explanation_tr"],
            "answer_verification": y["answer_verification"], "adapted": True,
            "adaptation_note": "Bağımsız anlatım: kaynak sorusunun metni aktarılmadı; kavram, ders notuyla ve "
                               "belirtilen dayanakla doğrulandı. SHGM çıkmış sorusu değildir.",
            "sources": [{"source": m["kaynak"], "url": m.get("url") or ham[m["k"]]["url"], "no": str(m["no"]),
                         "page": str(m.get("sayfa") or "")} for m in k["uyeler"]]})
        for m in k["uyeler"]:
            if etiket(m) == y["uye"]:
                karar(m, "new", y.get("neden", "Bankada aynı kavramı soran soru yok; ders notunda var."))
            else:
                karar(m, "duplicate_new", "Yeni adayla aynı kavram; kelime/şık sırası farkı ayrı soru gerektirmiyor.",
                      representative_key=tkey)
        for tag in y.get("ek_uyeler", []):        # aynı soruyu soran, kümeye girmemiş başka kayıtlar
            k2 = kume_bul(tag)
            adaylar[-1]["sources"] += [{"source": m["kaynak"], "url": m.get("url") or ham[m["k"]]["url"],
                                        "no": str(m["no"]), "page": str(m.get("sayfa") or "")} for m in k2["uyeler"]]
            for m in k2["uyeler"]:
                karar(m, "duplicate_new", "Yeni adayla aynı kavram; kelime/şık sırası farkı ayrı soru gerektirmiyor.",
                      representative_key=tkey)
    # 2) elle verilen kararlar
    for tag, bid in secim.get("var", {}).items():
        for m in kume_bul(tag)["uyeler"]:
            karar(m, "existing", "Aynı soru bankada var; kaynak bilgisi mevcut kimliğe eklenir.", bank_id=int(bid))
    for tag, neden in secim.get("inceleme", {}).items():
        for m in kume_bul(tag)["uyeler"]:
            karar(m, "review", neden)
    for tag, neden in secim.get("disi", {}).items():
        for m in kume_bul(tag)["uyeler"]:
            karar(m, "out_of_scope", neden)
    # 3) matcher 'var' (anahtarlı + aynı cevap)
    for bid, uyeler in var_kume.items():
        for v in uyeler:
            m = {"kaynak": v["kaynak"], "no": v["no"], "sayfa": v.get("sayfa"), "url": v.get("url"), "k": v.get("k")}
            karar(m, "existing", "Aynı soru ve aynı cevap bankada var; kaynak bilgisi mevcut kimliğe eklenir.",
                  bank_id=int(bid))
    # 4) otomatik: yakın komşu (aynı soru + aynı şık kümesi), helikopter, şekil
    bekleyen, varsayilanlar = [], []
    for k in kumeler:
        if all(f"{m['kaynak']}:{m['no']}" in islenen for m in k["uyeler"]):
            continue
        u = ust_uye(k)
        key = u["siklar"][u["dogru"]] if u["dogru"] is not None else None
        metin = u["metin"] + " " + " ".join(u["siklar"])
        nb = bank.komsular(u["metin"], key or "", " ".join(u["siklar"]))
        if nb and nb[0][0] >= 0.70 and nb[0][1] >= 0.50:
            bq = nb[0][2]
            for m in k["uyeler"]:
                karar(m, "existing", "Aynı soru bankada var (soru kökü ve şıklar birebir örtüşüyor).",
                      bank_id=bank.kanonik(bq["id"]))
        elif HELI.search(metin):
            for m in k["uyeler"]:
                karar(m, "out_of_scope", "Helikopter sorusu: PPL(A) kapsamı ve ders notu dışında.")
        elif SEKIL.search(u["metin"]):
            for m in k["uyeler"]:
                karar(m, "out_of_scope", "Şekil, grafik, harita ya da ek gerektiriyor; çizimi üretilmeden "
                                         "aktif soruya çevrilemez.")
        elif secim.get("varsayilan_disi") and not acik_mod:
            # Tek tek okunmuş, eklenmesine karar verilmemiş kümeler: kayıt dışı kalmasın diye ortak gerekçe
            for m in k["uyeler"]:
                karar(m, "out_of_scope", secim["varsayilan_disi"])
            varsayilanlar.append(k)
        else:
            bekleyen.append(k)
    if bekleyen:
        if acik_mod:
            gizli = 0
            for k in bekleyen:
                u = ust_uye(k)
                key = u["siklar"][u["dogru"]] if u["dogru"] is not None else None
                nb = bank.komsular(u["metin"], key or "", " ".join(u["siklar"]))
                if acik_ust and nb and nb[0][0] >= acik_ust and nb[0][1] >= 0.2:
                    gizli += 1                      # bankada benzer soru var: aynı konu
                    continue
                src = ",".join(etiket(m) for m in k["uyeler"])
                opts = " | ".join(f"{'abcde'[j]}){x[:60]}" for j, x in enumerate(u["siklar"]))
                opts = " | ".join(f"{'abcde'[j]}){x[:45]}" for j, x in enumerate(u["siklar"]))
                print(f"{src} {('[anahtar:' + key[:35] + '] ') if key else ''}S: {u['metin'][:150]}\n   {opts}")
                for sc_, oj, bq in nb[:2]:
                    if sc_ >= 0.35:
                        print(f"   ~{bq['id']}({bq['ders']}){'d' if bq['dup'] else ''} {sc_:.2f}/{oj:.2f}: "
                              f"{bq['t'][:80]} => {bq['ans'][:45]}")
            print(f"-- {len(bekleyen)} açık küme" + (f" ({gizli} tanesi bankada benzeri olduğu için gizlendi)" if gizli else ""))
            return
        print(f"HATA: {len(bekleyen)} küme için karar yok — seçim dosyasına ekle:", file=sys.stderr)
        for k in bekleyen:
            u = ust_uye(k)
            print(f"  {','.join(etiket(m) for m in k['uyeler'])}: {u['metin'][:110]}", file=sys.stderr)
        sys.exit(1)
    kaynaklar = sorted({m["source"] for m in kararlar})
    doc = {"schema_version": 1, "checked_at": secim.get("tarih", ""), "sources": [{"id": s} for s in kaynaklar],
           "decisions": kararlar, "candidates": adaylar,
           "notes": "scripts/kaynak_karar_olustur.py ile üretildi; seçim kayıtları data/kaynaklar/decisions/"
                    f"{ders}_secim.json."}
    out = ROOT / "data" / "kaynaklar" / "decisions" / f"{ders}_ek.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    say = collections.Counter(d["status"] for d in kararlar)
    print(f"{out.relative_to(ROOT)}: {len(kararlar)} karar {dict(say)}; {len(adaylar)} aday"
          + (f"; {len(varsayilanlar)} küme ortak gerekçeyle elendi" if varsayilanlar else ""))


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "liste":
        ders = a[1]
        sayilar = [x for x in a[2:] if x.isdigit()]
        ust = float(a[a.index("--ust") + 1]) if "--ust" in a else 2.0
        filtre = a[a.index("--filtre") + 1] if "--filtre" in a else None
        lo, hi = (int(sayilar[0]), int(sayilar[1])) if len(sayilar) >= 2 else (0, 10 ** 6)
        liste(ders, lo, hi, ust, filtre)
    elif a[0] == "ara":
        ara(a[1], a[2] if len(a) > 2 else None)
    elif a[0] == "uret":
        uret(a[1], a[2])
    elif a[0] == "acik":                          # kararı olmayan kümeleri komşularıyla göster
        uret(a[1], a[2], acik_mod=True, acik_ust=float(a[a.index("--ust") + 1]) if "--ust" in a else 0.0)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
