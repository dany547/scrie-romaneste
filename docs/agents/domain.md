# Domain Docs

Cum trebuie să consume skill-urile de engineering documentația de domeniu a acestui repo.

## Înainte de a explora codul, citește

- **`GLOSSARY.md`** la rădăcina repo-ului (dacă există).
- **`docs/adr/`**: deciziile arhitecturale care ating zona în care lucrezi.

Repo-ul e **single-context** (un singur pachet): un `GLOSSARY.md` + `docs/adr/` la rădăcină.

Dacă fișierele nu există, **continuă în silență** — nu semnala absența și nu propune crearea lor
dinainte. Ele se creează leneș, când un termen sau o decizie chiar se clarifică.

## Structură

```
/
├── GLOSSARY.md
├── docs/
│   ├── adr/
│   │   └── 0001-<decizie>.md
│   └── agents/
│       ├── issue-tracker.md   (unde trăiesc issue-urile)
│       ├── triage-labels.md   (vocabularul de triaj)
│       └── domain.md          (fișierul de față)
├── scripts/
└── tests/
```

## Reguli de consum

- Termenii din `GLOSSARY.md` sunt canonici: folosește-i exact în cod, teste, comentarii și issue-uri.
- Un ADR nu se rescrie; dacă decizia se schimbă, se adaugă un ADR nou care îl înlocuiește.
- Dacă un termen lipsește din glosar și îl folosești în cod nou, adaugă-l în același commit.
