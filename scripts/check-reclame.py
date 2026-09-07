#!/usr/bin/env python3
"""Verifică textele de reclamă: limite de caractere, politici editoriale ale
platformelor (Google Ads, Meta) și semnăturile structurale ale textului-forjat.

Rulează DOAR pe fișiere cu linii etichetate (H1:, D1:, Cale1:, Text:, Titlu:,
Descriere:). Fără etichete → „0 elemente de reclamă" și exit 0: genurile
existente (articol, pagină, literar) nu sunt atinse. Pleonasmele, clișeele și
formele nonnormative de limbă NU se duplică aici — le prind check-tipare,
check-modelisme și check-human-voice, rulate oricum de verifica.py.

Ce e dependent de gen și de aceea stă aici:
- limitele hard de caractere ale platformei (depășire = refuz sau trunchiere);
- politicile editoriale: „!" în headline-uri Google, CAPS, emoji, duplicate;
- semnăturile afirmărilor goale specifice anunțului, unde fiecare caracter
  costă: perechea temporală fără cauză („seara X, dimineața Y") și tautologia
  de beneficiu (acțiune + rezultat, fără niciun token de produs — efectul
  există oricum, cu sau fără produsul anunțat).

Formatul fișierului și limitele oficiale: references/reclame/platforme.md.

Usage:
    check-reclame.py <fisier_sau_->
    check-reclame.py <fisier> --platform google|meta   # forțează platforma
    check-reclame.py <fisier> --brand "Nume Brand"     # testul schimbării de brand
    check-reclame.py <fisier> --json                   # output structurat
    check-reclame.py --help

Exit codes:
    0 = curat (fără etichete sau fără semnale)
    1 = semnale de revizuit
    2 = eroare de input
"""
import json
import re
import sys
import unicodedata

import _comun

# ---- Limite oficiale (verificate 2026-09-07; surse în platforme.md) --------
# Google Responsive Search Ads
GOOGLE_H = 30
GOOGLE_D = 90
GOOGLE_CALE = 15
GOOGLE_H_MAX = 15
GOOGLE_D_MAX = 4
# Meta (Facebook/Instagram)
META_TEXT_REC = 125
META_TEXT_MAX = 2200
META_TITLU_REC = 40
META_TITLU_MAX = 255
META_DESCRIERE_REC = 25
META_DESCRIERE_MAX = 255

# ---- Parserul de etichete --------------------------------------------------
# Ordinea contează: etichetele lungi („Text principal") înaintea scurtelor.
# Tiparele recunosc eticheta indiferent de diacritice prin plierea liniei.
ETICHETE = (
    ("headline", r"^\s*H(\d{1,2})\s*:\s*(.*)$", "google"),
    ("headline", r"^\s*Headline\s*:\s*(.*)$", "google"),
    ("descriere_g", r"^\s*D(\d)\s*:\s*(.*)$", "google"),
    ("descriere_g", r"^\s*Description\s*:\s*(.*)$", "google"),
    ("cale", r"^\s*Cale(\d)?\s*:\s*(.*)$", "google"),
    ("cale", r"^\s*Path\s*:\s*(.*)$", "google"),
    ("text_meta", r"^\s*Text(?: principal)?\s*:\s*(.*)$", "meta"),
    ("text_meta", r"^\s*Primary text\s*:\s*(.*)$", "meta"),
    ("titlu_meta", r"^\s*Titlu\s*:\s*(.*)$", "meta"),
    ("descriere_meta", r"^\s*Descriere\s*:\s*(.*)$", "meta"),
    ("descriere_meta", r"^\s*Description\s*:\s*(.*)$", "meta"),
)

HEADINGS_PLATFORMA = {
    "google": ("google", "search", "rsa"),
    "meta": ("meta", "facebook", "instagram", "fb", "ig"),
}

# ---- Politici Google: CAPS, emoji, semne gimmick ----------------------------
# Acronime/termeni consacrecați, scriși cu litere mari legitim.
ALLOWLIST_CAPS = {"spf", "uv", "uva", "uvb", "bha", "aha", "seo", "ppc", "cta",
                  "kpi", "ctr", "ong", "sms", "gdpr", "eur", "usd", "ig", "fb"}
CAPS = re.compile(r"\b[A-ZĂÂÎȘȚŞŢ]{3,}\b")
EMOJI = re.compile(r"[\U0001F000-\U0001FAFF\u2190-\u21FF\u2600-\u27BF"
                   r"\u2B00-\u2BFF\uFE0F\u2049\u203C]")
GIMMICK = re.compile(r"(!\s*!|\?\s*\?|!{2,}|\?{2,}|\b[A-ZĂÂÎȘȚŞŢ](?:\s*-\s*"
                     r"[A-ZĂÂÎȘȚŞŢ]){2,}\b)")
INSERARE = re.compile(r"\{[^}]*\}")
PLACEHOLDER = re.compile(r"\[(?:de completat|todo|placeholder)[^\]]*\]|"
                         r"\{\{[^}]+\}\}", re.IGNORECASE)

# ---- Semnăturile afirmărilor goale (pe text pliat, fără diacritice) --------
# Două momente din zi în aceeași propoziție, fără conector cauzal între ele:
# „Seara cureți tenul, dimineața îl simți moale" — succesiunea nu creează un
# beneficiu. Virgula nu desparte propoziția-scandal; punctul da.
MOMENTE = re.compile(r"\b(seara|dimineata|noaptea|ziua|dupa[- ]?amiaza|"
                     r"la pranz|matina)\b")
CAUZALE = re.compile(r"\b(pentru ca|fiindca|deoarece|deci|asa ca|ca sa|incat|"
                     r"astfel|gratie|datorita)\b")

# Acțiune de rutină + rezultat pozitiv, FĂRĂ token de produs/brand: efectul
# se produce oricum, cu sau fără produsul anunțat („Te pieptănești, părul e
# neted"). Calibrarea intrărilor: sensul rezultatului trebuie să fie conținut
# în sensul acțiunii („a pieptăna" ⊃ „neted") sau produs din obișnuință.
ACTIUNI = re.compile(
    r"\b(pieptan\w*|spal\w*|speli|curat(?:eaz\w*|ez|am|ati|ati|are|i|esc)\w*|"
    r"cureti|clat\w*|aplic\w*|mas(?:eaz|ez)\w*|peri\w*|rad(?:e|i)?\b|manc\w*|"
    r"bea(?:m|ti)?\b|dorm\w*)\b")
REZULTATE = re.compile(
    r"\b(neted\w*|moale|catifelat\w*|matasos\w*|lucios\w*|fina?|finele|"
    r"curata?|curate|curati|proaspat\w*|hidratat\w*|radiant\w*|odihnit\w*|"
    r"hranit\w*|protejat\w*|elastic\w*|supla|suplu|uniform\w*|luminos\w*)\b")
PRODUSE = re.compile(
    r"\b(sampon\w*|balsam\w*|crema?|creme|ulei\w*|ser\b|masca|masti|"
    r"demachiant\w*|detergent\w*|gel(?:uri)?\b|spuma|toner\w*|hidratant\w*|"
    r"sapun\w*|pasta|paste|supliment\w*|machiaj\w*|esenta|lotiune)\b")

# Promisiuni perceptive fără mecanism; superlative fără demonstrație; fraze-
# șablon traduse mecanic din engleză. Fiecare apariție se raportează: în
# anunț textele sunt scurte prin construcție, pragurile de densitate din
# scripturile de proză n-ar declanșa niciodată.
PERCEPTIVE = re.compile(
    r"\b(vei simti|te vei simti|te vei bucura|vei vedea|simti diferenta|"
    r"vezi diferenta|de la prima (?:aplicare|utilizare|folosire)|"
    r"arat[ae] mai (?:bine|frumos|proaspat))\b")
SUPERLATIVE = re.compile(
    r"\b(cel mai bun|cea mai buna|cele mai bune|cei mai buni|nr\. ?1|"
    r"numarul 1|numar unu|100% (?:natural|sigur|eficient|original|legal)|"
    r"garantat)\b")
CALCURI = re.compile(
    r"\b(spun[eă].{0,6}la revedere|trezeste-?te cu|deblocheaz\w+|"
    r"elibereaza puterea|simti magia|lasa [^.]{0,30}sa (?:iti )?fac(?:a|e) treaba|"
    r"ridica[- ]?ti rutina|ia-?ti portia|feed-?ul tau merit[aă]?)\b")
HASHTAG = re.compile(r"#\w+")


def pliaza(text):
    return _comun.pliaza(unicodedata.normalize("NFC", text))


def parseaza(text, platform_forta=None):
    """Extrage elementele de anunț din liniile etichetate.

    Platforma vine din heading-ul anterior („# … Google …"), din
    `platform_forta` sau din platforma implicită a etichetei. Returnează o
    listă de dict-uri {tip, platforma, valoare, linie, eticheta}.
    """
    elemente = []
    platforma_curenta = None
    for i, linie in enumerate(text.splitlines(), 1):
        if linie.lstrip().startswith("#"):
            cap = pliaza(linie)
            platforma_curenta = None
            for platforma, chei in HEADINGS_PLATFORMA.items():
                if any(re.search(rf"\b{re.escape(k)}\b", cap) for k in chei):
                    platforma_curenta = platforma
                    break
            continue
        for tip, tipar, platforma_implicita in ETICHETE:
            m = re.match(tipar, linie, re.IGNORECASE)
            if not m:
                continue
            grupuri = m.groups()
            valoare = grupuri[-1].strip()
            prefix = grupuri[0] if len(grupuri) > 1 else ""
            eticheta = (tip[:1].upper() + str(prefix)) if tip in (
                "headline", "descriere_g") else tip
            if tip == "cale":
                eticheta = f"Cale{prefix or ''}"
            elif tip == "headline" and not prefix.isdigit():
                eticheta = f"H{len([e for e in elemente if e['tip'] == 'headline']) + 1}"
            elemente.append({
                "tip": tip,
                "platforma": platform_forta or platforma_curenta
                             or platforma_implicita,
                "valoare": valoare,
                "linie": i,
                "eticheta": eticheta,
            })
            break
    return elemente


def _semnal(severitate, categorie, element, detaliu, sugestie):
    return {
        "severitate": severitate,
        "categorie": categorie,
        "eticheta": element["eticheta"],
        "linie": element["linie"],
        "detaliu": detaliu,
        "sugestie": sugestie,
    }


def verifica_limite(element):
    tip, platforma, val = element["tip"], element["platforma"], element["valoare"]
    n = len(val)
    semnale = []

    def peste(categorie, limita, severitate, consiliu):
        semnale.append(_semnal(
            severitate, categorie, element, f"{n}/{limita} caractere",
            consiliu))

    if platforma == "google":
        if tip == "headline":
            if n > GOOGLE_H:
                peste("limita_caractere", GOOGLE_H, "critic",
                      f"scurtează la {GOOGLE_H} de caractere")
        elif tip == "descriere_g":
            if n > GOOGLE_D:
                peste("limita_caractere", GOOGLE_D, "critic",
                      f"scurtează la {GOOGLE_D} de caractere")
        elif tip == "cale":
            if n > GOOGLE_CALE:
                peste("limita_caractere", GOOGLE_CALE, "critic",
                      f"scurtează la {GOOGLE_CALE} de caractere")
            if re.search(r"[^\w-]", val, re.UNICODE) and val:
                semnale.append(_semnal(
                    "important", "cale_invalida", element, val,
                    "doar litere, cifre și cratimă, fără spații"))
    else:
        if tip == "text_meta":
            if n > META_TEXT_MAX:
                peste("limita_caractere", META_TEXT_MAX, "critic",
                      f"maximul Meta este {META_TEXT_MAX}")
            elif n > META_TEXT_REC:
                peste("text_peste_recomandat", META_TEXT_REC, "minor",
                      f"vizibil doar primele ~{META_TEXT_REC} de caractere, "
                      "pune ideea-cheie la început")
        elif tip == "titlu_meta":
            if n > META_TITLU_MAX:
                peste("limita_caractere", META_TITLU_MAX, "critic",
                      f"maximul Meta este {META_TITLU_MAX}")
            elif n > META_TITLU_REC:
                peste("titlu_peste_recomandat", META_TITLU_REC, "minor",
                      "titlul e trunchiat vizual în feed")
        elif tip == "descriere_meta":
            if n > META_DESCRIERE_MAX:
                peste("limita_caractere", META_DESCRIERE_MAX, "critic",
                      f"maximul Meta este {META_DESCRIERE_MAX}")
            elif n > META_DESCRIERE_REC:
                peste("descriere_peste_recomandat", META_DESCRIERE_REC,
                      "minor", "descrierea apare doar pe unele plasamente, "
                      "ține-o scurtă")
    return semnale


def verifica_politici_google(element):
    tip, val = element["tip"], element["valoare"]
    semnale = []
    if tip == "headline":
        if "!" in val:
            semnale.append(_semnal(
                "critic", "politica_google", element, "«!» în headline",
                "semnul exclamării nu e permis în headline-urile Google"))
    elif tip == "descriere_g":
        if val.count("!") > 1:
            semnale.append(_semnal(
                "critic", "politica_google", element,
                f"{val.count('!')} semne de exclamare",
                "maximum unul în descriere"))
    for m in CAPS.finditer(val):
        if pliaza(m.group(0)) in ALLOWLIST_CAPS:
            continue
        semnale.append(_semnal(
            "important", "caps_nepotrivit", element, m.group(0),
            "CAPS e respins de Google, afară de acronime"))
        break
    if EMOJI.search(val):
        severitate = "minor" if element["platforma"] == "meta" else "critic"
        semnale.append(_semnal(
            severitate, "emoji_in_anunt", element, EMOJI.search(val).group(0),
            "emoji nu e permis în textul anunțului Google" if element[
                "platforma"] == "google" else "emoji subțiază credibilitatea "
            "și e trunchiat pe unele plasamente"))
    m = GIMMICK.search(val)
    if m:
        semnale.append(_semnal(
            "critic", "punctuatie_gimmick", element, m.group(0),
            "punctuație repetată/„creativă” respinsă de platformă"))
    if INSERARE.search(val):
        semnale.append(_semnal(
            "important", "inserare_neverificata", element,
            INSERARE.search(val).group(0),
            "verifică că sintaxa de inserare e intenționată și că default-ul "
            "există"))
    if PLACEHOLDER.search(val):
        semnale.append(_semnal(
            "critic", "placeholder", element, PLACEHOLDER.search(val).group(0),
            "completează cu date reale sau elimină"))
    return semnale


def verifica_duplicate(elemente):
    """Assets identice în aceeași platformă și fel — politica de Repetition."""
    semnale = []
    vazute = {}
    for e in elemente:
        cheie = (e["platforma"], e["tip"], pliaza(e["valoare"]))
        if not cheie[2]:
            continue
        if cheie in vazute:
            semnale.append(_semnal(
                "important", "duplicat", e, e["valoare"],
                f"identic cu {vazute[cheie]} — anunțurile Google resping "
                "asset-urile repetate"))
        else:
            vazute[cheie] = e["eticheta"]
    return semnale


def verifica_structura_rsa(elemente):
    semnale = []
    h = [e for e in elemente if e["platforma"] == "google"
         and e["tip"] == "headline"]
    d = [e for e in elemente if e["platforma"] == "google"
         and e["tip"] == "descriere_g"]
    if h and len(h) < 3:
        semnale.append({
            "severitate": "important", "categorie": "structura_rsa",
            "eticheta": "google", "linie": h[0]["linie"],
            "detaliu": f"{len(h)} headline-uri",
            "sugestie": "minimum 3 headline-uri pentru un anunț responsiv",
        })
    if len(h) > GOOGLE_H_MAX:
        semnale.append({
            "severitate": "critic", "categorie": "structura_rsa",
            "eticheta": "google", "linie": h[0]["linie"],
            "detaliu": f"{len(h)} headline-uri",
            "sugestie": f"maximum {GOOGLE_H_MAX} headline-uri per anunț",
        })
    if d and len(d) < 2:
        semnale.append({
            "severitate": "minor", "categorie": "structura_rsa",
            "eticheta": "google", "linie": d[0]["linie"],
            "detaliu": f"{len(d)} descrieri",
            "sugestie": "două descrieri dau mașinii de licitare variante",
        })
    if len(d) > GOOGLE_D_MAX:
        semnale.append({
            "severitate": "critic", "categorie": "structura_rsa",
            "eticheta": "google", "linie": d[0]["linie"],
            "detaliu": f"{len(d)} descrieri",
            "sugestie": f"maximum {GOOGLE_D_MAX} descrieri per anunț",
        })
    return semnale


def verifica_pseudologie(element):
    """Perechi temporale fără cauză și tautologia de beneficiu — semnăturile
    structurale ale propoziției care nu promite nimic."""
    val = element["valoare"]
    pliat = pliaza(val)
    semnale = []

    momente = list(MOMENTE.finditer(pliat))
    tipuri_distincte = {m.group(1) for m in momente}
    if len(tipuri_distincte) >= 2:
        prima, ultima = momente[0], momente[-1]
        intre = pliat[prima.end():ultima.start()]
        if (ultima.start() - prima.start() <= 140
                and "." not in intre and "!" not in intre and "?" not in intre
                and not CAUZALE.search(intre)):
            semnale.append(_semnal(
                "important", "pseudologie_temporala", element,
                val[max(0, prima.start() - 10):ultima.end() + 10],
                "leagă cauza («pentru că…») sau spune o consecință concretă — "
                "două momente ale zilei nu creează un beneficiu"))

    # Tautologia se judecă pe propoziție, nu pe element: „Te pieptănești, părul
    # e neted” rămâne goală chiar dacă altă propoziție a anunțului numește
    # produsul. Produsul/brandul contează doar în ACEEAȘI propoziție cu efectul.
    for propozitie in re.split(r"[.!?]+", pliat):
        if not propozitie.strip():
            continue
        if (ACTIUNI.search(propozitie) and REZULTATE.search(propozitie)
                and not PRODUSE.search(propozitie)):
            fragment = (f"{ACTIUNI.search(propozitie).group(0)} → "
                        f"{REZULTATE.search(propozitie).group(0)}")
            semnale.append(_semnal(
                "important", "tautologie_beneficiu", element, fragment,
                "efectul există oricum, fără produsul anunțat — leagă-l de "
                "produs (agent + mecanism) sau taie propoziția"))
    return semnale


def verifica_limbaj_anunt(element):
    """Promisiuni perceptive, superlative nefundamentate, calcuri-sablon,
    hashtag-uri stivuite — fiecare apariție, pentru că în anunț textele sunt
    scurte prin construcție."""
    val = element["valoare"]
    pliat = pliaza(val)
    semnale = []
    m = PERCEPTIVE.search(pliat)
    if m:
        semnale.append(_semnal(
            "minor", "promisiune_perceptiva", element, m.group(0),
            "înlocuiește senzația cu consecința concretă și măsurabilă"))
    m = SUPERLATIVE.search(pliat)
    if m:
        semnale.append(_semnal(
            "important", "superlativ_nefundamentat", element, m.group(0),
            "susține afirmația pe landing page sau reformulează („printre "
            "cele mai…”, cifre verificate)"))
    m = CALCURI.search(pliat)
    if m:
        semnale.append(_semnal(
            "important", "calc_reclama", element, m.group(0),
            "formulă-sablon tradusă din engleză — spune concret"))
    if element["tip"] == "text_meta" and len(HASHTAG.findall(val)) > 3:
        semnale.append(_semnal(
            "minor", "hashtag_uri_stivuite", element,
            f"{len(HASHTAG.findall(val))} hashtag-uri",
            "maximum trei; restul sufocă mesajul"))
    return semnale


def analizeaza(text, platform_forta=None, brand=None):
    """Punctul de intrare pentru verifica.py. Returnează dict cu elementele și
    semnalele; genurile fără etichete ies curate."""
    elemente = parseaza(text, platform_forta)
    semnale = []
    if not elemente:
        return {"elemente": 0, "semnale": [], "platforme": {}}

    for e in elemente:
        if not e["valoare"]:
            semnale.append(_semnal(
                "important", "element_gol", e, e["eticheta"],
                "eticheta nu are text"))
            continue
        semnale.extend(verifica_limite(e))
        semnale.extend(verifica_politici_google(e))
        semnale.extend(verifica_pseudologie(e))
        semnale.extend(verifica_limbaj_anunt(e))
    semnale.extend(verifica_duplicate(elemente))
    semnale.extend(verifica_structura_rsa(elemente))

    if brand:
        brand_pliat = pliaza(brand)
        if not any(brand_pliat in pliaza(e["valoare"]) for e in elemente):
            semnale.append({
                "severitate": "minor", "categorie": "text_fara_brand",
                "eticheta": "general", "linie": 0,
                "detaliu": f"brandul „{brand}” nu apare nicăieri",
                "sugestie": "testul schimbării de brand: dacă textul rămâne "
                            "valabil pentru orice brand, nu spune nimic despre "
                            "al tău — numește brandul sau concretizează",
            })

    semnale.sort(key=lambda s: (s["linie"], s["eticheta"]))
    platforme = {}
    for e in elemente:
        platforme[e["platforma"]] = platforme.get(e["platforma"], 0) + 1
    return {"elemente": len(elemente), "semnale": semnale,
            "platforme": platforme}


ORDINE = {"critic": 0, "important": 1, "minor": 2}


def tipareste(rez):
    if not rez["elemente"]:
        print("0 elemente de reclama detectate (fara etichete H1:/D1:/Text:/"
              "Titlu: — vezi references/reclame/platforme.md)")
        return
    plat = ", ".join(f"{k}={v}" for k, v in sorted(rez["platforme"].items()))
    print(f"elemente={rez['elemente']} ({plat})")
    for s in rez["semnale"]:
        print(f"{s['severitate']}|{s['categorie']}|{s['eticheta']}"
              f"|L{s['linie']}|{s['detaliu']}|→ {s['sugestie']}")
    if not rez["semnale"]:
        print("0 semnale de reclama")


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    platforma = brand = None
    sursa = None
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--platform" and i + 1 < len(argv):
            platforma = argv[i + 1].lower()
            if platforma not in ("google", "meta"):
                print("eroare: --platform acceptă doar google sau meta",
                      file=sys.stderr)
                return 2
            i += 2
            continue
        if arg == "--brand" and i + 1 < len(argv):
            brand = argv[i + 1]
            i += 2
            continue
        if sursa is None and (arg == "-" or not arg.startswith("-")):
            sursa = arg
        i += 1
    if sursa is None:
        print("eroare: lipsește fișierul de verificat", file=sys.stderr)
        return 2
    try:
        text = _comun.citeste_intrare(sursa)
    except OSError as error:
        print(f"eroare: {error}", file=sys.stderr)
        return 2

    rez = analizeaza(text, platform_forta=platforma, brand=brand)
    if "--json" in argv:
        print(json.dumps(rez, ensure_ascii=False, indent=1))
    else:
        tipareste(rez)
    return 1 if rez["semnale"] else 0


if __name__ == "__main__":
    sys.exit(main())
