---
name: scrie-romaneste
description: >
  Scrie, rescrie si revizuieste text in limba romana care suna natural si uman,
  nu ca text de model: fara clisee AI (tranzitii mecanice, "in concluzie",
  introduceri formulaice, ezitari goale pastrand incertitudinea reala), fara romgleza si calcuri din engleza, cu
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

- **rescriere** (implicit) — livrează doar textul final, curat; fără metacomentarii sau liste de modificări.
- **audit** — raportează tiparele grupate pe severitate (`critic`, `important`, `minor`), cu citat și motiv. **Nu rescrie.** Începe cu `scripts/verifica.py <fișier>` (sau stdin `-`; **excepție obligatorie:** dacă intrarea e HTML/Gutenberg, proiectează-o întâi prin `references/seo/markup.md` înainte de `verifica.py`); încarcă din `references/` doar ce-ți trebuie pentru judecata calitativă sau categoriile semnalate. 7 expresii sunt pe densitate și lipsesc sub ~3 apariții (pentru ele: `check-tipare.py --tot`, detalii în `references/limba/cli-verificare.md`). Nu încheia un audit cu „0 semnale = text curat” fără recitire manuală: scriptul prinde doar `acord_numerale`, iar nici `verifica.py`, nici `--human-voice` nu au dicționar — rulează separat `scripts/check-cuvinte.py` și recitește integral (inclusiv titlul și excerptul) pentru acord, forme verbale și cuvinte inexistente (`references/limba/tipare-ro.md` §cuvant_inexistent).
- **editare** — modificări minime și țintite direct în fișierul indicat de utilizator (nu într-o copie alăturată); păstrează pasajele deja bune.
- **human-voice** — audit separat pentru reflexe mecanice de voce: `scripts/verifica.py <fișier> --human-voice` (`AI_PATTERN_SCORE/30`, `STATUS`, blocere). **Nu rescrie.** Un `PASS` aici nu atestă corectitudinea lexicală sau sensul. Reguli și excepții: `references/limba/human-voice-validator.md`.

Când cererea cere și audit, și rescriere („verifică și repară”), **livrează textul reparat urmat de un raport scurt** (ce ai schimbat și de ce). Pe un fișier al utilizatorului, modul e `editare`, nu `rescriere`.

## Profil de voce

Dacă cerința indică un ton, aplică-l consecvent; altfel alege după canal și
public. Detalii de registru în `references/limba/gramatica-stil.md` §7.

`publicistic` · `tehnic` · `colocvial` · `direct` · `cald`

Profilul schimbă lexicul și lungimea frazei, nu regulile de corectitudine.
Stabilește de la început și **tu** sau **dumneavoastră**, și nu comuta.

## Reguli critice (rezumat — detalii în references/)

Patru reguli de decizie, înaintea oricărei liste:
1. Spune concret cine face ce și de ce contează.
2. Păstrează o formulare convențională dacă se potrivește genului, vocii și scopului — nu o tăia doar fiindcă apare des în text de model.
3. Elimin-o dacă nu adaugă sens, dovadă, ritm sau relație cu cititorul.
4. Nu transforma un semnal stilistic într-o corecție automată. Erorile certe se corectează; alegerile stilistice se recitesc în context.

**Interzis** (liste și praguri în `references/limba/anti-tipare-ai.md`):
- Tranziții mecanice („în concluzie”, „prin urmare”, „de asemenea”, „totodată”, „mai mult decât atât”, „pe de o parte... pe de altă parte”), introduceri formulaice („în lumea de astăzi”, „în era digitală”), umpluturi meta-text („este important de menționat că”, „merită subliniat”).
- Adjective corporatiste („revoluționar”, „impresionant”, „abordare holistică”), cuantificări vagi („o serie de”, „o gamă largă de”), hedging gol („este posibil ca”, „s-ar putea ca” — dar **păstrează incertitudinea reală** când datele au limite).
- Romgleză și calcuri („face sens” → „are sens”; „a adresa o problemă” → „a aborda”; „în termeni de” → „în ceea ce privește”).
- „Capcana concluziei” (rezumat forțat la final), ritm monoton/paragrafe simetrice și **afirmații goale** fără agent sau mecanism (`anti-tipare-ai.md` §J; în text literar, redundanța poate fi stil).
- Abuz de simboluri (`anti-tipare-ai.md` §I), liniuța-cârjă repetată (`tipare-ro.md`, `punctuatie_carja`; dialogul și intervalele rămân neatinse), bullet Unicode „•” și ornamente `§ ¶ † ‡`.
- **En-dash `–`: niciodată.** Cratimă în compuse/intervale („10-12 zile”), linie de pauză `—` în incize (`liniuta_engleza`).
- Clickbait de tabloid și titlu-șablon de agenție („Ghidul suprem”, „Tot ce trebuie să știi” — `references/seo/titluri.md`).

**Obligatoriu**:
- Diateza activă (`references/limba/gramatica-stil.md` §4), cititor concret (`references/limba/scris-eficient.md`) și diacritice cu virgulă (`ș`, `ț`), nu sedilă (`ş`, `ţ`).
- Fără fapte, cifre, citate sau date de business inventate (`references/limba/tipare-ro.md`, `sursa_fabricata`, `references/seo/grounding.md`): ce lipsește se cere sau rămâne `[DE COMPLETAT: …]`. Fără date reale/personale de client neautorizate.
- Nu livra cuvinte pe care nu le poți susține. `verifica.py` și `--human-voice` nu au dicționar; `scripts/check-cuvinte.py` dă suspecți de verificat, nu verdicte (lipsa ≠ inexistență). Verifici forma, lema, sensul și registrul doar în surse permise, manual, fără scraping (`references/limba/revizie-contextuala.md` §acces); sugestiile nu confirmă; la neclar întrebi (`references/limba/tipare-ro.md` §cuvant_inexistent).
- Pentru conținut online: titlu cu promisiune concretă (`references/seo/titluri.md`) și deschidere directă (`references/seo/flux-articol.md`).

**Regulile de mai sus sunt suficiente ca să scrii un text bun.** Deschide din `references/` doar ce cere task-ul; **nu reconstitui din numele fișierului ce crezi că scrie în el.**

## Fluxul de lucru

Exemplu cap-coadă: `references/limba/flux-exemplu.md`.

1. **LOAD** — stabilește modul, profilul de voce și ruta din tabel:
   - **editare/rescriere scurtă**: `references/limba/anti-tipare-ai.md` la rescriere; nu încărca restul `references/` și nici manualul CLI.
   - **audit**: rulează întâi `scripts/verifica.py` (pe HTML/Gutenberg, proiectează întâi via `references/seo/markup.md`), apoi încarcă referințe doar la nevoie.
   - **articol simplu / blog (implicit)**: `references/limba/anti-tipare-ai.md`, `references/limba/exemple-voce.md` (pentru voce vie), `titluri.md`, `flux-articol.md` și `revizie-contextuala.md`. Încarcă `grounding.md` **doar** la date comerciale/de business, iar `blog-keyword.md`, `core.md`, `geo.md` **doar** pe trigger separat. La **text pur literar**, sari peste partea SEO și protejează repetiția, ritmul și dialogul.
   - **reclame / social / markup / CLI avansat / doar metadate**: urmează direct rândul din tabel (`reclame/`, `social/`, `markup.md`, `cli-verificare.md`; pentru doar metadate/heading-uri, nu edita corpul).
2. **CONTRACT** (intern, nu în livrare) — fixează **decizia cititorului**, **dovezile confirmate**, publicul, canalul/genul, registrul, `tu`/`dumneavoastră`, limitele de platformă la reclame (`references/reclame/platforme.md`) și incertitudinile reale (fără cote fixe de lungime/cuvinte-cheie). Cere o singură dată, grupat, doar ce e indispensabil.
3. **CONTEXT** — la conținut comercial, adună datele reale după conținut (`CLAUDE.md`/`AGENTS.md`, proiect, pagină publicată, conversație); detalii în `references/seo/grounding.md`. Sari la text literar sau fără date de business.
4. **DRAFT** — dintr-o trecere (`references/limba/scris-eficient.md` §1); pe text lung, pe bucăți cu `scripts/verifica.py` între ele (pe HTML/Gutenberg, proiectează întâi via `references/seo/markup.md`).
5. **AUTOCORECȚIE** — rulează `scripts/verifica.py <fișier>` (pe HTML/Gutenberg, proiectează **întâi** via `references/seo/markup.md` și rulează `verifica.py --fara-seo` pe proiecții; combină `--human-voice` unde e util; `--fara-seo` pentru non-online/literar; `--reclame` pentru anunțuri `H1:`/`D1:`/`Text:`/`Titlu:`). Verifică titlul, meta și excerptul separat lângă corp. Aplică `→` cu acord și topică; citește `human-voice` în context (blochează doar garbage, contaminare, placeholder-e).
   Apoi `references/limba/revizie-contextuala.md`: propoziție cu propoziție + **revizia obligatorie pe câmpuri** înainte de livrarea articolelor/paginilor online (SEO title, H1, meta, excerpt separat dacă se aplică, fiecare H2/H3 — snippet/outline, apoi față de secțiunea reală și decizia cititorului; verdict per câmp, citat/motiv/înlocuire minimă cu dovezi; textul bun rămâne neatins). Pe text persuasiv, testul §J din `anti-tipare-ai.md`.
6. **PASUL DOI** — reauditează textul corectat; maxim 2 cicluri pe FINAL, apoi escaladează. Observațiile rămân interne.
7. **POARTA DE LIVRARE** — verifică pe raportul deja rulat (fără rulare obligatorie doar cu `--scor`; `scor_automat=X/13` e penalizare deterministă, nu notă):
   - fără fapte, cifre, citate sau date de business inventate; incertitudinea reală păstrată;
   - fără artefacte de chat, markup rezidual sau placeholder publicabil;
   - erori certe + acord manual în titlu, meta, excerpt și heading-uri;
   - citire integrală + `scripts/check-cuvinte.py` (`revizie-contextuala.md` §acces, fără lookup automat; neclar se întreabă);
   - semnale stilistice și `--human-voice` fără blocere (`PASS` ≠ corectitudine/sens);
   - revizia contextuală + revizia pe câmpuri trecute (`references/limba/revizie-contextuala.md`);
   - online: titlu concret onorat în corp, deschidere directă, subtitluri coerente; HTML/WP: `references/seo/markup.md` + status explicit Gutenberg (`unverified` fără mediu disposable autorizat); reclame: `--reclame` curat.
   Liste opționale: `references/limba/scoring-checklist.md`, `references/seo/scoring-checklist.md`.
8. **LIVRARE** — conform modului; livrabilul intră în răspuns, iar la `editare` modificarea e în fișierul indicat cu poarta rerulată și confirmarea scurtă (citire integrală + `--human-voice` fără blocere). Semnalează separat `[DE COMPLETAT: …]`.
   În flux agentic: audit limbă + human-voice → editare minimă → reverificare → citire integrală lexic → reviewer editorial în **context proaspăt** când gazda/coordonatorul suportă și permite (prompt mărginit: text final + câmpuri + brief/decizia cititorului + dovezi confirmate, fără raționamentul scriitorului), altfel **auto-review** declarat; **reviewer-ul nu editează markup crud** și nu rescrie pasaje curate.

## Rutare și structura `references/`

Încarcă doar fișierele relevante — nu e nevoie să citești tot `references/` pentru o sarcină scurtă.

| Rută / Task | Fișiere de încărcat |
|---|---|
| editare/rescriere scurtă | `limba/anti-tipare-ai.md` (opțional `limba/exemple-voce.md`) |
| audit | întâi `scripts/verifica.py` (sau `seo/markup.md` întâi pe HTML/WP); apoi doar ce semnalează |
| articol simplu / blog (implicit) | `seo/titluri.md`, `seo/flux-articol.md`, `limba/revizie-contextuala.md` (+ `limba/anti-tipare-ai.md`) |
| conținut comercial / date de business | adaugă `seo/grounding.md` (doar când există date de firmă/produs/preț) |
| cercetare cuvinte-cheie / intenție | `seo/blog-keyword.md` |
| SEO tehnic, on-page, specific RO | `seo/core.md` |
| GEO / optimizare AI search | `seo/geo.md` |
| pagină de produs/categorie | `seo/core.md`, `seo/ecommerce.md`, `seo/titluri.md`, `seo/flux-articol.md`, `seo/grounding.md` |
| doar metadate / heading-uri | `seo/titluri.md`, `limba/revizie-contextuala.md` (fără editarea corpului) |
| markup HTML / WordPress (Gutenberg) | `seo/markup.md` (+ `limba/revizie-contextuala.md` pentru câmpuri/text) |
| text de reclamă Google/Meta/TikTok | `reclame/platforme.md`, `reclame/voce.md`, `limba/anti-tipare-ai.md` §J, `seo/grounding.md` |
| postare organică (IG/FB/LI/TikTok/forum) | `social/README.md`, `social/organic.md`, `limba/anti-tipare-ai.md` §K, `seo/grounding.md` |
| blog personal, lifestyle | `social/README.md`, `social/blog-personal.md`, `limba/anti-tipare-ai.md` §K |
| afacere locală / contact | `seo/core.md`, `seo/local.md`, `seo/grounding.md` |
| schema / date structurate | `seo/schema.md` |
| audit SEO complet, link building | `seo/core.md`, `seo/avansat.md` |
| CLI avansat / script individual | `limba/cli-verificare.md` |

Index `references/`:
- `limba/`: `anti-tipare-ai.md`, `exemple-voce.md`, `revizie-contextuala.md`, `human-voice-validator.md`, `cli-verificare.md`, `flux-exemplu.md`, `tipare-ro.md`, `gramatica-stil.md`, `scris-eficient.md`, `modelisme.md`, `calcuri.json`, `scoring-checklist.md`.
- `seo/`: `core.md`, `grounding.md`, `titluri.md`, `flux-articol.md`, `geo.md`, `schema.md`, `ecommerce.md`, `blog-keyword.md`, `local.md`, `avansat.md`, `markup.md`, `scoring-checklist.md`.
- `reclame/`: `platforme.md`, `voce.md`.
- `social/`: `README.md`, `organic.md`, `blog-personal.md`.

## scripts/

### Rețeta minimă și contracte critice

Scripturile stau în directorul skill-ului; rezolvă calea relativ la `SKILL.md` o singură dată. Punctul de intrare recomandat: `verifica.py`.

```bash
python3 <cale-skill>/scripts/verifica.py - <<'TEXT'
Textul integral, cu diacritice.
TEXT
```

sau, dacă textul e deja într-un fișier al proiectului:

```bash
python3 <cale-skill>/scripts/verifica.py drafts/articol.md
```

Pe Windows/PowerShell folosește un fișier temporar (nu escaping). Opțiuni uzuale: `--fara-seo`, `--scor`, `--json`, `--prag N`, `--human-voice`, `--reclame`, `--platform google|meta`, `--brand "Nume"`.

- **Exit codes**: `0` curat, `1` semnale (normal, nu eșec), `2` eroare de input/UTF-8 (convertește cu `iconv -f WINDOWS-1250 -t UTF-8`).
- **`--fara-seo`**: pentru text non-online sau fragmente proiectate; sedila se verifică oricum și rămâne sub `seo` (nu elimina cheia `seo`).
- **Scheme text**: `tipare`/`modelisme` emit `severitate|categorie|L<linie>|fragment[|→ sugestie]`; `ritm` emite `metrici|...` și `<semnal>|incredere=...|detaliu`, fără `L<n>`; `seo` emite `severitate|categorie|detaliu|context`; `human-voice` și `reclame` au scheme proprii cu `L<n>`. Pentru procesare programatică folosește `--json` (fragmentele pot conține `|`).
- **Scor și voce**: `scor_automat=X/13` e penalizare deterministă, nu notă (SEO nu intră); `--scor` e opțional. `--human-voice` se poate combina în același apel cu `verifica.py` (și cu `--json`, fără să schimbe `/13`); nu e corectură lexicală.
- **`--reclame`**: pentru fișiere cu etichete `H1:`/`D1:`/`Text:`/`Titlu:`; limite platformă, politici și afirmații goale (stratul SEO se reduce la sedilă).
- **`check-cuvinte.py`** (separat, fără scor): suspecți de verificat, nu verdicte; exit 0/1/2 (cu `--sugestii`, exit 2 poate indica Hunspell sau dicționarul indisponibil/defect când există suspecți afișați).
- **`check-calcuri.py`** (separat, opt-in, fără scor): colocări de recitit din `references/limba/calcuri.json`, semnal neutru către revizia contextuală (exit 0/1/2; detalii în manualul CLI).
- **Markup HTML/WordPress**: regula de proiecție din `references/seo/markup.md` are prioritate față de apelul direct `verifica.py <fișier>`, inclusiv în modul `audit` și pe drafturi lungi pe bucăți (proiectează întâi, apoi rulează `verifica.py --fara-seo` pe proiecții).
- Dacă `python3` lipsește, sari peste pasul mecanic, spune-o pe scurt și verifică pe `references/limba/anti-tipare-ai.md`.

### Manual CLI — încărcare condiționată

Citește `references/limba/cli-verificare.md` **înainte** de comandă sau interpretare dacă folosești un script individual, flag-uri în afara rețetei minime, filtrare/automatizare, depanare ori `evaluare-contextuala.py` (pilot offline pe corpus draft, în afara fluxului de scriere). Nu încărca manualul pentru sarcini simple acoperite de rețeta de mai sus.

### Cum citești raportul

- `critic` se corectează; `important` se verifică în fragment; `minor` e semnal de recitire, nu corecție automată; `prag_depasit` explică densitatea.
- `→` e corecție canonică: adapteaz-o la acord și topică.

Instrumentele sunt sprijin, nu verdicte; limitele reale le impune harness-ul. `check-ritm.py` are praguri din corpusuri englezești (posibile fals-pozitive pe registru formal). Judecata de ritm, naturalețe și sens rămâne manuală.
