#!/usr/bin/env python3
"""Listă de forme care lipsesc din lexiconul românesc, de verificat în surse permise.

NU e verdict. „Lipsește din lexicon" nu înseamnă „nu există": Rospell (2013)
nu are tot vocabularul (neologisme, forme rare). Invers, un cuvânt inventat
care coincide cu o formă reală trece. Scriptul doar restrânge ce trebuie
verificat; verificarea fiecărei forme se face în sursele permise, prin
revizuire contextuală — linkul din raport e doar un punct de pornire.
Absența din lexicon nu e verdict și nu impune nicio corectură: verifică forma,
lema și sensul în sursele permise, apoi decide; nu aplica automat
sugestiile.

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
    check-cuvinte.py <fisier> --sugestii            # variante ortografice (hunspell)
    check-cuvinte.py <fisier> --sugestii --dictionar NUME  # nume sau prefix de cale
                                                      # (fără .dic/.aff), implicit ro_RO

Cu `--sugestii`, imediat după fiecare formă afișată apare o linie
`sugestii|L<linie>|<afisat>|<var1> / <var2> ...` (maximum 5) sau
`sugestii|L<linie>|<afisat>|fără sugestii`. E opțional și doar informativ:
sugestiile NU se aplică automat și NU confirmă sensul. Fără flag nu se invocă
niciun proces hunspell. Cu flag, dacă motorul nu e disponibil pentru o listă
chiar afișată, scriptul iese cu 2 fără raport parțial; `--dictionar` fără
`--sugestii` e eroare de invocare (2).

Lângă lexicon, `scripts/lexicon/completari.txt` are forme românești confirmate
pe dexonline și lipsă din Rospell (`dronele`, `inchi`...); se aplică automat.
Dacă peste 30% din formele unice lipsesc din lexicon (text în engleză, cod,
mesaje de eroare), raportul are în loc de listă linia `info|cuvinte|text
predominant neromânesc`, apoi `---` și totalul; `--tot` dă lista oricum.

Raport: `important|cuvant_de_verificat|L<linie>|<formă> xN|→ <URL dexonline>`

Exit codes:
    0 = nicio formă de verificat
    1 = cel puțin o formă de verificat
    2 = eroare de input, lexicon indisponibil sau --sugestii fără motor disponibil
"""
import gzip
import os
import re
import sys
import zlib
from pathlib import Path

import _comun
import _hunspell

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
    r"(?:[.!?:]|\n|^)[ \t]*(?:(?:[#>*\-•—–]+|\d+[.)])[ \t]*)?[„\"«(]*$")


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
            # majuscula de la începutul unei părți (după cratimă) nu e brand:
            # brand = majusculă internă într-o parte (SlashGear, iPhone)
            brand = any(c.isupper() for p in token.split("-") for c in p[1:])
            if (not la_inceput[m.start()] or token.isupper() or brand
                    or _comun.pliaza(token) in nume):
                continue
        if any(len(p) >= LUNGIME_MINIMA for p in token.split("-")):
            examinate.add(_comun.pliaza(token))
        # termenul întreg (ex. `cold-pressed`) din lexicon sau --allow, înainte de
        # împărțirea pe părți; părțile separate se pot scoate și ele
        if _comun.pliaza(token) in lexicon or _comun.pliaza(token) in allow:
            continue
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
        dictionar = valoare("--dictionar")
    except ValueError as e:
        print(f"eroare: {e}", file=sys.stderr)
        return 2
    cu_sugestii = "--sugestii" in argv
    if dictionar is not None and not cu_sugestii:
        print("eroare: --dictionar se folosește doar împreună cu --sugestii",
              file=sys.stderr)
        return 2
    if dictionar is not None and not dictionar.strip():
        print("eroare: --dictionar cere un nume sau o cale nevidă",
              file=sys.stderr)
        return 2
    if dictionar is None:
        dictionar = "ro_RO"
    optiuni_cu_valoare = {"--lexicon", "--allow", "--dictionar"}
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
        except (OSError, EOFError, UnicodeDecodeError, zlib.error) as e:
            print(f"eroare: lexiconul {cale_lexicon} nu poate fi citit ({e}); "
                  "vezi --lexicon / SCRIE_RO_LEXICON", file=sys.stderr)
            return 2
        try:
            allow = incarca_allow(cale_allow) if cale_allow else frozenset()
        except (OSError, EOFError, UnicodeDecodeError) as e:
            print(f"eroare: fișierul --allow {cale_allow} nu poate fi citit ({e})",
                  file=sys.stderr)
            return 2
        allow = allow | incarca_completari(cale_lexicon)
    except (OSError, EOFError, UnicodeDecodeError, zlib.error) as e:
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
    # Rezolvăm toate sugestiile ÎNAINTE de tipărit: o eroare a motorului nu
    # trebuie să lase un raport pe jumătate printat (succes parțial).
    sugestii = {}
    if cu_sugestii:
        forme = []
        vazute = set()
        for g in afisate:
            if g["parte"] not in vazute:
                vazute.add(g["parte"])
                forme.append(g["parte"])
        try:
            sugestii = _hunspell.sugereaza(forme, dictionar=dictionar)
        except _hunspell.EroareHunspell as e:
            print(f"eroare: sugestiile nu au putut fi obținute: {e}",
                  file=sys.stderr)
            return 2
    for g in afisate:
        sufix = f" x{g['nr']}" if g["nr"] > 1 else ""
        print(f"important|cuvant_de_verificat|L{g['linie']}|{g['afisat']}{sufix}"
              f"|→ {DEXONLINE}{g['parte'].lower()}")
        if cu_sugestii:
            variante = sugestii.get(g["parte"], [])
            print(f"sugestii|L{g['linie']}|{g['afisat']}|"
                  + (" / ".join(variante) if variante else "fără sugestii"))
    if len(elemente) > len(afisate):
        print(f"mai_sunt|{len(elemente) - len(afisate)} forme neafișate (--tot)")
    print(f"---\ntotal={len(elemente)} forme de verificat | {cuvinte} cuvinte | "
          f"lexicon={len(lexicon)} forme")
    print("nota: lipsa din lexicon nu e verdict. Verifică forma, lema și sensul "
          "în sursele permise; nu aplica automat sugestiile — ele "
          "nu confirmă nici existența, nici sensul.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
