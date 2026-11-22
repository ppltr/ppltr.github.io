#!/usr/bin/env python3
"""data/aciklamalar/*.json çevrimdışı açıklamalarını ve ipuçlarını doğrular.

    python3 scripts/check_aciklamalar.py           # tüm açıklama dosyalarını denetler
    python3 scripts/check_aciklamalar.py 030       # 030 için %100 kapsamı ayrıca kontrol eder
"""

import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "atpl.db"
EXP_DIR = ROOT / "data" / "aciklamalar"

BAD_MD = re.compile(r"\*\*|__|```|^#{1,6}\s", re.M)
BAD_OPT = re.compile(
    r"\b([A-E]\s+şıkkı|[A-E]\s+seçeneği|doğru\s+şık\s+[A-E]|option\s+[A-E]|choice\s+[A-E])\b",
    re.I,
)


def main() -> None:
    if not EXP_DIR.exists():
        sys.exit(f"hata: {EXP_DIR} yok")

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    all_ids = {r[0] for r in conn.execute("SELECT id FROM questions")}

    seen: dict[int, str] = {}
    errors: list[str] = []
    total = 0

    for path in sorted(EXP_DIR.glob("*.json")):
        if path.name.startswith("_"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data.get("aciklamalar", {})
        if not isinstance(items, dict):
            errors.append(f"{path.name}: 'aciklamalar' sözlük değil")
            continue
        for sid, item in items.items():
            if not str(sid).isdigit():
                errors.append(f"{path.name}: geçersiz id {sid!r}")
                continue
            qid = int(sid)
            if qid not in all_ids:
                errors.append(f"{path.name}: {qid} veritabanında yok")
                continue
            if qid in seen:
                errors.append(f"{path.name}: {qid} zaten {seen[qid]} içinde")
                continue
            seen[qid] = path.name
            total += 1
            for field in ("ipucu", "tr", "en"):
                val = item.get(field)
                if not isinstance(val, str) or len(val.strip()) < 20:
                    errors.append(f"{path.name}: {qid}.{field} eksik veya çok kısa")
                    continue
                if BAD_MD.search(val):
                    errors.append(f"{path.name}: {qid}.{field} markdown işareti içeriyor")
                if BAD_OPT.search(val):
                    errors.append(f"{path.name}: {qid}.{field} şık harfine atıf yapıyor")

    req_subjects = sys.argv[1:] or ["030"]
    for code in req_subjects:
        rows = conn.execute(
            "SELECT id FROM questions WHERE subject_code = ? "
            "OR id IN (SELECT question_id FROM question_subjects WHERE subject_code = ?)",
            (code, code),
        ).fetchall()
        expected = {r[0] for r in rows}
        missing = sorted(expected - set(seen))
        if missing:
            errors.append(f"ders {code}: {len(missing)} soruda açıklama eksik: {missing[:10]}")
        else:
            print(f"ders {code}: {len(expected)}/{len(expected)} soru açıklamalı ve ipuçlu ✓")

    conn.close()
    print(f"toplam denetlenen açıklama: {total}")
    if errors:
        for e in errors[:30]:
            print("HATA:", e, file=sys.stderr)
        sys.exit(f"{len(errors)} hata bulundu")


if __name__ == "__main__":
    main()
