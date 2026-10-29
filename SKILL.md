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
  <fișier>`** (textul e de obicei în conversație — rețeta cu `-` e în „Cum le
  rulezi") — raportul dă direct citatele, severitatea și sugestiile de
  corecție; încarcă din `references/` doar ce-ți trebuie pentru judecata
  calitativă (ritm, naturalitate) sau pentru categoriile semnalate.
  Majoritatea expresiilor din lista Interzis apar în raport din prima apariție;
  doar 7 sunt pe densitate și lipsesc sub ~3 apariții („prin urmare",
  „de asemenea", „totodată", „impresionant", „o serie de", „este posibil ca",
  „s-ar putea ca"). Pentru ele, rulează
  `python3 <cale-skill>/scripts/check-tipare.py <fișier> --tot`: potrivirile
  `sub_prag` sunt semnale de recitire, nu erori (regulile de decizie 2 și 4).
  Un audit nu se poate încheia cu „0 semnale = text curat" fără o recitire a
  listei din `references/limba/anti-tipare-ai.md` §A-§H.
  Scriptul prinde un singur tip de acord, adjectiv + substantiv-număr
  (`acord_numerale`: „acești milioane", „câțiva sute"); restul, inclusiv
  „doi/două" și „primii/primele", rămâne la recitirea manuală — ca și topica
  și alegerea lexicală. Nici `verifica.py`, nici `--human-voice` nu au
  dicționar: un raport curat nu dovedește că vorbele există — rulează separat
  `scripts/check-cuvinte.py` (detalii la Obligatoriu). Recitește
  oricum textul integral, în special titlul și excerptul, pentru acord, forme
  verbale și cuvinte inexistente (`references/limba/tipare-ro.md`
  §cuvant_inexistent).
- **editare** — modificări minime și țintite în fișier. Păstrează intacte
  pasajele care sunt deja bune. Nu rescrie ce nu e stricat. Corecția intră
  în fișierul indicat de utilizator: nu lăsa varianta bună doar în răspuns
  sau într-o copie alăturată, cât timp sursa rămâne greșită.
- **human-voice** — audit separat pentru reflexe mecanice de voce. Rulează
  `scripts/verifica.py <fișier> --human-voice`; raportează citatele, scorul
  `AI_PATTERN_SCORE/30`, `STATUS` (`PASS`/`EDITED`/`REWRITE`) și blocerele.
  **Nu rescrie** în acest mod. Un `PASS` aici nu e pașaport lexical și nu
  atestă corectitudinea/sensul: validatorul nu vede cuvintele inexistente.
  Regulile, excepțiile și schema sunt în
  `references/limba/human-voice-validator.md`.

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
- **Afirmații goale** — propoziția care rămâne la fel de adevărată fără
  subiectul/actorul/produsul ei nu promite nimic („Seara cureți tenul,
  dimineața îl simți moale”; „Te pieptănești, părul e neted”). În text
  persuasiv, trece fiecare promisiune prin testul în 3 întrebări din
  `references/limba/anti-tipare-ai.md` §J. În text literar, redundanța poate
  fi stil — recitie, nu tăiere automată.
- Paragrafe simetrice și ritm monoton — variază lungimea frazelor.
- Abuz de simboluri: emoji decorative, liste cu „-" în locul prozei, liniuța ca
  paranteză improvizată, bold/italic dese — toate cu prag de abuz, nu interzicere
  absolută (`references/limba/anti-tipare-ai.md` §I).
- Liniuța-cârjă: `—` sau `-` ca singur conector, frază după frază, în locul
  virgulei sau al punctului. Dialogul și intervalele numerice rămân neatinse
  (`references/limba/tipare-ro.md` `punctuatie_carja`).
- En-dash `–`: niciodată, în niciun context. Cratimă în compuse și intervale
  („10-12 zile"), linie de pauză `—` în incize (`liniuta_engleza`).
- Bullet Unicode „•" în loc de „-", și `§ ¶ † ‡` presărate ca ornament: artefacte
  de fereastră de chat, nu punctuație românească.
- Clickbait de tabloid și titlul-șablon de agenție: „nu-ți vine să crezi",
  „Ghidul suprem pentru X", „Tot ce trebuie să știi despre X"
  (`references/seo/titluri.md`).

**Obligatoriu**:
- Diateza activă în locul pasivului birocratic (`references/limba/gramatica-stil.md` §4).
- Un cititor-țintă concret în minte înainte de a scrie (`references/limba/scris-eficient.md`).
- Verifică sursele înainte de a afirma fapte, cifre sau citate. Nu inventa
  precizie (`references/limba/tipare-ro.md`, `sursa_fabricata`). Se aplică și
  datelor de business — nume, adrese, telefoane, prețuri, autori: dacă nu le ai
  confirmate, cere-le sau lasă `[DE COMPLETAT: …]`.
- Diacritice cu virgulă (`ș`, `ț`), nu cu sedilă (`ş`, `ţ`).
- Nu livra un cuvânt pe care nu-l poți susține. `verifica.py` nu are
  dicționar; `scripts/check-cuvinte.py` dă lista formelor lipsă din lexicon —
  de verificat, nu verdict. Lipsa = neatestat în sursa consultată, nu inexistent.
  Verifici forma, lema, sensul și registrul în surse permise (poate fi un termen
  valid absent) și accepți doar sensul confirmat. Lookup extern numai ca în
  `references/limba/revizie-contextuala.md` §acces; sugestiile nu confirmă.
  La neclar întrebi, nu judeci absența (`references/limba/tipare-ro.md`
  §cuvant_inexistent).
- Titlul are o promisiune concretă și un element de precizie, nu e etichetă
  (`references/seo/titluri.md`).
- Deschiderea intră direct în subiect: fără încălzire, iar promisiunea titlului
  e onorată în primele propoziții (`references/seo/flux-articol.md`).

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
     după tabelul de rutare de mai jos; `titluri.md` se încarcă odată cu
     `core.md`. Dacă e text pur literar, sari peste partea SEO și protejează
     repetiția intenționată, ritmul și dialogul.
2. **CONTRACT** — înainte de a scrie, stabilește intern (nu în livrare):
   scopul textului și ce vrei să facă cititorul; cine e cititorul concret și
   cât știe deja; canalul și genul (email, pagină de produs, articol, anunț
   Google/Meta, documentație, comunicat, text literar); registrul, persoana de
   adresare (`tu`/`dumneavoastră`) și formalitatea; lungimea — pentru anunțuri,
   limitele de caractere ale platformei (`references/reclame/platforme.md`);
   faptele confirmate și
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
5. **AUTOCORECȚIE** — rulează `scripts/verifica.py <fișier>` (textul din conversație
   pe stdin — rețeta e în „Cum le rulezi"; `--fara-seo` pentru text literar).
   Raportul acoperă clișee, calcuri, pleonasme, paronime, ritm și SEO dintr-o
   trecere; citește-l ca în „Cum citești raportul" — `→` e corecție canonică,
   aplicată cu acord și topică. Dacă textul are titlu sau excerpt separat de corp (TITLE_RO/EXCERPT_RO,
   frontmatter), verifică-le ca text separat, lângă corp — nu le scoate din
   inputul verificat. Pentru problemele semnalate fără sugestie, sau ca să
   înțelegi o
   categorie, deschide referința relevantă (`anti-tipare-ai.md`,
   `tipare-ro.md`, `modelisme.md`). După acest audit, rulează separat
   `scripts/verifica.py <fișier> --human-voice`. Nu amesteca auditul de voce cu
   editarea: citește fiecare semnal în context, blochează doar garbage-ul,
   contaminarea și placeholder-ele, iar pentru restul editează minim.
   Apoi treci textul propoziție cu propoziție prin
   `references/limba/revizie-contextuala.md` (context de paragraf și public;
   titluri/excerpt/etichete de anunț citite și standalone; urmă internă
   OK/RESCRIU/NECLAR pe fiecare propoziție; corecția se recitește și ea —
   sens, repetiție, adresare, registru, fapte): scripturile nu prind
   construcții noi nefirești și nu învață modelul.
   Dacă textul e anunț (fișier cu etichete H1:/D1:/Text:/Titlu:), rulează și
   `scripts/verifica.py <fișier> --reclame` — limitele de caractere, politicile
   platformei și afirmările goale structurale. Pe un fișier cu etichete de anunț,
   stratul SEO se reduce la verificarea sedilei (ca la `--fara-seo`): semnalele de
   titlu de articol (etichetă, șablon, subtitluri plate) veneau din heading-ul
   markdown `# …` al fișierului, nu din eticheta `Titlu:` — limitele de anunț sunt
   în `check-reclame.py` și `references/reclame/platforme.md`.
   Pentru orice text persuasiv,
   aplică testul în 3 întrebări din `anti-tipare-ai.md` §J pe fiecare
   promisiune.
6. **PASUL DOI** — reauditează **textul deja corectat**, nu draftul. Rescrierea
   își introduce propriile tipare: tranziții reciclate, sinonime rotite peste
   aceeași idee, „reprezintă" strecurat în locul lui „este", ritm care s-a
   uniformizat la curățenie. Pasul ăsta prinde ce a apărut la pasul 5. Pe FINAL,
   maxim 2 cicluri audit → editare minimă → reverificare; dacă rămâne dezacord
   sau necunoscut, escaladează (întrebi), nu itera. Auditul nu editează (vezi
   Moduri); observațiile intermediare rămân interne, nu intră în livrare.
7. **POARTA DE LIVRARE** — `scripts/verifica.py <fișier> --scor` dă partea
   deterministă (`scor_automat=X/13`, penalizări, nu notă). Restul se
   verifică pe listă, nu pe punctaj — treci textul doar dacă toate se
   confirmă:
   - niciun fapt, citat, preț sau date de business inventate;
   - niciun artefact de chat, markup rezidual sau placeholder publicabil;
   - erorile certe (calc, sedilă, acord, artefact) sunt corectate — inclusiv în
     titlu și excerpt, unde acordul se recitește manual: neutre la plural
     (virusuri funcționale, nu virusuri funcționali), numeral+substantiv
     (primii/primele, doi/două), genul adjectivelor;
   - textul a fost citit integral, nu doar pe semnalele din raport. Formele
     fără suport (neatestate în sursele permise), acordurile neprinse de script
     și formele verbale greșite sunt corectate sau escaladate. `scor_automat` și
     `--human-voice` nu fac controlul ăsta: `arămriu` și `petechelui` ies curate.
     `scripts/check-cuvinte.py` pe text: formele listate se tratează ca la
     regula „Nu livra un cuvânt pe care nu-l poți susține"; procedura de
     verificare e în `references/limba/revizie-contextuala.md` — neclar se
     întreabă, nu se înlocuiește din burtă;
   - semnalele stilistice (ritm, concluzie, paralelism, listă) au fost
     recitite în context și păstrate sau tăiate deliberat;
   - textul respectă contractul de la pasul 2 — gen, registru, cititor,
     lungime;
   - auditul separat `--human-voice` nu are blocere; semnalele editoriale au
     fost păstrate sau tăiate deliberat, nu rescrise mecanic. Un PASS aici nu
     atestă corectitudinea/sensul;
   - revizia contextuală e trecută (`references/limba/revizie-contextuala.md`):
     citat exact + motiv concret + corecție minimă + verdict per problemă; pasajele
     bune intacte; metaforele/registrul nu au fost „corectate" automat; fiecare
     corecție recitită pentru sens, repetiție, adresare, registru, fapte;
   - dacă textul e de citit cap-coadă online: titlul promite ceva concret și
     corpul îl plătește; deschiderea nu e încălzire; subtitlurile citite în
     șir spun povestea articolului;
   - dacă textul e anunț: `--reclame` nu are semnale — headline-urile și
     descrierile în limitele platformei, fără politici încălcate, fiecare
     promisiune cu agent și mecanism;
   - fiecare paragraf justifică spațiul prin informație, exemplu, cauză,
     consecință, decizie sau efect stilistic intenționat.

   Rubricile din `references/limba/scoring-checklist.md` și
   `references/seo/scoring-checklist.md` rămân utile ca listă de citit, nu ca
   prag numeric.
8. **LIVRARE** — conform modului ales la pasul 1. Scrierea unui fișier nu
   închide taskul. Gata înseamnă că livrabilul modului e în răspuns și că
   poarta de la pasul 7 a fost trecută pe textul acela, nu pe draft.

   - **rescriere** — livrabilul e textul, în răspuns. Poarta rămâne internă;
     nu atașa un raport de verificări.
   - **audit** și **human-voice** — livrabilul e raportul, în răspuns. Un
     fișier salvat fără raport nu e gata.
   - **editare**, și orice flux care atinge un fișier al utilizatorului —
     corecția e în fișierul indicat, poarta e rerulată pe el, iar răspunsul
     spune, în una-două propoziții, ce scriptul nu poate spune: textul a fost
     citit integral pentru cuvinte inexistente, acord și verbe, și
     `--human-voice` nu are blocere. Nu declara gata doar fiindcă fișierul
     a fost scris.

   Semnalează separat, la final, orice `[DE COMPLETAT: …]` rămas în text.
   Când fluxul e agentic, păstrează ordinea: audit de limbă → audit
   human-voice → editare minimă → reverificare a ambelor → citire integrală
   pentru lexic → reviewer independent. Reviewerul validează contextul,
   excepțiile și vorbele pe care scriptul nu le vede; nu rescrie pasaje curate.
   În context separat când gazda suportă; altfel declari auto-review.

## Structura references/

```
references/
├── limba/
│   ├── anti-tipare-ai.md      # clișee, vocabular, praguri — obligatoriu la scriere
│   ├── exemple-voce.md        # transformări înainte/după, pe registre — modele pozitive
│   ├── revizie-contextuala.md # propoziție cu propoziție, pe sens: verdict + dovadă
│   ├── human-voice-validator.md # audit separat: A–J, scor, blocere, procedură
│   ├── cli-verificare.md      # manual CLI detaliat — doar înainte de uz avansat/individual
│   ├── flux-exemplu.md        # un traseu complet: cerere → contract → draft → raport → livrare
│   ├── tipare-ro.md           # acord, prepoziții, flexiune, cuvinte inexistente, calc
│   ├── gramatica-stil.md      # punctuație, ortografie, pleonasm — normă
│   ├── scris-eficient.md      # tehnici de proces: draft/editare, ritm, concizie
│   ├── modelisme.md           # pleonasme etimologice, anglicisme, paronimie
│   ├── calcuri.json           # registry static de colocări de recitit (check-calcuri.py, opt-in)
│   └── scoring-checklist.md   # criteriile de limbă, ca listă de citit
└── seo/
    ├── core.md                # tehnic, on-page, conținut, specific română
    ├── grounding.md           # date care nu se inventă + salvarea lor
    ├── titluri.md             # titlu, H1, subtitluri, meta — nu etichete
    ├── flux-articol.md        # deschidere, ritm, final, perspectiva proprie
    ├── geo.md                 # optimizare pentru AI search
    ├── schema.md              # JSON-LD / structured data
    ├── ecommerce.md           # pagini de produs și categorie
    ├── blog-keyword.md        # blog + cercetarea cuvintelor-cheie
    ├── local.md               # NAP, Google Business Profile
    ├── avansat.md             # link building, tehnic avansat, audit, competitiv
    └── scoring-checklist.md   # criteriile SEO/densitate, ca listă de citit
```

Plus `references/reclame/` pentru anunțuri plătite — un strat subțire care
referă regulile generale, nu le duplică:

```
references/
└── reclame/
    ├── platforme.md           # limite Google/Meta, politici, format de fișier
    └── voce.md                # promisiune→dovadă→CTA, modele pozitive, trimiteri
```

Rutare SEO — încarcă doar ce cere task-ul (plus `grounding.md` la orice conținut
comercial, `titluri.md` la orice conținut cu titlu vizibil și `flux-articol.md`
la orice text de citit cap-coadă):

| Task | Fișiere |
|---|---|
| articol de blog | `core.md`, `blog-keyword.md`, `geo.md`, `titluri.md`, `flux-articol.md` |
| pagină de produs/categorie | `core.md`, `ecommerce.md`, `titluri.md`, `flux-articol.md` |
| text de reclamă Google/Meta | `../reclame/platforme.md`, `../reclame/voce.md`, `../limba/anti-tipare-ai.md` §J, `grounding.md` |
| afacere locală / pagină de contact | `core.md`, `local.md` |
| schema / date structurate | `schema.md` |
| audit SEO complet, link building | `core.md`, `avansat.md` |

Încarcă doar fișierele relevante — nu e nevoie să citești tot `references/` pentru
o singură propoziție de rescris.

## scripts/

### Rețeta minimă și contracte critice

Scripturile stau în directorul skill-ului, nu în proiectul utilizatorului; rezolvă
calea relativ la `SKILL.md` o singură dată. Punctul de intrare recomandat este
`verifica.py`:

```bash
python3 <cale-skill>/scripts/verifica.py - <<'TEXT'
Textul integral, cu diacritice.
TEXT
```

sau, dacă textul e deja într-un fișier al proiectului:

```bash
python3 <cale-skill>/scripts/verifica.py drafts/articol.md
```

Pe Windows/PowerShell, pune textul din conversație într-un fișier temporar, nu
încerca escaping. Opțiunile uzuale: `--fara-seo`, `--scor`, `--json`, `--prag N`,
`--human-voice`, `--reclame`, `--platform google|meta`, `--brand "Nume"`.

- Exit 0 = curat, 1 = semnale (rezultat normal, nu eșec), 2 = eroare de input
  (inclusiv non-UTF-8; convertește cu `iconv -f WINDOWS-1250 -t UTF-8`, nu
  reîncerca escaping). Nu raporta exit 1 ca eroare.
- Pentru text fără destinație online (literar, email, document intern), folosește
  `--fara-seo`. Sedila se verifică oricum și rămâne în secțiunea `seo` (cheia
  `seo` în JSON); nu elimina acea secțiune din filtrare.
- `tipare` și `modelisme` folosesc liniile
  `severitate|categorie|L<linie>|fragment[|→ sugestie]`. `ritm` emite linii
  `metrici|...` și `<semnal>|incredere=...|detaliu`, fără `L<n>`; SEO are
  schema `severitate|categorie|detaliu|context`. `human-voice` și `reclame` au
  scheme proprii, cu `L<n>` și câmpuri specifice. Formatele detaliate sunt în
  manualul CLI. `--json` oferă structură pentru procesare programatică, fiindcă
  fragmentele din raportul text pot conține `|`.
- `scor_automat=X/13` este doar penalizare deterministă, nu notă; SEO nu intră
  în scor. `--human-voice` e audit separat, nu corectură lexicală; combinația
  `--human-voice --json` adaugă `human_voice` fără să schimbe scorul /13.
- `--reclame` se folosește pentru anunțuri cu etichetele H1:/D1:/Text:/Titlu:;
  păstrează limitele platformei și afirmările goale în verificare.
- `check-cuvinte.py` e separat, nu intră în `verifica.py` și nu are scor:
  listele sunt suspecți de verificat, nu verdicte. Exit 0 = niciun suspect,
  1 = forme de verificat, 2 = eroare de input/lexicon; cu `--sugestii`, exit 2
  poate indica și motorul Hunspell sau dicționarul indisponibil/defect când
  există suspecți afișați. Vezi manualul CLI pentru condiția exactă.
- `check-calcuri.py` e separat, opt-in (rulezi doar la cerere), nu intră în
  `verifica.py` și nu are scor: semnalizează colocări de recitit din
  `references/limba/calcuri.json` — deocamdată o singură regulă, forme de
  «a frâna» lângă forme de «încărcare», pe aceeași propoziție, la cel mult
  `--fereastra` cuvinte distanță (implicit 10; se acceptă și `--fereastra=N`).
  Perechea e de recitit în context — calc, metaforă sau frânare fizică
  legitimă («Camionul frânează la rampa de încărcare» e fals pozitiv
  acceptat) —, nu un verdict: fereastra numără cuvinte, nu sintaxă, iar
  semnalul trimite la revizia contextuală, nu la o corecție; un semnal nu e
  automat o eroare. «încărcătura» (sarcina, nu procesul) e exclusă. Exit 0 =
  nimic de recitit, 1 = cel puțin o colocare (caz normal), 2 = eroare de
  input, registry lipsă/defect sau argument necunoscut; `--registry`
  înlocuiește registry-ul. Limitele, formatul și creșterea manuală a
  registry-ului: manualul CLI.
- Dacă `python3` nu există, nu căuta alternative: sari peste pasul mecanic,
  spune-o pe scurt și fă verificarea pe listă, din
  `references/limba/anti-tipare-ai.md`.

### Manual CLI — încărcare condiționată

Agentul care folosește un script individual cu opțiuni sau comportament care
nu sunt rezumate aici, un flag în afara rețetei minime, automatizează/filtrează
rapoarte, depanează un apel sau rulează evaluatorul contextual citește
`references/limba/cli-verificare.md` **înainte** de comandă sau de interpretarea
rezultatului. Acolo sunt contractele detaliate de
intrare/ieșire, limitele și opțiunile scripturilor. Nu încărca manualul pentru
o sarcină simplă care folosește doar comenzile și contractele critice de mai sus.

`evaluare-contextuala.py` nu verifică text și nu rulează modele: numără
predicții deja furnizate față de corpusul draft
`tests/fixtures/evaluare-contextuala.json` (`draft_nevalidat_uman`), deci nu
produce benchmark. `--split referinta|holdout` limitează validarea și numărarea
la splitul ales; trebuie acoperite toate ID-urile lui. Exit 0 evaluare completă,
1 predicții incomplete/invalide, 2 eroare de fișier/JSON/corpus. Nu face parte
din fluxul de scriere.

### Cum citești raportul

- `critic` se corectează; `important` se verifică în fragment; `minor` e semnal
  de recitire, nu corecție automată. `prag_depasit` explică densitatea, nu o
  eroare izolată.
- `→` e o corecție canonică posibilă: adapteaz-o la acord și topică, nu o
  aplica mecanic.

Manualul detaliat de format al raportului, praguri, ieșiri și comportamentul
fiecărui script este în `references/limba/cli-verificare.md`. Înainte de uz
individual/avansat, urmează instrucțiunea de încărcare condiționată de mai sus.

Instrumentele sunt sprijin, nu verdicte; limitele reale de execuție le impune
harness-ul. `check-ritm.py` are praguri provenite din corpusuri englezești și
poate da fals pozitive pe registru formal. Judecata asupra ritmului,
naturaleții și relevanței rămâne manuală.
