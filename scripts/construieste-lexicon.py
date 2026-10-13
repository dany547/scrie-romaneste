#!/usr/bin/env python3
"""Regenerează scripts/lexicon/lexicon-ro.txt.gz din dicționarul Rospell.

Doar pentru mentenor: are nevoie de `unmunch` (pachetul hunspell-tools) și de
fișierele `.dic` + `.aff` din Rospell (ex. pachetul npm `dictionary-ro`).
Utilizatorii skill-ului NU rulează asta: lexiconul gata făcut vine din repo.

Rezultatul e o listă de forme flexionate, pliate fără diacritice (aceeași
pliere ca `_comun.pliaza`), sortate și fără duplicate, una pe linie.
Formele cu cratimă nu intră: scriptul de verificare își desparte singur
cuvintele compuse.

Usage:
    construieste-lexicon.py <ro_RO.dic> <ro_RO.aff> [--unmunch CALE] [--out CALE]
"""
import gzip
import subprocess
import sys
from pathlib import Path

import _comun

IMPLICIT = Path(__file__).resolve().parent / "lexicon" / "lexicon-ro.txt.gz"


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 2 or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv and argv[0] in ("-h", "--help") else 2
    dic, aff = argv[0], argv[1]
    unmunch, out = "unmunch", IMPLICIT
    if "--unmunch" in argv:
        unmunch = argv[argv.index("--unmunch") + 1]
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
    try:
        r = subprocess.run([unmunch, dic, aff], capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"eroare: unmunch a esuat: {e}", file=sys.stderr)
        return 2
    forme = set()
    for linie in r.stdout.decode("utf-8").splitlines():
        w = _comun.pliaza(linie.strip())
        if len(w) >= 2 and w.isalpha():
            forme.add(w)
    # mtime=0: același conținut → aceiași bytes (fișier reproductibil în git)
    with gzip.GzipFile(out, "wb", compresslevel=9, mtime=0) as f:
        f.write("\n".join(sorted(forme)).encode("utf-8"))
    print(f"{len(forme)} forme -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
