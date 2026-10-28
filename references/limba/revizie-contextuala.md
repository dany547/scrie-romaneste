# Revizie contextuală — propoziție cu propoziție, pe sens

Scripturile prind tipare, nu sens. O construcție nouă, nefirească, iese curată
din `verifica.py` fiindcă nu seamănă cu nimic din liste — și niciun script nu
învață modelul din ce i-ai corectat o dată. Fișierul ăsta e trecerea manuală
care lipsește: citești **toate** propozițiile în context de paragraf și public,
nu doar cuvintele suspecte sau semnalele din raport. Se aplică în fluxul deja
existent AUTOCORECȚIE → PASUL DOI → POARTĂ; nu e un flux nou.

## procedura

Parcurgi textul FINAL (nu draftul) cap-coadă, inclusiv titlul și excerptul ca
texte separate, lângă corp. La fiecare propoziție întrebi, în ordine:

1. **Verb–obiect:** cine face ce, cui? Verbul cere un obiect de tipul potrivit
   (o decizie se „ia", o cerere se „trimite", o întrebare se „pune")?
2. **Sensul expresiei:** formula există ca formulă, sau sunt doar cuvinte
   corecte puse unul lângă altul? Expresiile nu se traduc cuvânt cu cuvânt.
3. **Referentul:** fiecare pronume, demonstrativ și posesiv trimite la un
   singur candidat? Cu doi-trei candidați în frază, înlocuiești cu
   substantivul — repetiția clară bate eleganța ambiguă.
4. **Coerența:** la transformare — ce se schimbă în ce? La comparație — ce e
   comparat cu ce, pe ce scară măsurabilă? La cauzalitate — ce cauzează ce,
   prin ce mecanism?
5. **Rolul cititorului:** ce i se cere să facă, să creadă sau să simtă? Poate
   face asta (are contul, butonul, dreptul, informația)? Acțiunea imposibilă e
   eroare, nu stil.
6. **Jargon/registru:** termenul se potrivește genului și publicului? Un termen
   tehnic corect într-o fișă tehnică nu se „simplifică"; același termen într-un
   text pentru public larg se explică sau se înlocuiește.

Pentru fiecare problemă notezi în raportul de audit (livrabil în modurile
`audit`/`human-voice`, intern în `rescriere`/`editare`): **citatul exact**,
**motivul concret** (care întrebare de mai sus pică și de ce), **corecția
minimă** (schimbi doar ce repară sensul) și **verdictul**:

- `eroare susținută` — demonstrabilă printr-o regulă, o sursă sau contextul
  explicit din text (construcție nefirească, acțiune imposibilă, contradicție
  internă); se corectează.
- `suspiciune contextuală` — miroase a calc sau a referent rupt, dar sprijinul
  lipsește; se verifică, nu se corectează din burtă.
- `preferință` — ambele forme stau în picioare; alegi deliberat și mergi mai
  departe.
- `neclar` — sensul nu se poate reconstrui; întrebi utilizatorul.

Nu rescrie pasaje bune: o propoziție fără problemă rămâne neatinsă, chiar dacă
s-ar putea formula și altfel. Auditul nu editează: în modurile audit/human-voice
livrezi raportul fără să modifici textul; în rescriere și editare, observațiile
intermediare rămân interne și nu poluează livrarea. Pe FINAL, maxim 2 cicluri
audit → editare minimă → reverificare; dacă rămâne dezacord sau necunoscut,
escaladezi (întrebi), nu iterezi a treia oară.

Ce nu sunt erori: **metaforele și intonația** nu se „corectează" automat —
într-un text literar redundanța poate fi stil, iar o metaforă legitimă rămâne
chiar dacă sună neobișnuit la prima citire. Un text **conversațional** nu
înseamnă telegrafic și nici colocvial forțat: registrul ales la CONTRACT
decide, nu o regulă de simplificare. Protejezi **faptele, cifrele, numele,
negațiile, obligațiile și intenția** textului: o corecție care schimbă ce
promite textul e mai gravă decât greșeala pe care o repară.

Două mini-cazuri, ca principiu (nu ca listă de interdicții):

- „Raportul face o poză de ansamblu a pieței." — alegere contextuală, nu eroare:
  poate fi metaforă, poate fi formulă neașezată. Fără sursă care s-o infirme și
  fără ruptură logică în context, verdictul e `preferință`, cu alternativa neutră
  „Raportul dă o vedere de ansamblu a pieței." Alegi deliberat după registru —
  într-un text cu voce poți păstra metafora — fără interdicție.
- „După ce firma a preluat distribuitorul, și-a schimbat directorul." — al cui
  directorul? `suspiciune contextuală` spre `neclar`: dacă paragraful anterior spune
  explicit că distribuitorul și-a schimbat directorul, corectezi minim cu
  substantivul; altfel întrebi înainte să alegi — o rescriere care alege singură
  poate inversa sensul.

## dovezi

Judecata fără sprijin rămâne etichetată (`suspiciune contextuală`, `neclar`),
niciodată «confirmat». Sprijinul poate fi o regulă, o sursă sau contextul
explicit din text: o nepotrivire logică vizibilă în text (acțiune imposibilă,
contradicție internă) se susține din context, nu cere neapărat o intrare DEX. Sursele, pe roluri:

- **DEX / surse explicative de sensuri și expresii** — pentru ce înseamnă o
  vorbă și ce sensuri are o expresie. Citește **forma și lema plus TOATE
  sensurile relevante, registrul și ediția**; fără cherry-pick de sens și fără
  citat decorativ.
- **DOOM — forme și morfologie, nu definiții.** Îți spune cum se scrie și cum
  se flexionează, nu ce înseamnă.
- **Gramatică și uz** — pentru construcții (regim prepozițional, acord,
  topică): ce construcție e legitimă, nu ce sens are un cuvânt.

Două limite care nu se negociază: **absența nu dovedește inexistența**
(o formă poate lipsi dintr-o sursă și exista în limbă), iar **existența formei
nu dovedește potrivirea sensului** (cuvântul există, dar cu alt sens decât cel
din text — atunci îl tratezi ca neatestat, ca la `tipare-ro.md`
§cuvant_inexistent). Dovada înseamnă: sursă / ediție / identificator sau URL +
explicația legăturii cu propoziția din text. Fără sursă disponibilă, concluzia
e `neconfirmat` / întrebare, nu PASS lexical implicit. Și nu promite ce nu poți
livra: DEX-ul conține și expresii, dar nu validează orice combinație nouă —
potriveala unei colocații noi se judecă în context, nu se „demonstrează"
printr-o singură intrare.

## acces

- Licența dexonline (dexonline.ro/licenta) interzice accesul și extragerea
  automată fără acord, cu excepția seturilor oferite oficial. Asta te privește
  direct: **nu autoriza scraping și nu instrui ocoliri** — nici „câte un
  cuvânt cu curl", nici API presupus. Lookup-ul e manual, făcut de utilizator;
  tu lucrezi cu dovezi furnizate de el sau cu seturi autorizate.
- DOOM afișează pe doom.lingv.ro licența CC BY-NC-SA 4.0: o respecți ca atare —
  nu încorpora conținutul implicit într-o distribuție comercială și nu copia
  definiții protejate în repo. Linkurile către o sursă nu înseamnă permisiune
  de copiere.
- Dacă utilizatorul oferă un extras dintr-o sursă ca să verifici un sens, îl
  folosești la verificare; nu presupune din asta un drept de redistribuire.

## evaluare — propunere, nu rezultat

Corpusul de pilot există la `tests/fixtures/evaluare-contextuala.json`:
60 de cazuri sintetice draft, etichete nevalidate uman, cu split pe familie.
Câtă vreme etichetele nu sunt validate uman, **nu pretinde benchmark trecut
sau câștig măsurat** — e material de lucru, nu dovadă.

Propunerea de evaluare onestă, când vine vremea: compară bază vs instrucțiuni
vs instrucțiuni + dovezi, pe același model și aceeași configurație; raportează
rezultate ca numărări (câte erori susținute prinse, câte fals-pozitive, câte
escaladări corecte), nu ca scor unic. Concluziile despre grounding se trag doar
pe minimum 20 de cazuri cu surse atașate, cu etichete validate uman **înainte**
de rulări și fără leakage din holdout. Proba anterioară cu Hunspell și cu
LanguageTool, pe 20 de cazuri, nu certifică performanță generală — e doar pilot,
nu garanție. LanguageTool nu se adaugă ca dependență acum.
