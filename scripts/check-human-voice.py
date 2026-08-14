#!/usr/bin/env python3
"""Verifică prudent semnalele mecanice care slăbesc vocea umană.

Nu decide dacă un text a fost scris de AI și nu rescrie. Semnalele sunt indicii
pentru o lectură în context; excepția este contaminarea/placeholder-ele, care
blochează livrarea.

Usage:
    check-human-voice.py <fisier_sau_->
    check-human-voice.py <fisier> --json
    check-human-voice.py --help

Exit codes:
    0 = fără semnale
    1 = semnale de revizuit sau blocere
    2 = eroare de input
"""
import json
import re
import sys

import _comun

SCOR_MAXIM = 30
# Categoriile A-J sunt contractul extern. `subcategorie` păstrează motivul
# mecanic fără să fragmenteze calculul scorului pe zece categorii.
REGULI = (
    ("A", "filler", "minor", 2, r"\b(adev[aă]rul e c[aă]|hai s[aă](?: fim sinceri)?|s[aă] l[aă]murim|merit[aă] men[țt]ionat|s[aă] fim serio[sș]i|pe bune|ghici ce|[țt]ine minte)\b", "intră direct în idee"),
    ("B", "punchline", "important", 3, r"\b(asta e tot ce conteaz[aă]|at[aâ]t\.\s*$|f[aă]r[aă] doar [sș]i poate|regretele devin scumpe)\b", "păstrează doar dacă finalul adaugă sens"),
    ("C", "metafora_copywriter", "minor", 3, r"\b(busola (?:ta|noastr[aă])|puntea c[aă]tre succes|motorul (?:cre[șs]terii|succesului)|aprinde sc[aâ]nteia|piatra de temelie a succesului|farul (?:care|t[aă]u)|superputerea)\b", "păstrează metafora numai dacă e susținută de sens concret"),
    ("D", "autobiografie_nesustinuta", "important", 3, r"\b(din experien[țt]a mea|am [îi]nv[aă][țt]at (?:c[aă]|s[aă])|pot s[aă] spun din proprie experien[țt][aă])\b", "adaugă un episod, o dată sau o consecință verificabilă"),
    ("E", "structura_repetitiva", "minor", 3, r"\b([îi]n primul r[aâ]nd).{0,180}\b([îi]n al doilea r[aâ]nd).{0,180}\b([îi]n al treilea r[aâ]nd)\b", "renunță la scheletul repetitiv dacă ordinea nu contează"),
    ("F", "concluzie_redundanta", "minor", 3, r"\b(pe scurt|[îi]n esen[țt][aă]|r[aă]spunsul se vede singur|concluzia este clar[aă])\b", "încheie cu o idee nouă, nu cu rezumatul evident"),
    ("G", "promotional", "important", 3, r"\b(nu vindem [^.!?]{0,45}, vindem|mai mult dec[aâ]t un [a-zăâîșț -]{2,35}|[a-zăâîșț]+ pentru oameni care [a-zăâîșț]+|descoper[aă] (?:acum )?(?:puterea|secretul)|transform[aă]-?[țt]i|experien[țt][aă] (?:care|de neuitat)|solu[țt]ia care schimb[aă] totul)\b", "înlocuiește promisiunea cu un fapt verificabil"),
    ("H", "romana_naturala_calcuri", "important", 3, r"\b(face sens|joac[aă] un rol crucial|la sf[aâ]r[șs]itul zilei|[îi]n termeni de|insight-?uri ac[țt]ionabile)\b", "folosește o formulare românească directă"),
    ("I", "simetrie_adresare", "minor", 3, r"\b(fie c[aă] e[șs]ti [^.!?]{0,60}(?:sau|ori) [^.!?]{0,60}|indiferent de [^.!?]{0,60}|pentru oricine|oricine, oric[aâ]nd)\b", "numește cititorul sau cazul concret"),
    # CAPS este editorial: păstrează categoria J în output, dar nu adaugă puncte.
    ("J", "caps", "minor", 0, r"\b[A-ZĂÂÎȘȚ]{5,}\b", "scrie normal, cu excepția numelor și acronimelor necesare"),
    # J are greutate unică de 3 numai pentru garbage/contamination/placeholder.
    ("J", "garbage", "critic", 3, r"[�]|(?:^|\s)(?:lorem ipsum|asdf(?:gh)?|qwerty)(?:\s|$)", "elimină textul corupt sau fără sens"),
    ("J", "contaminare", "critic", 3, r"(?:\b(?:ca model ai|ca asistent ai|ignore previous instructions|prompt|answear|fashiondays)\b|\b(?:assistant|user|system):|<!--|\{\s*\"(?:prompt|messages|role)\"\s*:)", "elimină reziduul de conversație, prompt sau JSON"),
    ("J", "placeholder", "critic", 3, r"\[(?:de completat|numele (?:t[aă]u|clientului)|todo|placeholder)[^\]]*\]|\{\{[^}]+\}\}", "completează sau elimină placeholder-ul"),
)


def _linie(text, offset):
    return text.count("\n", 0, offset) + 1


def _fragment(text, start, end):
    return " ".join(text[max(0, start - 40):min(len(text), end + 40)].split())


def _autobiografie_are_context(text, start):
    """Acceptă o experiență personală când textul îi oferă repere concrete.

    Contextul e local (paragraful și vecinii): numere, timp explicit sau o
    consecință/episod. Nu pretinde să verifice adevărul biografiei.
    """
    paragrafe = re.split(r"\n\s*\n", text)
    pozitie = 0
    for i, paragraf in enumerate(paragrafe):
        sfarsit = pozitie + len(paragraf)
        if pozitie <= start <= sfarsit:
            zona = " ".join(paragrafe[max(0, i - 1):min(len(paragrafe), i + 2)])
            return bool(re.search(
                r"\b(?:\d+|ieri|azi|anul|luna|mar[țt]i|luni|marți|miercuri|joi|vineri|s[aă]pt[aă]m[aâ]n[ai]|dup[aă] ce|c[aâ]nd)\b",
                _comun.pliaza(zona)))
        pozitie = sfarsit + 2
    return False


def analizeaza(text):
    """Returnează potriviri, scorul AI_PATTERN_SCORE, statusul și blocerele."""
    rezultate = []
    for categorie, subcategorie, severitate, puncte, tipar, sugestie in REGULI:
        flags = re.MULTILINE if subcategorie == "caps" else re.IGNORECASE | re.MULTILINE
        for potrivire in re.finditer(tipar, text, flags):
            # Semnalul D este numai contextual. Reperele nu dovedesc biografia;
            # ele doar evită penalizarea mecanică a unei povești ancorate.
            if subcategorie == "autobiografie_nesustinuta" and _autobiografie_are_context(text, potrivire.start()):
                continue
            rezultate.append({
                "categorie": categorie, "categorie_cod": categorie,
                "subcategorie": subcategorie, "severitate": severitate,
                "puncte": puncte, "linie": _linie(text, potrivire.start()),
                "fragment": _fragment(text, potrivire.start(), potrivire.end()),
                "sugestie": sugestie, "offset": potrivire.start(),
            })

    # O categorie A-J poate costa cel mult greutatea ei. Mai multe tipuri J
    # păstrează citatele, fără să transforme scorul într-un detector de volum.
    categorii = {r["categorie"]: r["puncte"] for r in rezultate}
    scor = min(sum(categorii.values()), SCOR_MAXIM)
    blocere = sorted({r["subcategorie"] for r in rezultate
                      if r["subcategorie"] in {"garbage", "contaminare", "placeholder"}})
    if blocere or scor >= 11:
        status = "REWRITE"
    elif scor >= 6:
        status = "EDITED"
    else:
        status = "PASS"
    fabricate = any(r["categorie"] == "D" for r in rezultate)
    contamination = any(r["subcategorie"] in {"garbage", "contaminare", "placeholder"}
                        for r in rezultate)
    rezultate.sort(key=lambda r: r["offset"])
    return {"potriviri": rezultate, "ai_pattern_score": scor,
            "ai_pattern_maxim": SCOR_MAXIM, "status": status,
            "blockers": blocere, "fabricated_experience": fabricate,
            "contamination_found": contamination, "patterns_removed": 0}


def ca_json(rez):
    """Păstrează cheile lowercase existente și oferă contractul exact nou."""
    date = {k: v for k, v in rez.items() if k != "potriviri"} | {
        "potriviri": [{k: v for k, v in r.items() if k != "offset"}
                       for r in rez["potriviri"]]}
    return date | {
        "AI_PATTERN_SCORE": rez["ai_pattern_score"],
        "STATUS": rez["status"],
        "FABRICATED_EXPERIENCE": "YES" if rez["fabricated_experience"] else "NO",
        "CONTAMINATION_FOUND": "YES" if rez["contamination_found"] else "NO",
        "PATTERNS_REMOVED": rez["patterns_removed"],
    }


def tipareste(rez, detalii=True):
    if detalii:
        for r in rez["potriviri"]:
            print(f"{r['severitate']}|{r['categorie']}|{r['subcategorie']}|L{r['linie']}|{r['fragment']}|→ {r['sugestie']}")
    print(f"AI_PATTERN_SCORE={rez['ai_pattern_score']}/{rez['ai_pattern_maxim']}")
    print(f"STATUS={rez['status']}")
    print("FABRICATED_EXPERIENCE=" + ("YES" if rez["fabricated_experience"] else "NO"))
    print("CONTAMINATION_FOUND=" + ("YES" if rez["contamination_found"] else "NO"))
    print(f"PATTERNS_REMOVED={rez['patterns_removed']}")
    print("HUMAN_VOICE_BLOCKERS=" + (",".join(rez["blockers"]) or "niciunul"))


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    try:
        text = _comun.citeste_intrare(argv[0])
    except OSError as error:
        print(f"eroare: {error}", file=sys.stderr)
        return 2
    rez = analizeaza(text)
    if "--json" in argv:
        print(json.dumps(ca_json(rez), ensure_ascii=False, indent=1))
    else:
        tipareste(rez)
    return 1 if rez["potriviri"] else 0


if __name__ == "__main__":
    sys.exit(main())
