#!/usr/bin/env python3
"""Teste pentru check-calcuri.py — colocări de recitit, nu verdicte.

Fixează contractul public: liniile `minor|colocare_de_verificat|L<linie>|...`,
exit 0 (nimic) / 1 (cel puțin o pereche de recitit — caz normal) / 2 (eroare de
input sau registry lipsă/defect), aceeași propoziție, fereastră pe cuvinte,
insensibilitate la diacritice și majuscule, excepțiile legitime din registry.
Scriptul nu intră în `verifica.py` și nu are scor; semnalul nu e eroare.

Rulează: python3 -m unittest discover -s tests -p test_calcuri.py -v
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RADACINA = Path(__file__).resolve().parent.parent
SCRIPTS = RADACINA / "scripts"
REGISTRY = RADACINA / "references" / "limba" / "calcuri.json"

PERECHE = "Scripturile externe frânează încărcarea paginii.\n"


def ruleaza(*argumente, text=None, octeti=None):
    comanda = [sys.executable, str(SCRIPTS / "check-calcuri.py"), *argumente]
    if octeti is not None:
        r = subprocess.run(comanda, input=octeti, capture_output=True)
        return (r.returncode, r.stdout.decode("utf-8", "replace"),
                r.stderr.decode("utf-8", "replace"))
    r = subprocess.run(comanda, input=text, capture_output=True,
                       text=True, encoding="utf-8")
    if "Traceback" in r.stderr:
        raise AssertionError(
            f"check-calcuri.py {list(argumente)}: traceback pe stderr:\n{r.stderr}")
    return r.returncode, r.stdout, r.stderr


class TestCalcuri(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def _fisier(self, text, nume="t.md"):
        cale = Path(self.tmp.name) / nume
        cale.write_text(text, encoding="utf-8")
        return str(cale)

    # --- formatul raportului (contract public) -------------------------

    def test_pereche_verb_obiect_e_semnalata(self):
        cod, iesire, _ = ruleaza("-", text=PERECHE)
        self.assertEqual(cod, 1)
        linii = iesire.splitlines()
        self.assertEqual(len(linii), 4)
        self.assertTrue(linii[0].startswith("minor|colocare_de_verificat|L1|"))
        self.assertIn("Scripturile externe frânează încărcarea paginii.", linii[0])
        self.assertIn("|→ ", linii[0])
        self.assertEqual(linii[1], "---")
        self.assertEqual(linii[2], "total=1 colocare de verificat | 5 cuvinte")
        self.assertTrue(linii[3].startswith("nota: "))
        self.assertIn("nu e calc confirmat", linii[3])
        self.assertIn("revizia contextuală", linii[3])

    def test_plural_la_mai_multe_perechi(self):
        text = ("Aici frânează încărcarea paginii.\n"
                "Acolo frânează încărcarea fișierelor.\n")
        cod, iesire, _ = ruleaza("-", text=text)
        self.assertEqual(cod, 1)
        linii = [l for l in iesire.splitlines() if l.startswith("minor|")]
        self.assertEqual(len(linii), 2)
        self.assertIn("|L1|", linii[0])
        self.assertIn("|L2|", linii[1])
        self.assertIn("total=2 colocări de verificat", iesire)

    def test_un_semnal_pe_propozitie_si_per_regula(self):
        cod, iesire, _ = ruleaza(
            "-", text="Frânează și frânează încărcarea paginii.\n")
        self.assertEqual(cod, 1)
        self.assertEqual(
            len([l for l in iesire.splitlines() if l.startswith("minor|")]), 1)

    # --- diacritice, majuscule, forme flexionare -----------------------

    def test_fara_diacritice_si_cu_sedila_e_prins(self):
        cod, iesire, _ = ruleaza(
            "-", text="Scripturile şterse franeaza incarcarea paginii.\n")
        self.assertEqual(cod, 1)
        self.assertIn("minor|colocare_de_verificat|L1|", iesire)

    def test_majuscule_nu_conteaza(self):
        cod, iesire, _ = ruleaza("-", text="FRÂNEAZĂ ÎNCĂRCAREA.\n")
        self.assertEqual(cod, 1, iesire)

    def test_forme_flexionare_prinse(self):
        for text in ("Scripturile frânează vizibil încărcarea paginii.\n",
                     "A frânat încărcarea paginii.\n",
                     "Încărcarea paginii o frânează scripturile.\n"):
            cod, iesire, _ = ruleaza("-", text=text)
            self.assertEqual(cod, 1, text)

    # --- propoziții, ferestre, termeni izolați -------------------------

    def test_termenii_izolati_tac(self):
        for text in ("Scripturile frânează rularea paginii.\n",
                     "Încărcarea durează mai puțin.\n"):
            cod, iesire, _ = ruleaza("-", text=text)
            self.assertEqual(cod, 0, f"{text!r}\n{iesire}")
            self.assertIn("0 colocări de verificat", iesire)

    def test_propozitii_separate_tac(self):
        text = "Site-ul frânează vizitatorii. Încărcarea durează mult.\n"
        cod, iesire, _ = ruleaza("-", text=text)
        self.assertEqual(cod, 0, iesire)

    def test_paragrafe_separate_tac(self):
        text = "Scripturile frânează tot.\n\nÎncărcarea crește la galerie.\n"
        cod, iesire, _ = ruleaza("-", text=text)
        self.assertEqual(cod, 0, iesire)

    def test_element_de_lista_inchide_propozitia(self):
        text = "- Scripturile frânează tot\n- încărcarea crește la galerie\n"
        cod, iesire, _ = ruleaza("-", text=text)
        self.assertEqual(cod, 0, iesire)

    def test_randul_impartit_ramane_acelasi_propozitie(self):
        text = "Scripturile externe\nfrânează încărcarea paginii.\n"
        cod, iesire, _ = ruleaza("-", text=text)
        self.assertEqual(cod, 1, iesire)
        self.assertIn("|L2|", iesire)

    def test_fereastra_implicita_limiteaza_perechile(self):
        umplutura = " ".join(f"w{i}" for i in range(10))
        cod, _, _ = ruleaza("-", text=f"Frânează {umplutura} încărcarea.\n")
        self.assertEqual(cod, 1)  # exact 10 cuvinte între: încă în fereastră
        umplutura = " ".join(f"w{i}" for i in range(11))
        cod, _, _ = ruleaza("-", text=f"Frânează {umplutura} încărcarea.\n")
        self.assertEqual(cod, 0)  # 11: în afara ferestrei implicite

    def test_fereastra_personalizata(self):
        umplutura = " ".join(f"w{i}" for i in range(11))
        text = f"Frânează {umplutura} încărcarea.\n"
        cod, _, _ = ruleaza("-", text=text)
        self.assertEqual(cod, 0)
        cod, iesire, _ = ruleaza("-", "--fereastra", "11", text=text)
        self.assertEqual(cod, 1, iesire)

    # --- excepții de sintaxă (registry) --------------------------------

    def test_sistem_de_franare_ramine_tacut(self):
        text = "Sistemul de frânare suportă încărcarea maximă a remorcii.\n"
        cod, iesire, _ = ruleaza("-", text=text)
        self.assertEqual(cod, 0, iesire)

    def test_exceptia_merge_si_pe_rand_impartit(self):
        text = "Sistemul de\nfrânare suportă încărcarea maximă.\n"
        cod, iesire, _ = ruleaza("-", text=text)
        self.assertEqual(cod, 0, iesire)

    def test_incarcatorul_e_obiect_exclus(self):
        cod, iesire, _ = ruleaza("-", text="Încărcătorul frontal frânează în curte.\n")
        self.assertEqual(cod, 0, iesire)

    def test_frana_substantivul_nu_e_marcat(self):
        """Forma ambiguă «frâna» e acoperită doar cu marcă contextuală:
        substantivul și imperfectul fără marcă rămân intenționat în tăcere."""
        for text in ("Frâna mașinii se blochează la încărcarea maximă.\n",
                     "Șoferul frâna greu la coborâre, iar încărcarea aluneca.\n"):
            cod, iesire, _ = ruleaza("-", text=text)
            self.assertEqual(cod, 0, f"{text!r}\n{iesire}")

    def test_substantivele_derivate_nu_sunt_forme_de_infinitiv(self):
        for forma in ("frânarea", "frânare", "frânări"):
            text = f"Nu trebuie {forma} încărcării la rampă.\n"
            cod, iesire, _ = ruleaza("-", text=text)
            self.assertEqual(cod, 0, f"{text!r}\n{iesire}")

    def test_infinitivul_si_viitorul_cu_marca_e_prins(self):
        """«Pot frâna încărcarea» era neacoperit: forma ambiguă «frâna» contează
        ca verb doar cu marcă de infinitiv/viitor/modal imediat în față."""
        for text in ("Pot frâna încărcarea paginii.\n",
                     "A frâna încărcarea durează.\n",
                     "Va frâna încărcarea, garantat.\n",
                     "Trebuie să frâna încărcarea Operatorul.\n",
                     "Ar trebui să frâna încărcarea cineva.\n"):
            cod, iesire, _ = ruleaza("-", text=text)
            self.assertEqual(cod, 1, f"{text!r}\n{iesire}")

    def test_marca_contextuala_cere_inceput_de_cuvant(self):
        """Strictețe: «a»-ul din interiorul unui cuvânt («camera») nu e marcă
        de infinitiv — fără ancora de cuvânt, «Camera frâna» ar fi fals pozitiv."""
        cod, iesire, _ = ruleaza(
            "-", text="Camera frâna la fiecare mișcare, iar încărcarea creștea.\n")
        self.assertEqual(cod, 0, iesire)

    def test_incarcatura_e_exclusa(self):
        """«încărcătură» e sarcina transportată, nu procesul — nu e obiectul căutat."""
        for text in ("Camionul frânează brusc cu încărcătura completă.\n",
                     "Frânează cu încărcături grele pe rampă.\n"):
            cod, iesire, _ = ruleaza("-", text=text)
            self.assertEqual(cod, 0, f"{text!r}\n{iesire}")

    def test_context_logistic_primeste_mesaj_neutru(self):
        """Fals pozitiv documentat: frânare fizică lângă «încărcare» se
        marchează, dar cu mesaj neutru — fără calc sau site prezise."""
        cod, iesire, _ = ruleaza(
            "-", text="Camionul frânează la rampa de încărcare.\n")
        self.assertEqual(cod, 1)
        linie = next(l for l in iesire.splitlines() if l.startswith("minor|"))
        mic = linie.lower()
        for cuvant in ("site", "pagin", "slows down"):
            self.assertNotIn(cuvant, mic, linie)
        self.assertIn("de recitit în context", linie)
        self.assertIn("nu e verdict", linie)
        self.assertIn("nota: ", iesire)

    # --- flaguri și erori ----------------------------------------------

    def test_fisierul_e_acceptat(self):
        cod, iesire, _ = ruleaza(self._fisier(PERECHE))
        self.assertEqual(cod, 1)
        self.assertIn("minor|colocare_de_verificat|L1|", iesire)

    def test_stdin_si_fisier_dau_acelasi_raport(self):
        cod_f, iesire_f, _ = ruleaza(self._fisier(PERECHE))
        cod_s, iesire_s, _ = ruleaza("-", text=PERECHE)
        self.assertEqual((cod_f, iesire_f), (cod_s, iesire_s))

    def test_iesire_deterministica(self):
        rulari = [ruleaza("-", text=PERECHE) for _ in range(3)]
        self.assertEqual(len(set(rulari)), 1)

    def test_help_si_fisier_lipsa(self):
        cod, iesire, _ = ruleaza("--help")
        self.assertEqual(cod, 0)
        self.assertIn("Usage", iesire)
        cod, _, _ = ruleaza("/nu/exista.md")
        self.assertEqual(cod, 2)

    def test_flag_fara_valoare_si_fereastra_invalida(self):
        for argumente in (("--fereastra",), ("--fereastra", "abc"),
                          ("--fereastra", "-1"), ("--fereastra", "100")):
            cod, iesire, eroare = ruleaza("-", *argumente, text=PERECHE)
            self.assertEqual(cod, 2, argumente)
            self.assertIn("eroare:", eroare)

    def test_forma_cu_egale_e_suportata(self):
        """--fereastra=0 nu se ignoră în tăcere: fereastra 0 cere adjacenie."""
        cod, _, _ = ruleaza("-", "--fereastra=0", text="Frânează w1 încărcarea.\n")
        self.assertEqual(cod, 0)
        cod, iesire, _ = ruleaza("-", "--fereastra=1",
                                 text="Frânează w1 încărcarea.\n")
        self.assertEqual(cod, 1, iesire)
        cod, _, _ = ruleaza("-", "--fereastra=0",
                            text="Frânează încărcarea paginii.\n")
        self.assertEqual(cod, 1)  # adiacente: în fereastră și la 0
        for argumente in (("--fereastra=abc",), ("--fereastra=",),
                          ("--fereastra=-1",), ("--fereastra=100",)):
            cod, _, eroare = ruleaza("-", *argumente, text=PERECHE)
            self.assertEqual(cod, 2, argumente)
            self.assertIn("eroare:", eroare)

    def test_forma_cu_egale_la_registry(self):
        cale = self._registry({
            "schema_version": 1,
            "reguli": [{"id": "test", "verb_stem": ["xxxx"],
                        "obiect_stem": ["yyyy"], "sugestie": "recitește"}],
        }, "egal.json")
        cod, iesire, _ = ruleaza("-", f"--registry={cale}",
                                 text="Aici xxxx yyyy stă prost.\n")
        self.assertEqual(cod, 1, iesire)
        self.assertIn("|→ recitește", iesire)

    def test_argumente_necunoscute_sunt_refuzate(self):
        for argumente in (("--necunoscut",), ("--necunoscut=1",), ("-x",),
                          ("--sugestii",), (PERECHE, "--necunoscut")):
            cod, _, eroare = ruleaza("-", *argumente, text=PERECHE)
            self.assertEqual(cod, 2, argumente)
            self.assertIn("necunoscut", eroare)

    def test_doua_pozitionale_e_exit_2(self):
        cod, _, eroare = ruleaza("a.md", "b.md")
        self.assertEqual(cod, 2)
        self.assertIn("exact un fișier", eroare)

    def test_input_non_utf8_e_exit_2_fara_traceback(self):
        cod, iesire, eroare = ruleaza("-", octeti=b"\xff\xfe\n")
        self.assertEqual(cod, 2)
        self.assertIn("eroare:", eroare)

    def test_registry_lipsa_e_exit_2(self):
        cod, _, eroare = ruleaza("-", "--registry", "/nu/exista.json",
                                 text=PERECHE)
        self.assertEqual(cod, 2)
        self.assertIn("eroare: registry-ul", eroare)
        self.assertIn("/nu/exista.json", eroare)

    # --- registry defecte (date statice, validate strict) ---------------

    def _registry(self, date, nume, brut=None):
        cale = Path(self.tmp.name) / nume
        if brut is not None:
            cale.write_bytes(brut)
        else:
            cale.write_text(json.dumps(date, ensure_ascii=False),
                            encoding="utf-8")
        return str(cale)

    def test_registry_json_rupt_e_exit_2(self):
        cale = Path(self.tmp.name) / "rupt.json"
        cale.write_text('{"reguli": [', encoding="utf-8")
        cod, _, eroare = ruleaza("-", "--registry", str(cale), text=PERECHE)
        self.assertEqual(cod, 2)
        self.assertIn("nu e JSON valid", eroare)

    def test_registry_non_utf8_e_exit_2(self):
        cale = self._registry(None, "non-utf8.json", brut=b"\xff\xfe")
        cod, _, eroare = ruleaza("-", "--registry", cale, text=PERECHE)
        self.assertEqual(cod, 2)
        self.assertIn("nu e UTF-8 valid", eroare)

    def test_registry_fara_reguli_e_exit_2(self):
        for date in ({}, {"schema_version": 1}, {"schema_version": 1, "reguli": []},
                     {"schema_version": 2, "reguli": [{"id": "x"}]}):
            cale = self._registry(date, "fara-reguli.json")
            cod, _, eroare = ruleaza("-", "--registry", cale, text=PERECHE)
            self.assertEqual(cod, 2, date)
            self.assertIn("eroare: registry-ul", eroare)

    def test_registry_cu_regula_invalida_e_exit_2(self):
        baza = {"schema_version": 1}
        reguli = (
            {"id": "x", "verb_stem": [], "obiect_stem": ["y"], "sugestie": "s"},
            {"id": "x", "verb_stem": ["x"], "obiect_stem": ["y"]},
            {"id": "x", "verb_stem": ["x"], "obiect_stem": ["y"], "sugestie": "s",
             "exceptii_verb": "("},
        )
        for regula in reguli:
            cale = self._registry(dict(baza, reguli=[regula]), "regula-rau.json")
            cod, _, eroare = ruleaza("-", "--registry", cale, text=PERECHE)
            self.assertEqual(cod, 2, regula)
            self.assertIn("eroare: registry-ul", eroare)

    def test_schema_version_boolean_e_respins(self):
        """True == 1 în Python: validarea trebuie să ceară număr, nu bool."""
        for versiune in (True, False, "1", 1.0, 2):
            date = {"schema_version": versiune,
                    "reguli": [{"id": "x", "verb_stem": ["x"],
                                "obiect_stem": ["y"], "sugestie": "s"}]}
            cale = self._registry(date, "versiune-rau.json")
            cod, _, eroare = ruleaza("-", "--registry", cale, text=PERECHE)
            self.assertEqual(cod, 2, versiune)
            self.assertIn("schema_version", eroare)

    def test_forme_nefoldite_sunt_respinse(self):
        """Formele cu majuscule sau diacritice n-ar potrivi niciodată pe textul
        pliat — validarea le refuză explicit, nu le lasă să tacă."""
        baza = {"schema_version": 1, "reguli": [{
            "id": "x", "verb_stem": ["x"], "obiect_stem": ["y"],
            "sugestie": "s"}]}
        modificari = (
            ("verb_stem", ["Franeaz"]),
            ("verb_stem", ["frâneaz"]),
            ("obiect_stem", ["Încarc"]),
            ("exceptii_obiect", ["Incarcator"]),
            ("exceptii_obiect", ["încărcător"]),
            ("exceptii_verb", ["sistem de Frânare"]),
        )
        for cheie, valoare in modificari:
            regula = dict(baza["reguli"][0])
            regula[cheie] = valoare
            cale = self._registry(dict(baza, reguli=[regula]), "nefoldit.json")
            cod, _, eroare = ruleaza("-", "--registry", cale, text=PERECHE)
            self.assertEqual(cod, 2, (cheie, valoare))
            self.assertIn("pliat și cu minuscule", eroare)

    def test_verb_contexte_invalid_e_respins(self):
        baza = {"schema_version": 1, "reguli": [{
            "id": "x", "verb_stem": ["x"], "obiect_stem": ["y"],
            "sugestie": "s", "verb_contexte": [{"stem": "x",
                                               "contexte": ["a"]}]}]}
        cale = self._registry(baza, "context-bun.json")
        cod, _, _ = ruleaza("-", "--registry", cale, text="a xxxx yyyy.\n")
        self.assertEqual(cod, 1)  # forma contextuală validă funcționează
        for context in ([{"stem": "Frâna", "contexte": ["a"]}],
                        [{"stem": "frana", "contexte": []}],
                        [{"stem": "frana"}],
                        "nu-e-obiect"):
            regula = dict(baza["reguli"][0])
            regula["verb_contexte"] = context
            cale = self._registry(dict(baza, reguli=[regula]), "context-rau.json")
            cod, _, eroare = ruleaza("-", "--registry", cale, text=PERECHE)
            self.assertEqual(cod, 2, context)
            self.assertIn("eroare: registry-ul", eroare)

    def test_registry_personalizat_functioneaza(self):
        cale = self._registry({
            "schema_version": 1,
            "reguli": [{"id": "test", "verb_stem": ["xxxx"],
                        "obiect_stem": ["yyyy"], "sugestie": "recitește perechea"}],
        }, "personalizat.json")
        cod, iesire, _ = ruleaza("-", "--registry", cale,
                                 text="Aici xxxx yyyy stă prost.\n")
        self.assertEqual(cod, 1)
        self.assertIn("minor|colocare_de_verificat|L1|", iesire)
        self.assertIn("|→ recitește perechea", iesire)

    # --- registry-ul livrat: forme care nu trebuie să field false positive --

    def test_registry_livrat_acopera_familia_si_controlul(self):
        """Perechea suspectă se marchează; construcțiile legitime din ghid tac."""
        for text, asteptat in (
                ("Elementele animate încetinesc încărcarea paginii.\n", 0),
                ("Bannerele animate frânează încărcarea paginii de pornire.\n", 1),
                ("Sistemul de frânare al remorcii suportă sarcina maximă.\n", 0)):
            cod, iesire, _ = ruleaza("-", text=text)
            self.assertEqual(cod, asteptat, f"{text!r}\n{iesire}")

    def test_registry_livrat_are_schema_corecta(self):
        date = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(date["schema_version"], 1)
        self.assertNotIsInstance(date["schema_version"], bool)
        self.assertEqual(date["status"], "draft_nevalidat_uman")
        self.assertTrue(date["reguli"])
        for regula in date["reguli"]:
            self.assertIn("franeaz", regula["verb_stem"])
            self.assertIn("incarc", regula["obiect_stem"])
            sugestie = regula["sugestie"]
            # mesaj neutru: marchează perechea pentru recitire, fără calc
            # sau site prezise, fără reformulare de web-copy în mesajul fix
            self.assertIn("de recitit în context", sugestie)
            self.assertIn("nu e verdict", sugestie)
            for cuvant in ("site", "pagin", "slows down", "încetinește"):
                self.assertNotIn(cuvant, sugestie)
            # forma ambiguă «frâna» doar cu marcă contextuală; sarcina exclusă
            self.assertIn("incarcatur\\w*", regula["exceptii_obiect"])
            contextuale = {i["stem"]: i["contexte"]
                           for i in regula.get("verb_contexte", [])}
            self.assertIn("frana", contextuale)
            self.assertTrue(contextuale["frana"])


if __name__ == "__main__":
    unittest.main()
