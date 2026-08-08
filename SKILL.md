---
name: scrie-romaneste
description: >
  Scrie, rescrie si revizuieste text in limba romana care suna natural si uman,
  nu ca text de model: fara clisee AI (tranzitii mecanice, "in concluzie",
  introduceri formulaice, hedging), fara romgleza si calcuri din engleza, cu
  diacritice si acord corecte, in registrul cerut de gen si de cititor.
  Foloseste acest skill cand utilizatorul cere sa scrii, rescrii, editezi sau
  revizuiesti orice text in limba romana - articol, email, descriere de produs,
  pagina web, postare, text literar - sau cand mentioneaza "scrie romaneste",
  clisee AI, ton natural, romgleza. Acopera si regulile SEO/GEO, dar numai
  pentru continut cu destinatie online sau comerciala.
---

# Scrie Românește

Skill pentru generarea și revizuirea de text în limba română care sună natural și
uman, nu ca text produs de un model lingvistic. Combină reguli de limbă
(gramatică, stil, anti-tipare AI) cu reguli de optimizare SEO/GEO — fără ca una
să o strice pe cealaltă.

## Moduri

Alege modul din cerință. Dacă nu e clar, e **rescriere**.

- **rescriere** (implicit) — livrează textul final, curat. Fără metacomentarii,
  fără „Iată textul rescris conform regulilor", fără listă de modificări. Doar
  textul.
- **audit** — raportează tiparele găsite, grupate pe severitate (`critic`,
  `important`, `minor`), fiecare cu citatul și motivul. **Nu rescrie.** Unele
  alegeri sunt intenționate; decizia e a autorului. Se cere cu „ce e în neregulă
  cu textul", „verifică", „analizează". **Începe cu `scripts/verifica.py
  <fișier>`** — raportul dă direct citatele, severitatea și sugestiile de
  corecție; încarcă din `references/` doar ce-ți trebuie pentru judecata
  calitativă (ritm, naturalitate) sau pentru categoriile semnalate.
- **editare** — modificări minime și țintite în fișier. Păstrează intacte
  pasajele care sunt deja bune. Nu rescrie ce nu e stricat.

Când cererea cere două lucruri deodată („verifică textul și fă-l mai bun",
„zi-mi ce e prost și repară"), **fă rescrierea și pune raportul după text**, în
câteva rânduri: ce ai schimbat și de ce. Nu livra doar auditul — utilizatorul a
cerut și textul. Nu livra nici doar textul — a cerut și explicația. Dacă textul
e într-un fișier al utilizatorului, modul e `editare`, nu `rescriere`: nu
rescrie un fișier întreg când ți s-a cerut să-l repari.

## Profil de voce

Dacă cerința indică un ton, aplică-l consecvent; altfel alege după canal și
public. Detalii de registru în `references/limba/gramatica-stil.md` §7.

`publicistic` · `tehnic` · `colocvial` · `direct` · `cald`

Profilul schimbă lexicul și lungimea frazei, nu regulile de corectitudine.
Stabilește de la început și **tu** sau **dumneavoastră**, și nu comuta.

## Reguli critice (rezumat — detalii în references/)

Patru reguli de decizie, înaintea oricărei liste:

1. Spune concret cine face ce și de ce contează.
2. Păstrează o formulare convențională dacă se potrivește genului, vocii și
   scopului — nu o tăia doar fiindcă apare des în text de model.
3. Elimin-o dacă nu adaugă sens, dovadă, ritm sau relație cu cititorul.
4. Nu transforma un semnal stilistic într-o corecție automată. Erorile certe se
   corectează; alegerile stilistice se recitesc în context.

**Interzis** (vezi `references/limba/anti-tipare-ai.md` pentru liste complete și
praguri):
- Tranziții mecanice: „în concluzie", „prin urmare", „de asemenea", „totodată",
  „mai mult decât atât", „pe de o parte... pe de altă parte".
- Introduceri formulaice: „în lumea de astăzi", „în era digitală", „în contextul
  actual".
- Umpluturi meta-text: „este important de menționat că", „merită subliniat".
- Adjective corporatiste: „revoluționar", „impresionant"; sintagme ca „adoptă o
  abordare", „schimbare de paradigmă", „abordare holistică".
- Cuantificări vagi: „o serie de", „un număr semnificativ", „o gamă largă de".
- Hedging: „este posibil ca", „s-ar putea ca" — fii asertiv.
- Romgleză și calcuri: „face sens" → „are sens"; „a adresa o problemă" → „a
  aborda"; „în termeni de" → „în ceea ce privește".
- „Capcana concluziei" — nu încheia cu un rezumat forțat.
- Paragrafe simetrice și ritm monoton — variază lungimea frazelor.
- Abuz de simboluri: emoji decorative, liste cu „-" în locul prozei, liniuța ca
  paranteză improvizată, bold/italic dese — toate cu prag de abuz, nu interzicere
  absolută (`references/limba/anti-tipare-ai.md` §I).

**Obligatoriu**:
- Diateza activă în locul pasivului birocratic (`references/limba/gramatica-stil.md` §4).
- Un cititor-țintă concret în minte înainte de a scrie (`references/limba/scris-eficient.md`).
- Verifică sursele înainte de a afirma fapte, cifre sau citate. Nu inventa
  precizie (`references/limba/tipare-ro.md`, `sursa_fabricata`). Se aplică și
  datelor de business — nume, adrese, telefoane, prețuri, autori: dacă nu le ai
  confirmate, cere-le sau lasă `[DE COMPLETAT: …]`.
- Diacritice cu virgulă (`ș`, `ț`), nu cu sedilă (`ş`, `ţ`).

**Regulile de mai sus sunt suficiente ca să scrii un text bun.** Fișierele din
`references/` adaugă praguri, excepții și cazuri de graniță — le deschizi când
ai nevoie de ele, nu ca să ai voie să scrii. Dacă nu încarci un fișier, scrii
fără partea lui; **nu reconstitui din numele fișierului ce crezi că scrie în
el.** Un text corect și mai puțin nuanțat bate un text scris după o regulă
inventată.

## Fluxul de lucru

Dacă e prima dată când rulezi fluxul ăsta, `references/limba/flux-exemplu.md`
îl arată aplicat cap-coadă pe o descriere de produs, cu rapoartele reale ale
scripturilor și cu deciziile luate pe fiecare semnal.

1. **LOAD** — citește cerința, stabilește modul și profilul de voce.
   - **audit**: nu încărca nimic încă — rulează întâi `scripts/verifica.py`
     (pasul 5) și încarcă referințe doar la nevoie.
   - **rescriere/editare**: încarcă `references/limba/anti-tipare-ai.md`
     (interdicțiile trebuie știute *înainte* de a scrie — scriptul doar
     detectează, nu previne) și, dacă textul trebuie să sune viu, nu doar
     curat, `references/limba/exemple-voce.md` (transformări înainte/după).
     Dacă textul are destinație online/comercială, alege din `references/seo/`
     după tabelul de rutare de mai jos; dacă e text pur literar, sari peste
     partea SEO și protejează repetiția intenționată, ritmul și dialogul.
2. **CONTRACT** — înainte de a scrie, stabilește intern (nu în livrare):
   scopul textului și ce vrei să facă cititorul; cine e cititorul concret și
   cât știe deja; canalul și genul (email, pagină de produs, articol,
   documentație, comunicat, text literar); registrul, persoana de adresare
   (`tu`/`dumneavoastră`) și formalitatea; lungimea; faptele confirmate și
   incertitudinile pe care le vei declara. Dacă lipsește ceva indispensabil,
   cere-l o singură dată și grupat; dacă nu e indispensabil, scrie fără să
   inventezi. Contractul rămâne intern — nu-l livra ca preambul.
3. **CONTEXT** — pentru conținut comercial, adună datele reale înainte de a scrie.
   Grounding-ul poate fi în orice format (Markdown, YAML, JSON, PDF, o pagină
   publicată, un mesaj din conversație) — **caută conținutul, nu un nume de
   fișier**. Ordine: ce a indicat utilizatorul explicit → instrucțiunile
   proiectului (`CLAUDE.md`/`AGENTS.md`) → un brif sub orice nume → date deja
   prezente în cod și pe site → întreabă, o singură dată și grupat. Nu inventa
   nume de firmă, adrese, telefoane, prețuri, autori sau statistici proprii. După
   ce afli date noi, oferă-te să le salvezi în formatul proiectului. Detalii,
   tabelul de câmpuri și tratarea surselor contradictorii:
   `references/seo/grounding.md`. Pentru text literar sau fără date de business,
   sari peste pas.
4. **DRAFT** — scrie dintr-o trecere completă, fără să te oprești să corectezi
   propoziție cu propoziție (`references/limba/scris-eficient.md` §1).
5. **AUTOCORECȚIE** — rulează `scripts/verifica.py <fișier>` (sau `-` cu textul
   pe stdin; `--fara-seo` pentru text literar). Raportul acoperă clișee AI,
   calcuri, pleonasme, paronime, ritm și SEO dintr-o singură trecere, cu
   sugestia de corecție inline (`|→ …`) unde există una canonică. Aplică
   sugestiile cu judecată — potrivirea e mecanică, corecția cere acord și
   topică. Pentru problemele semnalate fără sugestie, sau ca să înțelegi o
   categorie, deschide referința relevantă (`anti-tipare-ai.md`,
   `tipare-ro.md`, `modelisme.md`).
6. **PASUL DOI** — reauditează **textul deja corectat**, nu draftul. Rescrierea
   își introduce propriile tipare: tranziții reciclate, sinonime rotite peste
   aceeași idee, „reprezintă" strecurat în locul lui „este", ritm care s-a
   uniformizat la curățenie. Pasul ăsta prinde ce a apărut la pasul 5.
7. **POARTA DE LIVRARE** — `scripts/verifica.py <fișier> --scor` dă partea
   deterministă (`scor_automat=X/13`, penalizări, nu notă). Restul se
   verifică pe listă, nu pe punctaj — treci textul doar dacă toate se
   confirmă:
   - niciun fapt, citat, preț sau date de business inventate;
   - niciun artefact de chat, markup rezidual sau placeholder publicabil;
   - erorile certe (calc, sedilă, acord, artefact) sunt corectate;
   - semnalele stilistice (ritm, concluzie, paralelism, listă) au fost
     recitite în context și păstrate sau tăiate deliberat;
   - textul respectă contractul de la pasul 2 — gen, registru, cititor,
     lungime;
   - fiecare paragraf justifică spațiul prin informație, exemplu, cauză,
     consecință, decizie sau efect stilistic intenționat.

   Rubricile din `references/limba/scoring-checklist.md` și
   `references/seo/scoring-checklist.md` rămân utile ca listă de citit, nu ca
   prag numeric.
8. **LIVRARE** — conform modului ales la pasul 1. Semnalează separat, la final,
   orice `[DE COMPLETAT: …]` rămas în text.

## Structura references/

```
references/
├── limba/
│   ├── anti-tipare-ai.md      # clișee, vocabular, praguri — obligatoriu la scriere
│   ├── exemple-voce.md        # transformări înainte/după, pe registre — modele pozitive
│   ├── flux-exemplu.md        # un traseu complet: cerere → contract → draft → raport → livrare
│   ├── tipare-ro.md           # acord, prepoziții, flexiune, calc sintactic
│   ├── gramatica-stil.md      # punctuație, ortografie, pleonasm — normă
│   ├── scris-eficient.md      # tehnici de proces: draft/editare, ritm, concizie
│   ├── modelisme.md           # pleonasme etimologice, anglicisme, paronimie
│   └── scoring-checklist.md   # criteriile de limbă, ca listă de citit
└── seo/
    ├── core.md                # tehnic, on-page, conținut, specific română
    ├── grounding.md           # date care nu se inventă + salvarea lor
    ├── geo.md                 # optimizare pentru AI search
    ├── schema.md              # JSON-LD / structured data
    ├── ecommerce.md           # pagini de produs și categorie
    ├── blog-keyword.md        # blog + cercetarea cuvintelor-cheie
    ├── local.md               # NAP, Google Business Profile
    ├── avansat.md             # link building, tehnic avansat, audit, competitiv
    └── scoring-checklist.md   # criteriile SEO/densitate, ca listă de citit
```

Rutare SEO — încarcă doar ce cere task-ul (plus `grounding.md` la orice conținut
comercial):

| Task | Fișiere |
|---|---|
| articol de blog | `core.md`, `blog-keyword.md`, `geo.md` |
| pagină de produs/categorie | `core.md`, `ecommerce.md` |
| afacere locală / pagină de contact | `core.md`, `local.md` |
| schema / date structurate | `schema.md` |
| audit SEO complet, link building | `core.md`, `avansat.md` |

Încarcă doar fișierele relevante — nu e nevoie să citești tot `references/` pentru
o singură propoziție de rescris.

## scripts/

### Cum le rulezi

Scripturile stau în directorul skill-ului, **nu** în proiectul utilizatorului.
Calea e relativă la fișierul ăsta: dacă citești `SKILL.md` din
`~/.claude/skills/scrie-romaneste/`, scripturile sunt în
`~/.claude/skills/scrie-romaneste/scripts/`. Notează calea o dată, la primul
apel, și refolosește-o.

Textul de verificat e de obicei în conversație, nu într-un fișier. Dă-l pe
stdin, cu `-` ca argument:

```bash
python3 <cale-skill>/scripts/verifica.py - <<'TEXT'
Textul de verificat, integral, cu diacritice.
TEXT
```

Dacă textul e deja într-un fișier al proiectului:

```bash
python3 <cale-skill>/scripts/verifica.py drafts/articol.md
```

Pe Windows/PowerShell, unde heredoc-ul nu există, scrie textul într-un fișier
temporar și dă-i calea. Nu încerca variante de escaping — pierzi diacriticele.

Trei lucruri de știut înainte de primul apel:

- **Exit 1 nu e eroare.** Înseamnă „am găsit semnale" și e rezultatul normal pe
  un draft. Doar exit 2 e eroare (fișier lipsă, argument greșit). Nu raporta
  utilizatorului că scriptul „a eșuat".
- **`--fara-seo` pentru orice text fără destinație online** — literar, email,
  document intern. Altfel primești semnale despre H1 și heading-uri pentru un
  text care n-are așa ceva.
- **Dacă `python3` nu există** în mediu, nu insista și nu căuta alternative:
  sari peste pasul mecanic, spune-o pe scurt și fă verificarea pe listă, din
  `references/limba/anti-tipare-ai.md`.

### Cum citești raportul

```
severitate|categorie|linie|fragmentul găsit|→ corecția canonică
minor|copula_evitata|L3|…centrale termice reprezintă o decizie…|→ «este», sau …
prag_depasit|copula_evitata|3 aparitii|densitate
```

- `critic` — eroare. Se corectează, fără discuție: artefact de chat,
  placeholder, calc din engleză, introducere formulaică.
- `important` — aproape sigur de corectat, dar citește fragmentul întâi.
- `minor` — semnal de recitire. Îl păstrezi dacă genul îl cere; îl tai dacă nu
  adaugă nimic. Nu-l corecta automat.
- `→` apare doar unde există o corecție canonică. Aplic-o adaptând acordul și
  topica — potrivirea e mecanică, corecția nu.
- `prag_depasit` spune de ce s-a raportat o categorie care singură ar fi fost
  acceptabilă: prea multe apariții, prea aproape una de alta.

`scor_automat=X/13` numără penalizări deterministe, nu calitate. 0/13 nu
înseamnă text bun, înseamnă doar că n-a călcat pe nicio mină automată.

Dacă iei decizii pe baza raportului în loc să-l citești (filtrezi pe severitate,
numeri categorii, iterezi până la un prag), folosește `--json`. E același
conținut, structurat — parsarea liniilor cu `|` se strică la primul fragment
care conține o bară.

### Ce face fiecare

- **`verifica.py` — punctul de intrare recomandat.** Rulează toate verificările
  dintr-un singur apel și calculează scorul combinat
  (`scor_automat=X/13`). Flags: `--fara-seo` (text literar), `--scor` (doar
  scorurile), `--json` (output structurat), `--prag N`. Celelalte scripturi sunt
  utile doar pentru verificări punctuale — implicit rulezi `verifica.py`.
- `check-tipare.py` — clișee, calcuri, artefacte de generare. Potrivirea ignoră
  diacriticele, deci merge și pe text scris fără ele sau cu sedilă. Raportează
  severitate și praguri de densitate. Categoriile `copula_evitata`,
  `referinta_vaga` și `simetrie_de_acoperire` se numără pe familie, nu pe
  expresie, și nu intră în scor — sunt semnale de recitire.
- `check-ritm.py` — uniformitatea frazelor și a paragrafelor, structura excesivă,
  capcana concluziei.
- `check-modelisme.py` — pleonasme etimologice (prefixe, sufixe, diminutive),
  anglicisme, paronime. Paronimele sunt informative: scriptul vede coapariția a
  două cuvinte în aceeași frază, nu confuzia dintre ele.
- `check-seo.py` — heading-uri (H1 unic, fără sărituri), keyword stuffing,
  secțiuni prea lungi între heading-uri, diacritice în URL-uri, sedilă.

Sunt instrumente de sprijin, nu verdicte. `check-ritm.py` mai ales: pragurile lui
vin din corpusuri englezești și dau fals pozitiv pe registru formal. Nu înlocuiesc
judecata asupra ritmului, naturaleții sau relevanței conținutului.
