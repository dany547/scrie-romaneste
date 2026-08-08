# Anti-tipare AI — ce evită un text românesc natural

Listă de verificare pentru a detecta și elimina tiparele specifice textului generat
de modele. Aplic-o în faza de autocorecție, după ce ai un draft complet
(vezi `scris-eficient.md` §1).

Pentru greșeli de limbă specifice românei — acord, prepoziții, flexiune, calc
sintactic — vezi `tipare-ro.md`.

## Cum se citește pragul

Nu orice apariție e o problemă. Fiecare intrare are un prag:

- **mereu** — formula nu se salvează prin context. Se taie sau se înlocuiește.
- **la_aglomerare** — o apariție e normală, trei în același paragraf nu.
- **la_densitate** — se judecă raportat la lungimea textului. Un cuvânt abstract
  într-o pagină e firesc; zece e ceață.

Un singur „de asemenea" într-un articol de 2000 de cuvinte nu strică nimic. Șase
îl fac să sune automat. Diferența asta contează mai mult decât lista în sine.

## A. Structură, tranziții și ritm

- **Fără tranziții mecanice**: elimină conectorii folosiți obsesiv. Cel mai des,
  relația dintre idei e evidentă și conectorul doar lungește fraza — începe
  paragraful direct cu informația nouă.
- **Fără paragrafe simetrice**: evită structura de eseu școlar (frază-temă →
  dezvoltare → frază-rezumat, repetată la fiecare paragraf).
- **Ritm monoton**: alternează fraze scurte cu fraze lungi. Lungimea uniformă e
  semnul cel mai vizibil de text automat — mai vizibil decât orice cuvânt din
  listele de mai jos, pentru că nu se repară prin sinonime.
- **Fără „capcana concluziei"**: nu încheia cu o secțiune „Concluzie"/„Rezumat"
  care repetă ce s-a spus. Termină cu o idee de final sau o deschidere.
- **Fără structură excesivă**: titluri și subtitluri pentru un subiect simplu,
  liste de 3/5/7 puncte fără necesitate reală. Păstrează doar ierarhia cerută de
  canal și de cititor.

| Nu folosi | Folosește | Prag |
|---|---|---|
| În concluzie | taie tot paragraful, sau termină cu ideea nouă | mereu |
| În esență | taie | mereu |
| Mai mult decât atât | taie, sau „și" | mereu |
| Pe de o parte… pe de altă parte | pune faptele alături, fără schelet | mereu |
| În primul rând… în al doilea rând | numerotare doar dacă ordinea contează | mereu |
| Prin urmare | „deci", sau nimic | la_aglomerare |
| De asemenea | „și", sau nimic | la_aglomerare |
| În plus | taie | la_aglomerare |
| Totodată | taie | la_aglomerare |
| Cu toate acestea | „dar", „totuși" | la_aglomerare |
| Pe scurt | taie | la_aglomerare |
| Nu doar…, ci și… | reformulează direct | la_aglomerare |
| Nu e vorba doar de…, ci de… | spune direct despre ce e vorba | la_aglomerare |
| Nu în ultimul rând | taie — enumerarea se vede | la_aglomerare |
| Atunci când vine vorba de | „la", „în privința", „când" | la_aglomerare |

**Fără simetrie de acoperire**: fraza care se adresează tuturor ca să nu excludă
niciun cititor — „Fie că ești începător sau profesionist…", „indiferent de
buget…", „pentru oricine". O propoziție adevărată pentru toată lumea nu
informează pe nimeni; numește cititorul concret. Atenție, conjuncția corelativă
obișnuită („Fie că plouă, fie că nu, plecăm") nu are nicio legătură cu tiparul —
semnalul cere adresarea la persoana a II-a. Prag: familie (3+ apariții).
Detaliat, cu celelalte reflexe de gen, în `../seo/core.md`, „Registrul «articol
SEO»".

## B. Introduceri, umpluturi și meta-text

Formulele de deschidere ceremonioasă și comentariul despre text sunt cele mai
sigure semne. Cititorul a venit pentru informație, nu pentru anunțul ei.

| Nu folosi | Folosește | Prag |
|---|---|---|
| În lumea de astăzi / modernă / digitală | intră direct în subiect | mereu |
| În era digitală | idem | mereu |
| În societatea modernă | idem | mereu |
| Într-o lume în continuă schimbare | idem | mereu |
| În contextul actual | spune care e contextul, concret | mereu |
| De când lumea și pământul | taie | mereu |
| Este important de menționat că | spune lucrul direct | mereu |
| Merită subliniat / precizat faptul că | idem | mereu |
| Trebuie menționat că | idem | mereu |
| Este demn de remarcat | idem | mereu |
| În acest articol… | taie; articolul se vede singur | mereu |
| În cele ce urmează | taie | mereu |

## C. Vocabular corporatist și dramatic

| Nu folosi | Folosește | Prag |
|---|---|---|
| revoluționar | ce face concret, altfel decât înainte | mereu |
| vibrant | descrie ce se vede | mereu |
| schimbare de paradigmă | ce s-a schimbat, în cuvinte simple | mereu |
| un pilon fundamental | „stă pe", „ține de" | mereu |
| o componentă esențială | „are nevoie de" | mereu |
| abordare holistică | ce cuprinde, enumerat | mereu |
| adoptă o abordare / filozofie | „face", „lucrează așa" | mereu |
| soluție inovatoare / de ultimă generație | ce face, comparativ cu ce era | mereu |
| se recomandă adoptarea unei abordări | cine ce trebuie să facă | mereu |
| impresionant | cifra sau faptul | la_aglomerare |
| remarcabil | idem | la_aglomerare |
| se remarcă prin | „are", „face" | la_aglomerare |

**Fără înșiruiri de adjective**: nu aglomera 3+ adjective înainte de un substantiv.

**Fără evitarea copulei**: folosește „este". Nu forța „reprezintă" / „constituie"
doar ca să sune academic. *Centrala reprezintă o soluție* → *Centrala e o soluție*.

## D. Abstracțiuni și verbe generice

Substantivul abstract ascunde cine face ce. Înlocuiește-l cu verbul din care
provine și numește actorul.

| Nu folosi | Folosește | Prag |
|---|---|---|
| optimizare | „am făcut X mai rapid cu Y%" | la_densitate |
| eficientizare | ce s-a tăiat, concret | la_densitate |
| implementare | „am pus în funcțiune", „am scris" | la_densitate |
| valorificare | „am folosit", „am vândut" | la_densitate |
| aliniere | „am pus de acord" | la_densitate |
| a facilita | „ajută la", „permite" | la_densitate |
| a contribui la | „ajută", sau cifra contribuției | la_densitate |
| a avea un impact semnificativ asupra | ce s-a schimbat și cu cât | la_aglomerare |

## E. Cuantificări vagi

Formula vagă e mai lungă decât cifra pe care o înlocuiește.

| Nu folosi | Folosește | Prag |
|---|---|---|
| o multitudine de | cifra | mereu |
| un număr semnificativ / considerabil | cifra | mereu |
| o gamă / paletă largă de | enumeră, sau dă cifra | mereu |
| un spectru larg de | idem | mereu |
| o serie de | cifra, sau taie | la_aglomerare |

## F. Hedging

Rezerva se păstrează unde incertitudinea e reală. Pusă la fiecare afirmație,
devine tic.

| Nu folosi | Folosește | Prag |
|---|---|---|
| Este posibil ca X să… | „X se întâmplă când…", sau asumă | la_aglomerare |
| S-ar putea ca | idem | la_aglomerare |
| Poate fi considerat | „este" | la_aglomerare |
| În general | taie, sau spune excepția | la_densitate |
| De regulă | idem | la_densitate |

## G. Romgleză

| Nu folosi | Folosește |
|---|---|
| Face sens | Are sens |
| Joacă un rol crucial | Are un rol esențial / E determinant |
| La sfârșitul zilei | În cele din urmă / Până la urmă |
| În termeni de | În ceea ce privește / Din punct de vedere al |
| Insight-uri acționabile | Concluzii utile / Ce se poate face |
| Seamless | Fără întreruperi / Fără cusur |
| A performa | A funcționa / A se descurca |

Lista completă de calcuri, prieteni falși și regim prepozițional greșit e în
`tipare-ro.md`.

**Fără abuz de diateză pasivă**: preferă vocea activă („Echipa a realizat
proiectul", nu „Proiectul a fost realizat de către echipă"). Detaliu tehnic în
`gramatica-stil.md` §4.

## H. Ton și stil

- **Fără explicații excesive**: nu explica redundant concepte simple. Cititorul
  înțelege aluziile. Vezi și regula celor 10% din `scris-eficient.md` §6.
- **Fără neutralitate sterilă**: dacă textul permite, injectează opinii, nuanțe,
  un ton conversațional. Evită tonul diplomatic lipsit de personalitate.
- **Fără echilibru forțat**: nu compensa fiecare afirmație cu o rezervă. Detalii
  în `tipare-ro.md`, secțiunea `echilibru_fortat`.

## I. Simboluri și formatare excesivă

Ca și restul listei, pragul contează mai mult decât interdicția absolută. Emoji e
legitim în profil `colocvial`/`cald`; o listă ocazională cu „-" e normală; o singură
paranteză cu liniuță nu strică nimic. Semnalul apare doar la aglomerare sau densitate
mare.

- **Emoji decorative**: emoji folosite ca marcatori de listă sau presărate în proză fără
  rol semantic („🚀 Lansăm produsul!", „✅ Beneficiu 1"). 1-2 emoji într-un text lung sau
  colocvial e ton, nu tipar; 5+ la 500 de cuvinte e semnal. Prag: `la_densitate`.
- **Liste cu „-" abuzate**: transformarea prozei în liste marcate cu „-" fără necesitate
  reală — vezi și regula „Fără structură excesivă" din secțiunea A. O listă de
  funcționalități sau un FAQ nu e abuz; semnalul e proporția majoritară de linii-listă
  față de proză. Prag: proporție dedicată, nu densitate/1000 cuvinte.
- **Liniuța ca paranteză improvizată**: „text - precizare - continuare" sau „text —
  precizare — continuare" repetat ca tic sintactic în loc de virgulă, paranteză sau frază
  nouă. Prag: `la_aglomerare`.
- **Bold/italic excesiv**: `**text**` / `*text*` pentru accentuare deasă — tipic markdown
  de chat, nepotrivit pentru text publicat. Prag: `la_densitate`.

## Verificare rapidă înainte de livrare

1. Caută tranzițiile din tabelul A. Numără-le. Peste trei într-un text scurt,
   taie jumătate.
2. Verifică prima propoziție a fiecărui paragraf — dacă toate au aceeași
   structură și lungime, rescrie jumătate.
3. Verifică ultimul paragraf — dacă rezumă mecanic, taie-l sau transformă-l în
   idee nouă.
4. Caută calcurile din tabelul G și din `tipare-ro.md`.
5. Caută reziduuri de conversație și placeholdere necompletate
   (`tipare-ro.md`, `artefact_chatbot` și `amprenta_unealta`).
6. Verifică emoji, liste cu „-" și bold/italic față de proporția de text din jur
   (secțiunea I) — un abuz izolat trece neobservat la citire, dar sare în ochi agregat.

Pentru verificarea mecanică: `scripts/check-tipare.py` acoperă tabelele de mai
sus, iar `scripts/check-ritm.py` măsoară punctul 2.
