#!/usr/bin/env python3
"""Rulează toate verificările (tipare AI, modelisme, ritm, SEO) într-o trecere.

Punctul de intrare recomandat pentru agenți: un singur apel, un raport unic,
scorul combinat calculat automat. Scripturile individuale rămân utile pentru
verificări punctuale.

Raportul păstrează formatul pipe al scripturilor individuale, grupat pe
secțiuni. Scorul automat numără penalizări deterministe, nu calitate (max 13
puncte: tipare 6 + ritm 3 + modelisme 4); naturalitatea, densitatea de
informație și sursele rămân la judecata modelului, după listele din
references/*/scoring-checklist.md. Un scor mic nu garantează un text bun.

Usage:
    verifica.py <fisier_sau_->
    verifica.py <fisier> --fara-seo    # text literar / fără destinație online
    verifica.py [optiuni] <fisier_sau_->   # ordinea optiuni/fișier nu contează
    verifica.py <fisier> --scor        # doar scorurile, fără potriviri
    verifica.py <fisier> --json        # output structurat pentru procesare
    verifica.py <fisier> --prag 5      # densitate apariții/1000 cuvinte
    verifica.py <fisier> --human-voice # audit separat al vocii umane
    verifica.py --help

Exit codes:
    0 = curat pe toate verificările
    1 = cel puțin un semnal raportat
    2 = eroare de input
"""
import json
import sys

import _comun

tipare = _comun.incarca_script("check-tipare")
modelisme = _comun.incarca_script("check-modelisme")
ritm = _comun.incarca_script("check-ritm")
seo = _comun.incarca_script("check-seo")
human_voice = _comun.incarca_script("check-human-voice")

SCOR_MAXIM = tipare.SCOR_MAXIM + 3 + modelisme.SCOR_MAXIM  # 6 + 3 + 4 = 13


def analizeaza_tot(text, prag, cu_seo=True, cu_human_voice=False):
    """Returnează un dict cu rezultatele tuturor verificărilor."""
    rap_t, dep_t, cuvinte = _comun.scaneaza(
        text, tipare.CATEGORII, tipare.CATEGORII_ORIGINAL, prag,
        detectoare_extra=tipare.DETECTOARE_EXTRA)
    semnale_t, scor_t = tipare.calculeaza_scor(rap_t, dep_t)

    rap_m, dep_m, _ = _comun.scaneaza(text, modelisme.CATEGORII, None, prag)
    semnale_m, scor_m = modelisme.calculeaza_scor(rap_m, dep_m)

    a = ritm.analizeaza(text)
    semnale_r = ritm.semnale(a) if a["fraze"] >= 5 else []
    scor_r = ritm.calculeaza_scor(semnale_r)

    probleme_seo = seo.verifica(text) if cu_seo else []

    return {
        "cuvinte": cuvinte,
        "tipare": {"potriviri": rap_t, "depasiri": dep_t,
                   "semnale": semnale_t, "scor": scor_t, "max": tipare.SCOR_MAXIM},
        "modelisme": {"potriviri": rap_m, "depasiri": dep_m,
                      "semnale": semnale_m, "scor": scor_m, "max": modelisme.SCOR_MAXIM},
        "ritm": {"metrici": a, "semnale": semnale_r, "scor": scor_r, "max": 3,
                 "text_prea_scurt": a["fraze"] < 5},
        "seo": {"probleme": probleme_seo, "verificat": cu_seo},
        "human_voice": human_voice.analizeaza(text) if cu_human_voice else None,
        "scor_automat": scor_t + scor_m + scor_r,
        "scor_maxim": SCOR_MAXIM,
    }


def are_semnale(rez):
    return bool(rez["tipare"]["potriviri"] or rez["tipare"]["depasiri"]
                or rez["modelisme"]["potriviri"] or rez["modelisme"]["depasiri"]
                or rez["ritm"]["semnale"] or rez["seo"]["probleme"]
                or (rez["human_voice"] and rez["human_voice"]["potriviri"]))


def ca_json(rez):
    """Variantă serializabilă, fără câmpurile interne (offset, tipar)."""
    def potrivire(r):
        p = {"severitate": r["severitate"], "categorie": r["categorie"],
             "linie": r["linie"], "fragment": r["fragment"]}
        if r.get("sugestie"):
            p["sugestie"] = r["sugestie"]
        return p

    return {
        "cuvinte": rez["cuvinte"],
        "scor_automat": rez["scor_automat"],
        "scor_maxim": rez["scor_maxim"],
        "scoruri": {s: {"scor": rez[s]["scor"], "max": rez[s]["max"],
                        "semnale": [n for n, _ in rez[s]["semnale"]]}
                    for s in ("tipare", "modelisme")}
        | {"ritm": {"scor": rez["ritm"]["scor"], "max": rez["ritm"]["max"],
                    "semnale": [n for n, _, _ in rez["ritm"]["semnale"]]}},
        "tipare": [potrivire(r) for r in rez["tipare"]["potriviri"]],
        "modelisme": [potrivire(r) for r in rez["modelisme"]["potriviri"]],
        "ritm": {"metrici": {k: v for k, v in rez["ritm"]["metrici"].items()
                             if k != "min_max"},
                 "semnale": [{"nume": n, "incredere": i, "detaliu": d}
                             for n, i, d in rez["ritm"]["semnale"]]},
        "seo": [{"categorie": c, "detaliu": d, "context": ctx}
                for c, d, ctx in rez["seo"]["probleme"]],
        "human_voice": (human_voice.ca_json(rez["human_voice"])
                        if rez["human_voice"] else None),
        "de_evaluat_manual": ["naturalitate si ritm perceput", "densitate informatie",
                              "fapte si surse (nimic inventat)", "relevanta pentru public"],
    }


def linie_scor(rez):
    t, m, r = rez["tipare"], rez["modelisme"], rez["ritm"]
    return (f"scor_automat={rez['scor_automat']}/{rez['scor_maxim']} "
            f"(tipare={t['scor']}/{t['max']}, ritm={r['scor']}/{r['max']}, "
            f"modelisme={m['scor']}/{m['max']})")


def tipareste(rez):
    if rez["tipare"]["potriviri"] or rez["tipare"]["depasiri"]:
        print("== tipare AI")
        _comun.tipareste_raport(rez["tipare"]["potriviri"],
                                rez["tipare"]["depasiri"], rez["cuvinte"], "AI")
    if rez["modelisme"]["potriviri"] or rez["modelisme"]["depasiri"]:
        print("== modelisme")
        _comun.tipareste_raport(rez["modelisme"]["potriviri"],
                                rez["modelisme"]["depasiri"], rez["cuvinte"], "modelisme")

    a = rez["ritm"]["metrici"]
    if rez["ritm"]["text_prea_scurt"]:
        print(f"== ritm: text prea scurt pentru statistica ({a['fraze']} fraze)")
    elif rez["ritm"]["semnale"]:
        print("== ritm")
        print(f"metrici|fraze={a['fraze']}|medie={a['lungime_medie']:.1f}"
              f"|deviatie={a['deviatie']:.1f}|cv={a['cv_fraze']:.3f}")
        for nume, incredere, detaliu in rez["ritm"]["semnale"]:
            print(f"{nume}|incredere={incredere}|{detaliu}")

    if rez["seo"]["probleme"]:
        print("== seo")
        for categorie, detaliu, context in rez["seo"]["probleme"]:
            print(f"{categorie}|{detaliu}|{context}")

    if rez["human_voice"]:
        print("== human voice")
        human_voice.tipareste(rez["human_voice"])

    print("---")
    print(linie_scor(rez))
    print("de evaluat manual: naturalitate, densitate informatie, fapte/surse "
          "— listele din references/*/scoring-checklist.md")


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    # Fișierul e primul argument pozițional; „-” e stdin chiar dacă începe cu „-”.
    # Ordinea optiuni/fișier nu contează, dar valoarea lui --prag nu e fișier.
    sursa = None
    for i, arg in enumerate(argv):
        if arg == "--prag" or (i > 0 and argv[i - 1] == "--prag"):
            continue
        if arg == "-" or not arg.startswith("-"):
            sursa = arg
            break
    if sursa is None:
        print("eroare: lipsește fișierul de verificat", file=sys.stderr)
        return 2
    prag = _comun.PRAG_DENSITATE_IMPLICIT
    if "--prag" in argv:
        try:
            prag = float(argv[argv.index("--prag") + 1])
        except (IndexError, ValueError):
            print("eroare: --prag cere un număr", file=sys.stderr)
            return 2

    try:
        text = _comun.citeste_intrare(sursa)
    except OSError as e:
        print(f"eroare: {e}", file=sys.stderr)
        return 2

    rez = analizeaza_tot(text, prag, cu_seo="--fara-seo" not in argv,
                         cu_human_voice="--human-voice" in argv)

    if "--json" in argv:
        print(json.dumps(ca_json(rez), ensure_ascii=False, indent=1))
    elif "--scor" in argv:
        print(linie_scor(rez))
        if rez["human_voice"]:
            human_voice.tipareste(rez["human_voice"], detalii=False)
    elif not are_semnale(rez):
        print(f"0 semnale automate ({rez['cuvinte']} cuvinte) — nu inseamna text "
              "bun, doar ca n-a calcat pe nicio mina automata")
        print(linie_scor(rez))
        if rez["human_voice"]:
            print("== human voice")
            human_voice.tipareste(rez["human_voice"], detalii=False)
        else:
            print("de evaluat manual: naturalitate, densitate informatie, fapte/surse")
    else:
        tipareste(rez)

    return 1 if are_semnale(rez) else 0


if __name__ == "__main__":
    sys.exit(main())
