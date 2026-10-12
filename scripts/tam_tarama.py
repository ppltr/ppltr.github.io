#!/usr/bin/env python3
"""Tam kaynak taramasını derler, çapraz kaynak bağlarını çözer ve denetler.

python3 scripts/tam_tarama.py --derle
python3 scripts/tam_tarama.py --rapor

Ham dış soru bankalarını yayımlamaz. İncelenmiş karar manifestlerini kullanır.
Kimlik tahsisi kaynak_derle.py içindedir; bu betik mevcut soruları düzenlemez.
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from kaynak_derle import compile_decisions, question_hash, write

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DECISIONS = DATA / "kaynaklar/decisions"
CODES = ("020", "030", "040", "050", "060", "070", "080", "090")
NAMES = {"020": "Aircraft General Knowledge", "030": "Flight Performance and Planning",
         "040": "Human Performance", "050": "Meteorology", "060": "Navigation",
         "070": "Operational Procedures", "080": "Principles of Flight", "090": "Communications"}
FULL_ROWS = {"020": (471, 1183, 150), "030": (425, 602, 150),
             "040": (385, 859, 150), "050": (424, 744, 150),
             "060": (533, 798, 150), "070": (292, None, 150),
             "080": (440, 17, 150), "090": (274, None, 150)}


def read(path):
    return json.loads(path.read_text())


def paths_for(code):
    old = DECISIONS / f"other_subjects_{code}.json"
    return ([old] if old.exists() else []) + sorted(DECISIONS.glob(f"full*_{code}.json"))


def bank():
    result = {}
    for path in DATA.glob("*.json"):
        doc = read(path)
        for q in doc.get("questions", []):
            if q["id"] in result:
                raise ValueError(f"Bankada çift kimlik: {q['id']}")
            result[q["id"]] = (doc["subject_code"], q)
    return result


def require_full_coverage():
    # Bunlar bu tarihli yayımlanmış dosyaların gerçek satır sayılarıdır;
    # yeni soru kotası değildir. Eksik bir manifest tamamlandı sayılamaz.
    for code, sizes in FULL_ROWS.items():
        for family, count in zip(("subjects", "caab", "linx"), sizes):
            if count is None:
                continue
            path = DECISIONS / f"full_{family}_{code}.json"
            if not path.exists() or len(read(path).get("decisions", [])) != count:
                raise ValueError(f"Tam kaynak taraması eksik: {path.name}, beklenen {count} satır")


def verify_baseline(current=None):
    current = bank() if current is None else current
    baseline = read(DATA / "kaynaklar/baseline_full_20261013.json")["questions"]
    for qid, old_hash in baseline.items():
        if int(qid) not in current or question_hash(current[int(qid)][1]) != old_hash:
            raise ValueError(f"Başlangıçtaki soru değişti veya kayboldu: {qid}")
    return baseline


def resolve_links():
    docs = {p: read(p) for p in DECISIONS.glob("full*.json")}
    ids = {code: read(DATA / f"kaynaklar/idler_{code}.json")["anahtarlar"] for code in CODES}
    existing_keys = {}
    for doc in docs.values():
        for d in doc.get("decisions", []):
            if d["status"] == "existing":
                existing_keys[d.get("key", f"{d['source']}:{d['no']}")] = d["bank_id"]
    active = bank()
    candidate_owners = {c["key"]: c["section"][:3] for doc in docs.values()
                        for c in doc.get("candidates", [])}

    def target(code, key):
        qid = ids.get(code, {}).get(key) or existing_keys.get(key)
        return qid if qid in active else None

    count = 0
    for path, doc in docs.items():
        link_map = {l["representative_key"]: l for l in doc.get("cross_manifest_links", [])}
        for d in doc.get("decisions", []):
            qids = []
            if d.get("covered_candidate_keys"):
                qids = [target(x["subject"], x["key"]) for x in d["covered_candidate_keys"]]
            elif d.get("cross_subject_candidate_key"):
                key = d["cross_subject_candidate_key"]
                code = d.get("cross_subject_code") or candidate_owners.get(key)
                if code is None and key in existing_keys:
                    code = active[existing_keys[key]][0]
                qids = [target(code, key)]
                if code:
                    d["cross_subject_code"] = code
            elif d.get("representative_key") in link_map:
                l = link_map[d["representative_key"]]
                qids = [target(l["target_subject"], l["target_candidate_key"])]
            if not qids or any(qid is None for qid in qids):
                continue
            # Aynı derste yeni aday temsilcisi derleyicide zaten çözülür.
            if d["status"] == "new":
                continue
            d.update(status="existing", bank_id=qids[0],
                     reason="Aynı doğrulanmış kural/koşul mevcut veya bu taramada kabul edilen tek ID ile kapsanır.",
                     reason_tr="Aynı doğrulanmış kural/koşul mevcut veya bu taramada kabul edilen tek ID ile kapsanır.")
            if len(qids) > 1:
                d["additional_bank_ids"] = qids[1:]
                d["reason"] = d["reason_tr"] = "Kaynağın iki farklı konfigürasyonu iki ayrı kayıtla kapsanır; kimlikleri birleştirilmez."
            d.pop("representative_key", None)
            count += 1
        # Eski, elde yazılmış sayaçlar son incelemeden sonra yanıltıcı olmasın.
        stats = dict(Counter(d["status"] for d in doc.get("decisions", [])))
        doc["final_audit_counts"] = {"scanned": len(doc.get("decisions", [])),
                                     "new_candidates": len(doc.get("candidates", [])), "decisions": stats}
        if isinstance(doc.get("audit_totals"), dict):
            totals = doc["audit_totals"]
            for field in ("scanned", "source_questions_scanned"):
                if field in totals:
                    totals[field] = len(doc.get("decisions", []))
            for field in ("unique_new_candidates", "accepted_unique_candidates"):
                if field in totals:
                    totals[field] = len(doc.get("candidates", []))
            for field in ("decision_counts", "counts"):
                if field in totals:
                    totals[field] = stats
        write(path, doc)
    return count


def compile_all():
    # İlk geçiş kimlikleri ve bütün derslerin kayıtlarını oluşturur. İkinci geçiş
    # yalnız artık gerçek bankada bulunan çapraz koşullara kaynak bağlar.
    require_full_coverage()
    baseline = verify_baseline()
    # Mevcut banka sağlam olsa bile bir manifest eski bir kaydı değiştirmeyi
    # planlıyor olabilir. Bu tarihli tarama başlamadan önceki kayıtlara yapılan
    # böyle bir düzeltmeyi, ilk dosya yazılmadan yakala.
    for code in CODES:
        ledger_path = DATA / f"kaynaklar/idler_{code}.json"
        ledger = read(ledger_path)["anahtarlar"] if ledger_path.exists() else {}
        for path in paths_for(code):
            for c in read(path).get("candidates", []):
                qid = ledger.get(c["key"])
                if str(qid) in baseline:
                    planned = {"id": qid, "section": c["section"], "text": c["text"], "options": c["options"]}
                    if c.get("needs_figure"):
                        planned["needs_figure"] = True
                    if question_hash(planned) != baseline[str(qid)]:
                        raise ValueError(f"Başlangıç sorusuna değişiklik planlanmış: {qid}")
    for code in CODES:
        compile_decisions(code, paths_for(code))
    print(f"Çapraz kaynak/koşul bağı çözüldü: {resolve_links()}")
    for code in CODES:
        report = compile_decisions(code, paths_for(code))
        print(code, report["yeni_benzersiz"], "toplam ek kaynak sorusu;", report["inceleme"], "inceleme")


def audit():
    require_full_coverage()
    current = bank()
    baseline = verify_baseline(current)
    new_ids = set(current) - set(map(int, baseline))
    if any(qid <= 0 for qid in current):
        raise ValueError("Geçersiz soru kimliği")
    declared_ids = set()
    sources = {}
    source_decisions = defaultdict(list)
    credits = Counter()
    subjects = {}
    excluded = []
    for code in CODES:
        report = read(DATA / f"kaynaklar/rapor_{code}.json")
        compiled = {d["key"]: d for d in report["kararlar"]}
        ledger = read(DATA / f"kaynaklar/idler_{code}.json")["anahtarlar"]
        rows = []
        for path in sorted(DECISIONS.glob(f"full*_{code}.json")):
            doc = read(path)
            for s in doc.get("sources", []):
                sources[s["id"]] = s
            excluded.extend(doc.get("secondary_review_exclusions", []))
            for c in doc.get("candidates", []):
                qid = ledger[c["key"]]
                if qid not in new_ids:
                    raise ValueError(f"Yeni aday yeni kayıt değil: {c['key']}")
                declared_ids.add(qid)
                if len(c["options"]) != len(c["tr_options"]) or not c.get("answer_verification") or not c.get("sources"):
                    raise ValueError(f"Eksik seçenek/çeviri/dayanak/kaynak: {c['key']}")
                for v in c["answer_verification"]:
                    if not v.get("section") or not v["url"].startswith("https://"):
                        raise ValueError(f"Eksik cevap doğrulama konumu: {c['key']}")
                credits[c["sources"][0]["source"]] += 1
            for d in doc.get("decisions", []):
                key = d.get("key", f"{d['source']}:{d['no']}")
                final = compiled[key]
                source_decisions[d["source"]].append(final)
                rows.append(final)
        subjects[code] = {"ad": NAMES[code], "yeni": sum(current[qid][0] == code for qid in new_ids),
                          "taranan": len(rows), "kararlar": dict(Counter(d["status"] for d in rows))}
    if declared_ids != new_ids:
        raise ValueError(f"Bildirilmeyen/eksik yeni kimlikler: {sorted(new_ids ^ declared_ids)}")
    # Bir kaynak satırı yalnız bir kez sayılır. Ortak ders kullanımı yeni ID değildir.
    seen = set()
    for sid, rows in source_decisions.items():
        for d in rows:
            key = (sid, str(d["no"]))
            if key in seen:
                raise ValueError(f"Kaynak satırı çift sayıldı: {key}")
            seen.add(key)
            if not d.get("page") or not d.get("url"):
                raise ValueError(f"Kaynak sayfası/URL eksik: {key}")
            for qid in [d.get("question_id")] + d.get("additional_bank_ids", []):
                if qid is not None and qid not in current:
                    raise ValueError(f"Kaynak bağı bankada yok: {key} -> {qid}")
    source_report = []
    for sid in sorted(set(source_decisions) | set(credits)):
        rows = source_decisions[sid]
        counts = Counter(d["status"] for d in rows)
        before_matches, new_matches = 0, 0
        for d in rows:
            if d["status"] not in ("existing", "new", "duplicate_new"):
                continue
            matched = [d.get("question_id")] + d.get("additional_bank_ids", [])
            if any(qid in new_ids for qid in matched):
                new_matches += 1
            else:
                before_matches += 1
        source_report.append({"id": sid, "ad": sources[sid].get("ad", sources[sid].get("name", sid)),
                              "url": sources[sid]["url"], "taranan": len(rows),
                              "kararlar": dict(counts), "baslangicta_mevcut_eslesme": before_matches,
                              "bu_tur_yeni_tipe_eslesme": new_matches,
                              "eklenen_ilk_kaynak": credits[sid]})
    if sum(s["eklenen_ilk_kaynak"] for s in source_report) != len(new_ids):
        raise ValueError("Yeni kayıtların ilk-kaynak dağılımı toplamla uyuşmuyor")
    summary = {"tarih": "2026-10-13", "baslangic_soru": len(baseline),
               "korunan_soru": len(baseline), "son_soru": len(current),
               "yeni_benzersiz": len(new_ids), "taranan_gercek_kaynak_satiri": len(seen),
               "dersler": subjects, "kaynaklar": source_report, "ikincil_incelemede_elenen": excluded,
               "yeni_idler": sorted(new_ids),
               "sinir": "Yayımlanmış ve normal erişimle incelenebilen PDF kapsamı; bütün güncel SHGM/PPL sınav bankasının eksik sayısı olduğu iddia edilmez.",
               "onceki_29": "2026-10-12 örnekleme turunda eklenen29 bu yeni sayıya dahil değildir; başlangıç3051 içindedir.",
               "erisim_engelli_ek_kaynak": {"url": "https://www.caab.gov.bd/secfiles/ATPL-FOOL%20Question%20Bank%202016.zip",
                  "taranan": 0, "neden": "Normal erişimde zaman aşımı ve SSLsertifika doğrulama hatası; doğrulama devre dışı bırakılmadı."}}
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--derle", action="store_true")
    parser.add_argument("--rapor", action="store_true")
    args = parser.parse_args()
    if args.derle:
        compile_all()
    summary = audit()
    if args.rapor:
        write(DATA / "kaynaklar/rapor_tam_tarama_20261013.json", summary)
    print(f"{summary['korunan_soru']} başlangıç sorusu aynen korundu; "
          f"{summary['taranan_gercek_kaynak_satiri']} kaynak satırı; {summary['yeni_benzersiz']} yeni benzersiz kayıt.")
    for code, d in summary["dersler"].items():
        print(code, d["yeni"], "yeni", d["taranan"], "taranan")


if __name__ == "__main__":
    main()
