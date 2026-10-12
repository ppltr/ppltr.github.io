#!/usr/bin/env python3
"""Kaynak ekleme güvenlik ve geçmiş koruma testleri (yalnız geçici dosyalar)."""
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


init = module("bank_init", "scripts/init_db.py")
build = module("bank_build", "scripts/build_web.py")
apply = module("source_apply", "scripts/kaynak_uygula.py")
match = module("source_match", "scripts/kaynak_esle.py")
server = module("db", "server/db.py")
sys.modules["db"] = server
stats = module("source_stats", "server/stats.py")


class SourcePipelineTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.data = self.root / "data"
        self.data.mkdir()
        self.sources = self.data / "kaynaklar"
        self.sources.mkdir()
        self.tr = self.data / "tr"
        self.tr.mkdir()
        self.en = self.data / "en"
        self.en.mkdir()
        self.db = self.root / "bank.db"
        self.patches = [
            patch.object(init, "DB_PATH", self.db), patch.object(init, "DATA_DIR", self.data),
            patch.object(init, "TR_DIR", self.tr), patch.object(init, "EN_DIR", self.en),
            patch.object(build, "DB", self.db), patch.object(build, "SOURCE_DIR", self.sources),
            patch.object(build, "NOTES_DIR", self.root / "notes"),
            patch.object(build, "FIG_DIR", self.root / "figures"),
            patch.object(server, "BANK_DB", self.db), patch.object(server, "APP_DB", self.root / "history.db"),
            patch.object(apply, "DB", self.db), patch.object(apply, "DATA", self.data),
            patch.object(apply, "HAM", self.sources / "_ham"),
        ]
        for p in self.patches:
            p.start()
        self.conn = init.connect()
        self.conn.row_factory = sqlite3.Row
        self.write(self.data / "010.json", {"subject_code": "010", "subject_name": "Air Law",
            "sections": {"010-01": "Rules"}, "questions": [
                {"id": 1, "section": "010-01", "text": "Rule?", "options": ["Yes", "No"]},
                {"id": 3, "section": "010-01", "text": "Uncertain?", "options": ["A", "B"], "inceleme": True}]})
        self.write(self.data / "030.json", {"subject_code": "030", "subject_name": "Performance",
            "sections": {"030-01": "Runway"}, "questions": [
                {"id": 2, "section": "030-01", "text": "Take-off run?", "options": ["TORA", "TODA"]}]})
        init.import_file(self.conn, self.data / "010.json")
        init.import_file(self.conn, self.data / "030.json")
        self.conn.execute("UPDATE questions SET explanation='existing explanation' WHERE id=1")
        self.conn.commit()
        self.write(self.sources / "_kaynaklar.json", {"kaynaklar": [
            {"id": "source", "ad": "Source", "url": "https://example.com/bank", "erisim": "acik"}]})
        self.write_notes({"2": {"isaret": "dogrulanmis", "tr": "Koşu uzunluğu.", "en": "Run length.",
                        "also_subjects": ["010"], "src": [{"k": "source", "no": "48", "sayfa": "4"}]}})
        init.import_notes(self.conn)

    def tearDown(self):
        self.conn.close()
        for p in reversed(self.patches):
            p.stop()
        self.temp.cleanup()

    @staticmethod
    def write(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    def write_notes(self, data):
        self.write(self.data / "_kaynak_notlari.json", {"notlar": data})

    def test_notes_upsert_keeps_existing_explanations_and_ids(self):
        before = [tuple(r) for r in self.conn.execute("SELECT id,text,created_at FROM questions ORDER BY id")]
        self.write_notes({"2": {"src": [{"k": "source", "no": "48", "url": "https://example.com/q/48"}]}})
        init.import_notes(self.conn)
        init.import_notes(self.conn)
        after = [tuple(r) for r in self.conn.execute("SELECT id,text,created_at FROM questions ORDER BY id")]
        self.assertEqual(before, after)
        self.assertEqual(self.conn.execute("SELECT explanation FROM questions WHERE id=1").fetchone()[0], "existing explanation")
        self.assertEqual(self.conn.execute("SELECT explanation FROM questions WHERE id=2").fetchone()[0], "Koşu uzunluğu.")
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM question_sources").fetchone()[0], 1)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM question_subjects").fetchone()[0], 1)

    def test_invalid_notes_fail_before_any_write(self):
        before = list(map(tuple, self.conn.execute("SELECT * FROM question_sources")))
        self.write_notes({"2": {"tr": "should not be written"}, "999": {"src": [{"k": "missing"}]}})
        with self.assertRaises(SystemExit):
            init.import_notes(self.conn)
        self.assertEqual(list(map(tuple, self.conn.execute("SELECT * FROM question_sources"))), before)
        self.assertEqual(self.conn.execute("SELECT explanation FROM questions WHERE id=2").fetchone()[0], "Koşu uzunluğu.")

    def test_figure_is_exported_and_server_only_serves_existing_named_asset(self):
        figures = self.root / "figures"
        figures.mkdir()
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><text x="1" y="10">L</text></svg>'
        (figures / "forecast_low.svg").write_text(svg)
        self.write(figures / "index.json", {"1": "forecast_low", "2": "../private", "3": "missing"})
        with patch.object(server, "ROOT", self.root):
            self.assertEqual(server.figure_url(1), "/figures/forecast_low.svg")
            self.assertIsNone(server.figure_url(2))
            self.assertIsNone(server.figure_url(3))
        # Şüpheli/görseli olmayan eşleşmelerin export örneğine karışmasına gerek yok.
        self.write(figures / "index.json", {"1": "forecast_low"})
        exported = build.export()
        first = next(q for q in exported["q"] if q[0] == 1)
        self.assertEqual(first[9], "forecast_low")
        self.assertEqual(exported["fg"]["forecast_low"], svg)

    def test_authoritative_refs_remove_corrected_citation_without_erasing_other_questions(self):
        self.conn.execute("INSERT INTO question_sources VALUES (1,'source','untouched','1','https://example.com/old')")
        self.conn.execute("INSERT OR REPLACE INTO question_sources VALUES (2,'source','48','1','https://example.com/wrong')")
        self.conn.commit()
        self.write_notes({"2": {"replace_sources": True, "src": [
            {"k": "source", "no": "49", "url": "https://example.com/corrected"}]}})
        init.import_notes(self.conn)
        refs = list(self.conn.execute("SELECT question_id,ref FROM question_sources ORDER BY question_id"))
        self.assertEqual([tuple(r) for r in refs], [(1, "untouched"), (2, "49")])
        self.assertEqual(self.conn.execute("SELECT explanation FROM questions WHERE id=1").fetchone()[0], "existing explanation")

    def test_uncertain_questions_have_no_correct_answer_or_active_export(self):
        self.assertEqual(self.conn.execute("SELECT SUM(is_correct) FROM options WHERE question_id=3").fetchone()[0], 0)
        self.write(self.sources / "inceleme_010.json", {"ders": "010", "sorular": [
            {"kaynak": "source", "no": "174", "sayfa": "12", "url": "https://example.com/q",
             "konu": "TL", "neden": "answer not verified"}]})
        export = build.export()
        self.assertEqual([q[0] for q in export["q"]], [1, 2])
        self.assertEqual(export["x"][2]["a"], ["010"])
        self.assertEqual(len(export["rq"]), 2)
        self.assertEqual(export["rq"][0]["kaynaklar"][0]["no"], "174")
        self.assertFalse(any("dogru_index" in item for item in export["rq"]))

    def test_shared_subject_history_and_server_filter(self):
        server.init()
        with server.db() as conn:
            conn.execute("INSERT INTO users(id,name,is_guest,created_at) VALUES (1,'Pilot',1,'2026-10-12')")
            server.record(conn, 1, None, 2, 1, True, 1000)
            before = list(map(tuple, conn.execute("SELECT * FROM attempts")))
        init.import_file(self.conn, self.data / "030.json")
        init.import_notes(self.conn)
        with server.db() as conn:
            for hide_dups in (True, False):
                qids = server.pick_questions(conn, 1, subject="010", section="all", hide_dups=hide_dups,
                    show_gen=True, only_wrong=False, limit=500)
                self.assertEqual(set(qids), {1, 2})
                self.assertEqual(len(qids), 2)
            self.assertIsNone(server.question(conn, 3))
            qids = server.pick_questions(conn, 1, subject="010", section="010-X", hide_dups=False,
                    show_gen=True, only_wrong=False, limit=500)
            self.assertEqual(qids, [2])
            subject = next(r for r in server.subjects(conn) if r["code"] == "010")
            self.assertEqual(subject["n"], 2)
            section = next(r for r in server.sections(conn, "010") if r["code"] == "010-X")
            self.assertEqual(section["n"], 1)
            self.assertEqual(list(map(tuple, conn.execute("SELECT * FROM attempts"))), before)
            law = next(r for r in stats.per_subject(conn, 1) if r["code"] == "010")
            self.assertEqual((law["bank_n"], law["uniq"]), (2, 1))

    def test_non_a_active_answer_is_rejected(self):
        path = self.data / "invalid.json"
        self.write(path, {"subject_code": "010", "subject_name": "Air Law", "questions": [
            {"id": 4, "text": "Bad?", "options": ["a", "b"], "correct_index": 1}]})
        with self.assertRaises(SystemExit):
            init.import_file(self.conn, path)
        self.assertIsNone(self.conn.execute("SELECT id FROM questions WHERE id=4").fetchone())

    def test_answer_selection_fails_closed(self):
        decision = {"kume": "C", "dogru_dogrulandi": True, "dayanak": "Verified rule",
                    "dogru_url": "https://example.com/rule", "siklar": ["+3"]}
        raw = {"siklar": ["-3", "+3"], "dogru": 1}
        self.assertEqual(apply.dogru_sirasi(decision, raw), ["+3", "-3"])
        with self.assertRaises(ValueError):
            apply.dogru_sirasi({**decision, "siklar": ["+ 3"]}, raw)
        with self.assertRaises(ValueError):
            apply.dogru_sirasi({**decision, "dogru_dogrulandi": False}, raw)
        with self.assertRaises(ValueError):
            apply.dogru_sirasi(decision, {**raw, "dogru": 0})

    def test_unknown_answers_and_changed_conditions_are_not_auto_duplicates(self):
        self.assertEqual(match.siniflandir({"dogru_metin": None}, [
            {"stem": .99, "bank_cevap_sikta": 1}]), "aday")
        raw = {"dil": "en", "metin": "Aircraft in IFR flight at 180 degrees?",
               "siklar": ["FL100", "FL110"], "dogru_metin": "FL100"}
        changed = {**raw, "metin": "Aircraft in VFR flight at 180 degrees?"}
        conflict = {**raw, "dogru_metin": "FL110"}
        self.assertEqual(len(match.kumele([raw, changed, conflict])), 3)

    def test_dry_run_does_not_write_review_queue(self):
        self.write(self.sources / "_ham" / "_esleme_010.json", {"ders": "010", "kumeler": [], "var": []})
        decision = self.root / "decision.json"
        self.write(decision, {"kabul": [], "nihai_kararlar": [], "inceleme_kuyrugu": [
            {"kume": "pending", "metin": "Unverified?", "siklar": ["a", "b"]}]})
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*.json")}
        with patch.object(sys, "argv", ["kaynak_uygula.py", "010", str(decision), "--kuru"]):
            apply.main()
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*.json")}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
