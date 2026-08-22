#!/usr/bin/env python3
"""Şekilleri geriye doğru teyit için kontak sayfası üretir.

Her çizimi sorusunun ve doğru şıkkının yanına koyar; şekle bakıp cevabın
çizimden okunabildiği doğrulanır. Ayrıca şekil gerektirip çizimi olmayan
soruları listeler.

    python3 scripts/check_figures.py        → figures/_kontrol.html
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "atpl.db"
FIGDIR = ROOT / "figures"
OUT = FIGDIR / "_kontrol.html"

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#eceff3;color:#111;
  font:15px/1.55 ui-sans-serif,system-ui,Segoe UI,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:26px 20px 70px}
h1{font-size:26px;margin:0 0 4px;letter-spacing:-.02em}
.sub{color:#555;margin:0 0 22px;font-size:14px}
.miss{background:#ffe9e0;border:1px solid #d97a4c;border-radius:8px;
  padding:12px 14px;margin-bottom:20px;font-size:14px}
.ok{background:#e2f0e8;border:1px solid #4c9b73;border-radius:8px;
  padding:12px 14px;margin-bottom:20px;font-size:14px}
.card{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;
  background:#fff;border:1px solid #ccd3db;border-radius:10px;
  padding:16px;margin-bottom:16px;align-items:start}
@media (max-width:820px){.card{grid-template-columns:1fr}}
.fig{background:#fff;border:1px solid #e0e5ea;border-radius:8px;padding:8px}
.fig svg{display:block;width:100%;height:auto}
.meta{font:12px ui-monospace,SFMono-Regular,Menlo,monospace;color:#667;
  margin-bottom:6px}
.q{font-weight:600;margin:0 0 10px;font-size:15.5px}
ol{margin:0;padding-left:0;list-style:none;counter-reset:o}
li{counter-increment:o;position:relative;padding-left:26px;margin-bottom:4px;
  font-size:14px;color:#445}
li::before{content:counter(o,upper-alpha);position:absolute;left:0;top:0;
  width:19px;height:19px;display:grid;place-items:center;font-size:11px;
  border:1px solid #ccd3db;border-radius:5px;
  font-family:ui-monospace,Menlo,monospace}
li.right{color:#14532d;font-weight:600}
li.right::before{background:#2f7d52;color:#fff;border-color:#2f7d52}
.share{font-size:12px;color:#667;margin-top:10px}
"""


def main() -> None:
    if not DB.exists():
        sys.exit("atpl.db yok — önce scripts/init_db.py çalıştır")
    idx = json.loads((FIGDIR / "index.json").read_text(encoding="utf-8"))

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT q.id, q.subject_code, s.name AS sec, q.text "
        "FROM questions q LEFT JOIN sections s ON s.id = q.section_id "
        "WHERE q.needs_figure = 1 ORDER BY q.subject_code, q.id").fetchall()

    missing = [r["id"] for r in rows if str(r["id"]) not in idx]
    extra = [k for k in idx if not any(str(r["id"]) == k for r in rows)]

    # aynı çizimi paylaşan sorular
    shared: dict[str, list[int]] = {}
    for qid, name in idx.items():
        shared.setdefault(name, []).append(int(qid))

    parts = [f"<style>{CSS}</style><div class='wrap'>",
             "<h1>Şekil teyidi</h1>",
             f"<p class='sub'>{len(rows)} soru şekil gerektiriyor · "
             f"{len(set(idx.values()))} çizim üretildi</p>"]

    if missing:
        parts.append(f"<div class='miss'><b>Çizimi olmayan {len(missing)} soru:</b> "
                     + ", ".join(str(m) for m in missing) + "</div>")
    else:
        parts.append("<div class='ok'><b>Şekil gerektiren her sorunun çizimi var.</b> "
                     "Aşağıda her çizimin yanında sorusu ve doğru şıkkı duruyor — "
                     "cevabın çizimden okunabildiğini teyit et.</div>")
    if extra:
        parts.append(f"<div class='miss'><b>Karşılığı olmayan eşleme:</b> "
                     + ", ".join(extra) + "</div>")

    for r in rows:
        name = idx.get(str(r["id"]))
        fig = ((FIGDIR / f"{name}.svg").read_text(encoding="utf-8")
               if name else "<i>çizim yok</i>")
        opts = conn.execute(
            "SELECT label, text, is_correct FROM options "
            "WHERE question_id = ? ORDER BY ord", (r["id"],)).fetchall()
        lis = "".join(
            f"<li class='{'right' if o['is_correct'] else ''}'>{o['text']}</li>"
            for o in opts)
        others = [x for x in shared.get(name, []) if x != r["id"]]
        share = (f"<div class='share'>aynı çizim: "
                 + ", ".join(str(x) for x in others) + "</div>") if others else ""
        parts.append(
            f"<div class='card'><div class='fig'>{fig}</div><div>"
            f"<div class='meta'>{r['subject_code']} · {r['sec'] or ''} · "
            f"id {r['id']} · {name or '—'}</div>"
            f"<p class='q'>{r['text']}</p><ol>{lis}</ol>{share}</div></div>")

    parts.append("</div>")
    OUT.write_text("<!doctype html><meta charset='utf-8'>"
                   "<title>Şekil teyidi</title>" + "".join(parts), encoding="utf-8")
    print(f"{OUT}  ({len(rows)} soru, eksik: {len(missing)})")
    if missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
