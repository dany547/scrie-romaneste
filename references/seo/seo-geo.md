# SEO tehnic, on-page, e-commerce, blog, local + GEO

Aplică aceste reguli **fără a compromite naturalitatea textului** — vezi `references/limba/anti-tipare-ai.md`
pentru interdicția de keyword stuffing și clișee. Un text optimizat SEO care sună robotizat
și-a ratat scopul.

## 1. SEO tehnic și on-page (bazele)

- **Titlu de pagină (`<title>`)**: unic pentru fiecare pagină, descrie exact conținutul,
  scurt dar informativ (motoarele de căutare taie titlurile prea lungi). Evită titluri
  generice („Pagina nouă") sau înșiruiri de cuvinte-cheie fără sens gramatical.
- **Meta descriere**: un rezumat de o propoziție-două, gândit ca text care să atragă un
  click din pagina de rezultate — nu un rezumat plictisitor, nici o listă de cuvinte-cheie.
  Unică pentru fiecare pagină.
- **URL-uri**: simple, cu cuvinte relevante pentru conținut, structură de directoare
  puțin adâncă, fără parametri/ID-uri criptice, fără litere mari inconsistente. O singură
  versiune canonică per conținut (evită duplicate pe URL-uri diferite).
- **Ierarhia de heading-uri (H1-H6)**: un singur H1 per pagină (subiectul central),
  H2/H3 pentru subsecțiuni în ordine logică, fără să sari niveluri (H1 → H3 fără H2) și
  fără să folosești heading-uri doar pentru stilizarea vizuală a textului.
- **Structură de navigare**: ierarhie clară de la general la specific (pagină principală →
  categorie → conținut specific), breadcrumbs pentru orientare, majoritatea legăturilor
  în text simplu (nu doar în meniuri JS/imagini) pentru accesibilitate și crawling.
- **Sitemap**: un fișier XML Sitemap pentru motoarele de căutare + eventual o pagină HTML
  de site map pentru utilizatori, dacă site-ul are multe pagini.

## 2. Conținut (partea unde textul propriu-zis contează)

- **Conținut util și original** contează mai mult decât orice truc tehnic — utilizatorii
  recunosc conținutul de calitate și îl distribuie organic.
- **Anticipează vocabularul cititorului**: un cunoscător caută alți termeni decât un
  începător pe același subiect; include variații naturale de exprimare, nu doar termenul
  „oficial" — dar fără să îngrămădești sinonime artificial.
- **Anchor text (textul unui link)**: descriptiv și concis, nu „click aici" sau „articol";
  spune ce se găsește la destinație. Valabil și pentru linkurile interne, nu doar externe.
- **Imagini**: nume de fișier descriptiv + atribut `alt` care descrie imaginea (util pentru
  accesibilitate și pentru căutarea de imagini) — scurt, nu o propoziție întreagă, fără
  înghesuire de cuvinte-cheie. Imaginile de calitate oferă suficient context pentru ca
  utilizatorii să distingă dacă rezultatul corespunde căutării lor.
- **Text lizibil**: fără greșeli gramaticale/ortografice, text real (nu încorporat în
  imagini, unde nu poate fi citit de crawler sau copiat de utilizator).
- **Conținut organizat pe subiect**: paragrafe/secțiuni separate clar, nu blocuri masive
  de text pe subiecte diferite fără separare vizuală.
- **Conținut actualizat**: verifică periodic conținutul publicat și actualizează-l la nevoie;
  șterge conținutul care nu mai este relevant. Paginile actualizate au șanse mai mari de
  ranking decât cele abandonate.
- **Calitate peste cantitate**: nu există un număr magic de cuvinte țintă. Scrie natural,
  variază vocabularul — cu cât folosești mai multe cuvinte relevante, cu atât ai mai multe
  șanse să apări în rezultate, dar nu umple textul artificial.

## 3. Ce evită un text SEO natural (interzis)

- Keyword stuffing — repetarea nefirească a cuvântului-cheie doar pentru motor, nu pentru
  cititor (ex. „cumpără X, cel mai bun X, X ieftin, X calitate" înșirat fără sens).
- Text ascuns de utilizatori dar vizibil crawlerelor (practică penalizată, oricum).
- Titluri/meta-descrieri care nu au legătură cu conținutul paginii.
- Conținut duplicat sau reciclat fără valoare adăugată reală.
- Conținut generat în masă (scaled content abuse) — crearea de pagini multiple cu scopul
  de a manipula rankingul, chiar dacă sunt scrise cu AI. Google penalizează acest comportament.
- Continut slab, lipsit de valoare reală pentru utilizator — „commodity content" (ex. „7
  sfaturi pentru cumpărători începători") care nu oferă perspectivă unică sau expertiză.
- Reclame excesive care distrag atenția de la conținutul principal și îngreunează lectura.

## 4. SEO pentru e-commerce

- Descrierile de produs vând prin **beneficii reale**, nu prin specificații tehnice goale
  și clișee („calitate superioară", „design inovator" — interzise și de `anti-tipare-ai.md`).
- Fiecare produs are titlu și meta-descriere proprii — niciodată un singur text dublat
  pe zeci de variante de produs.
- Structurează informația scanabil: caracteristici cheie în listă, restul în text continuu.
- Structura URL-urilor e-commerce: `categorie/produs-nume` — directoare logice pentru
  ca Google să înțeleagă frecvența de actualizare a fiecărei zone.
- Pagină dedicată per produs, cu descriere unică; evită pagini de categorie cu text generic
  copiat.
- Implementează pagination sau infinite scroll cu link-uri către paginile următoare
  pentru ca Google să indexeze tot catalogul.
- Folosește `rel="canonical"` pe variantele de produs (culoare, dimensiune) pentru a
  evita conținutul duplicat.

## 5. SEO pentru blog și pagini de conținut

- Titlu + introducere care promit clar ce oferă articolul, fără deschideri formulaice.
- Structură pe subtitluri (H2/H3) pentru scanabilitate — vezi și `references/limba/scris-eficient.md` §6.
- Liste și bold pentru puncte cheie, fără să transformi tot textul în liste.
- Scrie pentru cititor, nu pentru robot — conținutul util, convingător și orientat spre
  oameni va influența prezența în rezultate mai mult decât orice altă sugestie tehnică.
- Include imagini de calitate lângă text relevant — acestea ajută Google să înțeleagă
  contextul imaginii și al paginii.
- Adaugă link-uri către resurse relevante (interne și externe) — linkurile ajută Google
  să descopere pagini noi și oferă valoare cititorului.
- Folosește link text descriptiv (anchor text) — nu „click aici", ci text care descrie
  conținutul paginii de destinație.

## 6. Cercetarea cuvintelor-cheie (keyword research)

- **Pornește de la afacere, nu de la cuvinte**: identifică produsele/serviciile reale
  pe care le oferi, apoi găsește cum le caută oamenii. Nu inventa cuvinte-cheie fără
  legătură cu realitatea afacerii.
- **Anticipează vocabularul cititorului**: un expert caută termeni diferiți decât un
  începător pe același subiect. Include variații naturale de exprimare — nu doar termenul
  „oficial" (ex. „asigurare auto" vs. „RCA" vs. „poliță de asigurare").
- **Un cuvânt-cheie per pagină**: fiecare pagină țintește un cuvânt-cheie principal și
  2-3 variante secundare. Nu comprima 10 cuvinte-cheie pe o singură pagină — diluezi
  relevanța.
- **Intenția de căutare (search intent)**: clasifică fiecare cuvânt-cheie după intenție:
  - **Informativă** („ce este SEO") → articol explicativ, ghid
  - **Navigațională** („Google Search Console login") → pagină dedicată
  - **Tranzacțională** („cumpără hosting") → pagină de produs/landing
  - **Comparațională** („WordPress vs. Joomla") → articol de comparație
  Pagina ta trebuie să corespundă intenției — nu pune o pagină de vânzare pe un cuvânt
  informativ.
- **Cuvinte-cheie long-tail** (expresii lungi, specifice): au volum de căutare mai mic
  dar conversie mai mare și competiție mai scăzută. Exemplu: „cel mai bun laptop
  pentru programare sub 4000 lei" vs. „laptop".
- **Instrumente de cercetare**: Google Trends (tendințe în timp), autosugestiile Google
  (ce caută oamenii concret), „Oamenii mai întreabă și" (People Also Ask), Google
  Search Console (ce cuvinte aduc deja trafic), competiția directă (ce cuvinte folosesc
  competitorii).
- **Evaluează dificultatea**: cuvintele cu competiție mare (site-uri mari cu multe
  backlinks) necesită timp și efort semnificativ. Prioritizează cuvinte cu competiție
  moderată/scăzută pentru rezultate rapide.
- **Actualizează cercetarea periodic**: tendințele de căutare se schimbă. Re-verifică
  cuvintele-cheie la fiecare 3-6 luni, mai ales pentru subiecte sezoniere sau în
  schimbare rapidă.

## 7. Link building și autoritate (off-page SEO)

- **Backlinks de calitate** de la site-uri relevante și cu autoritate sunt cel mai important
  semnal off-page. Un link de la un site de specialitate valorează mai mult decât 100 de
  link-uri de la site-uri generice.
- **Textul anchor** al linkurilor primite trebuie să fie natural și diversificat — nu forța
  cuvinte-cheie exacte în toate linkurile.
- **Diversificare surselor**: linkuri de la domenii diferite (nu doar de la același site)
  au mai multă greutate.
- Promovarea naturală prin conținut de calitate: articole de specialitate, studii de caz,
  infografice, resurse utile — acestea atrag linkuri organice.
- Evită schemele de linkuri cumpărate sau schimbate artificial — Google le detectează și
  penalizează.
- Guest posting-ul pe bloguri relevante din industrie este o tactică legitimă, dar doar
  dacă aduce valoare reală cititorilor, nu doar un link.

## 8. SEO tehnic avansat

- **robots.txt**: controlează ce crawl Googlebot; nu bloca resurse CSS/JS critice — Google
  trebuie să vadă pagina ca un utilizator obișnuit. Blochează doar paginile cu adevărat
  irelevante (admin, căutare internă, parametri de sortare).
- **Canonical URLs**: specifică URL-ul canonic cu `rel="canonical"` pentru a preveni
  indexarea conținutului duplicat. Google va alege automat un URL canonic dacă nu specifici,
  dar e mai bine să decizi tu.
- **Redirect-uri 301**: folosește redirect 301 (permanent) pentru mutarea paginilor; redirect
  302 (temporar) doar pentru teste A/B pe perioade scurte. Lanțurile lungi de redirect-uri
  (301 → 301 → 301) consumă bugetul de crawl.
- **Meta robots tag**: `noindex` pentru paginile pe care nu vrei să le indexeze Google
  (rezultate de căutare internă, pagini de login); `nofollow` pe linkuri către pagini
  nesigure. Eticheta `X-Robots-Tag` în header-ul HTTP face același lucru.
- **Hreflang pentru site-uri multilingve**: folosește `hreflang` pentru a indica Google
  versiunea de limbă/regiune a fiecărei pagini; include și `x-default` pentru versiunea
  implicită. Erorile hreflang pot cauza afișarea greșită a versiunii de limbă.
- **JavaScript SEO**: Google poate procesa conținutul din JavaScript atâta timp cât nu
  este blocat. Pentru site-uri SPA/JS, asigură-te că routing-ul funcționează cu
  server-side rendering (SSR) sau dynamic rendering. Verifică că toate resursele
  critice (CSS, JS) sunt accesibile crawlerului.
- **Core Web Vitals**: măsoară și optimizare LCP ( Largest Contentful Paint < 2.5s),
  INP (Interaction to Next Paint < 200ms), CLS (Cumulative Layout Shift < 0.1).
  PageSpeed Insights oferă diagnostice specifice pentru fiecare metrică.
- **Mobile-first indexing**: Google indexează versiunea mobilă a conținutului ca versiune
  principală. Asigură-te că tot conținutul important este disponibil și pe mobil,
  cu același markup și aceleași date.
- **HTTPS obligatoriu**: site-urile fără HTTPS sunt marcate ca „Not Secure" în browser
  și pot fi penalizate în ranking. Migrarea la HTTPS necesită redirect 301 de la HTTP.
- **Pagina de eroare 404**: personalizată, cu link-uri către conținut relevant, nu
  redirect automat către homepage (pierde contextul pentru crawler și utilizator).

## 9. Structured Data / Schema Markup

- **Format**: folosește JSON-LD (cel mai simplu de implementat și menținut); evită
  Microdata și RDFa decât dacă ai un motiv specific.
- **Validare obligatorie**: testează întotdeauna markup-ul cu Google Rich Results Test
  înainte de publicare; corectează erorile critice. Apoi folosește URL Inspection tool
  din Search Console pentru a verifica cum vede Google pagina.
- **Tipuri de schema utile**:
  - `Product` — pentru pagini de produs (preț, disponibilitate, recenzii)
  - `Article` / `NewsArticle` — pentru articole de blog și știri (headline, author,
    datePublished, dateModified)
  - `FAQPage` — pentru secțiuni de întrebări frecvente
  - `HowTo` — pentru tutoriale pas-cu-pas
  - `LocalBusiness` — pentru afaceri locale (adresă, telefon, program)
  - `BreadcrumbList` — pentru navigarea ierarhică (breadcrumbs)
  - `Organization` — pentru identitatea companiei (logo, social media)
  - `Review` / `AggregateRating` — pentru recenzii și evaluări

- **Schema Product — proprietăți obligatorii**:
  - `name`: numele produsului (string)
  - `image`: cel puțin o imagine (URL sau array de URL-uri)
  - `description`: descrierea produsului
  - `offers`: obiect cu `price`, `priceCurrency`, `availability`, `url`

- **Schema Product — proprietăți recomandate**:
  - `sku`, `mpn`, `gtin` — identificatori unici ai produsului
  - `brand` — obiect cu `name` (ex. `{"@type": "Brand", "name": "ACME"}`)
  - `review` — obiect Review cu `reviewRating` (ratingValue, bestRating) și `author`
  - `aggregateRating` — obiect AggregateRating cu `ratingValue` și `reviewCount`

- **Schema Product Snippet vs. Merchant Listing**:
  - **Product Snippet**: pentru pagini unde NU se vinde direct (recenzii editoriale,
    comparații). Suportă `positiveNotes` și `negativeNotes` (pros/cons).
  - **Merchant Listing**: pentru pagini cu cumpărare directă. Suportă detalii de shipping,
    return policy, dimensiuni vestimentare, loialitate.
  - Ambele tipuri pot coexiste pe aceeași pagină; cu cât mai multe proprietăți, cu atât
    mai multe posibile îmbunătățiri ale afișării în rezultate.

- **Exemplu JSON-LD Product (review page)**:
```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Nume Produs",
  "image": ["https://exemple.ro/1x1.jpg", "https://exemple.ro/4x3.jpg"],
  "description": "Descriere scurtă a produsului.",
  "sku": "0446310786",
  "brand": {"@type": "Brand", "name": "Brand"},
  "review": {
    "@type": "Review",
    "reviewRating": {"@type": "Rating", "ratingValue": 4, "bestRating": 5},
    "author": {"@type": "Person", "name": "Ion Popescu"}
  },
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.4, "reviewCount": 89},
  "offers": {
    "@type": "Offer",
    "url": "https://exemple.ro/produs",
    "priceCurrency": "RON",
    "price": 119.99,
    "priceValidUntil": "2026-12-31",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "https://schema.org/InStock"
  }
}
```

- **Exemplu JSON-LD FAQPage**:
```json
{
  "@context": "https://schema.org/",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Ce este SEO?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "SEO (Search Engine Optimization) este procesul de îmbunătățire a vizibilității unui site în motoarele de căutare."
    }
  }]
}
```

- **Exemplu JSON-LD Article**:
```json
{
  "@context": "https://schema.org/",
  "@type": "Article",
  "headline": "Titlul articolului",
  "author": {"@type": "Person", "name": "Autor"},
  "datePublished": "2026-01-15",
  "dateModified": "2026-07-18",
  "image": "https://exemple.ro/cover.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "Nume Site",
    "logo": {"@type": "ImageObject", "url": "https://exemple.ro/logo.png"}
  }
}
```

- **Exemplu JSON-LD BreadcrumbList**:
```json
{
  "@context": "https://schema.org/",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Acasă", "item": "https://exemple.ro/"},
    {"@type": "ListItem", "position": 2, "name": "Categorie", "item": "https://exemple.ro/categorie"},
    {"@type": "ListItem", "position": 3, "name": "Produs"}
  ]
}
```

- **Politici de business** (sub `Organization`):
  - `hasMerchantReturnPolicy` — politica de returnare
  - `hasLoyaltyProgram` — programul de loialitate
  - `shippingDetails` — politica de livrare (tarife, timp estimat)

- **Rich results nu sunt garantate**: chiar dacă markup-ul este valid, Google decide
  dacă afișează rich results în funcție de relevanță și calitatea generală a paginii.

## 10. Local SEO

- **Google Business Profile (GBP)**: creează și completează profilul cu informații
  exacte — numele afacerii, adresa completă, telefonul, domeniul de activitate, programul,
  fotografiile. Verifică afacerea (Google trimite un cod prin poștă sau telefon).
- **NAP consistency (Name, Address, Phone)**: aceleași date exacte pe tot site-ul și
  pe toate directoarele online. Orice inconsistență (ex. „Str. Mihai Viteazu" vs
  „Strada Mihai Viteazu nr. 10") poate afecta rankingul local.
- **Program actualizat**: include orele regulate și orele speciale (sărbători, vacanțe).
  Actualizarea regulată arată Google că afacerea este activă.
- **Recenzii și răspunsuri**: încurajează recenziile de la clienți reali; răspunde la
  fiecare recenzie (pozitivă sau negativă) — arată că valoarezi feedback-ul. Recenziile
  pozitive și răspunsurile utile ajută afacerea să iasă în evidență.
- **Fotografii și videoclipuri**: adaugă fotografii reale ale afacerii (interior, exterior,
  produse, echipă). Fotografiile de calitate cresc încrederea și rata de click.
- **Produse în magazin**: pentru retail, afișează produsele disponibile în magazin pe GBP
  — clienții pot vedea ce e în stoc înainte de a veni.
- **Factorii de ranking local**:
  - **Relevanța**: cât de bine corespunde profilul cu căutarea; completează toate
    câmpurile cu informații detaliate.
  - **Distanța**: cât de departe este afacerea de locația căutătorului; dacă nu își
    comunică locația, Google folosește datele pe care le are.
  - **Proeminența**: cât de cunoscută este afacerea — numărul de linkuri către site,
    numărul și calitatea recenziilor, prezența în directoare.
- **Nu poți plăti pentru ranking local mai bun**: Google nu oferă posibilitatea de a
  cumpăra poziții în rezultatele locale. Algoritmii sunt confidențiali pentru echitate.
- **Integrează referințe geografice reale** în conținutul de pe site (nume de zonă,
  cartier, oraș) — dar nu forța cuvântul-cheie local în fiecare propoziție.

## 11. GEO — Generative Engine Optimization (optimizare pentru AI search)

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

## 12. Audit SEO și monitorizare

- **Google Search Console**: instrument esențial gratuit — verifică indexarea, erorile
  de crawl, performanța în căutări (cuvinte-cheie, clicuri, impresii), Core Web Vitals,
  markup-ul de date structurate.
- **URL Inspection Tool**: testează cum vede Google o pagină specifică — verifică dacă
  este indexată, dacă are redirect-uri, dacă schema markup este detectat.
- **Google PageSpeed Insights**: analizează performanța paginilor (LCP, INP, CLS) pe
  desktop și mobil; oferă recomandări specifice de optimizare.
- **Rich Results Test**: validează markup-ul de date structurate JSON-LD/Microdata
  înainte de publicare.
- **KPI-uri de urmărit**:
  - Organic clicks și impresii (Search Console Performance)
  - Poziția medie pentru cuvinte-cheie țintă
  - Core Web Vitals (LCP, INP, CLS)
  - Numărul de pagini indexate vs. pagini submitate în sitemap
  - Numărul de erori de crawl
  - Rata de click (CTR) din rezultatele de căutare
  - Converziile din trafic organic

### Proces de audit SEO

1. **Verifică indexarea**: operatorul `site:domain.ro` arată câte pagini sunt indexate.
   Compară cu numărul real de pagini importante.
2. **Analizează erorile de crawl** în Search Console (Coverage report) — corectează
   erorile 404, redirect-urile lanț, paginile blocate de robots.txt sau noindex.
3. **Testează viteza** cu PageSpeed Insights pe cele mai importante 10-20 de pagini;
   prioritează LCP și INP.
4. **Verifică datele structurate** — testează fiecare tip de schema cu Rich Results Test.
5. **Analizează conținutul**: identifică paginile cu performanță slabă (multe impresii,
   puține clicuri) — pot fi necesare îmbunătățiri de titlu/descriere.
6. **Verifică linkurile interne**: toate paginile importante trebuie accesibile în
   maxim 3 click-uri de la homepage.
7. **Testează pe mobil**: asigură-te că experiența mobilă este identică cu cea desktop
   (conținut, imagini, funcționalități).

## 13. SEO competitiv

- Analizează **primele 5-10 rezultate** pentru cuvântul-cheie țintă: ce tip de conținut
  au (articol, ghid, listă, video), cât de lung este, ce structură au, ce date structurate
  folosesc.
- Verifică **linkurile competitorilor** (prin instrumente third-party) pentru a identifica
  oportunități de link building.
- Analizează **conținutul lipsă** — ce nu acoperă competitorii pe care tu îl poți oferi?
  Aceasta este oportunitatea ta de conținut non-commodity.
- Urmărește **actualizările de ranking** Google (core updates, spam updates) — schimbările
  de ranking pot indica oportunități noi sau vulnerabilități.
- Compară **structura tehnică**: viteza de încărcare, schema markup, mobile UX,
  Core Web Vitals ale competitorilor vs. ale tale.
