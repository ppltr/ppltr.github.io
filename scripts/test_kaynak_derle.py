"""Kaynak derleyicisinin kimlik, inceleme ve kuru çalışma güvenceleri."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from kaynak_derle import compile_decisions


class CompilerSafetyTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.data = self.root / "data"
        self.data.mkdir()
        self.put("data/010_original.json", {"subject_code": "010", "sections": {"010-03": "Rules"},
            "questions": [{"id": 42, "text": "Existing historical question?", "options": ["Yes", "No"]}]})
        self.put("data/kaynaklar/_kaynaklar.json", {"kaynaklar": [{"id": "s", "ad": "Source", "url": "https://example.org/bank"}]})
        self.candidate = {"key": "new:q1", "section": "010-03", "text": "A verified new question?",
            "options": ["Correct", "Incorrect"], "tr_text": "Doğrulanmış yeni soru?",
            "tr_options": ["Doğru", "Yanlış"], "explanation_tr": "Doğrulandı.",
            "explanation_en": "Verified.", "adapted": True,
            "answer_verification": [{"url": "https://authority.example.org/rule", "section": "1.2"}]}
        self.doc = {"candidates": [self.candidate], "decisions": [
            {"source": "s", "no": "1", "key": "s:1", "status": "duplicate_new", "representative_key": "new:q1", "reason": "Same rule"},
            {"source": "s", "no": "2", "key": "s:2", "status": "review", "reason": "No verified answer"}]}

    def tearDown(self):
        self.temp.cleanup()

    def put(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))
        return path

    def run_compile(self, doc=None, dry=False):
        path = self.put("audit.json", self.doc if doc is None else doc)
        return compile_decisions("010", [path], root=self.root, dry=dry)

    def test_dry_run_and_unknown_answers_do_not_create_scored_items(self):
        before = {p: p.read_bytes() for p in self.data.rglob("*") if p.is_file()}
        self.run_compile(dry=True)
        self.assertEqual(before, {p: p.read_bytes() for p in self.data.rglob("*") if p.is_file()})
        report = self.run_compile()
        bank = json.loads((self.data / "010_ek_kaynak_sorulari.json").read_text())
        self.assertEqual(len(bank["questions"]), 1)
        self.assertEqual(report["inceleme"], 1)
        self.assertNotIn("s:2", json.loads((self.data / "kaynaklar/idler_010.json").read_text())["anahtarlar"])

    def test_ids_and_original_bytes_are_preserved_across_reordering(self):
        original = (self.data / "010_original.json").read_bytes()
        self.run_compile()
        first = (self.data / "010_ek_kaynak_sorulari.json").read_bytes()
        self.doc["decisions"].reverse()
        self.run_compile()
        self.assertEqual(first, (self.data / "010_ek_kaynak_sorulari.json").read_bytes())
        self.assertEqual(original, (self.data / "010_original.json").read_bytes())

    def test_unresolved_duplicate_is_review_without_guessing(self):
        self.doc["decisions"][0]["representative_key"] = "missing:representative"
        report = self.run_compile()
        self.assertEqual(report["inceleme"], 2)

    def test_missing_verification_fails_before_writing(self):
        del self.candidate["answer_verification"]
        with self.assertRaises(ValueError):
            self.run_compile()
        self.assertFalse((self.data / "010_ek_kaynak_sorulari.json").exists())

    def test_reusing_or_reinterpreting_a_permanent_id_is_rejected(self):
        self.run_compile()
        self.candidate["options"] = ["A different answer", "Incorrect"]
        with self.assertRaisesRegex(ValueError, "içeriği değişti"):
            self.run_compile()

    def test_duplicate_keys_and_duplicate_answer_choices_fail_closed(self):
        doc = copy.deepcopy(self.doc)
        doc["decisions"].append(doc["decisions"][0])
        with self.assertRaises(ValueError):
            self.run_compile(doc)
        self.candidate["options"] = ["Same", "Same"]
        with self.assertRaises(ValueError):
            self.run_compile()

    def test_answer_signs_and_different_conditions_are_preserved(self):
        self.candidate["options"] = ["-3", "+3"]
        self.candidate["tr_options"] = ["-3", "+3"]
        self.assertEqual(self.run_compile()["yeni_benzersiz"], 1)

    def test_existing_notes_require_verification_and_cannot_redirect_id(self):
        note = {"key": "existing:note", "bank_id": 42, "explanation_tr": "Açıklama.",
                "explanation_en": "Explanation.", "answer_verification": []}
        self.doc["existing_notes"] = [note]
        with self.assertRaises(ValueError):
            self.run_compile()
        note["answer_verification"] = self.candidate["answer_verification"]
        self.run_compile()
        ids = json.loads((self.data / "kaynaklar/idler_010.json").read_text())
        ids["anahtarlar"]["existing:note"] = 99999
        self.put("data/kaynaklar/idler_010.json", ids)
        with self.assertRaisesRegex(ValueError, "farklı kimliğe"):
            self.run_compile()

    def test_band_allocation_ignores_existing_high_ids_and_has_limit(self):
        self.put("data/020_original.json", {"subject_code": "020", "questions": [
            {"id": 99999, "text": "Other historical?", "options": ["Yes", "No"]}]})
        self.doc["existing_notes"] = [{"key": "existing:high", "bank_id": 99999,
            "explanation_tr": "Açıklama.", "explanation_en": "Explanation.",
            "answer_verification": self.candidate["answer_verification"]}]
        self.run_compile()
        self.run_compile()
        output = json.loads((self.data / "010_ek_kaynak_sorulari.json").read_text())
        self.assertEqual(output["questions"][0]["id"], 61001)
        self.put("data/kaynaklar/idler_010.json", {"anahtarlar": {"old:key": 61999}})
        with self.assertRaisesRegex(ValueError, "bandı doldu"):
            self.run_compile()

    def test_stale_mapping_is_not_a_verified_active_representative(self):
        self.put("data/kaynaklar/idler_010.json", {"anahtarlar": {"stale:key": 61002}})
        self.doc["decisions"][0]["representative_key"] = "stale:key"
        report = self.run_compile()
        self.assertEqual(report["inceleme"], 2)
        self.assertEqual(report["kaynak_yeni_benzersiz"]["s"], 0)

    def test_per_source_duplicate_new_counts_do_not_inflate_unique_new(self):
        self.doc["decisions"].append({"source": "s", "no": "3", "key": "s:3", "status": "duplicate_new",
            "representative_key": "new:q1", "reason": "Same question"})
        report = self.run_compile()
        self.assertEqual(report["kaynaklar"]["s"]["duplicate_new"], 2)
        self.assertEqual(report["kaynak_yeni_benzersiz"]["s"], 1)

    def test_reference_sections_on_same_url_remain_distinct(self):
        self.candidate["answer_verification"].append({"url": "https://authority.example.org/rule", "section": "1.3"})
        self.run_compile()
        notes = json.loads((self.data / "_kaynak_notlari.json").read_text())["notlar"]
        refs = [ref for ref in notes["61001"]["src"] if ref["k"].startswith("ref-")]
        self.assertEqual({r["sayfa"] for r in refs}, {"1.2", "1.3"})
        self.assertEqual(len({r["k"] for r in refs}), 2)

    def test_hidden_existing_matches_link_to_canonical_without_bank_edits(self):
        self.put("data/030_original.json", {"subject_code": "030", "questions": [
            {"id": 43, "text": "Same historical question?", "options": ["Yes", "No"]}]})
        self.put("data/_tekrarlar.json", {"gruplar": [{"ids": [43, 42]}]})
        before = (self.data / "010_original.json").read_bytes()
        self.doc["decisions"][0] = {"source": "s", "no": "1", "key": "s:1", "status": "existing",
            "bank_id": 42, "reason": "Matched same question"}
        report = self.run_compile()
        d = next(d for d in report["kararlar"] if d["key"] == "s:1")
        self.assertEqual((d["question_id"], d["matched_bank_id"]), (43, 42))
        notes = json.loads((self.data / "_kaynak_notlari.json").read_text())["notlar"]
        self.assertEqual(notes["43"]["also_subjects"], ["010"])
        self.assertEqual((self.data / "010_original.json").read_bytes(), before)
        self.assertNotIn("42", notes)

    def test_duplicate_new_resolved_to_existing_counts_as_existing(self):
        self.doc["existing_notes"] = [{"key": "special:existing", "bank_id": 42,
            "explanation_tr": "Açıklama.", "explanation_en": "Explanation.",
            "answer_verification": self.candidate["answer_verification"]}]
        self.doc["decisions"][0]["representative_key"] = "special:existing"
        report = self.run_compile()
        self.assertEqual(report["kaynaklar"]["s"].get("existing"), 1)
        self.assertEqual(report["kaynak_yeni_benzersiz"]["s"], 0)


if __name__ == "__main__":
    unittest.main()
