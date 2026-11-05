# Scrie Românește

> Un skill pentru texte românești firești și omenești, nu pentru formulări care sună a text generat de un model lingvistic.

**Autor:** Dan Mutu — [adcelerum.ro](https://adcelerum.ro)

[**Română**](README.md) | [English](README.en.md)

<a id="what-it-does"></a>

## Ce face

Unește regulile limbii române (gramatică, stil, tipare de text generat de AI) cu optimizarea SEO/GEO, fără să le lase să se încurce una pe alta. Folosește-l când scrii, rescrii, editezi sau revizuiești texte în română: articole, descrieri de produse, pagini web, articole de blog și postări pentru rețele sociale.

<a id="key-features"></a>

### Funcții principale

- **Patru moduri** — `rescriere` (text final, fără comentarii), `audit` (raportează tiparele fără să rescrie), `editare` (modificări puține și precise), `human-voice` (audit separat al reflexelor mecanice de exprimare, cu scor din 30 și blocere stricte).
- **Tipare de text AI** — tranziții mecanice, limbaj corporatist, formulări ezitante și cuantificări vagi. Fiecare intrare are o **înlocuire** și un **prag**: unele expresii sunt greșite în orice context, altele doar când se repetă prea des. Un singur „de asemenea” într-un articol de 2.000 de cuvinte e în regulă; șase nu.
- **Probleme specifice românei** — acord la distanță, regimul prepozițiilor, forme flexionare greșite, cuvinte inventate (filtrul de lexic listează forme suspecte, care trebuie verificate în surse permise și în context, manual, fără extragere automată), calcuri sintactice, confuzii între cuvinte, articularea împrumuturilor și refacerea diacriticelor.
- **Revizie contextuală** — verificarea propoziție cu propoziție a textului final (`references/limba/revizie-contextuala.md`): verb–obiect, sensul expresiei, referent, coerența transformării/comparației/cauzalității, rolul cititorului și registrul. Verdicturile (`eroare susținută` / `suspiciune contextuală` / `preferință` / `neclar`) vin cu dovezi. Se fac cel mult două cicluri audit → editare → reverificare; apoi cazul se escaladează.
- **Gramatică și stil** — punctuație, acord, ortografie, diateză și registre ale limbii (peste 400 de reguli din manuale școlare românești).
- **Modele pozitive de exprimare** — rescrieri adnotate înainte/după, pe registre, care arată ce să scrii, nu doar ce să elimini.
- **Tehnici de scriere** — ritm, concizie, structură și adaptare la public.
- **SEO/GEO** — optimizare on-page și tehnică, comerț electronic, SEO local, cercetarea cuvintelor-cheie, date structurate și optimizare pentru căutarea generativă cu AI.
- **Titluri și cursul articolului** — titluri cu o promisiune concretă și un element de precizie, nu etichete sau titluri de tabloid; începuturi care intră direct în subiect și secțiuni cu ritm variat, nu un șablon cu cinci subtitluri H2.
- **Scripturi de verificare** — scaner de tipare (insensibil la diacritice și atent la morfologie), analizor stilometric al ritmului, verificator de structură SEO și filtru de forme suspecte, de verificat în sursele permise, nu doar în DEX (căutare manuală).

<a id="installation"></a>

## Instalare

<a id="optional-hunspell-setup"></a>

### Configurarea opțională a Hunspell

Skill-ul are nevoie doar de Python 3.9+ pentru scripturi și nu depinde de pachete pip. Hunspell este necesar numai pentru opțiunea `check-cuvinte.py --sugestii`. Parametrul `--dictionar` este opțional și alege un dicționar diferit de cel implicit, `ro_RO`. Nimic nu se instalează automat; comenzile de mai jos trebuie rulate de tine.

**Debian / Ubuntu**

```bash
sudo apt update
sudo apt install hunspell hunspell-ro
hunspell -v    # engine version
hunspell -D    # lists installed dictionaries; ro_RO should appear
```

**macOS**

```bash
brew install hunspell
```

Homebrew instalează motorul `hunspell`. Nu am verificat fiecare resursă inclusă în formulă, așa că nu presupune ce mai conține. Dicționarul românesc (`ro_RO.dic` + `ro_RO.aff`) nu este garantat; verifică folosind `hunspell -D` și, dacă lipsește `ro_RO`, instalează un dicționar din resursele distribuției tale.

**Alte sisteme (Windows, alte distribuții Linux etc.)**

- Adaugă în `PATH` un executabil `hunspell` compatibil.
- Instalează o pereche autorizată de fișiere pentru dicționarul românesc: `ro_RO.dic` și `ro_RO.aff`, cu aceeași bază de nume.
- Transmite dicționarul fără extensie: `--dictionar /path/to/ro_RO`. Fără `--dictionar`, motorul caută numele implicit `ro_RO`.

Surse oficiale: <https://hunspell.github.io/> și resursele pentru dicționare ale distribuției tale. Configurarea nu a fost verificată pe Windows.

**Diagnostic.** Dacă `hunspell -D` nu afișează `ro_RO`, o rulare cu `--sugestii` și dicționarul implicit se încheie cu exit 2 când raportul afișează forme suspecte. Regula nu se aplică dacă indici explicit `--dictionar /path/prefix`: acel dicționar poate fi folosit chiar dacă nu se află în calea de căutare. Fără `--sugestii`, verificatorul lexical rulează normal și nu apelează Hunspell.

**Teste rapide** (din directorul skill-ului, cu diacritice păstrate și codare UTF-8). Înlocuiește `/path/to/ro_RO` cu prefixul dicționarului tău înainte să rulezi a doua comandă:

```bash
printf 'Cerul era arămriu deasupra dealurilor.\n' | python3 scripts/check-cuvinte.py - --sugestii
printf 'Cerul era arămriu deasupra dealurilor.\n' | python3 scripts/check-cuvinte.py - --sugestii --dictionar /path/to/ro_RO
```

Exit 1 este un rezultat normal numai dacă Hunspell rulează cu succes folosind dicționarul necesar: înseamnă că forma a fost listată pentru verificare, nu că a eșuat comanda. Dacă există forme suspecte, dar motorul Hunspell sau dicționarul lipsește ori dă eroare, comanda se încheie cu exit 2. Pentru `arămriu` s-ar putea sugera `arămiu`; ordinea exactă depinde de versiunea dicționarului și nu este garantată. Sugestiile nu se aplică automat și nu confirmă existența sau sensul unui cuvânt.

### Claude Code

Copiază directorul skill-ului în proiect:

```bash
# In your project root
mkdir -p .claude/skills
cp -r /path/to/scrie-romaneste .claude/skills/scrie-romaneste
```

Sau instalează-l global:

```bash
mkdir -p ~/.claude/skills
cp -r /path/to/scrie-romaneste ~/.claude/skills/scrie-romaneste
```

Skill-ul se activează automat când ceri să scrii un text în română.

### OpenAI Codex CLI

```bash
# In your project root
mkdir -p .agents/skills
cp -r /path/to/scrie-romaneste .agents/skills/scrie-romaneste
```

Sau instalează-l global:

```bash
mkdir -p ~/.agents/skills
cp -r /path/to/scrie-romaneste ~/.agents/skills/scrie-romaneste
```

### Kilo CLI

```bash
# In your project root
mkdir -p .claude/skills
cp -r /path/to/scrie-romaneste .claude/skills/scrie-romaneste
```

Kilo folosește aceeași structură de directoare `.claude/skills/`. Skill-ul se încarcă prin instrumentul `skill`.

### Cursor

```bash
# In your project root
mkdir -p .cursor/rules
```

Apoi creează `.cursor/rules/scrie-romaneste.md` cu acest conținut:

```markdown
---
globs: "*.md,*.txt,*.html"
alwaysApply: false
description: "Romanian text generation and review skill"
---
```

Copiază conținutul din `SKILL.md` în acel fișier sau indică fișierul:

```bash
cp /path/to/scrie-romaneste/SKILL.md .cursor/rules/scrie-romaneste.md
```

### Windsurf / Devin Desktop

```bash
# In your project root
mkdir -p .windsurf/rules
cp /path/to/scrie-romaneste/SKILL.md .windsurf/rules/scrie-romaneste.md
```

Sau pentru Devin:

```bash
mkdir -p .devin/rules
cp /path/to/scrie-romaneste/SKILL.md .devin/rules/scrie-romaneste.md
```

### Cline

Cline poate citi nativ mai multe formate de skill:

```bash
# As a skill (recommended)
mkdir -p .cline/skills
cp -r /path/to/scrie-romaneste .cline/skills/scrie-romaneste

# Or as rules
mkdir -p .clinerules
cp /path/to/scrie-romaneste/SKILL.md .clinerules/scrie-romaneste.md
```

Cline citește și `.claude/skills/`, și `.cursorrules`, așa că îl va găsi dacă este deja instalat pentru alt instrument.

### Continue.dev

```bash
mkdir -p .continue/rules
cp /path/to/scrie-romaneste/SKILL.md .continue/rules/scrie-romaneste.md
```

### Aider

```bash
# Copy the skill contents to your project
cp -r /path/to/scrie-romaneste ./CONVENTIONS.md

# Or reference it in .aider.conf.yml:
# read: [scrie-romaneste/SKILL.md]
```

Aider încarcă regulile prin `--read` sau `.aider.conf.yml`.

### GitHub Copilot

```bash
mkdir -p .github
cp /path/to/scrie-romaneste/SKILL.md .github/copilot-instructions.md
```

Pentru instrucțiuni specifice unor căi:

```bash
mkdir -p .github/instructions
cp /path/to/scrie-romaneste/SKILL.md .github/instructions/romanian-text.instructions.md
```

Adaugă `applyTo: "*.md"` în frontmatter pentru a limita aplicarea.

### Hermes Agent

```bash
mkdir -p ~/.config/hermes/docs
cp -r /path/to/scrie-romaneste ~/.config/hermes/docs/scrie-romaneste
```

<a id="file-structure"></a>

## Structura fișierelor

```
scrie-romaneste/
├── SKILL.md                        # Main skill definition (load this)
├── references/
│   ├── limba/
│   │   ├── anti-tipare-ai.md       # AI clichés with replacements + thresholds
│   │   ├── exemple-voce.md         # Annotated before/after rewrites, by register
│   │   ├── revizie-contextuala.md   # Sentence-by-sentence sense pass: verdict + evidence
│   │   ├── human-voice-validator.md # Separate voice audit: A–J categories, score, blockers
│   │   ├── cli-verificare.md        # Detailed CLI manual; load before advanced or per-script use
│   │   ├── flux-exemplu.md         # One complete run: request → contract → draft → report → delivery
│   │   ├── tipare-ro.md            # Romanian-specific failure modes
│   │   ├── gramatica-stil.md       # Agreement, punctuation, spelling, pleonasms
│   │   ├── scris-eficient.md       # Process techniques: draft/edit, rhythm, concision
│   │   ├── modelisme.md            # Etymological pleonasms, anglicisms, paronyms
│   │   ├── calcuri.json            # Static registry of collocations to review (check-calcuri.py, opt-in)
│   │   └── scoring-checklist.md    # Pre-delivery language checklist
│   └── seo/                        # Split by topic so agents load only what a task needs
│       ├── core.md                 # Technical, on-page, content, Romanian-specific
│       ├── grounding.md            # Business data that must never be invented
│       ├── titluri.md              # Titles, H1, subheads, meta — not labels
│       ├── flux-articol.md         # Opening, section rhythm, ending, original perspective
│       ├── geo.md                  # Generative Engine Optimization (AI search)
│       ├── schema.md               # JSON-LD / structured data
│       ├── ecommerce.md            # Product and category pages
│       ├── blog-keyword.md         # Blog content + keyword research
│       ├── local.md                # NAP, Google Business Profile
│       ├── avansat.md              # Link building, advanced technical, audits
│       └── scoring-checklist.md    # Pre-delivery SEO/information-density checklist
│   ├── reclame/                    # Paid ads — thin layer over the general rules
│   │   ├── platforme.md            # Google/Meta/PMax limits, TikTok (unverified), file format
│   │   └── voce.md                 # Promise→proof→CTA, positive models, native ads
│   └── social/                     # Organic posts and personal blog (not SEO articles)
│       ├── README.md               # Index by genre + "numbers only with a source"
│       ├── organic.md              # Instagram, Facebook, LinkedIn, TikTok, forum
│       └── blog-personal.md        # Personal/lifestyle blog voice
├── scripts/
│   ├── verifica.py                 # Orchestrator: all checks, one call, combined score
│   ├── check-tipare.py             # AI clichés, calques, generation artefacts, non-normative forms
│   ├── check-human-voice.py        # Conversational filler, punchlines, promo voice, contamination
│   ├── check-ritm.py               # Sentence/paragraph uniformity (stylometry)
│   ├── check-cuvinte.py            # Forms missing from the Rospell lexicon -> suspect list for permitted sources
│   ├── check-calcuri.py            # Opt-in flagger for verb+object collocations to review (static registry)
│   ├── _hunspell.py                # Opt-in Hunspell suggestions helper (local engine + external dictionary)
│   ├── construieste-lexicon.py     # Maintainer only: rebuild lexicon/ from Rospell (needs unmunch)
│   ├── lexicon/                    # lexicon-ro.txt.gz (MPL/LGPL, not MIT) + completari.txt + licence texts
│   ├── check-modelisme.py          # Pleonasms (incl. commercial), anglicisms, paronyms
│   ├── check-reclame.py            # Ad copy only: character limits, platform policies, empty claims
│   ├── check-seo.py                # Headings and keyword stuffing
│   ├── evaluare-contextuala.py     # Offline pilot: counts supplied predictions vs the draft corpus (no models)
│   └── _comun.py                   # Shared scanning engine (not a CLI)
├── LICENSE                         # MIT (the lexicon word list keeps its own licence)
└── tests/                          # Fixtures + unittest suite (stdlib only)
```

<a id="verification-scripts"></a>

## Scripturi de verificare

```bash
python3 scripts/verifica.py <file>          # all checks in one pass + combined score
python3 scripts/verifica.py <file> --json   # structured output for programmatic use
python3 scripts/verifica.py <file> --scor   # scores only
python3 scripts/verifica.py <file> --prag N   # density threshold (appearances/1000 words)
python3 scripts/verifica.py <file> --fara-seo  # skip SEO checks (literary text)
python3 scripts/verifica.py <file> --human-voice  # separate voice audit: AI_PATTERN_SCORE/30, STATUS, blockers
python3 scripts/verifica.py <file> --reclame [--platform google|meta] [--brand "Nume"]  # ad-copy audit (labeled files only)

python3 scripts/check-tipare.py <file>      # AI clichés and calques only
python3 scripts/check-tipare.py <file> --tot  # also show sub-threshold matches
python3 scripts/check-human-voice.py <file> # mechanical voice reflexes only
python3 scripts/check-ritm.py <file>        # rhythm uniformity only
python3 scripts/check-cuvinte.py <file>     # forms missing from the lexicon, to check on dexonline (exit 0 clean, 1 forms to check, 2 input/lexicon error)
python3 scripts/check-cuvinte.py <file> --allow terms.txt --tot  # confirmed terms to skip; show all (default cap 10); --lexicon PATH overrides the bundled list
python3 scripts/check-cuvinte.py <file|-> --sugestii [--dictionar ro_RO] [--allow terms.txt] [--tot]  # opt-in spelling suggestions via local Hunspell
python3 scripts/check-calcuri.py <file>     # suspicious verb+object collocations to review (opt-in)
python3 scripts/check-calcuri.py <file|-> --fereastra N --registry PATH  # word window (default 10) and an alternative registry
python3 scripts/check-modelisme.py <file>   # pleonasms/paronyms only
python3 scripts/check-seo.py <file>         # SEO structure + title register (clickbait, template, label)
python3 scripts/check-reclame.py <file>     # ad copy only: limits, policies, empty claims
```

<a id="spelling-suggestions-opt-in-hunspell"></a>

### Sugestii de ortografie (Hunspell, opțional)

Instrucțiunile de configurare sunt la [Configurarea opțională a Hunspell](#optional-hunspell-setup).

`check-cuvinte.py --sugestii` cere sugestii pentru formele necunoscute deja afișate, folosind un motor Hunspell instalat local (programul în `PATH` și un dicționar instalat separat): cel mult 5 variante pentru fiecare formă, fără aplicare automată și fără dependențe noi dacă nu este folosit flag-ul. `--dictionar` primește numele unui dicționar sau prefixul unei căi fără `.dic`/`.aff` și cere `--sugestii`; formele permise prin `--allow` și completările protejate rămân neschimbate. Liniile cu sugestii apar numai la cerere: `sugestii|L<n>|forma|v1 / v2`, sau `sugestii|L<n>|forma|fără sugestii` dacă nu există variante. Exit 2 dacă motorul sau dicționarul lipsește ori dă eroare și există forme suspecte de afișat; motorul nu pornește când nu există forme afișate sau când euristica suprimă lista pentru un text predominant neromânesc. Scorul /13, `verifica.py` și codurile de ieșire 0/1/2 rămân neschimbate. Sugestiile nu confirmă nici existența, nici sensul cuvântului; versiunile de dicționar diferă, iar instrumentul nu este un corector semantic.

Exit 0 = text fără semnale, 1 = semnale găsite, 2 = eroare de intrare. Rulează `--help` pentru detalii. Când un tipar are o corecție consacrată, raportul o include după citat (`|→ are sens`), astfel încât agentul să poată corecta textul fără să deschidă mai întâi fișierele de referință.

Potrivirea ignoră diacriticele, deci verifică și textele fără diacritice sau cu sedilele vechi `ş/ţ` în locul virgulei corecte dedesubt `ș/ț`. Tiparele recunosc forme flexionate, nu doar forma de dicționar.

<a id="collocation-review-opt-in"></a>

### Verificarea colocărilor (opțional)

`check-calcuri.py` semnalează perechi verb–obiect dintr-un registru static restrâns (`references/limba/calcuri.json`; în prezent, forme ale verbului „a frâna” apropiate de forme ale lui „încărcare”, în aceeași propoziție și într-o fereastră limitată de cuvinte — `--fereastra N` sau `--fereastra=N`, implicit 10; `--registry PATH` sau `--registry=PATH` înlocuiește registrul). Potrivirea nu ține cont de diacritice sau majuscule. Forma ambiguă „frâna” este recunoscută ca verb doar dacă este precedată imediat de un marcator de infinitiv/viitor/modalitate („a frâna”, „pot frâna”); substantivul și imperfectul fără marcator nu sunt semnalate. Sunt excluse și excepțiile legitime din registru (compuse despre sistemul de frânare, substantivul „încărcător”), precum și „încărcătură” (marfa, nu procesul).

Frânarea fizică în apropierea cuvântului „încărcare” („Camionul frânează la rampa de încărcare”) este un fals pozitiv documentat: apare un mesaj neutru care cere recitirea, fără să presupună un calc sau un text de pe un site. Rădăcina obiectului se potrivește și cu adjectivul participial „încărcat”, așa că poate fi semnalată și o propoziție legitimă precum „Camionul încărcat frânează greu în curte”; acesta este un alt fals pozitiv acceptat, care cere doar recitire și nu reprezintă un verdict. Argumentele necunoscute sunt refuzate cu exit 2, nu ignorate în tăcere. Liniile raportului au forma `minor|colocare_de_verificat|L<line>|fragment|→ suggestion`, urmate de liniile `total=` și `nota:`; fragmentele pot conține `|`, deci citește-le ca text. Semnalul cere o revizie, nu confirmă un calc și nu este o eroare: fereastra numără cuvinte, nu analizează sintaxa, iar verdictul se dă la revizia contextuală. Registrul se extinde numai cu colocări verificate manual (surse permise, fără date de client), niciodată automat dintr-un corpus. Verificatorul nu face parte din `verifica.py` și nu contribuie la scorul /13. Exit 0 = nimic de recitit, 1 = cel puțin o pereche de verificat (rezultat normal), 2 = eroare de intrare, registru sau argument necunoscut.

<a id="offline-evaluation-contextual-revision-pilot"></a>

### Evaluare offline (pilotul de revizie contextuală)

`scripts/evaluare-contextuala.py` nu verifică textul și nu rulează modele: numără potrivirile, omisiunile și alarmele false dintr-un fișier cu predicții **deja furnizate** (un obiect `{"id", "verdict"}` pentru fiecare caz — rezultatul unei rulări anterioare), comparându-le cu corpusul de lucru `tests/fixtures/evaluare-contextuala.json` (`draft_nevalidat_uman`: etichetele nu au fost validate de un om, deci valorile sunt orientative și nu reprezintă un benchmark).

```bash
python3 scripts/evaluare-contextuala.py predictii.json [--split referinta|holdout] [--detaliu] [--json]
```

- Predicțiile trebuie să acopere toate ID-urile din corpus sau, cu `--split`, toate ID-urile din splitul ales. ID-urile din celălalt split sunt respinse ca necunoscute. ID-uri lipsă, necunoscute sau duplicate, precum și verdicturile invalide opresc evaluarea (exit 1), fără numărarea rezultatelor.
- Grupe, fiecare caz fiind într-una singură: `potrivit`, `semnal_acceptabil` (schimb între eroare și suspiciune), `escaladat` (s-a întrebat în loc să se corecteze), `ratat`, `neclar_ratat`, `fals_pozitiv`. Liniile de ieșire: `status|`, `acoperire|`, `<split>|k=v`, `total|`, `nota|`; cu `--split` este afișat doar splitul ales, iar `--detaliu` listează cazurile diferite de `potrivit`.
- Codurile de ieșire diferă de cele ale scripturilor de verificare de mai sus: 0 = evaluare completă, 1 = predicții incomplete sau invalide, 2 = eroare de fișier, JSON sau corpus.
- Folosește doar biblioteca standard, offline și determinist. Iterează pe `referinta`; măsoară `holdout` o singură dată, la final. Testele structurale verifică doar suprapunerea literală de șase cuvinte cu ghidul, nu absența unei contaminări semantice.

**Despre `check-ritm.py`:** pragurile sale provin din corpusuri în limba engleză și pot semnala prea multe probleme în registre formale. Ratele publicate de rezultate fals pozitive pentru această categorie de detector depășesc 60% la autorii care nu scriu în limba maternă. Tratează un scor slab ca pe un motiv de recitire, nu ca pe o dovadă că textul a fost scris de o mașină.

```bash
python3 -m unittest discover tests
```

<a id="releasing"></a>

## Publicarea unei versiuni

Un commit pe `main` cu subiectul `vX.Y.Z: rezumat` declanșează o versiune. Este permis și un sufix de pre-lansare (`vX.Y.Z-alpha:`). După ce trece workflow-ul `tests`, workflow-ul `release` creează tag-ul adnotat dacă nu ai trimis deja unul, apoi publică un GitHub Release pornind de la mesajul commitului. Un tag existent nu este mutat niciodată. Pentru a publica un tag care se află deja în repo, rulează manual workflow-ul `release` și setează `tag` la `vX.Y.Z`.

<a id="version"></a>

## Istoricul versiunilor

- **v0.14.1** — Test de vechime pentru limitele platformelor: `platforme.md` trebuie să aibă data verificării în antet, iar peste 6 luni testul dă avertisment (nu eșec). 355 de teste.
- **v0.14.0** — Audit pe texte de modele mici și strat nou pentru social media. Auditul a arătat că textele a trei modele ieftine treceau cu `PASS` deși aveau diacritice lipsă, resturi de cod și reflexe de chat. Detectoare noi în `check-tipare.py`: `diacritice_lipsa` (pe paragraf, fără lexicon: proporția cuvintelor cu diacritice și forme care nu există fără ele), `rest_cod` (cod, HTML și variabile de șablon în proză), `engagement_bait` (cereri artificiale de interacțiune, `minor`) și `artefact_chatbot` extins la introduceri și încheieri de chat („Perfect!”, „Iată setul…”, „Dacă vrei, pot extinde…”). `check-human-voice.py` primește `testat_pe_mine` (mărturie de testare personală neconfirmată, fără scutire de context). `check-cuvinte.py` nu mai verifică hashtag-urile ca cuvinte. Corectură Meta: textul principal 150 și titlul 27 de caractere, conform ghidului oficial citit la 2026-11-05; cifrele 125/40/25 nu mai au sursă oficială, iar descrierea nu mai are recomandare. Parserul `check-reclame.py` nu mai tratează un rând de hashtag-uri drept titlu și verifică `Description:` de sub un titlu Meta. Referințe noi: `references/social/` (`README.md`, `organic.md`, `blog-personal.md`), cu limite doar din surse oficiale și restul marcat „neverificat”; `platforme.md` primește Performance Max și TikTok (CTA oficiale, limitele de text neverificate); `voce.md` primește reclame native. `anti-tipare-ai.md` §K descrie reflexele literare ale modelelor mici, iar pasul DRAFT cere scris pe bucăți. `docs/audit-modele/` păstrează findings, planurile și criticile. 354 de teste. TikTok în `check-reclame.py` și detectorul de hashtag-uri fără diacritice au fost amânate deliberat (fără limite oficiale, respectiv fals pozitive pe `#romania`).
- **v0.13.0** — Adaugă detectorul opțional `check-calcuri.py`, care verifică colocările verb–obiect înregistrate, în prezent frânare + încărcare. Nu are scor și nu intră în `verifica.py`; semnalele neutre cer revizie contextuală, nu sunt verdicte. Exemplele documentate includ infinitivele (`a frâna`, `pot frâna`) și frânarea fizică legitimă în apropierea încărcării; rădăcina prinde și participii, astfel că poate fi semnalată propoziția „Camionul încărcat frânează greu în curte”. Formele substantivale `frânarea`, `frânare` și `frânări` sunt excluse din potrivirea contextuală cu infinitivul. Cazurile evaluării contextuale offline sunt o ciornă nevalidată, nu un benchmark. Detectorul folosește un registru static restrâns și o fereastră de cuvinte, nu sintaxa; poate da rezultate fals pozitive, iar fiecare semnal cere verificare umană.
- **v0.12.0** — Rutarea skill-ului și pilotul de evaluare offline. `SKILL.md` începe acum cu rețeta minimă și contractele a căror încălcare îi afectează pe agenți (schema liniilor pe secțiune, câmpuri separate prin `|`, exit 0/1/2 și scor maxim /13) și indică referințele înainte de folosire. Manualul CLI detaliat a fost mutat în `references/limba/cli-verificare.md` și se citește doar înainte de utilizarea avansată sau individuală a scripturilor. Ghidul de revizie contextuală adaugă exemple lucrate de tip greșit → corect, cu un pas de control: corecția se recitește pentru sens, repetiție, adresare, registru și fapte. Noul `scripts/evaluare-contextuala.py` nu verifică text și nu rulează modele; numără potriviri, semnale acceptabile, escaladări, omisiuni și rezultate fals pozitive în predicții furnizate anterior ca `id` + `verdict`, comparate cu corpusul de lucru de 68 de cazuri (`referinta` 44 / `holdout` 24, etichete încă neverificate de oameni). Are propriile coduri de ieșire (0 evaluare completă, 1 predicții incomplete sau invalide, 2 eroare de fișier ori corpus). `verifica.py`, secțiunile raportului și scorul /13 nu s-au schimbat. 294 de teste.
- **v0.11.0** — Sugestii opționale Hunspell și revizie contextuală. `check-cuvinte.py --sugestii [--dictionar NUME_OR_PREFIX]` cere unui `hunspell` instalat local (în `PATH`), împreună cu un dicționar românesc separat, cel mult 5 variante pentru fiecare formă necunoscută afișată; nimic nu se aplică automat, nu se folosește rețeaua și nu apare nicio dependență nouă fără flag. Instrucțiunile de configurare: [Configurarea opțională a Hunspell](#optional-hunspell-setup). Verificat pe Linux cu Hunspell 1.7.2 și dicționarul românesc LibreOffice 25.2.3 (20 de cazuri, primele variante în 5/5 cazuri de greșeli intenționate; cele 3 cazuri de acord și 4 cazuri contextuale nu au fost detectate). Revizia contextuală (`references/limba/revizie-contextuala.md`) verifică fiecare propoziție și oferă verdicturi cu dovezi; permite cel mult două cicluri audit → editare → reverificare, nu tratează lipsa din lexic ca verdict și folosește numai surse permise. Corpusul sintetic de 60 de cazuri (`tests/fixtures/evaluare-contextuala.json`) este o ciornă, nu a fost validat de un cititor uman și nu reprezintă un benchmark trecut. 249 de teste. Nu este inclus niciun LLM sau motor semantic.
- **v0.10.1** — Verificări mai stricte și fișier de licență. Adaugă licența MIT `LICENSE` (lista de cuvinte Rospell rămâne sub MPL 1.1 / LGPL 2.1). Un benchmark cu forme românești inventate plauzibile și romgleză (`tests/fixtures/cuvinte-grele-*.md`, adevărul de referință verificat pe dexonline) stabilește ce trebuie să listeze `check-cuvinte.py`. Procedura dexonline a acoperit răspunsul HTTP 404 fără corp (istorică, acum înlocuită: căutarea este manuală, fără preluare automată — regula actuală este în `tipare-ro.md` §cuvant_inexistent). 181 de teste.
- **v0.10.0** — Filtru lexical pentru forme posibil inexistente. Noul `check-cuvinte.py` listează formele absente din lexicul derivat din Rospell (`scripts/lexicon/`, MPL 1.1 / LGPL 2.1; restul repo-ului rămâne MIT), fiecare cu adresa sa dexonline. Lista cere verificare, nu este verdict: nu are scor și nu intră în `verifica.py`. Afișează cel mult 10 forme (`--tot` le arată pe toate), acceptă `--allow` pentru termeni confirmați și `--lexicon` pentru altă listă și afișează o singură linie informativă în loc de listă când textul nu este preponderent românesc. Verifică și cuvintele de la începutul propoziției; nu verifică numele proprii din mijlocul ei. `lexicon/completari.txt` conține forme confirmate pe dexonline care lipsesc din Rospell. Procedura dexonline din `tipare-ro.md` explică acum cum se citește pagina, cum se tratează formele flexionate și anglicismele și de ce înlocuitorul trebuie să păstreze același sens și să fie verificat la rândul său. 180 de teste.
- **v0.9.0** — Cuvinte inventate și criterii de finalizare. Niciun script, inclusiv `--human-voice`, nu are dicționar: un raport fără semnale nu dovedește că toate cuvintele există. Înainte de livrare, textul se recitește integral pentru cuvinte inventate, acord și forme verbale. Se caută numai cuvintele incerte, pe rând, la `https://dexonline.ro/definitie/CUVÂNT`. Lipsa unei forme dintr-un dicționar nu dovedește că forma nu există; sugestiile nu confirmă, iar codul HTTP nu dă verdictul. Scrierea unui fișier nu înseamnă că sarcina s-a încheiat: livrabilul modului trebuie să apară în răspuns, iar modificarea se face în fișierul indicat de utilizator, nu într-o copie alăturată. Aceeași precizie pentru instrumente: sedila se verifică și cu `--fara-seo`; un fișier de anunț verificat cu `--reclame` nu mai primește semnale SEO pentru titluri de articol din titlul Markdown; intrarea care nu este UTF-8 primește exit 2, nu o urmă de eroare cu exit 1. 151 de teste.
- **v0.8.0** — Formele DOOM ajung în verificatoarele generale (verbe nenormative, acordul numeralelor, pleonasme lexicale) și apare un strat restrâns pentru reclame: `verifica.py --reclame` verifică limitele Google/Meta, politicile și afirmațiile goale.
- **v0.7.1** — Linia en-dash este interzisă în orice situație; apar și simbolurile de chat. `–` (U+2013) este mutat din categoria `punctuatie_carja`, bazată pe frecvență, în categoria separată `liniuta_engleza`, semnalată la fiecare apariție: româna nu folosește această linie — compusele și intervalele folosesc cratima („10-12 zile”), iar incizele folosesc linia de pauză. Este singura regulă absolută din zona punctuației, cu severitatea `important`, dar rămâne în afara lui `scor_automat` /13. `—` și `-` păstrează pragul de densitate, fiindcă au utilizări legitime. În `simboluri_excesive` se adaugă marcatorii de listă Unicode (`• ▪ ◆ ‣ ·` — Markdown cere `-`), numărați și de detectorul proporției `liste_abuzate`, precum și simbolurile ornamentale de referință (`§ ¶ † ‡ № ™ ‰`), cu prag de densitate pentru ca o citare juridică izolată să nu fie semnalată. Notațiile matematice (`×`, `°`, `±`) sunt excluse intenționat. Unsprezece teste noi; fixture-urile juridice, academice și literare sunt cazuri de control care nu trebuie să fie semnalate.
- **v0.7.0** — Detector pentru linia de pauză folosită ca sprijin mecanic. Noua categorie `punctuatie_carja` din `check-tipare.py` caută tic-ul de model cel mai des întâlnit: `—`, `–` sau `-` folosit repetat ca unic conector între propoziții ori părți de propoziție, în locul virgulei sau punctului. Toate trei caracterele sunt numărate împreună — en-dash-ul `–` nu apărea înainte în niciun tipar — iar detectorul anterior, care verifica doar perechi, a fost mutat în aceeași categorie, astfel încât aceeași secvență să nu fie raportată de două ori. Replicile de dialog, marcatorii de listă (inclusiv cei indentați), intervalele numerice și cuvintele cu cratimă sunt excluse prin construcție, nu printr-o listă de excepții; o linie de pauză împărțită la capăt de rând este totuși detectată. Tiparul are pragul său de densitate (4/1000 de cuvinte), calibrat astfel încât `pereche-dupa.md` — rescrierea de model din repo, cu două linii de pauză în 293 de cuvinte — să nu fie semnalată; `_comun.scaneaza` acceptă acum un prag numeric pe tipar, pe lângă pragurile de tip text. Semnalul este `minor` și nu intră în `scor_automat` /13. Fixture nou `rau-liniuta.md`, opt teste noi (dialogul și rescrierea de model sunt cazuri de control).
- **v0.6.0** — Titluri bine construite și curs firesc al articolului. Apar `titluri.md` (anatomia unui titlu care merită clicul: subiect, promisiune, precizie, unghi — nu o etichetă și nu un titlu de tabloid) și `flux-articol.md` (deschidere fără încălzire, ritm variat al secțiunilor, perspectivă originală stabilită la CONTEXT, final care nu recapitulează). Ambele sunt încărcate global pentru conținutul online, nu doar pentru rândul de blog. `check-seo.py` raportează acum severitatea, ca celelalte verificatoare (fără să contribuie la `scor_automat` /13), și semnalează registrul titlului: clickbait, șabloane de agenție („Ghidul suprem”, „Tot ce trebuie să știi”), titluri-etichete, titluri prea lungi și subtitluri H2 plate. Fixture nou `rau-titlu.md`; `SKILL.md` primește două reguli critice, un criteriu de livrare și rutare pentru fișierele noi.
- **v0.5.3** — Validator de voce umană. Audit separat (`verifica.py <file> --human-voice` sau scriptul autonom `check-human-voice.py`) pentru reflexe mecanice pe care verificările lingvistice nu le detectează: umpluturi conversaționale, punchline-uri, metafore de copywriter, autobiografie fără susținere, promisiuni promoționale, majuscule și contaminare cu conversații sau prompturi, tratate ca blocere stricte. Raportul oferă `AI_PATTERN_SCORE/30` și statusul `PASS`/`EDITED`/`REWRITE`; semnalele cer decizii editoriale, nu corectări automate — metafora literară, tonul colocvial și sloganurile de brand pot fi alegeri legitime. Reguli și procedură în `references/limba/human-voice-validator.md`. Cinci fixture-uri și acoperire completă a testelor; `SKILL.md` primește un mod dedicat și un criteriu de livrare. La un rezultat complet curat, orchestratorul afișează în continuare rezumatul de voce, ca agentul care face auditul să aibă ce raporta. Ordinea flag-urilor din `verifica.py` nu mai contează (înainte, `verifica.py --fara-seo file.md` eșua); lipsa fișierului produce o eroare corectă cu exit 2. CI rulează acum fiecare script pe fiecare fixture (exit ≥ 2 eșuează), confirmă că fixture-urile curate rămân curate și cele negative sunt detectate și face un test rapid cu stdin — cu două clase de teste noi care oglindesc verificările CI.
- **v0.5.0** — Naturalețea primează în fața bifării unei liste.

  *Fluxul de lucru.* Apare pasul `CONTRACT`: genul, cititorul, canalul, registrul și adresarea se stabilesc înainte de draft, nu se deduc după. Dispare pragul global de scor **8/10**: amesteca o rubrică manuală cu numărul determinist de penalizări din `verifica.py` și nu putea fi atins de textele fără SEO; cele două liste de evaluare devin liste de verificare înainte de livrare, cu blocere explicite.

  *Motorul de potrivire.* Se repară o eroare tăcută: orice tipar din mai multe cuvinte care traversa o întrerupere de rând era ratat complet. De acum, spațiul literal dintr-un tipar acceptă și o singură întrerupere de rând care nu începe un paragraf nou, fără să schimbe spațiile din clasele de caractere (tiparul pentru linii de pauză exclude intenționat `\n`, ca să nu recunoască marcatorii de listă). În proză românească cu rânduri împărțite, la 80 de coloane motorul vechi rata aproximativ o potrivire din șase, iar la 40 de coloane jumătate.

  *Detecții noi.* `copula_evitata`, `referinta_vaga` și `simetrie_de_acoperire` numără aparițiile pe familie, nu pe tipar — astfel detectează registrul nominal („reprezintă” de două ori plus „constituie” o dată) și propoziția adresată tuturor, ca să se potrivească oricărei căutări. Niciuna nu contribuie la scor. Abuzul de simboluri (emoji decorative, proză transformată în liste cu liniuțe, linia de pauză folosită ca paranteză improvizată, bold/italic prea des) primește o categorie proprie, cu praguri de abuz, nu interdicții absolute.

  *Rezultate fals pozitive eliminate.* Paronimele devin informative (`minor`, fără scor): detectorul observă co-apariția, nu sensul, și semnala propoziții în care ambele cuvinte erau folosite corect. Fereastra de potrivire a pleonasmelor se restrânge de la 80 la 25 de caractere, ca să nu mai traverseze limitele dintre propoziții. Categoria planificată `sablon_seo` este abandonată: trei expresii aparțin tabelului existent `structura`, iar forma simplă `fie că… fie că` este o conjuncție corelativă obișnuită.

  *Material nou.* `references/limba/exemple-voce.md` aduce rescrieri adnotate înainte/după, în variante neutră și colocvială. `references/limba/flux-exemplu.md` arată un traseu complet, de la cerere la livrare, cu rezultate reale ale scripturilor și cele patru probleme pe care acestea nu le detectează. `scris-eficient.md` scade de la 237 la aproximativ 110 rânduri: dispar materialele despre obiceiurile bloggerilor și se rezolvă contradicțiile cu regulile anti-tipare. `core.md` primește o secțiune despre registrul românesc al textelor de agenție. Se repară și numerotarea secțiunilor SEO (`core.md` sărise de la 3 la 13, rămăseseră cifre după separarea `seo-geo.md`).

  *Ușurința folosirii de către agenți.* `SKILL.md` precizează unde se află scripturile, cum se transmite textul prin stdin, că exit 1 este rezultat normal, nu eșec, cum se citește raportul după severitate, ce se face dacă lipsește `python3`, când se folosește `--json` și cum se răspunde unei cereri care cere simultan audit și rescriere. Permite explicit scrierea fără încărcarea unui fișier de referință, în locul ghicirii conținutului acestuia.

  *Testele cresc de la 39 la 65.* Se adaugă un test de documentație (fiecare `file.md` și `§N` indicat trebuie să existe, iar fiecare fișier de referință trebuie să fie rutat din `SKILL.md`) și trei fixture-uri pentru genurile pe care verificatoarele le-ar putea afecta: texte juridice, academice și literare care conțin intenționat construcțiile detectate.
- **v0.4.0** — Versiune orientată spre eficiența agenților. Noul orchestrator `verifica.py` rulează toate verificările dintr-un singur apel, cu scor determinist combinat (`X/13`), ieșire `--json` și `--fara-seo`. Rapoartele includ acum corecția canonică (`|→ are sens`; paronimele primesc explicații de sens), astfel încât auditul nu mai cere încărcarea fișierelor de referință. `seo-geo.md` (43 KB) este împărțit în opt fișiere tematice, cu tabel de rutare în `SKILL.md`; o sarcină de blog încarcă aproximativ 23 KB în loc de 43 KB. Motorul de scanare comun este extras în `_comun.py` (se elimină aproximativ 150 de linii duplicate). Noul `check-modelisme.py` caută pleonasme etimologice, anglicisme și paronime; se repară ramuri moarte pentru diacritice și rezultate fals pozitive garantate („caut să adopt”, „de aceea”). Testele cresc de la 24 la 39: acoperire pentru modelisme, teste de orchestrator, verificarea igienei tiparelor (fără diacritice în expresiile regulate normalizate) și verificare de neconcordanțe între SKILL și scripturi.
- **v0.3.1** — Descoperirea datelor de fundamentare nu mai depinde de format: skill-ul caută datele de business după conținut în orice tip de fișier, pagină publicată sau mesaj anterior, nu după o listă fixă de nume de fișiere. Gestionează surse contradictorii și explică salvarea datelor confirmate în formatul folosit de proiect. Nu este inclus intenționat un șablon gol de brief: unul completat pe jumătate poate produce date plauzibile, dar false.
- **v0.3.0** — Actualizare SEO/GEO pentru 2026. Se corectează recomandările depășite despre date structurate (rezultatele extinse FAQ au fost retrase în mai 2026, `HowTo` din 2023) și se explică rolul nou al schemei ca semnal de încredere/entitate pentru AI Mode. Sunt adăugate tactici GEO susținute de dovezi din studiul Princeton/KDD 2024 și analize pe corpusuri mari, diferențiate de poziția oficială Google. Apare o secțiune SEO specifică românei: diacritice în interogări, textul paginii și sluguri; romgleză în cercetarea cuvintelor-cheie; țintire `ro-RO`/`ro-MD`. Secțiunea §0 despre datele de business care trebuie găsite în surse sau cerute, niciodată inventate, intră în flux la pasul CONTEXT. `check-seo.py` primește verificări pentru sedile, diacritice în URL și lungimea secțiunilor, precum și primele teste proprii. CI rulează pe Python 3.9/3.11/3.13.
- **v0.2.0** — Trei moduri (rescriere/audit/editare), autocorectare în două treceri și profiluri de voce. Potrivirea tiparelor devine insensibilă la diacritice și ține cont de morfologie (înainte, textele fără diacritice nu erau detectate). Interdicțiile binare sunt înlocuite cu niveluri de severitate și praguri de densitate. Apare `tipare-ro.md`, cu probleme specifice limbii române, și un analizor stilometric al ritmului. Se adaugă suita de teste.
- **v0.1.0-alpha** — Prima versiune. Gramatică și stil din șapte manuale școlare românești, tehnici de scriere din metodologia de eficiență și reguli SEO/GEO din documentația Google actuală la acel moment.

<a id="license"></a>

## Licență

MIT (vezi `LICENSE`), cu excepția `scripts/lexicon/lexicon-ro.txt.gz`: listă de cuvinte derivată din dicționarul românesc Rospell (2005–2013, Rospell Team), folosită sub licențele MPL 1.1 / LGPL 2.1. Textele complete (`MPL-1.1.txt`, `LGPL-2.1.txt`) și nota de atribuire (`LICENTA-ROSPELL.txt`) se află în `scripts/lexicon/`.
