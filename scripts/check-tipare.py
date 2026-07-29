#!/usr/bin/env python3
"""Scanează un text pentru clișee AI, calcuri din engleză și tranziții mecanice.

Potrivirea ignoră diacriticele, deci prinde și textul scris fără ele sau cu
sedilă (ş/ţ) în loc de virgulă (ș/ț). Tiparele acoperă formele flexionare, nu
doar forma de dicționar.

Categoria `simboluri_excesive` acoperă abuzul de formatare — emoji decorative,
liniuța ca paranteză improvizată în frază, bold/italic dese și (separat, pe
proporție de linii, nu pe regex) liste cu „-" în locul prozei. Toate au prag
de abuz, nu interdicție absolută — o listă de funcționalități sau un singur
bold nu sunt semnal.

Fiecare tipar are o severitate (critic/important/minor) și un prag:
    mereu          — semnalat la orice apariție
    la_aglomerare  — semnalat la 3+ în același paragraf sau peste densitate
    la_densitate   — semnalat doar peste densitate

Unde există o corecție canonică, raportul o dă direct după fragment:
    critic|romgleza|L12|...face sens...|→ are sens

Usage:
    check-tipare.py <fisier_sau_->
    check-tipare.py <fisier> --prag 5      # apariții/1000 cuvinte (default 5)
    check-tipare.py <fisier> --tot         # arată și potrivirile sub prag
    check-tipare.py <fisier> --scor        # doar scorul de semnale
    check-tipare.py --help

Exit codes:
    0 = curat (nimic critic sau important, niciun prag depășit)
    1 = potriviri raportate
    2 = eroare de input (fișier lipsă etc.)
"""
import re
import sys

import _comun


def adj(tulpina):
    """Adjectiv: toate terminațiile de gen, număr și articol."""
    return rf"\b{tulpina}(a|ul|ului|ui|i|ii|ilor|e|ele|elor)?\b"


def subst(tulpina):
    """Substantiv: singular/plural, nearticulat/articulat."""
    return rf"\b{tulpina}(a|ea|ul|ului|le|lor|i|ii|e|ele)?\b"


# Tiparele sunt scrise fără diacritice — se potrivesc pe textul pliat.
# Format: (regex, prag) sau (regex, prag, sugestie de corecție).
CATEGORII = {
    "structura": ("important", [
        (r"\bin concluzie\b", "mereu", "elimină — încheie cu o idee, nu cu un rezumat"),
        (r"\bin esenta\b", "mereu", "elimină sau spune direct ideea"),
        (r"\bpe scurt\b", "la_aglomerare"),
        (r"\bprin urmare\b", "la_aglomerare", "deci / așa că — sau leagă ideile fără conector"),
        (r"\bde asemenea\b", "la_aglomerare", "și / elimină — leagă ideile direct"),
        (r"\bin plus\b", "la_aglomerare"),
        (r"\btotodata\b", "la_aglomerare"),
        (r"\bcu toate acestea\b", "la_aglomerare", "dar / totuși"),
        (r"\bmai mult decat atat\b", "mereu", "elimină conectorul, spune direct"),
        (r"\bpe de o parte\b.{0,400}?\bpe de alta parte\b", "mereu",
         "renunță la simetria forțată; ia o poziție"),
        (r"\bin primul rand\b.{0,600}?\bin al doilea rand\b", "mereu",
         "enumerarea mecanică — leagă ideile natural sau folosește o listă"),
        (r"\bnu doar\b.{0,120}?\bci si\b", "la_aglomerare"),
    ]),
    "introduceri": ("critic", [
        (r"\bin lumea (de astazi|digitala|moderna|contemporana)\b", "mereu",
         "elimină; începe cu subiectul concret"),
        (r"\bintr-o lume in continua schimbare\b", "mereu", "elimină; începe cu subiectul concret"),
        (r"\bin era digitala\b", "mereu", "elimină; începe cu subiectul concret"),
        (r"\bin societatea moderna\b", "mereu", "elimină; începe cu subiectul concret"),
        (r"\bin contextul actual\b", "mereu", "elimină; începe cu subiectul concret"),
        (r"\bde cand lumea si pamantul\b", "mereu", "elimină clișeul"),
    ]),
    "umpluturi": ("critic", [
        (r"\beste important de mentionat ca\b", "mereu", "elimină; spune direct faptul"),
        (r"\bmerita (precizat|subliniat|mentionat) (faptul )?ca\b", "mereu",
         "elimină; spune direct faptul"),
        (r"\btrebuie mentionat (faptul )?ca\b", "mereu", "elimină; spune direct faptul"),
        (r"\beste demn de (remarcat|mentionat)\b", "mereu", "elimină; spune direct faptul"),
        (r"\bin acest articol\b", "mereu", "elimină meta-textul"),
        (r"\bin cele ce urmeaza\b", "mereu", "elimină meta-textul"),
    ]),
    "vocabular_corporatist": ("important", [
        (adj("revolutionar"), "mereu", "spune concret ce face diferit"),
        (adj("impresionant"), "la_aglomerare", "dă cifra sau detaliul, nu adjectivul"),
        (adj("remarcabil"), "la_aglomerare", "dă cifra sau detaliul, nu adjectivul"),
        (adj("vibrant"), "mereu", "descrie concret, nu cu epitet de broșură"),
        (r"\bschimbare de paradigma\b", "mereu", "spune ce se schimbă concret"),
        (r"\bun pilon fundamental\b", "mereu", "spune rolul concret"),
        (r"\bo componenta esentiala\b", "mereu", "spune rolul concret"),
        (r"\babordare holistica\b", "mereu", "spune ce acoperă concret"),
        (r"\badopta o (abordare|filozofie|strategie)\b", "mereu", "verb concret: face / folosește"),
        (r"\bse remarca prin\b", "la_aglomerare", "are / oferă + detaliul concret"),
        (r"\bsolutie? de ultima generatie\b", "mereu", "spune ce o face nouă"),
        (r"\bsolutii? inovatoare\b", "mereu", "spune ce o face nouă"),
    ]),
    "abstractiuni": ("minor", [
        (subst("optimizar"), "la_densitate"),
        (subst("aliniere"), "la_densitate"),
        (subst("eficientizar"), "la_densitate"),
        (subst("implementar"), "la_densitate"),
        (subst("valorificar"), "la_densitate"),
        (r"\ba facilita\b", "la_densitate", "a ușura / a ajuta"),
        (r"\ba contribui la\b", "la_densitate"),
        (r"\bun impact (semnificativ|major|considerabil) asupra\b", "la_aglomerare",
         "spune efectul concret, cu cifre dacă le ai"),
        (r"\bse recomanda adoptarea\b", "mereu", "diateza activă: cine, ce să facă"),
    ]),
    "cuantificari_vagi": ("important", [
        (r"\bo serie de\b", "la_aglomerare", "cifra exactă sau enumeră"),
        (r"\bo multitudine de\b", "mereu", "cifra exactă sau «multe»"),
        (r"\bun numar (semnificativ|considerabil|impresionant)\b", "mereu", "cifra exactă"),
        (r"\bo (gama|paleta) (larga|variata) de\b", "mereu", "enumeră 2-3 exemple concrete"),
        (r"\bun spectru larg de\b", "mereu", "enumeră 2-3 exemple concrete"),
    ]),
    "hedging": ("important", [
        (r"\beste posibil ca\b", "la_aglomerare", "afirmă sau spune condiția exactă"),
        (r"\bs-ar putea ca\b", "la_aglomerare", "afirmă sau spune condiția exactă"),
        (r"\bpoate fi considerat\b", "la_aglomerare", "este — sau spune cine îl consideră"),
        (r"\bin general\b", "la_densitate"),
        (r"\bde regula\b", "la_densitate"),
    ]),
    "romgleza": ("critic", [
        (r"\bface sens\b", "mereu", "are sens"),
        (r"\b(joaca|joc|jucat|juca|jucand|jucam) un rol (crucial|cheie)\b", "mereu",
         "este esențial / contează decisiv"),
        (r"\bla sfarsitul zilei\b", "mereu", "în fond / până la urmă"),
        (r"\bin termeni de\b", "mereu", "în ceea ce privește / ca"),
        (r"\bseamless\b", "mereu", "fără întreruperi / fluent"),
        (r"\binsight-?uri\b", "mereu", "concluzii / observații"),
        (adj("actionabil"), "mereu", "concret / aplicabil"),
        (r"\ba performa\b", "mereu", "a funcționa / a da rezultate"),
    ]),
    "calc_sintactic": ("critic", [
        (r"\ba adresa (o |aceasta |aceste |problema|probleme)", "mereu",
         "a aborda / a rezolva problema"),
        (r"\b(adreseaza|adresam|adresat|adresand) (o |aceasta |aceste )?(problema|probleme|provocar)",
         "mereu", "abordează / rezolvă problema"),
        (r"\ba aplica pentru (un |o |acest|aceasta)?\s*(post|job|rol|pozitie)", "mereu",
         "a candida la / a-și depune candidatura"),
        (r"\bde catre (sistem|platforma|algoritm|aplicatie|program|software)", "mereu",
         "diateza activă: sistemul face X"),
        (r"\bin ordine sa\b", "mereu", "ca să / pentru a"),
        (r"\bbazat pe faptul ca\b", "mereu", "pentru că / fiindcă"),
    ]),
    "pleonasm": ("important", [
        (r"\ba reveni din nou\b|\brevine din nou\b|\brevenit din nou\b", "mereu", "revine"),
        (r"\ba colabora impreuna\b|\bcolaboreaza impreuna\b", "mereu", "colaborează"),
        (r"\bconsens comun\b", "mereu", "consens"),
        (r"\bprogres inainte\b|\bavanseaza inainte\b", "mereu", "progres / avansează"),
        (r"\bmijloace mass-?media\b", "mereu", "mass-media"),
        (r"\baniversarea a \d+ ani\b", "mereu", "împlinirea a N ani / aniversarea"),
    ]),
    "repetitie_mascata": ("minor", [
        (r"\bclar si usor de inteles\b", "mereu", "clar"),
        (r"\beficient si productiv\b", "mereu", "alege unul"),
        (r"\brapid si intr-un timp scurt\b", "mereu", "rapid"),
        (r"\bsimplu si facil\b", "mereu", "simplu"),
        (r"\butil si benefic\b", "mereu", "alege unul"),
    ]),
    "echilibru_fortat": ("minor", [
        (r"\balegerea (optima|potrivita) depinde de\b", "mereu", "ia o poziție sau dă criteriul"),
        (r"\bdepinde de nevoile (fiecaruia|dumneavoastra|tale)\b", "mereu",
         "ia o poziție sau dă criteriul"),
        (r"\bare (propriile |si )?avantaje si dezavantaje\b", "la_aglomerare",
         "spune care sunt, concret"),
        (r"\bdepinde de context\b", "la_aglomerare", "spune de ce anume depinde"),
    ]),
    "artefact_chatbot": ("critic", [
        (r"^\s*(sigur|desigur|cu placere)[!,.]", "mereu", "elimină formula de asistent"),
        (r"\bexcelenta intrebare\b", "mereu", "elimină formula de asistent"),
        (r"\bsper ca (te ajuta|va ajuta|informatiile)\b", "mereu", "elimină formula de asistent"),
        (r"\banunta-ma daca\b|\bspune-mi daca (mai )?ai\b", "mereu", "elimină formula de asistent"),
        (r"\bhai sa (analizam|gandim|o luam) pas cu pas\b", "mereu", "elimină formula de asistent"),
        (r"\biata (textul|articolul|varianta) (rescris|rescrisa|final)", "mereu",
         "elimină metacomentariul; livrează doar textul"),
        (r"\bin speranta ca\b", "mereu", "elimină formula de asistent"),
    ]),
    "amprenta_unealta": ("critic", [
        (r"\[numele (tau|dvs|companiei)\]", "mereu", "completează cu date reale sau [DE COMPLETAT: …]"),
        (r"\[(x|y|nume|data|oras|link|url)\]", "mereu",
         "completează cu date reale sau [DE COMPLETAT: …]"),
        (r"\b\d{4}-xx-xx\b|\bxx\.xx\.\d{4}\b", "mereu", "pune data reală"),
        (r"oai_citation", "mereu", "artefact de generare — șterge"),
        (r"cite\s*turn\d+\w*", "mereu", "artefact de generare — șterge"),
        (r"utm_source=(chatgpt|claude|perplexity|gemini)", "mereu", "curăță URL-ul de tracking"),
    ]),
}

# Tipare care depind de caracterele originale (ghilimele, diacritice, cifre) și
# de aceea se aplică pe textul nepliat.
CATEGORII_ORIGINAL = {
    "tipografie_anglicizata": ("minor", [
        (r'"[^"\n]{3,}"', "la_aglomerare", "ghilimele românești: „…”"),
        (r"\b\d+\.\d+\s*(%|la suta|lei|euro)", "mereu", "virgulă zecimală: 3,5"),
        (r"\s—\s.{0,80}\s—\s", "la_aglomerare", "reformulează fără incidentă între linii de pauză"),
    ]),
    "simboluri_excesive": ("minor", [
        # emoji decorative — presărate în proză sau ca marcatori de listă
        (r"[\U0001F300-\U0001FAFF☀-➿←-⇿⬀-⯿️]", "la_densitate",
         "taie emoji decorativ, sau păstrează unul singur dacă tonul e colocvial"),
        # liniuța „-" ca paranteză improvizată în frază (nu cuvânt compus).
        # [ \t], nu \s — \s prinde și newline-ul dinaintea unui marcator de
        # listă („text.\n- alt item"), care nu e deloc același tipar.
        (r"[ \t]-[ \t].{0,80}[ \t]-[ \t]", "la_aglomerare",
         "virgulă, paranteză sau frază nouă în loc de liniuță"),
        # bold/italic dese, tipic markdown de chat, nepotrivit pt. text publicat
        (r"\*\*[^*\n]{2,40}\*\*", "la_densitate", "taie accentuarea sau rezervă-o pentru un singur termen cheie"),
        (r"(?<!\*)\*[^*\n]{2,40}\*(?!\*)", "la_densitate",
         "taie accentuarea sau rezervă-o pentru un singur termen cheie"),
    ]),
}

# Liste cu „-" nu intră în tabelul generic: o listă de 3+ funcționalități sau
# întrebări FAQ e conținut SEO normal, nu abuz — aglomerarea per-paragraf din
# motorul generic ar semnala orice listă obișnuită. Semnalul real e proporția:
# proza integrală transformată în fragmente cu „-" în loc de fraze. Pragurile
# sunt calibrate ca un articol scurt cu o singură listă de 3 puncte (frecvent
# și legitim în conținut SEO) să nu treacă de prag — vezi tests/test_scripts.py
# TestTipare.test_lista_scurta_normala_nu_e_semnalata.
LINIE_LISTA = re.compile(r"^[ \t]*-[ \t]+\S.*$", re.MULTILINE)
PROPORTIE_LISTA_ABUZATA = 0.65
MIN_LINII_PT_PROPORTIE = 10
MIN_CUVINTE_PT_PROPORTIE = 60


def detecteaza_liste_abuzate(text):
    """Detector extra pentru `_comun.scaneaza` — vezi contractul acolo."""
    linii_continut = [l for l in text.splitlines() if l.strip()]
    if (len(linii_continut) < MIN_LINII_PT_PROPORTIE
            or _comun.numara_cuvinte(text) < MIN_CUVINTE_PT_PROPORTIE):
        return [], None
    potriviri = list(LINIE_LISTA.finditer(text))
    if len(potriviri) < _comun.PRAG_AGLOMERARE:
        return [], None
    proportie = len(potriviri) / len(linii_continut)
    if proportie < PROPORTIE_LISTA_ABUZATA:
        return [], None

    rezultate = []
    for m in potriviri:
        start = max(0, m.start() - _comun.CONTEXT_CHARS)
        end = min(len(text), m.end() + _comun.CONTEXT_CHARS)
        fragment = " ".join(text[start:end].split())
        linie = text.count("\n", 0, m.start()) + 1
        rezultate.append({
            "categorie": "simboluri_excesive",
            "severitate": "minor",
            "prag": "proportie",
            "tipar": "liste_abuzate",
            "sugestie": "transformă o parte din liste înapoi în proză",
            "offset": m.start(),
            "sfarsit": m.end(),
            "linie": linie,
            "fragment": fragment,
        })
    depasire = ("simboluri_excesive", "liste_abuzate", len(rezultate),
                f"proportie={proportie:.0%}")
    return rezultate, depasire


DETECTOARE_EXTRA = [detecteaza_liste_abuzate]


SCOR_MAXIM = 6


def calculeaza_scor(raportate, depasiri):
    """Semnale deterministe, 0-6 puncte. Restul rubricii ține de judecata umană."""
    raportate = [r for r in raportate if r["severitate"] != "sub_prag"]
    categorii = {r["categorie"] for r in raportate}
    semnale = []
    tranzitii = sum(1 for r in raportate if r["categorie"] == "structura")
    if tranzitii >= 3:
        semnale.append(("tranzitii_standard_repetate", 1))
    if categorii & {"romgleza", "calc_sintactic"}:
        semnale.append(("calc_din_engleza", 1))
    if categorii & {"introduceri", "umpluturi"}:
        semnale.append(("formule_de_deschidere", 1))
    lexic = sum(1 for r in raportate if r["categorie"] in
                ("vocabular_corporatist", "abstractiuni", "cuantificari_vagi"))
    if lexic >= 3:
        semnale.append(("lexic_corporatist", 1))
    if categorii & {"artefact_chatbot", "amprenta_unealta"}:
        semnale.append(("artefact_de_generare", 2))
    return semnale, sum(p for _, p in semnale)


NOTA_SCOR = ("nota: semnalele despre surse inventate si densitatea de "
             "informatie nu pot fi masurate automat — le evalueaza modelul.")


def main():
    return _comun.ruleaza_cli(
        __doc__, sys.argv[1:], CATEGORII, CATEGORII_ORIGINAL,
        calculeaza_scor, SCOR_MAXIM, eticheta="AI", nota_scor=NOTA_SCOR,
        detectoare_extra=DETECTOARE_EXTRA)


if __name__ == "__main__":
    sys.exit(main())
