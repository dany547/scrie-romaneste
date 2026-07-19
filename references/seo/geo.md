# GEO — Generative Engine Optimization (AI search)

Aplică regulile **fără a compromite naturalitatea textului** — vezi `references/limba/anti-tipare-ai.md`. Un text optimizat SEO care sună robotizat și-a ratat scopul.

### Ce este GEO și de ce contează

GEO (Generative Engine Optimization) este procesul de optimizare a conținutului pentru
a fi vizibil și citat de motoarele generative: AI Overviews, AI Mode (Google), Perplexity,
ChatGPT Search, Bing Copilot. Aceste sisteme folosesc **retrieval-augmented generation (RAG)** —
o tehnică (numită și grounding) care îmbunătățește calitatea, acuratețea și prospețimea
răspunsurilor AI prin intermediul sistemelor de ranking tradiționale, care recuperează
pagini relevante din indexul de căutare.

### Cum funcționează query fan-out

Când un utilizator pune o întrebare complexă, modelul generează **query-uri conexe
simultane** (query fan-out) pentru a obține mai multe informații relevante. Exemplu:
întrebarea „cum să repar o gazon plin de buruieni" poate genera query-uri precum
„erbicide bune pentru gazon", „îndepărtare buruieni fără chimicale", „prevenire buruieni
în gazon". Pagina ta poate apărea în rezultatele mai multor query-uri fan-out.

### SEO tradițional rămâne fundamentul GEO

Cele mai bune practici SEO continuă să fie relevante pentru că funcțiile generative AI
din Google Search se bazează pe sistemele fundamentale de ranking și calitate. Nu sunt
discipline opuse — optimizarea pentru AI search este, de fapt, optimizare pentru
experiența de căutare.

### Conținut non-commodity cu perspectivă unică

- Oferă o **perspectivă unică** care iese în evidență — AI-ul analizează multe surse,
  așa că e util să ai un punct de vedere diferit. O recenzie bazată pe experiență
  personală oferă perspectivă unică; un sumar al conținutului existent reia informații
  disponibile deja.
- Creează conținut **non-commodity** (peste cunoștințele comune): „De ce am renunțat
  la inspecție și am economisit banii" oferă expertiză reală, spre deosebire de
  „7 sfaturi pentru cumpărători începători" (conținut commodity).
- **Anticipează vocabularul cititorului**: scrie conținutul pentru publicul țintă,
  includând variații naturale de exprimare. Google înțelege sinonimele și sensul general
  al căutărilor — nu trebuie să capturezi fiecare variație exactă.

### Structură optimă pentru AI search

- **Întrebare → Răspuns scurt → Explicație**: începe secțiunea cu o formulare clară a
  întrebării/subiectului, oferă un răspuns direct în 1-2 propoziții, apoi dezvoltă.
- **Definiții clare și autonome**: o propoziție care definește termenul central trebuie
  să aibă sens chiar scoasă din context — motoarele generative citează fragmente izolate.
- **Date factuale verificabile**: cifre, date concrete, atribuiri corecte. Conținutul
  cu fapte verificabile are șanse mai mari de a fi citat ca sursă de încredere.
- **Organizare pe paragrafe și secțiuni** cu heading-uri clare — AI-ul poate extrage
  și prezenta secțiuni specifice din pagină. Nu este necesar să fragmentezi artificial
  conținutul în bucăți mici (Google înțelege nuanțele chiar și pe pagini lungi).
- **Include imagini și videoclipuri de calitate** — funcțiile generative AI pot aduce
  imagini și video relevante din pagină, deci mai multe oportunități de apariție în
  rezultate dincolo de link-uri simple.

### Ce NU funcționează pentru GEO (mituri)

- **Nu trebuie să creezi fișiere LLMS.txt** sau markup special pentru AI — Google nu
  le folosește. Crearea acestor fișiere nu afectează rankingul nici pozitiv, nici negativ.
- **Nu este necesar să „chunkuiești" conținutul** în bucăți mici — Google înțelege
  nuanțele mai multor subiecte pe o singură pagină. Fă pagini pentru publicul tău, nu
  pentru motoarele generative.
- **Nu trebuie să rescrii conținutul** într-un anumit mod doar pentru AI — sistemele
  AI înțeleg sinonimele și sensul general al căutărilor. Nu ai nevoie de cuvinte-cheie
  long-tail specifice sau de capturarea fiecărei variații.
- **Nu urmări „mențiuni" false** pe web — sistemele de ranking acordă atenție conținutului
  de calitate, iar sistemul de spam blochează manipulările. Funcțiile generative AI se
  bazează pe ambele.
- **Nu supra-optimizezi structured data** — nu este obligatoriu pentru GEO, nu există
  markup schema.org special. Folosește-l ca parte a strategiei SEO generale pentru
  a fi eligibil pentru rich results.

### Tactici GEO cu dovezi măsurate (studii independente, nu declarații Google)

Secțiunea de mituri de mai sus reflectă ce spune Google oficial. Ce urmează vine din
studii terțe care au măsurat corelații pe corpusuri mari. Cele două nu se contrazic
neapărat: Google spune „nu e nevoie să rescrii pentru AI", iar studiile arată că
textele bine scrise, dense factual și structurate cu răspunsul în față sunt citate
mai des. Aplică-le pentru că fac textul mai bun, nu ca pe niște trucuri.

**La nivel de scriitură** (studiul Princeton/Georgia Tech/IIT Delhi/Allen AI,
KDD 2024, ~10.000 de query-uri — cel mai riguros de până acum). Cinci modificări
au crescut vizibilitatea în răspunsurile generative cu 30-41%:

1. **Adaugă statistici** — cea mai eficientă modificare (+41%). „Aproape un sfert
   din căutări afișează un AI Overview" e mai citabil decât „tot mai multe căutări
   afișează un AI Overview". Vezi și regula anti-cuantificări-vagi din
   `references/limba/anti-tipare-ai.md` — aici cele două se suprapun perfect.
2. **Citează sursele** — atribuire explicită, cu numele sursei în text, nu doar
   un link ascuns în „aici".
3. **Include citate directe** (+28-40%) — o frază între ghilimele, atribuită unei
   persoane sau instituții reale.
4. **Voce autoritară** — afirmă, nu ezita. Coincide cu interdicția de hedging.
5. **Fluență** — fraze curate, fără îmbâcseală. Coincide cu tot ce cere
   `references/limba/scris-eficient.md`.

Atenție: regula de bază rămâne cea din `references/limba/tipare-ro.md` — **nu
inventa cifre, citate sau surse** ca să bifezi punctele de mai sus. O statistică
fabricată e o greșeală mai gravă decât absența ei.

**La nivel de structură**:

- **Răspunsul în prima treime a paginii**: o analiză pe 100 de AI Overviews a găsit
  că 55% dintre citări provin din primele 30% ale paginii. Concret: pune răspunsul
  direct la întrebarea principală în primele ~200 de cuvinte, nu după trei paragrafe
  de context. Se potrivește oricum cu regula anti-introduceri-formulaice.
- **Secțiuni de 120-180 de cuvinte** între heading-uri: pe 216.000 de pagini,
  acestea au avut în medie 4,6 citări, față de 2,7 pentru secțiuni mai scurte.
  Nu fragmenta artificial (Google confirmă că înțelege pagini lungi), dar nici nu
  lăsa blocuri de 600 de cuvinte fără subtitlu.
- **Heading-uri formulate ca întrebarea utilizatorului**: „Ce este GEO?" se
  potrivește mai bine cu interogarea decât „Despre GEO" sau „Prezentare generală".
  În română, formulează subtitlul cum ar tasta cititorul, nu cum sună într-un
  cuprins academic.
- **Paragrafe autonome**: fiecare paragraf trebuie să aibă sens scos din context —
  motoarele generative extrag fragmente izolate. Evită deschideri de paragraf care
  depind de anafora din paragraful anterior („Acest lucru înseamnă că…").
- **Definiții explicite** pentru termenii centrali, într-o singură propoziție.

**La nivel de pagină și site**:

- **Prospețime**: 76,4% dintre paginile cel mai citate de ChatGPT fuseseră
  actualizate în ultimele 30 de zile (Ahrefs, 17M citări); conținutul actualizat în
  ultimele 90 de zile e de ~2x mai probabil să fie citat. Actualizări de substanță,
  nu schimbarea datei. Afișează vizibil „Ultima actualizare: …".
- **Randare server-side obligatorie**: măsurători pe 500M de fetch-uri (Vercel/MERJ)
  nu au găsit **nicio** execuție de JavaScript la GPTBot, ClaudeBot sau
  PerplexityBot. Conținutul randat exclusiv client-side este invizibil pentru
  ChatGPT, Perplexity și Claude. Pentru SPA-uri: SSR sau prerendering.
- **Nu bloca crawlerele AI** în `robots.txt` (GPTBot, ClaudeBot, PerplexityBot,
  OAI-SearchBot) dacă vrei vizibilitate în ele — e o decizie de business, dar
  trebuie luată conștient, nu moștenită dintr-un `robots.txt` copiat.
- **Mențiuni pe surse terțe > backlinks**: pe 75.000 de branduri (Ahrefs),
  mențiunile de brand corelează 0,664 cu vizibilitatea în AI Overviews, față de
  0,218 pentru backlinks. Sursele terțe sunt citate de ~6,5x mai des decât
  conținutul propriu. Presa de specialitate, forumurile și comunitățile contează.
  (Google avertizează separat că mențiunile *fabricate* nu ajută — diferența e
  între acoperire reală câștigată și mențiuni cumpărate.)
- **Acoperirea sub-întrebărilor (fan-out)**: paginile care se poziționează pe
  sub-interogările conexe sunt cu 161% mai probabil citate în AI Overviews. Tratează
  subiectul cu întrebările lui satelit, nu doar cu interogarea principală.
- **Cercetare proprie**: paginile cu date proprii obțin de ~4,3x mai multe citări
  decât listările generice. Un mic set de date propriu (un test, o comparație de
  prețuri pe piața românească, un sondaj în rândul clienților) valorează mai mult
  decât încă un articol de sinteză.
- **Viteza contează și pentru citare**: paginile cu FCP sub 0,4s au avut de ~3x mai
  multe citări în ChatGPT decât cele peste 1,13s.

**Ce e speculativ sau riscant** (nu investi):

- `llms.txt` — adoptat de ~10% dintre domenii, fără nicio corelație măsurată cu
  citările; Google confirmă că nu îl folosește.
- Conținut servit diferit agenților AI față de utilizatori („shadow sites") — e
  cloaking clasic, încălcare de spam.
- Injectare adversarială de conținut pentru a influența modelele — risc de
  penalizare și de daună reputațională, fără beneficiu demonstrat.
- Schema `speakable` — nicio platformă AI nu a confirmat că o folosește.

### Măsoară vizibilitatea în AI features

- Folosește **Generative AI performance report** din Search Console pentru a vedea
  cum se comportă conținutul tău în funcțiile generative AI din Google Search.
- Fii sceptic față de instrumentele third-party care promit ranking sau pretind că
  folosesc metrici interne Google — niciun tool third-party nu are acces la sistemele
  interne de ranking.

### Agentic experiences (experiențe agente)

- AI agenții (autonomi) pot accesa site-ul tău pentru a colecta date: analizează
  rendering-ul vizual (screenshot-uri), inspectează DOM-ul, interpretează arborele
  de accesibilitate.
- Pregătește site-ul pentru agenți: asigură accesibilitatea informațiilor esențiale
  în markup semantic, evită dependența exclusivă de JavaScript pentru conținutul critic.
- Protocoale noi precum Universal Commerce Protocol (UCP) vor permite agenților
  Search să interacționeze mai avansat cu site-urile.

