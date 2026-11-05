# Audit pe texte de modele mici: findings și plan de implementare

Data: 2026-11-05. Autor: Claude (Sonnet 5.5), la cererea utilizatorului.
Status: **PLAN, neimplementat**. Cere critică înainte de cod.

## 1. Context

Trei modele ieftine, rulate în Herdr (workspace CODE, tab-uri Deepseek / Mimo26 / GLM), au primit
aceeași cerere: „texte în română: poezii, proză, povestiri, postări Instagram/Meta, preview de
blog, rețete, reportaj, discuții, bannere. Fără skills, fără MCP.” Modele:

- Deepseek v4.1 flash (opencode-go), două răspunsuri: poezii+proză, apoi 10 formate
- Mimo 2.6
- GLM 5.3 flash (zai), thinking low

Textele brute sunt în `tests/fixtures/modele-slabe/` (4 fișiere). Scopul: să vedem ce prinde skill-ul
`scrie-romaneste` pe text real de model slab și ce lasă să treacă.

## 2. Rezultat: skill-ul dă verde pe toate

Comenzi rulate pe fiecare fișier: `verifica.py <f> --fara-seo --human-voice` și
`check-cuvinte.py <f> --tot`.

| Fișier | verifica.py | human-voice | check-cuvinte | Realitate |
|---|---|---|---|---|
| deepseek-1 | 1 critic (fals-ish, „e despre”) | 0/30 PASS | 7 forme | Delir în ultimele paragrafe |
| deepseek-2 | 21 semnale (placeholdere, `numeral_fara_de`, emoji) | 2/30 | 12 forme | Cuvinte inventate, rețetă incoerentă |
| mimo | 1 critic (placeholder) + minore | PASS | 4 forme (hashtag-uri) | Cel mai bun; reflexe AI subtile |
| glm | 31 semnale, aproape toate minore | 2/30 **PASS** | 18 forme | Fără diacritice, cod scăpat, engleză |

Concluzie: `PASS` din `--human-voice` nu spune nimic despre calitatea reală. Skill-ul avertizează
singur (SKILL.md: „un raport curat nu dovedește că vorbele există”), dar un agent slab sau grăbit
citește `PASS`.

## 3. Findings pe model

### 3.1 Deepseek flash

- **Degenerare spre final.** Fiecare text începe bine și se strică. Exemple: „Seara, mâna era să
  se întovărășească de o șurubă”, „l-am învățat pe copilul rasei”, „gura gurii strânse”, „le
  scufund într-un zahar”, „două disciplinat minute”. Rețeta de roșii e delir aproape integral.
  Gramatical corecte, deci invizibile pentru scripturi.
- **Cuvinte inventate / folosite greșit:** „călcaseu”, „administratrație”, „încineșat”, „ascuițit”,
  „sportit”, „macază”, „Șotroană”, „Trei zeci și șapte”, „buzele-n dinti”.
  `check-cuvinte` le prinde, dar e separat de `PASS`.
- **Tipare literare absente din skill:**
  - aforismul de final, repetat: „Se întoarce tot, la altcineva” de 4 ori în același set;
  - „Nu X, ci Y”: „Nu banda, taie”, „Nu despre îndesat”;
  - comparația „ca un X care…” la capătul fiecărei strofe;
  - tricolon și listă „Ce am învățat, în ordine:” cu 3 puncte;
  - fraze-sentință: „Atât.”, „ceea ce nu mă așteptam”;
  - inventar standard de nostalgie (tata, bunica, mușcate, cartier, blocuri).
- **Același fapt reciclat în 7 formate** (patru vecini, aparatul de abur, citatul bibliotecarei).
  Incoerențe între formate: „0 lei” vs. cost, „buletin” vs. „carnet”.
- **Citate și persoane inventate** prezentate ca reale (bibliotecara Rodica etc.).
- Formatare: en-dash `–` în liste, emoji decorative, hashtag-uri lipite (`#viațălentă`).

### 3.2 Mimo 2.6 (cel mai bun)

- **Greșeli de scriere izolate:** „Opr-te”, „Salută-ma”, „RETETĂ”, „un peste râul” (cuvânt
  lipsă), „Nu niciodată”. Hashtag-uri fără diacritice (`#dimineata`, `#liniste`).
- **Reflexe de copywriter AI nedetectate:**
  - „Nu e vina ta… Creierul tău nu e defect”;
  - „Omul nu bea cafea. Omul ținea o gardă.”;
  - ultima frază aforistică din fiecare povestire („…iar asta a fost de ajuns”);
  - „testate pe mine timp de o lună” = experiență personală inventată
    (`FABRICATED_EXPERIENCE=NO` în validator, deci miss);
  - „Salută-mă în comentarii cu ce bei azi” = engagement bait;
  - „Prietenii tăi deja vin. Tu?”, „garantat se întoarce zâmbind”.
- **Logică ruptă în reportaj:** scara care duce în apă și „traversăm ca înainte”.
- Știre cu localitate și persoană inventate („Valea Seacă”, „Elena M.”).

### 3.3 GLM 5.3 flash (cel mai slab)

- **Diacritice lipsă aproape peste tot:** „tarziu”, „ramas”, „ciorba”, „mamaliga”, „dimineata”,
  „saptamani”. Modelul a afirmat în deschidere că textele sunt „fără diacritice lipsă”.
  Skill-ul verifică doar sedila (`check-seo.py::verifica_sedila`), nu absența diacriticelor.
- **Resturi de cod:** „mâncare de.BigDecimal facturi”.
- **Engleză strecurată:** „lecture”, „internalise”, „thing”, „serious”, „Copy”.
- **Forme inventate:** „cumere”, „seguimente” (probabil „suplimente”), „automatărează”,
  „dimineataleta”, „boarfega”.
- **Fraze fără sens:** „stiloul său cersetor”, „cu o delegație de ceață”, „să se interneze —
  ca era internat”.
- Dialog cu imitație forțată de oralitate („numa'”).
- Liniuța-cârjă: 12 apariții (singurul semnal pe care skill-ul îl prinde bine).

### 3.4 Comune celor trei

- Introducere/încheiere de chat: „Iată setul…”, „Perfect!”, „Notă scurtă:”, „Dacă vrei, pot
  extinde…”, „Spune-mi… și fluieră”.
- Știri cu nume/sate/cifre inventate prezentate ca reale (deepseek le marchează cu `[...]`, ceilalți nu).
- Emoji și hashtag-uri decorative.

## 4. Plan de implementare

Ordine = efort crescător, valoare descrescătoare pentru primele trei. Toate cu fixture-uri din
`tests/fixtures/modele-slabe/` copiate în `tests/fixtures/` și teste în `tests/test_scripts.py`.

### P1. Detector de diacritice lipsă (mecanic, cea mai mare valoare)

- Nou în `scripts/check-tipare.py` (sau modul separat `check-diacritice.py` apelat din
  `verifica.py`), categoria `diacritice_lipsa`.
- Algoritm: pentru fiecare cuvânt fără diacritice care **nu** e în lexicon dar al cărui
  echivalent cu diacritice (prin tabel de restaurare ă/â/î/ș/ț) **e** în lexicon → candidat.
  Cuvintele care sunt valide și fără diacritice („sa”, „si”, „ca”, „in”, „la”, „fara”?) se
  tratează separat: nu se numără izolat; contează doar ca indiciu de context (vezi mai jos).
- Prag: ≥ 5 candidați unici la 1000 de cuvinte sau ≥ 15% din cuvintele cu diacritice posibile
  → `critic` „text fără diacritice” (un singur semnal agregat, nu 100 de linii). Sub prag →
  `important` per cuvânt, max 10 afișate.
- Excepții: URL-uri, hashtag-uri (semnal separat, minor), cod, citate în altă limbă, numele
  proprii absente din lexicon.
- Fixture: `glm.txt` (trebuie să iasă `critic`), `mimo.txt` (hashtag-uri → minor), `deepseek-*`
  (nu trebuie să iasă critic).

### P2. `PASS` condiționat de lexic și de diacritice

- `verifica.py --human-voice`: dacă `check-cuvinte` are > N forme (N = 3 sau > 3 la 1000 de
  cuvinte) sau P1 e `critic`, `STATUS` nu mai poate fi `PASS`; devine `UNVERIFIED_LEXICON`
  (sau `REWRITE` pentru P1 critic). Raportul afișează explicit „lexic: K forme neverificate”.
- Motiv: să nu mai existe `PASS` pe text cu cuvinte inventate.

### P3. Cuvinte străine și resturi de cod

- Lista scurtă de engleză frecventă în text românesc („lecture”, „thing”, „serious”,
  „internalise”) nu scalează. Alternativă: în `check-cuvinte`, o formă absentă din lexicon
  RO care **e** în ortografia englezească (listă mică de sufixe -ise/-tion/-ing + wordlist
  minimală) primește eticheta `posibil_englez`.
- Resturi de cod: regex pentru `\.[A-Z][a-zA-Z]+\b` lipit de cuvânt românesc, `</?[a-z]+>`,
  `{{…}}`, `\w+\(\)` în proză → `critic` `rest_cod`.

### P4. Secțiune K, „Text literar și narativ”, în `anti-tipare-ai.md`

Conținut (referință pentru agentul care scrie, nu detector):
- aforismul de final și propoziția-sentință;
- „Nu X, ci Y” / „Nu e X. E Y.” repetat;
- comparația „ca un X care…” obligatorie la capăt de strofă;
- tricolon și enumerare în 3;
- inventar de nostalgie și detaliu „prea la locul lui”;
- experiență personală inventată în text persuasiv/blog („testate pe mine”);
- cerere de comentarii/engagement bait;
- reciclarea aceluiași fapt în mai multe formate.
Fiecare cu un exemplu prost (din fixture) și un contra-exemplu. Referință din `SKILL.md`
la pasul LOAD pentru text literar și la modul human-voice.

### P5. Detector de repetiție (în `check-human-voice.py`)

- aceeași secvență de ≥ 5 cuvinte de ≥ 3 ori într-un document (prinde „Se întoarce tot, la
  altcineva”);
- „Nu <fraza>, ci/nu …” de > 2 ori;
- paragraf închis cu propoziție de ≤ 4 cuvinte de > 3 ori;
- mod „set multi-format”: același nume propriu sau aceeași cifră în ≥ 4 secțiuni.
Toate `minor`/semnal de recitire (regula de decizie 4 din SKILL.md): nu corecții automate.

### P6. Încheiere și introducere de chat

- Regex pe prima și ultima propoziție a documentului: `^(Iată|Perfect|Sigur|Desigur|Bineînțeles)\b`,
  `(Dacă vrei|Spune-mi|Pot (extinde|adapta|salva))`, `^Notă`. → `critic` `amprenta_chat`
  în orice mod. (Există `amprenta_unealta` pentru placeholdere; de verificat dacă se poate
  extinde acolo.)

### P7. Regulă de proces pentru modele mici (doar documentație)

- În `SKILL.md`, la DRAFT: textul lung se scrie pe bucăți, fiecare bucată verificată înainte
  de următoarea; degenerarea apare spre final.
- În `revizie-contextuala.md`: pentru fiecare propoziție, întrebarea „ce imagine sau acțiune
  concretă e aici?”; dacă nu există răspuns, se taie, nu se rescrie.
- Nu se poate automatiza; rămâne judecată editorială.

## 5. Ce NU facem

- Nu adăugăm un detector de „coerență semantică” bazat pe model: skill-ul rămâne determinist
  și rulează fără rețea.
- Nu transformăm semnalele stilistice (P4, P5) în corecții automate (regula 4 din SKILL.md).
- Nu rescriem textele modelelor în `exemple-voce.md` decât dacă utilizatorul cere.

## 6. Riscuri și întrebări deschise (pentru critică)

1. **Fals pozitive la P1:** cuvinte care sunt valide și cu, și fără diacritice (fată/fata,
   mâna/mana?, pară/para, sânt/sant…). Prag agregat suficient? Alternativă: numărăm doar
   cuvintele a căror formă fără diacritice **nu** e în lexicon.
2. **Lexicon:** 1,45 M forme, `lexicon-ro.txt.gz`. Cât costă încărcarea la fiecare rulare?
   Există cache în `_comun.py`?
3. **P2 schimbă contractul `STATUS`** (PASS/EDITED/REWRITE). Impact asupra testelor existente
   și asupra documentației `human-voice-validator.md`?
4. **P3 engleză:** wordlist minimă sau euristică de sufixe? Risc de fals pozitive la
   anglicisme legitime (flex, hashtag, caption…) care sunt acceptate în registre colocviale.
5. **Eșantion mic:** 4 fișiere, 3 modele. Suficient ca să calibrăm pragurile sau riscăm
   supra-ajustare la aceste texte?
6. **Textele deepseek-1 au fost scrise cu thinking max și au degenerat;** e un caz de model, nu
   de skill. Merită investiție în P7 sau e în afara scopului skill-ului?
7. **Prioritate:** există un caz de utilizare real în care skill-ul e rulat de un model slab
   fără ghidare? Dacă nu, P1/P2 sunt suficiente și P4–P6 pot aștepta.

## 7. Cerere pentru reviewer

Critică acest plan, nu implementa nimic. Pentru fiecare punct P1–P7: merită / nu merită, ce
risc ai identificat, ce ai schimba. Verifică afirmațiile din §2–§3 pe textele din
`tests/fixtures/modele-slabe/` și rulează scripturile dacă te îndoiești. Semnalează orice finding greșit sau
exagerat, orice punct lipsă și ordinea recomandată. Răspuns scurt, verdictul primul.

## 8. Critica lui Opus 5.5 și status implementare (2026-11-05)

Verdict reviewer: planul merită, ordine schimbată; P1 ca scris nu se poate (lexiconul e pliat, deci
„restaurarea prin lexicon" e imposibilă). Corecții la findings: GLM are diacritice amestecate (~19%),
nu lipsă peste tot; `check-cuvinte` nu prinde structural „Șotroană", „Trei zeci", „dinti", „Opr-te",
„RETETĂ", „Nu niciodată"; din semnalele deepseek-2 o parte sunt fals pozitive (`numeral_fara_de` pe
„500 g"); „e despre" e calc real. Lipsă: regula D (autobiografie) se suprimă singură pe „luna"/cifre,
filler „hai să" dă fals pozitive în dialog, engagement bait fără semnal.

Set de control uman: `check-cuvinte` dă 6–24 de forme pe text uman bun → P2 cu prag fix e inaplicabil.

| Punct | Status |
|---|---|
| P6 intro/încheiere chat | FĂCUT: extins `artefact_chatbot` (Perfect!, Iată setul, Dacă vrei pot…, Notă scurtă:) |
| P3 `rest_cod` | FĂCUT: critic în `check-tipare.py` (`.CamelCase` lipit, tag-uri HTML, `{{…}}`); euristica pentru engleză NU |
| P1 diacritice lipsă | FĂCUT, altă metodă: pe paragraf, <8% cuvinte cu diacritice (≥18 cuvinte) sau ≥2 forme din listă (≥10 cuvinte); critic la ≥2 paragrafe. Fără fals pozitive pe fixture-urile umane/Mimo/Deepseek |
| hashtag-uri în `check-cuvinte` | FĂCUT: excluse (Mimo 4 → 1 formă) |
| regula D (autobiografie) | DE FĂCUT |
| P2 `LEXICON_UNVERIFIED` | DE DECIS: control uman dă 6–24 forme, deci doar câmp informativ, nu influențează STATUS; lexiconul costă ~0,36 s |
| P4, P7 (documentație) | DE FĂCUT |
| P5 (n-gramă repetată, multi-format) | DE FĂCUT |

Teste: 349 trec (au fost 346 + 3 noi pentru P1; teste existente adaptate: `test_diacriticele_nu_conteaza`
compară acum semnalele fără `diacritice_lipsa`; textul din `test_lista_scurta_normala` are diacritice).
