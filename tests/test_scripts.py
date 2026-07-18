#!/usr/bin/env python3
"""Teste pentru scripturile de verificare. Rulează: python3 -m unittest discover tests

Fără dependențe externe — doar stdlib, ca scripturile.
"""
import subprocess
import sys
import unittest
from pathlib import Path

RADACINA = Path(__file__).resolve().parent.parent
SCRIPTS = RADACINA / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def ruleaza(script, *argumente):
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *argumente],
        capture_output=True, text=True)
    return r.returncode, r.stdout


class TestTipare(unittest.TestCase):

    def test_text_curat_nu_e_semnalat(self):
        cod, iesire = ruleaza("check-tipare.py", str(FIXTURES / "bun-articol.md"))
        self.assertEqual(cod, 0, f"text uman semnalat gresit:\n{iesire}")
        self.assertIn("0 tipare AI gasite", iesire)

    def test_text_cu_clisee_e_semnalat(self):
        cod, iesire = ruleaza("check-tipare.py",
                              str(FIXTURES / "rau-cu-diacritice.md"))
        self.assertEqual(cod, 1)
        self.assertIn("critic|", iesire)

    def test_diacriticele_nu_conteaza(self):
        """Regresie: tiparele erau scrise cu diacritice, deci textul fara
        diacritice trecea complet nedetectat."""
        _, cu = ruleaza("check-tipare.py", str(FIXTURES / "rau-cu-diacritice.md"))
        cod, fara = ruleaza("check-tipare.py",
                            str(FIXTURES / "rau-fara-diacritice.md"))
        self.assertEqual(cod, 1, "textul fara diacritice nu a fost semnalat")
        total_cu = [l for l in cu.splitlines() if l.startswith("total=")]
        total_fara = [l for l in fara.splitlines() if l.startswith("total=")]
        self.assertEqual(total_cu, total_fara,
                         "acelasi text da rezultate diferite dupa diacritice")

    def test_sedila_e_tratata_ca_virgula(self):
        """Regresie: 'ş' (U+015F) nu se potriveste cu 'ș' (U+0219)."""
        cod, iesire = ruleaza("check-tipare.py", str(FIXTURES / "rau-sedila.md"))
        self.assertEqual(cod, 1)
        self.assertIn("critic|", iesire)

    def test_formele_flexionare_sunt_prinse(self):
        text = "O solutie revolutionara. Doua abordari revolutionare. Un plan revolutionar."
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertEqual(iesire.count("vocabular_corporatist"), 3,
                         f"nu a prins toate formele:\n{iesire}")

    def test_o_aparitie_izolata_nu_declanseaza_prag(self):
        """Un singur 'de asemenea' intr-un text lung nu e un tipar."""
        text = ("De asemenea, am plecat. " + "Vremea era buna si drumul lung. " * 60)
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("structura", iesire,
                         f"o aparitie izolata a fost semnalata:\n{iesire}")

    def test_repetitia_declanseaza_prag(self):
        text = ("De asemenea am plecat. " * 8) + ("Vremea era buna. " * 20)
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertIn("structura", iesire)
        self.assertEqual(cod, 1)

    def test_artefacte_de_generare(self):
        text = "Sper ca te ajuta! Contact: [Numele tau] la ?utm_source=chatgpt.com"
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertIn("artefact_chatbot", iesire)
        self.assertIn("amprenta_unealta", iesire)


class TestRitm(unittest.TestCase):

    def test_text_uniform_e_semnalat(self):
        cod, iesire = ruleaza("check-ritm.py", str(FIXTURES / "pereche-inainte.md"))
        self.assertEqual(cod, 1)
        self.assertIn("ritm_uniform", iesire)
        self.assertIn("fraze_egale", iesire)

    def test_text_variat_nu_e_semnalat(self):
        cod, iesire = ruleaza("check-ritm.py", str(FIXTURES / "bun-articol.md"))
        self.assertEqual(cod, 0, f"proza umana semnalata gresit:\n{iesire}")

    def test_rescrierea_creste_variatia(self):
        """Perechea inainte/dupa demonstreaza ce trebuie sa se intample."""
        def cv(fisier):
            _, iesire = ruleaza("check-ritm.py", str(FIXTURES / fisier))
            linie = next(l for l in iesire.splitlines() if l.startswith("metrici|fraze"))
            return float(linie.split("cv=")[1].split("|")[0])
        self.assertGreater(cv("pereche-dupa.md"), cv("pereche-inainte.md") * 2,
                           "rescrierea nu a variat suficient ritmul")

    def test_capcana_concluziei(self):
        cod, iesire = ruleaza("check-ritm.py", str(FIXTURES / "pereche-inainte.md"))
        self.assertIn("capcana_concluziei", iesire)

    def test_text_scurt_nu_da_verdict(self):
        cod, iesire = ruleaza_stdin("check-ritm.py", "O propozitie. Si inca una.")
        self.assertEqual(cod, 0)
        self.assertIn("prea scurt", iesire)


class TestContractCLI(unittest.TestCase):

    def test_help_pe_toate(self):
        for script in ("check-tipare.py", "check-ritm.py", "check-seo.py"):
            cod, iesire = ruleaza(script, "--help")
            self.assertEqual(cod, 0, script)
            self.assertIn("Usage", iesire, script)

    def test_fisier_lipsa_da_exit_2(self):
        for script in ("check-tipare.py", "check-ritm.py"):
            cod, _ = ruleaza(script, "/nu/exista.md")
            self.assertEqual(cod, 2, script)


def ruleaza_stdin(script, text):
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / script), "-"],
        input=text, capture_output=True, text=True)
    return r.returncode, r.stdout


if __name__ == "__main__":
    unittest.main()
