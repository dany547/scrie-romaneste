#!/usr/bin/env python3
"""Scanează un text pentru clișee AI, romgleză și tranziții mecanice.

Proiectat după principiile AXI (axi.md) pentru CLI-uri agent-ergonomice:
output compact tip TOON, trunchiere de context, agregate precalculate,
stare goală explicită, exit code ca semnal de stare, --help minimal.

Usage:
    check-tipare.py <fisier_sau_->
    check-tipare.py --help

Exit codes:
    0 = text curat (0 potriviri)
    1 = potriviri găsite
    2 = eroare de input (fișier lipsă etc.)
"""
import re
import sys

CATEGORII = {
    "structura": [
        r"\bîn concluzie\b", r"\bprin urmare\b", r"\bde asemenea\b",
        r"\bpe de o parte\b.*\bpe de altă parte\b", r"\bîn plus\b",
        r"\bmai mult decât atât\b", r"\btotodată\b",
    ],
    "introduceri": [
        r"\bîn lumea (de astăzi|digitală|modernă)\b",
        r"\bîn era digitală\b", r"\bîn societatea modernă\b",
        r"\bde când lumea și pământul\b",
    ],
    "umpluturi": [
        r"\beste important de menționat că\b",
        r"\bmerită (precizat|subliniat) faptul că\b",
        r"\bîn acest articol\b", r"\bîn cele ce urmează\b",
    ],
    "vocabular_corporatist": [
        r"\brevoluționar\b", r"\bimpresionant\b", r"\bremarcabil\b",
        r"\bvibrant\b", r"\badoptă o abordare\b", r"\bse remarcă prin\b",
        r"\bschimbare de paradigmă\b", r"\bun pilon fundamental\b",
        r"\bo componentă esențială\b",
    ],
    "cuantificari_vagi": [
        r"\bo serie de\b", r"\bun număr semnificativ\b",
        r"\bo gamă largă de\b", r"\bo paletă largă de\b",
        r"\bun spectru larg de\b",
    ],
    "hedging": [
        r"\beste posibil ca\b", r"\bs-ar putea ca\b",
    ],
    "romgleza": [
        r"\bface sens\b", r"\bjoacă un rol crucial\b",
        r"\bla sfârșitul zilei\b", r"\bîn termeni de\b",
    ],
}

CONTEXT_CHARS = 40


def scaneaza(text):
    rezultate = []
    for categorie, tipare in CATEGORII.items():
        for tipar in tipare:
            for m in re.finditer(tipar, text, re.IGNORECASE):
                start = max(0, m.start() - CONTEXT_CHARS)
                end = min(len(text), m.end() + CONTEXT_CHARS)
                fragment = text[start:end].replace("\n", " ").strip()
                linie = text.count("\n", 0, m.start()) + 1
                rezultate.append((categorie, linie, fragment))
    return rezultate


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    sursa = argv[0]
    try:
        if sursa == "-":
            text = sys.stdin.read()
        else:
            with open(sursa, "r", encoding="utf-8") as f:
                text = f.read()
    except OSError as e:
        print(f"eroare: {e}", file=sys.stderr)
        return 2

    rezultate = scaneaza(text)

    if not rezultate:
        print("0 tipare AI găsite")
        return 0

    # output compact tip TOON: categorie|linie|fragment
    for categorie, linie, fragment in rezultate:
        print(f"{categorie}|L{linie}|{fragment}")

    agregate = {}
    for categorie, _, _ in rezultate:
        agregate[categorie] = agregate.get(categorie, 0) + 1
    total = len(rezultate)
    rezumat = ", ".join(f"{c}={n}" for c, n in sorted(agregate.items()))
    print(f"---\ntotal={total} ({rezumat})")

    return 1


if __name__ == "__main__":
    sys.exit(main())
