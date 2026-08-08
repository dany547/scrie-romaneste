# Structured Data / Schema Markup

- **Format**: folosește JSON-LD (cel mai simplu de implementat și menținut); evită
  Microdata și RDFa decât dacă ai un motiv specific.
- **Validare obligatorie**: testează întotdeauna markup-ul cu Google Rich Results Test
  înainte de publicare; corectează erorile critice. Apoi folosește URL Inspection tool
  din Search Console pentru a verifica cum vede Google pagina.
- **Tipuri de schema utile**:
  - `Product` — pentru pagini de produs (preț, disponibilitate, recenzii)
  - `Article` / `NewsArticle` — pentru articole de blog și știri (headline, author,
    datePublished, dateModified)
  - `LocalBusiness` — pentru afaceri locale (adresă, telefon, program)
  - `BreadcrumbList` — pentru navigarea ierarhică (breadcrumbs)
  - `Organization` — pentru identitatea companiei (logo, social media, `sameAs`)
  - `Review` / `AggregateRating` — pentru recenzii și evaluări
  - `FAQPage` — **nu mai produce rich results** (vezi mai jos), dar rămâne tip
    valid schema.org, util ca semnal semantic
  - `HowTo` — deprecat pe desktop din 2023; nu mai produce rich results

- **Tipuri retrase de Google (nu mai afișează rich results)**:
  - `FAQPage` — retras pe **7 mai 2026**. Raportarea în Search Console se oprește
    în iunie 2026, suportul API în august 2026. Markup-ul poate rămâne pe pagină
    fără probleme, iar rankingul nu e afectat — e o schimbare de afișare, nu de
    algoritm. Conținutul de tip întrebare-răspuns rămâne valoros pentru GEO (`geo.md`),
    doar că nu-ți mai extinde listarea în SERP.
  - `HowTo` — deprecat pe desktop din septembrie 2023.
  - Retrase în iunie 2025: `Book Actions`, `Course Info`, `ClaimReview`,
    `EstimatedSalary`, `LearningVideo`, `SpecialAnnouncement`, `VehicleListing`.
  - Tiparul de fond: când un tip de rich result e exploatat masiv de tool-uri SEO
    și încetează să descrie fidel pagina, Google îl restrânge și apoi îl elimină.
    Nu construi o strategie pe un rich result; construiește pe conținut corect
    descris.

- **Rolul nou al schemei (din 2026)**: AI Mode (Gemini) citește datele structurate
  ca **semnal de încredere și de verificare a entității**, nu ca declanșator de
  afișare. Schema exactă, care corespunde conținutului vizibil, crește
  probabilitatea de a fi citat într-un răspuns AI chiar și când nu se afișează
  niciun rich result. Nu există markup special „pentru AI" — e același markup pe
  care îl implementezi oricum pentru căutarea organică.

- **`sameAs` pentru dezambiguizarea entității**: leagă `Organization`/`Person` de
  profilurile canonice (Wikipedia, Wikidata, LinkedIn, pagini sociale oficiale).
  Un studiu controlat Schema App a măsurat +46% impresii și +42% clicuri pe 85 de
  zile după adăugarea `sameAs`. Pentru un brand românesc, include și profilurile
  locale relevante (Google Business Profile, pagina de firmă).

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

- **Exemplu JSON-LD FAQPage** (nu mai produce rich results din mai 2026; păstrat
  ca semnal semantic pentru sistemele generative):
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

