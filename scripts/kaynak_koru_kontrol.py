#!/usr/bin/env python3
"""Ek soru çalışmasının mevcut soruları bozmadığını doğrular.

    python3 scripts/kaynak_koru_kontrol.py [temel_db]     # varsayılan: git'teki ae0aeb2 sürümü

Temel veritabanındaki HER soru (kimlik, ders, bölüm kodu, metin, çeviriler, tekrar bağı, kaynak/
şekil bayrakları, şıkların sırası ve doğru şık) güncel veritabanında birebir aynı kalmalı.
Çözüm geçmişi tarayıcıda soru kimliğine bağlıdır; kimlik ve içerik değişmediği sürece korunur.
Yeni sorular ek kimlik bantlarında (61xxx-69xxx) ya da kullanıcının onayladığı
sınav hatırlatma dosyasında kayıtlı kimliklerde olabilir.
"""

import json
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMEL_SURUM = "ae0aeb2"      # Air Law genişletmesinden önceki, 2.934 soruluk banka


def satirlar(db: Path) -> dict:
    c = sqlite3.connect(db)
    out = {}
    for r in c.execute(
            "SELECT q.id, q.subject_code, s.code, q.text, q.text_tr, q.text_en, q.dup_of, q.origin, "
            "q.needs_figure, q.flagged, q.lang FROM questions q LEFT JOIN sections s ON s.id = q.section_id"):
        sik = c.execute("SELECT text, text_tr, text_en, is_correct FROM options WHERE question_id = ? "
                        "ORDER BY ord", (r[0],)).fetchall()
        out[r[0]] = (r[1:], tuple(sik))
    c.close()
    return out


def main() -> None:
    if len(sys.argv) > 1:
        temel = Path(sys.argv[1])
    else:
        tmp = Path(tempfile.mkdtemp()) / "temel.db"
        tmp.write_bytes(subprocess.run(["git", "show", f"{TEMEL_SURUM}:atpl.db"], cwd=ROOT,
                                       capture_output=True, check=True).stdout)
        temel = tmp
    eski, yeni = satirlar(temel), satirlar(ROOT / "atpl.db")
    bozuk = [i for i in eski if i not in yeni or yeni[i] != eski[i]]
    ekler = sorted(set(yeni) - set(eski))
    hatirlatma_dosyasi = ROOT / "data" / "050_sinav_hatirlatma_sorulari.json"
    hatirlatma_idleri = {
        q["id"] for q in json.loads(hatirlatma_dosyasi.read_text(encoding="utf-8"))["questions"]
    } if hatirlatma_dosyasi.exists() else set()
    bant_disi = [i for i in ekler if not 61000 < i < 70000 and i not in hatirlatma_idleri]
    dogru_a = [i for i in yeni if sum(o[3] for o in yeni[i][1]) != 1 or yeni[i][1][0][3] != 1]
    print(f"temel {len(eski)} soru · güncel {len(yeni)} · eklenen {len(ekler)}")
    print(f"değişen/silinen mevcut soru: {len(bozuk)}" + (f"  → {bozuk[:10]}" if bozuk else "  ✓"))
    print(f"ek bant dışı yeni kimlik: {len(bant_disi)}" + (f"  → {bant_disi[:10]}" if bant_disi else "  ✓"))
    print(f"doğru cevabı A olmayan soru: {len(dogru_a)}" + (f"  → {dogru_a[:10]}" if dogru_a else "  ✓"))
    if bozuk or bant_disi or dogru_a:
        sys.exit(1)


if __name__ == "__main__":
    main()
