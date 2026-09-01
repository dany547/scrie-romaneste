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
    - registrul titlului: clickbait, șablon de agenție, etichetă, lungime,
      subtitluri plate

SEVERITATE FĂRĂ PUNCTAJ

Returnează tupluri (severitate, categorie, detaliu, context), ca restul
scripturilor. Severitatea e ghid de citire, nu contribuție la `scor_automat`:
SEO nu alimentează scorul, iar /13 rămâne neschimbat.

Alinierea la modelul comun s-a făcut când a apărut prima verificare care cere
judecată — detecția de registru în titlu. Faptele structurale (două H1, salt
de nivel, diacritice în slug) rămân fapte; clickbaitul, șablonul și eticheta
cer o lectură a fragmentului înainte de corecție.

    critic     — sedilă (normă, nu alegere)
    important  — heading, url_diacritice, keyword_stuffing, titlu_clickbait,
                 titlu_sablon
    minor      — sectiune_lunga, scanabilitate, titlu_lung, titlu_eticheta,
                 subtitluri_plate

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

import _comun

MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
HTML_HEADING = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
LISTA = re.compile(r"^\s*([-*+]|\d+\.)\s+", re.MULTILINE)
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
TITLU_META = re.compile(
    r"^(?:title|TITLE_RO)\s*[:=]\s*[\"']?(.+?)[\"']?\s*$",
    re.MULTILINE | re.IGNORECASE)
CUVANT = re.compile(r"\b[\wăâîșțĂÂÎȘȚ]+\b", re.IGNORECASE)
CUVANT_CAPS = re.compile(r"\b[\wĂÂÎȘȚŞŢ]+\b")

LUNGIME_MIN_PENTRU_SCANABILITATE = 1500

# Secțiunile de 120-180 de cuvinte între heading-uri se citează cel mai des în
# motoarele generative. Pragul e permisiv intenționat: semnalăm doar blocurile
# clar prea mari, nu abaterile de la optim.
CUVINTE_MAX_PER_SECTIUNE = 400

# <title> se taie în SERP pe lățime; 65 de caractere e pragul de recitire.
CARACTERE_MAX_TITLU = 65
CUVINTE_MAX_ETICHETA = 3
H2_SCURT_MAX_CUVINTE = 2
H2_PLATE_MIN = 3

SEDILA = re.compile(r"[şţŞŢ]")
DIACRITICE = "ăâîșțĂÂÎȘȚşţŞŢ"
# URL-uri în markdown, HTML sau text simplu
URL = re.compile(r"(?:\]\(|href=[\"']|https?://)([^\s\"'()<>]+)")

CLICKBAIT_FRAZE = (
    "nu-ti vine sa crezi",
    "te va soca",
    "te va surprinde",
    "ce a urmat",
    "motivul te va",
    "socant",
    "incredibil",
)
SABLON_FRAZE = (
    "ghidul suprem",
    "ghid suprem",
    "tot ce trebuie sa stii",
    "tot ce ai nevoie sa stii",
)
SABLON_TOP = re.compile(r"top\s+\d+\s+cele mai bune")


def extrage_headinguri(text):
    headinguri = [(len(h), t.strip()) for h, t in MARKDOWN_HEADING.findall(text)]
    if not headinguri:
        headinguri = [(int(n), re.sub(r"<[^>]+>", "", t).strip())
                       for n, t in HTML_HEADING.findall(text)]
    return headinguri


def cuvinte_din(text):
    return CUVANT.findall(text)


def extrage_titlu(text):
    """Primul H1 (markdown sau HTML); altfel frontmatter title: / TITLE_RO."""
    for nivel, titlu in extrage_headinguri(text):
        if nivel == 1 and titlu:
            return titlu
    cap = "\n".join(text.splitlines()[:20])
    fm = FRONTMATTER.match(text)
    if fm:
        cap = fm.group(1) + "\n" + cap
    m = TITLU_META.search(cap)
    if m:
        return m.group(1).strip().strip("\"'")
    return None


def verifica_titlu(titlu, headinguri):
    """Registrul titlului și al subtitlurilor. Fără titlu, apelantul sare."""
    probleme = []
    pliat = _comun.pliaza(titlu)

    for fraza in CLICKBAIT_FRAZE:
        if fraza in pliat:
            probleme.append(("important", "titlu_clickbait", fraza, titlu[:60]))
            break
    else:
        if titlu.count("!") >= 2:
            probleme.append(("important", "titlu_clickbait", "!!", titlu[:60]))
        else:
            for cuvant in CUVANT_CAPS.findall(titlu):
                litere = [c for c in cuvant if c.isalpha()]
                if len(litere) >= 4 and all(c.isupper() for c in litere):
                    probleme.append(
                        ("important", "titlu_clickbait", "CAPS", cuvant))
                    break

    if SABLON_TOP.search(pliat):
        probleme.append(("important", "titlu_sablon", "top N cele mai bune",
                         titlu[:60]))
    else:
        for fraza in SABLON_FRAZE:
            if fraza in pliat:
                probleme.append(
                    ("important", "titlu_sablon", fraza, titlu[:60]))
                break

    if len(titlu) > CARACTERE_MAX_TITLU:
        probleme.append(
            ("minor", "titlu_lung", f"{len(titlu)} caractere", titlu[:60]))

    n_cuvinte = len(cuvinte_din(titlu))
    if 0 < n_cuvinte <= CUVINTE_MAX_ETICHETA:
        probleme.append(
            ("minor", "titlu_eticheta", f"{n_cuvinte} cuvinte", titlu[:60]))

    h2 = [t for nivel, t in headinguri if nivel == 2]
    h2_scurte = [t for t in h2 if 0 < len(cuvinte_din(t)) <= H2_SCURT_MAX_CUVINTE]
    if len(h2_scurte) >= H2_PLATE_MIN:
        probleme.append((
            "minor",
            "subtitluri_plate",
            f"{len(h2_scurte)} H2 scurte",
            ", ".join(t[:30] for t in h2_scurte[:4]),
        ))

    return probleme


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
            probleme.append(("minor", "sectiune_lunga", f"{n} cuvinte", titlu[:40]))
    return probleme


def verifica(text):
    probleme = []
    headinguri = extrage_headinguri(text)

    h1_count = sum(1 for nivel, _ in headinguri if nivel == 1)
    if h1_count == 0 and headinguri:
        probleme.append(("important", "heading", "lipsă H1",
                         "niciun heading de nivel 1 găsit"))
    elif h1_count > 1:
        probleme.append(("important", "heading", f"{h1_count} H1",
                         "mai mult de un H1 în document"))

    nivel_anterior = None
    for nivel, titlu in headinguri:
        if nivel_anterior is not None and nivel > nivel_anterior + 1:
            probleme.append((
                "important",
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
            probleme.append(("important", "keyword_stuffing", f"x{n}", fraza))

    for m in SEDILA.finditer(text):
        start = max(0, m.start() - 20)
        probleme.append((
            "critic",
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
            probleme.append(("important", "url_diacritice", "".join(gasite), url[:60]))

    probleme.extend(sectiuni_prea_lungi(text))

    are_lista = bool(LISTA.search(text))
    if len(text) > LUNGIME_MIN_PENTRU_SCANABILITATE and not headinguri and not are_lista:
        probleme.append((
            "minor",
            "scanabilitate",
            f"{len(text)} caractere",
            "text lung fără heading-uri sau liste",
        ))

    titlu = extrage_titlu(text)
    if titlu:
        probleme.extend(verifica_titlu(titlu, headinguri))

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

    for severitate, categorie, detaliu, context in probleme:
        print(f"{severitate}|{categorie}|{detaliu}|{context}")

    agregate = Counter(categorie for _, categorie, _, _ in probleme)
    rezumat = ", ".join(f"{c}={n}" for c, n in sorted(agregate.items()))
    print(f"---\ntotal={len(probleme)} ({rezumat})")

    return 1


if __name__ == "__main__":
    sys.exit(main())
