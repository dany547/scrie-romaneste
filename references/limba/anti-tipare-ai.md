# Anti-tipare AI — ce evită un text românesc natural

Listă de verificare pentru a detecta și elimina tiparele toxice specifice textului generat
de modele lingvistice. Aplic-o în faza de autocorecție, după ce ai un draft complet
(vezi `scris-eficient.md` §1).

## A. Structură, tranziții și ritm

- **Fără tranziții mecanice**: elimină conectorii rigizi folosiți obsesiv — *„În concluzie",
  „Prin urmare", „De asemenea", „Pe de o parte... pe de altă parte", „În plus", „Mai mult
  decât atât", „Totodată"*.
- **Fără paragrafe simetrice**: evită structura de eseu școlar (frază-temă → dezvoltare →
  frază-rezumat repetată la fiecare paragraf). Variază lungimea paragrafelor.
- **Ritm monoton (burstiness)**: alternează fraze scurte, impactante, cu fraze lungi,
  complexe. O lungime medie uniformă a propozițiilor e semnul cel mai vizibil de text automat.
- **Fără „capcana concluziei"**: nu încheia cu o secțiune explicită „Concluzie"/„Rezumat"
  care doar repetă ideile spuse deja. Termină cu o idee de final sau o deschidere, nu cu
  o recapitulare forțată.

## B. Vocabular, clișee și meta-introduceri

- **Fără introduceri formulaice**: interzis să începi cu *„În lumea de astăzi", „În era
  digitală", „În societatea modernă", „De când lumea și pământul"*.
- **Fără umpluturi și meta-text**: elimină *„Este important de menționat că", „Merită
  precizat/subliniat faptul că", „În acest articol", „În cele ce urmează"*.
- **Fără adjective dramatice/corporatiste**: interzis *„revoluționar, impresionant,
  remarcabil, vibrant"*. Evită *„adoptă o abordare/filozofie", „se remarcă prin", „schimbare
  de paradigmă", „un pilon fundamental", „o componentă esențială"*.
- **Fără cuantificări vagi**: evită *„o serie de", „un număr semnificativ", „o gamă/paletă/
  spectru larg de"* — dă cifra sau exemplul concret în loc.
- **Fără înșiruiri de adjective**: nu aglomera 3+ adjective înainte de un substantiv.
- **Fără hedging (ezitare)**: elimină *„este posibil ca", „s-ar putea ca"*. Fii asertiv.
- **Fără evitarea copulei**: folosește normal „este". Nu forța „reprezintă"/„constituie"
  doar ca să sune mai academic.

## C. Romgleză și calchieri (traduceri nefirești din engleză)

| Nu folosi | Folosește |
|---|---|
| „Face sens" | „Are sens" |
| „A juca un rol crucial" | „A avea un rol esențial" / „A fi determinant" |
| „La sfârșitul zilei" | „În cele din urmă" / „Până la urmă" |
| „În termeni de..." | „În ceea ce privește" / „Din punct de vedere al" |

- **Fără abuz de diateză pasivă**: preferă vocea activă („Echipa a realizat proiectul",
  nu „Proiectul a fost realizat de către echipă"). Detaliu tehnic în `gramatica-stil.md` §1.

## D. Ton și stil

- **Fără explicații excesive (over-explanation)**: nu explica concepte simple redundant.
  Cititorul înțelege aluziile; nu-l trata ca pe un copil. Vezi și regula celor 10% din
  `scris-eficient.md` §5.
- **Păstrează neutralitatea doar când e cerută**: dacă textul permite, injectează opinii,
  nuanțe culturale, regionalisme subtile sau un ton conversațional. Evită tonul diplomatic,
  steril, lipsit de personalitate.

## Verificare rapidă înainte de livrare

Scanează draftul o dată doar pentru aceste tipare (independent de evaluarea calitativă
generală din `scoring-checklist.md`):

1. Caută în text: „în concluzie", „de asemenea", „totodată", „mai mult decât atât" — elimină
   sau înlocuiește cu conexiune naturală ori cu nimic (asyndeton).
2. Verifică prima propoziție a fiecărui paragraf — dacă toate au aceeași structură
   (subiect-verb-complement, aceeași lungime), rescrie jumătate din ele.
3. Verifică ultimul paragraf — dacă rezumă mecanic tot ce s-a spus, taie-l sau transformă-l
   într-o idee nouă.
4. Caută calcuri de engleză din tabelul de mai sus.
