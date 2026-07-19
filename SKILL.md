---
name: scrie-romaneste
description: >
  Genereaza si rescrie text in limba romana natural, uman, fluent, fara
  cliseele tipice modelelor AI (tranzitii mecanice, "in concluzie", romgleza,
  hedging) si respectand regulile SEO/GEO. Foloseste acest skill cand
  utilizatorul cere sa scrii, rescrii, editezi sau revizuiesti orice text in
  limba romana - articole, descrieri de produs, pagini web, continut blog,
  postari - sau cand mentioneaza explicit "scrie romaneste", clisee AI,
  ton natural, romgleza, SEO/GEO in limba romana.
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

## Profil de voce

Dacă cerința indică un ton, aplică-l consecvent; altfel alege după canal și
public. Detalii de registru în `references/limba/gramatica-stil.md` §7.

`publicistic` · `tehnic` · `colocvial` · `direct` · `cald`

Profilul schimbă lexicul și lungimea frazei, nu regulile de corectitudine.
Stabilește de la început și **tu** sau **dumneavoastră**, și nu comuta.

## Reguli critice (rezumat — detalii în references/)

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

**Obligatoriu**:
- Diateza activă în locul pasivului birocratic (`references/limba/gramatica-stil.md` §4).
- Un cititor-țintă concret în minte înainte de a scrie (`references/limba/scris-eficient.md`).
- Verifică sursele înainte de a afirma fapte, cifre sau citate. Nu inventa
  precizie (`references/limba/tipare-ro.md`, `sursa_fabricata`). Se aplică și
  datelor de business — nume, adrese, telefoane, prețuri, autori: dacă nu le ai
  confirmate, cere-le sau lasă `[DE COMPLETAT: …]`.
- Diacritice cu virgulă (`ș`, `ț`), nu cu sedilă (`ş`, `ţ`).

## Fluxul de lucru

1. **LOAD** — citește cerința, stabilește modul și profilul de voce.
   - **audit**: nu încărca nimic încă — rulează întâi `scripts/verifica.py`
     (pasul 4) și încarcă referințe doar la nevoie.
   - **rescriere/editare**: încarcă `references/limba/anti-tipare-ai.md`
     (interdicțiile trebuie știute *înainte* de a scrie — scriptul doar
     detectează, nu previne). Dacă textul are destinație online/comercială,
     alege din `references/seo/` după tabelul de rutare de mai jos; dacă e text
     pur literar, sari peste partea SEO.
2. **CONTEXT** — pentru conținut comercial, adună datele reale înainte de a scrie.
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
3. **DRAFT** — scrie dintr-o trecere completă, fără să te oprești să corectezi
   propoziție cu propoziție (`references/limba/scris-eficient.md` §1).
4. **AUTOCORECȚIE** — rulează `scripts/verifica.py <fișier>` (sau `-` cu textul
   pe stdin; `--fara-seo` pentru text literar). Raportul acoperă clișee AI,
   calcuri, pleonasme, paronime, ritm și SEO dintr-o singură trecere, cu
   sugestia de corecție inline (`|→ …`) unde există una canonică. Aplică
   sugestiile cu judecată — potrivirea e mecanică, corecția cere acord și
   topică. Pentru problemele semnalate fără sugestie, sau ca să înțelegi o
   categorie, deschide referința relevantă (`anti-tipare-ai.md`,
   `tipare-ro.md`, `modelisme.md`).
5. **PASUL DOI** — reauditează **textul deja corectat**, nu draftul. Rescrierea
   își introduce propriile tipare: tranziții reciclate, sinonime rotite peste
   aceeași idee, „reprezintă" strecurat în locul lui „este", ritm care s-a
   uniformizat la curățenie. Pasul ăsta prinde ce a apărut la pasul 3.
6. **EVALUARE** — `scripts/verifica.py <fișier> --scor` dă partea deterministă
   (`scor_automat=X/13`). Evaluează manual restul: naturalitate, densitate de
   informație, fapte/surse — rubricile din
   `references/limba/scoring-checklist.md` și
   `references/seo/scoring-checklist.md`. Prag minim: **8/10** pe rubrica
   combinată. Sub prag → refactorizează și reevaluează.
7. **LIVRARE** — conform modului ales la pasul 1. Semnalează separat, la final,
   orice `[DE COMPLETAT: …]` rămas în text.

## Structura references/

```
references/
├── limba/
│   ├── anti-tipare-ai.md      # clișee, vocabular, praguri — obligatoriu la scriere
│   ├── tipare-ro.md           # acord, prepoziții, flexiune, calc sintactic
│   ├── gramatica-stil.md      # punctuație, ortografie, pleonasm — normă
│   ├── scris-eficient.md      # tehnici de proces: draft/editare, ritm, concizie
│   ├── modelisme.md           # pleonasme etimologice, anglicisme, paronimie
│   └── scoring-checklist.md   # rubrica 1-10, criteriile de limbă (1-3)
└── seo/
    ├── core.md                # tehnic, on-page, conținut, specific română
    ├── grounding.md           # date care nu se inventă + salvarea lor
    ├── geo.md                 # optimizare pentru AI search
    ├── schema.md              # JSON-LD / structured data
    ├── ecommerce.md           # pagini de produs și categorie
    ├── blog-keyword.md        # blog + cercetarea cuvintelor-cheie
    ├── local.md               # NAP, Google Business Profile
    ├── avansat.md             # link building, tehnic avansat, audit, competitiv
    └── scoring-checklist.md   # rubrica 1-10, criteriile SEO (4-5)
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

- **`verifica.py` — punctul de intrare recomandat.** Rulează toate verificările
  dintr-un singur apel și calculează scorul combinat
  (`scor_automat=X/13`). Flags: `--fara-seo` (text literar), `--scor` (doar
  scorurile), `--json` (output structurat), `--prag N`.
- `check-tipare.py` — clișee, calcuri, artefacte de generare. Potrivirea ignoră
  diacriticele, deci merge și pe text scris fără ele sau cu sedilă. Raportează
  severitate și praguri de densitate.
- `check-ritm.py` — uniformitatea frazelor și a paragrafelor, structura excesivă,
  capcana concluziei.
- `check-modelisme.py` — pleonasme etimologice (prefixe, sufixe, diminutive),
  anglicisme, paronime.
- `check-seo.py` — heading-uri (H1 unic, fără sărituri), keyword stuffing,
  secțiuni prea lungi între heading-uri, diacritice în URL-uri, sedilă.

Exit 0 = curat, 1 = potriviri, 2 = eroare de input. `--help` pentru detalii.
Unde tiparele au o corecție canonică, raportul o dă inline după fragment
(`|→ are sens`) — aplic-o adaptând acordul și topica, nu prin înlocuire oarbă.

Sunt instrumente de sprijin, nu verdicte. `check-ritm.py` mai ales: pragurile lui
vin din corpusuri englezești și dau fals pozitiv pe registru formal. Nu înlocuiesc
judecata asupra ritmului, naturaleții sau relevanței conținutului.
