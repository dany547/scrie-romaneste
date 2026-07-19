# SEO de bază — tehnic, on-page, conținut, specific limbii române

Aplică regulile **fără a compromite naturalitatea textului** — vezi `references/limba/anti-tipare-ai.md`. Un text optimizat SEO care sună robotizat și-a ratat scopul.

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


## 13. Specific pentru limba română

Regulile de mai sus sunt valabile în orice limbă. Cele de aici apar doar când
scrii pentru un public românesc.

### Diacriticele — cea mai frecventă confuzie

Google tratează **separat** căutările cu și fără diacritice: „masina de spalat" și
„mașină de spălat" sunt interogări distincte, cu volume și rezultate diferite,
chiar dacă Google cunoaște legătura dintre ele. Majoritatea utilizatorilor români
tastează fără diacritice.

De aici, regula practică:

- **Scrie textul cu diacritice.** Corectitudinea limbii nu se negociază, iar
  Google potrivește oricum textul cu diacritice la interogările fără. Textele cu
  diacritice sunt și dezambiguizate mai bine (`fata`/`fața`, `tara`/`țara`,
  `pastele`/`Paștele`, `sanie`/`sânie`).
- **Nu scrie două versiuni ale aceluiași text** ca să „prinzi" ambele forme — e
  conținut duplicat și keyword stuffing deodată.
- **Slug-uri și URL-uri fără diacritice**, transliterate ASCII:
  `masina-de-spalat`, nu `mașină-de-spălat`. Diacriticele în URL ajung
  percent-encoded (`ma%C8%99in%C4%83`), urât la partajare și predispus la erori.
  Transliterare: `ă→a`, `â→a`, `î→i`, `ș→s`, `ț→t`.
- **Diacritice cu virgulă, nu cu sedilă**: `ș`/`ț` (U+0219/U+021B), nu `ş`/`ţ`
  (U+015F/U+0163, caractere turcești). Sedila strică potrivirea în unele sisteme
  și e o greșeală de normă. Vezi `references/limba/gramatica-stil.md`.
- **Verifică volumele pentru ambele forme** în Keyword Planner înainte de a alege
  formularea din titlu — uneori diferența e de un ordin de mărime.
- **`alt` la imagini și numele fișierelor**: fără diacritice în numele fișierului;
  în `alt` scrie normal, cu diacritice.

### Romgleza în cercetarea de cuvinte-cheie

`references/limba/anti-tipare-ai.md` interzice romgleza **în text**. Pentru
cuvinte-cheie situația e alta: dacă publicul caută efectiv „review", „second
hand", „delivery" sau „laptop gaming", ignorarea termenului te scoate din
rezultate. Împacă-le astfel:

- Folosește termenul căutat acolo unde e necesar tehnic (titlu, un H2, o dată în
  text), cu forma românească alături: „Recenzie (review) …" sau alternând natural.
- Nu importa romgleza în restul textului doar pentru consecvență cu keyword-ul.
- Termenii consacrați în română au prioritate când există și se caută:
  „livrare" bate „delivery", „telefon mobil" bate „mobile phone".

### Configurare regională

- **`hreflang="ro-RO"`** pentru conținutul destinat României; `ro-MD` dacă
  targetezi separat Republica Moldova (vocabular și realități diferite). Include
  `x-default`.
- **`lang="ro"`** pe `<html>` — banal, dar des omis; afectează și cititoarele de
  ecran, și segmentarea corectă a textului.
- **Monedă `RON`** în schema `Offer`, prețuri afișate în lei, cu TVA menționat
  explicit (obligatoriu legal pentru consumatori).
- **Formate locale**: dată `15.01.2026` sau „15 ianuarie 2026" în text, dar
  `2026-01-15` (ISO) în schema markup; separator zecimal virgulă (`119,99 lei`)
  în text, punct în JSON-LD.
- **Adrese și NAP**: aceeași formă exactă peste tot, inclusiv abrevierile
  („Str." vs. „Strada", „nr." vs. „numărul", sectorul pentru București).

### GEO în română — ce e diferit

Modelele generative citează **mai puține surse externe** când întrebarea e pusă
în română decât în engleză, iar pe subiecte tehnice sau reglementate calitatea
răspunsurilor scade și apar confuzii de terminologie. Practic:

- Competiția pentru citare în română e mai slabă decât în engleză — un conținut
  bine structurat, cu date verificabile, are șanse disproporționat de mari.
- Zonele reglementate (fiscalitate, sănătate, dreptul muncii, asigurări) sunt
  exact acolo unde modelele greșesc cel mai des în română. Conținut corect,
  datat, cu referință la actul normativ concret (număr, an, articol) e valoros și
  citabil.
- Include explicit termenii instituționali românești (ANAF, ANPC, CASMB,
  Monitorul Oficial) — ancorează pagina la entitățile locale corecte.

