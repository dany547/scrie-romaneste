#!/usr/bin/env python3
"""Guard de regresie pentru documentația de revizie contextuală și lookup-ul dexonline.

NU e verdict semantic general despre documentație și nu înlocuiește lectura.
Verifică doar un set restrâns de clauze vechi, cunoscut periculoase, pe paragrafe
cu spațiile normalizate:
- absența dintr-o sursă tratată ca inexistență sau respingere;
- comanda veche de retry `curl -s -L -A`.

Plus prezențe de structură: urmă internă pe propoziții (OK/RESCRIU/NECLAR),
citirea standalone a titlurilor, verificarea corecției pe cinci planuri și
exemplele greșit/bun cu control. Propozițiile de interdicție („nu autoriza
scraping") nu sunt penalizate: detectorul caută doar formulările vechi, exacte.

Rulează: python3 -m unittest discover -s tests -p test_revizie_contextuala.py -v
"""
import re
import unittest
from pathlib import Path

RADACINA = Path(__file__).resolve().parent.parent

DOCUMENTE = [
    "SKILL.md",
    "README.md",
    "references/limba/tipare-ro.md",
    "references/limba/revizie-contextuala.md",
]
REFERINTA = "references/limba/revizie-contextuala.md"

# Clauze vechi, cunoscute ca periculoase. Fiecare cere un model exact, nu o clasă.
CLAUZE_VECHI = {
    "absenta_inseamna_inexistenta": re.compile(
        r"nu (este|e) în dicționar\W+(înseamnă|deci)\s+(că\s+)?(forma\s+)?nu există", re.I),
    "pagina_spune_forma_nu_exista": re.compile(
        r"pagina\b[^.]{0,120}\bforma nu există\b", re.I),
    "absenta_nu_se_livreaza": re.compile(
        r"(absent|neatestat)\w*[^.]{0,120}\bnu se livrează\b", re.I),
}

# Comanda de retry care ocolea pagina: nu are ce căuta în documentație.
RETRY_CURL = "curl -s -L -A"
REGULA_ACCES = "nu autoriza scraping"


def _paragrafe(text):
    """Paragrafe cu spațiile normalizate: un rând nou în mijlocul unei fraze nu contează."""
    return [" ".join(p.split()) for p in re.split(r"\n\s*\n", text) if p.strip()]


def gaseste_clauze_vechi(text):
    """Numele clauzelor vechi găsite în text, una per paragraf în care apar."""
    gasite = []
    for paragraf in _paragrafe(text):
        for nume, model in CLAUZE_VECHI.items():
            if model.search(paragraf):
                gasite.append(nume)
    return gasite


def _citeste(relativ):
    return (RADACINA / relativ).read_text(encoding="utf-8")


class TestDetectorClauzeVechi(unittest.TestCase):
    """Testele helperului: dovedesc că guard-ul prinde ce trebuie și lasă liber ce nu."""

    def test_clauza_veche_e_detectata(self):
        text = "Nu este în dicționar înseamnă că forma nu există."
        self.assertEqual(gaseste_clauze_vechi(text), ["absenta_inseamna_inexistenta"])

    def test_formularea_corecta_e_permisa(self):
        text = "Absența nu dovedește inexistența: forma poate lipsi dintr-o sursă."
        self.assertEqual(gaseste_clauze_vechi(text), [])

    def test_clauza_veche_pe_mai_multe_randuri_e_detectata(self):
        """Spațiile normalizate: fraza tăiată de un rând nou rămâne aceeași clauză."""
        text = "Pagina spune\n   că forma nu există, deci verifică din nou."
        self.assertEqual(gaseste_clauze_vechi(text), ["pagina_spune_forma_nu_exista"])


class TestDocumentatieFaraClauzeVechi(unittest.TestCase):
    """Guard: documentele din repo nu conțin clauzele vechi cunoscute."""

    def test_nicio_clauza_veche_in_documente(self):
        gasite = {doc: gaseste_clauze_vechi(_citeste(doc)) for doc in DOCUMENTE}
        gasite = {doc: c for doc, c in gasite.items() if c}
        self.assertEqual(gasite, {}, "clauze vechi periculoase în documentație")

    def test_fara_comanda_veche_de_retry(self):
        for doc in DOCUMENTE:
            paragrafe = " ".join(_paragrafe(_citeste(doc)))
            self.assertNotIn(RETRY_CURL, paragrafe, f"comanda veche în {doc}")


class TestReferintaRevizie(unittest.TestCase):
    """Prezențe pozitive: raportul de audit și regula de acces."""

    @classmethod
    def setUpClass(cls):
        cls.plat = " ".join(_citeste(REFERINTA).split())

    def test_raportul_de_audit_are_campurile_si_clasele(self):
        for camp in ["citatul exact", "motivul concret", "corecția minimă", "verdictul",
                     "eroare susținută", "suspiciune contextuală", "preferință", "neclar"]:
            self.assertIn(camp, self.plat, camp)

    def test_absenta_nu_dovedeste_inexistenta(self):
        self.assertIn("absența nu dovedește inexistența", self.plat.lower())

    def test_regula_de_acces_fara_scraping(self):
        self.assertIn(REGULA_ACCES, self.plat)

    def test_urma_interna_pe_fiecare_propozitie(self):
        """Fiecare propoziție primește o urmă internă, cu cele trei stări."""
        for camp in ["urmă internă", "OK", "RESCRIU", "NECLAR"]:
            self.assertIn(camp, self.plat, camp)

    def test_titluri_citite_standalone(self):
        self.assertIn("standalone", self.plat)

    def test_corectia_se_verifica_pe_cinci_planuri(self):
        """Corecția aplicată se recitește: sens, repetiție, adresare, registru, fapte."""
        for camp in ["se recitește și ea", "pe cinci planuri", "sens",
                     "repetiție", "adresare", "registru", "fapte"]:
            self.assertIn(camp, self.plat, camp)

    def test_exemple_gresit_bun_cu_control(self):
        """Perechile greșit/bun și controalele lor sunt în ghid."""
        for frag in ["Ce câștigi când e rapidă", "Ce câștigi cu un site rapid",
                     "Viteza bună se vede în confortul fiecărei vizite",
                     "O pagină care se încarcă rapid face navigarea mai plăcută",
                     "control:"]:
            self.assertIn(frag, self.plat, frag)


if __name__ == "__main__":
    unittest.main()
