#!/usr/bin/env python3
"""Numără potriviri, ratări și fals-pozitive pe predicții deja furnizate.

NU rulează niciun model și NU evaluează texte. Primește un fișier de predicții
(ieșirea unei rulări anterioare a fluxului de revizie: `id` + `verdict` per
caz) și le compară cu etichetele din corpusul draft
(`tests/fixtures/evaluare-contextuala.json`, status `draft_nevalidat_uman`).
Etichetele nu sunt validate uman: numărările de aici sunt material de lucru,
nu benchmark și nu performanță măsurată.

Folosire:
    python3 scripts/evaluare-contextuala.py PREDICTII.json [--split referinta|holdout] [--detaliu] [--json]
    python3 scripts/evaluare-contextuala.py - <<'JSON'
    [{"id": "lex-ref-01", "verdict": "eroare"},
     {"id": "lex-ref-02", "verdict": "pastreaza"},
     {"id": "sens-ref-01", "verdict": "suspiciune"}]
    JSON

Fișierul de predicții trebuie să acopere toate id-urile corpusului; cu
`--split referinta|holdout`, doar id-urile splitului ales — predicțiile pentru
celălalt split sunt respinse ca id necunoscut. Un singur id lipsă → exit 1,
fără numărări.

Format predicții: listă JSON `[{"id": ..., "verdict": ...}, ...]` sau obiect
`{"predictii": [...]}`. Verdicte permise: `eroare`, `suspiciune`, `pastreaza`,
`neclar` — aceleași valori ca în corpus. Câmpurile în plus se ignoră.

Numărare — fiecare caz cade în exact o categorie:
- `potrivit`          — verdictul prezis = eticheta;
- `semnal_acceptabil` — eticheta `eroare`/`suspiciune`, prezis celălalt din
  pereche (ambele înseamnă „semnalat");
- `escaladat`         — eticheta `eroare`/`suspiciune`, prezis `neclar`
  (întreabă în loc să corecteze: direcție conservatoare, numărată separat);
- `ratat`             — eticheta `eroare`/`suspiciune`, prezis `pastreaza`;
- `neclar_ratat`      — eticheta `neclar`, prezis altceva (nu a întrebat);
- `fals_pozitiv`      — eticheta `pastreaza`, prezis orice altceva.

Ieșire (text): linii `status|...`, `acoperire|...`, `<split>|k=v k=v ...`,
`total|...`, `nota|...`; cu `--split`, doar splitul ales, iar `total|` repetă
valorile lui; `--detaliu` adaugă
`detaliu|<id>|<split>|eticheta=<v>|prezis=<v>` pentru fiecare caz din afara
`potrivit` (folosește-l pe `referinta`; holdout-ul se măsoară o dată, la
final). `--json` dă același conținut structurat.

Exit: 0 evaluare completă (ratele fac parte din rezultat, nu sunt eroare);
1 predicții incomplete sau invalide (id lipsă/necunoscut/duplicat, verdict
nepermis sau lipsă) — nu se emit numărări; 2 eroare de utilizare (fișier
lipsă/inaccesibil, JSON rupt, corpus invalid).

Fără dependențe: doar biblioteca standard, fără rețea. Determinist: toate
listele din ieșire sunt sortate sau în ordinea corpusului.
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

VERDICTE = ("eroare", "suspiciune", "pastreaza", "neclar")
SEMNAL = ("eroare", "suspiciune")
BUCKETE = ("potrivit", "semnal_acceptabil", "escaladat", "ratat",
           "neclar_ratat", "fals_pozitiv")
SPLITURI = ("referinta", "holdout")
CORPUS_IMPLICIT = (Path(__file__).resolve().parent.parent / "tests" /
                   "fixtures" / "evaluare-contextuala.json")
SCRIPT_EXCEPTIE = "evaluare-contextuala.py"


class EroareUtilizare(Exception):
    """Fișier lipsă/inaccesibil, JSON rupt sau corpus invalid — exit 2."""


def _citeste_json(cale):
    """Conținutul parsat al fișierului; `-` citește stdin."""
    try:
        text = sys.stdin.read() if cale == "-" else Path(cale).read_text(
            encoding="utf-8")
    except OSError as e:
        raise EroareUtilizare(f"fișier inaccesibil: {e}")
    except UnicodeDecodeError as e:
        raise EroareUtilizare(f"fișier non-UTF-8: {e}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise EroareUtilizare(f"JSON rupt: {e}")


def _incarca_corpus(cale):
    """{id: (eticheta, split)}, statusul corpusului; validare strictă."""
    date = _citeste_json(str(cale))
    if not isinstance(date, dict) or not isinstance(date.get("cases"), list):
        raise EroareUtilizare("corpus invalid: lipsesc cheile status/cases")
    etichete = {}
    for caz in date["cases"]:
        cid = caz.get("id") if isinstance(caz, dict) else None
        if not isinstance(cid, str) or not cid or cid in etichete:
            raise EroareUtilizare(f"corpus invalid: id lipsă sau duplicat la {cid!r}")
        if caz.get("expected_verdict") not in VERDICTE:
            raise EroareUtilizare(
                f"corpus invalid: verdict nepermis la {cid}: "
                f"{caz.get('expected_verdict')!r}")
        if caz.get("split") not in SPLITURI:
            raise EroareUtilizare(
                f"corpus invalid: split necunoscut la {cid}: {caz.get('split')!r}")
        etichete[cid] = (caz["expected_verdict"], caz["split"])
    return etichete, date.get("status", "necunoscut")


def _incarca_predictii(date):
    """{id: verdict} + lista id-urilor duplicate; structură, nu acoperire."""
    if isinstance(date, dict):
        date = date.get("predictii")
    if not isinstance(date, list):
        raise EroareUtilizare(
            'predicții invalide: listă JSON [{"id", "verdict"}] sau '
            '{"predictii": [...]}')
    prezise = {}
    duplicate = []
    for intrare in date:
        if not isinstance(intrare, dict):
            raise EroareUtilizare(
                "predicții invalide: fiecare intrare e obiect cu id și verdict")
        cid = intrare.get("id")
        if not isinstance(cid, str) or not cid:
            raise EroareUtilizare("predicții invalide: intrare fără id")
        if cid in prezise:
            duplicate.append(cid)
            continue
        prezise[cid] = intrare.get("verdict")
    return prezise, duplicate


def _bucket(eticheta, prezis):
    """Categoria pentru un caz; acoperă toate combinațiile, fără rest."""
    if prezis == eticheta:
        return "potrivit"
    if eticheta in SEMNAL:
        if prezis == "neclar":
            return "escaladat"
        if prezis == "pastreaza":
            return "ratat"
        return "semnal_acceptabil"
    if eticheta == "neclar":
        return "neclar_ratat"
    return "fals_pozitiv"


def _numara(etichete, prezise):
    """Counter per split + total și lista detaliilor din afara potrivit."""
    numaratori = {split: Counter() for split in SPLITURI}
    numaratori["total"] = Counter()
    detaliu = []
    for cid, (eticheta, split) in etichete.items():
        b = _bucket(eticheta, prezise[cid])
        numaratori[split][b] += 1
        numaratori["total"][b] += 1
        if b != "potrivit":
            detaliu.append({"id": cid, "split": split, "eticheta": eticheta,
                            "prezis": prezise[cid]})
    detaliu.sort(key=lambda d: d["id"])
    return numaratori, detaliu


def _probleme_acoperire(etichete, prezise, duplicate):
    """Lista problemelor de acoperire/validitate; goală = evaluabil."""
    probleme = [f"id lipsă din predicții: {cid}"
                for cid in sorted(set(etichete) - set(prezise))]
    probleme += [f"id necunoscut în predicții: {cid}"
                 for cid in sorted(set(prezise) - set(etichete))]
    probleme += [f"id duplicat în predicții: {cid}"
                 for cid in sorted(set(duplicate))]
    probleme += sorted(f"verdict nepermis la {cid}: {prezise[cid]!r}"
                       for cid in set(prezise) & set(etichete)
                       if prezise[cid] not in VERDICTE)
    return probleme


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog=SCRIPT_EXCEPTIE,
        description=("Numără potriviri/ratări/fals-pozitive pe predicții deja "
                     "furnizate. Fără modele, fără rețea, fără dependențe."))
    parser.add_argument("predictii",
                        help='fișier JSON de predicții, sau "-" pentru stdin')
    parser.add_argument("--corpus", default=str(CORPUS_IMPLICIT),
                        help=f"implicit: {CORPUS_IMPLICIT}")
    parser.add_argument("--split", choices=SPLITURI,
                        help="numără doar splitul ales (implicit: ambele)")
    parser.add_argument("--detaliu", action="store_true",
                        help="listează cazurile din afara potrivit")
    parser.add_argument("--json", action="store_true",
                        help="ieșire structurată, același conținut")
    args = parser.parse_args(argv)

    try:
        etichete, status = _incarca_corpus(args.corpus)
        if args.split:
            # filtrare înainte de validarea acoperirii și de numărare: id-urile
            # din celălalt split devin necunoscute pentru splitul ales
            etichete = {cid: et for cid, et in etichete.items()
                        if et[1] == args.split}
        date = _citeste_json(args.predictii)
        prezise, duplicate = _incarca_predictii(date)
    except EroareUtilizare as e:
        print(f"eroare|{e}", file=sys.stderr)
        return 2

    probleme = _probleme_acoperire(etichete, prezise, duplicate)
    if probleme:
        for problema in probleme:
            print(f"problema|{problema}")
        print("nota|numărări blocate: corectează predicțiile și rulează din nou")
        return 1

    numaratori, detaliu = _numara(etichete, prezise)
    splits_afisate = (args.split,) if args.split else SPLITURI
    note = [
        f"etichete nevalidate uman (status: {status}): numărări de lucru, "
        "nu benchmark",
        "scriptul compară predicții deja furnizate; nu rulează modele și nu "
        "evaluează texte",
    ]
    detaliu_iesire = detaliu if args.detaliu else []
    if args.json:
        print(json.dumps({
            "status": status,
            "acoperire": {"acoperite": len(etichete), "total": len(etichete)},
            **{split: {b: numaratori[split].get(b, 0) for b in BUCKETE}
               for split in splits_afisate},
            "total": {b: numaratori["total"].get(b, 0) for b in BUCKETE},
            "detaliu": detaliu_iesire,
            "note": note,
        }, ensure_ascii=False, indent=2))
        return 0
    print(f"status|{status}")
    print(f"acoperire|{len(etichete)}/{len(etichete)}")
    for cheie in splits_afisate + ("total",):
        n = numaratori[cheie]
        print(f"{cheie}|" + " ".join(f"{b}={n.get(b, 0)}" for b in BUCKETE))
    for d in detaliu_iesire:
        print(f"detaliu|{d['id']}|{d['split']}"
              f"|eticheta={d['eticheta']}|prezis={d['prezis']}")
    for nota in note:
        print(f"nota|{nota}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
