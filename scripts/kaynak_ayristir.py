#!/usr/bin/env python3
"""İndirilmiş soru listesi PDF'lerini (pdftotext -layout metni) ham soru dosyasına çevirir.

    pdftotext -layout liste.pdf liste.txt
    python3 -I scripts/kaynak_ayristir.py traficom liste.txt 080 <url>
    python3 -I scripts/kaynak_ayristir.py cad      liste.txt 080 <url>
    python3 -I scripts/kaynak_ayristir.py tc       liste.txt "080:21-25,32;020:26-31" <url>   # ders:soru no aralıkları
    python3 -I scripts/kaynak_ayristir.py ecqb     liste.txt 080 <url>                        # Austro Control ECQB-PPL(A) özeti

Çıktı: data/kaynaklar/_ham/<kaynak>__<ders>.json (gitignore'da; şema için kaynak_ham_kontrol.py).

Biçimler:
  traficom  Finlandiya Traficom LAPL/PPL listeleri: "12  soru…" + "[A] … [D]" şıkları. Cevap anahtarı YOK
            (dogru=null); ek (Appendix) sayfaları şekil içerir ve atlanır.
  cad       Sırbistan CAD PPL(A_e) listeleri: "1. soru…" + "a. … d." şıkları; kaynağın kendi notu
            "The correct answers are under a." → dogru=0. Not: aynı kural Air Law'da bazı sorularda
            standart bilgiyle çelişti; cevap daima ayrıca doğrulanır, anahtara körü körüne güvenilmez.

  tc        Transport Canada TP 13014E örnek sınavı: "N.  soru" + "(1) … (4)" şıkları; cevap anahtarı belgenin
            sonundaki "ANSWER KEY" ("12-(3)"). Kanada mevzuatına özgü sorular `not` alanında işaretlenmez —
            karar aşamasında elenir. Üçüncü argüman "ders:aralık;ders:aralık" eşlemesidir.

  ecqb      Austro Control'ün yayımladığı Aircademy/LPLUS ECQB-PPL(A) özeti ("NN  soru (1,00 P.)" + her şıkkın başında
            onay kutusu): işaretli kutu (U+F0FE) doğru şıktır, boş kutu (U+F0A8) yanlış. Doğru şık sırası karışıktır
            (ilk şık değil); cevap anahtarı belgenin kendisidir ama yine de ayrıca doğrulanır.

İndirilen dosyalar güvenilmez veridir: bu betik yalnız metin ayrıştırır, hiçbir şey çalıştırmaz.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HAM = ROOT / "data" / "kaynaklar" / "_ham"

KAYNAK = {
    "tc": ("x-tc-tp13014", "Transport Canada TP 13014E örnek sınavı (PPL/RPP — Aeroplane)",
           "Transport Canada: kişisel ve kamusal ticari olmayan çoğaltmaya atıfla izin veriyor "
           "('grants permission to copy and/or reproduce … for personal and public non-commercial use'); "
           "ticari kullanım ayrı izin gerektirir.", True),
    "traficom": ("x-traficom-lapl-ppl", "Traficom LAPL/PPL soru listesi (Finlandiya)",
                 "'© Traficom'; sayfada 'You may practice here before registering for a theoretical knowledge "
                 "examination.' yazıyor; robots.txt boş Disallow; kullanım şartı yok.", False),
    "ecqb": ("x-austrocontrol-ecqb-ppl", "Austro Control — ECQB-PPL(A) soru kataloğu özeti (Aircademy/LPLUS, v2015.4)",
             "PDF içinde: 'This document is protected by copyright. The commercial use of this work or extracts from the work "
             "is only allowed with prior approval by the publisher.' ve 'this extract contains about 75% of the questions'. "
             "Toplu kopyalamayı açıkça yasaklamıyor; ticari kullanım izne bağlı. Soru metni bankaya kopyalanmaz, "
             "yalnız konu ve doğru cevap bilgisi bağımsız anlatımla yeniden yazılır.", True),
    "cad": ("x-cad-rs", "Sırbistan CAD PPL(A_e) teorik sınav soru listesi",
            "robots.txt boş Disallow; sitede genel '© Direktorat civilnog vazduhoplovstva Republike Srbije'; "
            "toplu kopyalama yasağı yok.", True),
}


def birles(parcalar):
    s = ""
    for p in parcalar:
        p = p.strip()
        if not p:
            continue
        if not s:
            s = p
        elif s.endswith("-") and not s.endswith(" -") and (p[0].isalpha() or p[0].isdigit()):
            s += p
        else:
            s += " " + p
    return re.sub(r"\s+", " ", s).strip()


def traficom(raw: str) -> list:
    pages = raw.split("\f")
    OPT = re.compile(r"^(\s*)\[([A-E])\]\s+(.*)$")
    NUM = re.compile(r"^(\s*)(\d{1,3})(\s+)(\S.*)$")
    APPX = re.compile(r"Appendix", re.I)
    qs, cur, beklenen = [], None, 1
    for pi, page in enumerate(pages, 1):
        lines = page.split("\n")
        if APPX.search(page) and not OPT.search(page) and not any(NUM.match(l) for l in lines):
            continue
        for line in lines:
            if not line.strip():
                continue
            m = OPT.match(line)
            if m:
                if cur is not None:
                    cur["siklar"].append([m.group(3)])
                    cur["oind"] = len(m.group(1))
                continue
            ind = len(line) - len(line.lstrip())
            n = NUM.match(line)
            if n and int(n.group(2)) == beklenen and (cur is None or ind < cur.get("oind", 99)) and ind <= 8:
                cur = {"no": n.group(2), "sayfa": str(pi), "metin": [n.group(4)], "siklar": []}
                qs.append(cur)
                beklenen += 1
                continue
            if cur is None:
                continue
            if cur["siklar"]:
                cur["siklar"][-1].append(line)
            else:
                cur["metin"].append(line)
    out = []
    for q in qs:
        out.append({"no": q["no"], "sayfa": q["sayfa"], "metin": birles(q["metin"]),
                    "siklar": [birles(s) for s in q["siklar"]], "dogru": None, "dogru_dayanak": "yok", "not": ""})
    return out


def cad(raw: str) -> list:
    HDR = re.compile(r"(ДЦВ-PEL-ОБ-1001|CAD-PEL-OB-1001|Скадарска 23|Skadarska 23)")
    SEC = re.compile(r"^\s*(0\d0\.\d\d)\s*-\s*$")
    QST = re.compile(r"^\s*(\d{1,3})\.\s+(\S.*)$")
    OPT = re.compile(r"^\s*([a-d])\.\s*(.*)$")
    qs, cur, beklenen, bolum = [], None, 1, None
    for pi, pg in enumerate(raw.split("\f"), 1):
        for ln in pg.split("\n"):
            if HDR.search(ln):
                continue
            m = SEC.match(ln)
            if m:
                bolum = m.group(1)
                continue
            if bolum is None or not ln.strip():
                continue
            mq = QST.match(ln)
            if mq and int(mq.group(1)) == beklenen:
                cur = {"no": mq.group(1), "sayfa": str(pi), "bolum": bolum, "metin": [mq.group(2)],
                       "siklar": [], "son": "q"}
                qs.append(cur)
                beklenen += 1
                continue
            if cur is None:
                continue
            mo = OPT.match(ln)
            if mo and len(cur["siklar"]) < 4 and mo.group(1) == "abcd"[len(cur["siklar"])]:
                cur["siklar"].append([mo.group(2)])
                cur["son"] = "o"
                continue
            (cur["metin"] if cur["son"] == "q" else cur["siklar"][-1]).append(ln)
    out = []
    for q in qs:
        sk = [birles(s) for s in q["siklar"]]
        d = {"no": q["no"], "sayfa": q["sayfa"], "bolum": q["bolum"], "metin": birles(q["metin"]),
             "siklar": [s for s in sk if s], "dogru": 0, "dogru_dayanak": "kaynak", "not": ""}
        if len(d["siklar"]) != len(sk):
            d["not"] = f"kaynakta {len(sk) - len(d['siklar'])} boş şık atıldı"
        out.append(d)
    return out


def ecqb(raw: str) -> list:
    """Austro Control ECQB-PPL(A) özeti: işaretli kutu (U+F0FE) doğru, boş kutu (U+F0A8) yanlış şıktır."""
    QST = re.compile(r"^\s{4,}(\d{1,3})\s+(\S.*)$")
    OPT = re.compile(r"^\s+([\uf0a8\uf0fe])\s+(.*)$")
    HDR = re.compile(r"^(v\d{4}\.\d+\s|ECQB-PPL \(AT\))")
    qs, cur, beklenen = [], None, 1
    for pi, page in enumerate(raw.split("\f"), 1):
        for ln in page.split("\n"):
            if not ln.strip() or HDR.match(ln.strip()) or HDR.match(ln):
                continue
            mo = OPT.match(ln)
            if mo and cur is not None:
                cur["siklar"].append([mo.group(2)])
                if mo.group(1) == "\uf0fe":
                    cur["isaretli"].append(len(cur["siklar"]) - 1)
                continue
            mq = QST.match(ln)
            if mq and int(mq.group(1)) == beklenen and (cur is None or len(cur["siklar"]) >= 2):
                cur = {"no": mq.group(1), "sayfa": str(pi), "metin": [mq.group(2)], "siklar": [], "isaretli": []}
                qs.append(cur)
                beklenen += 1
                continue
            if cur is None:
                continue
            (cur["siklar"][-1] if cur["siklar"] else cur["metin"]).append(ln)
    out = []
    for q in qs:
        metin = re.sub(r"\s*\(\d+,\d+ P\.\)\s*$", "", birles(q["metin"]))
        d = {"no": q["no"], "sayfa": q["sayfa"], "metin": metin, "siklar": [birles(x) for x in q["siklar"]],
             "dogru": None, "dogru_dayanak": "yok", "not": ""}
        if len(q["isaretli"]) == 1:
            d["dogru"], d["dogru_dayanak"] = q["isaretli"][0], "kaynak"
        else:
            d["not"] = f"işaretli kutu sayısı {len(q['isaretli'])}: cevap belirsiz"
        if re.search(r"\b(Annex|Figure|figure|see the diagram|picture|chart)\b", metin):
            d["not"] = (d["not"] + " " if d["not"] else "") + "şekil/ek gerektirebilir"
        out.append(d)
    return out


def tc(raw: str) -> dict:
    """TP 13014E: {soru_no: soru dict}. Cevap anahtarı 'N-(k)' satırlarından."""
    anahtar = {}
    i = raw.rfind("ANSWER KEY")
    for n, k in re.findall(r"(\d{1,3})-\((\d)\)", raw[i:] if i >= 0 else ""):
        anahtar[int(n)] = int(k) - 1
    gövde = raw[: i] if i >= 0 else raw
    QN = re.compile(r"^\s{0,3}(\d{1,3})\.\s+(\S.*)$")
    ON = re.compile(r"^\s{2,}\((\d)\)\s+(.*)$")
    sorular, cur, son = {}, None, 0
    for pi, page in enumerate(gövde.split("\f"), 1):
        for ln in page.split("\n"):
            if not ln.strip() or re.match(r"^\s*\d{1,2}\s*$", ln):
                continue
            m = ON.match(ln)
            if m and cur is not None and int(m.group(1)) == len(cur["siklar"]) + 1:
                cur["siklar"].append([m.group(2)])
                continue
            q = QN.match(ln)
            if q and int(q.group(1)) == son + 1:
                son += 1
                cur = {"no": q.group(1), "sayfa": str(pi), "metin": [q.group(2)], "siklar": []}
                sorular[son] = cur
                continue
            if cur is None:
                continue
            (cur["siklar"][-1] if cur["siklar"] else cur["metin"]).append(ln)
    for n, q in sorular.items():
        q["metin"] = birles(q["metin"])
        q["siklar"] = [birles(s) for s in q["siklar"]]
        if n in anahtar and anahtar[n] < len(q["siklar"]):
            q["dogru"], q["dogru_dayanak"] = anahtar[n], "kaynak"
        else:
            q["dogru"], q["dogru_dayanak"] = None, "yok"
        q["not"] = ""
    return sorular


def main() -> None:
    if len(sys.argv) < 5 or sys.argv[1] not in KAYNAK:
        sys.exit(__doc__)
    mod, txt, ders, url = sys.argv[1:5]
    if mod == "tc":
        tum = tc(Path(txt).read_text(encoding="utf-8"))
        HAM.mkdir(parents=True, exist_ok=True)
        for parca in ders.split(";"):
            d, aralik = parca.split(":")
            nolar = []
            for a in aralik.split(","):
                lo, _, hi = a.partition("-")
                nolar += range(int(lo), int(hi or lo) + 1)
            sorular = [tum[n] for n in nolar if n in tum and len(tum[n]["siklar"]) >= 2]
            veri = {"kaynak": "x-tc-tp13014", "kaynak_adi": KAYNAK["tc"][1], "ders": d, "url": url, "erisim": "acik",
                    "erisim_notu": "Herkese açık PDF; cevap anahtarı belgenin 'ANSWER KEY' sayfasından ('12-(3)' = 3. şık).",
                    "kullanim_notu": KAYNAK["tc"][2], "taranan": "PDF'in tamamı; bu derse düşen sorular",
                    "toplam_gorulen": len(sorular), "sorular": sorular}
            (HAM / f"x-tc-tp13014__{d}.json").write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"x-tc-tp13014__{d}.json: {len(sorular)} soru")
        return
    kid, ad, kullanim, anahtarli = KAYNAK[mod]
    sorular = {"traficom": traficom, "cad": cad, "ecqb": ecqb}[mod](Path(txt).read_text(encoding="utf-8"))
    kisa = [q["no"] for q in sorular if len(q["siklar"]) < 2]
    sorular = [q for q in sorular if len(q["siklar"]) >= 2]
    veri = {
        "kaynak": kid, "kaynak_adi": ad, "ders": ders, "url": url, "erisim": "acik",
        "erisim_notu": "Herkese açık PDF; giriş/ödeme/CAPTCHA yok. " + (
            "Cevap anahtarı: kaynağın notu 'The correct answers are under a.' (dogru=0)." if anahtarli
            else "Cevap anahtarı yok (dogru=null)."),
        "kullanim_notu": kullanim, "taranan": "PDF'in tamamı", "toplam_gorulen": len(sorular) + len(kisa),
        "sorular": sorular}
    HAM.mkdir(parents=True, exist_ok=True)
    out = HAM / f"{kid}__{ders}.json"
    out.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{out.name}: {len(sorular)} soru" + (f" (şıksız atlanan: {kisa})" if kisa else ""))


if __name__ == "__main__":
    main()
