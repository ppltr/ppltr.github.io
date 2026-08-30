#!/usr/bin/env python3
"""atpl.db'yi web/template.html içine gömerek web/atpl-soru-bankasi.html üretir.

    python3 scripts/build_web.py

Sonra aynı dosya yolunu Artifact olarak yeniden yayımla — link değişmez.
Şıklar veritabanındaki sırayla (doğru cevap ilk) gömülür; karıştırma tarayıcıda,
çalışma anında yapılır.
"""

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "atpl.db"
TPL = ROOT / "web" / "template.html"
OUT = ROOT / "web" / "atpl-soru-bankasi.html"
PAGES = ROOT / "docs" / "index.html"        # GitHub Pages /docs kökünden yayımlar
NOTES_DIR = ROOT / "notes"

# Ders notu dosyasındaki kod, soru bankasındaki ders koduna eşlenir
FIG_DIR = ROOT / "figures"
FBCONF = ROOT / "web" / "firebase-config.json"
NOTE_SUBJECT = {"073": "070"}
NOTE_SKIP = {"annex-kart-promptlari.md"}    # üretim promptları, çalışma notu değil


def export_notes() -> list:
    """notes/*.md dosyalarını başlık + ders koduyla birlikte toplar."""
    out = []
    if not NOTES_DIR.exists():
        return out
    for f in sorted(NOTES_DIR.glob("*.md")):
        if f.name in NOTE_SKIP:
            continue
        text = f.read_text(encoding="utf-8")
        title = text.lstrip().split("\n", 1)[0].lstrip("# ").strip() or f.stem
        code = f.name[:3]
        if f.name.startswith("annex"):
            subject = "010"                  # ICAO Annex'leri Air Law dersine ait
        else:
            subject = NOTE_SUBJECT.get(code, code if code.isdigit() else "")
        out.append({"f": f.name, "t": title, "s": subject, "md": text})
    return out


def export_figures() -> tuple[dict, dict]:
    """figures/index.json + SVG'leri okur.

    Döner: ({çizim_adı: svg}, {soru_id: çizim_adı}).  Aynı çizimi paylaşan
    sorular tek kopya taşır; artifact'ta yer kaybı olmaz.
    """
    idx_path = FIG_DIR / "index.json"
    if not idx_path.exists():
        return {}, {}
    by_q = json.loads(idx_path.read_text(encoding="utf-8"))
    svgs = {}
    for name in set(by_q.values()):
        f = FIG_DIR / f"{name}.svg"
        if not f.exists():
            sys.exit(f"hata: {f} yok — scripts/make_figures.py çalıştır")
        svgs[name] = f.read_text(encoding="utf-8").strip()
    return svgs, by_q


def export() -> dict:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    subjects, subj_idx, sec_idx = [], {}, {}
    for r in conn.execute(
            "SELECT code, name, name_tr, name_en, level FROM subjects ORDER BY code"):
        subj_idx[r["code"]] = len(subjects)
        d = {"c": r["code"], "n": r["name"], "lv": r["level"] or "ppl", "sec": []}
        if r["name_tr"]:
            d["nt"] = r["name_tr"]          # Türkçe ders adı
        if r["name_en"]:
            d["ne"] = r["name_en"]          # İngilizce ders adı (kaynağı Türkçe olanlar)
        subjects.append(d)

    # Bölüm satırı: [kod, kaynak ad, Türkçe ad, İngilizce ad] — sondakiler boş olabilir
    for r in conn.execute(
            "SELECT subject_code, code, name, name_tr, name_en FROM sections "
            "ORDER BY subject_code, code"):
        s = subjects[subj_idx[r["subject_code"]]]
        sec_idx[(r["subject_code"], r["code"])] = len(s["sec"])
        sat = [r["code"], r["name"], r["name_tr"] or "", r["name_en"] or ""]
        while len(sat) > 2 and not sat[-1]:
            sat.pop()
        s["sec"].append(sat)

    figs, fig_of = export_figures()
    eksik = [q["id"] for q in conn.execute(
        "SELECT id FROM questions WHERE needs_figure = 1")
        if str(q["id"]) not in fig_of]
    if eksik:
        print(f"uyarı: şekli olmayan {len(eksik)} soru: "
              + ", ".join(str(x) for x in eksik[:10]), file=sys.stderr)

    qs = []
    ceviri = ceviri_en = 0
    for r in conn.execute(
        "SELECT q.id, q.subject_code, s.code AS sec, q.text, q.text_tr, q.text_en, q.lang, q.flagged, "
        "       (q.dup_of IS NOT NULL) AS dup, (q.origin = 'uretilmis') AS gen, "
        "       q.needs_figure AS fig "
        "FROM questions q LEFT JOIN sections s ON s.id = q.section_id "
        "ORDER BY q.subject_code, s.code, q.id"
    ):
        rows = conn.execute(
            "SELECT text, text_tr, text_en FROM options WHERE question_id = ? ORDER BY ord",
            (r["id"],)).fetchall()
        opts = [o["text"] for o in rows]
        row = [r["id"], subj_idx[r["subject_code"]],
               sec_idx.get((r["subject_code"], r["sec"]), 0),
               r["text"], opts, r["flagged"] or 0, r["dup"], r["gen"],
               r["fig"] or 0, fig_of.get(str(r["id"]), "")]
        # 10-11: Türkçe metin+şıklar, 12-13: İngilizce metin+şıklar.
        # Kaynak dilin alanı boş bırakılır (q[3]/q[4] zaten o dildedir).
        tr_var = bool(r["text_tr"]) and all(o["text_tr"] for o in rows)
        en_var = bool(r["text_en"]) and all(o["text_en"] for o in rows)
        row += [r["text_tr"] if tr_var else "", [o["text_tr"] for o in rows] if tr_var else ""]
        row += [r["text_en"] if en_var else "", [o["text_en"] for o in rows] if en_var else ""]
        while len(row) > 10 and not row[-1]:
            row.pop()
        if tr_var or r["lang"] == "tr":
            ceviri += 1
        if en_var or r["lang"] != "tr":
            ceviri_en += 1
        qs.append(row)
    conn.close()
    return {"s": subjects, "q": qs, "n": export_notes(), "fg": figs,
            "tr": ceviri, "en": ceviri_en}


def main() -> None:
    if not TPL.exists():
        sys.exit(f"hata: {TPL} yok")

    data = export()
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # </script> dizisi JSON içinde geçerse script bloğunu erken kapatır
    blob = blob.replace("</", "<\\/")

    # Firebase web yapılandırması — yoksa bulut katmanı kapalı kalır.
    # Bu değerler sır değildir, istemcide görünmeleri normaldir; erişimi
    # firestore.rules kısıtlar.
    fb = "null"
    if FBCONF.exists():
        try:
            conf = json.loads(FBCONF.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            sys.exit(f"hata: {FBCONF} bozuk JSON")
        eksik = [k for k in ("apiKey", "authDomain", "projectId", "appId")
                 if not conf.get(k)]
        if eksik:
            sys.exit(f"hata: {FBCONF} eksik alan: {', '.join(eksik)}")
        fb = json.dumps(conf, ensure_ascii=False, separators=(",", ":"))

    tpl = TPL.read_text(encoding="utf-8")
    for yer in ("__DATA__", "__FIREBASE__"):
        if yer not in tpl:
            sys.exit(f"hata: şablonda {yer} yer tutucusu yok")

    html = tpl.replace("__DATA__", blob).replace("__FIREBASE__", fb)
    OUT.write_text(html, encoding="utf-8")
    PAGES.parent.mkdir(parents=True, exist_ok=True)
    PAGES.write_text(html, encoding="utf-8")
    kb = OUT.stat().st_size / 1024
    print(f"{OUT}  ({len(data['q'])} soru (TR {data['tr']}, EN {data['en']}), {len(data['s'])} ders, "
          f"{len(data['n'])} not, {len(data['fg'])} çizim, {kb:.1f} KB"
          + (", bulut açık)" if fb != "null" else ", bulut kapalı)"))
    print(f"{PAGES}  (GitHub Pages için aynı dosya)")


if __name__ == "__main__":
    main()
