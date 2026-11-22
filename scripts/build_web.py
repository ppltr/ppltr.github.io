#!/usr/bin/env python3
"""atpl.db'yi web/template.html içine gömerek web/atpl-soru-bankasi.html üretir.

    python3 scripts/build_web.py

Sonra aynı dosya yolunu Artifact olarak yeniden yayımla — link değişmez.
Şıklar veritabanındaki sırayla (doğru cevap ilk) gömülür; karıştırma tarayıcıda,
çalışma anında yapılır.
"""

import base64
import hashlib
import json
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "atpl.db"
TPL = ROOT / "web" / "template.html"
OUT = ROOT / "web" / "atpl-soru-bankasi.html"
PAGES = ROOT / "docs" / "index.html"        # GitHub Pages /docs kökünden yayımlar
NOTES_DIR = ROOT / "notes"
SOURCE_DIR = ROOT / "data" / "kaynaklar"
ICONS_DIR = ROOT / "web" / "icons"       # site ikonu kaynağı; docs/ köküne kopyalanır
SEO_DIR = ROOT / "web" / "seo"

# Ders notu dosyasındaki kod, soru bankasındaki ders koduna eşlenir
FIG_DIR = ROOT / "figures"
FBCONF = ROOT / "web" / "firebase-config.json"
NOTE_SUBJECT = {"073": "070"}
NOTE_SKIP = {"annex-kart-promptlari.md", "hava_hukuku_1_TASLAK.md"}    # üretim promptları, çalışma notu değil


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
    for name in sorted(set(by_q.values())):
        f = FIG_DIR / f"{name}.svg"
        if not f.exists():
            sys.exit(f"hata: {f} yok — scripts/make_figures.py çalıştır")
        svgs[name] = f.read_text(encoding="utf-8").strip()
    return svgs, by_q


def export_extras(conn) -> tuple[dict, dict]:
    """Soru başına ek bilgi (ek kaynak, ⭐/aday işareti, inceleme, ipucu, açıklama, kaynaklar).

    Döner: ({soru_id: {...}}, {kaynak_id: [ad, adres]}).  Satır düzenine (q[0..13]) dokunmaz;
    uygulama bunu id ile ayrı bir sözlükten okur. Anahtarlar kısa tutulur:
      o=1 ek kaynak sorusu · k='d' ⭐ doğrulanmış / 'a' benzer aday · r=1 inceleme kuyruğu
      rn inceleme nedeni · h çevrimdışı ipucu · e/ee Türkçe/İngilizce açıklama · s=[[kaynak_id, no, sayfa, adres]]
    """
    qcols = {r[1] for r in conn.execute("PRAGMA table_info(questions)")}
    has_hint = "hint" in qcols
    hint_sel = "q.hint" if has_hint else "NULL AS hint"
    hint_where = " OR q.hint IS NOT NULL" if has_hint else ""
    x: dict = {}
    for r in conn.execute(
            f"SELECT q.id, q.mark, q.review, q.review_note, {hint_sel}, q.explanation, q.explanation_en, "
            "       (q.origin = 'ek') AS ek "
            "FROM questions q "
            "WHERE q.mark IS NOT NULL OR q.review = 1 OR q.explanation IS NOT NULL "
            f"   OR q.explanation_en IS NOT NULL{hint_where} OR q.origin = 'ek' "
            "   OR EXISTS (SELECT 1 FROM question_sources s WHERE s.question_id = q.id) "
            "   OR EXISTS (SELECT 1 FROM question_subjects a WHERE a.question_id = q.id)"):
        d = {}
        if r["ek"]:
            d["o"] = 1
        if r["mark"]:
            d["k"] = "d" if r["mark"] == "dogrulanmis" else "a"
        if r["review"]:
            d["r"] = 1
            if r["review_note"]:
                d["rn"] = r["review_note"]
        if r["hint"]:
            d["h"] = r["hint"]
        if r["explanation"]:
            d["e"] = r["explanation"]
        if r["explanation_en"]:
            d["ee"] = r["explanation_en"]
        x[r["id"]] = d
    for r in conn.execute("SELECT question_id,subject_code FROM question_subjects ORDER BY question_id,subject_code"):
        x.setdefault(r["question_id"], {}).setdefault("a", []).append(r["subject_code"])
    kullanilan = {r["id"]: [r["name"], r["url"] or ""]
                  for r in conn.execute("SELECT id, name, url FROM sources ORDER BY id")}
    for r in conn.execute(
            "SELECT s.question_id, s.source_id, s.ref, s.page, s.url, src.name, src.url AS surl "
            "FROM question_sources s JOIN sources src ON src.id = s.source_id "
            "ORDER BY s.question_id, s.source_id, s.ref"):
        sat = [r["source_id"], r["ref"] or "", r["page"] or "", r["url"] or ""]
        while len(sat) > 2 and not sat[-1]:
            sat.pop()
        x.setdefault(r["question_id"], {}).setdefault("s", []).append(sat)
        kullanilan[r["source_id"]] = [r["name"], r["surl"] or ""]
    return x, kullanilan


def export_review_queue(conn) -> list:
    """Belirsiz adayları ayrı, cevap işaretlemeyen okuma paneline aktarır."""
    out = []
    for path in sorted(SOURCE_DIR.glob("inceleme_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data.get("sorular", data.get("kuyruk", [])):
            normalized = {"ders": data.get("ders", ""), **item}
            if item.get("kaynak") and not item.get("kaynaklar"):
                normalized["kaynaklar"] = [{"k": item["kaynak"], "no": item.get("no"),
                                             "sayfa": item.get("sayfa"), "url": item.get("url")}]
            out.append(normalized)
    # Önceki içe aktarımlardaki review kayıtları da aktif sorulara karışmaz.
    for row in conn.execute("SELECT id, subject_code, text, review_note FROM questions WHERE review=1"):
        out.append({"ders": row["subject_code"], "kume": str(row["id"]),
                    "metin": row["text"], "neden": row["review_note"],
                    "siklar": [r[0] for r in conn.execute(
                        "SELECT text FROM options WHERE question_id=? ORDER BY ord", (row["id"],))],
                    "kaynaklar": [{"k": r[0], "no": r[1], "sayfa": r[2], "url": r[3]}
                        for r in conn.execute("SELECT source_id, ref, page, url FROM question_sources "
                                              "WHERE question_id=?", (row["id"],))]})
    return out


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
        "FROM questions q LEFT JOIN sections s ON s.id = q.section_id WHERE q.review=0 "
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
    ekstra, kaynaklar = export_extras(conn)
    review_queue = export_review_queue(conn)
    conn.close()
    return {"s": subjects, "q": qs, "n": export_notes(), "fg": figs,
            "tr": ceviri, "en": ceviri_en, "x": ekstra, "ks": kaynaklar, "rq": review_queue}


SW_FILES = (
    "index.html",
    "site.webmanifest",
    "favicon.svg",
    "favicon.ico",
    "apple-touch-icon.png",
    "icon-192.png",
    "icon-512.png",
    "icon-maskable-512.png",
)

SW_TEMPLATE = """// Otomatik üretildi (scripts/build_web.py) — elle düzenleme.
const CACHE = 'ppl-offline-__VER__';
const FONT_CACHE = 'ppl-fonts-v1';
const CORE = __CORE__;

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await Promise.all(CORE.map(async url => {
      const res = await fetch(new Request(url, { cache: 'reload' }));
      if (!res.ok) throw new Error('Precache failed: ' + url + ' (' + res.status + ')');
      await cache.put(url, res);
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys
      .filter(k => k.startsWith('ppl-offline-') && k !== CACHE)
      .map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('message', event => {
  const msg = event.data;
  if (!msg || typeof msg !== 'object') return;
  if (msg.type === 'SKIP_WAITING') {
    self.skipWaiting();
    return;
  }
  if (msg.type === 'CACHE_CHECK' && event.ports && event.ports[0]) {
    event.waitUntil((async () => {
      try {
        const cache = await caches.open(CACHE);
        const hit = await cache.match('./index.html', { ignoreSearch: true });
        const keys = await cache.keys();
        event.ports[0].postMessage({ ready: !!hit, version: CACHE, count: keys.length });
      } catch (e) {
        event.ports[0].postMessage({ ready: false, version: CACHE, count: 0 });
      }
    })());
  }
});

function fetchWithTimeout(request, ms) {
  return new Promise((resolve, reject) => {
    let done = false;
    const timer = setTimeout(() => {
      if (!done) { done = true; reject(new Error('timeout')); }
    }, ms);
    fetch(request).then(res => {
      if (!done) { done = true; clearTimeout(timer); resolve(res); }
    }, err => {
      if (!done) { done = true; clearTimeout(timer); reject(err); }
    });
  });
}

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Google Fonts: önbellekten anında sun; çevrimdışıysa hiç bekletme
  if (url.origin === 'https://fonts.googleapis.com' || url.origin === 'https://fonts.gstatic.com') {
    event.respondWith((async () => {
      const cache = await caches.open(FONT_CACHE);
      const cached = await cache.match(req);
      if (cached) return cached;
      try {
        const res = await fetchWithTimeout(req, 3000);
        if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone());
        return res;
      } catch (e) {
        return new Response('', { status: 504, statusText: 'Offline' });
      }
    })());
    return;
  }

  // Firebase Auth/Firestore ve diğer dış kaynaklara müdahale etme
  if (url.origin !== self.location.origin) return;
  // sw.js güncelleme denetimi her zaman ağa gitsin
  if (url.pathname.endsWith('/sw.js')) return;

  // Sayfa açılışı: uçak/kötü Wi-Fi'da takılmamak için 2 sn ağ, düşerse anında önbellek
  if (req.mode === 'navigate') {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE);
      try {
        const res = await fetchWithTimeout(req, 2000);
        if (res && res.ok && res.type === 'basic' && !res.redirected) {
          cache.put('./index.html', res.clone());
          return res;
        }
      } catch (e) {}
      return (await cache.match('./index.html', { ignoreSearch: true }))
        || (await cache.match('./', { ignoreSearch: true }))
        || Response.error();
    })());
    return;
  }

  // Aynı kaynaklı statik dosyalar (ikonlar, manifest, HTML indirme): önce önbellek
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const cached = await cache.match(req, { ignoreSearch: true });
    if (cached) return cached;
    try {
      const res = await fetch(req);
      if (res && res.ok && res.type === 'basic') cache.put(req, res.clone());
      return res;
    } catch (e) {
      return (await cache.match('./index.html', { ignoreSearch: true })) || Response.error();
    }
  })());
});
"""


def write_service_worker(docs_dir: Path) -> tuple[Path, str]:
    """docs/ içindeki çevrimdışı varlıklardan içerik özetli sw.js üretir."""
    h = hashlib.sha256()
    core = ["./"]
    for name in SW_FILES:
        f = docs_dir / name
        if f.exists():
            h.update(name.encode("utf-8"))
            h.update(b"\0")
            h.update(f.read_bytes())
            h.update(b"\0")
            core.append("./" + name)
    ver = h.hexdigest()[:12]
    sw = SW_TEMPLATE.replace("__VER__", ver).replace(
        "__CORE__", json.dumps(core, ensure_ascii=False))
    sw_path = docs_dir / "sw.js"
    sw_path.write_text(sw, encoding="utf-8")
    return sw_path, ver


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
    for yer in ("__DATA__", "__FIREBASE__", "__FAVICON__"):
        if yer not in tpl:
            sys.exit(f"hata: şablonda {yer} yer tutucusu yok")

    # Favicon satır içi gömülür: tek dosya sürümü (artifact) de ikonu taşısın
    fav = ICONS_DIR / "favicon.svg"
    fav_uri = "data:image/svg+xml;base64," + base64.b64encode(fav.read_bytes()).decode()
    html = tpl.replace("__DATA__", blob).replace("__FIREBASE__", fb).replace("__FAVICON__", fav_uri)
    OUT.write_text(html, encoding="utf-8")
    PAGES.parent.mkdir(parents=True, exist_ok=True)
    PAGES.write_text(html, encoding="utf-8")
    for f in ICONS_DIR.iterdir():               # Pages yalnız docs/ klasörünü yayımlar
        if f.is_file():
            shutil.copy2(f, PAGES.parent / f.name)
    for f in SEO_DIR.iterdir():
        if f.is_file():
            shutil.copy2(f, PAGES.parent / f.name)
    sw_path, sw_ver = write_service_worker(PAGES.parent)
    kb = OUT.stat().st_size / 1024
    print(f"{OUT}  ({len(data['q'])} soru (TR {data['tr']}, EN {data['en']}), {len(data['s'])} ders, "
          f"{len(data['n'])} not, {len(data['fg'])} çizim, {len(data['x'])} ek bilgili soru, {kb:.1f} KB"
          + (", bulut açık)" if fb != "null" else ", bulut kapalı)"))
    print(f"{PAGES}  (GitHub Pages için aynı dosya)")
    print(f"{sw_path}  (çevrimdışı önbellek sürümü: ppl-offline-{sw_ver})")


if __name__ == "__main__":
    main()
