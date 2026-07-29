# Scoring checklist — limbă (naturalitate, ritm, gramatică)

Rubrică de auto-evaluare pentru un text în limba română, partea de limbă (3 din cele
5 criterii ale rubricii complete — vezi `references/seo/scoring-checklist.md` pentru
criteriile 4-5, SEO/GEO și densitatea informației).

## Criterii (0-2 puncte fiecare, max 6 pentru această jumătate)

1. **Naturalitate (lipsa clișeelor AI)** — 0-2 pct
   Verifică față de `anti-tipare-ai.md`: tranziții mecanice, introduceri formulaice,
   umpluturi meta-text, adjective corporatiste, cuantificări vagi, hedging, abuz de
   simboluri (emoji, liste cu „-", liniuță ca paranteză, bold/italic — §I).
   *Intrare mecanică:* `scripts/check-tipare.py`, categoria `simboluri_excesive`
   inclusă. Orice rezultat `critic` rămas înseamnă maximum 1 punct. Două sau mai
   multe înseamnă 0.

2. **Ritm și burstiness** — 0-2 pct
   Alternanță de fraze scurte/lungi; paragrafe de lungime variabilă; fără structură de
   eseu școlar repetitivă.
   *Intrare mecanică:* `scripts/check-ritm.py`. Dacă raportează `ritm_uniform` sau
   `fraze_egale`, nu-ți da 2/2 — indiferent cât de bine sună la citit. Dacă
   raportează `capcana_concluziei`, taie secțiunea înainte de a reevalua.

3. **Corectitudine gramaticală și lexicală (fără romgleză)** — 0-2 pct
   Verifică față de `gramatica-stil.md` (normă) și `tipare-ro.md` (tipare de eșec
   ale modelelor): acord la distanță, regim prepozițional, flexiune, calcuri din
   engleză, pleonasme, diacritice cu virgulă nu cu sedilă.

## Prag minim: 8/10 (pe rubrica completă, limbă + SEO)

Dacă scorul auto-evaluat pe partea de limbă e sub 6/6 (sau contribuie la un total sub 8/10
cu partea SEO), NU livra textul. Intră în buclă de refactoring:

1. Identifică exact ce a picat: rulează mental (sau cu `scripts/check-tipare.py`) o căutare
   a frazelor problematice — găsește toate aparițiile de „De asemenea", „În concluzie" etc.
2. Rescrie acele secțiuni aplicând regulile din `anti-tipare-ai.md` și `gramatica-stil.md`.
3. Reverifică ritmul (alternanța lungimii frazelor) — dacă tot corectat sună uniform,
   variază structura sintactică, nu doar vocabularul.
4. Repetă evaluarea. Livrează doar după ce treci pragul.

## Notă despre subiectivitate

Scorul e un instrument de disciplină, nu o știință exactă. Pentru texte scurte (sub 100
cuvinte — titluri, sloganuri, mesaje) aplică doar criteriile relevante; nu forța o evaluare
pe 6 puncte pentru un text de o propoziție.
