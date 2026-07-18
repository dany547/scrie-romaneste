#!/usr/bin/env python3
"""Scanează un text pentru clișee AI, calcuri din engleză și tranziții mecanice.

Potrivirea ignoră diacriticele, deci prinde și textul scris fără ele sau cu
sedilă (ş/ţ) în loc de virgulă (ș/ț). Tiparele acoperă formele flexionare, nu
doar forma de dicționar.

Fiecare tipar are o severitate (critic/important/minor) și un prag:
    mereu          — semnalat la orice apariție
    la_aglomerare  — semnalat la 3+ în același paragraf sau peste densitate
    la_densitate   — semnalat doar peste densitate

Usage:
    check-tipare.py <fisier_sau_->
    check-tipare.py <fisier> --prag 5      # apariții/1000 cuvinte (default 5)
    check-tipare.py <fisier> --tot         # arată și potrivirile sub prag
    check-tipare.py <fisier> --scor        # doar scorul de semnale
    check-tipare.py --help

Exit codes:
    0 = curat (nimic critic sau important, niciun prag depășit)
    1 = potriviri raportate
    2 = eroare de input (fișier lipsă etc.)
"""
import re
import sys
import unicodedata
from collections import defaultdict

PRAG_DENSITATE_IMPLICIT = 5.0  # apariții la 1000 de cuvinte
PRAG_AGLOMERARE = 3  # apariții ale aceluiași tipar în același paragraf
CONTEXT_CHARS = 40

# Fold length-preserving: fiecare caracter devine exact un caracter, deci
# offset-urile din textul pliat rămân valide în textul original.
FOLD = str.maketrans({
    "ă": "a", "â": "a", "î": "i", "ș": "s", "ț": "t",
    "Ă": "A", "Â": "A", "Î": "I", "Ș": "S", "Ț": "T",
    "ş": "s", "ţ": "t", "Ş": "S", "Ţ": "T",  # sedilă (legacy)
})


def adj(tulpina):
    """Adjectiv: toate terminațiile de gen, număr și articol."""
    return rf"\b{tulpina}(a|ul|ului|ui|i|ii|ilor|e|ele|elor)?\b"


def subst(tulpina):
    """Substantiv: singular/plural, nearticulat/articulat."""
    return rf"\b{tulpina}(a|ea|ul|ului|le|lor|i|ii|e|ele)?\b"


# Tiparele sunt scrise fără diacritice — se potrivesc pe textul pliat.
CATEGORII = {
    "structura": ("important", [
        (r"\bin concluzie\b", "mereu"),
        (r"\bin esenta\b", "mereu"),
        (r"\bpe scurt\b", "la_aglomerare"),
        (r"\bprin urmare\b", "la_aglomerare"),
        (r"\bde asemenea\b", "la_aglomerare"),
        (r"\bin plus\b", "la_aglomerare"),
        (r"\btotodata\b", "la_aglomerare"),
        (r"\bcu toate acestea\b", "la_aglomerare"),
        (r"\bmai mult decat atat\b", "mereu"),
        (r"\bpe de o parte\b.{0,400}?\bpe de alta parte\b", "mereu"),
        (r"\bin primul rand\b.{0,600}?\bin al doilea rand\b", "mereu"),
        (r"\bnu doar\b.{0,120}?\bci si\b", "la_aglomerare"),
    ]),
    "introduceri": ("critic", [
        (r"\bin lumea (de astazi|digitala|moderna|contemporana)\b", "mereu"),
        (r"\bintr-o lume in continua schimbare\b", "mereu"),
        (r"\bin era digitala\b", "mereu"),
        (r"\bin societatea moderna\b", "mereu"),
        (r"\bin contextul actual\b", "mereu"),
        (r"\bde cand lumea si pamantul\b", "mereu"),
    ]),
    "umpluturi": ("critic", [
        (r"\beste important de mentionat ca\b", "mereu"),
        (r"\bmerita (precizat|subliniat|mentionat) (faptul )?ca\b", "mereu"),
        (r"\btrebuie mentionat (faptul )?ca\b", "mereu"),
        (r"\beste demn de (remarcat|mentionat)\b", "mereu"),
        (r"\bin acest articol\b", "mereu"),
        (r"\bin cele ce urmeaza\b", "mereu"),
    ]),
    "vocabular_corporatist": ("important", [
        (adj("revolutionar"), "mereu"),
        (adj("impresionant"), "la_aglomerare"),
        (adj("remarcabil"), "la_aglomerare"),
        (adj("vibrant"), "mereu"),
        (r"\bschimbare de paradigma\b", "mereu"),
        (r"\bun pilon fundamental\b", "mereu"),
        (r"\bo componenta esentiala\b", "mereu"),
        (r"\babordare holistica\b", "mereu"),
        (r"\badopta o (abordare|filozofie|strategie)\b", "mereu"),
        (r"\bse remarca prin\b", "la_aglomerare"),
        (r"\bsolutie? de ultima generatie\b", "mereu"),
        (r"\bsolutii? inovatoare\b", "mereu"),
    ]),
    "abstractiuni": ("minor", [
        (subst("optimizar"), "la_densitate"),
        (subst("aliniere"), "la_densitate"),
        (subst("eficientizar"), "la_densitate"),
        (subst("implementar"), "la_densitate"),
        (subst("valorificar"), "la_densitate"),
        (r"\ba facilita\b", "la_densitate"),
        (r"\ba contribui la\b", "la_densitate"),
        (r"\bun impact (semnificativ|major|considerabil) asupra\b", "la_aglomerare"),
        (r"\bse recomanda adoptarea\b", "mereu"),
    ]),
    "cuantificari_vagi": ("important", [
        (r"\bo serie de\b", "la_aglomerare"),
        (r"\bo multitudine de\b", "mereu"),
        (r"\bun numar (semnificativ|considerabil|impresionant)\b", "mereu"),
        (r"\bo (gama|paleta) (larga|variata) de\b", "mereu"),
        (r"\bun spectru larg de\b", "mereu"),
    ]),
    "hedging": ("important", [
        (r"\beste posibil ca\b", "la_aglomerare"),
        (r"\bs-ar putea ca\b", "la_aglomerare"),
        (r"\bpoate fi considerat\b", "la_aglomerare"),
        (r"\bin general\b", "la_densitate"),
        (r"\bde regula\b", "la_densitate"),
    ]),
    "romgleza": ("critic", [
        (r"\bface sens\b", "mereu"),
        (r"\b(joaca|joc|jucat|juca|jucand|jucam) un rol (crucial|cheie)\b", "mereu"),
        (r"\bla sfarsitul zilei\b", "mereu"),
        (r"\bin termeni de\b", "mereu"),
        (r"\bseamless\b", "mereu"),
        (r"\binsight-?uri\b", "mereu"),
        (adj("actionabil"), "mereu"),
        (r"\ba performa\b", "mereu"),
    ]),
    "calc_sintactic": ("critic", [
        (r"\ba adresa (o |aceasta |aceste |problema|probleme)", "mereu"),
        (r"\b(adreseaza|adresam|adresat|adresand) (o |aceasta |aceste )?(problema|probleme|provocar)", "mereu"),
        (r"\ba aplica pentru (un |o |acest|aceasta)?\s*(post|job|rol|pozitie)", "mereu"),
        (r"\bde catre (sistem|platforma|algoritm|aplicatie|program|software)", "mereu"),
        (r"\bin ordine sa\b", "mereu"),
        (r"\bbazat pe faptul ca\b", "mereu"),
    ]),
    "pleonasm": ("important", [
        (r"\ba reveni din nou\b|\brevine din nou\b|\brevenit din nou\b", "mereu"),
        (r"\ba colabora impreuna\b|\bcolaboreaza impreuna\b", "mereu"),
        (r"\bconsens comun\b", "mereu"),
        (r"\bprogres inainte\b|\bavanseaza inainte\b", "mereu"),
        (r"\bmijloace mass-?media\b", "mereu"),
        (r"\baniversarea a \d+ ani\b", "mereu"),
    ]),
    "repetitie_mascata": ("minor", [
        (r"\bclar si usor de inteles\b", "mereu"),
        (r"\beficient si productiv\b", "mereu"),
        (r"\brapid si intr-un timp scurt\b", "mereu"),
        (r"\bsimplu si facil\b", "mereu"),
        (r"\butil si benefic\b", "mereu"),
    ]),
    "echilibru_fortat": ("minor", [
        (r"\balegerea (optima|potrivita) depinde de\b", "mereu"),
        (r"\bdepinde de nevoile (fiecaruia|dumneavoastra|tale)\b", "mereu"),
        (r"\bare (propriile |si )?avantaje si dezavantaje\b", "la_aglomerare"),
        (r"\bdepinde de context\b", "la_aglomerare"),
    ]),
    "artefact_chatbot": ("critic", [
        (r"^\s*(sigur|desigur|cu placere)[!,.]", "mereu"),
        (r"\bexcelenta intrebare\b", "mereu"),
        (r"\bsper ca (te ajuta|va ajuta|informatiile)\b", "mereu"),
        (r"\banunta-ma daca\b|\bspune-mi daca (mai )?ai\b", "mereu"),
        (r"\bhai sa (analizam|gandim|o luam) pas cu pas\b", "mereu"),
        (r"\biata (textul|articolul|varianta) (rescris|rescrisa|final)", "mereu"),
        (r"\bin speranta ca\b", "mereu"),
    ]),
    "amprenta_unealta": ("critic", [
        (r"\[numele (tau|dvs|companiei)\]", "mereu"),
        (r"\[(x|y|nume|data|oras|link|url)\]", "mereu"),
        (r"\b\d{4}-xx-xx\b|\bxx\.xx\.\d{4}\b", "mereu"),
        (r"oai_citation", "mereu"),
        (r"cite\s*turn\d+\w*", "mereu"),
        (r"utm_source=(chatgpt|claude|perplexity|gemini)", "mereu"),
    ]),
}

# Tipare care depind de caracterele originale (ghilimele, diacritice, cifre) și
# de aceea se aplică pe textul nepliat.
CATEGORII_ORIGINAL = {
    "tipografie_anglicizata": ("minor", [
        (r'"[^"\n]{3,}"', "la_aglomerare"),          # ghilimele englezești
        (r"\b\d+\.\d+\s*(%|la suta|lei|euro)", "mereu"),  # punct zecimal
        (r"\s—\s.{0,80}\s—\s", "la_aglomerare"),     # abuz de linie de pauză
    ]),
}


def pliaza(text):
    """Normalizează NFC și înlocuiește diacriticele 1:1 (lungimea se păstrează)."""
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


def scaneaza(text, prag_densitate=PRAG_DENSITATE_IMPLICIT, arata_tot=False):
    text = unicodedata.normalize("NFC", text)
    pliat = pliaza(text)
    limite = indici_paragrafe(text)
    cuvinte = max(numara_cuvinte(text), 1)

    brute = []  # (categorie, severitate, prag, tipar, offset, linie, fragment)
    surse = [(CATEGORII, pliat), (CATEGORII_ORIGINAL, text)]
    for tabel, tinta in surse:
        for categorie, (severitate, tipare) in tabel.items():
            for tipar, prag in tipare:
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


ORDINE_SEVERITATE = {"critic": 0, "important": 1, "minor": 2, "sub_prag": 3}


SCOR_MAXIM = 6


def calculeaza_scor(raportate, depasiri):
    """Semnale deterministe, 0-6 puncte. Restul rubricii ține de judecata umană."""
    raportate = [r for r in raportate if r["severitate"] != "sub_prag"]
    categorii = {r["categorie"] for r in raportate}
    semnale = []
    tranzitii = sum(1 for r in raportate if r["categorie"] == "structura")
    if tranzitii >= 3:
        semnale.append(("tranzitii_standard_repetate", 1))
    if categorii & {"romgleza", "calc_sintactic"}:
        semnale.append(("calc_din_engleza", 1))
    if categorii & {"introduceri", "umpluturi"}:
        semnale.append(("formule_de_deschidere", 1))
    lexic = sum(1 for r in raportate if r["categorie"] in
                ("vocabular_corporatist", "abstractiuni", "cuantificari_vagi"))
    if lexic >= 3:
        semnale.append(("lexic_corporatist", 1))
    if categorii & {"artefact_chatbot", "amprenta_unealta"}:
        semnale.append(("artefact_de_generare", 2))
    return semnale, sum(p for _, p in semnale)


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
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
        text = sys.stdin.read() if sursa == "-" else open(
            sursa, "r", encoding="utf-8").read()
    except OSError as e:
        print(f"eroare: {e}", file=sys.stderr)
        return 2

    raportate, depasiri, cuvinte = scaneaza(text, prag, arata_tot)
    semnale, scor = calculeaza_scor(raportate, depasiri)

    if doar_scor:
        detaliu = ", ".join(f"{n}={p}" for n, p in semnale) or "niciun semnal"
        print(f"scor_automat={scor}/{SCOR_MAXIM} ({detaliu})")
        print("nota: semnalele despre surse inventate si densitatea de "
              "informatie nu pot fi masurate automat — le evalueaza modelul.")
        return 1 if scor else 0

    if not raportate:
        print(f"0 tipare AI gasite ({cuvinte} cuvinte)")
        return 0

    raportate.sort(key=lambda b: (ORDINE_SEVERITATE[b["severitate"]], b["offset"]))
    for r in raportate:
        print(f"{r['severitate']}|{r['categorie']}|L{r['linie']}|{r['fragment']}")

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


if __name__ == "__main__":
    sys.exit(main())
