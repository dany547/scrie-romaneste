#!/usr/bin/env python3
"""Listă de forme care lipsesc din lexiconul românesc, de verificat pe dexonline.

NU e verdict. „Lipsește din lexicon" nu înseamnă „nu există": Rospell (2013)
nu are tot vocabularul (neologisme, forme rare). Invers, un cuvânt inventat
care coincide cu o formă reală trece. Scriptul doar restrânge ce trebuie
verificat; agentul caută fiecare formă listată, pe rând, la adresa din raport.
Corectezi doar când dexonline spune „nu este în dicționar".

Se ignoră: blocuri/fragmente de cod, URL-uri, emailuri, cuvinte sub 4 litere
și numele proprii (majusculă în mijlocul propoziției, majuscule interne ca
`SlashGear`, sigle). Un cuvânt cu majusculă doar la început de propoziție se
verifică, ca un cuvânt inventat acolo să nu treacă drept nume. Din cuvintele compuse cu cratimă
se verifică fiecare parte de cel puțin 4 litere. Comparația e diacritic-
insensibilă (aceeași pliere ca restul scripturilor).

Usage:
    check-cuvinte.py <fisier_sau_->
    check-cuvinte.py <fisier> --allow termeni.txt   # un termen pe linie, # comentariu
    check-cuvinte.py <fisier> --tot                 # fără plafon de afișare
    check-cuvinte.py <fisier> --lexicon cale.txt.gz # sau SCRIE_RO_LEXICON

Lângă lexicon, `scripts/lexicon/completari.txt` are forme românești confirmate
pe dexonline și lipsă din Rospell (`dronele`, `inchi`...); se aplică automat.
Dacă peste 30% din formele unice lipsesc din lexicon (text în engleză, cod,
mesaje de eroare), raportul are o singură linie `info|cuvinte|text
predominant neromânesc` în loc de listă; `--tot` o dă oricum.

Raport: `important|cuvant_de_verificat|L<linie>|<formă> xN|→ <URL dexonline>`

Exit codes:
    0 = nicio formă de verificat
    1 = cel puțin o formă de verificat
    2 = eroare de input sau lexicon indisponibil
"""
import gzip
import os
import re
import sys
from pathlib import Path

import _comun

LEXICON_IMPLICIT = Path(__file__).resolve().parent / "lexicon" / "lexicon-ro.txt.gz"
COMPLETARI_IMPLICIT = Path(__file__).resolve().parent / "lexicon" / "completari.txt"
PLAFON = 10
PRAG_NEROMANESC = 0.30  # peste această pondere din formele unice → text neromânesc
MIN_EXAMINATE = 40      # sub atâtea forme unice nu se judecă limba textului
LUNGIME_MINIMA = 4
DEXONLINE = "https://dexonline.ro/definitie/"

_COD = re.compile(r"```.*?```|~~~.*?~~~|`[^`\n]*`", re.S)
_URL = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
_CUVANT = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*")
# Ce precede un cuvânt la început de propoziție: punct, două puncte, început de
# rând, eventual cu marcator markdown (#, *, -, >, 1.) sau ghilimea deschisă.
_INCEPUT_PROPOZITIE = re.compile(
    r"(?:[.!?:]|\n|^)[ \t]*(?:(?:[#>*\-•]+|\d+[.)])[ \t]*)?[„\"«(]*$")


def incarca_lexicon(cale):
    with gzip.open(cale, "rt", encoding="utf-8") as f:
        return frozenset(f.read().split("\n"))


def incarca_allow(cale):
    """Fișier cu un termen pe linie; `#` începe un comentariu."""
    termeni = set()
    with open(cale, encoding="utf-8-sig") as f:
        for linie in f:
            linie = linie.split("#", 1)[0].strip()
            if linie:
                termeni.add(_comun.pliaza(linie))
    return termeni


def incarca_completari(cale_lexicon):
    """Completări manuale, lângă lexicon: forme confirmate pe dexonline, lipsă
    din Rospell. Cu `--lexicon` propriu, completările implicite nu se aplică."""
    cale = COMPLETARI_IMPLICIT if Path(cale_lexicon) == LEXICON_IMPLICIT else None
    if cale is None or not cale.exists():
        return frozenset()
    return frozenset(incarca_allow(cale))


def _maskeaza(text):
    """Înlocuiește codul și URL-urile cu spații (lungime păstrată → linii corecte)."""
    def spatii(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    return _URL.sub(spatii, _COD.sub(spatii, text))


def gaseste(text, lexicon, allow=frozenset()):
    """Returnează ({formă_pliată: {"afisat", "parte", "linie", "nr"}}, examinate).

    `examinate` = câte forme unice au fost judecate (baza pentru ponderea
    formelor lipsă). Rezultatul păstrează ordinea apariției.
    """
    text = _maskeaza(text)
    rezultat = {}
    examinate = set()
    la_inceput = {}
    nume = set()  # forme care apar cu majusculă în mijlocul propoziției
    for m in _CUVANT.finditer(text):
        token = m.group(0)
        if token[0].isupper():
            la_inceput[m.start()] = bool(
                _INCEPUT_PROPOZITIE.search(text[max(0, m.start() - 12):m.start()]))
            if not la_inceput[m.start()]:
                nume.add(_comun.pliaza(token))
    for m in _CUVANT.finditer(text):
        token = m.group(0)
        if token[0].isupper():
            # nume propriu/marcă: majusculă în mijlocul propoziției, majuscule
            # interne (SlashGear), sigle (ARN) sau un cuvânt care apare altundeva
            # cu majusculă. Un cuvânt capitalizat doar la început de propoziție
            # se verifică, altfel „Procesorarea" ar trece drept nume.
            if (not la_inceput[m.start()] or token.isupper()
                    or any(c.isupper() for c in token[1:])
                    or _comun.pliaza(token) in nume):
                continue
        if any(len(p) >= LUNGIME_MINIMA for p in token.split("-")):
            examinate.add(_comun.pliaza(token))
        necunoscut = None  # prima parte a compusului care lipsește
        for parte in token.split("-"):
            if len(parte) < LUNGIME_MINIMA:
                continue
            forma = _comun.pliaza(parte)
            if forma not in lexicon and forma not in allow:
                necunoscut = necunoscut or parte
        if not necunoscut:
            continue
        cheie = _comun.pliaza(token)
        if cheie in rezultat:
            rezultat[cheie]["nr"] += 1
        else:
            rezultat[cheie] = {"afisat": token, "parte": necunoscut, "nr": 1,
                               "linie": text.count("\n", 0, m.start()) + 1}
    return rezultat, len(examinate)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    def valoare(flag):
        if flag not in argv:
            return None
        i = argv.index(flag)
        if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
            raise ValueError(f"{flag} cere o valoare")
        return argv[i + 1]

    try:
        cale_lexicon = (valoare("--lexicon") or os.environ.get("SCRIE_RO_LEXICON")
                        or LEXICON_IMPLICIT)
        cale_allow = valoare("--allow")
    except ValueError as e:
        print(f"eroare: {e}", file=sys.stderr)
        return 2
    optiuni_cu_valoare = {"--lexicon", "--allow"}
    pozitionale = [a for i, a in enumerate(argv)
                   if not a.startswith("--") and (i == 0 or argv[i - 1] not in optiuni_cu_valoare)]
    if len(pozitionale) != 1:
        print("eroare: cere exact un fișier (sau '-' pentru stdin)", file=sys.stderr)
        return 2
    sursa = pozitionale[0]

    try:
        text = _comun.citeste_intrare(sursa)
        try:
            lexicon = incarca_lexicon(cale_lexicon)
        except (OSError, EOFError) as e:
            print(f"eroare: lexiconul {cale_lexicon} nu poate fi citit ({e}); "
                  "vezi --lexicon / SCRIE_RO_LEXICON", file=sys.stderr)
            return 2
        allow = incarca_allow(cale_allow) if cale_allow else frozenset()
        allow = allow | incarca_completari(cale_lexicon)
    except (OSError, EOFError) as e:
        print(f"eroare: {e}", file=sys.stderr)
        return 2

    gasite, examinate = gaseste(text, lexicon, allow)
    cuvinte = _comun.numara_cuvinte(text)
    if not gasite:
        print(f"0 forme de verificat ({cuvinte} cuvinte, lexicon={len(lexicon)} forme)")
        return 0

    elemente = list(gasite.values())
    pondere = len(elemente) / max(examinate, 1)
    if examinate >= MIN_EXAMINATE and pondere > PRAG_NEROMANESC and "--tot" not in argv:
        print(f"info|cuvinte|text predominant neromânesc: {len(elemente)} din "
              f"{examinate} forme unice ({pondere:.0%}) lipsesc din lexicon; lista nu "
              f"se afișează (--tot o dă)")
        print(f"---\ntotal={len(elemente)} forme de verificat | {cuvinte} cuvinte | "
              f"lexicon={len(lexicon)} forme")
        return 1
    afisate = elemente if "--tot" in argv else elemente[:PLAFON]
    for g in afisate:
        sufix = f" x{g['nr']}" if g["nr"] > 1 else ""
        print(f"important|cuvant_de_verificat|L{g['linie']}|{g['afisat']}{sufix}"
              f"|→ {DEXONLINE}{g['parte'].lower()}")
    if len(elemente) > len(afisate):
        print(f"mai_sunt|{len(elemente) - len(afisate)} forme neafișate (--tot)")
    print(f"---\ntotal={len(elemente)} forme de verificat | {cuvinte} cuvinte | "
          f"lexicon={len(lexicon)} forme")
    print("nota: lipsa din lexicon nu e verdict. Verifică fiecare formă pe "
          "dexonline; corectează doar la „nu este în dicționar”.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
