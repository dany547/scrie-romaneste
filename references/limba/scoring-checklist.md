# Checklist de limbă — naturalitate, ritm, gramatică

Listă de citit înainte de livrare, partea de limbă. Pentru densitatea informației și
partea online vezi `references/seo/scoring-checklist.md`.

Nu e o rubrică de punctaj. Un text nu devine bun fiindcă adună puncte, iar
`scripts/verifica.py` numără penalizări deterministe (`scor_automat=X/13`), nu
calitate. Întrebarea la fiecare punct e „e corectat sau e o alegere pe care o susțin?",
nu „câte puncte îmi dau?".

## 1. Naturalitate — clișee și formatare

Verifică față de `anti-tipare-ai.md`: tranziții mecanice, introduceri formulaice,
umpluturi meta-text, adjective corporatiste, cuantificări vagi, hedging, abuz de
simboluri (emoji, liste cu „-", liniuță ca paranteză, bold/italic — §I).

*Intrare mecanică:* `scripts/check-tipare.py`, categoria `simboluri_excesive` inclusă.

**Blocant:** orice rezultat `critic` rămas necorectat — artefact de chat, placeholder,
introducere formulaică, calc din engleză. Astea sunt erori, nu alegeri.
**De recitit:** semnalele `important` și `minor`, plus categoriile care se raportează
fără scor (`copula_evitata`, `referinta_vaga`). Se taie dacă nu adaugă nimic; se
păstrează dacă genul le cere.

Pentru cu ce înlocuiești, nu doar ce tai: `exemple-voce.md`.

## 2. Ritm

Alternanță de fraze scurte și lungi; paragrafe de lungime variabilă; fără structura de
eseu școlar repetată la fiecare paragraf.

*Intrare mecanică:* `scripts/check-ritm.py`. **Semnalele lui nu sunt blocante.** Pragurile
vin din corpusuri englezești și dau fals pozitiv pe registru formal, tehnic și juridic —
vezi nota din capul scriptului. `ritm_uniform` sau `fraze_egale` înseamnă „recitește cu
voce tare", nu „textul e greșit". Dacă la citit sună bine în registrul ales, păstrează-l
și treci mai departe.

`capcana_concluziei` merită tăiată în articol, postare sau pagină; într-un raport, o
lucrare academică sau o notă juridică, concluzia e cerută de gen.

Nu forța lungimi diferite ca să miști o metrică. Ritmul se schimbă rescriind ideea, nu
tăind fraze la nimereală.

## 3. Corectitudine gramaticală și lexicală

Verifică față de `gramatica-stil.md` (normă) și `tipare-ro.md` (tipare de eșec ale
modelelor): acord la distanță, regim prepozițional, flexiune, calcuri din engleză,
pleonasme, diacritice cu virgulă (`ș`/`ț`) nu cu sedilă.

**Blocant:** tot ce e eroare de normă. Paronimele semnalate de `check-modelisme.py` sunt
informative — scriptul vede două cuvinte în aceeași frază, nu sensul; verifică-le tu și
ignoră semnalul dacă ambele sunt folosite corect.

**Titlu și excerpt** se recitesc separat pentru acord: neutre la plural (virusuri
funcționale, nu virusuri funcționali), numeral+substantiv (primii/primele, doi/două),
genul adjectivelor — `tipare-ro.md` § `acord_plural_neutru`.

## Texte scurte

Sub 100 de cuvinte — titluri, sloganuri, mesaje — aplică doar ce se aplică. Statistica de
ritm nici nu rulează sub 5 fraze.
