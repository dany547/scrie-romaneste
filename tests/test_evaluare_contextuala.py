#!/usr/bin/env python3
"""Structura corpusului sintetic pentru revizia contextuală.

Testează doar forma fișierului `fixtures/evaluare-contextuala.json`: număr de
cazuri, câmpuri, splituri, familii, absența placeholder-elor și a datelor
personale. NU testează performanța vreunui model sau detector: etichetele sunt
provizorii (`status: draft_nevalidat_uman`), iar corpusul nu intră în regex-urile
scripturilor.

Rulează: python3 -m unittest discover -s tests -p test_evaluare_contextuala.py -v
"""
import json
import re
import unittest
from collections import Counter, defaultdict
from pathlib import Path

RADACINA = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
CORPUS = FIXTURES / "evaluare-contextuala.json"
SCRIPTS = RADACINA / "scripts"

CAMPURI = {"id", "family", "split", "category", "audience", "context", "text",
           "expected_verdict", "rationale", "minimal_correction", "source_status"}
CATEGORII = ["lexic", "acord", "sens", "calc", "registru", "valid"]
SPLITURI = {"referinta": 36, "holdout": 24}
VERDICTE = {"eroare", "suspiciune", "pastreaza", "neclar"}
PLACEHOLDER = re.compile(
    r"\bTODO\b|\bTBD\b|\bXXX\b|lorem|\[[^\]\n]*\]|<[^>\n]*>|\{\{|\}\}|\?\?\?", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
TELEFON = re.compile(r"(?<!\d)(\+?\d[\d .-]{7,}\d)(?!\d)")
URL = re.compile(r"https?://|www\.", re.I)
N_SHINGLE = 6


def _incarca():
    with CORPUS.open(encoding="utf-8") as f:
        return json.load(f)


def _shingles(text, n=N_SHINGLE):
    cuvinte = re.findall(r"\w+", text.lower())
    return {" ".join(cuvinte[i:i + n]) for i in range(len(cuvinte) - n + 1)}


class TestCorpusEvaluare(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.date = _incarca()
        cls.cazuri = cls.date["cases"]

    def test_radacina(self):
        self.assertEqual(self.date["schema_version"], 1)
        self.assertEqual(self.date["status"], "draft_nevalidat_uman")
        self.assertTrue(self.date["description"].strip())

    def test_numar_total_si_splituri(self):
        self.assertEqual(len(self.cazuri), 60)
        numar = Counter(c["split"] for c in self.cazuri)
        self.assertEqual(dict(numar), SPLITURI)

    def test_categorii_zece_fiecare(self):
        numar = Counter(c["category"] for c in self.cazuri)
        self.assertEqual(set(numar), set(CATEGORII))
        for cat in CATEGORII:
            self.assertEqual(numar[cat], 10, cat)

    def test_categorii_pe_split(self):
        """Câte 6 de referință și 4 de holdout pe fiecare categorie."""
        numar = Counter((c["category"], c["split"]) for c in self.cazuri)
        for cat in CATEGORII:
            self.assertEqual(numar[(cat, "referinta")], 6, cat)
            self.assertEqual(numar[(cat, "holdout")], 4, cat)

    def test_id_unic(self):
        ids = [c["id"] for c in self.cazuri]
        self.assertEqual(len(ids), len(set(ids)), "id-uri duplicate")
        for i in ids:
            self.assertRegex(i, r"^[a-z]+-(ref|hold)-\d{2}$", i)

    def test_campuri_exacte(self):
        for c in self.cazuri:
            self.assertEqual(set(c), CAMPURI, c.get("id"))

    def test_valori_permise(self):
        for c in self.cazuri:
            self.assertIn(c["category"], CATEGORII, c["id"])
            self.assertIn(c["split"], SPLITURI, c["id"])
            self.assertIn(c["expected_verdict"], VERDICTE, c["id"])
            self.assertEqual(c["source_status"], "neconfirmat", c["id"])

    def test_texte_si_explicatii_nevide(self):
        for c in self.cazuri:
            for camp in ("family", "audience", "context", "text", "rationale"):
                self.assertIsInstance(c[camp], str, f"{c['id']}.{camp}")
                self.assertTrue(c[camp].strip(), f"{c['id']}.{camp} gol")
            corectie = c["minimal_correction"]
            self.assertTrue(corectie is None or (isinstance(corectie, str)
                                                 and corectie.strip()), c["id"])

    def test_pastreaza_si_neclar_fara_corectie_fixa(self):
        """Corecția minimă apare doar la eroare sau suspiciune cu rescriere locală."""
        for c in self.cazuri:
            if c["expected_verdict"] in ("pastreaza", "neclar"):
                self.assertIsNone(c["minimal_correction"], c["id"])
            if c["expected_verdict"] == "eroare":
                self.assertIsInstance(c["minimal_correction"], str, c["id"])

    def test_familie_intr_un_singur_split(self):
        splituri = defaultdict(set)
        for c in self.cazuri:
            splituri[c["family"]].add(c["split"])
        for familie, s in splituri.items():
            self.assertEqual(len(s), 1, f"familia {familie} apare în {sorted(s)}")

    def test_familie_are_control(self):
        """Fiecare familie din categorii cu greșeli are măcar un control `pastreaza`
        în același split (perechea eroare/control rămâne împreună)."""
        grupe = defaultdict(list)
        for c in self.cazuri:
            grupe[c["family"]].append(c)
        for familie, membri in grupe.items():
            self.assertGreaterEqual(len(membri), 2, familie)
            if membri[0]["category"] == "valid":
                continue
            verdicte = {m["expected_verdict"] for m in membri}
            self.assertIn("pastreaza", verdicte, f"{familie} n-are control")
            self.assertTrue(verdicte - {"pastreaza"}, f"{familie} n-are caz de semnalat")

    def test_fara_placeholders(self):
        for c in self.cazuri:
            for camp, valoare in c.items():
                if isinstance(valoare, str):
                    self.assertIsNone(PLACEHOLDER.search(valoare), f"{c['id']}.{camp}")

    def test_fara_date_personale(self):
        for c in self.cazuri:
            for camp, valoare in c.items():
                if not isinstance(valoare, str):
                    continue
                self.assertIsNone(EMAIL.search(valoare), f"email în {c['id']}.{camp}")
                self.assertIsNone(URL.search(valoare), f"URL în {c['id']}.{camp}")
                self.assertIsNone(TELEFON.search(valoare), f"număr în {c['id']}.{camp}")

    def test_fara_sovaiala_fata_de_fixturile_existente(self):
        """Niciun text din corpus nu repetă o secvență de 6 cuvinte din alte fixturi."""
        existente = set()
        for fisier in FIXTURES.glob("*.md"):
            existente |= _shingles(fisier.read_text(encoding="utf-8"))
        suprapuneri = [c["id"] for c in self.cazuri
                       if _shingles(c["text"]) & existente]
        self.assertEqual(suprapuneri, [])

    def test_corpusul_nu_intra_in_detectoare(self):
        """Scripturile și testele existente nu citesc corpusul."""
        for cale in list(SCRIPTS.glob("*.py")) + [Path(__file__).resolve().parent /
                                                  "test_scripts.py"]:
            self.assertNotIn("evaluare-contextuala", cale.read_text(encoding="utf-8"),
                             cale.name)


if __name__ == "__main__":
    unittest.main()
