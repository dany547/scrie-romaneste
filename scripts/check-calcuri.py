#!/usr/bin/env python3
"""Colocări suspecte (verb + obiect pe aceeași propoziție), de verificat — nu verdicte.

Registry static: `references/limba/calcuri.json` (lângă skill). Fiecare regulă
leagă forme pliate ale unui verb de forme pliate ale obiectului lui; scanarea
semnalizează perechi pe ACEEAȘI PROPOZIȚIE, la cel mult `--fereastra` cuvinte
distanță (implicit 10). E o fereastră pe cuvinte, nu sintaxă: scriptul NU
detectează relații de dependență, acord sau sens — perechea e suspectă de calc
și se recitește în context, atât. Un semnal nu e automat o eroare.

Nu prinde: termenii izolați (fără pereche în propoziție), perechile peste
graniță de propoziție (punct/semn de exclamare/întrebare/două puncte, rând gol,
început de element de listă sau heading), forma ambiguă «frâna» acoperită doar
cu marcă de infinitiv/viitor/modal în față («a frâna», «pot frâna» —
substantivul «frâna» rămâne tăcut), «încărcătura» (sarcina transportată, nu
procesul) și construcțiile legitime trecute la excepții în registry («sistem
de frânare», substantivul «încărcător»). Fals pozitive acceptate și
documentate: propoziții cu frânare fizică lângă «încărcare» («Camionul
frânează la rampa de încărcare») — de aceea sugestia e neutră, de recitit în
context, fără să prezinte un calc sau un site. Preferă tăcerea la falsuri
negative: propoziții împărțite greșit (abrevieri de tip «ex.») pot ascunde
perechi reale — limită acceptată, deterministă.

Registry-ul crește doar cu colocări verificate manual, în surse permise
(procedura: `references/limba/revizie-contextuala.md`), nu automat din corpus;
fără date de client.

Usage:
    check-calcuri.py <fisier_sau_->
    check-calcuri.py <fisier> --fereastra N    # cuvinte max între verb și obiect (implicit 10, 0-99)
    check-calcuri.py <fisier> --fereastra=N    # forma cu «=» e acceptată
    check-calcuri.py <fisier> --registry cale  # alt registry JSON (și --registry=cale)

Argumentele necunoscute sunt refuzate cu exit 2, nu ignorate în tăcere.

Raport (ca la celelalte scripturi; `minor` = semnal de recitire, nu eroare):
    minor|colocare_de_verificat|L<linie>|<fragment>|→ <sugestie>
    ---
    total=N colocări de verificat | <cuvinte> cuvinte
    nota: perechea e de recitit, nu e calc confirmat; ...

O singură pereche per propoziție și per regulă (cea mai apropiată). Fragmentul
poate conține `|` — citește-l ca text, nu-l parsă mecanic.

Exit codes:
    0 = nicio colocare de verificat
    1 = cel puțin o colocare de verificat (caz normal, nu eșec)
    2 = eroare de input sau registry lipsă/defect
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import _comun

REGISTRY_IMPLICIT = (Path(__file__).resolve().parent.parent
                     / "references" / "limba" / "calcuri.json")
FEREASTRA_IMPLICIT = 10

# Un interval de propoziție se închide la: punctuație de final (și «:») urmată
# de spațiu/sfârșit, rând gol (graniță de paragraf), și rând nou care începe un
# element de listă sau un heading. Un rând nou simplu NU închide: textul e
# wrapped, iar propoziția continuă pe rândul următor.
_LIMITA = re.compile(
    r"[.!?…:]+[»”’)]*(?:\s|$)"
    r"|\n[ \t]*\n"
    r"|\n(?=[ \t]*(?:[-*+>#•]|\d+[.)])[ \t])")


def _verifica_pliata(cale, nume, cheie, valoare, regex=False):
    """Formele și pattern-urile din registry trebuie să fie deja pliate:
    minuscule, fără diacritice — pe textul pliat n-ar potrivi niciodată."""
    if _comun.pliaza(valoare) != valoare:
        raise ValueError(f"registry-ul {cale}: regula {nume}: {cheie} trebuie să fie "
                         f"pliat și cu minuscule (fără diacritice): {valoare!r}")
    if not regex and not re.fullmatch(r"[a-z]+", valoare):
        raise ValueError(f"registry-ul {cale}: regula {nume}: {cheie} trebuie să "
                         f"conțină doar litere mici: {valoare!r}")


def _context_re(stem, context):
    r"""Contextul cere infinitivul exact, nu substantive derivate din stem."""
    return re.compile(r"\b(?:" + _comun.spatii_flexibile(context)
                      + r")\s+(\b" + re.escape(stem) + r"(?:\b|r\b))")


def incarca_registry(cale):
    """Validare strictă, cu mesaje pe care le poate citi cineva la terminal.
    La ieșire, fiecare regulă are și regex-urile precompilate (cheile `_…`):
    un regex invalid iese la încărcare, nu la prima scanare."""
    try:
        with open(cale, "r", encoding="utf-8-sig") as f:
            date = json.load(f)
    except OSError as e:
        raise ValueError(f"registry-ul {cale} nu poate fi citit: {e}")
    except UnicodeDecodeError as e:
        raise ValueError(f"registry-ul {cale} nu e UTF-8 valid: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"registry-ul {cale} nu e JSON valid: {e}")
    if not isinstance(date, dict):
        raise ValueError(f"registry-ul {cale} trebuie să fie un obiect JSON")
    versiune = date.get("schema_version")
    if isinstance(versiune, bool) or not isinstance(versiune, int) or versiune != 1:
        raise ValueError(f"registry-ul {cale}: schema_version trebuie să fie numărul 1")
    reguli = date.get("reguli")
    if not isinstance(reguli, list) or not reguli:
        raise ValueError(f"registry-ul {cale} nu are nicio regulă (cheia «reguli»)")
    for regula in reguli:
        if not isinstance(regula, dict):
            raise ValueError(f"registry-ul {cale}: regulile trebuie să fie obiecte")
        nume = regula.get("id", "?")
        for cheie in ("id", "sugestie"):
            valoare = regula.get(cheie)
            if not isinstance(valoare, str) or not valoare.strip():
                raise ValueError(f"registry-ul {cale}: regula {nume} nu are {cheie} nevid")
        for cheie in ("verb_stem", "obiect_stem"):
            valori = regula.get(cheie)
            if (not isinstance(valori, list) or not valori
                    or not all(isinstance(v, str) and v.strip() for v in valori)):
                raise ValueError(f"registry-ul {cale}: regula {nume} "
                                 f"nu are {cheie} cu cel puțin o formă")
            for v in valori:
                _verifica_pliata(cale, nume, cheie, v)
        for cheie in ("exceptii_verb", "exceptii_obiect"):
            valori = regula.get(cheie, [])
            if not isinstance(valori, list) or not all(
                    isinstance(v, str) for v in valori):
                raise ValueError(f"registry-ul {cale}: regula {nume} are {cheie} invalid")
            for v in valori:
                _verifica_pliata(cale, nume, cheie, v, regex=True)
        contexte = regula.get("verb_contexte", [])
        if not isinstance(contexte, list):
            raise ValueError(f"registry-ul {cale}: regula {nume} are verb_contexte invalid")
        compilate = []
        for intrare in contexte:
            if not isinstance(intrare, dict):
                raise ValueError(f"registry-ul {cale}: regula {nume}: verb_contexte "
                                 "trebuie să fie obiecte cu stem + contexte")
            stem = intrare.get("stem")
            if not isinstance(stem, str) or not stem.strip():
                raise ValueError(f"registry-ul {cale}: regula {nume}: o intrare "
                                 "verb_contexte nu are stem nevid")
            _verifica_pliata(cale, nume, "verb_contexte.stem", stem)
            lista = intrare.get("contexte")
            if (not isinstance(lista, list) or not lista
                    or not all(isinstance(c, str) and c.strip() for c in lista)):
                raise ValueError(f"registry-ul {cale}: regula {nume}: stem-ul {stem!r} "
                                 "nu are contexte nevide")
            for c in lista:
                _verifica_pliata(cale, nume, "verb_contexte.contexte", c, regex=True)
            try:
                compilate.extend(_context_re(stem, c) for c in lista)
            except re.error as eroare:
                raise ValueError(f"registry-ul {cale}: regex invalid în {nume}: {eroare}")
        try:
            for e in (regula.get("exceptii_verb", [])
                      + regula.get("exceptii_obiect", [])):
                re.compile(_comun.spatii_flexibile(e))
        except re.error as eroare:
            raise ValueError(f"registry-ul {cale}: regex invalid în {nume}: {eroare}")
        regula["_verb_re"] = _stem_re(regula["verb_stem"])
        regula["_obiect_re"] = _stem_re(regula["obiect_stem"])
        regula["_exceptii_verb_re"] = _exceptii_re(regula.get("exceptii_verb", []))
        regula["_exceptii_obiect_re"] = _exceptii_re(regula.get("exceptii_obiect", []))
        regula["_verb_context_re"] = compilate
    return reguli


def _stem_re(stems):
    """Formele se potrivesc ca prefix la început de cuvânt, pe textul pliat."""
    return re.compile(r"\b(?:" + "|".join(sorted(re.escape(s) for s in stems))
                      + r")\w*")


def _exceptii_re(exceptii):
    return [re.compile(_comun.spatii_flexibile(e), re.IGNORECASE) for e in exceptii]


def _spanuri(pliat, regex, exceptii):
    """Potriviri (început, sfârșit) care nu se suprapun cu nicio excepție."""
    ex_spanuri = []
    for e in exceptii:
        ex_spanuri.extend(m.span() for m in e.finditer(pliat))
    rezultat = []
    for m in regex.finditer(pliat):
        s, e = m.span()
        if any(es < e and s < ee for es, ee in ex_spanuri):
            continue
        rezultat.append((s, e))
    return rezultat


def _spanuri_contextuale(pliat, compilate, exceptii):
    """Forme care contează ca verb doar cu context în față (grupa 1)."""
    ex_spanuri = []
    for e in exceptii:
        ex_spanuri.extend(m.span() for m in e.finditer(pliat))
    rezultat = []
    for regex in compilate:
        for m in regex.finditer(pliat):
            s, e = m.start(1), m.end(1)
            if any(es < e and s < ee for es, ee in ex_spanuri):
                continue
            rezultat.append((s, e))
    return rezultat


def _intervale(pliat):
    """Intervale (start, end) ale propozițiilor, după granițele din _LIMITA."""
    margini = [0]
    for m in _LIMITA.finditer(pliat):
        margini.append(m.start())
        margini.append(m.end())
    margini.append(len(pliat))
    return list(zip(margini[0::2], margini[1::2]))


def _cuvinte_intre(pliat, span1, span2):
    stanga = min(span1[1], span2[1])
    dreapta = max(span2[0], span1[0])
    return len(re.findall(r"\w+", pliat[stanga:dreapta]))


def gaseste(text, reguli, fereastra):
    """Listă de semnale (linie, fragment, sugestie), sortate pe text.

    O singură pereche per propoziție și per regulă: cea mai apropiată, cu
    egalitate zdrobită pe poziție (determinist, indiferent de ordinea din
    registry).
    """
    text = unicodedata.normalize("NFC", text)
    pliat = _comun.pliaza(text)
    intervale = _intervale(pliat)
    semnale = []
    for regula in reguli:
        verbe = _spanuri(pliat, regula["_verb_re"],
                         regula["_exceptii_verb_re"])
        verbe += _spanuri_contextuale(pliat, regula["_verb_context_re"],
                                      regula["_exceptii_verb_re"])
        obiecte = _spanuri(pliat, regula["_obiect_re"],
                           regula["_exceptii_obiect_re"])
        alese = {}
        for vspan in verbe:
            for ospan in obiecte:
                if vspan[0] < ospan[1] and ospan[0] < vspan[1]:
                    continue  # același span, nu e pereche
                if not any(a <= vspan[0] < b and a <= ospan[0] < b
                           for a, b in intervale):
                    continue  # propoziții separate: tace
                distanta = _cuvinte_intre(pliat, vspan, ospan)
                if distanta > fereastra:
                    continue  # perechi prea depărtate: tace
                inceput = min(vspan[0], ospan[0])
                sfarsit = max(vspan[1], ospan[1])
                cheie = next(i for i, (a, b) in enumerate(intervale)
                             if a <= vspan[0] < b)
                anterioara = alese.get(cheie)
                if anterioara is None or (distanta, inceput) < (
                        anterioara[0], anterioara[1]):
                    alese[cheie] = (distanta, inceput, sfarsit, regula["sugestie"])
        for _dist, inceput, sfarsit, sugestie in alese.values():
            context_s = max(0, inceput - _comun.CONTEXT_CHARS)
            context_e = min(len(text), sfarsit + _comun.CONTEXT_CHARS)
            semnale.append({
                "offset": inceput,
                "linie": text.count("\n", 0, inceput) + 1,
                "fragment": " ".join(text[context_s:context_e].split()),
                "sugestie": sugestie,
            })
    semnale.sort(key=lambda s: s["offset"])
    return semnale


_FLAGURI = ("--fereastra", "--registry")


def _parseaza_argumente(argv):
    """Poziționale, `--flag valoare` și `--flag=valoare`; necunoscute sau fără
    valoare → ValueError (ieșire cu 2, nu tăcere)."""
    arata_help = False
    valori = {"--fereastra": None, "--registry": None}
    pozitionale = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("-h", "--help"):
            arata_help = True
        elif arg.startswith("--"):
            nume, egal, valoare = arg.partition("=")
            if nume not in _FLAGURI:
                raise ValueError(f"argument necunoscut: {arg}")
            if not egal:
                if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
                    raise ValueError(f"{nume} cere o valoare")
                valoare = argv[i + 1]
                i += 1
            if not valoare:
                raise ValueError(f"{nume} cere o valoare nevidă")
            valori[nume] = valoare
        elif arg.startswith("-") and arg != "-":
            raise ValueError(f"argument necunoscut: {arg}")
        else:
            pozitionale.append(arg)
        i += 1
    return arata_help, valori, pozitionale


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        arata_help, valori, pozitionale = _parseaza_argumente(argv)
    except ValueError as e:
        print(f"eroare: {e}", file=sys.stderr)
        return 2
    if arata_help:
        print(__doc__)
        return 0
    if len(pozitionale) != 1:
        print("eroare: cere exact un fișier (sau '-' pentru stdin)",
              file=sys.stderr)
        return 2
    sursa = pozitionale[0]
    bruta_fereastra = valori["--fereastra"]
    if bruta_fereastra is None:
        fereastra = FEREASTRA_IMPLICIT
    else:
        try:
            fereastra = int(bruta_fereastra)
        except ValueError:
            print("eroare: --fereastra cere un număr întreg", file=sys.stderr)
            return 2
        if not 0 <= fereastra <= 99:
            print("eroare: --fereastra cere un număr între 0 și 99",
                  file=sys.stderr)
            return 2
    cale_registry = valori["--registry"] or REGISTRY_IMPLICIT

    try:
        text = _comun.citeste_intrare(sursa)
        reguli = incarca_registry(cale_registry)
    except (OSError, ValueError) as e:
        print(f"eroare: {e}", file=sys.stderr)
        return 2

    semnale = gaseste(text, reguli, fereastra)
    cuvinte = _comun.numara_cuvinte(unicodedata.normalize("NFC", text))
    if not semnale:
        print(f"0 colocări de verificat ({cuvinte} cuvinte)")
        return 0
    for s in semnale:
        print(f"minor|colocare_de_verificat|L{s['linie']}|{s['fragment']}"
              f"|→ {s['sugestie']}")
    total = ("1 colocare de verificat" if len(semnale) == 1
             else f"{len(semnale)} colocări de verificat")
    print(f"---\ntotal={total} | {cuvinte} cuvinte")
    print("nota: perechea e marcată pentru recitire, nu e calc confirmat; "
          "fereastra pe cuvinte nu vede sintaxa. Decizia o dă revizia "
          "contextuală (references/limba/revizie-contextuala.md), nu scriptul.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
