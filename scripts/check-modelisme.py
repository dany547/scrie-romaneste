#!/usr/bin/env python3
"""Scanează un text pentru pleonasme etimologice, anglicisme și paronime.

Potrivirea ignoră diacriticele, deci prinde și textul scris fără ele sau cu
sedilă (ş/ţ) în loc de virgulă (ș/ț).

Paronimele se raportează informativ (`minor`, fără contribuție la scor):
detecția e coapariția a două cuvinte în aceeași frază, nu confuzia dintre ele.
Un text care le folosește corect pe amândouă se potrivește la fel de bine.

Fiecare tipar are o severitate (critic/important/minor) și un prag:
    mereu          — semnalat la orice apariție
    la_aglomerare  — semnalat la 3+ în același paragraf sau peste densitate
    la_densitate   — semnalat doar peste densitate

Unde există o corecție canonică, raportul o dă direct după fragment:
    important|pleonasm_etimologic|L4|...hemoragie de sânge...|→ hemoragie

Usage:
    check-modelisme.py <fisier_sau_->
    check-modelisme.py <fisier> --prag 5      # apariții/1000 cuvinte (default 5)
    check-modelisme.py <fisier> --tot         # arată și potrivirile sub prag
    check-modelisme.py <fisier> --scor        # doar scorul de semnale
    check-modelisme.py --help

Exit codes:
    0 = curat (nimic critic sau important, niciun prag depășit)
    1 = potriviri raportate
    2 = eroare de input (fișier lipsă etc.)
"""
import sys

import _comun

# Fereastra de potrivire pentru pleonasme: 25 de caractere. La 80 (valoarea
# inițială) tiparul sărea peste granița de propoziție și raporta drept pleonasm
# construcții corecte — „Hemoragia a fost oprită, dar pacientul pierduse mult
# sânge". Pleonasmul etimologic real stă în aceeași sintagmă, nu la două clauze
# distanță.
CTX = r".{0,25}?"

# Paronimele au nevoie de fereastra largă: semnalul e coapariția în aceeași
# frază. De aceea sunt și informative, nu erori — vezi nota de la `paronimie`.
CTX_FRAZA = r".{0,80}?"

# Tiparele rulează pe textul pliat (fără diacritice) — nu scrie diacritice în
# regex-uri; testul de igienă din tests/ pică dacă apar.
CATEGORII = {
    "pleonasm_etimologic": ("important", [
        (r"\bhemoragi(e|a)\b" + CTX + r"\bde sange\b", "mereu", "hemoragie"),
        # „ortografia corectă a cuvântului X" e uz curent, mai ales didactic —
        # doar sintagma nudă, fără complement, e pleonasmul propriu-zis.
        (r"\bortografi(a|e)\b\s+corecta\b(?!\s+(a|al|ai|ale)\b)", "mereu", "ortografie"),
        (r"\baltitudinea?\b" + CTX + r"\b(inalta|mare)\b", "mereu", "altitudine"),
        (r"\banivers(a|eaza|area)\b" + CTX + r"\b(anii?|un numar|ani)\b", "mereu",
         "împlinirea a N ani / aniversarea"),
        (r"\bsecuritatea\b" + CTX + r"\basigur(a|eaza|and)\b", "mereu",
         "asigură protecția / garantează securitatea"),
        (r"\basigur(a|eaza|and)\b" + CTX + r"\bsecuritatea\b", "mereu",
         "asigură protecția / garantează securitatea"),
        (r"\bavans(eaz|a|and)\b" + CTX + r"\binainte\b", "mereu", "avansează"),
        (r"\bcomemor(eaza|area|a)\b" + CTX + r"\bmemoria\b", "mereu", "comemorează"),
        (r"\bdezvoltare(a)?\b" + CTX + r"\bevolutiva\b", "mereu", "dezvoltare"),
        (r"\bdiurna\b" + CTX + r"\bzilnica\b", "mereu", "diurnă"),
        (r"\bdiurna\b" + CTX + r"\bpe zi\b", "mereu", "diurnă"),
        (r"\blimonada\b" + CTX + r"\bde lamai(e)?\b", "mereu", "limonadă"),
        (r"\bmijloace(le|lor)?\b" + CTX + r"\bmass-?media\b", "mereu", "mass-media"),
        (r"\bmijlocul\b" + CTX + r"\blocului\b", "mereu", "mijlocul"),
        (r"\bdestul\b" + CTX + r"\bde satul\b", "mereu", "sătul"),
        (r"\bdiagrama\b" + CTX + r"\bgrafica\b", "mereu", "diagramă"),
        (r"\beradic(a|heaza|and)\b" + CTX + r"\bdin radacina\b", "mereu", "eradichează"),
        (r"\bmanuscris(ul)?\b" + CTX + r"\bde mana\b", "mereu", "manuscris"),
        (r"\bprima\b" + CTX + r"\bprioritate\b", "mereu", "prioritatea / primul lucru"),
        (r"\badevarul\b" + CTX + r"\badevarat\b", "mereu", "adevărul"),
        (r"\barsita\b" + CTX + r"\barzatoare\b", "mereu", "arșiță"),
        (r"\bcrucificat\b" + CTX + r"\bpe cruce\b", "mereu", "crucificat"),
        (r"\bsaleur(i|e)\b" + CTX + r"\bsarate\b", "mereu", "saleuri"),
        (r"\bconstelati(a|e)\b" + CTX + r"\bstelelor\b", "mereu", "constelație"),
        (r"\bdiseminarea\b" + CTX + r"\bsemintelor\b", "mereu",
         "diseminarea / împrăștierea semințelor"),
        (r"\baduc(e|and|us)\b" + CTX + r"\baport(ul)?\b", "mereu",
         "contribuie / își aduce contribuția"),
        (r"\baport(ul)?\b" + CTX + r"\baduc(e|and|us)\b", "mereu",
         "contribuie / își aduce contribuția"),
    ]),
    "pleonasm_prefix": ("important", [
        # re- = din nou / înapoi
        (r"\brestitu(i|ie)\b" + CTX + r"\binapoi\b", "mereu", "restituie"),
        (r"\brestabilire(a)?\b" + CTX + r"\binapoi\b", "mereu", "restabilire"),
        (r"\brealiment(eaza|a)\b" + CTX + r"\binapoi\b", "mereu", "realimentează"),
        # auto- = de sine
        (r"\bautoportret\b" + CTX + r"\bpropriu\b", "mereu", "autoportret"),
        # co- = împreună
        (r"\bcoexist(a|enta)\b" + CTX + r"\bimpreuna\b", "mereu", "coexistă"),
        # contra- = împotrivă
        (r"\bcontraven(i|ea|it)\b" + CTX + r"\bimpotriva\b", "mereu", "contravine + dativ"),
        # inter- = între
        (r"\b(se )?interpune\b" + CTX + r"\bintre\b", "mereu", "se interpune"),
        (r"\bintervine\b" + CTX + r"\bintre\b", "mereu", "intervine"),
        # pre- = introductiv
        (r"\bprefata\b" + CTX + r"\bintroductiva\b", "mereu", "prefață"),
        # supra- = excesiv
        (r"\bsupraaglomerat(ie|a)\b" + CTX + r"\bexcesiva?\b", "mereu", "supraaglomerare"),
        # hiper- = mare / crescut
        (r"\bhiperaciditat(e|ea)\b" + CTX + r"\b(crescuta|mare)\b", "mereu", "hiperaciditate"),
        # hipo- = mic / joasă
        (r"\bhipotensiune\b" + CTX + r"\bjoasa\b", "mereu", "hipotensiune"),
        # ante- = înainte
        (r"\bantepune\b" + CTX + r"\binainte\b", "mereu", "antepune"),
        # post- = după
        (r"\bpostpune\b" + CTX + r"\bdupa\b", "mereu", "postpune"),
        # -algie = durere
        (r"\bnevralgi(e|a)\b" + CTX + r"\bdureroasa\b", "mereu", "nevralgie"),
        # -ită = inflamație
        (r"\blaringita\b" + CTX + r"\binflamata\b", "mereu", "laringită"),
    ]),
    "pleonasm_diminutiv": ("important", [
        (r"\bcopilas(ul)?\b" + CTX + r"\bmic\b", "mereu", "copilaș"),
        (r"\bfetita\b" + CTX + r"\bmititica\b", "mereu", "fetiță"),
        (r"\bbaietel\b" + CTX + r"\bmititel\b", "mereu", "băiețel"),
        (r"\bcapetel\b" + CTX + r"\bmic\b", "mereu", "căpețel"),
        (r"\bmasuta\b" + CTX + r"\bmica\b", "mereu", "măsuță"),
    ]),
    "pleonasm_reflexiv": ("minor", [
        (r"\bse cearta\b" + CTX + r"\breciproc\b", "mereu", "se ceartă"),
        (r"\bse saluta\b" + CTX + r"\b(reciproc|impreuna)\b", "mereu", "se salută"),
        (r"\bse contrazic\b" + CTX + r"\bunul pe altul\b", "mereu", "se contrazic"),
        (r"\bse saruta\b" + CTX + r"\breciproc\b", "mereu", "se sărută"),
        (r"\bse casatoresc\b" + CTX + r"\bimpreuna\b", "mereu", "se căsătoresc"),
    ]),
    # Pleonasme lexicale de funcție gramaticală și de limbaj comercial: perechi
    # de conectori/adverbe cu sens identic și sintagme din anunțuri în care un
    # termen conține deja sensul celuilalt.
    "pleonasm_lexical": ("important", [
        (r"\bdar insa\b", "mereu", "«dar» sau «însă»"),
        (r"\bdecat numai\b", "mereu", "«decât» sau «numai»"),
        (r"\bprefer(a|ez|am|ati|a)?\b" + CTX + r"\bmai bine\b", "mereu", "preferă"),
        (r"\bmentine\b" + CTX + r"\bin continuare\b", "mereu", "menține"),
        # verbe de mișcare + «înapoi»: direcția e deja în verb
        (r"\b(intors|intoarsa|returnata?|revenit|reintors)\b" + CTX + r"\binapoi\b",
         "mereu", "fără «înapoi»: întors / returnat / revenit"),
        # adjectivul în -bil arată deja posibilitatea
        (r"\b(cu putinta|posibila?|posibile)\b" + CTX + r"\b[a-z]+bil(a|e|ului|ilor|i)?\b",
         "mereu", "taie «cu putință/posibil» — -bil arată deja posibilitatea"),
        # limbaj comercial — erori întâlnite mai ales în anunțuri, dar eroare
        # de registru neutru, nu specifică reclamei
        (r"\bnou(a|e)?\s+inovat\w*\b", "mereu", "o inovație / o noutate"),
        (r"\bcadou\s+gratuit\b", "mereu", "cadou"),
    ]),
    "accentuare_redundanta": ("minor", [
        # «mai» și «încă» adaugă ambele ideea de continuare/persistență;
        # „încă mai” colocvial e acceptabil, deci recitire, nu eroare
        (r"\bmai\b[^.!?\n]{0,60}?\binca\b|\binca\b[^.!?\n]{0,60}?\bmai\b",
         "la_densitate", "păstrează unul singur: «mai» sau «încă»"),
        (r"\bbonus\s+gratuit\b", "mereu", "bonus / gratuit"),
    ]),
    "anglicism": ("minor", [
        (r"\bboy-?band\b", "la_densitate"),
        (r"\bchart-?uri\b", "la_densitate", "topuri / clasamente"),
        (r"\bcover-?ul\b", "la_densitate"),
        (r"\bgirl-?power\b", "la_densitate"),
        (r"\bhomestudio\b", "la_densitate"),
        (r"\bnew-?wave\b", "la_densitate"),
        (r"\bsongwriter-?ita\b", "la_densitate"),
        (r"\bplay-?back\b", "la_densitate"),
        (r"\bcome-?back\b", "la_densitate", "revenire"),
        (r"\bwall-?paper\b", "la_densitate", "imagine de fundal"),
        (r"\bup-?grade\b", "la_densitate", "actualizare"),
        (r"\bparty-?time\b", "la_densitate"),
        (r"\bmaxi-?single\b", "la_densitate"),
        (r"\bnick-?name\b", "la_densitate", "poreclă / pseudonim"),
        (r"\bhair-?styling\b", "la_densitate", "coafat"),
        (r"\bcollege-?shirt\b", "la_densitate"),
        (r"\btank-?shirt\b", "la_densitate", "maiou"),
        (r"\bsuper-?trendy\b", "la_densitate", "la modă"),
    ]),
    # INFORMATIV, nu eroare. Scriptul vede două cuvinte în aceeași frază, nu
    # sensul lor: un text care le folosește corect pe amândouă — sau unul care
    # explică diferența dintre ele — se potrivește la fel de bine. Severitate
    # `minor`, fără contribuție la scor, ca să nu forțeze corecții inutile.
    "paronimie": ("minor", [
        (r"\babilitate\b" + CTX_FRAZA + r"\bagilitate\b", "mereu",
         "abilitate=pricepere, agilitate=sprinteneală — informativ, verifică sensul"),
        (r"\bagilitate\b" + CTX_FRAZA + r"\babilitate\b", "mereu",
         "abilitate=pricepere, agilitate=sprinteneală — informativ, verifică sensul"),
        (r"\bantigel\b" + CTX_FRAZA + r"\bantigen\b", "mereu",
         "antigel=lichid auto, antigen=substanță imunologică"),
        (r"\bantigen\b" + CTX_FRAZA + r"\bantigel\b", "mereu",
         "antigel=lichid auto, antigen=substanță imunologică"),
        (r"\bantinomie\b" + CTX_FRAZA + r"\bantonimie\b", "mereu",
         "antinomie=contradicție logică, antonimie=sens opus"),
        (r"\bantonimie\b" + CTX_FRAZA + r"\bantinomie\b", "mereu",
         "antinomie=contradicție logică, antonimie=sens opus"),
        (r"\batlas\b" + CTX_FRAZA + r"\batlaz\b", "mereu", "atlas=hărți, atlaz=țesătură"),
        (r"\batlaz\b" + CTX_FRAZA + r"\batlas\b", "mereu", "atlas=hărți, atlaz=țesătură"),
        (r"\belipsa\b" + CTX_FRAZA + r"\beclipsa\b", "mereu",
         "elipsă=omisiune/curbă, eclipsă=fenomen astronomic"),
        (r"\beclipsa\b" + CTX_FRAZA + r"\belipsa\b", "mereu",
         "elipsă=omisiune/curbă, eclipsă=fenomen astronomic"),
        (r"\beminent\b" + CTX_FRAZA + r"\biminent\b", "mereu",
         "eminent=remarcabil, iminent=pe cale să se întâmple"),
        (r"\biminent\b" + CTX_FRAZA + r"\beminent\b", "mereu",
         "eminent=remarcabil, iminent=pe cale să se întâmple"),
        (r"\bcompliment\b" + CTX_FRAZA + r"\bcomplement\b", "mereu",
         "compliment=laudă, complement=parte de propoziție/adaos"),
        (r"\bcomplement\b" + CTX_FRAZA + r"\bcompliment\b", "mereu",
         "compliment=laudă, complement=parte de propoziție/adaos"),
        (r"\bconjunctura\b" + CTX_FRAZA + r"\bconjectura\b", "mereu",
         "conjunctură=împrejurare, conjectură=presupunere"),
        (r"\bconjectura\b" + CTX_FRAZA + r"\bconjunctura\b", "mereu",
         "conjunctură=împrejurare, conjectură=presupunere"),
        (r"\bmortal\b" + CTX_FRAZA + r"\bmortar\b", "mereu",
         "mortal=aducător de moarte, mortar=material de construcție"),
        (r"\bmortar\b" + CTX_FRAZA + r"\bmortal\b", "mereu",
         "mortal=aducător de moarte, mortar=material de construcție"),
        (r"\bpadela\b" + CTX_FRAZA + r"\bpedala\b", "mereu", "padelă=vâslă, pedală=la picior"),
        (r"\bpedala\b" + CTX_FRAZA + r"\bpadela\b", "mereu", "padelă=vâslă, pedală=la picior"),
        (r"\bcauzal\b" + CTX_FRAZA + r"\bcazual\b", "mereu", "cauzal=de cauză, cazual=întâmplător"),
        (r"\bcazual\b" + CTX_FRAZA + r"\bcauzal\b", "mereu", "cauzal=de cauză, cazual=întâmplător"),
        (r"\bflagrant\b" + CTX_FRAZA + r"\bfragrant\b", "mereu",
         "flagrant=evident/în fapt, fragrant=parfumat"),
        (r"\bfragrant\b" + CTX_FRAZA + r"\bflagrant\b", "mereu",
         "flagrant=evident/în fapt, fragrant=parfumat"),
    ]),
}


SCOR_MAXIM = 4


def calculeaza_scor(raportate, depasiri):
    raportate = [r for r in raportate if r["severitate"] != "sub_prag"]
    categorii = {r["categorie"] for r in raportate}
    semnale = []
    pleonasme = sum(1 for r in raportate if r["categorie"].startswith("pleonasm"))
    if pleonasme >= 3:
        semnale.append(("pleonasme_etimologice", 1))
    if "anglicism" in categorii:
        n_anglicisme = sum(1 for r in raportate if r["categorie"] == "anglicism")
        if n_anglicisme >= 2:
            semnale.append(("anglicisme_frecvente", 1))
    # `paronimie` nu intră în scor: detecția e coapariție lexicală, nu sens.
    # „Un savant eminent a anunțat un pericol iminent" folosește ambele cuvinte
    # corect și tot s-ar potrivi. Se raportează ca `minor`, spre verificare.
    if depasiri:
        semnale.append(("praguri_depasite", 1))
    return semnale, sum(p for _, p in semnale)


def main():
    return _comun.ruleaza_cli(
        __doc__, sys.argv[1:], CATEGORII, None,
        calculeaza_scor, SCOR_MAXIM, eticheta="modelisme")


if __name__ == "__main__":
    sys.exit(main())
