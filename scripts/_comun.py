"""Infrastructură comună pentru scripturile de verificare.

Nu se rulează direct. Oferă: fold de diacritice length-preserving, segmentare
pe paragrafe, motorul de scanare cu praguri (mereu / la_aglomerare /
la_densitate), deduplicare și formatarea raportului pipe-delimited.

Tiparele sunt tupluri (regex, prag) sau (regex, prag, sugestie). Sugestia,
când există, apare în raport după fragment: `...|→ sugestia`.
"""
import importlib.util
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

PRAG_DENSITATE_IMPLICIT = 5.0  # apariții la 1000 de cuvinte
PRAG_AGLOMERARE = 3  # apariții ale aceluiași tipar în același paragraf
CONTEXT_CHARS = 40

ORDINE_SEVERITATE = {"critic": 0, "important": 1, "minor": 2, "sub_prag": 3}

# Fold length-preserving: fiecare caracter devine exact un caracter, deci
# offset-urile din textul pliat rămân valide în textul original.
FOLD = str.maketrans({
    "ă": "a", "â": "a", "î": "i", "ș": "s", "ț": "t",
    "Ă": "A", "Â": "A", "Î": "I", "Ș": "S", "Ț": "T",
    "ş": "s", "ţ": "t", "Ş": "S", "Ţ": "T",  # sedilă (legacy)
})


def pliaza(text):
    """Înlocuiește diacriticele 1:1 (lungimea se păstrează)."""
    return text.translate(FOLD).lower()


def indici_paragrafe(text):
    """Listă de (start, end) pentru fiecare paragraf, în ordine."""
    limite = []
    pozitie = 0
    for bucata in re.split(r"\n\s*\n", text):
        start = text.find(bucata, pozitie)
        if start < 0:
            start = pozitie
        limite.append((start, start + len(bucata)))
        pozitie = start + len(bucata)
    return limite


def paragraf_pentru(offset, limite):
    for i, (start, end) in enumerate(limite):
        if start <= offset <= end:
            return i
    return -1


def numara_cuvinte(text):
    return len(re.findall(r"\b[\wăâîșțĂÂÎȘȚ]+\b", text))


def _desfa(intrare):
    """(regex, prag) sau (regex, prag, sugestie) -> (regex, prag, sugestie|None)."""
    if len(intrare) == 3:
        return intrare
    tipar, prag = intrare
    return tipar, prag, None


def scaneaza(text, categorii, categorii_original=None,
             prag_densitate=PRAG_DENSITATE_IMPLICIT, arata_tot=False):
    """Rulează categoriile pe textul pliat (și, opțional, pe cel original).

    Returnează (raportate, depasiri, cuvinte). Fiecare potrivire raportată e un
    dict cu categorie, severitate, linie, fragment, sugestie (sau None).
    """
    text = unicodedata.normalize("NFC", text)
    pliat = pliaza(text)
    limite = indici_paragrafe(text)
    cuvinte = max(numara_cuvinte(text), 1)

    brute = []
    surse = [(categorii, pliat)]
    if categorii_original:
        surse.append((categorii_original, text))
    for tabel, tinta in surse:
        for categorie, (severitate, tipare) in tabel.items():
            for intrare in tipare:
                tipar, prag, sugestie = _desfa(intrare)
                if prag == "niciodata":
                    continue
                for m in re.finditer(tipar, tinta, re.IGNORECASE | re.MULTILINE):
                    start = max(0, m.start() - CONTEXT_CHARS)
                    end = min(len(text), m.end() + CONTEXT_CHARS)
                    fragment = " ".join(text[start:end].split())
                    linie = text.count("\n", 0, m.start()) + 1
                    brute.append({
                        "categorie": categorie,
                        "severitate": severitate,
                        "prag": prag,
                        "tipar": tipar,
                        "sugestie": sugestie,
                        "offset": m.start(),
                        "sfarsit": m.end(),
                        "linie": linie,
                        "fragment": fragment,
                    })

    # Filtrare pe praguri: „mereu" trece mereu; celelalte doar dacă tiparul se
    # aglomerează într-un paragraf sau depășește densitatea pe tot textul.
    pe_tipar = defaultdict(list)
    for b in brute:
        pe_tipar[b["tipar"]].append(b)

    raportate = []
    depasiri = []
    for tipar, aparitii in pe_tipar.items():
        prag = aparitii[0]["prag"]
        if prag == "mereu":
            raportate.extend(aparitii)
            continue

        densitate = len(aparitii) * 1000.0 / cuvinte
        pe_paragraf = defaultdict(int)
        for a in aparitii:
            pe_paragraf[paragraf_pentru(a["offset"], limite)] += 1
        aglomerat = any(n >= PRAG_AGLOMERARE for n in pe_paragraf.values())

        # Una sau două apariții nu sunt niciodată un tipar — indiferent cât de
        # scurt e textul. Fără regula asta, un text de 100 de cuvinte depășește
        # orice densitate la prima potrivire.
        destule = len(aparitii) >= PRAG_AGLOMERARE

        if destule and (densitate >= prag_densitate or aglomerat):
            raportate.extend(aparitii)
            motiv = "aglomerare" if aglomerat else f"densitate={densitate:.1f}"
            depasiri.append((aparitii[0]["categorie"], aparitii[0]["tipar"],
                             len(aparitii), motiv))
        elif arata_tot:
            for a in aparitii:
                a["severitate"] = "sub_prag"
            raportate.extend(aparitii)

    raportate.sort(key=lambda b: b["offset"])
    return dedupleaza(raportate), depasiri, cuvinte


def dedupleaza(raportate):
    """Două tipare din aceeași categorie care prind același fragment se
    raportează o singură dată."""
    pastrate = []
    ultim_sfarsit = {}
    for r in raportate:
        cat = r["categorie"]
        if r["offset"] < ultim_sfarsit.get(cat, -1):
            continue
        ultim_sfarsit[cat] = r["sfarsit"]
        pastrate.append(r)
    return pastrate


def linie_raport(r):
    baza = f"{r['severitate']}|{r['categorie']}|L{r['linie']}|{r['fragment']}"
    if r.get("sugestie"):
        baza += f"|→ {r['sugestie']}"
    return baza


def tipareste_raport(raportate, depasiri, cuvinte, eticheta):
    """Raportul standard: potriviri sortate pe severitate + agregate + praguri.

    Returnează exit code-ul (0 curat, 1 potriviri grave sau praguri depășite).
    """
    if not raportate:
        print(f"0 tipare {eticheta} gasite ({cuvinte} cuvinte)")
        return 0

    raportate.sort(key=lambda b: (ORDINE_SEVERITATE[b["severitate"]], b["offset"]))
    for r in raportate:
        print(linie_raport(r))

    agregate = defaultdict(int)
    for r in raportate:
        agregate[r["severitate"]] += 1
    rezumat = ", ".join(f"{s}={n}" for s, n in
                        sorted(agregate.items(), key=lambda x: ORDINE_SEVERITATE[x[0]]))
    densitate = len(raportate) * 1000.0 / max(cuvinte, 1)
    print(f"---\ntotal={len(raportate)} ({rezumat}) | "
          f"{cuvinte} cuvinte | densitate={densitate:.1f}/1000cuv")
    if depasiri:
        pe_categorie = defaultdict(lambda: [0, set()])
        for categorie, _tipar, n, motiv in depasiri:
            pe_categorie[categorie][0] += n
            pe_categorie[categorie][1].add(motiv.split("=")[0])
        for categorie, (n, motive) in sorted(pe_categorie.items()):
            print(f"prag_depasit|{categorie}|{n} aparitii|{','.join(sorted(motive))}")

    grav = any(r["severitate"] in ("critic", "important") for r in raportate)
    return 1 if (grav or depasiri) else 0


def citeste_intrare(sursa):
    """Citește fișierul sau stdin ('-'). Aruncă OSError la eșec."""
    if sursa == "-":
        return sys.stdin.read()
    with open(sursa, "r", encoding="utf-8") as f:
        return f.read()


def ruleaza_cli(doc, argv, categorii, categorii_original, calculeaza_scor,
                scor_maxim, eticheta, nota_scor=None):
    """main() comun pentru scripturile bazate pe categorii de tipare."""
    if not argv or argv[0] in ("-h", "--help"):
        print(doc)
        return 0

    sursa = argv[0]
    prag = PRAG_DENSITATE_IMPLICIT
    if "--prag" in argv:
        try:
            prag = float(argv[argv.index("--prag") + 1])
        except (IndexError, ValueError):
            print("eroare: --prag cere un număr", file=sys.stderr)
            return 2
    arata_tot = "--tot" in argv
    doar_scor = "--scor" in argv

    try:
        text = citeste_intrare(sursa)
    except OSError as e:
        print(f"eroare: {e}", file=sys.stderr)
        return 2

    raportate, depasiri, cuvinte = scaneaza(
        text, categorii, categorii_original, prag, arata_tot)
    semnale, scor = calculeaza_scor(raportate, depasiri)

    if doar_scor:
        detaliu = ", ".join(f"{n}={p}" for n, p in semnale) or "niciun semnal"
        print(f"scor_automat={scor}/{scor_maxim} ({detaliu})")
        if nota_scor:
            print(nota_scor)
        return 1 if scor else 0

    return tipareste_raport(raportate, depasiri, cuvinte, eticheta)


def incarca_script(nume):
    """Importă un script frate după numele fișierului (au cratime în nume)."""
    cale = Path(__file__).resolve().parent / f"{nume}.py"
    spec = importlib.util.spec_from_file_location(nume.replace("-", "_"), cale)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul
