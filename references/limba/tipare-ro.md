# Tipare de eșec specifice românei

Greșelile pe care le face un model când scrie românește nu sunt aceleași cu cele
din engleză. Fluența nu garantează corectitudinea: un text poate curge perfect și
să aibă acordul rupt, prepoziția calchiată sau pluralul inventat.

Fișierul acoperă ce nu se vede dintr-o listă de clișee traduse. Pentru clișee și
vocabular, vezi `anti-tipare-ai.md`. Pentru normă generală, `gramatica-stil.md`.

---

## calc_sintactic

Traducere literală care sună inteligibil, dar nu e română.

| Nu folosi | Folosește | Vine din |
|---|---|---|
| a adresa o problemă | a aborda / a rezolva o problemă | address |
| a aplica la facultate; a-mi depune aplicația | a candida pentru; a depune dosarul | apply for |
| a se focusa pe | a se concentra asupra | focus on |
| a ridica bani | a atrage fonduri | raise money |
| al doilea cel mai mare oraș | al doilea oraș ca mărime | second biggest |
| O eroare s-a produs | S-a produs o eroare | An error occurred |
| a downloada | a descărca | download |
| a eșuat patetic | a eșuat lamentabil | pathetic |
| în ordine să | pentru a / ca să | in order to |
| bazat pe faptul că | pentru că / întrucât | based on the fact |

**Prieteni falși** — cuvântul există în română, dar cu alt sens:

| Cuvânt | Sensul greșit (din engleză) | Ce trebuie folosit |
|---|---|---|
| locație | loc, amplasare | loc, amplasare (locație = închiriere) |
| actual, actualmente | propriu-zis, efectiv | propriu-zis, real |
| eventual | în cele din urmă | în cele din urmă |
| atașament | fișier atașat | anexă, fișier atașat |
| sensibil | rezonabil, practic | rezonabil |
| librărie | bibliotecă | bibliotecă |
| nuvelă | roman | roman |
| bilion | miliard | miliard |
| colegiu | facultate | facultate |
| fizician | medic | medic |
| a rezuma | a relua o activitate | a relua |

**„de către" pus mecanic.** Agentul neînsuflețit cere „de", nu „de către":
*înregistrate de către documente* → **înregistrate de documente**. Iar la diateza
activă nu-i nevoie deloc: *Raportul a fost procesat de către sistem* → **Sistemul
a procesat raportul**.

**Termeni tehnici traduși când nu trebuie.** *word embeddings* → „încorporările
Word" e greșit; e **reprezentări vectoriale ale cuvintelor**. Codul, identificatorii
și numele proprii nu se traduc niciodată: *Telegram* nu devine „Telegrama",
`for i in range(...)` nu devine „pentru i în interval".

---

## regim_prepozitional

Prepoziția schimbă sensul verbului, iar traducerea o alege pe cea probabilă
semantic, nu pe cea corectă.

| Greșit | Corect |
|---|---|
| Rămâneți pe telefon | Rămâneți **la** telefon |
| S-a discutat asupra referatului | discuții **despre / cu privire la** referat |
| are o părere asupra colegului | o părere **despre** coleg |
| nivel de București | **nivelul Bucureștiului** |
| ca și consilier | **drept** consilier / **ca** consilier |
| 122 dolari pe baril | 122 **de** dolari pe baril |
| cu textele care le aveți | cu textele **pe care** le aveți |
| ei avertizează pe turiști | ei **îi** avertizează pe turiști |

„în Cluj" e județul, „la Cluj" e orașul. Aceeași distincție la toate reședințele.

Verbe unde prepoziția decide sensul, deci nu se schimbă la întâmplare: *a se abate
pe la* (a se opri) vs *a se abate asupra* (a lovi); *a suspecta de* (o faptă) vs
*a suspecta pentru* (o acuzație); *a activa în* (instituție) vs *a activa ca*
(funcție).

---

## acord_la_distanta

Acordul cedează când nucleul sintagmei e departe de determinant. Sunt locurile
unde un text fluent are cele mai mari șanse să fie greșit.

| Greșit | Corect | Ce s-a rupt |
|---|---|---|
| alegerea candidatelor cele mai potrivite | candidatelor **celor** mai potrivite | superlativul nu s-a acordat în caz |
| titlul unei lucrări scrisă recent | unei lucrări **scrise** recent | participiul s-a acordat cu titlul, nu cu lucrarea |
| acei milioane de lei | **acele** milioane de lei | acord cu referentul, nu cu „milioane" |
| un batic a mamei | un batic **al** mamei | posesivul nu s-a acordat cu obiectul posedat |
| cei doi frați a prietenei | cei doi frați **ai** prietenei | idem, la plural |
| vecinii a căror fete | vecinii **ai căror** fete | idem, la relativ |
| Mi s-a făcut vrăji | Mi **s-au** făcut vrăji | subiect postpus, la plural |
| reporterii Realitatea | reporterii **Realității** | genitivul numelui propriu |

Cu substantive colective sunt corecte ambele: *Majoritatea a votat* / *Majoritatea
au votat*.

**Persoana comută la mijlocul frazei.** Cea mai vizibilă eroare de traducere
automată: *„Mănâncă o dietă echilibrată și asigurați-vă că include..."* — sare din
tu în dumneavoastră într-o singură propoziție. Alege o formă de adresare și ține-o
pe tot textul.

---

## acord_plural_neutru

Substantivele neutre iau la plural forme de gen feminin: adjectivele și
ordinalele se acordă ca la femininul plural, nu ca la masculinul plural.
Capcana cea mai frecventă în vocabularul tehnic:

| Greșit | Corect | Regula |
|---|---|---|
| virusuri funcționali | virusuri **funcționale** | pluralul neutru cere feminin plural |
| modele performanți | modele **performante** | idem |
| niveluri înalți | niveluri **înalte** | idem |
| dispozitive inteligenti | dispozitive **inteligente** | idem |
| servicii rapizi | servicii **rapide** | idem |

Pluralul substantivului însuși, la neologisme:

| Singular | Plural |
|---|---|
| virus | virusuri |
| model | modele |
| nivel | niveluri (nu „nivele") |
| dispozitiv | dispozitive |
| serviciu | servicii |

La împrumuturile recente, cratima la plural (device-uri, update-uri) e o
politică de consecvență, nu o eroare — vezi `articol_imprumuturi`.

**Numeral + substantiv:** „doi" e masculin; „două" e feminin și neutru.

| Greșit | Corect |
|---|---|
| doi aplicații | **două** aplicații |
| două editori | **doi** editori |
| doi modele | **două** modele |

**Ordinale:** „primii/ultimii" masculine; „primele/ultimele" feminine și neutre.

| Greșit | Corect |
|---|---|
| primii versiuni | **primele** versiuni |
| primele utilizatori | **primii** utilizatori |
| ultimii actualizări | **ultimele** actualizări |

Acordurile astea pică des în titluri și excerpte — text scurt, care nu trece
prin recitirea corpului. Verifică-le explicit acolo.

---

## morfologie_flexiune

Formele rare și neologismele se construiesc prin analogie greșită.

**Verbe:**

| Greșit | Corect |
|---|---|
| vroiam, vroia | **voiam, voia** |
| el precede, ei preced | el **precedă** |
| el succede | el **succedă** |
| vor apare | vor **apărea** |
| A panicat | **S-a** panicat |
| merită apreciată | merită **să fie** apreciată |
| ne complacem (cu sensul „ne place") | ne **place** |
| Nu fă și tu aceeași greșeală | Nu **face** și tu |
| Voi bănui că așa e | **Bănuiesc** că așa e |
| Președinții se urmează la 4 ani | se **succedă** la 4 ani |

**Plural și articulare:**

| Greșit | Corect |
|---|---|
| ridichii | **ridichi** |
| membrii (nearticulat) | **membri** |
| victimile | **victimele** |
| croasanți | **croasante** |
| ecleruri | **eclere** |
| aragazuri | **aragaze** |
| monezi | **monede** |
| sindromuri | **sindroame** |
| pârâuri | **pâraie** |
| succesuri | **succese** |
| doi hamburger | doi **hamburgeri** |
| almanahe | **almanahuri** |

Forme feminine acceptate azi: **filoloagă**, **dramaturgă**, **demagoagă**.

**Alte tipare:** *Consumați minim 2 litri* → **minimum** 2 litri. *Am mâncat decât
migdale* → **doar** migdale. *Am vrut ca să fim obiectivi* → **să** fim. *Le-am
spus la copii* → **copiilor**. *Tu însuși ai spus* (fem.) → **tu însăți**.
*Muntele e înalt ca Vf. Omu* → **mai înalt decât**.

---

## articol_imprumuturi

Regula e fonetică, nu grafică: cratima apare doar când finalul cuvântului se
citește altfel decât se scrie.

**Fără cratimă** — finalul se citește ca în română:
blogul, spamul, linkul, stickul, clickuri, trendul, serverul, logoul, widgetul,
gadgetul, driverul, pluginul, reviewul, boardul, bodyul, boyul, rockuri, drinkuri.

**Cu cratimă** — finalul se citește diferit sau e mut:
site-uri [sait], show-ul, bungalow-ul, chardonnay-ul, acquis-ul, bleu-ul,
Bruxelles-ul, dandy-ul, flash-uri. La fel siglele și literele: CD-uri, VIP-uri,
RATB-ul, ph-ul, x-ul.

Greșeala tipică a modelelor nu e alegerea în sine, ci **inconsecvența**: aceeași
formă scrisă în două feluri în același text. Stabilește politica o dată și
ține-o.

---

## diacritice

**Folosește virgulă, nu sedilă.** `ș` și `ț` sunt corecte; `ş` și `ţ` sunt
caractere turcești, moștenite din fonturi vechi. Arată identic la prima vedere și
strică orice căutare, sortare sau potrivire de text.

**â/î în interiorul cuvântului** e cea mai frecventă greșeală de restaurare —
supracorectarea spre î: *român* → *romîn*. Regula: î la început și la sfârșit de
cuvânt, â în interior. Excepție: compusele cu prefix păstrează î-ul cuvântului de
bază — **neîndoielnic**, **reîncepe**.

**Nu pune diacritice unde nu trebuie:** în cod, în identificatori, în adrese web,
în nume proprii străine, în acronime.

**Cuvinte care își schimbă sensul fără diacritice** — verifică-le explicit când
textul vine dintr-o sursă fără diacritice: tara/țara/tară/țară · fata/față/fată ·
peste/pește · paturi/pături · fisa/fișa · sfant/sfânt/sfanț · manie/mânie ·
rama/râmă/ramă · rau/râu/rău · var/vâr/văr · soc/șoc · tine/ține · tipa/țipă/tipă ·
roman/român/romană · tanc/tânc · mama/mamă · masa/masă. „Tata" se poate citi în
șase feluri.

---

## clitice_pronume

**Dublarea clitică e obligatorie** cu complement direct determinat introdus prin
„pe": *ei avertizează pe turiști* → *ei **îi** avertizează pe turiști*. Cade prima
când topica e copiată din engleză.

**„pe care", nu „care"**, la complement direct: *textele care le aveți* → *textele
**pe care** le aveți*. Dispare cu atât mai des cu cât relativa e mai lungă.

**Pronume fără antecedent clar.** În fraze cu doi-trei candidați, „el", „aceasta",
„lor" devin ambigue. Înlocuiește cu substantivul, chiar dacă se repetă — repetiția
clară bate eleganța confuză.

---

## tipografie_anglicizata

- Ghilimele: **„așa"**, nu "așa". Citat în citat: **„…«…»…"**.
- Zecimale cu virgulă: **12,5%**, nu 12.5%. Mii cu punct sau spațiu: 1.200 lei.
- Fără majuscule la fiecare cuvânt din titlu — asta e regulă englezească. În
  română, majusculă doar la primul cuvânt și la nume proprii.
- Linia de pauză nu se pune la fiecare inflexiune. Două perechi în același
  paragraf înseamnă că frazele trebuie sparte.
- Virgula nu se pune automat după fiecare conector, și niciodată între subiect și
  predicat, oricât de lung ar fi subiectul.

---

## registru_inconsecvent

- **Alege tu sau dumneavoastră** și nu comuta. Amestecul în aceeași frază e
  semnătura traducerii automate.
- **Entuziasm promoțional în context nepotrivit.** Un anunț administrativ sau o
  descriere tehnică nu se scriu cu adjective de reclamă.
- **ro-RO sau ro-MD** — stabilește varianta de la început. Termenii administrativi,
  monedele și instituțiile diferă.
- **Formule de email traduse literal.** „Sper că acest email te găsește bine" nu e
  o formulă românească.

---

## sursa_fabricata

Modelul inventează exact lucrurile care sună cel mai credibil: procente precise,
studii, citate, funcții, instituții.

Semnale: procente cu zecimale fără sursă; referințe bibliografice pe care nu le
găsești; citate atribuite unei persoane fără context; norme juridice sau medicale
prezentate ca reguli universale; numere care par măsurate dar nu au de unde.

Regula practică: **cifră, citat sau normă fără sursă verificabilă nu se publică.**
Dacă exemplul e ipotetic, spune că e ipotetic. Nu inventa precizie ca să pară
textul documentat — un „aproximativ o treime" onest bate un „34,7%" fals.

---

## repetitie_mascata

Aceeași idee, reformulată cu sinonime, ca să pară că textul avansează.

Perechi decorative de tăiat: *clar și ușor de înțeles*, *eficient și productiv*,
*rapid și într-un timp scurt*, *simplu și facil*, *util și benefic*.

Pleonasme frecvente: *a reveni din nou*, *a colabora împreună*, *consens comun*,
*progres înainte*, *mijloace mass-media*, *aniversarea a 10 ani*.

Testul: dacă a doua formulare nu adaugă un fapt, un exemplu sau o consecință,
taie-o. La fel cu introducerea și concluzia care spun același lucru ca și corpul.

---

## echilibru_fortat

Textul care compensează fiecare afirmație cu o rezervă ajunge corect și inutil.

Semnale: avantaje și dezavantaje prezentate simetric chiar când o parte domină
clar; „poate", „în general", „de regulă", „depinde de context" la fiecare
paragraf; finaluri de tipul „alegerea optimă depinde de nevoile fiecăruia".

Remediu: spune după ce criteriu se alege. Dacă dovezile permit o concluzie,
asum-o. Păstrează rezerva doar unde incertitudinea e reală, nu ca politețe.

---

## artefact_chatbot

Reziduuri de conversație în text livrat: „Sigur!", „Desigur!", „Excelentă
întrebare!", „Sper că te ajută!", „Anunță-mă dacă mai ai nevoie", „Hai să analizăm
pas cu pas", „Iată textul rescris". Se taie integral — nu fac parte din text.

## amprenta_unealta

Urme mecanice care trădează generarea, independent de limbă: placeholdere
necompletate (`[Numele tău]`, `[X]`, `2026-XX-XX`), markup de citare
(`oai_citation`, `citeturn0search0`), parametri de urmărire în linkuri
(`utm_source=chatgpt.com`). Verifică-le la final, mereu.
