# Plan: postări organice, blog personal și reclame (Meta, Google, TikTok)

Data: 2026-11-05. Autor: Claude (Sonnet 5.5). Status: **PLAN, neimplementat. Cere critică.**
Context: auditul pe texte de modele mici (`findings-si-plan.md`) a arătat că skill-ul nu are reguli
pentru postări organice (Instagram, Facebook, LinkedIn, TikTok, forum) și are doar reguli de bază
pentru reclame (Google RSA, Meta). Modelele au produs hashtag-uri fără diacritice, emoji decorative,
engagement bait („Salută-mă în comentarii”) și mărturii personale inventate.

## 1. Ce există azi

| Zonă | Fișiere | Acoperire |
|---|---|---|
| Blog (SEO, structură) | `references/seo/blog-keyword.md`, `flux-articol.md` | deschidere, ritm, final, SEO; **nu** voce de blog personal/lifestyle |
| Reclame plătite | `references/reclame/platforme.md`, `voce.md`, `scripts/check-reclame.py` | Google RSA (30/90, politici), Meta (text/titlu/descriere, max 3 hashtag-uri) |
| Postări organice | nimic | — |
| TikTok (organic sau ads), LinkedIn, Performance Max | nimic | — |

`check-reclame.py` recunoaște etichetele `H1…H15`, `D1…D4`, `Cale1/2` (Google) și `Text`, `Titlu`,
`Descriere` (Meta), cu `--platform google|meta`. `platforme.md` e marcat „verificat 2026-09-07”.

## 2. Principii

- **Fapte vs. sfaturi.** Limitele numerice intră în skill doar cu sursă oficială, URL și dată.
  Fără sursă → scris explicit „neverificat”, nu o cifră. Sfaturile de conversie sunt separate și marcate.
- **Platformele își schimbă regulile.** Nu hardcodăm în scripturi limite de organic. Scripturile
  verifică doar limite hard documentate (reclame) și tipare de limbă.
- **Reguli de voce, nu șabloane.** Fiecare platformă primește principii și contra-exemple, nu texte-tip
  de copiat (altfel apar clișee noi).
- **Minim de risc.** Nimic din ce există nu se rescrie; adăugăm fișiere și categorii noi, cu teste.

## 3. Componente

### C1. `references/social/organic.md` (nou, doar referință)

Secțiuni: Instagram (caption, carusel, reels), Facebook (pagină/grup), LinkedIn, TikTok organic,
forum/comunități, blog personal/lifestyle (voce, nu SEO). Fiecare conține:
- limite verificate (tabel, cu sursă și dată) și punctul de trunchiere acolo unde e documentat;
- structură care ține de cititor: hook în prima linie vizibilă, un singur CTA, link în text vs. comentariu
  (marcat „sfat”, cu sursă);
- ce e penalizat sau respins (engagement bait, hashtag-uri excesive);
- specific românesc: diacritice în hashtag-uri și text, registrul (tu/dumneavoastră) pe canal;
- 2–3 exemple prost/bine (din textele modelelor, rescrise de noi), cu motivul.
Rutare în `SKILL.md`: rând nou în tabelul de rutare, `references/social/organic.md` +
`limba/anti-tipare-ai.md` §K + `grounding.md` pentru conținut comercial.

### C2. Reclame: `references/reclame/platforme.md` (extins)

- Secțiune nouă **TikTok Ads** (limite pentru ad text, nume brand, CTA, politici), doar din documentație
  oficială.
- **Performance Max**: număr și limite pentru text assets, doar dacă sunt verificabile oficial.
- Actualizare dată de verificare; valorile neconfirmate se marchează „neverificat”.
- `voce.md`: o secțiune „Reclame native pe platforme sociale” (stil TikTok/Meta Reels: voce directă,
  demonstrație, fără ton de spot) și lista de formule de engagement bait respinse în reclame.

### C3. `scripts/check-reclame.py` (extins, opțional și doar după C2)

- `--platform tiktok` cu limite din C2. Eticheta pentru text de reclamă TikTok: aceeași `Text:`,
  distinsă doar prin `--platform tiktok` sau prin heading („TikTok”), ca să nu intrăm în conflict cu
  Meta.
- Fără etichete noi pentru PMax decât dacă limitele din sursă sunt clare.
- Teste cu fixture-uri bune/rele, ca la Google și Meta.

### C4. `scripts/check-tipare.py` (două categorii noi, ieftine)

- `hashtag_fara_diacritice` (`minor`): hashtag care conține un cuvânt românesc fără diacriticele
  cerute (`#dimineata`, `#liniste`). Dificultate: fără lexicon nu știm ce cuvinte cer diacritice →
  folosim lista mică de forme fără variantă validă fără diacritice (aceeași idee ca în
  `diacritice_lipsa`), plus sufixe sigure. Acceptăm fals negative multe, fără fals pozitive.
- `engagement_bait` (`important`): „salută-mă în comentarii”, „comentează cu…”, „taguiește un prieten”,
  „dă share dacă”, „distribuie, te rog” când cererea nu are legătură cu conținutul. Formule fixe,
  fără euristici largi. Exclus din text citat și din dialog.
- Ambele se aplică pe orice text; nu depind de platformă.

### C5. Fixture-uri și teste

- Fixture-uri noi în `tests/fixtures/social/`: postări bune (scrise de noi, scurte), postări rele
  (extrase adaptate din textele celor trei modele), reclame TikTok bune/rele.
- Teste: fiecare regulă nouă, cu un caz pozitiv, unul negativ și unul de graniță.
- Setul de control uman rămâne în afara repo-ului; pentru fals pozitive pe social media folosim
  fixture-uri scrise de noi, nu texte copiate.

### C6. Documentație

`SKILL.md` (rutare, mod „social”), `references/limba/cli-verificare.md`, `README.md` + `README.en.md`
(testele de paritate a flag-urilor impun consecvență), `tipare-ro.md` pentru noile categorii.

## 4. Ordine propusă

1. C4 (detectoare, cu teste) — deterministe, risc mic.
2. Cercetare verificată (rapoartele de la subagenți, vezi §6) → C2 (referința de reclame, inclusiv TikTok).
3. C1 (organic.md) pe baza cercetării.
4. C3 (script TikTok), doar dacă C2 are limite clare.
5. C6 (documentație, README-uri, teste de paritate).

## 5. Ce NU facem

- Nu hardcodăm în scripturi limite pentru postări organice.
- Nu promitem „scoruri de conversie” sau „algoritmul preferă X”; doar sfaturi cu sursă.
- Nu adăugăm șabloane de postări de copiat.
- Nu modificăm `check-ritm.py`, `check-seo.py` sau regulile existente.
- Nu includem texte cu drepturi de autor în repo.

## 6. Cercetare (input pentru plan)

Trei rapoarte, în `docs/audit-modele/cercetare/`:
- `cercetare-luna.md` (`gpt-6-luna` via pi/openai-codex): subțire, 17 valori „NEVERIFICAT”, doar
  limitele Google RSA confirmate; data din antet („18 februarie 2025”) e greșită, de ignorat.
- `cercetare-organic.md` (Sonnet 5.5, cu acces web). Confirmat oficial: Instagram 2.200 caractere,
  max 20 slide-uri, 5 hashtag-uri (anunț gradual din 2025-12-18); LinkedIn 3.000; TikTok 2.200
  (UTF-16, prin API). NEVERIFICAT: punctele „mai mult/vezi mai mult”, politica engagement bait,
  hashtag-uri Facebook/LinkedIn/TikTok, forumuri românești.
- `cercetare-ads.md` (Sonnet 5.5, cu acces web). Confirmat oficial: Google RSA și Performance Max;
  Meta: 50–150 text principal, 27 titlu (**diferă de 125/40/25 din `platforme.md`**, de lămurit);
  TikTok: doar lista oficială de CTA. NEVERIFICAT: politici Meta/TikTok, maxime Meta, limite text și
  nume brand TikTok (paginile oficiale au dat 404 sau doar titlul).

Consecință pentru plan: din C1/C2 se pot scrie ferm doar limitele confirmate; restul rămâne marcat
„neverificat”, cu instrucțiunea de a verifica în interfața platformei înainte de producție.

## 7. Riscuri și întrebări deschise (pentru critică)

1. **Limite instabile.** Cât din C1/C2 riscă să fie depășit în luni? Merită o dată de verificare
   obligatorie și un test care semnalează fișierul dacă dată > 6 luni?
2. **TikTok în `check-reclame.py`:** conflict de etichete cu Meta. `--platform tiktok` obligatoriu e
   suficient sau complică utilizarea?
3. **`engagement_bait`:** fals pozitive în texte legitime (concursuri, întrebări autentice către
   comunitate). Formule fixe sunt suficiente sau categoria ar trebui doar `minor`?
4. **`hashtag_fara_diacritice`:** valoare mică vs. fals pozitive (hashtag-uri de brand). Merită?
5. **Blog personal:** reguli de voce în `organic.md` sau fișier propriu `references/social/blog-personal.md`?
6. **Dimensiunea skill-ului:** `SKILL.md` e deja lung. O rutare nouă adaugă încărcare cognitivă; mai
   bine un fișier-index `references/social/README.md`?
7. **Conversie:** există sfaturi cu dovezi solide (nu bloguri de marketing) pe care ne putem baza?
   Dacă nu, secțiunile de „conversie” ar trebui reduse la principii generale cu sursă.
8. **Prioritate:** care componentă aduce cea mai mare valoare pe unitatea de risc?

## 8. Cerere pentru reviewer

Critică acest plan, nu implementa nimic. Pentru fiecare componentă C1–C6: merită / nu merită, risc,
ce schimbi. Citește `references/reclame/*`, `scripts/check-reclame.py` și `scripts/check-tipare.py` ca să
verifici fezabilitatea. Citește rapoartele din §6 și spune ce nu se poate folosi ca atare (cifre fără
sursă, dată greșită, afirmații de marketing). Răspuns scurt, verdictul primul.

## 9. Critica lui Opus 5.5 și status implementare (2026-11-05)

Verdict: planul e bun, ordinea se schimbă; C3 (TikTok în script) și `hashtag_fara_diacritice` se amână.
Opus a găsit și o eroare existentă: `platforme.md` și `check-reclame.py` verificau Meta după cifre
(125/40/25) care nu mai apar pe pagina oficială (ghidul actual: text 50–150, titlu 27).
Bug-uri de parser confirmate în cod: un rând care începe cu `#hashtag` era tratat ca heading și reseta
platforma; `Description:` sub heading Meta era tipat Google și nu i se verifica limita.

| Punct | Status |
|---|---|
| Corectură Meta (150/27, descriere fără recomandare), parser `#`, `Description:` sub Meta | FĂCUT, cu teste |
| C4 `engagement_bait` (minor, formule fixe; întrebări reale nu se prind) | FĂCUT, cu teste |
| C4 `hashtag_fara_diacritice` | AMÂNAT: `#romania`/`#bucuresti` fără diacritice sunt etichetele folosite |
| C2 PMax (oficial), TikTok doar CTA și „neverificat", reclame native în `voce.md` | FĂCUT |
| C1 `references/social/` (README, organic, blog-personal) | FĂCUT, doar cifre confirmate |
| C3 TikTok în `check-reclame.py` | AMÂNAT: fără limite oficiale; scriptul trimite orice non-Google pe ramura Meta |
| C6 rutare în `SKILL.md`, `tipare-ro.md` | FĂCUT; README-urile (RO/EN) neactualizate |
| Test de vechime pentru data din `platforme.md` | DE DECIS |
