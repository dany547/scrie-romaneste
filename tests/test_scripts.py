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


class TestModelisme(unittest.TestCase):

    def test_pleonasm_detectat_cu_sugestie(self):
        cod, iesire = ruleaza_stdin("check-modelisme.py",
                                    "A avut o hemoragie de sânge severă.")
        self.assertEqual(cod, 1)
        self.assertIn("pleonasm_etimologic", iesire)
        self.assertIn("→ hemoragie", iesire)

    def test_text_curat_trece(self):
        cod, iesire = ruleaza("check-modelisme.py", str(FIXTURES / "bun-articol.md"))
        self.assertEqual(cod, 0, f"text curat semnalat gresit:\n{iesire}")

    def test_paronimia_da_explicatia_sensurilor(self):
        cod, iesire = ruleaza_stdin("check-modelisme.py",
                                    "Un savant eminent a anuntat un pericol iminent.")
        self.assertEqual(cod, 1)
        self.assertIn("paronimie", iesire)
        self.assertIn("eminent=remarcabil", iesire)

    def test_fara_diacritice_e_prins(self):
        cod, iesire = ruleaza_stdin("check-modelisme.py",
                                    "Mijloacele mass-media au relatat totul.")
        self.assertEqual(cod, 1)
        self.assertIn("pleonasm", iesire)

    def test_fals_pozitive_reparate(self):
        """Regresie: 'caut sa adopt' si 'de aceea' erau semnalate desi sunt corecte."""
        cod, iesire = ruleaza_stdin(
            "check-modelisme.py",
            "Caut să adopt un câine. De aceea am venit abia acum la adăpost.")
        self.assertEqual(cod, 0, f"text corect semnalat:\n{iesire}")


class TestVerifica(unittest.TestCase):

    def test_agrega_scorurile(self):
        cod, iesire = ruleaza("verifica.py", str(FIXTURES / "rau-cu-diacritice.md"))
        self.assertEqual(cod, 1)
        self.assertIn("== tipare AI", iesire)
        self.assertIn("scor_automat=", iesire)
        self.assertIn("/13", iesire)

    def test_text_curat_da_exit_0(self):
        cod, iesire = ruleaza("verifica.py", str(FIXTURES / "bun-articol.md"))
        self.assertEqual(cod, 0, f"text curat semnalat:\n{iesire}")
        self.assertIn("curat", iesire)

    def test_json_e_valid_si_are_sugestii(self):
        import json
        cod, iesire = ruleaza_stdin_cu_flags("verifica.py", "Asta face sens.", "--json")
        date = json.loads(iesire)
        self.assertEqual(cod, 1)
        self.assertEqual(date["scor_maxim"], 13)
        romgleza = [t for t in date["tipare"] if t["categorie"] == "romgleza"]
        self.assertTrue(romgleza)
        self.assertEqual(romgleza[0]["sugestie"], "are sens")

    def test_fara_seo_sare_verificarea_seo(self):
        text = "# Unu\n\ntext\n\n# Doi\n\ntext"  # doua H1 = problema SEO
        cod_cu, iesire_cu = ruleaza_stdin("verifica.py", text)
        self.assertIn("heading", iesire_cu)
        cod_fara, iesire_fara = ruleaza_stdin_cu_flags("verifica.py", text, "--fara-seo")
        self.assertNotIn("heading|", iesire_fara)

    def test_scor_compact(self):
        cod, iesire = ruleaza_stdin_cu_flags(
            "verifica.py", "Un text scurt si cuminte despre nimic.", "--scor")
        self.assertIn("scor_automat=0/13", iesire)
        self.assertEqual(cod, 0)


class TestIgienaTiparelor(unittest.TestCase):
    """Tiparele din CATEGORII ruleaza pe text pliat — diacriticele din regex
    sunt ramuri moarte care nu se potrivesc niciodata."""

    DIACRITICE = set("ăâîșțĂÂÎȘȚşţŞŢ")

    def _verifica_modul(self, nume_script):
        import importlib.util
        cale = SCRIPTS / nume_script
        spec = importlib.util.spec_from_file_location(
            nume_script.replace("-", "_").replace(".py", ""), cale)
        modul = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SCRIPTS))
        try:
            spec.loader.exec_module(modul)
        finally:
            sys.path.remove(str(SCRIPTS))
        for categorie, (_sev, tipare) in modul.CATEGORII.items():
            for intrare in tipare:
                tipar = intrare[0]
                gasite = self.DIACRITICE & set(tipar)
                self.assertFalse(
                    gasite,
                    f"{nume_script}:{categorie}: diacritice moarte {gasite} in {tipar!r}")

    def test_check_tipare_fara_diacritice(self):
        self._verifica_modul("check-tipare.py")

    def test_check_modelisme_fara_diacritice(self):
        self._verifica_modul("check-modelisme.py")


class TestDriftGuard(unittest.TestCase):
    """Expresiile interzise promise in SKILL.md trebuie sa fie prinse de
    check-tipare.py — altfel documentatia si scriptul au divergat."""

    EXPRESII = [
        "În concluzie, asta e tot.",
        "Trăim în era digitală.",
        "Este important de menționat că plouă.",
        "Compania are o abordare holistică.",
        "Oferim o multitudine de servicii.",
        "Asta face sens pentru noi.",
        "Vrem să adresăm această problemă rapid.",
        "Mai mult decât atât, e ieftin.",
    ]

    def test_expresiile_din_skill_sunt_acoperite(self):
        for text in self.EXPRESII:
            cod, iesire = ruleaza_stdin("check-tipare.py", text)
            self.assertEqual(
                cod, 1, f"expresie interzisa neprinsă: {text!r}\n{iesire}")


class TestSeo(unittest.TestCase):

    def test_text_curat_nu_e_semnalat(self):
        cod, iesire = ruleaza("check-seo.py", str(FIXTURES / "bun-articol.md"))
        self.assertEqual(cod, 0, f"articol corect semnalat gresit:\n{iesire}")
        self.assertIn("0 probleme SEO", iesire)

    def test_h1_multiplu(self):
        cod, iesire = ruleaza_stdin("check-seo.py", "# Unu\n\ntext\n\n# Doi\n\ntext")
        self.assertEqual(cod, 1)
        self.assertIn("2 H1", iesire)

    def test_salt_de_nivel(self):
        cod, iesire = ruleaza_stdin("check-seo.py", "# Unu\n\ntext\n\n### Trei\n\ntext")
        self.assertEqual(cod, 1)
        self.assertIn("salt H1->H3", iesire)

    def test_sedila_e_semnalata(self):
        """Sedila (U+015F) in loc de virgula (U+0219) — greseala de norma."""
        cod, iesire = ruleaza_stdin("check-seo.py", "# Titlu\n\nAcesta eşte textul.")
        self.assertEqual(cod, 1)
        self.assertIn("sedila", iesire)

    def test_virgula_corecta_nu_e_semnalata(self):
        cod, iesire = ruleaza_stdin("check-seo.py", "# Titlu\n\nAceșția sunt corecți.")
        self.assertNotIn("sedila", iesire, f"diacritice corecte semnalate:\n{iesire}")

    def test_diacritice_in_url(self):
        text = "# Titlu\n\nVezi [ghidul](https://exemplu.ro/mașină-de-spălat) aici."
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("url_diacritice", iesire)

    def test_url_transliterat_e_acceptat(self):
        text = "# Titlu\n\nVezi [ghidul](https://exemplu.ro/masina-de-spalat) aici."
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertNotIn("url_diacritice", iesire,
                         f"slug ASCII corect semnalat:\n{iesire}")

    def test_sectiune_prea_lunga(self):
        text = "# Titlu\n\n" + ("cuvant " * 500)
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("sectiune_lunga", iesire)

    def test_sectiune_de_dimensiune_buna(self):
        text = "# Titlu\n\n" + ("cuvant " * 150) + "\n\n## Alta\n\n" + ("cuvant " * 150)
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertNotIn("sectiune_lunga", iesire,
                         f"sectiune de dimensiune optima semnalata:\n{iesire}")

    def test_keyword_stuffing(self):
        text = "# Titlu\n\n" + ("cea mai buna oferta de vara. " * 12)
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("keyword_stuffing", iesire)

    def test_headinguri_html(self):
        text = "<h1>Unu</h1><p>text</p><h3>Trei</h3><p>text</p>"
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertIn("salt H1->H3", iesire)


class TestContractCLI(unittest.TestCase):

    TOATE = ("check-tipare.py", "check-ritm.py", "check-seo.py",
             "check-modelisme.py", "verifica.py")

    def test_help_pe_toate(self):
        for script in self.TOATE:
            cod, iesire = ruleaza(script, "--help")
            self.assertEqual(cod, 0, script)
            self.assertIn("Usage", iesire, script)

    def test_fisier_lipsa_da_exit_2(self):
        for script in self.TOATE:
            cod, _ = ruleaza(script, "/nu/exista.md")
            self.assertEqual(cod, 2, script)


def ruleaza_stdin(script, text):
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / script), "-"],
        input=text, capture_output=True, text=True)
    return r.returncode, r.stdout


def ruleaza_stdin_cu_flags(script, text, *flags):
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / script), "-", *flags],
        input=text, capture_output=True, text=True)
    return r.returncode, r.stdout


if __name__ == "__main__":
    unittest.main()
