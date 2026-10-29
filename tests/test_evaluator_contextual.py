#!/usr/bin/env python3
"""Teste pentru evaluatorul offline de predicții (scripts/evaluare-contextuala.py).

Scriptul nu rulează modele și nu evaluează texte: compară un fișier de
predicții deja furnizate cu etichetele draft din corpus și numără potriviri,
ratări, fals-pozitive. Testele verifică exact atât: numărarea pe cazuri
construite (ratare, fals pozitiv, escaladare, pereche eroare/suspiciune),
refuzul datelor incomplete sau invalide, codurile de ieșire și onestitatea
raportului (status draft, fără pretenții de benchmark). Nimic aici nu atestă
performanța vreunui model.

Rulează: python3 -m unittest discover -s tests -p test_evaluator_contextual.py -v
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RADACINA = Path(__file__).resolve().parent.parent
SCRIPT = RADACINA / "scripts" / "evaluare-contextuala.py"
CORPUS = RADACINA / "tests" / "fixtures" / "evaluare-contextuala.json"


def _etichete():
    with CORPUS.open(encoding="utf-8") as f:
        return {c["id"]: c["expected_verdict"] for c in json.load(f)["cases"]}


def _ruleaza(predictii, *extra, corpus=str(CORPUS), stdin=False):
    """Rulează evaluatorul; întoarce (cod ieșire, stdout, stderr).

    Cu `stdin=True` predicțiile merg pe stdin (cale `-`), ca la celelalte
    scripturi din repo.
    """
    if stdin:
        comanda = [sys.executable, str(SCRIPT), "-", "--corpus", corpus]
        comanda += list(extra)
        r = subprocess.run(comanda, input=json.dumps(predictii, ensure_ascii=False),
                           capture_output=True, text=True)
        return r.returncode, r.stdout, r.stderr
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8") as f:
        json.dump(predictii, f, ensure_ascii=False)
        cale = f.name
    try:
        comanda = [sys.executable, str(SCRIPT), cale, "--corpus", corpus]
        comanda += list(extra)
        r = subprocess.run(comanda, capture_output=True, text=True)
        return r.returncode, r.stdout, r.stderr
    finally:
        Path(cale).unlink(missing_ok=True)


def _linia(out, prefix):
    potrivite = [l for l in out.splitlines() if l.startswith(prefix)]
    return potrivite[0] if potrivite else ""


def _intoarce_verdictul(pred, cid, verdict):
    copie = [dict(p) for p in pred]
    for p in copie:
        if p["id"] == cid:
            p["verdict"] = verdict
    return copie


class TestEvaluatorContextual(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with CORPUS.open(encoding="utf-8") as f:
            cls.cazuri = json.load(f)["cases"]
        cls.etichete = {c["id"]: c["expected_verdict"] for c in cls.cazuri}
        cls.splituri = {c["id"]: c["split"] for c in cls.cazuri}
        cls.perfecte = [{"id": c["id"], "verdict": c["expected_verdict"]}
                        for c in cls.cazuri]
        cls.id_eroare = next(i for i, v in cls.etichete.items() if v == "eroare")
        cls.id_pastreaza = next(i for i, v in cls.etichete.items()
                                if v == "pastreaza")
        cls.id_neclar = next(i for i, v in cls.etichete.items() if v == "neclar")
        cls.id_suspiciune = next(i for i, v in cls.etichete.items()
                                 if v == "suspiciune")

    def _perfecte_pentru(self, split):
        """Predicții corecte doar pentru id-urile splitului dat."""
        return [{"id": c["id"], "verdict": c["expected_verdict"]}
                for c in self.cazuri if c["split"] == split]

    # --- numărare ------------------------------------------------------

    def test_predictii_perfecte_tot_potrivit(self):
        cod, out, err = _ruleaza(self.perfecte)
        self.assertEqual(cod, 0, err)
        self.assertIn("status|draft_nevalidat_uman", out)
        n = len(self.perfecte)
        self.assertIn(f"acoperire|{n}/{n}", out)
        total = _linia(out, "total|")
        self.assertIn(f"potrivit={n}", total)
        for b in ("semnal_acceptabil=0", "escaladat=0", "ratat=0",
                  "neclar_ratat=0", "fals_pozitiv=0"):
            self.assertIn(b, total, b)
        self.assertNotIn("detaliu|", out)

    def test_ratare_eroare_etichetata_pastreaza(self):
        pred = _intoarce_verdictul(self.perfecte, self.id_eroare, "pastreaza")
        cod, out, _ = _ruleaza(pred)
        self.assertEqual(cod, 0)
        total = _linia(out, "total|")
        self.assertIn("ratat=1", total)
        self.assertIn(f"potrivit={len(pred) - 1}", total)
        self.assertIn("fals_pozitiv=0", total)

    def test_fals_pozitiv_control_etichetat_eroare(self):
        pred = _intoarce_verdictul(self.perfecte, self.id_pastreaza, "eroare")
        cod, out, _ = _ruleaza(pred)
        self.assertEqual(cod, 0)
        total = _linia(out, "total|")
        self.assertIn("fals_pozitiv=1", total)
        self.assertIn(f"potrivit={len(pred) - 1}", total)
        self.assertIn("ratat=0", total)

    def test_escaladare_eroare_etichetata_neclar(self):
        """Întreabă în loc să corecteze: conservator, dar nu potrivit."""
        pred = _intoarce_verdictul(self.perfecte, self.id_eroare, "neclar")
        cod, out, _ = _ruleaza(pred)
        self.assertEqual(cod, 0)
        total = _linia(out, "total|")
        self.assertIn("escaladat=1", total)
        self.assertIn("ratat=0", total)
        self.assertIn(f"potrivit={len(pred) - 1}", total)

    def test_pereche_eroare_suspiciune_e_semnal_acceptabil(self):
        pred = _intoarce_verdictul(self.perfecte, self.id_eroare, "suspiciune")
        cod, out, _ = _ruleaza(pred)
        self.assertEqual(cod, 0)
        total = _linia(out, "total|")
        self.assertIn("semnal_acceptabil=1", total)
        self.assertIn("ratat=0", total)

    def test_neclar_ratat(self):
        pred = _intoarce_verdictul(self.perfecte, self.id_neclar, "pastreaza")
        cod, out, _ = _ruleaza(pred)
        self.assertEqual(cod, 0)
        self.assertIn("neclar_ratat=1", _linia(out, "total|"))

    def test_numarare_pe_split(self):
        """Cazul modificat se numără în splitul lui, nu doar la total."""
        pred = _intoarce_verdictul(self.perfecte, self.id_eroare, "pastreaza")
        cod, out, _ = _ruleaza(pred, "--detaliu")
        self.assertEqual(cod, 0)
        split = self.id_eroare.split("-")[1]  # „ref” / „hold”
        nume_split = {"ref": "referinta", "hold": "holdout"}[split]
        rand_split = _linia(out, f"{nume_split}|")
        self.assertIn("ratat=1", rand_split)

    # --- --split: evaluare pe un singur split --------------------------

    def test_split_referinta_exclusiv(self):
        """--split referinta: numără doar splitul ales și nu emite rezultate
        pentru holdout. Corpusul se încarcă întreg înainte de filtrare —
        testul nu pretinde izolare la încărcare."""
        pred = self._perfecte_pentru("referinta")
        cod, out, err = _ruleaza(pred, "--split", "referinta")
        self.assertEqual(cod, 0, err)
        n = len(pred)
        self.assertIn(f"acoperire|{n}/{n}", out)
        self.assertIn("referinta|", out)
        self.assertNotIn("holdout|", out)
        self.assertEqual(_linia(out, "total|").split("|", 1)[1],
                         _linia(out, "referinta|").split("|", 1)[1])

    def test_split_holdout_exclusiv(self):
        """--split holdout: numără doar splitul ales și nu emite rezultate
        pentru referinta. Corpusul se încarcă întreg înainte de filtrare —
        testul nu pretinde izolare la încărcare."""
        pred = self._perfecte_pentru("holdout")
        cod, out, err = _ruleaza(pred, "--split", "holdout")
        self.assertEqual(cod, 0, err)
        self.assertIn(f"acoperire|{len(pred)}/{len(pred)}", out)
        self.assertIn("holdout|", out)
        self.assertNotIn("referinta|", out)
        self.assertIn("potrivit=24", _linia(out, "holdout|"))

    def test_id_alt_split_respins_la_split_selectat(self):
        """Cu --split referinta, un id de holdout e id necunoscut: exit 1."""
        pred = self._perfecte_pentru("referinta")
        id_holdout = next(i for i, s in self.splituri.items() if s == "holdout")
        pred.append({"id": id_holdout, "verdict": "eroare"})
        cod, out, _ = _ruleaza(pred, "--split", "referinta")
        self.assertEqual(cod, 1)
        self.assertIn(f"problema|id necunoscut în predicții: {id_holdout}", out)
        self.assertNotIn("total|", out)

    def test_split_cu_id_lipsa_din_splitul_ales_blocheaza(self):
        pred = self._perfecte_pentru("holdout")[:-1]
        cod, out, _ = _ruleaza(pred, "--split", "holdout")
        self.assertEqual(cod, 1)
        self.assertIn("problema|id lipsă din predicții", out)

    def test_split_invalid_exit_2(self):
        cod, out, err = _ruleaza(self.perfecte, "--split", "tot")
        self.assertEqual(cod, 2)

    def test_split_json_structurat_fara_cealalt_split(self):
        pred = self._perfecte_pentru("referinta")
        cod, out, _ = _ruleaza(pred, "--split", "referinta", "--json")
        self.assertEqual(cod, 0)
        date = json.loads(out)
        self.assertIn("referinta", date)
        self.assertNotIn("holdout", date)
        self.assertEqual(sum(date["referinta"].values()), len(pred))

    # --- --detaliu -----------------------------------------------------

    def test_detaliu_lista_deviații(self):
        pred = _intoarce_verdictul(self.perfecte, self.id_eroare, "pastreaza")
        cod, out, _ = _ruleaza(pred, "--detaliu")
        self.assertEqual(cod, 0)
        self.assertIn(f"detaliu|{self.id_eroare}|", out)
        self.assertIn("|eticheta=eroare|prezis=pastreaza", out)

    def test_fara_detaliu_fara_lista(self):
        pred = _intoarce_verdictul(self.perfecte, self.id_eroare, "pastreaza")
        cod, out, _ = _ruleaza(pred)
        self.assertEqual(cod, 0)
        self.assertNotIn("detaliu|", out)

    # --- date incomplete / invalide (exit 1, fără numărări) ------------

    def test_id_lipsa_blocheaza(self):
        cod, out, _ = _ruleaza(self.perfecte[:-1])
        self.assertEqual(cod, 1)
        self.assertIn("problema|id lipsă din predicții", out)
        self.assertNotIn("total|", out)

    def test_id_necunoscut_blocheaza(self):
        pred = self.perfecte + [{"id": "inexistent-ref-99", "verdict": "eroare"}]
        cod, out, _ = _ruleaza(pred)
        self.assertEqual(cod, 1)
        self.assertIn("problema|id necunoscut în predicții: inexistent-ref-99", out)

    def test_id_duplicat_blocheaza(self):
        pred = self.perfecte + [dict(self.perfecte[0])]
        cod, out, _ = _ruleaza(pred)
        self.assertEqual(cod, 1)
        self.assertIn("problema|id duplicat în predicții", out)

    def test_verdict_nepermis_blocheaza(self):
        pred = _intoarce_verdictul(self.perfecte, self.id_eroare, "magic")
        cod, out, _ = _ruleaza(pred)
        self.assertEqual(cod, 1)
        self.assertIn("problema|verdict nepermis", out)
        self.assertNotIn("total|", out)

    def test_verdict_lipsa_blocheaza(self):
        pred = [p for p in self.perfecte if p["id"] != self.id_eroare]
        pred.append({"id": self.id_eroare})
        cod, out, _ = _ruleaza(pred)
        self.assertEqual(cod, 1)
        self.assertIn("problema|verdict nepermis", out)
        self.assertNotIn("total|", out)

    # --- utilizare (exit 2) și formate ---------------------------------

    def test_json_rupt_exit_2(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                         encoding="utf-8") as f:
            f.write('{"predictii": [')
            cale = f.name
        try:
            r = subprocess.run([sys.executable, str(SCRIPT), cale,
                                "--corpus", str(CORPUS)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 2, r.stdout)
            self.assertIn("JSON rupt", r.stderr)
        finally:
            Path(cale).unlink(missing_ok=True)

    def test_fisier_lipsa_exit_2(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "nu-exista-nicdoi.json",
                            "--corpus", str(CORPUS)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)

    def test_format_obiect_predictii_acceptat(self):
        cod, out, _ = _ruleaza({"predictii": self.perfecte})
        self.assertEqual(cod, 0)
        self.assertIn(f"acoperire|{len(self.perfecte)}/{len(self.perfecte)}", out)

    def test_stdin_acceptat(self):
        cod, out, err = _ruleaza(self.perfecte, stdin=True)
        self.assertEqual(cod, 0, err)
        self.assertIn(f"potrivit={len(self.perfecte)}", _linia(out, "total|"))

    def test_json_output_structurat(self):
        pred = _intoarce_verdictul(self.perfecte, self.id_eroare, "pastreaza")
        cod, out, _ = _ruleaza(pred, "--detaliu", "--json")
        self.assertEqual(cod, 0)
        date = json.loads(out)
        self.assertEqual(date["status"], "draft_nevalidat_uman")
        self.assertEqual(date["total"]["ratat"], 1)
        self.assertEqual(date["total"]["potrivit"], len(pred) - 1)
        for split in ("referinta", "holdout"):
            asteptat = sum(1 for c in self.cazuri if c["split"] == split)
            self.assertEqual(sum(date[split].values()), asteptat, split)
        self.assertEqual(date["detaliu"][0]["id"], self.id_eroare)

    # --- onestitatea raportului ----------------------------------------

    def test_raportul_poarta_status_draft_si_notele(self):
        cod, out, _ = _ruleaza(self.perfecte)
        self.assertEqual(cod, 0)
        self.assertIn("status|draft_nevalidat_uman", out)
        self.assertIn("nu benchmark", out)
        self.assertIn("nu rulează modele", out)

    def test_fara_dependente_de_retea_ide_procese(self):
        """Evaluatorul e offline: doar biblioteca standard, fără rețea/procese."""
        sursa = SCRIPT.read_text(encoding="utf-8")
        for modul in ("requests", "urllib", "http.client", "socket", "subprocess",
                      "import os"):
            self.assertNotIn(modul, sursa, modul)


if __name__ == "__main__":
    unittest.main()
