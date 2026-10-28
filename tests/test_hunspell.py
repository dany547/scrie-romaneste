#!/usr/bin/env python3
"""Teste pentru extensia Hunspell (`scripts/_hunspell.py`) și opțiunea `--sugestii`
din `check-cuvinte.py`.

Hunspell nu e necesar: `shutil.which` și `subprocess.run` ale modulului sunt
înlocuite cu un motor fals, care răspunde în formatul `hunspell -a`. Nu se
creează executabile și nu se instalează nimic.

Contract (implementat separat): `EroareHunspell(Exception)` și
`sugereaza(forme, dictionar='ro_RO') -> dict[str, list[str]]`.

Rulează: python3 -m unittest discover -s tests -p test_hunspell.py -v
"""
import gzip
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _hunspell  # noqa: E402  (contractul: modul din scripts/)

BANNER = "Hunspell 1.7.2\n"


class _Motor:
    """Înlocuiește `subprocess.run`: câte o linie de răspuns pentru fiecare formă
    trimisă cu prefixul `^`, fiecare urmată de o linie goală."""

    def __init__(self, raspunsuri=None, banner=BANNER, trunchiat=False,
                 cod=0, stderr=b"", iesire=None, exceptie=None):
        self.raspunsuri = raspunsuri or {}
        self.banner = banner
        self.trunchiat = trunchiat  # elimină ultimul bloc: răspuns trunchiat
        self.cod = cod
        self.stderr = stderr
        self.iesire = iesire        # octeți bruti, când testăm decodarea
        self.exceptie = exceptie
        self.apeluri = []

    def __call__(self, argv, *args, **kwargs):
        self.apeluri.append((argv, kwargs))
        if self.exceptie is not None:
            raise self.exceptie
        if self.iesire is not None:
            return subprocess.CompletedProcess(argv, self.cod, stdout=self.iesire,
                                               stderr=self.stderr)
        intrare = kwargs.get("input", b"")
        if isinstance(intrare, bytes):
            intrare = intrare.decode("utf-8")
        formele = [linia[1:] for linia in intrare.split("\n") if linia.startswith("^")]
        blocuri = [self.raspunsuri.get(forma, "*") for forma in formele]
        if self.trunchiat:
            blocuri = blocuri[:-1]
        corp = self.banner + "".join(bloc + "\n\n" for bloc in blocuri)
        # subprocess.run cu text=True/encoding întoarce str; fără ele, bytes.
        # Testele nu depind de forma pe care o alege implementarea.
        texte = bool(kwargs.get("text") or kwargs.get("universal_newlines")
                     or "encoding" in kwargs)
        return subprocess.CompletedProcess(argv, self.cod,
                                           stdout=corp if texte else corp.encode("utf-8"),
                                           stderr=self.stderr)

    def intrare_trimisa(self):
        """Textul trimis la stdin în ultimul apel, decodat din UTF-8."""
        _, kwargs = self.apeluri[-1]
        intrare = kwargs.get("input", b"")
        return intrare.decode("utf-8") if isinstance(intrare, bytes) else intrare


def _sugereaza(forme, motor, which="/usr/bin/hunspell", dictionar=None):
    with mock.patch.object(_hunspell.shutil, "which", return_value=which), \
            mock.patch.object(_hunspell.subprocess, "run", side_effect=motor):
        if dictionar is None:
            return _hunspell.sugereaza(forme)
        return _hunspell.sugereaza(forme, dictionar=dictionar)


class TestSugereaza(unittest.TestCase):

    def test_gol_nu_porneste_procesul(self):
        motor = _Motor()
        self.assertEqual(_sugereaza([], motor), {})
        self.assertEqual(motor.apeluri, [])

    def test_recunoscut_intoarce_lista_goala(self):
        """`*` (corect), `+` (derivat dintr-o rădăcină), `-` (compus) => []."""
        motor = _Motor({"pereți": "*", "tavanul": "+ tavan", "clientii": "-",
                        "proiectul": "# proiectul 0"})
        rez = _sugereaza(["pereți", "tavanul", "clientii", "proiectul"], motor)
        self.assertEqual(list(rez), ["pereți", "tavanul", "clientii", "proiectul"])
        for forma in rez:
            self.assertEqual(rez[forma], [], forma)

    def test_sugestii_din_linia_ampersand(self):
        motor = _Motor({"pereti": "& pereti 2 0: pereți, perete"})
        self.assertEqual(_sugereaza(["pereti"], motor),
                         {"pereti": ["pereți", "perete"]})

    def test_sugestii_din_linia_semnul_intrebarii(self):
        """`?` are același protocol ca `&`: cuvânt, număr, offset, apoi lista."""
        motor = _Motor({"zorbul": "? zorbul 2 0: zorbi, zorbul"})
        self.assertEqual(_sugereaza(["zorbul"], motor), {"zorbul": ["zorbi", "zorbul"]})

    def test_linia_question_fara_protocol_e_respinsa(self):
        """Forma inventată „? cuvânt, sug1” nu e protocol Hunspell: nu se acceptă."""
        motor = _Motor({"zorbul": "? zorbul, zorbi"})
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["zorbul"], motor)

    def test_diacritice_pastrate_in_cheie_si_in_intrare(self):
        motor = _Motor({"ţară": "& ţară 1 0: țară"})
        rez = _sugereaza(["țară"], motor)
        self.assertEqual(list(rez), ["țară"])
        self.assertIn("^țară\n", motor.intrare_trimisa())

    def test_dedup_in_ordinea_aparitiei(self):
        motor = _Motor({"x": "& x 3 0: a, b, a"})
        rez = _sugereaza(["tavanul", "pereți", "tavanul", "etajul"], motor)
        self.assertEqual(list(rez), ["tavanul", "pereți", "etajul"])

    def test_maxim_cinci_sugestii_fara_duplicate(self):
        motor = _Motor({"x": "& x 8 0: a, b, a, c, d, e, f, g"})
        self.assertEqual(_sugereaza(["x"], motor)["x"], ["a", "b", "c", "d", "e"])

    def test_numarul_din_linie_trebuie_sa_corespunda_listei(self):
        """Count 2 cu un singur element e ieșire trunchiată, nu sugestie validă."""
        motor = _Motor({"x": "& x 2 0: a"})
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["x"], motor)

    def test_ecou_gresit_nu_e_mapat_altui_token(self):
        motor = _Motor({"pereți": "& tavanul 1 0: tavane"})
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["pereți", "tavanul"], motor)

    def test_decodare_text_mode_utf8_invalid(self):
        motor = _Motor(exceptie=UnicodeDecodeError("utf-8", b"\xff", 0, 1,
                                                   "invalid start byte"))
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["pereti"], motor)

    def test_dictionar_invalid_nu_porneste_procesul(self):
        for dictionar in ["", "   ", "ro\x00RO", "ro\nRO", "-ro_RO"]:
            motor = _Motor()
            with self.subTest(dictionar=repr(dictionar)):
                with self.assertRaises(_hunspell.EroareHunspell):
                    _sugereaza(["pereti"], motor, dictionar=dictionar)
                self.assertEqual(motor.apeluri, [])

    def test_forme_goale_sau_cu_spatii_respinse(self):
        for forme in [[""], ["pere ti"], ["pereti\n"], ["pereti\t"]]:
            motor = _Motor()
            with self.subTest(forme=forme):
                with self.assertRaises(_hunspell.EroareHunspell):
                    _sugereaza(forme, motor)
                self.assertEqual(motor.apeluri, [])

    def test_mai_multe_forme_raspuns_in_ordine(self):
        motor = _Motor({"aaaa": "& aaaa 1 0: unu", "bbbb": "*", "cccc": "# cccc 0"})
        rez = _sugereaza(["aaaa", "bbbb", "cccc"], motor)
        self.assertEqual(rez, {"aaaa": ["unu"], "bbbb": [], "cccc": []})

    def test_banner_ispell_acceptat(self):
        motor = _Motor({"pereti": "& pereti 1 0: pereți"},
                       banner="@(#) International Ispell Version 3.3.02\n")
        self.assertEqual(_sugereaza(["pereti"], motor), {"pereti": ["pereți"]})

    def test_argv_lista_fara_shell_si_cale_cu_spatii(self):
        motor = _Motor()
        _sugereaza(["pereti"], motor, which="/cale cu spații/hunspell")
        argv, kwargs = motor.apeluri[0]
        self.assertIsInstance(argv, (list, tuple))
        self.assertEqual(argv[0], "/cale cu spații/hunspell")
        self.assertIs(kwargs.get("shell", False), False)
        self.assertIn("-a", argv)
        self.assertEqual(argv[argv.index("-i") + 1], "UTF-8")

    def test_dictionar_implicit_ro_RO(self):
        motor = _Motor()
        _sugereaza(["pereti"], motor)
        argv, _ = motor.apeluri[0]
        self.assertEqual(argv[argv.index("-d") + 1], "ro_RO")

    def test_dictionar_explicit(self):
        motor = _Motor()
        _sugereaza(["pereti"], motor, dictionar="en_US")
        argv, _ = motor.apeluri[0]
        self.assertEqual(argv[argv.index("-d") + 1], "en_US")

    def test_timeout_explicit_si_locale_utf8(self):
        motor = _Motor()
        _sugereaza(["pereti"], motor)
        _, kwargs = motor.apeluri[0]
        self.assertIsNotNone(kwargs.get("timeout"))
        self.assertGreater(kwargs["timeout"], 0)
        env = kwargs.get("env")
        self.assertIsNotNone(env, "procesul trebuie pornit cu locale UTF-8 explicit")
        self.assertIn("UTF", (env.get("LC_ALL") or env.get("LANG") or "").upper())

    def test_intrare_anti_protocol_respinsa_fara_proces(self):
        for forma in ["pereți\nbanane", "ok\r", "a\x00b"]:
            motor = _Motor()
            with self.subTest(forma=repr(forma)):
                with self.assertRaises(_hunspell.EroareHunspell):
                    _sugereaza([forma], motor)
                self.assertEqual(motor.apeluri, [])


class TestEroriHunspell(unittest.TestCase):

    def test_binar_lipsa(self):
        with mock.patch.object(_hunspell.shutil, "which", return_value=None), \
                mock.patch.object(_hunspell.subprocess, "run") as run:
            with self.assertRaises(_hunspell.EroareHunspell):
                _hunspell.sugereaza(["pereti"])
            run.assert_not_called()

    def test_timeout(self):
        motor = _Motor(exceptie=subprocess.TimeoutExpired(cmd="hunspell", timeout=5))
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["pereti"], motor)

    def test_oserror_la_pornire(self):
        motor = _Motor(exceptie=OSError("permisiune refuzată"))
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["pereti"], motor)

    def test_cod_de_iesire_nenul_dictionar_lipsa(self):
        motor = _Motor(cod=1, stderr=b"Can't open affix or dictionary files")
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["pereti"], motor)

    def test_decodare_invalida(self):
        motor = _Motor(iesire=BANNER.encode("utf-8") + b"\xff\xfe\n\n")
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["pereti"], motor)

    def test_raspuns_trunchiat(self):
        motor = _Motor({"aaaa": "*", "bbbb": "*"}, trunchiat=True)
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["aaaa", "bbbb"], motor)

    def test_raspuns_trunchiat_o_singura_forma(self):
        """Ca trunchiat: o singură formă, fără bloc de răspuns."""
        motor = _Motor({"aaaa": "*"}, trunchiat=True)
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["aaaa"], motor)

    def test_linie_malformata(self):
        motor = _Motor({"aaaa": "asta nu e un răspuns Hunspell"})
        with self.assertRaises(_hunspell.EroareHunspell):
            _sugereaza(["aaaa"], motor)


def _incarca_cli():
    spec = importlib.util.spec_from_file_location("check_cuvinte",
                                                  SCRIPTS / "check-cuvinte.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


CLI = _incarca_cli()

# Forme pliate, ca în lexiconul real. „clurfanizarea” lipsește intenționat.
FORME_CUNOSCUTE = ["echipa", "livrat", "proiectul", "timp", "lansata", "ieri", "fost"]
TEXT_SUSPECT = "Echipa a livrat proiectul la timp.\nClurfanizarea a fost lansată ieri.\n"
SUGESTII = {"clurfanizarea": ["clarificarea", "curfanizarea"]}
PLAFON_12 = ("zorbacul bragnoti frimzel plinxiu gorvanet hurbaci kiplumba mirzonet "
             "nastrofa oblinkar pardulic quarnaz")
ENGLEZA = (
    "system window cursor button settings network browser session module "
    "package version release default backend frontend component service "
    "request response database query server client token cookie header "
    "footer master slider modal toggle filter export import upload reboot "
    "console logger terminal kernel driver socket thread queue buffer stream "
    "parser")


def _stdin(text):
    """stdin ca în producție: `_comun.citeste_intrare` citește `sys.stdin.buffer`."""
    return io.TextIOWrapper(io.BytesIO(text.encode("utf-8")), encoding="utf-8")


def _adaptor(sugestii=None, exceptie=None):
    """Adaptor fals pentru `sugereaza`: răspunde cu chei pliate, ca lista din test."""
    sugestii = SUGESTII if sugestii is None else sugestii

    def sugereaza(forme, dictionar="ro_RO"):
        if exceptie is not None:
            raise exceptie
        return {f: sugestii.get(f.lower(), []) for f in forme}
    return mock.Mock(side_effect=sugereaza)


class TestCLISugestii(unittest.TestCase):
    """`check-cuvinte.py --sugestii`: opt-in, citește lexiconul temporar,
    nu modifică fișierele și nu afișează scor."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.lex = Path(cls.tmp.name) / "lex.txt.gz"
        with gzip.open(cls.lex, "wt", encoding="utf-8") as f:
            f.write("\n".join(FORME_CUNOSCUTE))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def _fisier(self, text):
        cale = Path(self.tmp.name) / "text.md"
        cale.write_text(text, encoding="utf-8")
        return cale

    def _ruleaza(self, argv, text=None, adaptor=None, which="/usr/bin/hunspell",
                 lexicon=True):
        """Rulează `CLI.main` cu adaptorul fals; întoarce (cod, stdout, stderr).

        Lexiconul temporar se pasează cu `--lexicon`; `lexicon=False` lasă
        lexiconul implicit (cu completările din `scripts/lexicon/`)."""
        out, err = io.StringIO(), io.StringIO()
        adaptor = adaptor if adaptor is not None else _adaptor()
        extra = ["--lexicon", str(self.lex)] if lexicon else []
        with mock.patch.object(_hunspell, "sugereaza", adaptor), \
                mock.patch.object(_hunspell.shutil, "which", return_value=which), \
                mock.patch.object(_hunspell.subprocess, "run") as run, \
                mock.patch("sys.stdin", _stdin(text or "")), \
                redirect_stdout(out), redirect_stderr(err):
            self._ultimul_run = run
            cod = CLI.main([*argv, *extra])
        self._adaptor = adaptor
        self.assertNotIn("Traceback", err.getvalue())
        return cod, out.getvalue(), err.getvalue()

    def test_fara_flag_zero_dependenta(self):
        adaptor = _adaptor()
        cod, out, _ = self._ruleaza(["-"], text=TEXT_SUSPECT, adaptor=adaptor)
        self.assertEqual(cod, 1)
        self.assertNotIn("sugestii|", out)
        adaptor.assert_not_called()
        self._ultimul_run.assert_not_called()

    def test_linia_sugestii_dupa_suspect(self):
        cod, out, _ = self._ruleaza(["-", "--sugestii"], text=TEXT_SUSPECT)
        self.assertEqual(cod, 1)
        linii = out.splitlines()
        i = next(n for n, l in enumerate(linii) if "|Clurfanizarea|" in l)
        self.assertTrue(linii[i].startswith("important|cuvant_de_verificat|L2|"))
        self.assertEqual(linii[i + 1],
                         "sugestii|L2|Clurfanizarea|clarificarea / curfanizarea")

    def test_fara_sugestii_gol(self):
        cod, out, _ = self._ruleaza(["-", "--sugestii"], text=TEXT_SUSPECT,
                                    adaptor=_adaptor(sugestii={}))
        self.assertIn("sugestii|L2|Clurfanizarea|fără sugestii", out.splitlines())

    def test_dictionar_default_si_valoare_explicita(self):
        _, _, _ = self._ruleaza(["-", "--sugestii"], text=TEXT_SUSPECT)
        args, kwargs = self._adaptor.call_args
        dictionar = kwargs.get("dictionar", args[1] if len(args) > 1 else None)
        self.assertEqual(dictionar, "ro_RO")
        _, _, _ = self._ruleaza(["-", "--sugestii", "--dictionar", "en_US"],
                                text=TEXT_SUSPECT)
        args, kwargs = self._adaptor.call_args
        dictionar = kwargs.get("dictionar", args[1] if len(args) > 1 else None)
        self.assertEqual(dictionar, "en_US")

    def test_dictionar_fara_sugestii_exit_2(self):
        adaptor = _adaptor()
        cod, _, _ = self._ruleaza(["-", "--dictionar", "ro_RO"], text=TEXT_SUSPECT,
                                  adaptor=adaptor)
        self.assertEqual(cod, 2)
        adaptor.assert_not_called()

    def test_dictionar_fara_valoare_exit_2(self):
        cod, _, _ = self._ruleaza(["-", "--sugestii", "--dictionar"], text=TEXT_SUSPECT)
        self.assertEqual(cod, 2)

    def test_dictionar_gol_sau_spatii_exit_2_fara_motor(self):
        """Valoare explicită goală sau doar spații: nu cade pe ro_RO, nu citește, nu pornește."""
        for valoare in ["", "   "]:
            adaptor = _adaptor()
            with self.subTest(dictionar=repr(valoare)):
                cod, out, _ = self._ruleaza(["-", "--sugestii", "--dictionar", valoare],
                                            text=TEXT_SUSPECT, adaptor=adaptor)
                self.assertEqual(cod, 2)
                self.assertEqual(out, "")
                adaptor.assert_not_called()
                self._ultimul_run.assert_not_called()

    def test_plafon_zece_forme_interogate(self):
        cod, out, _ = self._ruleaza(["-", "--sugestii"], text=PLAFON_12 + "\n",
                                    adaptor=_adaptor(sugestii={}))
        self.assertEqual(cod, 1)
        self.assertEqual(out.count("sugestii|"), 10)
        self.assertIn("mai_sunt|2 forme neafișate", out)
        forme_trimise = self._adaptor.call_args[0][0]
        self.assertEqual(len(forme_trimise), 10)

    def test_tot_interogheaza_toate_formele(self):
        cod, out, _ = self._ruleaza(["-", "--sugestii", "--tot"], text=PLAFON_12 + "\n",
                                    adaptor=_adaptor(sugestii={}))
        self.assertEqual(out.count("sugestii|"), 12)

    def test_cuvant_din_allow_nu_se_interogheaza(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write("clurfanizarea\n")
        adaptor = _adaptor()
        cod, out, _ = self._ruleaza(["-", "--sugestii", "--allow", f.name],
                                    text=TEXT_SUSPECT, adaptor=adaptor)
        Path(f.name).unlink()
        self.assertEqual(cod, 0)
        self.assertNotIn("sugestii|", out)
        adaptor.assert_not_called()

    def test_text_neromanesc_nu_porneste_motorul(self):
        adaptor = _adaptor()
        cod, out, _ = self._ruleaza(["-", "--sugestii"], text=ENGLEZA + "\n",
                                    adaptor=adaptor)
        self.assertIn("info|cuvinte|text predominant neromânesc", out)
        self.assertNotIn("sugestii|", out)
        adaptor.assert_not_called()

    def test_fara_suspecti_nu_porneste_motorul(self):
        adaptor = _adaptor()
        cod, out, _ = self._ruleaza(["-", "--sugestii"],
                                    text="Echipa a livrat proiectul la timp.\n",
                                    adaptor=adaptor)
        self.assertEqual(cod, 0)
        adaptor.assert_not_called()
        self._ultimul_run.assert_not_called()

    def test_motor_indisponibil_exit_2_fara_succes_partial(self):
        adaptor = _adaptor(exceptie=_hunspell.EroareHunspell("binarul lipsește"))
        cod, out, err = self._ruleaza(["-", "--sugestii"], text=TEXT_SUSPECT,
                                      adaptor=adaptor)
        self.assertEqual(cod, 2)
        self.assertIn("eroare", err)
        self.assertEqual(out, "", "nicio linie de raport la eroarea motorului")

    def test_binar_lipsa_real_exit_2(self):
        """Fără mock pe `sugereaza`: `which` întoarce None, deci motorul e indisponibil."""
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(_hunspell.shutil, "which", return_value=None), \
                mock.patch.object(_hunspell.subprocess, "run") as run, \
                mock.patch("sys.stdin", _stdin(TEXT_SUSPECT)), \
                redirect_stdout(out), redirect_stderr(err):
            cod = CLI.main(["-", "--sugestii", "--lexicon", str(self.lex)])
        self.assertEqual(cod, 2)
        self.assertNotIn("Traceback", err.getvalue())
        self.assertEqual(out.getvalue(), "", "nicio linie de raport la eroarea motorului")
        run.assert_not_called()

    def test_completarile_implicite_nu_cheama_motorul(self):
        """`dronele` e în completari (lexicon implicit): nu devine suspect și nu ajunge
        la hunspell."""
        adaptor = _adaptor()
        cod, out, _ = self._ruleaza(["-", "--sugestii"],
                                    text="Am văzut dronele pe cer.\n",
                                    adaptor=adaptor, lexicon=False)
        self.assertNotIn("|dronele|", out.lower())
        for apel in adaptor.call_args_list:
            forme = apel[0][0] if apel[0] else apel[1]["forme"]
            self.assertNotIn("dronele", [f.lower() for f in forme])

    def test_nota_nu_cere_corectie_din_absenta(self):
        """Absența din lexicon nu e verdict; nota nu mai spune să corectezi doar la
        „nu este în dicționar”, ci să verifici forma, lema și sensul."""
        cod, out, _ = self._ruleaza(["-"], text=TEXT_SUSPECT)
        nota = [l for l in out.splitlines() if l.startswith("nota:")]
        self.assertEqual(len(nota), 1)
        self.assertIn("nu e verdict", nota[0])
        self.assertIn("sensul", nota[0])
        self.assertNotIn("corectează doar", nota[0])
        self.assertNotIn("nu este în dicționar", nota[0])

    def test_nu_modifica_fisierul_si_nu_da_scor(self):
        fisier = self._fisier(TEXT_SUSPECT)
        original = fisier.read_bytes()
        cod, out, _ = self._ruleaza([str(fisier), "--sugestii"])
        self.assertEqual(fisier.read_bytes(), original)
        self.assertNotIn("/13", out)
        self.assertNotIn("scor", out.lower())


if __name__ == "__main__":
    unittest.main()
