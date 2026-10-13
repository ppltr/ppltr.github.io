#!/usr/bin/env python3
"""ATPL soru bankası veritabanını oluşturur ve JSON dosyalarını içe aktarır.

Kullanım:
    python3 scripts/init_db.py                       # data/ altındaki tüm JSON'ları yükler
    python3 scripts/init_db.py data/501_*.json       # sadece verilen dosyaları yükler

Betik idempotenttir: aynı dosya tekrar yüklenirse sorular güncellenir, çoğaltılmaz.
"""

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "atpl.db"
DATA_DIR = ROOT / "data"
TR_DIR = DATA_DIR / "tr"          # soruların Türkçe hâli
EN_DIR = DATA_DIR / "en"          # soruların İngilizce hâli (kaynağı Türkçe olanlar için)
# Her sorunun iki dilde de karşılığı olmalı: kaynağı İngilizceyse data/tr/ içinde
# Türkçesi, kaynağı Türkçeyse data/en/ içinde İngilizcesi durur. Böylece seçilen
# dil ne olursa olsun bütün sorular o dilde gelir, kip içinde karışma olmaz.

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS subjects (
    code  TEXT PRIMARY KEY,             -- ör. '501'
    name  TEXT NOT NULL,                -- ör. 'Havacılığa Giriş'
    level TEXT NOT NULL DEFAULT 'ppl'   -- 'ppl' | 'atpl'  (banka şu an tümüyle PPL)
);

CREATE TABLE IF NOT EXISTS sections (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_code TEXT NOT NULL REFERENCES subjects(code) ON DELETE CASCADE,
    code         TEXT NOT NULL,         -- ör. '01-01'
    name         TEXT NOT NULL,
    UNIQUE (subject_code, code)
);

CREATE TABLE IF NOT EXISTS questions (
    id           INTEGER PRIMARY KEY,   -- kaynaktaki soru ID'si (ATPL TV)
    subject_code TEXT NOT NULL REFERENCES subjects(code) ON DELETE CASCADE,
    section_id   INTEGER REFERENCES sections(id) ON DELETE SET NULL,
    text         TEXT NOT NULL,
    explanation  TEXT,                  -- sonradan not eklemek için
    source       TEXT,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS options (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    ord         INTEGER NOT NULL,       -- 1..5
    label       TEXT NOT NULL,          -- A, B, C, D, E
    text        TEXT NOT NULL,
    is_correct  INTEGER NOT NULL DEFAULT 0,
    UNIQUE (question_id, ord)
);

-- Dış kaynak kaydı (data/kaynaklar/_kaynaklar.json) ve soru ↔ kaynak bağı.
-- Aynı soru birden çok kaynakta geçebilir; mevcut soruya yeni kaynak eklenir, soru çoğaltılmaz.
CREATE TABLE IF NOT EXISTS sources (
    id     TEXT PRIMARY KEY,            -- ör. 'gdh-ppla'
    name   TEXT NOT NULL,
    url    TEXT,
    kind   TEXT,                        -- 'pdf' | 'web' | 'scribd' ...
    access TEXT,                        -- 'acik' | 'kismi' | 'engelli'
    note   TEXT                         -- kullanım/telif notu
);
CREATE TABLE IF NOT EXISTS question_sources (
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    source_id   TEXT    NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    ref         TEXT    NOT NULL DEFAULT '',   -- kaynaktaki soru no
    page        TEXT,                          -- sayfa / bölüm
    url         TEXT,                          -- soruya özel adres (yoksa kaynağınki)
    PRIMARY KEY (question_id, source_id, ref)
);
-- Aynı kimliği farklı bir dersin çalışma kapsamında da gösterir; soru/ilerleme çoğalmaz.
CREATE TABLE IF NOT EXISTS question_subjects (
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    subject_code TEXT NOT NULL REFERENCES subjects(code) ON DELETE CASCADE,
    section_code TEXT,
    PRIMARY KEY (question_id, subject_code)
);

CREATE INDEX IF NOT EXISTS idx_questions_subject ON questions(subject_code);
CREATE INDEX IF NOT EXISTS idx_questions_section ON questions(section_id);
CREATE INDEX IF NOT EXISTS idx_options_question  ON options(question_id);
CREATE INDEX IF NOT EXISTS idx_options_correct   ON options(question_id, is_correct);

-- Soru + doğru cevabı tek satırda veren görünüm.
-- Kaynak şıkları doğru cevap başta veriyor: doğru cevap her zaman A.
DROP VIEW IF EXISTS v_sorular;
CREATE VIEW v_sorular AS
SELECT q.id                        AS soru_id,
       q.subject_code              AS ders,
       s.code                      AS bolum,
       s.name                      AS bolum_adi,
       q.text                      AS soru,
       o.label                     AS dogru_sik,
       o.text                      AS dogru_cevap
FROM questions q
LEFT JOIN sections s ON s.id = q.section_id
LEFT JOIN options  o ON o.question_id = q.id AND o.is_correct = 1;

-- Şıkları kaynak sırasıyla, tek tek satır olarak veren görünüm
DROP VIEW IF EXISTS v_quiz;
CREATE VIEW v_quiz AS
SELECT q.id                        AS soru_id,
       q.subject_code              AS ders,
       s.code                      AS bolum,
       q.text                      AS soru,
       o.label                     AS sik,
       o.text                      AS sik_metni,
       o.is_correct                AS dogru_mu
FROM questions q
LEFT JOIN sections s ON s.id = q.section_id
JOIN options o ON o.question_id = q.id
ORDER BY q.id, o.ord;
"""

FTS_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS questions_fts
USING fts5(text, content='questions', content_rowid='id', tokenize='unicode61');
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    try:
        conn.executescript(FTS_SCHEMA)
    except sqlite3.OperationalError:
        print("uyarı: FTS5 mevcut değil, tam metin arama tablosu atlandı")
    migrate(conn)
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    """Var olan veritabanına sonradan eklenen sütunlar."""
    scols = {r[1] for r in conn.execute("PRAGMA table_info(subjects)")}
    if "level" not in scols:
        conn.execute("ALTER TABLE subjects ADD COLUMN level TEXT NOT NULL DEFAULT 'ppl'")

    cols = {r[1] for r in conn.execute("PRAGMA table_info(questions)")}
    if "origin" not in cols:
        # 'banka' = gerçek sınav sorusu, 'uretilmis' = ders notundan üretilmiş
        conn.execute("ALTER TABLE questions ADD COLUMN origin TEXT NOT NULL DEFAULT 'banka'")
    if "needs_figure" not in cols:
        # soru bir şekle/diyagrama atıf yapıyor; görsel olmadan cevaplanamaz
        conn.execute("ALTER TABLE questions ADD COLUMN needs_figure INTEGER NOT NULL DEFAULT 0")
    if "dup_of" not in cols:
        # aynı sorunun kopyasıysa kanonik sorunun id'si
        conn.execute("ALTER TABLE questions ADD COLUMN dup_of INTEGER")
    if "flagged" not in cols:
        # kaynakta "Attention!" işaretli sorular: cevabı tartışmalı olabilir
        conn.execute("ALTER TABLE questions ADD COLUMN flagged INTEGER NOT NULL DEFAULT 0")
    if "text_tr" not in cols:
        # Türkçe çeviri; boşsa uygulama kaynak metne düşer
        conn.execute("ALTER TABLE questions ADD COLUMN text_tr TEXT")
    if "text_en" not in cols:
        # İngilizce çeviri; kaynağı Türkçe olan sorular için
        conn.execute("ALTER TABLE questions ADD COLUMN text_en TEXT")
    if "lang" not in cols:
        # sorunun **kaynak** dili: 'en' (sınav raporu) | 'tr' (ders notu, 501, 502).
        # Kaynağı Türkçe olan sorunun çeviriye ihtiyacı yoktur.
        conn.execute("ALTER TABLE questions ADD COLUMN lang TEXT NOT NULL DEFAULT 'en'")

    if "mark" not in cols:
        # 'dogrulanmis' = kullanıcı bu soruyu sınavda gördüğünü doğruladı (⭐);
        # 'aday' = hatırlanan konuya benzer aday, kesin metin eşleşmesi yok.
        # Hiçbiri resmî SHGM çıkmış sorusu değildir.
        conn.execute("ALTER TABLE questions ADD COLUMN mark TEXT")
    if "review" not in cols:
        # 1 = inceleme kuyruğunda (belirsiz soru): puanlanan turlara asla girmez
        conn.execute("ALTER TABLE questions ADD COLUMN review INTEGER NOT NULL DEFAULT 0")
    if "review_note" not in cols:
        conn.execute("ALTER TABLE questions ADD COLUMN review_note TEXT")
    if "explanation_en" not in cols:
        conn.execute("ALTER TABLE questions ADD COLUMN explanation_en TEXT")

    ocols = {r[1] for r in conn.execute("PRAGMA table_info(options)")}
    if "text_tr" not in ocols:
        conn.execute("ALTER TABLE options ADD COLUMN text_tr TEXT")
    if "text_en" not in ocols:
        conn.execute("ALTER TABLE options ADD COLUMN text_en TEXT")

    if "name_tr" not in scols:
        conn.execute("ALTER TABLE subjects ADD COLUMN name_tr TEXT")
    if "name_en" not in scols:
        conn.execute("ALTER TABLE subjects ADD COLUMN name_en TEXT")

    seccols = {r[1] for r in conn.execute("PRAGMA table_info(sections)")}
    if "name_tr" not in seccols:
        conn.execute("ALTER TABLE sections ADD COLUMN name_tr TEXT")
    if "name_en" not in seccols:
        conn.execute("ALTER TABLE sections ADD COLUMN name_en TEXT")
    if "section_code" not in {r[1] for r in conn.execute("PRAGMA table_info(question_subjects)")}:
        conn.execute("ALTER TABLE question_subjects ADD COLUMN section_code TEXT")

    conn.commit()



def apply_duplicates(conn: sqlite3.Connection) -> int:
    """data/_tekrarlar.json'daki grupları uygular: gruptaki ilk id kanonik sayılır."""
    path = DATA_DIR / "_tekrarlar.json"
    conn.execute("UPDATE questions SET dup_of = NULL")
    if not path.exists():
        return 0
    groups = json.loads(path.read_text(encoding="utf-8"))["gruplar"]
    n = 0
    for g in groups:
        ids = g["ids"]
        canon = ids[0]
        for other in ids[1:]:
            cur = conn.execute(
                "UPDATE questions SET dup_of = ? WHERE id = ? AND dup_of IS NULL", (canon, other))
            n += cur.rowcount
    conn.commit()
    return n


def import_file(conn: sqlite3.Connection, path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))

    subject_code = data["subject_code"]
    conn.execute(
        "INSERT INTO subjects(code, name, level) VALUES (?, ?, ?) "
        "ON CONFLICT(code) DO UPDATE SET name = excluded.name, level = excluded.level",
        (subject_code, data["subject_name"], data.get("level", "ppl")),
    )

    # Bölümler: ya tek bölüm (section_code/section_name) ya da {kod: ad} sözlüğü.
    sections = dict(data.get("sections", {}))
    if data.get("section_code"):
        sections[data["section_code"]] = data.get("section_name", "")

    section_ids: dict[str, int] = {}
    for code, name in sections.items():
        conn.execute(
            "INSERT INTO sections(subject_code, code, name) VALUES (?, ?, ?) "
            "ON CONFLICT(subject_code, code) DO UPDATE SET name = excluded.name",
            (subject_code, code, name),
        )
        section_ids[code] = conn.execute(
            "SELECT id FROM sections WHERE subject_code = ? AND code = ?",
            (subject_code, code),
        ).fetchone()[0]

    default_section = data.get("section_code")
    source = data.get("source")
    origin = data.get("origin", "banka")
    lang = data.get("lang", "en")           # kaynak dil, dosya düzeyinde
    labels = "ABCDE"

    # Önce bütün dosyayı doğrula; hatalı bir anahtar kısmi içe aktarıma yol açmasın.
    for q in data["questions"]:
        opts = q.get("options")
        if not isinstance(opts, list) or not 2 <= len(opts) <= 5 or any(
                not isinstance(o, str) or not o.strip() for o in opts):
            sys.exit(f"hata: soru {q.get('id')}: 2–5 dolu şık gerekli")
        if not q.get("inceleme") and (type(q.get("correct_index", 0)) is not int or
                                       q.get("correct_index", 0) != 0):
            sys.exit(f"hata: soru {q.get('id')}: doğrulanmış doğru cevap A/0 olmalı")

    for q in data["questions"]:
        code = q.get("section", default_section)
        if code and code not in section_ids:
            sys.exit(f"hata: soru {q['id']} tanımsız bölüme işaret ediyor: {code}")

        conn.execute(
            "INSERT INTO questions(id, subject_code, section_id, text, source, flagged, origin, "
            "                      needs_figure, lang, review, review_note) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET subject_code = excluded.subject_code, "
            "section_id = excluded.section_id, text = excluded.text, "
            "source = excluded.source, flagged = excluded.flagged, origin = excluded.origin, "
            "needs_figure = excluded.needs_figure, lang = excluded.lang, "
            "review = excluded.review, review_note = excluded.review_note",
            (q["id"], subject_code, section_ids.get(code), q["text"], source,
             1 if q.get("flagged") else 0, q.get("origin", origin),
             1 if q.get("needs_figure") else 0, q.get("lang", lang),
             1 if q.get("inceleme") else 0, q.get("inceleme_nedeni")),
        )
        # Şıklar her içe aktarımda yeniden yazılır (sıra/metin düzeltmeleri için)
        conn.execute("DELETE FROM options WHERE question_id = ?", (q["id"],))
        # Belirsiz bir soruda ilk şık doğru sayılmaz. Bu kayıtlar yalnız inceleme içindir.
        correct_index = None if q.get("inceleme") else 0
        for i, opt in enumerate(q["options"]):
            conn.execute(
                "INSERT INTO options(question_id, ord, label, text, is_correct) VALUES (?, ?, ?, ?, ?)",
                (q["id"], i + 1, labels[i], opt, 1 if i == correct_index else 0),
            )

    conn.commit()
    return len(data["questions"])


def prune_removed(conn: sqlite3.Connection, keep: set[int]) -> int:
    """JSON'dan çıkarılmış soruları veritabanından da düşürür.

    data/*.json tek doğruluk kaynağıdır; bir soru dosyadan silinince atpl.db'de
    kalması onu uygulamaya geri sokardı. Yalnız tam içe aktarımda (dosya adı
    verilmeden) çalışır — tek dosya güncellenirken öteki derslerin soruları
    "eksik" sanılmasın. Şıklar ON DELETE CASCADE ile gider.
    """
    rows = conn.execute("SELECT id FROM questions").fetchall()
    gone = [r[0] for r in rows if r[0] not in keep]
    if gone:
        conn.executemany("DELETE FROM questions WHERE id = ?", [(i,) for i in gone])
        conn.execute("UPDATE questions SET dup_of = NULL WHERE dup_of IS NOT NULL "
                     "AND dup_of NOT IN (SELECT id FROM questions)")
        conn.commit()
    return len(gone)


def import_translations(conn: sqlite3.Connection) -> tuple[int, int]:
    """data/tr/ ve data/en/ içindeki çevirileri sorulara ve şıklara yazar.

    Şıklar **sırayla** eşlenir: kaynakta doğru cevap ilk sıradadır, çeviri de
    aynı sırayı taşımak zorundadır. Sayı tutmuyorsa dosya reddedilir — sessizce
    yanlış şıkka doğru cevap etiketi yapıştırmaktansa derleme dursun.

    Döner: (Türkçesi olan soru sayısı, İngilizcesi olan soru sayısı).
    """
    conn.execute("UPDATE questions SET text_tr = NULL, text_en = NULL")
    conn.execute("UPDATE options SET text_tr = NULL, text_en = NULL")
    sayim = {"tr": 0, "en": 0}

    for dil, klasor in (("tr", TR_DIR), ("en", EN_DIR)):
        if not klasor.exists():
            continue
        qcol, ocol = f"text_{dil}", f"text_{dil}"
        ders = klasor / "_dersler.json"
        if ders.exists():
            d = json.loads(ders.read_text(encoding="utf-8"))
            for code, ad in d.get("subjects", {}).items():
                conn.execute(f"UPDATE subjects SET name_{dil} = ? WHERE code = ?", (ad, code))
            for code, ad in d.get("sections", {}).items():
                conn.execute(f"UPDATE sections SET name_{dil} = ? WHERE code = ?", (ad, code))

        for path in sorted(klasor.glob("*.json")):
            if path.name.startswith("_"):
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            for sid, tr in data.get("questions", {}).items():
                qid = int(sid)
                row = conn.execute("SELECT id FROM questions WHERE id = ?", (qid,)).fetchone()
                if row is None:
                    sys.exit(f"hata: {path.name} bilinmeyen soru id'si çeviriyor: {qid}")
                opts = conn.execute(
                    "SELECT id FROM options WHERE question_id = ? ORDER BY ord", (qid,)).fetchall()
                tops = tr.get("options", [])
                if len(tops) != len(opts):
                    sys.exit(f"hata: {path.name} soru {qid}: {len(tops)} şık çevrilmiş, "
                             f"kaynakta {len(opts)} şık var")
                if not tr.get("text", "").strip() or any(not t.strip() for t in tops):
                    sys.exit(f"hata: {path.name} soru {qid}: boş çeviri")
                conn.execute(f"UPDATE questions SET {qcol} = ? WHERE id = ?", (tr["text"], qid))
                for (oid,), t in zip(opts, tops):
                    conn.execute(f"UPDATE options SET {ocol} = ? WHERE id = ?", (t, oid))
                sayim[dil] += 1
    conn.commit()
    return sayim["tr"], sayim["en"]


def import_notes(conn: sqlite3.Connection) -> tuple[int, int, int]:
    """Dış kaynak kaydını ve soru notlarını yazar.

    data/kaynaklar/_kaynaklar.json  → `sources`
    data/_kaynak_notlari.json       → soru başına kaynak bağı, kısa açıklama (TR/EN) ve
                                      işaret (`dogrulanmis` ⭐ / `aday`)

        {"notlar": {"61001": {"src": [{"k": "gdh-ppla", "no": "57", "sayfa": "p.4", "url": "…"}],
                              "tr": "Kısa açıklama.", "en": "Short explanation.",
                              "isaret": "dogrulanmis"}}}

    Bilinmeyen soru id'si ya da kayıtta olmayan kaynak derlemeyi durdurur: sessizce
    kaybolan bir kaynak bilgisi, "bu soru nereden geldi" sorusunu cevapsız bırakır.
    Döner: (kaynak sayısı, kaynak bağı sayısı, notlu soru sayısı).
    """
    reg_path = DATA_DIR / "kaynaklar" / "_kaynaklar.json"
    notes_path = DATA_DIR / "_kaynak_notlari.json"
    n_src = n_link = n_note = 0
    registry = json.loads(reg_path.read_text(encoding="utf-8"))["kaynaklar"] if reg_path.exists() else []
    notes = json.loads(notes_path.read_text(encoding="utf-8"))["notlar"] if notes_path.exists() else {}
    kayitli = {r[0] for r in conn.execute("SELECT id FROM sources")} | {k["id"] for k in registry}
    # Kaynak eklemek, mevcut (veya bu dosyada yer almayan) açıklamaları silmez.
    # Bütün bağımlılıklar yazmadan önce kontrol edilir.
    for sid, n in notes.items():
        qid = int(sid)
        if conn.execute("SELECT 1 FROM questions WHERE id = ?", (qid,)).fetchone() is None:
            sys.exit(f"hata: _kaynak_notlari.json bilinmeyen soru id'si: {qid}")
        if n.get("isaret") not in (None, "dogrulanmis", "aday"):
            sys.exit(f"hata: soru {qid}: geçersiz işaret {n.get('isaret')!r}")
        for s in n.get("src", []):
            if s["k"] not in kayitli:
                sys.exit(f"hata: soru {qid}: kayıtta olmayan kaynak {s['k']!r}")
        for code in n.get("also_subjects", []):
            if conn.execute("SELECT 1 FROM subjects WHERE code=?", (code,)).fetchone() is None:
                sys.exit(f"hata: soru {qid}: bilinmeyen ortak ders {code!r}")
        for code, section in n.get("also_sections", {}).items():
            if code not in n.get("also_subjects", []) or not conn.execute(
                    "SELECT 1 FROM sections WHERE subject_code=? AND code=?", (code, section)).fetchone():
                sys.exit(f"hata: soru {qid}: bilinmeyen ortak ders bölümü {code}/{section}")
    if reg_path.exists():
        for k in registry:
            conn.execute(
                "INSERT INTO sources(id, name, url, kind, access, note) VALUES (?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET name=excluded.name, url=excluded.url, "
                "kind=excluded.kind, access=excluded.access, note=excluded.note",
                (k["id"], k["ad"], k.get("url"), k.get("tur"), k.get("erisim"), k.get("kullanim_notu")))
            kayitli.add(k["id"])
            n_src += 1
    if notes_path.exists():
        for sid, n in notes.items():
            qid = int(sid)
            if conn.execute("SELECT 1 FROM questions WHERE id = ?", (qid,)).fetchone() is None:
                sys.exit(f"hata: _kaynak_notlari.json bilinmeyen soru id'si: {qid}")
            isaret = n.get("isaret")
            if isaret not in (None, "dogrulanmis", "aday"):
                sys.exit(f"hata: soru {qid}: geçersiz işaret {isaret!r}")
            for key, column in (("isaret", "mark"), ("tr", "explanation"), ("en", "explanation_en")):
                if key in n:              # null açıkça yazılırsa alan silinebilir
                    conn.execute(f"UPDATE questions SET {column} = ? WHERE id = ?", (n[key], qid))
            if "also_subjects" in n:
                conn.execute("DELETE FROM question_subjects WHERE question_id=?", (qid,))
                for code in n["also_subjects"]:
                    if code == conn.execute("SELECT subject_code FROM questions WHERE id=?", (qid,)).fetchone()[0]:
                        continue  # Kendi dersine ikinci bir ortak-ders kaydı ekleme.
                    section = n.get("also_sections", {}).get(code)
                    conn.execute("INSERT OR IGNORE INTO question_subjects(question_id,subject_code,section_code) VALUES (?,?,?)", (qid, code, section))
                    if not section:
                        conn.execute("INSERT OR IGNORE INTO sections(subject_code,code,name,name_tr,name_en) "
                                     "VALUES (?,?,?,?,?)", (code, f"{code}-X", "Shared questions", "Ortak sorular", "Shared questions"))
            n_note += 1
            if n.get("replace_sources"):
                # Derlenmiş tam liste açıkça yetkiliyse kaldırılan/yanlış eski atıfları da temizle.
                # Kısmi not güncellemelerinde var olan diğer kaynak bağları korunur.
                conn.execute("DELETE FROM question_sources WHERE question_id=?", (qid,))
            for s in n.get("src", []):
                if s["k"] not in kayitli:
                    sys.exit(f"hata: soru {qid}: kayıtta olmayan kaynak {s['k']!r}")
                conn.execute(
                    "INSERT INTO question_sources(question_id, source_id, ref, page, url) "
                    "VALUES (?, ?, ?, ?, ?) ON CONFLICT(question_id, source_id, ref) "
                    "DO UPDATE SET page=excluded.page, url=excluded.url",
                    (qid, s["k"], str(s.get("no", "")), s.get("sayfa"), s.get("url")))
                n_link += 1
    conn.commit()
    return n_src, n_link, n_note


def rebuild_fts(conn: sqlite3.Connection) -> None:
    try:
        conn.execute("INSERT INTO questions_fts(questions_fts) VALUES ('rebuild')")
        conn.commit()
    except sqlite3.OperationalError:
        pass


def main() -> None:
    paths = [Path(p) for p in sys.argv[1:]] or sorted(
        f for f in DATA_DIR.glob("*.json") if not f.name.startswith("_"))
    if not paths:
        sys.exit(f"hata: {DATA_DIR} içinde JSON bulunamadı")

    conn = connect()
    total = 0
    for path in paths:
        n = import_file(conn, path)
        total += n
        print(f"{path.name}: {n} soru içe aktarıldı")

    if len(sys.argv) == 1:                    # tam içe aktarım: JSON'da olmayan gider
        keep: set[int] = set()
        for path in paths:
            keep.update(q["id"] for q in json.loads(path.read_text(encoding="utf-8"))["questions"])
        gone = prune_removed(conn, keep)
        if gone:
            print(f"JSON'dan çıkarılmış {gone} soru veritabanından düşürüldü")

    dups = apply_duplicates(conn)
    ceviri, ceviri_en = import_translations(conn)
    n_src, n_link, n_note = import_notes(conn)
    rebuild_fts(conn)

    q = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    o = conn.execute("SELECT COUNT(*) FROM options").fetchone()[0]
    uret = conn.execute("SELECT COUNT(*) FROM questions WHERE origin = 'uretilmis'").fetchone()[0]
    trsrc = conn.execute("SELECT COUNT(*) FROM questions WHERE lang = 'tr'").fetchone()[0]
    missing = conn.execute(
        "SELECT COUNT(*) FROM questions q "
        "WHERE NOT EXISTS (SELECT 1 FROM options o WHERE o.question_id = q.id AND o.is_correct = 1)"
    ).fetchone()[0]
    ek = conn.execute("SELECT COUNT(*) FROM questions WHERE origin = 'ek'").fetchone()[0]
    inc = conn.execute("SELECT COUNT(*) FROM questions WHERE review = 1").fetchone()[0]
    yil = conn.execute("SELECT COUNT(*) FROM questions WHERE mark = 'dogrulanmis'").fetchone()[0]
    adayn = conn.execute("SELECT COUNT(*) FROM questions WHERE mark = 'aday'").fetchone()[0]
    conn.close()

    print(f"\n{DB_PATH}: toplam {q} soru, {o} şık")
    print(f"  {dups} tekrar işaretlendi → {q - dups} benzersiz soru")
    print(f"  {uret} soru ders notundan üretilmiş")
    print(f"  {ek} soru ek kaynaklardan eklendi ({inc} soru inceleme kuyruğunda)")
    print(f"  {n_src} kaynak kaydı, {n_link} soru↔kaynak bağı, {n_note} notlu soru "
          f"(⭐ doğrulanmış {yil}, benzer aday {adayn})")
    print(f"  Türkçe: {ceviri} çeviri + {trsrc} zaten Türkçe = {ceviri + trsrc}/{q}")
    print(f"  İngilizce: {ceviri_en} çeviri + {q - trsrc} zaten İngilizce = {ceviri_en + q - trsrc}/{q}")
    eksik_tr, eksik_en = q - (ceviri + trsrc), q - (ceviri_en + q - trsrc)
    if eksik_tr or eksik_en:
        print(f"  UYARI: Türkçe {eksik_tr}, İngilizce {eksik_en} soru eksik — "
              f"o sorular kip içinde diğer dilde görünür")
    if missing:
        print(f"UYARI: {missing} sorunun doğru cevabı işaretlenmemiş")


if __name__ == "__main__":
    main()
