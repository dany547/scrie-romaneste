# Pasul organic prin articol

Un articol scris de om nu arată ca o schemă. Nu începe cu o definiție, nu are
cinci H2-uri de lungime egală cu câte trei bullets, nu se închide cu un
rezumat. Fișierul ăsta e despre ritmul ăsta — pentru orice text citit
cap-coadă, nu doar pentru blog.

## 1. Deschiderea

Prima propoziție e scurtă și concretă, fără dregere de glas.

Se taie: definiția obligatorie, contextul de încălzire, „în acest articol vom
vedea", „X este un proces prin care". Reflexele astea sunt deja numite în
`core.md`, registrul „articol SEO".

Funcționează: o scenă, o cifră care contrazice așteptarea, o întrebare pe care
cititorul și-a pus-o deja, un verdict direct.

Promisiunea titlului se atinge în primele două-trei propoziții. E aceeași
regulă ca răspunsul în primele ~200 de cuvinte din `geo.md`, văzută dinspre
cititor: a venit pentru ce-a citit în titlu, nu ca să fie pregătit pentru
subiect. Contractul titlu–corp e în `titluri.md`.

## 2. Ritmul secțiunilor

Un articol scris de om nu are secțiuni egale. Alternează explicație lungă /
exemplu scurt / listă doar unde itemii chiar sunt paraleli / paragraf de o
propoziție pentru accent.

Semnalul de mecanic: poți prezice structura secțiunii următoare din cea
curentă. Dacă fiecare H2 deschide cu o definiție, continuă cu trei bullets și
închide cu o frază de trece-mai-departe, e șablon — indiferent cât de curate
sunt propozițiile.

Detectat automat, grosier: `check-ritm.py`, `structura_excesiva`. Scriptul
vede densitatea de heading-uri, nu replica dintre secțiuni. Replica se
recitește.

## 3. Paragrafe

Maximum ~4 rânduri, dar nu toate de 4. Un paragraf de o propoziție după o
explicație lungă e accent, nu sărăcie. Cinci paragrafe identice ca lungime
sunt metronom.

## 4. Dovada

Orice afirmație contestabilă stă lângă o cifră, un exemplu, un caz, un citat
atribuit sau o sursă pe nume. Fără ele, afirmația e opinie — și atunci se
declară ca opinie.

Interdicția rămâne: nu inventa. Cifra, cazul, citatul și sursa vin din
CONTEXT, nu din obișnuința de a suna precis (`grounding.md`,
`tipare-ro.md`).

## 5. Perspectiva proprie

Partea pe care modelul n-o poate produce singur, de aceea trebuie **cerută**
la pasul CONTEXT: un caz real, o cifră proprie, o opinie asumată, o greșeală
recunoscută.

Un articol fără nicio propoziție care putea fi scrisă doar de autorul lui e
commodity content. Se găsește în zece tab-uri deschise pe aceeași interogare.

Dacă utilizatorul n-a dat perspectiva, nu o fabrica. Pune `[DE COMPLETAT: caz
propriu / cifră proprie / ce-ați învățat voi din treaba asta]` și cere-o
grupat, o dată. Textul rămâne mai sărac până vine.

## 6. Legături interne

Două-trei pagini proprii relevante, cu anchor descriptiv — ce se găsește la
destinație, nu „click aici" și nu „articol" (`core.md`).

Doar pagini care există. Nu inventa URL-uri, nu inventa titluri de articole
„pe care le vom publica", nu trimite la o categorie goală. Dacă nu cunoști
arhitectura site-ului, întreabă sau lasă `[DE COMPLETAT: link intern]`.

## 7. Finalul

Nu rezumat. Capcana concluziei e deja interzisă; „în concluzie" e detector, nu
excepție. Un raport sau o lucrare academică au voie să aibă concluzie — acolo
genul o cere (`scris-eficient.md` §7).

Merge: ultimul pas concret, ce se schimbă pentru cititor, un singur CTA
specific. „Compară cele trei modele din tabel", nu „Contactează-ne pentru mai
multe informații". Încheierea de politețe e reflex de breaslă, deja tăiat în
`core.md`.

Ultima frază e a doua cea mai citită după titlu. Nu o irosi pe o formulă.

## 8. Testul „cui i-a fost util"

Întrebări, nu prag. Un „nu" la ultimele trei nu se repară din editare — cere
alt contract, alt unghi sau alt subiect.

- Cine a scris, și e evident cititorului?
- Dacă e generat, se declară?
- Pagina există ca să ajute pe cineva concret sau ca să prindă o interogare?
- Cititorul trebuie să caute din nou după ce a citit?
- Ai da linkul unui prieten cu exact problema asta?
- Ai scrie despre subiect dacă n-ar avea volum de căutare?
- Ai scris până la un număr de cuvinte?

## 9. Pe alte genuri, pe scurt

**Pagină de produs.** Promisiunea stă în primul ecran: ce e, pentru cine, cu
ce iese cumpărătorul. Specificațiile vin după, nu înainte. Fără povestea
originii firmei în hero.

**Pagină locală.** Serviciul + locul, NAP-ul, ce se întâmplă dacă suni. Nu e
articol: n-are nevoie de deschidere de încălzire și n-are nevoie de cinci H2.
Detaliile sunt în `local.md`.

**Comunicat.** Știrea în prima frază. Cine, ce, când, unde. Contextul după.
Fără „suntem încântați să anunțăm", fără rezumat la final — comunicatul se
taie de jos, nu se încheie.
