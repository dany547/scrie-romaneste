#!/usr/bin/env python3
"""Verifică respectarea best-practices SEO/GEO de bază într-un text Markdown/HTML.

Proiectat după principiile AXI (axi.md) pentru CLI-uri agent-ergonomice:
output compact, agregate precalculate, stare goală explicită, exit code
ca semnal de stare, --help minimal.

Verifică:
    - un singur H1
    - fără sărituri de nivel de heading (H1 -> H3 fără H2)
    - fără keyword stuffing (aceeași frază de 3+ cuvinte repetată excesiv)
    - scanabilitate: text lung fără nicio listă/heading
    - secțiuni prea lungi între heading-uri (citabilitate GEO)
    - diacritice în URL-uri/slug-uri (trebuie transliterate ASCII)
    - sedilă (ş/ţ) în loc de virgulă (ș/ț)

Usage:
    check-seo.py <fisier_sau_->
    check-seo.py --help

Exit codes:
    0 = nicio problemă găsită
    1 = probleme găsite
    2 = eroare de input
"""
import re
import sys
from collections import Counter

MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
HTML_HEADING = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
LISTA = re.compile(r"^\s*([-*+]|\d+\.)\s+", re.MULTILINE)

LUNGIME_MIN_PENTRU_SCANABILITATE = 1500

# Secțiunile de 120-180 de cuvinte între heading-uri se citează cel mai des în
# motoarele generative. Pragul e permisiv intenționat: semnalăm doar blocurile
# clar prea mari, nu abaterile de la optim.
CUVINTE_MAX_PER_SECTIUNE = 400

SEDILA = re.compile(r"[şţŞŢ]")
DIACRITICE = "ăâîșțĂÂÎȘȚşţŞŢ"
# URL-uri în markdown, HTML sau text simplu
URL = re.compile(r"(?:\]\(|href=[\"']|https?://)([^\s\"'()<>]+)")


def extrage_headinguri(text):
    headinguri = [(len(h), t.strip()) for h, t in MARKDOWN_HEADING.findall(text)]
    if not headinguri:
        headinguri = [(int(n), re.sub(r"<[^>]+>", "", t).strip())
                       for n, t in HTML_HEADING.findall(text)]
    return headinguri


def sectiuni_prea_lungi(text):
    """Blocuri de text între două heading-uri markdown, peste pragul de citabilitate."""
    pozitii = [(m.start(), m.group(2).strip()) for m in MARKDOWN_HEADING.finditer(text)]
    if not pozitii:
        return []

    probleme = []
    for i, (start, titlu) in enumerate(pozitii):
        end = pozitii[i + 1][0] if i + 1 < len(pozitii) else len(text)
        corp = text[start:end]
        corp = corp[corp.find("\n") + 1:] if "\n" in corp else ""
        n = len(corp.split())
        if n > CUVINTE_MAX_PER_SECTIUNE:
            probleme.append(("sectiune_lunga", f"{n} cuvinte", titlu[:40]))
    return probleme


def verifica(text):
    probleme = []
    headinguri = extrage_headinguri(text)

    h1_count = sum(1 for nivel, _ in headinguri if nivel == 1)
    if h1_count == 0 and headinguri:
        probleme.append(("heading", "lipsă H1", "niciun heading de nivel 1 găsit"))
    elif h1_count > 1:
        probleme.append(("heading", f"{h1_count} H1", "mai mult de un H1 în document"))

    nivel_anterior = None
    for nivel, titlu in headinguri:
        if nivel_anterior is not None and nivel > nivel_anterior + 1:
            probleme.append((
                "heading",
                f"salt H{nivel_anterior}->H{nivel}",
                titlu[:40],
            ))
        nivel_anterior = nivel

    cuvinte = re.findall(r"\b[\wăâîșțĂÂÎȘȚ]+\b", text.lower())
    fraze_3 = [" ".join(cuvinte[i:i + 3]) for i in range(len(cuvinte) - 2)]
    contor = Counter(fraze_3)
    prag_stuffing = max(4, len(cuvinte) // 200)
    for fraza, n in contor.items():
        if n >= prag_stuffing and len(fraza) > 8:
            probleme.append(("keyword_stuffing", f"x{n}", fraza))

    for m in SEDILA.finditer(text):
        start = max(0, m.start() - 20)
        probleme.append((
            "sedila",
            m.group(0),
            text[start:m.end() + 20].replace("\n", " ").strip(),
        ))
        if len(probleme) > 200:  # text integral cu sedilă — un semnal e destul
            break

    for m in URL.finditer(text):
        url = m.group(1)
        gasite = sorted({c for c in url if c in DIACRITICE})
        if gasite:
            probleme.append(("url_diacritice", "".join(gasite), url[:60]))

    probleme.extend(sectiuni_prea_lungi(text))

    are_lista = bool(LISTA.search(text))
    if len(text) > LUNGIME_MIN_PENTRU_SCANABILITATE and not headinguri and not are_lista:
        probleme.append((
            "scanabilitate",
            f"{len(text)} caractere",
            "text lung fără heading-uri sau liste",
        ))

    return probleme


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

    probleme = verifica(text)

    if not probleme:
        print("0 probleme SEO găsite")
        return 0

    for categorie, detaliu, context in probleme:
        print(f"{categorie}|{detaliu}|{context}")

    agregate = Counter(categorie for categorie, _, _ in probleme)
    rezumat = ", ".join(f"{c}={n}" for c, n in sorted(agregate.items()))
    print(f"---\ntotal={len(probleme)} ({rezumat})")

    return 1


if __name__ == "__main__":
    sys.exit(main())
