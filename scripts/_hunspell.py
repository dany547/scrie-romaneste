#!/usr/bin/env python3
"""Motor opțional de sugestii ortografice (hunspell) pentru check-cuvinte.py.

NU e autocorectare și NU e verdict. Sugestiile sunt doar variante grafice
propuse de un dicționar extern (Rospell / ro_RO etc.); sensul formei rămâne
de verificat în sursele permise, prin revizuire contextuală. Textul de
intrare nu se modifică și nu se scrie niciodată aici.

API:
    sugereaza(forme, dictionar='ro_RO') -> dict[str, list[str]]

Folosește numai executabilul local `hunspell` din PATH (shutil.which), un
singur proces per lot, cu protocolul ispell `-a` verificat în proba nativă:
o formă pe linie cu prefix `^` (input literal), `-i UTF-8`, `-d <dicționar>`,
LC_ALL=C.UTF-8. Răspunsurile, în ordinea inputului:

    & cuvanta 3 0: sug1, sug2, sug3   formă necunoscută, cu sugestii
    ? cuvanta 1 0: sug1                aceeași structură ca & (a doua trecere)
    # cuvanta 0                        formă necunoscută, fără sugestii
    *  / + lema / -                    formă recunoscută (nu înseamnă „sens corect”)

Bannerul e `@(#) International Ispell Version ...` sau `Hunspell x.y.z`;
restul liniilor necunoscute înseamnă output inconsistent → EroareHunspell.
Mesajele de eroare nu conțin dump brut din stderr-ul procesului. Fără rețea,
fără fișiere temporare, doar stdlib (Python 3.9+).
"""
import os
import re
import shutil
import subprocess

__all__ = ["EroareHunspell", "sugereaza"]

TIMP_LIMITA = 5        # secunde per lot; altfel verificatorul stă după text
MAX_SUGESTII = 5
LUNGIME_MAXIMA_FORMA = 64

# & cuvant 3 0: sug1, sug2, sug3   și   ? cuvant 1 0: sug1
# (cuvânt, număr sugestii, offset, listă; aceleași două forme de răspuns)
_SUGESTII = re.compile(r"^[&?]\s+(?P<cuvant>\S+)\s+(?P<cateva>\d+)\s+\d+\s*:\s*(?P<lista>.*)$")
# # cuvant 0   (necunoscut, fără sugestii)
_FARA_SUGESTII = re.compile(r"^#\s+(?P<cuvant>\S+)\s+(?P<cateva>\d+)\s*$")
# banner de versiune/encodare, permis doar înaintea primului răspuns
_BANNER = re.compile(r"^(@\(#\) |Hunspell\b|HUNSPELL_VERSION\b|Using encoding\b)")

_FOLD = str.maketrans({
    "ă": "a", "â": "a", "î": "i", "ș": "s", "ț": "t",
    "Ă": "a", "Â": "a", "Î": "i", "Ș": "s", "Ț": "t",
    "ş": "s", "ţ": "t", "Ş": "s", "Ţ": "t",
})


class EroareHunspell(Exception):
    """Motorul sau dicționarul nu a putut fi folosit; mesajul e de prezentat."""


def _pliaza(text):
    """Fold diacritic-insensibil (comparăm ecoul hunspell cu forma cerută)."""
    return text.translate(_FOLD).casefold()


def _verifica_forma(forma):
    if not isinstance(forma, str) or not forma:
        raise EroareHunspell("formele interogate trebuie să fie șiruri nevide")
    if len(forma) > LUNGIME_MAXIMA_FORMA:
        raise EroareHunspell(
            f"formă prea lungă pentru interogare ({len(forma)} caractere)")
    # isalpha() exclude newline, NUL, cifre, spațiu și orice caracter de
    # protocol (`&`, `?`, `#`, `^`, `+`, `-`): se acceptă doar litere.
    if not forma.isalpha():
        raise EroareHunspell(
            f"formă invalidă pentru hunspell (se acceptă doar litere): "
            f"{forma[:20]!r}")


def _verifica_dictionar(dictionar):
    if not isinstance(dictionar, str) or not dictionar.strip():
        raise EroareHunspell("numele dicționarului nu poate fi gol")
    if any(ord(c) < 32 or ord(c) == 127 for c in dictionar):
        raise EroareHunspell("numele dicționarului conține caractere de control")
    if dictionar.startswith("-"):
        raise EroareHunspell("numele dicționarului nu poate începe cu '-'")


def _lista_variante(text):
    """Split la virgulă, fără duplicate, maximum MAX_SUGESTII; curăț doar spațiile."""
    variante = []
    for bucata in text.split(","):
        b = bucata.strip()
        if not b or b in variante:
            continue
        variante.append(b)
    return variante[:MAX_SUGESTII]


def _ruleaza(binar, forme, dictionar):
    intrare = "\n".join("^" + forma for forma in forme) + "\n"
    mediu = dict(os.environ, LC_ALL="C.UTF-8")
    try:
        proces = subprocess.run(
            [binar, "-a", "-i", "UTF-8", "-d", dictionar],
            input=intrare, capture_output=True, text=True,
            encoding="utf-8", errors="strict", timeout=TIMP_LIMITA,
            env=mediu, shell=False)
    except subprocess.TimeoutExpired:
        raise EroareHunspell(
            f"hunspell nu a răspuns în {TIMP_LIMITA} secunde "
            f"(lot de {len(forme)} forme)") from None
    except UnicodeDecodeError:
        raise EroareHunspell("hunspell a scos text care nu e UTF-8 valid") from None
    except OSError as e:
        raise EroareHunspell(
            f"hunspell nu a putut fi pornit "
            f"({e.strerror or e.__class__.__name__})") from None
    if proces.returncode != 0:
        # Fără dump brut din stderr-ul procesului; indiciul cel mai uzual:
        raise EroareHunspell(
            f"hunspell a ieșit cu codul {proces.returncode}; verifică dacă "
            f"dicționarul '{dictionar}' e instalat (hunspell -D)")
    return proces.stdout


def _decodeaza(stdout):
    """Mock-urile pot întoarce bytes chiar cu text=True; gestionez ambele."""
    if isinstance(stdout, bytes):
        try:
            return stdout.decode("utf-8")
        except UnicodeDecodeError:
            raise EroareHunspell(
                "hunspell a scos text care nu e UTF-8 valid") from None
    if isinstance(stdout, str):
        return stdout
    raise EroareHunspell("ieșire hunspell de un tip neașteptat")


def _verifica_ecoul(cuvant_ecou, forme, cate_raspunsuri):
    """Ecoul liniei &/?/# trebuie să fie forma cerută pe poziția respectivă."""
    if cate_raspunsuri >= len(forme):
        raise EroareHunspell("hunspell a dat mai multe răspunsuri decât forme")
    if _pliaza(cuvant_ecou) != _pliaza(forme[cate_raspunsuri]):
        raise EroareHunspell(
            f"răspuns hunspell neașteptat pentru '{forme[cate_raspunsuri]}' "
            f"(ecou '{cuvant_ecou}')")


def _parseaza(iesire, forme):
    raspunsuri = []  # câte o listă de sugestii pe formă, în ordinea inputului
    for linie in _decodeaza(iesire).splitlines():
        linie = linie.strip()
        if not linie:
            continue
        m = _SUGESTII.match(linie)
        if m:
            _verifica_ecoul(m["cuvant"], forme, len(raspunsuri))
            brute = [b for b in (x.strip() for x in m["lista"].split(",")) if b]
            if len(brute) < int(m["cateva"]):
                raise EroareHunspell(
                    f"ieșire trunchiată: {m['cateva']} sugestii anunțate, "
                    f"{len(brute)} primite")
            raspunsuri.append(_lista_variante(m["lista"]))
            continue
        m = _FARA_SUGESTII.match(linie)
        if m:
            _verifica_ecoul(m["cuvant"], forme, len(raspunsuri))
            raspunsuri.append([])
            continue
        if linie in ("*", "+", "-") or linie.startswith("+ "):
            # Recunoscut de dicționarul extern: listă goală, nu confirmare de
            # sens (lexiconul nostru și dicționarul extern pot diferi oricum).
            raspunsuri.append([])
            continue
        if not raspunsuri and _BANNER.match(linie):
            continue  # doar banner-ul de versiune, înainte de primul răspuns
        raise EroareHunspell(
            f"ieșire malformată de la hunspell (rând neașteptat după "
            f"{len(raspunsuri)} răspunsuri)")
    if len(raspunsuri) != len(forme):
        raise EroareHunspell(
            f"hunspell a dat {len(raspunsuri)} răspunsuri pentru "
            f"{len(forme)} forme; output inconsistent")
    return dict(zip(forme, raspunsuri))


def sugereaza(forme, dictionar="ro_RO"):
    """Dict {formă: [maximum 5 sugestii]}; formele recunoscute au listă goală.

    `forme` = lista formelor originale (cu diacritice); se deduplică păstrând
    ordinea. Listă goală → {} fără niciun proces. Nimic din aceste funcții nu
    aplică sugestii și nu scrie textul de intrare.
    """
    unice = []
    vazute = set()
    for forma in forme:
        _verifica_forma(forma)
        if forma not in vazute:
            vazute.add(forma)
            unice.append(forma)
    if not unice:
        return {}
    _verifica_dictionar(dictionar)
    binar = shutil.which("hunspell")
    if binar is None:
        raise EroareHunspell(
            "executabilul 'hunspell' nu e în PATH; instalează-l sau rulează "
            "fără --sugestii")
    return _parseaza(_ruleaza(binar, unice, dictionar), unice)
