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

    def test_lista_scurta_normala_nu_e_semnalata(self):
        """O lista de 3 puncte intr-un articol scurt e continut SEO normal,
        nu abuz — nu trebuie semnalata doar pentru ca atinge 50% din linii."""
        text = ("Cafeaua de specialitate a devenit populara in ultimii ani. "
                "Diferenta vine din boabele selectate manual.\n\n"
                "Cateva criterii merita atentie:\n\n"
                "- originea boabelor\n- data prajirii\n- metoda de preparare\n\n"
                "Pretul variaza intre 35 si 60 de lei. Cafeaua proaspat prajita "
                "pastreaza arome pe care cea de supermarket le pierde.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("simboluri_excesive", iesire,
                         f"lista scurta normala semnalata gresit:\n{iesire}")
        self.assertEqual(cod, 0)

    def test_proza_transformata_in_liste_e_semnalata(self):
        """Cand majoritatea unui text de lungime normala devine fragmente
        marcate cu '-', semnalul de proportie trebuie sa se declanseze."""
        linii = "\n".join(
            f"- Beneficiul numarul {i} explicat pe scurt in cateva cuvinte"
            for i in range(1, 10))
        text = "Introducere scurta despre produs.\n\n" + linii + "\n\nInchidere scurta."
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertIn("simboluri_excesive", iesire)
        self.assertIn("proportie", iesire)
        self.assertEqual(cod, 1)


class TestTextWrapped(unittest.TestCase):
    """Regresie: tiparele de mai multe cuvinte se rupeau la capat de rand.

    Textul real e wrapped. Inainte de fix, „in era digitala" era prins, iar
    „in era\\ndigitala" trecea complet — acelasi text, semnale diferite in
    functie de unde a cazut intamplator taietura de rand.
    """

    def test_acelasi_text_da_acelasi_rezultat_wrapped(self):
        pe_o_linie = ("Traim in era digitala. Este important de mentionat ca "
                      "oferim o gama larga de solutii. Asta face sens pentru noi.")
        wrapped = ("Traim in era\ndigitala. Este important de\nmentionat ca "
                   "oferim o gama\nlarga de solutii. Asta face\nsens pentru noi.")
        _, iesire_linie = ruleaza_stdin("check-tipare.py", pe_o_linie)
        _, iesire_wrap = ruleaza_stdin("check-tipare.py", wrapped)
        categorii = lambda s: sorted(l.split("|")[1] for l in s.splitlines()
                                     if "|L" in l)
        self.assertEqual(categorii(iesire_linie), categorii(iesire_wrap),
                         f"wrapping-ul schimba rezultatul:\n{iesire_wrap}")
        self.assertIn("introduceri", categorii(iesire_wrap))

    def test_nu_trece_peste_granita_de_paragraf(self):
        """O sintagma nu se intinde peste un rand gol — ar fi doua paragrafe."""
        cod, iesire = ruleaza_stdin("check-tipare.py",
                                    "Traim in era\n\ndigitala si e bine asa.")
        self.assertEqual(cod, 0, f"potrivire peste granita de paragraf:\n{iesire}")

    def test_liniuta_paranteza_nu_inghite_un_heading(self):
        """Fereastra dintre doua linii de pauza se opreste la capat de paragraf,
        altfel prinde ultimul cuvant al unui paragraf si primul din urmatorul."""
        text = ("Prima idee se incheie aici — cu o precizare scurta.\n\n"
                "## Alt subiect\n\n"
                "Al doilea paragraf incepe — si continua normal mai departe.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("punctuatie_carja", iesire,
                         f"potrivire peste granita de paragraf:\n{iesire}")

    def test_pleonasmul_wrapped_e_prins(self):
        cod, iesire = ruleaza_stdin("check-modelisme.py",
                                    "A avut o hemoragie\nde sange severa.")
        self.assertEqual(cod, 1, f"pleonasm ratat peste capat de rand:\n{iesire}")

    def test_lista_cu_liniuta_la_inceput_de_rand_nu_e_confundata(self):
        """Spatiile din interiorul claselor raman neatinse: `[ \\t]-[ \\t]` nu
        trebuie sa prinda marcatorii de lista de la inceput de rand."""
        text = ("Produsul are trei calitati clare care conteaza la munte.\n"
                "- greutate mica\n- rezistenta la apa\n- pret bun\n"
                "Restul sunt detalii de catalog fara importanta reala.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("simboluri_excesive", iesire,
                         f"marcatori de lista confundati cu liniuta-paranteza:\n{iesire}")
        self.assertNotIn("punctuatie_carja", iesire,
                         f"marcatori de lista confundati cu liniuta-conector:\n{iesire}")


class TestPunctuatieCarja(unittest.TestCase):
    """Liniuta ca singur conector de fraza — tic de model, nu semn de punctuatie.

    Detectorul cere litera inainte de spatiu, deci dialogul, marcatorul de lista
    si intervalul numeric sunt excluse prin constructie, nu prin lista de
    exceptii. Pragul e propriu tiparului (4.0/1000), pentru ca liniutele cu
    spatii sunt mult mai rare decat cuvintele.
    """

    def test_liniuta_conector_repetata_e_semnalata(self):
        cod, iesire = ruleaza("check-tipare.py", str(FIXTURES / "rau-liniuta.md"))
        self.assertEqual(cod, 1, f"ticul liniutei nu a fost prins:\n{iesire}")
        self.assertIn("punctuatie_carja", iesire)
        self.assertIn("prag_depasit|punctuatie_carja", iesire)

    def test_em_dash_si_cratima_sunt_prinse_pe_frecventa(self):
        """Amandoua au intrebuintari legitime, deci se judeca pe prag. En-dash-ul
        e scos separat, prin regula absoluta — vezi TestLiniutaEngleza."""
        for liniuta in ("—", "-"):
            text = (f"Solutia noastra e buna {liniuta} foarte buna, de fapt.\n"
                    f"Clientii vin des {liniuta} pentru ca au incredere.\n"
                    f"Rezultatele se vad rapid {liniuta} in prima luna deja.")
            cod, iesire = ruleaza_stdin("check-tipare.py", text)
            self.assertIn("punctuatie_carja", iesire,
                          f"liniuta {liniuta!r} ratata:\n{iesire}")

    def test_dialogul_literar_nu_e_semnalat(self):
        """Blocant: `—` la inceput de replica e obligatoriu in proza romaneasca."""
        cod, iesire = ruleaza("check-tipare.py", str(FIXTURES / "legit-literar.md"))
        self.assertNotIn("punctuatie_carja", iesire,
                         f"dialog literar confundat cu tic de model:\n{iesire}")

    def test_replicile_dese_nu_declanseaza_pragul(self):
        text = ("Au tacut amandoi o vreme, pana a pornit trenul.\n\n"
                "— Iar intarzie, a zis femeia.\n\n"
                "— Iar, a zis barbatul.\n\n"
                "— Ca intotdeauna, a zis copilul de langa ei.\n\n"
                "— Asa e in fiecare dimineata, a zis femeia din nou.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("punctuatie_carja", iesire,
                         f"replici de dialog numarate ca tipar:\n{iesire}")

    def test_intervalul_numeric_nu_e_semnalat(self):
        text = ("Preturile pornesc de la 4.000 - 7.000 lei pentru montaj.\n"
                "Termenul de livrare e 10 - 12 zile lucratoare in toata tara.\n"
                "Garantia tine 24 - 36 de luni, in functie de model si de firma.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("punctuatie_carja", iesire,
                         f"interval numeric confundat cu liniuta-conector:\n{iesire}")

    def test_liniuta_la_capat_de_rand_e_prinsa(self):
        """Textul real e wrapped — semnalul nu are voie sa depinda de unde a
        cazut taierea de rand (vezi TestTextWrapped)."""
        text = ("Solutia noastra e buna —\nfoarte buna, de fapt, spun clientii.\n"
                "Rezultatele se vad rapid —\nin prima luna deja se simte.\n"
                "Echipa lucreaza bine —\nfara sedinte lungi si fara rapoarte.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertIn("punctuatie_carja", iesire,
                      f"liniuta rupta la capat de rand ratata:\n{iesire}")

    def test_doua_liniute_intr_un_text_bun_raman_tacute(self):
        """Calibrare: `pereche-dupa.md` e rescrierea-model a repo-ului si
        foloseste doua linii de pauza la 293 de cuvinte. Daca pragul o
        semnaleaza, pragul e gresit, nu textul."""
        cod, iesire = ruleaza("check-tipare.py", str(FIXTURES / "pereche-dupa.md"))
        self.assertNotIn("punctuatie_carja", iesire,
                         f"rescrierea-model semnalata pentru doua linii de pauza:\n{iesire}")

    def test_nu_intra_in_scorul_automat(self):
        """Semnal de recitire, nu penalizare — `/13` ramane neschimbat."""
        cod, iesire = ruleaza("check-tipare.py", str(FIXTURES / "rau-liniuta.md"),
                              "--scor")
        self.assertIn("scor_automat=0/6", iesire, iesire)


class TestLiniutaEngleza(unittest.TestCase):
    """En-dash-ul „–" nu are rol in norma romaneasca: compusele si intervalele
    cer cratima, incizele cer linie de pauza. Singura regula absoluta din zona
    de punctuatie — restul liniutelor se judeca pe frecventa."""

    def test_o_singura_aparitie_e_semnalata(self):
        cod, iesire = ruleaza_stdin("check-tipare.py", "Solutia e buna – foarte buna.")
        self.assertEqual(cod, 1, f"en-dash ratat:\n{iesire}")
        self.assertIn("liniuta_engleza", iesire)

    def test_intervalul_cu_en_dash_e_semnalat(self):
        """Tocmai intervalul e calea pe care intra: conventie engleza, nu RO."""
        cod, iesire = ruleaza_stdin("check-tipare.py",
                                    "Programul tine 10–12 zile lucratoare.")
        self.assertIn("liniuta_engleza", iesire, iesire)

    def test_em_dash_si_cratima_nu_sunt_prinse_de_regula_absoluta(self):
        """Doar en-dash-ul e interzis mereu; celelalte au prag."""
        cod, iesire = ruleaza_stdin("check-tipare.py",
                                    "Solutia e buna — foarte buna, spun clientii.")
        self.assertNotIn("liniuta_engleza", iesire, iesire)

    def test_nu_intra_in_scorul_automat(self):
        cod, iesire = ruleaza_stdin_cu_flags(
            "check-tipare.py", "Solutia e buna – foarte buna.", "--scor")
        self.assertIn("scor_automat=0/6", iesire, iesire)


class TestSimboluriOrnamentale(unittest.TestCase):
    """Bullet-ul Unicode si simbolurile de referinta („§", „¶", „†") sunt
    artefacte de fereastra de chat, nu punctuatie romaneasca."""

    def test_bullet_unicode_e_semnalat(self):
        text = ("Produsul are trei calitati clare care conteaza la munte.\n"
                "• greutate mica\n• rezistenta la apa\n• pret bun\n"
                "Restul sunt detalii de catalog fara importanta reala.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertIn("simboluri_excesive", iesire, iesire)
        self.assertIn("marcator Markdown", iesire, iesire)

    def test_lista_markdown_normala_nu_e_semnalata(self):
        text = ("Produsul are trei calitati clare care conteaza la munte.\n"
                "- greutate mica\n- rezistenta la apa\n- pret bun\n"
                "Restul sunt detalii de catalog fara importanta reala.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("marcator Markdown", iesire, iesire)

    def test_simbolurile_de_referinta_dese_sunt_semnalate(self):
        text = ("Vezi § 5 si § 7 din regulament, plus § 12 pentru detalii.\n"
                "Nota † explica termenul, iar ¶ 3 il reia mai jos in text.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertIn("simboluri_excesive", iesire, iesire)

    def test_o_citare_izolata_nu_e_semnalata(self):
        """Doua trimiteri sunt citare, nu ornament — regula «1-2 nu sunt tipar»."""
        text = ("Norma germana e stricta: § 5 BGB cere forma scrisa, iar § 126\n"
                "detaliaza semnatura. In dreptul romanesc, echivalentul e\n"
                "articolul 1179 din Codul civil, care cere aceleasi conditii.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("simboluri_excesive", iesire, iesire)

    def test_semnele_matematice_nu_sunt_semnalate(self):
        """«×», «°» si «±» sunt notatie normala, nu ornament."""
        text = ("Camera are 3 × 4 metri, adica 12 metri patrati utili.\n"
                "Temperatura urca la 21 °C, cu o abatere de ± 2 grade.\n"
                "Suprafata totala e de 3 × 4 metri in fiecare dintre camere.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("simboluri_excesive", iesire, iesire)

    def test_proza_in_bulleturi_unicode_intra_in_proportie(self):
        """Detectorul de proportie numara si marcatorii Unicode — altfel un text
        integral bullet-uit cu «•» trecea pe langa el."""
        linii = [f"• ideea numarul {i} lamurita in cateva cuvinte simple"
                 for i in range(12)]
        cod, iesire = ruleaza_stdin("check-tipare.py", "\n".join(linii))
        self.assertIn("proportie", iesire, iesire)

    def test_genurile_legitime_raman_curate(self):
        for fixture in ("legit-juridic.md", "legit-academic.md", "legit-literar.md"):
            cod, iesire = ruleaza("check-tipare.py", str(FIXTURES / fixture))
            self.assertNotIn("liniuta_engleza", iesire, f"{fixture}: {iesire}")
            self.assertNotIn("simboluri_excesive", iesire, f"{fixture}: {iesire}")


class TestRegistruNominal(unittest.TestCase):
    """Categoriile numarate pe familie: `copula_evitata`, `referinta_vaga`."""

    def test_registrul_nominal_e_semnalat(self):
        cod, iesire = ruleaza("check-tipare.py", str(FIXTURES / "pereche-inainte.md"))
        self.assertIn("copula_evitata", iesire,
                      f"registrul nominal a trecut nedetectat:\n{iesire}")
        self.assertEqual(cod, 1)

    def test_doua_aparitii_nu_sunt_un_tipar(self):
        """Doua verbe nominale intr-un text lung raman uz normal."""
        text = ("Centrala reprezinta o solutie buna pentru case mici. "
                "Pompa de caldura constituie alternativa scumpa. "
                + "Am montat-o intr-o zi si merge bine de atunci. " * 40)
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("copula_evitata", iesire,
                         f"uz normal semnalat ca tipar:\n{iesire}")

    def test_formula_juridica_izolata_nu_e_semnalata(self):
        text = ("Fapta constituie infractiune si se pedepseste cu inchisoare. "
                + "Instanta a stabilit termenul de judecata pentru luna viitoare. " * 30)
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("copula_evitata", iesire,
                         f"formula juridica fixa semnalata:\n{iesire}")

    def test_referinta_vaga_repetata_e_semnalata(self):
        text = ("Acest lucru schimba totul pentru echipa noastra. "
                "Acest aspect ne-a costat trei luni de munca. "
                "Aceasta solutie a fost aleasa dupa multe discutii. "
                "Acest lucru ramane valabil si acum, dupa doi ani.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertIn("referinta_vaga", iesire)

    def test_familiile_nu_intra_in_scor(self):
        """Sunt semnale de recitire, nu erori — nu umfla scorul automat."""
        cod, iesire = ruleaza_stdin_cu_flags(
            "check-tipare.py", (FIXTURES / "pereche-inainte.md").read_text(), "--scor")
        self.assertNotIn("copula_evitata", iesire)
        self.assertNotIn("referinta_vaga", iesire)

    def test_simetria_de_acoperire_e_semnalata(self):
        text = ("Fie ca esti incepator sau ai deja experienta, ghidul te ajuta. "
                "Indiferent de bugetul disponibil, exista o varianta buna. "
                "Solutia e potrivita pentru oricine, la orice scara.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertIn("simetrie_de_acoperire", iesire)

    def test_fie_ca_corelativ_nu_e_semnalat(self):
        """«Fie ca… fie ca» e conjunctie corelativa normala. Fara adresare la
        persoana a II-a nu e formula de acoperire."""
        text = ("Fie ca ploua, fie ca ninge, drumul ramane deschis. "
                "Fie ca vine iarna devreme, fie ca intarzie, pregatim utilajele. "
                "Fie ca ne convine, fie ca nu, termenul e in martie.")
        cod, iesire = ruleaza_stdin("check-tipare.py", text)
        self.assertNotIn("simetrie_de_acoperire", iesire,
                         f"conjunctie corelativa normala semnalata:\n{iesire}")

    def test_textele_curate_raman_curate(self):
        for fixture in ("bun-articol.md", "pereche-dupa.md"):
            cod, iesire = ruleaza("check-tipare.py", str(FIXTURES / fixture))
            for categorie in ("copula_evitata", "referinta_vaga",
                              "simetrie_de_acoperire"):
                self.assertNotIn(categorie, iesire, f"{fixture}:\n{iesire}")


class TestFormeNonnormative(unittest.TestCase):
    """Forme contrazise explicit de norma academica si acorduri de numerale
    frecvent gresite de modelele putin antrenate pe romana."""

    def test_formele_nonnormative_sunt_prinse(self):
        for text, sugestie in (
                ("Vroiam să vin, dar am rămas.", "voiam"),
                ("El precede pe ceilalți.", "precedă"),
                ("Mi-ar place o cafea.", "plăcea"),
                ("Se merită efortul.", "merită"),
                ("Perioada de dinainte de război.", "dinainte"),
                ("Nici un răspuns nu a venit.", "niciun")):
            cod, iesire = ruleaza_stdin("check-tipare.py", text)
            self.assertEqual(cod, 1, f"{text!r} nu a fost semnalat")
            self.assertIn("forme_nonnormative", iesire)
            self.assertIn(f"→ {sugestie}", iesire)

    def test_formele_corecte_raman_tacute(self):
        cod, iesire = ruleaza_stdin(
            "check-tipare.py",
            "Voiam să vin. El precedă pe ceilalți. Mi-ar plăcea o cafea. "
            "Merită efortul. Dinaintea războiului. Niciun răspuns.")
        self.assertEqual(cod, 0, f"forme corecte semnalate:\n{iesire}")

    def test_acordul_cu_substantivul_numar(self):
        cod, iesire = ruleaza_stdin(
            "check-tipare.py", "Am primit acești milioane de lei.")
        self.assertEqual(cod, 1)
        self.assertIn("acord_numerale", iesire)
        cod, _ = ruleaza_stdin(
            "check-tipare.py", "Am primit aceste milioane de lei.")
        self.assertEqual(cod, 0)

    def test_numarul_fara_de_in_cifre(self):
        cod, iesire = ruleaza_stdin("check-tipare.py", "Am vizitat 200 muzee.")
        self.assertEqual(cod, 1)
        self.assertIn("numeral_fara_de", iesire)

    def test_numerele_legitime_raman_tacute(self):
        for text in ("Am 20 de ani.", "Pe 30 iunie am plecat.",
                     "În 1990 românii au votat.", "Am 5 lei.",
                     "Redus cu 20% din preț.", "Ai 19 șanse."):
            cod, iesire = ruleaza_stdin("check-tipare.py", text)
            self.assertEqual(cod, 0, f"{text!r} semnalat greșit:\n{iesire}")


class TestPleonasmLexical(unittest.TestCase):
    """Perechi de conectori/adverbe cu sens identic și pleonasmele limbajului
    comercial — eroare de registru neutru, pe orice tip de text."""

    def test_perechile_duble_sunt_prinse(self):
        for text, sugestie in (
                ("Nu vrea, dar însă acceptă.", "«dar» sau «însă»"),
                ("Nu am decât numai bine de spus.", "«decât» sau «numai»"),
                ("Preferă mai bine varianta scurtă.", "preferă"),
                ("Va menține în continuare contactul.", "menține"),
                ("S-a întors înapoi acasă.", "fără «înapoi»"),
                ("O nouă inovație ne așteaptă.", "o inovație / o noutate"),
                ("Primești un cadou gratuit.", "cadou")):
            cod, iesire = ruleaza_stdin("check-modelisme.py", text)
            self.assertEqual(cod, 1, f"{text!r} neprins")
            self.assertIn("pleonasm_lexical", iesire)
            self.assertIn(f"→ {sugestie}", iesire)

    def test_formele_corecte_raman_tacute(self):
        cod, iesire = ruleaza_stdin(
            "check-modelisme.py",
            "Nu vrea, dar acceptă. Nu am decât bine de spus. Preferă varianta "
            "scurtă. Va menține contactul. S-a întors acasă. O inovație ne "
            "așteaptă. Primești un cadou.")
        self.assertEqual(cod, 0, f"text curat semnalat:\n{iesire}")

    def test_mai_inca_e_recitire_minor(self):
        """La 3+ aparitii semnalul iese, dar ca `minor` — nu blochează scorul,
        doar atenționează; «încă mai» colocvial e acceptabil, deci recitire."""
        cod, iesire = ruleaza_stdin(
            "check-modelisme.py",
            "Dovezile mai erau încă vii. Au mai rămas încă trei zile. "
            "Mai stai încă puțin.")
        self.assertIn("minor|accentuare_redundanta", iesire)


class TestReclame(unittest.TestCase):
    """Scriptul de anunțuri: limite, politici, semnăturile afirmărilor goale.
    Fără etichete → tăcere (genurile existente nu sunt atinse)."""

    def test_fara_etichete_ramane_mut(self):
        cod, iesire = ruleaza_stdin("check-reclame.py", "Un articol obișnuit.")
        self.assertEqual(cod, 0)
        self.assertIn("0 elemente de reclama", iesire)

    def test_pseudologie_temporala(self):
        cod, iesire = ruleaza_stdin(
            "check-reclame.py",
            "H1: Seara cureți tenul, dimineața îl simți moale")
        self.assertEqual(cod, 1)
        self.assertIn("pseudologie_temporala", iesire)

    def test_pseudologia_cu_conector_cauzal_tacere(self):
        cod, iesire = ruleaza_stdin_cu_flags(
            "check-reclame.py",
            "Text: Aplică seara, pentru că noaptea pielea se regenerează",
            "--platform", "meta")
        self.assertEqual(cod, 0, f"cauzală legitimă semnalată:\n{iesire}")

    def test_tautologia_beneficiu_si_contra_cazurile(self):
        cod, iesire = ruleaza_stdin(
            "check-reclame.py", "H1: Te pieptănești, părul e neted")
        self.assertEqual(cod, 1)
        self.assertIn("tautologie_beneficiu", iesire)
        # produs prezent / fără acțiune / agent explicit → tăcere
        for text in ("Text: Aplică masca seara, părul e mătăsos",
                     "Text: Piele moale 24h",
                     "Text: Șamponul netezește părul uscat"):
            cod, iesire = ruleaza_stdin_cu_flags(
                "check-reclame.py", text, "--platform", "meta")
            self.assertEqual(cod, 0, f"{text!r} semnalat greșit:\n{iesire}")

    def test_limitele_google_hard(self):
        cod, iesire = ruleaza_stdin(
            "check-reclame.py", "H1: " + "x" * 31 + "\nD1: " + "y" * 91)
        self.assertEqual(cod, 1)
        self.assertEqual(iesire.count("limita_caractere"), 2)

    def test_limitele_la_limita_trec(self):
        cod, iesire = ruleaza_stdin(
            "check-reclame.py",
            "H1: a" + "x" * 29 + "\nH2: b" + "x" * 29 + "\nH3: c" + "x" * 29
            + "\nD1: a" + "y" * 89 + "\nD2: b" + "y" * 89)
        self.assertEqual(cod, 0, f"limite legitime semnalate:\n{iesire}")

    def test_politica_exclamarii_google(self):
        cod, iesire = ruleaza_stdin(
            "check-reclame.py", "H1: Vinzi mai mult!\nD1: Oferă! Două! Trei!")
        self.assertEqual(cod, 1)
        self.assertIn("politica_google", iesire)

    def test_caps_emoji_duplicat(self):
        text = "H1: CREMĂ NATURALĂ\nH1: Cremă naturală\nD1: Creme cu 😍 acum"
        cod, iesire = ruleaza_stdin("check-reclame.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("caps_nepotrivit", iesire)
        self.assertIn("emoji_in_anunt", iesire)
        self.assertIn("duplicat", iesire)

    def test_structura_rsa(self):
        cod, iesire = ruleaza_stdin(
            "check-reclame.py", "H1: Abcd\nH2: Efgh\nD1: Ijklmnop")
        self.assertEqual(cod, 1)
        self.assertIn("structura_rsa", iesire)

    def test_limitele_recomandate_meta(self):
        cod, iesire = ruleaza_stdin(
            "check-reclame.py", "Titlu: " + "x" * 41 + "\nText: " + "y" * 126)
        self.assertEqual(cod, 1)
        self.assertIn("titlu_peste_recomandat", iesire)
        self.assertIn("text_peste_recomandat", iesire)
        self.assertNotIn("limita_caractere", iesire)

    def test_superlativ_si_calc(self):
        cod, iesire = ruleaza_stdin(
            "check-reclame.py",
            "H1: Cea mai bună cremă\nD1: Trezește-te cu pielea frumoasă")
        self.assertEqual(cod, 1)
        self.assertIn("superlativ_nefundamentat", iesire)
        self.assertIn("calc_reclama", iesire)

    def test_platforma_din_heading_si_flag(self):
        cod, iesire = ruleaza_stdin_cu_flags(
            "check-reclame.py", "Titlu: " + "x" * 41, "--platform", "google")
        self.assertEqual(cod, 0, "fără heading, Titlu e meta; forțat google, "
                                 "limita de 30 nu se aplică titlului meta")

    def test_flag_brand(self):
        def ruleaza_cu_brand(text, brand):
            return ruleaza_stdin_cu_flags(
                "check-reclame.py",
                "Text: " + text, "--platform", "meta", "--brand", brand)
        cod, iesire = ruleaza_cu_brand("Creme naturale", "Verdea")
        self.assertEqual(cod, 1)
        self.assertIn("text_fara_brand", iesire)
        cod, iesire = ruleaza_cu_brand("Creme Verdea", "Verdea")
        self.assertEqual(cod, 0)

    def test_fixtureurile_de_reclama(self):
        cod, _ = ruleaza("check-reclame.py",
                         str(FIXTURES / "reclame-google-rau.md"))
        self.assertEqual(cod, 1)
        cod, _ = ruleaza("check-reclame.py",
                         str(FIXTURES / "reclame-google-bun.md"))
        self.assertEqual(cod, 0, "anunțul google curat a fost semnalat")
        cod, iesire = ruleaza("check-reclame.py",
                              str(FIXTURES / "reclame-meta-rau.md"))
        self.assertEqual(cod, 1)
        self.assertIn("tautologie_beneficiu", iesire)
        cod, _ = ruleaza("check-reclame.py",
                         str(FIXTURES / "reclame-meta-bun.md"))
        self.assertEqual(cod, 0, "anunțul meta curat a fost semnalat")

    def test_integrare_verifica(self):
        cod, iesire = ruleaza_stdin_cu_flags(
            "verifica.py", "H1: Seara cureți tenul, dimineața îl simți moale",
            "--reclame")
        self.assertEqual(cod, 1)
        self.assertIn("== reclame", iesire)
        self.assertIn("pseudologie_temporala", iesire)
        # fără flag, același text: tăcere totală pe stratul de reclame
        cod, iesire = ruleaza_stdin_cu_flags(
            "verifica.py", "H1: Seara cureți tenul, dimineața îl simți moale")
        self.assertEqual(cod, 0)
        self.assertNotIn("pseudologie", iesire)


class TestRitm(unittest.TestCase):

    def test_text_uniform_e_semnalat(self):
        cod, iesire = ruleaza("check-ritm.py", str(FIXTURES / "pereche-inainte.md"))
        self.assertEqual(cod, 1)
        self.assertIn("ritm_uniform", iesire)
        self.assertIn("fraze_egale", iesire)

    def test_text_variat_nu_e_semnalat(self):
        cod, iesire = ruleaza("check-ritm.py", str(FIXTURES / "bun-articol.md"))
        self.assertEqual(cod, 0, f"proza umana semnalata gresit:\n{iesire}")

    def test_rescrierea_iese_din_zona_uniforma(self):
        """Perechea inainte/dupa: rescrierea trebuie sa scoata textul din zona
        semnalata, nu sa atinga un multiplu de CV. Un prag de tip «CV-ul se
        dubleaza» ar premia taierea frazelor la intamplare — exact ce nu vrem."""
        def cv(fisier):
            _, iesire = ruleaza("check-ritm.py", str(FIXTURES / fisier))
            linie = next(l for l in iesire.splitlines() if l.startswith("metrici|fraze"))
            return float(linie.split("cv=")[1].split("|")[0])
        self.assertLess(cv("pereche-inainte.md"), 0.16, "fixture-ul inainte nu mai e uniform")
        self.assertGreater(cv("pereche-dupa.md"), 0.22,
                           "rescrierea a ramas in zona nedecisa")

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

    def test_paronimia_e_informativa_nu_eroare(self):
        """Ambele cuvinte sunt folosite corect aici. Scriptul vede coaparitia,
        nu sensul, deci raporteaza `minor` si nu blocheaza livrarea (exit 0)."""
        cod, iesire = ruleaza_stdin("check-modelisme.py",
                                    "Un savant eminent a anuntat un pericol iminent.")
        self.assertEqual(cod, 0, f"paronimia corecta a blocat livrarea:\n{iesire}")
        self.assertIn("minor|paronimie", iesire)
        self.assertIn("eminent=remarcabil", iesire)

    def test_paronimia_nu_intra_in_scor(self):
        cod, iesire = ruleaza_stdin_cu_flags(
            "check-modelisme.py",
            "Un savant eminent a anuntat un pericol iminent.", "--scor")
        self.assertIn("scor_automat=0/4", iesire)

    def test_pleonasmul_nu_sare_granita_de_propozitie(self):
        """Regresie: fereastra de 80 de caractere prindea doua clauze diferite."""
        cod, iesire = ruleaza_stdin(
            "check-modelisme.py",
            "Hemoragia a fost oprita in zece minute, dar pacientul pierduse "
            "deja o cantitate mare de sange.")
        self.assertEqual(cod, 0, f"constructie corecta semnalata:\n{iesire}")

    def test_ortografia_corecta_a_unui_cuvant_nu_e_pleonasm(self):
        cod, iesire = ruleaza_stdin(
            "check-modelisme.py",
            "Elevii invata ortografia corecta a cuvintelor cu diftong.")
        self.assertEqual(cod, 0, f"uz didactic normal semnalat:\n{iesire}")

    def test_ortografie_corecta_nud_ramane_pleonasm(self):
        cod, iesire = ruleaza_stdin("check-modelisme.py",
                                    "Textul are o ortografie corecta.")
        self.assertEqual(cod, 1)
        self.assertIn("pleonasm_etimologic", iesire)

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
        self.assertIn("0 semnale automate", iesire)
        self.assertIn("de evaluat manual", iesire,
                      "raportul curat nu trebuie sa incurajeze livrarea imediata")

    def test_ordinea_flag_uri_si_fisier_nu_conteaza(self):
        cod, iesire = ruleaza("verifica.py", "--fara-seo", "--human-voice",
                              str(FIXTURES / "bun-articol.md"))
        self.assertEqual(cod, 0,
                         f"flag-urile inaintea fisierului au stricat input-ul:\n{iesire}")
        self.assertIn("AI_PATTERN_SCORE=", iesire)

    def test_prag_inaintea_fisierului_nu_confunda_valoarea_cu_inputul(self):
        cod, iesire = ruleaza("verifica.py", "--prag", "5",
                              str(FIXTURES / "bun-articol.md"))
        self.assertEqual(cod, 0, f"--prag inaintea fisierului a stricat input-ul:\n{iesire}")

    def test_lipsa_fisierului_e_eroare_de_input(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "verifica.py"), "--fara-seo"],
            capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("eroare", r.stderr)

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

    def test_fara_seo_sare_si_verificarile_de_titlu(self):
        text = "# Ghidul suprem pentru centrale termice\n\nUn paragraf."
        _, iesire_cu = ruleaza_stdin("verifica.py", text)
        self.assertIn("titlu_sablon", iesire_cu)
        _, iesire_fara = ruleaza_stdin_cu_flags("verifica.py", text, "--fara-seo")
        self.assertNotIn("titlu_sablon", iesire_fara)

    def test_json_seo_are_severitate(self):
        import json
        text = "# Unu\n\ntext\n\n# Doi\n\ntext"
        cod, iesire = ruleaza_stdin_cu_flags("verifica.py", text, "--json")
        date = json.loads(iesire)
        self.assertEqual(cod, 1)
        self.assertTrue(date["seo"])
        self.assertIn("severitate", date["seo"][0])
        self.assertEqual(date["seo"][0]["severitate"], "important")

    def test_scor_compact(self):
        cod, iesire = ruleaza_stdin_cu_flags(
            "verifica.py", "Un text scurt si cuminte despre nimic.", "--scor")
        self.assertIn("scor_automat=0/13", iesire)
        self.assertEqual(cod, 0)


class TestHumanVoice(unittest.TestCase):

    def test_cazurile_rele_sunt_semnalate(self):
        cod, iesire = ruleaza("check-human-voice.py",
                              str(FIXTURES / "human-voice-rau.md"))
        self.assertEqual(cod, 1)
        for categorie in ("filler", "promotional", "metafora_copywriter",
                          "punchline"):
            self.assertIn(categorie, iesire)
        self.assertIn("AI_PATTERN_SCORE=11/30", iesire)
        self.assertIn("STATUS=REWRITE", iesire)

    def test_textul_curat_trece(self):
        cod, iesire = ruleaza("check-human-voice.py",
                              str(FIXTURES / "human-voice-curat.md"))
        self.assertEqual(cod, 0, iesire)
        self.assertIn("AI_PATTERN_SCORE=0/30", iesire)
        self.assertIn("STATUS=PASS", iesire)

    def test_metafora_literara_legitima_nu_e_prinsa(self):
        cod, iesire = ruleaza("check-human-voice.py",
                              str(FIXTURES / "human-voice-metafora-legitima.md"))
        self.assertEqual(cod, 0, iesire)
        self.assertNotIn("metafora_copywriter", iesire)

    def test_autobiografia_cu_reper_nu_e_prinsa(self):
        cod, iesire = ruleaza("check-human-voice.py",
                              str(FIXTURES / "human-voice-autobiografie.md"))
        self.assertEqual(cod, 0, iesire)
        self.assertNotIn("autobiografie_nesustinuta", iesire)
        cod, iesire = ruleaza_stdin("check-human-voice.py",
                                    "Din experiența mea, munca se învață greu.")
        self.assertEqual(cod, 1)
        self.assertIn("autobiografie_nesustinuta", iesire)

    def test_contaminarea_si_placeholderul_sunt_blocere(self):
        cod, iesire = ruleaza("check-human-voice.py",
                              str(FIXTURES / "human-voice-contaminare.md"))
        self.assertEqual(cod, 1)
        self.assertIn("contaminare", iesire)
        self.assertIn("placeholder", iesire)
        self.assertIn("STATUS=REWRITE", iesire)
        self.assertIn("CONTAMINATION_FOUND=YES", iesire)
        self.assertIn("HUMAN_VOICE_BLOCKERS=contaminare,placeholder", iesire)

    def test_verifica_pastreaza_scorul_si_adauga_human_voice_json(self):
        import json
        cod, iesire = ruleaza_stdin_cu_flags(
            "verifica.py", "assistant: [DE COMPLETAT: nume]", "--human-voice", "--json")
        date = json.loads(iesire)
        self.assertEqual(cod, 1)
        self.assertEqual(date["scor_maxim"], 13)
        self.assertEqual(date["human_voice"]["ai_pattern_maxim"], 30)
        self.assertEqual(date["human_voice"]["STATUS"], "REWRITE")
        self.assertEqual(date["human_voice"]["CONTAMINATION_FOUND"], "YES")
        self.assertEqual(date["human_voice"]["blockers"],
                         ["contaminare", "placeholder"])

    def test_variantele_din_feedback_sunt_acoperite(self):
        cazuri = {
            "Hai să începem.": ("A", "filler"),
            "Să lămurim un lucru.": ("A", "filler"),
            "Merită menționat faptul că plouă.": ("A", "filler"),
            "Ține minte regula.": ("A", "filler"),
            "În esență, e simplu.": ("F", "concluzie_redundanta"),
            "Răspunsul se vede singur.": ("F", "concluzie_redundanta"),
            "Regretele devin scumpe.": ("B", "punchline"),
            "Answear și Fashiondays au rămas în draft.": ("J", "contaminare"),
            '{"prompt": "rescrie"}': ("J", "contaminare"),
            "[PLACEHOLDER]": ("J", "placeholder"),
            "ACESTA ESTE UN TITLU CAPS.": ("J", "caps"),
        }
        for text, (categorie, subcategorie) in cazuri.items():
            cod, iesire = ruleaza_stdin("check-human-voice.py", text)
            self.assertEqual(cod, 1, text)
            self.assertIn(f"|{categorie}|{subcategorie}|", iesire, text)

    def test_pragurile_de_status_si_blocker_override(self):
        # A (2) + B (3) = 5: PASS.
        _, iesire = ruleaza_stdin("check-human-voice.py",
                                  "Hai să. Asta e tot ce contează.")
        self.assertIn("AI_PATTERN_SCORE=5/30", iesire)
        self.assertIn("STATUS=PASS", iesire)
        # A (2) + C (3) + F (3) = 8: EDITED.
        _, iesire = ruleaza_stdin(
            "check-human-voice.py",
            "Hai să. Busola ta arată drumul. Pe scurt, alegi simplu.")
        self.assertIn("AI_PATTERN_SCORE=8/30", iesire)
        self.assertIn("STATUS=EDITED", iesire)
        # J=3 ar intra numeric la PASS, dar contaminarea forțează REWRITE.
        _, iesire = ruleaza_stdin("check-human-voice.py", "assistant: salut")
        self.assertIn("AI_PATTERN_SCORE=3/30", iesire)
        self.assertIn("STATUS=REWRITE", iesire)
        # CAPS rămâne un semnal J, fără greutate suplimentară.
        _, iesire = ruleaza_stdin("check-human-voice.py", "ACESTA ESTE UN TITLU CAPS.")
        self.assertIn("|J|caps|", iesire)
        self.assertIn("AI_PATTERN_SCORE=0/30", iesire)
        self.assertIn("STATUS=PASS", iesire)


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
    detectorul potrivit — altfel documentatia si scriptul au divergat.

    Corpul trece prin check-tipare.py. Titlurile-șablon („ghidul suprem",
    „tot ce trebuie să știi") sunt prinse de check-seo.py, și doar în titlu.
    """

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

    # Titlurile-șablon promise la Interzis sunt prinse de titlu_sablon,
    # doar dacă apar în titlu — nu în corp.
    EXPRESII_TITLU = [
        "# Ghidul suprem pentru centrale termice\n\nUn paragraf despre montaj.",
        "# Tot ce trebuie să știi despre pompe de căldură\n\nUn paragraf despre montaj.",
    ]

    def test_expresiile_din_skill_sunt_acoperite(self):
        for text in self.EXPRESII:
            cod, iesire = ruleaza_stdin("check-tipare.py", text)
            self.assertEqual(
                cod, 1, f"expresie interzisa neprinsă: {text!r}\n{iesire}")

    def test_titlurile_sablon_din_skill_sunt_acoperite(self):
        for text in self.EXPRESII_TITLU:
            cod, iesire = ruleaza_stdin("check-seo.py", text)
            self.assertEqual(
                cod, 1, f"titlu-șablon neprins: {text!r}\n{iesire}")
            self.assertIn("titlu_sablon", iesire, text)


class TestGenuriLegitime(unittest.TestCase):
    """Text formal si literar corect nu trebuie stricat de detectoare.

    Fixture-urile contin deliberat constructiile pe care le detectam — „constituie"
    de trei ori in cel juridic, „acest aspect"/„aceasta abordare"/„acest lucru" in
    cel academic, repetitie intentionata si dialog in cel literar. Un fixture care
    le evita n-ar demonstra nimic.

    Invariantul: detectoarele de continut (tipare, modelisme) tac. Familiile pot
    raporta `minor` — asta e rolul lor, semnal de recitire fara consecinta. Ritmul
    poate raporta: pragurile lui vin din corpusuri englezesti si dau fals pozitiv
    pe registru formal, motiv pentru care nu blocheaza livrarea (vezi
    `references/limba/scoring-checklist.md` §2).
    """

    GENURI = ("legit-juridic.md", "legit-academic.md", "legit-literar.md")

    def test_detectoarele_de_continut_tac(self):
        for fixture in self.GENURI:
            cod, iesire = ruleaza("verifica.py", str(FIXTURES / fixture), "--fara-seo")
            linie = next(l for l in iesire.splitlines() if l.startswith("scor_automat"))
            self.assertIn("tipare=0/6", linie, f"{fixture}: {iesire}")
            self.assertIn("modelisme=0/4", linie, f"{fixture}: {iesire}")

    def test_nicio_eroare_critica(self):
        for fixture in self.GENURI:
            cod, iesire = ruleaza("verifica.py", str(FIXTURES / fixture), "--fara-seo")
            critice = [l for l in iesire.splitlines() if l.startswith("critic|")]
            self.assertEqual(critice, [], f"{fixture}: text legitim semnalat ca eroare")

    def test_familiile_raporteaza_fara_sa_penalizeze(self):
        """Juridicul foloseste «constituie» de trei ori, academicul are trei
        referinte pronominale. Ambele se raporteaza, niciuna nu costa un punct."""
        for fixture, categorie in (("legit-juridic.md", "copula_evitata"),
                                   ("legit-academic.md", "referinta_vaga")):
            cod, iesire = ruleaza("verifica.py", str(FIXTURES / fixture), "--fara-seo")
            self.assertIn(f"minor|{categorie}", iesire, f"{fixture}: {iesire}")
            linie = next(l for l in iesire.splitlines() if l.startswith("scor_automat"))
            self.assertIn("tipare=0/6", linie,
                          f"{fixture}: familia a ajuns in scor")

    def test_proza_literara_ramane_intacta(self):
        """Repetitie intentionata, paralelism si dialog cu linie de pauza —
        niciunul nu e tipar de model."""
        cod, iesire = ruleaza("verifica.py", str(FIXTURES / "legit-literar.md"),
                              "--fara-seo")
        self.assertEqual(cod, 0, f"proza literara semnalata:\n{iesire}")


class TestTrimiteriDocumentatie(unittest.TestCase):
    """Trimiterile din SKILL.md si references/ trebuie sa duca undeva.

    Un agent care urmeaza o trimitere moarta fie se blocheaza, fie inventeaza
    continutul fisierului lipsa. Clasa asta de bug a aparut de doua ori: dupa
    spargerea lui `seo-geo.md` in references/seo/, si dupa renumerotarea
    sectiunilor SEO (trimiteri ramase la §8, §11).
    """

    # Fisiere ale proiectului utilizatorului sau exemple de nume, nu fisiere
    # ale skill-ului: nu au cum sa existe aici.
    EXTERNE = {"CLAUDE.md", "AGENTS.md", "README.md",
               "BRIEF.md", "CONTEXT.md", "brand.md"}

    def _surse(self):
        cai = [RADACINA / "SKILL.md"]
        cai.extend(sorted((RADACINA / "references").rglob("*.md")))
        return cai

    def _rezolva(self, sursa, referinta):
        """Intai relativ la fisierul sursa, apoi la radacina, apoi dupa nume.

        Cautarea dupa nume e deliberata: skill-ul foloseste peste tot nume nude
        („incarca `core.md`"), iar un agent le rezolva la fel — cauta fisierul
        cu numele ala in skill.
        """
        for candidat in ((sursa.parent / referinta).resolve(),
                         (RADACINA / referinta).resolve()):
            if candidat.exists():
                return candidat
        nume = Path(referinta).name
        return next((f for f in RADACINA.rglob(nume) if ".git" not in f.parts), None)

    def test_fisierele_referite_exista(self):
        import re
        tipar = re.compile(r"`([\w./-]+\.md)`")
        lipsa = []
        for sursa in self._surse():
            for referinta in tipar.findall(sursa.read_text(encoding="utf-8")):
                if Path(referinta).name in self.EXTERNE:
                    continue
                if self._rezolva(sursa, referinta) is None:
                    lipsa.append(f"{sursa.relative_to(RADACINA)} -> {referinta}")
        self.assertEqual(lipsa, [], "trimiteri catre fisiere inexistente:\n" +
                         "\n".join(lipsa))

    def test_sectiunile_referite_exista(self):
        """`fisier.md` §N trebuie sa aiba un heading care incepe cu N."""
        import re
        tipar = re.compile(r"`([\w./-]+\.md)`\s*(?:,\s*)?§([\w.]+)")
        headinguri = re.compile(r"^#{1,6}\s+(\S+)", re.MULTILINE)
        lipsa = []
        for sursa in self._surse():
            text = sursa.read_text(encoding="utf-8")
            for referinta, sectiune in tipar.findall(text):
                if Path(referinta).name in self.EXTERNE:
                    continue
                tinta = self._rezolva(sursa, referinta)
                if tinta is None:
                    continue  # raportat de testul de mai sus
                etichete = {e.rstrip(".") for e in
                            headinguri.findall(tinta.read_text(encoding="utf-8"))}
                # „§1.1-1.5" trimite la un interval — verifica primul capat.
                capat = sectiune.split("-")[0].rstrip(".")
                if capat not in etichete:
                    lipsa.append(f"{sursa.relative_to(RADACINA)} -> {referinta} §{sectiune}")
        self.assertEqual(lipsa, [], "trimiteri catre sectiuni inexistente:\n" +
                         "\n".join(lipsa))

    def test_fisierele_din_references_sunt_toate_rutate(self):
        """Un fisier pe care SKILL.md nu-l pomeneste nu va fi incarcat niciodata."""
        skill = (RADACINA / "SKILL.md").read_text(encoding="utf-8")
        orfane = [f.name for f in (RADACINA / "references").rglob("*.md")
                  if f.name not in skill]
        self.assertEqual(orfane, [], f"fisiere nereferite in SKILL.md: {orfane}")


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

    def test_titlu_clickbait(self):
        text = "# Nu-ți vine să crezi ce a urmat la montaj\n\nUn paragraf.\n"
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("titlu_clickbait", iesire)

    def test_titlu_clickbait_semne_de_exclamare(self):
        text = "# Centrală termică la bloc, acum!!\n\nUn paragraf.\n"
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("titlu_clickbait", iesire)

    def test_titlu_clickbait_cuvant_caps(self):
        text = "# ATENȚIE la montajul centralei pe gaz\n\nUn paragraf.\n"
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("titlu_clickbait", iesire)

    def test_titlu_bun_nu_e_clickbait(self):
        text = ("# Cum alegi o centrală termică pentru un apartament de 60 mp"
                "\n\nUn paragraf despre montaj.\n")
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertNotIn("titlu_clickbait", iesire, iesire)
        self.assertNotIn("titlu_sablon", iesire, iesire)
        self.assertNotIn("titlu_eticheta", iesire, iesire)
        self.assertNotIn("titlu_lung", iesire, iesire)

    def test_titlu_sablon(self):
        text = "# Ghidul suprem pentru centrale termice pe gaz\n\nUn paragraf.\n"
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("titlu_sablon", iesire)

    def test_titlu_sablon_top(self):
        text = "# Top 10 cele mai bune centrale termice\n\nUn paragraf.\n"
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("titlu_sablon", iesire)

    def test_sablon_in_corp_nu_e_semnalat(self):
        """Șablonul e problemă de titlu, nu de corp."""
        text = ("# Cum alegi o centrală termică pentru un apartament de 60 mp"
                "\n\nNu e ghidul suprem și nici tot ce trebuie să știi.\n")
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertNotIn("titlu_sablon", iesire, iesire)

    def test_titlu_lung(self):
        lung = "Cum alegi o centrală termică în 2026 pentru un apartament mic de 60 mp"
        self.assertGreater(len(lung), 65)
        text = f"# {lung}\n\nUn paragraf.\n"
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("titlu_lung", iesire)

    def test_titlu_eticheta(self):
        text = "# Centrale termice\n\nUn paragraf despre montaj.\n"
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("titlu_eticheta", iesire)

    def test_subtitluri_plate(self):
        text = ("# Cum alegi o centrală termică pentru un apartament de 60 mp\n\n"
                "Intro.\n\n## Beneficii\n\ntext\n\n## Caracteristici\n\n"
                "text\n\n## Preț\n\ntext\n")
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertEqual(cod, 1)
        self.assertIn("subtitluri_plate", iesire)

    def test_subtitluri_normale_nu_sunt_semnalate(self):
        text = ("# Cum alegi o centrală termică pentru un apartament de 60 mp\n\n"
                "Intro.\n\n## Ce costă o centrală de 24 kW la bloc\n\ntext\n\n"
                "## Dacă stai la casă, racordul decide\n\ntext\n\n"
                "## Ce se strică în anul trei de funcționare\n\ntext\n")
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertNotIn("subtitluri_plate", iesire, iesire)

    def test_fara_titlu_sare_verificarile_de_titlu(self):
        text = "Un paragraf fără heading și fără frontmatter.\n"
        cod, iesire = ruleaza_stdin("check-seo.py", text)
        self.assertNotIn("titlu_", iesire, iesire)

    def test_fixture_rau_titlu(self):
        cod, iesire = ruleaza("check-seo.py", str(FIXTURES / "rau-titlu.md"))
        self.assertEqual(cod, 1)
        self.assertIn("titlu_clickbait", iesire)
        self.assertIn("titlu_sablon", iesire)
        self.assertIn("subtitluri_plate", iesire)
        self.assertIn("important|", iesire)
        self.assertIn("minor|", iesire)


class TestContractCLI(unittest.TestCase):

    TOATE = ("check-tipare.py", "check-ritm.py", "check-seo.py",
             "check-modelisme.py", "check-human-voice.py", "verifica.py")

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


class TestMatriceFixtureuri(unittest.TestCase):
    """Orice script pe orice fixture are voie să dea doar exit 0 sau 1.

    Exit 2 înseamnă eroare de input — adică scriptul nu suportă un fișier
    valid din propriul corpus de test. Asta e defect, indiferent de verdict.
    """

    SCRIPTURI = ["check-tipare.py", "check-ritm.py", "check-modelisme.py",
                 "check-seo.py", "check-human-voice.py", "check-reclame.py"]

    def test_orice_script_ruleaza_pe_orice_fixture(self):
        erori = []
        for fisier in sorted(FIXTURES.glob("*.md")):
            for script in self.SCRIPTURI:
                cod, iesire = ruleaza(script, str(fisier))
                if cod >= 2:
                    erori.append(f"{script} pe {fisier.name}: exit {cod}\n{iesire}")
            cod, iesire = ruleaza("verifica.py", "--fara-seo", "--human-voice",
                                  str(fisier))
            if cod >= 2:
                erori.append(f"verifica.py --fara-seo --human-voice "
                             f"pe {fisier.name}: exit {cod}\n{iesire}")
        self.assertEqual(erori, [],
                         "scripturile au dat eroare de input pe fixture-uri valide:\n"
                         + "\n".join(erori))

    def test_fixtureurile_rau_au_nevoie_de_macar_un_semnal(self):
        """Un fixture numit rau_* trebuie prins de cel puțin un detector."""
        for fisier in sorted(FIXTURES.glob("rau-*.md")):
            cod, _ = ruleaza("verifica.py", str(fisier))
            self.assertEqual(cod, 1,
                             f"{fisier.name} ar trebui semnalat de macar o verificare")


def ruleaza_stdin_cu_flags(script, text, *flags):
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / script), "-", *flags],
        input=text, capture_output=True, text=True)
    return r.returncode, r.stdout


if __name__ == "__main__":
    unittest.main()
