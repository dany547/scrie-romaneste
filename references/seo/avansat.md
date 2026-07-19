# SEO avansat — link building, tehnic avansat, audit, competitiv

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


## 14. SEO competitiv

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
