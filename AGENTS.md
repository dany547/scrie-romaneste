# AGENTS.md — scrie-romaneste

> Sumar de proiect pentru agenți. Fapte verificate în cod. Repo **public** — orice commit e vizibil imediat.

## Ce este
Skill (instalabil în `.claude/skills/`, `.agents/skills/` etc.) pentru text în română care sună natural,
nu AI: verificare deterministă a tiparelor, ritmului, modelismelor + audit SEO/GEO și de reclame.
Autor: Dan Mutu (adcelerum.ro). Branch `main`, publicare directă.
Punct de intrare: `scripts/verifica.py`; documentația de contract: `SKILL.md` + `README.md`.

## Structură
`SKILL.md` (definiția skill-ului) · `references/{limba,seo,reclame}/` · `scripts/` (verificatoare Python) ·
`tests/test_scripts.py` + `tests/fixtures/` · `README.md`.

## Comenzi
- Test (exact ca în CI): `python -m unittest discover -s tests -v`
  (fără `pyproject.toml`/`pytest.ini`, fără dependențe de instalat; CI rulează pe Python 3.9/3.11/3.13)
- `python3 scripts/verifica.py <fișier>` (citește și de pe stdin): `--json`, `--scor`, `--human-voice`,
  `--reclame`, `--fara-seo`
- Scripturi individuale: `check-tipare.py`, `check-modelisme.py`, `check-ritm.py`, `check-seo.py`,
  `check-human-voice.py`, `check-reclame.py`

## CI / release
- `.github/workflows/tests.yml` (push/PR pe `main`): testele unittest + verificări de contract pe fixture-uri
  (fixture curate rămân curate, fixture rele sunt prinse, textul pe stdin e acceptat).
- `.github/workflows/release.yml`: după CI reușit pe `main` **publică automat tag + GitHub Release**.
  Consecință: un merge pe `main` nu e „doar cod", e o versiune publică. Tag-urile/releases nu se ating manual.

## Ce înseamnă „gata"
- `python -m unittest discover -s tests -v` verde.
- Orice schimbare de **format de output** are test care o fixează + `SKILL.md` și `README.md` actualizate în același commit.

## Zone sensibile
- **Formatul output-ului** e consumat de agenți: coloane, pipe-uri, coduri de ieșire = contract public.
- **Scorul automat e max 13 puncte** (tipare 6 + ritm 3 + modelisme 4), doar penalizări deterministe —
  nu măsoară calitatea; scor mic ≠ text bun.
- Scripturile trebuie să rămână diacritic-insensibile și deterministe (testele verifică).
- Fără date reale de client în repo public sau în exemple.

## Ce nu se atinge (regulă pentru orice agent)
Secrete, `.github/workflows/*`, releases/tags, `main`, Administration. Fix-urile: branch + PR; merge = Dan.

## Severitate
- `BLOCK`: date reale/personale în repo public · schimbare de format fără test + fără update în `SKILL.md` ·
  release publicat cu conținut rupt · scripturi nedeterministe.
- `WARN`: text de referință modificat fără test · exemple/scoruri care induc în eroare ·
  inconsistență `SKILL.md` ↔ `README.md` ↔ `--help`.
- `NIT`: formulare, ordine, spațiere.

## Owner
Dan Mutu (`dany547`, adcelerum.ro)
