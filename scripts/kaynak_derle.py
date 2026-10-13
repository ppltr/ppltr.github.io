#!/usr/bin/env python3
"""İnsan/ajan incelemesi tamamlanan kaynak kararlarını güvenli, tekrar çalıştırılabilir biçimde derler.

python3 scripts/kaynak_derle.py 010 data/kaynaklar/decisions/*audit.json data/kaynaklar/decisions/root_special.json

Ham bankalar yayımlanmaz. Yeni sorular bağımsız anlatımla, doğrulanmış cevap,
iki dil ve kaynak konumuyla yazılır. Belirsiz kayıtların yalnız inceleme metadatası
tutulur; yanlışlıkla doğru cevap atayıp aktif soru yaratılmaz. --kuru dosya yazmaz.
Kimlik tahsisi kalıcıdır; var olan kimlikler ve tarihsel banka dosyaları değiştirilmez.
"""

import argparse
import hashlib
import json
import os
import re
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANDS = {"010": 61000, "020": 62000, "030": 63000, "040": 64000, "050": 65000, "060": 66000,
         "070": 67000, "080": 68000, "090": 69000}
STATUS = {"existing", "new", "duplicate_new", "out_of_scope", "review"}


def read(path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write(json.dumps(value, ensure_ascii=False, indent=1) + "\n")
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def norm(value):
    # İşaretler/sayılar koşulu veya cevabı değiştirebilir: -3 ile +3 birleştirilmez.
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value).casefold()).strip()


def compile_decisions(subject, paths, root=ROOT, dry=False):
    if subject not in BANDS:
        raise ValueError(f"Bilinmeyen ders: {subject}")
    data = root / "data"
    registry_path = data / "kaynaklar/_kaynaklar.json"
    registry = read(registry_path, {"kaynaklar": []})
    sources = {s["id"]: s for s in registry["kaynaklar"]}
    candidates, decisions, existing_notes, retired = {}, {}, [], {}
    for path in paths:
        doc = read(path)
        for key, why in doc.get("retired", {}).items():
            if not isinstance(why, dict) or not why.get("neden_tr") or not why.get("neden_en"):
                raise ValueError(f"Emekli kaydı iki dilde neden ister: {key}")
            retired[key] = why
        for s in doc.get("sources", []):
            if "id" in s:
                sources.setdefault(s["id"], {}).update(s)
        for c in doc.get("candidates", []):
            if c["key"] in candidates:
                raise ValueError(f"Aday anahtarı iki kez kullanıldı: {c['key']}")
            candidates[c["key"]] = c
        existing_notes.extend(doc.get("existing_notes", []))
        for d in doc.get("decisions", []):
            if d["status"] not in STATUS:
                raise ValueError(f"Bilinmeyen karar: {d}")
            d = dict(d)
            key = d.get("key") or f"{d['source']}:{d['no']}"
            d["key"] = key
            if key in decisions:
                raise ValueError(f"Kaynak sorusu iki kez sayıldı: {key}")
            decisions[key] = d

    output_path = data / f"{subject}_ek_kaynak_sorulari.json"
    bank, section_names, subject_codes, bank_subjects = {}, {}, set(), {}
    subject_name = subject
    for path in sorted(data.glob("*.json")):
        if path.name.startswith("_") or path == output_path:
            continue
        doc = read(path)
        if doc.get("subject_code"):
            subject_codes.add(doc["subject_code"])
        if doc.get("subject_code") == subject:
            section_names.update(doc.get("sections", {}))
            subject_name = doc.get("subject_name") or subject_name
        for q in doc.get("questions", []):
            if q["id"] in bank:
                raise ValueError(f"Bankada çakışan kimlik: {q['id']}")
            bank[q["id"]] = q
            bank_subjects[q["id"]] = doc.get("subject_code")
    duplicate_targets = {}
    for group in read(data / "_tekrarlar.json", {"gruplar": []})["gruplar"]:
        for qid in group["ids"][1:]:
            target = group["ids"][0]
            if qid in duplicate_targets and duplicate_targets[qid] != target:
                raise ValueError(f"Mevcut tekrar kaydında çelişki: {qid}")
            duplicate_targets[qid] = target

    def canonical(qid):
        visited = set()
        while qid in duplicate_targets:
            if qid in visited:
                raise ValueError(f"Mevcut tekrar kaydında döngü: {qid}")
            visited.add(qid)
            qid = duplicate_targets[qid]
        return qid

    for d in decisions.values():
        if d["status"] == "existing":
            original = d["bank_id"]
            d["bank_id"] = canonical(original)
            if d["bank_id"] != original:
                d["matched_bank_id"] = original
    id_path = data / f"kaynaklar/idler_{subject}.json"
    ids = read(id_path, {"ders": subject, "anahtarlar": {}})["anahtarlar"]
    old_output = {q["id"]: q for q in read(output_path, {"questions": []})["questions"]}
    if any(type(qid) is not int or qid <= 0 for qid in ids.values()):
        raise ValueError("Kalıcı kimlikler pozitif tam sayı olmalı")
    new_ids = [qid for qid in ids.values() if qid not in bank]
    if len(set(new_ids)) != len(new_ids):
        raise ValueError("Kalıcı kimlik kaydında çakışma")
    # Mevcut soru notlarının kimlikleri yeni soru bandının dışındadır.
    next_id = max([BANDS[subject]] + [qid for qid in ids.values()
                                   if BANDS[subject] < qid <= BANDS[subject] + 999])
    for key in sorted(candidates, key=lambda k: (0 if k.startswith("special:") else 1, k)):
        if key not in ids:
            next_id += 1
            if next_id > BANDS[subject] + 999:
                raise ValueError(f"{subject} yeni soru kimlik bandı doldu; yeni bant gerekli")
            if next_id in bank:
                raise ValueError(f"Yeni kimlik mevcut soruya çarpıyor: {next_id}")
            ids[key] = next_id
        if ids[key] in bank:
            raise ValueError(f"Yeni kimlik tarihsel bankayı değiştirir: {ids[key]}")
        if not BANDS[subject] < ids[key] <= BANDS[subject] + 999:
            raise ValueError(f"Yeni soru kimliği ayrılan bant dışında: {key}")

    # Emekli adaylar: kimlikleri ayrılmış kalır (yeniden kullanılmaz), ama soru olarak derlenmez.
    for key in retired:
        if key not in candidates:
            raise ValueError(f"Emekli kaydı bilinmeyen adayı gösteriyor: {key}")
        if key not in ids:
            raise ValueError(f"Emekli aday için kalıcı kimlik yok: {key}")
    retired_ids = {key: ids[key] for key in retired}
    for key in retired:
        del candidates[key]

    notes_doc = read(data / "_kaynak_notlari.json", {"notlar": {}})
    notes = notes_doc["notlar"]
    for qid in retired_ids.values():
        notes.pop(str(qid), None)
    # Bu derleyicinin önceki kaynak notlarını sıfırdan hesapla; başka dersler korunur.
    for n in notes.values():
        n["src"] = [s for s in n.get("src", []) if s.get("derleyen") != subject]
        n["replace_sources"] = True

    def add_ref(qid, source, url, no="", page=""):
        if source not in sources:
            raise ValueError(f"Kayıtsız kaynak: {source}")
        ref = {"k": source, "url": url or sources[source].get("url", ""), "no": str(no),
               "sayfa": str(page), "derleyen": subject}
        n = notes.setdefault(str(qid), {"src": []})
        n["replace_sources"] = True
        n.setdefault("src", [])
        if not any((s["k"], s.get("no", ""), s.get("sayfa", ""), s.get("url", "")) ==
                   (ref["k"], ref["no"], ref["sayfa"], ref["url"]) for s in n["src"]):
            n["src"].append(ref)

    def attach(qid, c):
        if any(not isinstance(c.get(field), str) or not c[field].strip()
               for field in ("explanation_tr", "explanation_en")):
            raise ValueError(f"Soru {qid}: iki dilde kısa açıklama gerekli")
        proof = c.get("answer_verification")
        if not isinstance(proof, list) or not proof or any(
                not isinstance(v, dict) or not v.get("section") or
                not isinstance(v.get("url"), str) or not v["url"].startswith("https://") for v in proof):
            raise ValueError(f"Soru {qid}: doğrulanmış cevabın URL/konumu eksik")
        if c.get("mark") not in (None, "dogrulanmis", "aday"):
            raise ValueError(f"Soru {qid}: geçersiz kullanıcı işareti")
        aliases = c.get("also_subjects", [])
        if not isinstance(aliases, list) or any(code not in subject_codes for code in aliases):
            raise ValueError(f"Soru {qid}: ortak ders bilinmiyor")
        n = notes.setdefault(str(qid), {"src": []})
        n.update(tr=c["explanation_tr"], en=c["explanation_en"])
        if c.get("mark") and n.get("isaret") != "dogrulanmis":
            n["isaret"] = c["mark"]
        if c.get("also_subjects"):
            n["also_subjects"] = sorted(set(n.get("also_subjects", [])) | set(c["also_subjects"]))
        n["answer_verification"] = c["answer_verification"]
        n["adapted"] = c.get("adapted", False)
        for s in c.get("sources", []):
            add_ref(qid, s["source"], s["url"], s.get("no", ""), s.get("page", ""))
        for v in c["answer_verification"]:
            source = "ref-" + hashlib.sha256((v["url"] + "#" + v["section"]).encode()).hexdigest()[:12]
            host = re.sub(r"^https?://(www\.)?", "", v["url"]).split("/")[0]
            sources[source] = {**sources.get(source, {}), "id": source, "ad": "Cevap doğrulama · " + host,
                "url": v["url"], "tur": "resmi-dayanak", "erisim": "acik",
                "kullanim_notu": "Resmî kural atfı; soru metni bağımsız yazılmıştır."}
            add_ref(qid, source, v["url"], "", v["section"])

    questions, translations, seen_stems = [], {}, {}
    for key, c in sorted(candidates.items(), key=lambda item: ids[item[0]]):
        required = ["section", "text", "options", "tr_text", "tr_options", "explanation_tr",
                    "explanation_en", "answer_verification"]
        if any(not c.get(k) for k in required):
            raise ValueError(f"Eksik cevap/çeviri/dayanak: {key}")
        opts, tr_opts = c["options"], c["tr_options"]
        if not isinstance(opts, list) or not isinstance(tr_opts, list) or not 2 <= len(opts) <= 5 or len(opts) != len(tr_opts):
            raise ValueError(f"Şık/çeviri sayısı: {key}")
        if any(not isinstance(s, str) or not s.strip() for s in opts + tr_opts) or len(set(map(norm, opts))) != len(opts):
            raise ValueError(f"Boş veya tekrarlı şık: {key}")
        if not c["section"].startswith(subject + "-"):
            raise ValueError(f"Ders dışına yazılan aday: {key}")
        if any(not v.get("section") or not v.get("url", "").startswith("https://")
               for v in c["answer_verification"]):
            raise ValueError(f"Cevap dayanağı konumu/URL eksik: {key}")
        stem = norm(c["text"])
        if stem in seen_stems:
            raise ValueError(f"Yeni adaylarda aynı soru kökü: {key}, {seen_stems[stem]}")
        if any(norm(q["text"]) == stem for q in bank.values()):
            raise ValueError(f"Yeni aday zaten bankada: {key}")
        seen_stems[stem] = key
        qid = ids[key]
        q = {"id": qid, "section": c["section"], "text": c["text"], "options": opts}
        # Kimliği verilmiş bir soru farklı içeriğe sessizce dönüştürülemez.
        if qid in old_output and old_output[qid] != q:
            raise ValueError(f"Kalıcı yeni sorunun içeriği değişti: {key}; açık düzeltme gerekir")
        questions.append(q)
        translations[str(qid)] = {"text": c["tr_text"], "options": tr_opts}
        attach(qid, c)
    removed = set(old_output) - {q["id"] for q in questions} - set(retired_ids.values())
    if removed:
        raise ValueError(f"Önceden eklenen sorular silinemez: {sorted(removed)}")
    for c in existing_notes:
        c = dict(c)
        c["bank_id"] = canonical(c["bank_id"])
        if c["bank_id"] not in bank:
            raise ValueError(f"Bilinmeyen mevcut kimlik: {c['bank_id']}")
        if bank_subjects[c["bank_id"]] != subject:
            c["also_subjects"] = sorted(set(c.get("also_subjects", [])) | {subject})
        if c["key"] in ids and ids[c["key"]] != c["bank_id"]:
            if canonical(ids[c["key"]]) != c["bank_id"]:
                raise ValueError(f"Mevcut soru anahtarı farklı kimliğe yönlendirildi: {c['key']}")
            ids[c["key"]] = c["bank_id"]   # kaynak bağı mevcut kanoniğe taşınır; soru/ilerleme değişmez
        ids.setdefault(c["key"], c["bank_id"])
        attach(c["bank_id"], c)

    def resolve(key, visited=None):
        # Emekli/eksik bir anahtarın eski ID kaydı aktif soru oluşturmaz.
        if key in ids and (key in candidates or ids[key] in bank):
            return canonical(ids[key]) if ids[key] in bank else ids[key]
        visited = set() if visited is None else visited
        if key in visited:
            raise ValueError(f"Döngülü tekrar kararı: {key}")
        visited.add(key)
        d = decisions.get(key, {})
        if d.get("status") == "existing":
            return d["bank_id"]
        if d.get("representative_key"):
            return resolve(d["representative_key"], visited)
        return None

    def retired_by(key, visited=None):
        # Karar kendisi ya da temsilcisi emekli bir adaysa o adayın anahtarını döndürür.
        visited = set() if visited is None else visited
        if key in visited:
            return None
        visited.add(key)
        if key in retired:
            return key
        rep = decisions.get(key, {}).get("representative_key")
        return retired_by(rep, visited) if rep else None

    queue, counts, unique_new = [], {}, {}
    active_new_ids = {q["id"] for q in questions}
    for key, d in decisions.items():
        sid = d["source"]
        if sid not in sources:
            raise ValueError(f"Kararda kayıtsız kaynak: {sid}")
        qid = d.get("bank_id") if d["status"] == "existing" else resolve(key)
        if d["status"] in {"new", "duplicate_new"} and qid is None and retired_by(key):
            why = retired[retired_by(key)]
            d["status"], d["bank_id"] = "out_of_scope", None
            d["reason"] = "Ders notlarında karşılığı yok / aynı konu: " + why["neden_en"]
            d["reason_tr"] = "Ders notlarında karşılığı yok / aynı konu: " + why["neden_tr"]
            d["emekli_kimlik"] = retired_ids[retired_by(key)]
            d.pop("question_id", None)
        elif d["status"] in {"new", "duplicate_new"} and qid is None:
            # Seçilmeyen/cevabı belirsiz bir temsilciye atıf da incelemedir.
            d["status"] = "review"
            d["reason"] += " Temsilci aktif bankaya kabul edilmedi."
        if d["status"] == "existing" and qid not in bank:
            raise ValueError(f"Yanlış mevcut soru referansı: {key} -> {qid}")
        if d["status"] == "duplicate_new" and qid in bank:
            d["original_status"] = "duplicate_new"
            d["status"], d["bank_id"] = "existing", qid
        if qid is not None and d["status"] in {"existing", "new", "duplicate_new"}:
            if qid not in bank and qid not in active_new_ids:
                raise ValueError(f"Aktif olmayan soru referansı: {key} -> {qid}")
            if d["status"] == "new" and qid in bank:
                raise ValueError(f"Yeni kararı mevcut soruya bağlandı: {key} -> {qid}")
            d["question_id"] = qid
            add_ref(qid, sid, d.get("url", ""), d["no"], d.get("page", ""))
            if qid in bank and bank_subjects[qid] != subject:
                n = notes.setdefault(str(qid), {"src": []})
                n["also_subjects"] = sorted(set(n.get("also_subjects", [])) | {subject})
            if qid in active_new_ids:
                unique_new.setdefault(sid, set()).add(qid)
        if d["status"] == "review":
            queue.append({"kaynak": sid, "no": str(d["no"]), "sayfa": str(d.get("page", "")),
                "url": d.get("url") or sources[sid]["url"],
                "konu": d.get("topic_tr") or d.get("reason_tr") or d.get("topic") or d.get("reason", "İnceleme bekliyor"),
                "neden": d.get("reason_tr") or d["reason"]})
        counts.setdefault(sid, Counter())[d["status"]] += 1
    for sid, counter in counts.items():
        sources[sid].setdefault("taranan", {})[subject] = {
            "sayi": sum(counter.values()), "kapsam": "Her soru için karar kaydı; kapsam kaynak notunda",
            "url": next((d["url"] for d in decisions.values() if d["source"] == sid and d.get("url")), sources[sid]["url"])}
        sources[sid]["karar_sayilari"] = dict(counter)
        sources[sid]["yeni_benzersiz"] = len(unique_new.get(sid, set()))
    output = {"subject_code": subject, "subject_name": subject_name,
        "origin": "ek", "source": "Dış kaynaklarda saptanan eksik soru tipleri; bağımsız anlatım ve resmî cevap kontrolü (2026-10-12)",
        "answer_convention": "İki dilde aynı sırada; ilk şık doğru. Belirsiz cevap aktif bankada yok.",
        "id_convention": "Kalıcı idler_" + subject + ".json; eski veya emekli kimlik yeniden kullanılmaz.",
        "sections": {c: section_names.get(c, "Additional Questions" if c.endswith("-EK") else c)
                     for c in sorted({q['section'] for q in questions})},
        "questions": questions}
    report = {"ders": subject, "tarih": "2026-10-12", "yeni_benzersiz": len(questions),
        "taranan": len(decisions), "kaynaklar": {k: dict(v) for k, v in counts.items()},
        "yildizlar": [int(k) for k, n in notes.items() if n.get("isaret") == "dogrulanmis"],
        "inceleme": len(queue), "kararlar": list(decisions.values()),
        "kaynak_yeni_benzersiz": {sid: len(unique_new.get(sid, set())) for sid in counts}}
    if not dry:
        tr_path = data / f"tr/{subject}_ek_kaynak_sorulari_01.json"
        if questions:
            write(output_path, output)
            write(tr_path, {"questions": translations})
        else:
            # Hiç soru kalmadıysa boş dosya bırakılmaz (init_db boş bir ders dosyasını anlamsız bulur).
            output_path.unlink(missing_ok=True)
            tr_path.unlink(missing_ok=True)
        write(id_path, {"ders": subject, "anahtarlar": ids,
                        "emekli": {k: {"id": retired_ids[k], **retired[k]} for k in sorted(retired_ids)}})
        notes_doc["_aciklama"] = "Kullanıcı doğrulaması ile kaynak/cevap doğrulaması ayrıdır; hiçbir işaret resmî SHGM çıkmış sorusu iddiası değildir."
        write(data / "_kaynak_notlari.json", notes_doc)
        registry["kaynaklar"] = list(sources.values())
        write(registry_path, registry)
        write(data / f"kaynaklar/inceleme_{subject}.json", {"ders": subject, "sorular": queue})
        write(data / f"kaynaklar/rapor_{subject}.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("subject", choices=sorted(BANDS))
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--kuru", action="store_true")
    args = parser.parse_args()
    result = compile_decisions(args.subject, args.paths, dry=args.kuru)
    print(f"{result['taranan']} kaynak sorusu değerlendirildi; {result['yeni_benzersiz']} yeni benzersiz soru; "
          f"{result['inceleme']} inceleme kaydı; yıldızlar: {result['yildizlar']}")


if __name__ == "__main__":
    main()
