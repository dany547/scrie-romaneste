# Scris eficient — proces, structură, concizie

Instrucțiuni de proces pentru redactare. Ce ține de clișee și praguri e în
`anti-tipare-ai.md`; ce ține de normă, în `gramatica-stil.md`.

## 1. Draft complet înainte de editare

Generarea și corectura sunt operații diferite și se blochează reciproc dacă le
faci simultan. Scrie textul integral dintr-o trecere, fără să te oprești să
perfecționezi prima frază înainte de a scrie a doua. Corectează abia după.

Un text corectat pe măsură ce se scrie iese sacadat și inconsecvent ca ton — și
tinde spre fraze de aceeași lungime, exact semnalul pe care `check-ritm.py` îl
raportează.

## 2. Cui îi scrii

Stabilește un cititor concret înainte de prima frază: ce știe deja, ce vrea să
facă după ce citește, ce l-ar face să închidă pagina. Scrii pentru o persoană,
nu pentru un public.

Din cititor rezultă lexicul. Termenul de specialitate rămâne dacă cititorul îl
folosește el însuși; altfel îl explici o dată sau îl înlocuiești. Împrumuturile
deja firești într-un domeniu („commit", „deploy", „lead") nu se traduc forțat —
romgleza e problemă când înlocuiește un cuvânt românesc existent și uzual, nu
când numește ceva ce n-are nume românesc.

## 3. Întrebările care găsesc golurile

Înainte de a scrie, formulează întrebările la care textul trebuie să răspundă.
Ce n-ai putut răspunde cu date confirmate e un gol de informație: îl documentezi,
îl întrebi sau îl marchezi `[DE COMPLETAT: …]`. Nu îl umpli cu formulări generale.

Un text cu zece răspunsuri concrete e mai bun decât unul cu douăzeci de
paragrafe de context. Dacă nu ai ce spune într-o secțiune, taie secțiunea.

## 4. Titlul și structura

Titlul decide dacă textul e citit și trebuie să fie concret: „Ghid complet"
nu spune nimic, „Cum eviți cele cinci greșeli la montajul centralei" spune.

Introducerea e o promisiune: intră direct în subiect și spune ce capătă
cititorul. Corpul dezvoltă ideile care merită dezvoltate — numărul lor vine din
subiect, nu dintr-un tipar de cinci-șase secțiuni.

## 5. Formatare — instrument, nu decor

Listele, subtitlurile, bold-ul și italicul sunt unelte de scanare. Au rol când
conținutul e enumerabil sau când cititorul caută un anume punct într-un text
lung. Devin semnal de text automat la aglomerare: proză tăiată în fragmente cu
„-", subtitluri peste fiecare două paragrafe, bold pe câte un cuvânt din fiecare
frază.

Testul: dacă transformi lista înapoi în proză și textul nu pierde nimic, lista
n-avea rol. Dacă tai bold-ul și cititorul tot găsește ce caută, bold-ul era
decor. Pragurile mecanice sunt în `anti-tipare-ai.md` §I și în
`check-tipare.py`, categoria `simboluri_excesive`.

Paragrafele scurte ajută, dar nu toate: alternează, altfel obții exact ritmul
uniform pe care încerci să-l eviți.

## 6. Reducere sistematică — regula celor 10%

După draft, taie aproximativ o zecime din cuvinte:

- adjective care nu adaugă informație;
- fraze care explică ce s-a înțeles deja;
- propoziții care repetă o idee spusă mai sus cu alte cuvinte;
- perechi sinonimice („clar și ușor de înțeles", „util și benefic").

Dacă o idee încape într-o propoziție, nu o întinde pe un paragraf.

## 7. Finalul

Nu rezuma automat. Termină cu faptul care contează, cu implicația, cu decizia pe
care o are de luat cititorul sau cu întrebarea reală din spatele subiectului.

Îndemnul la acțiune se pune doar dacă genul îl cere — pagină comercială,
newsletter, email — și într-o singură propoziție utilă, nu într-un paragraf de
încheiere. Un raport sau o lucrare academică au voie să aibă concluzie: acolo
concluzia e cerută de gen, nu e capcană.

## 8. Diateza și persoana

Preferă activul: „Instalatorul echilibrează circuitul", nu „Circuitul este
echilibrat de către instalator". Activul spune cine face ce, deci se poate
verifica.

Pasivul și reflexivul rămân legitime când actorul e necunoscut, irelevant sau
deliberat ascuns („Legea a fost adoptată în 2019", „ușa se deschide automat").
Reflexivul impersonal e normal în text tehnic și juridic. Nu le elimina mecanic
— elimină pasivul birocratic care ascunde responsabilitatea fără motiv.

Persoana I și a II-a apropie textul de cititor și se potrivesc ghidurilor,
blogului și emailului. Persoana a III-a se potrivește textelor oficiale și
științifice. Alege una la începutul textului și nu comuta.
