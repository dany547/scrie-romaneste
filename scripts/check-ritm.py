#!/usr/bin/env python3
"""Măsoară ritmul unui text: uniformitatea frazelor, a paragrafelor, structura.

Textul generat de model are fraze mult mai egale ca lungime decât cel scris de
om. Metrica utilă nu e lungimea medie — aceea e aproape identică — ci împrăștierea
(deviația standard și coeficientul de variație).

PRAGURI ȘI ÎNCREDEREA ÎN ELE

  deviatie / coeficient de variatie ....... încredere medie
      Din literatura de stilometrie: text uman std ~5.5 cuvinte/frază, text de
      model 2.6-3.5. Cifrele sunt derivate din corpusuri ENGLEZEȘTI de text
      enciclopedic. Româna are frază mai lungă (flexiune, subordonare), deci
      pragurile absolute în cuvinte sunt probabil deplasate în sus. Coeficientul
      de variație, fiind adimensional, se transferă mai bine decât deviația.

  banda 15-28 cuvinte ..................... încredere scăzută
      Circulă cifra „85% din frazele de model cad în banda asta", dar nu are
      sursă cu metodologie. Tratat ca indiciu, nu ca dovadă.

  uniformitatea paragrafelor .............. fără prag publicat
      Construit prin analogie cu frazele. Calibrează-l pe textele tale.

CALIBRARE PE ROMÂNĂ

Pragurile de mai sus sunt conservatoare: prind textul flagrant uniform, dar
lasă să treacă text mediu. Pe textele de test românești am măsurat coeficienți
de variație de 0,41-0,72 la proză scrisă de om și 0,12 la text de model — deci
distanța dintre cele două clase pare mai mare în română decât în engleză, iar
pragul care separă util e probabil mai sus de 0,16. Două texte nu sunt o
calibrare. Dacă ai un corpus propriu, măsoară-l și ridică pragurile.

Niciun număr de aici nu dovedește nimic singur. Detectoarele de acest tip
greșesc masiv pe scriitori non-nativi și pe registru formal — pe eseuri scrise
de non-nativi s-au raportat rate de fals pozitiv peste 60%. Un scor prost
înseamnă „merită recitit", nu „e scris de un model".

Usage:
    check-ritm.py <fisier_sau_->
    check-ritm.py <fisier> --scor       # doar scorul de semnale
    check-ritm.py --help

Exit codes:
    0 = ritm variat, fără semnale
    1 = semnale de uniformitate
    2 = eroare de input
"""
import re
import sys
import unicodedata

# Încredere medie — derivate din literatură, calibrate pe engleză.
CV_UNIFORM = 0.16          # sub -> suspect de uniform
CV_VARIAT = 0.22           # peste -> variație de tip uman
DEV_UNIFORM = 3.5          # cuvinte/frază
DEV_VARIATA = 4.8

# Încredere scăzută — euristică fără sursă metodologică.
BANDA = (15, 28)
BANDA_PROPORTIE = 0.70

# Fără prag publicat — calibrează pe corpus propriu.
CV_PARAGRAFE_UNIFORM = 0.30
DESCHIDERI_REPETATE = 0.40  # proporție de paragrafe care încep la fel
HEADINGURI_LA_100_CUV = 2.0

CUVANT = re.compile(r"\b[\wăâîșțĂÂÎȘȚ'-]+\b")
FINAL_FRAZA = re.compile(r"(?<=[.!?…])[\s\"»)]+")
CONCLUZIE = re.compile(
    r"^#{1,6}\s*(concluzi|rezumat|in (concluzie|esenta)|pe scurt|"
    r"gânduri finale|în încheiere)", re.IGNORECASE | re.MULTILINE)


def curata(text):
    """Scoate blocurile de cod, heading-urile și marcajele care ar strica statistica."""
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"^\s{0,3}#{1,6}\s.*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+[.)]\s+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`>|]", " ", text)
    return text


def fraze(text):
    brute = FINAL_FRAZA.split(curata(text))
    return [len(CUVANT.findall(f)) for f in brute if len(CUVANT.findall(f)) >= 3]


def paragrafe(text):
    bucati = re.split(r"\n\s*\n", curata(text))
    return [b.strip() for b in bucati if len(CUVANT.findall(b)) >= 10]


def medie(valori):
    return sum(valori) / len(valori) if valori else 0.0


def deviatie(valori):
    if len(valori) < 2:
        return 0.0
    m = medie(valori)
    return (sum((v - m) ** 2 for v in valori) / (len(valori) - 1)) ** 0.5


def cv(valori):
    m = medie(valori)
    return deviatie(valori) / m if m else 0.0


def analizeaza(text):
    text = unicodedata.normalize("NFC", text)
    lungimi = fraze(text)
    paras = paragrafe(text)
    lungimi_para = [len(CUVANT.findall(p)) for p in paras]

    in_banda = sum(1 for L in lungimi if BANDA[0] <= L <= BANDA[1])
    proportie_banda = in_banda / len(lungimi) if lungimi else 0.0

    deschideri = [CUVANT.findall(p)[:2] for p in paras]
    deschideri = [" ".join(d).lower() for d in deschideri if d]
    repetate = 0
    if deschideri:
        frecvente = {}
        for d in deschideri:
            primul = d.split()[0]
            frecvente[primul] = frecvente.get(primul, 0) + 1
        repetate = max(frecvente.values()) / len(deschideri)

    cuvinte = len(CUVANT.findall(text))
    headinguri = len(re.findall(r"^\s{0,3}#{1,6}\s", text, re.MULTILINE))
    densitate_head = headinguri * 100.0 / cuvinte if cuvinte else 0.0

    return {
        "cuvinte": cuvinte,
        "fraze": len(lungimi),
        "lungime_medie": medie(lungimi),
        "deviatie": deviatie(lungimi),
        "cv_fraze": cv(lungimi),
        "min_max": (min(lungimi), max(lungimi)) if lungimi else (0, 0),
        "proportie_banda": proportie_banda,
        "paragrafe": len(paras),
        "cv_paragrafe": cv(lungimi_para),
        "deschideri_repetate": repetate,
        "headinguri": headinguri,
        "headinguri_la_100": densitate_head,
        "are_concluzie": bool(CONCLUZIE.search(text)),
    }


def semnale(a):
    """Semnale de uniformitate, cu eticheta de încredere a pragului."""
    gasite = []
    if a["fraze"] >= 8:
        if a["cv_fraze"] < CV_UNIFORM:
            gasite.append(("ritm_uniform", "medie",
                           f"cv={a['cv_fraze']:.3f} < {CV_UNIFORM}"))
        elif a["cv_fraze"] < CV_VARIAT:
            gasite.append(("ritm_la_limita", "medie",
                           f"cv={a['cv_fraze']:.3f}, zona nedecisa "
                           f"{CV_UNIFORM}-{CV_VARIAT}"))
        if a["deviatie"] < DEV_UNIFORM:
            gasite.append(("fraze_egale", "medie",
                           f"deviatie={a['deviatie']:.1f} < {DEV_UNIFORM} cuvinte"))
        if a["proportie_banda"] >= BANDA_PROPORTIE:
            gasite.append(("concentrare_in_banda", "scazuta",
                           f"{a['proportie_banda']:.0%} din fraze in "
                           f"{BANDA[0]}-{BANDA[1]} cuvinte"))
    if a["paragrafe"] >= 4:
        if a["cv_paragrafe"] < CV_PARAGRAFE_UNIFORM:
            gasite.append(("paragrafe_egale", "necalibrata",
                           f"cv={a['cv_paragrafe']:.3f} < {CV_PARAGRAFE_UNIFORM}"))
        if a["deschideri_repetate"] >= DESCHIDERI_REPETATE:
            gasite.append(("deschideri_repetate", "necalibrata",
                           f"{a['deschideri_repetate']:.0%} din paragrafe incep "
                           f"cu acelasi cuvant"))
    if a["headinguri_la_100"] > HEADINGURI_LA_100_CUV and a["cuvinte"] > 150:
        gasite.append(("structura_excesiva", "necalibrata",
                       f"{a['headinguri']} headinguri la {a['cuvinte']} cuvinte"))
    if a["are_concluzie"]:
        gasite.append(("capcana_concluziei", "sigura",
                       "sectiune finala de tip Concluzie/Rezumat"))
    return gasite


def calculeaza_scor(gasite):
    """0-3 puncte. Se adună cu scorul din check-tipare.py."""
    nume = {n for n, _, _ in gasite}
    scor = 0
    if "ritm_uniform" in nume or "fraze_egale" in nume:
        scor += 1
    if "paragrafe_egale" in nume or "deschideri_repetate" in nume:
        scor += 1
    if "structura_excesiva" in nume or "capcana_concluziei" in nume:
        scor += 1
    return scor


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    sursa = argv[0]
    try:
        text = sys.stdin.read() if sursa == "-" else open(
            sursa, "r", encoding="utf-8").read()
    except OSError as e:
        print(f"eroare: {e}", file=sys.stderr)
        return 2

    a = analizeaza(text)
    if a["fraze"] < 5:
        print(f"text prea scurt pentru statistica ({a['fraze']} fraze)")
        return 0

    gasite = semnale(a)
    scor = calculeaza_scor(gasite)

    if "--scor" in argv:
        print(f"scor_automat={scor}/3 " +
              (f"({', '.join(n for n, _, _ in gasite)})" if gasite
               else "(niciun semnal)"))
        return 1 if scor else 0

    print(f"metrici|fraze={a['fraze']}|medie={a['lungime_medie']:.1f}"
          f"|deviatie={a['deviatie']:.1f}|cv={a['cv_fraze']:.3f}"
          f"|min-max={a['min_max'][0]}-{a['min_max'][1]}")
    print(f"metrici|paragrafe={a['paragrafe']}|cv={a['cv_paragrafe']:.3f}"
          f"|in_banda={a['proportie_banda']:.0%}"
          f"|headinguri={a['headinguri']}")

    if not gasite:
        print("---\n0 semnale de uniformitate")
        return 0

    for nume, incredere, detaliu in gasite:
        print(f"{nume}|incredere={incredere}|{detaliu}")
    print(f"---\ntotal={len(gasite)} semnale | scor_automat={scor}/3")
    print("nota: semnal, nu verdict. Pragurile vin din corpusuri englezesti "
          "si gresesc pe registru formal.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
