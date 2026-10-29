# Manual CLI — verificatoarele de text

## Cine îl deschide și când

Agentul care folosește un script individual cu opțiuni ori comportament care nu sunt rezumate în `SKILL.md`, un flag în afara rețetei minime, automatizează sau filtrează rapoarte, depanează un apel ori rulează evaluatorul contextual citește acest fișier **înainte** de comandă sau de interpretarea rezultatului. Aici sunt contractele detaliate de intrare/ieșire, limitele și opțiunile scripturilor. Nu-l încărca pentru o sarcină simplă de scriere sau audit care folosește doar rețeta standard și contractele critice din `SKILL.md`.

## Cum le rulezi

Scripturile stau în directorul skill-ului, **nu** în proiectul utilizatorului. Calea e relativă la `SKILL.md`: dacă acesta e în `~/.claude/skills/scrie-romaneste/`, scripturile sunt în `~/.claude/skills/scrie-romaneste/scripts/`. Notează calea o dată, la primul apel, și refolosește-o.

Textul de verificat e de obicei în conversație, nu într-un fișier. Dă-l pe stdin, cu `-` ca argument:

```bash
python3 <cale-skill>/scripts/verifica.py - <<'TEXT'
Textul de verificat, integral, cu diacritice.
TEXT
```

sau, dacă textul e deja într-un fișier al proiectului:

```bash
python3 <cale-skill>/scripts/verifica.py drafts/articol.md
```

Pe Windows/PowerShell, unde heredoc-ul nu există, scrie textul într-un fișier temporar și dă-i calea. Nu încerca variante de escaping — pierzi diacriticele.

Trei lucruri de știut înainte de primul apel:

- **Exit 1 nu e eroare.** Înseamnă „am găsit semnale" și e rezultatul normal pe un draft. Doar exit 2 e eroare (fișier lipsă, argument greșit, intrare non-UTF-8 — convertește cu `iconv -f WINDOWS-1250 -t UTF-8`, nu reîncerca variante de escaping). Nu raporta utilizatorului că scriptul „a eșuat".
- **`--fara-seo` pentru orice text fără destinație online** — literar, email, document intern. Altfel primești semnale despre H1 și heading-uri pentru un text care n-are așa ceva. Sedila se verifică oricând, inclusiv cu `--fara-seo` — apare sub secțiunea `seo` a raportului (cheia `seo` în JSON): dacă filtrezi „seo" la text literar, pierzi un semnal critic.
- **Dacă `python3` nu există** în mediu, nu insista și nu căuta alternative: sari peste pasul mecanic, spune-o pe scurt și fă verificarea pe listă, din `references/limba/anti-tipare-ai.md`.

## Cum citești raportul

```
severitate|categorie|linie|fragmentul găsit|→ corecția canonică
minor|copula_evitata|L3|…centrale termice reprezintă o decizie…|→ «este», sau …
prag_depasit|copula_evitata|3 aparitii|densitate
```

- `critic` — eroare. Se corectează, fără discuție: artefact de chat, placeholder, calc din engleză, introducere formulaică.
- `important` — aproape sigur de corectat, dar citește fragmentul întâi.
- `minor` — semnal de recitire. Îl păstrezi dacă genul îl cere; îl tai dacă nu adaugă nimic. Nu-l corecta automat.
- `→` apare doar unde există o corecție canonică. Aplic-o adaptând acordul și topica — potrivirea e mecanică, corecția nu.
- `prag_depasit` spune de ce s-a raportat o categorie care singură ar fi fost acceptabilă: prea multe apariții, prea aproape una de alta.

Formatele diferă între secțiuni:

- `tipare` și `modelisme`: `severitate|categorie|L<linie>|fragment[|→ sugestie]`.
- `ritm`: `metrici|...` și `<semnal>|incredere=<nivel>|<detaliu>`, fără `L<n>`. `check-ritm.py` mai emite o linie separată `metrici|paragrafe=...`.
- `seo`: `severitate|categorie|detaliu|context`, fără `L<n>`.
- `human-voice`: `severitate|categorie_cod|subcategorie|L<linie>|fragment|→ sugestie`.
- `reclame`: `severitate|categorie|eticheta|L<linie>|detaliu|→ sugestie`.

Acestea sunt formatele text; pentru procesare programatică folosește `--json`.

`scor_automat=X/13` numără penalizări deterministe, nu calitate. 0/13 nu înseamnă text bun și nu înseamnă că vorbele există: înseamnă doar că n-a călcat pe nicio mină automată.

Secțiunea `seo` din raport are și ea severitate (`critic`/`important`/`minor`), ca ghid de citire. Nu intră în `scor_automat` — `/13` rămâne neschimbat.

Dacă iei decizii pe baza raportului în loc să-l citești (filtrezi pe severitate, numeri categorii, iterezi până la un prag), folosește `--json`. E același conținut, structurat — parsarea liniilor cu `|` se strică la primul fragment care conține o bară.

## Ce face fiecare

- **`verifica.py` — punctul de intrare recomandat.** Rulează toate verificările dintr-un singur apel și calculează scorul combinat (`scor_automat=X/13`). Flags: `--fara-seo` (text literar), `--scor` (doar scorurile), `--json` (output structurat), `--prag N`, `--human-voice` (audit separat, cu `AI_PATTERN_SCORE/30`, `STATUS` și blocere). Combinația `--human-voice --json` adaugă obiectul `human_voice` fără să modifice scorul existent /13. Celelalte scripturi sunt utile doar pentru verificări punctuale — implicit rulezi `verifica.py`.
- `check-tipare.py` — clișee, calcuri, artefacte de generare. Potrivirea ignoră diacriticele, deci merge și pe text scris fără ele sau cu sedilă. Raportează severitate și praguri de densitate. Categoriile `copula_evitata`, `referinta_vaga` și `simetrie_de_acoperire` se numără pe familie, nu pe expresie, și nu intră în scor — sunt semnale de recitire.
- `check-human-voice.py` — semnale mecanice prudente pentru filler conversațional, punchline, slogan/promo, metafore de copywriter, autobiografie fără context, CAPS și contaminare. Nu detectează cuvinte inexistente: `arămriu` iese curat. Citește `human-voice-validator.md`; nu îl folosi pentru a decide automat că un text este AI, că e corect lexical, sau pentru a rescrie voce legitimă.
- `check-reclame.py` — doar pentru fișiere de anunț (cu etichete H1:/D1:/Text:/Titlu:; fără ele, tace). Limitele de caractere Google/Meta, politicile editoriale ale platformei („!", CAPS, emoji, duplicate) și semnăturile afirmărilor goale: perechea temporală fără cauză și tautologia de beneficiu (acțiune + rezultat fără produs în propoziție). Limitele oficiale și formatul: `references/reclame/platforme.md`. Flags: `--platform google|meta`, `--brand "Nume"`.
- `check-cuvinte.py` — formele care lipsesc din lexiconul Rospell (`scripts/lexicon/`, MPL/LGPL, nu MIT), cu adresa dexonline pentru fiecare. Nu intră în `verifica.py` și nu are scor. Lipsa din lexicon nu e verdict: Rospell (2013) nu are tot vocabularul, iar un cuvânt inventat care coincide cu o formă reală trece. Plafon 10 forme afișate (`--tot` le dă pe toate), `--allow fișier` pentru termeni confirmați, `--lexicon cale` pentru altă listă. `scripts/lexicon/completari.txt` are formele românești confirmate pe dexonline și lipsă din Rospell. Peste 30% forme lipsă (text englezesc, cod, log) raportul are în loc de listă linia `info|cuvinte|text predominant neromânesc`, apoi `---` și `total=…` (fără `nota:`) (exit 1 și aici, sub 40 de forme unice nu se aplică). Ieșirea: liniile `important|cuvant_de_verificat|L<linie>|<formă> xN|→ <url>`, `mai_sunt|N forme neafișate (--tot)` când e depășit plafonul, apoi `---`, `total=…` și o linie `nota:`; citește și de pe stdin (`-`). Exit: 0 nimic de verificat, 1 forme de verificat (caz normal, nu eșec), 2 eroare de input sau lexicon indisponibil. Linia `text predominant neromânesc` e doar euristică (multe forme lipsă), nu diagnostic. Sugestii de corectare (opt-in, motor Hunspell local + dicționar instalat separat): `check-cuvinte.py <fișier|-> --sugestii [--dictionar ro_RO] [--allow termeni.txt] [--tot]` — motor Hunspell local în PATH + dicționar separat (setup: `README.md#optional-hunspell-setup`); fără flag, nicio dependență nouă. `--dictionar` acceptă nume sau prefix de cale fără `.dic`/`.aff` și cere `--sugestii`. Doar formele necunoscute AFIȘATE primesc sugestii (max 5, fără înlocuire automată); `allow`/completări protejate; linii noi doar opt-in (`sugestii|L<n>|<forma>|<v1> / <v2>`, sau `fără sugestii`). Exit 2 dacă motorul/dicționarul lipsește sau eșuează și există suspecți; fără suspecți sau cu lista suprimată, motorul nu pornește. Scor /13, `verifica.py`, exituri 0/1/2, neschimbate. Variantele nu confirmă existența/sensul; versiuni diferite dau sugestii diferite — nu e corector semantic.
- `check-ritm.py` — uniformitatea frazelor și a paragrafelor, structura excesivă, capcana concluziei.
- `check-modelisme.py` — pleonasme etimologice (prefixe, sufixe, diminutive), anglicisme, paronime. Paronimele sunt informative: scriptul vede coapariția a două cuvinte în aceeași frază, nu confuzia dintre ele.
- `check-seo.py` — heading-uri (H1 unic, fără sărituri), keyword stuffing, secțiuni prea lungi între heading-uri, diacritice în URL-uri, sedilă, plus registrul titlului (clickbait, șablon, etichetă, lungime, subtitluri plate). Raportează severitate ca restul scripturilor, dar nu contribuie la `scor_automat`.
- `evaluare-contextuala.py` — nu verifică text: numără potriviri, ratări și fals-pozitive pe predicții deja furnizate (fișier JSON `id` + `verdict`) față de corpusul draft `tests/fixtures/evaluare-contextuala.json` (`draft_nevalidat_uman`), pentru pilotul de evaluare al reviziei contextuale (`references/limba/revizie-contextuala.md` §evaluare). `--split referinta|holdout` limitează validarea și numărarea la un split; predicțiile trebuie să acopere toate id-urile alese. `--corpus` înlocuiește calea corpusului, `--detaliu` listează cazurile din afara `potrivit`, iar `--json` păstrează același conținut în format structurat. Exit 0 evaluare completă, 1 predicții incomplete/invalide, 2 fișier sau corpus defect. Nu rulează modele, nu are scor și nu face parte din fluxul de scriere: etichetele nevalidate uman fac numărările material de lucru, nu benchmark. Fără dependențe.

  Verdicte permise în predicții: `eroare`, `suspiciune`, `pastreaza`, `neclar`. Acestea sunt etichete de intrare, nu bucket-uri. Evaluatorul clasifică rezultatele în bucket-urile `potrivit`, `semnal_acceptabil`, `escaladat`, `ratat`, `neclar_ratat` și `fals_pozitiv`.

Sunt instrumente de sprijin, nu verdicte. Skill-ul e instrucțiune: limitele reale de execuție le impune harness-ul, nu le garantează textul. `check-ritm.py` mai ales: pragurile lui vin din corpusuri englezești și dau fals pozitiv pe registru formal. Nu înlocuiesc judecata asupra ritmului, naturaleții sau relevanței conținutului.
