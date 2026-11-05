# Platforme de reclamă — limite, politici, format

Sursele de mai jos și data verificării. Când platformele își schimbă limitele,
actualizează aici și constantele din capul `scripts/check-reclame.py` (un singur
loc). Verificat: Google RSA 2026-09-07; Meta, Performance Max și TikTok 2026-11-05.

- Google Ads — „About responsive search ads":
  https://support.google.com/google-ads/answer/7684791
- Google Ads — „About text ads" (tabel de limite):
  https://support.google.com/google-ads/answer/1704389
- Google Ads — politici editoriale (punctuație, majuscule, repetiție):
  https://support.google.com/adspolicy/answer/6021546
- Meta — „Creative best practices for text in ads":
  https://www.facebook.com/business/help/223409425500940

## Limite de caractere

### Google Search (Responsive Search Ads) — limite hard

| Câmp | Limită | Observații |
|---|---|---|
| Headline (max 15) | 30 caractere | peste 30, Google nu acceptă textul |
| Descriere (max 4) | 90 caractere | |
| Cale de afișare (2) | 15 fiecare | doar litere, cifre și cratimă; fără spații |
| Semnul exclamării | — | interzis în headline-uri; maximum unul în descrieri |
| CAPS | — | respinse, afară de acronime (SPF, UV) |
| Emoji | — | respinse în textul anunțului |
| Asset-uri identice | — | respinse (politica de Repetition) |
| Structură minimă | 3 headline-uri, 2 descrieri | pentru Ad Strength decent |

### Meta (Facebook/Instagram)

| Câmp | Recomandat | Maxim hard |
|---|---|---|
| Text principal (Primary text) | 50–150 caractere (ghid oficial Meta, 2026-11-05) | 2200 (neverificat oficial) |
| Titlu (Headline) | 27 caractere (ghid oficial Meta, 2026-11-05) | 255 (neverificat oficial) |
| Descriere (Description) | fără recomandare oficială actuală; apare doar pe unele plasamente | 255 (neverificat oficial) |

Sursă pentru recomandările de mai sus: ghidul de reclame Meta pentru feed
(`https://www.facebook.com/business/ads-guide/image/facebook-feed/traffic`), citit la 2026-11-05.
Pagina „Creative best practices for text in ads" citată mai sus nu mai arată cifre.
Valorile 125 / 40 / 25, des citate în ghiduri terțe, nu au sursă oficială actuală (pot veni dintr-o
versiune mai veche sau din specificațiile Lead Ads). Pragul în care „Vezi mai mult" taie textul depinde
de plasament și nu e confirmat oficial: pune ideea-cheie la început, fără să te bazezi pe o cifră.
Înainte de producție, verifică limitele în Ads Manager.

Hashtag-uri: maximum trei; restul sufocă mesajul și scad credibilitatea.

### Google Performance Max (text assets) — limite oficiale

Sursă: https://support.google.com/google-ads/answer/17091269 (citită 2026-11-05, fără dată pe pagină).

| Câmp | Limită | Observații |
|---|---|---|
| Titlu | 30 caractere, 3–15 (recomandat 11+) | cel puțin unul de maximum 15 caractere |
| Titlu lung | 90 caractere, 1–5 (recomandat 2+) | |
| Descriere | 90 caractere, 2–5 (recomandat 4+) | una poate fi scurtă |
| Nume firmă | 25 caractere | să corespundă domeniului sau firmei verificate, fără text promoțional |
| CTA | 1, automat sau din listă | |

Activele se combină în orice ordine: fără trimiteri de tipul „vezi mai jos". `check-reclame.py` nu
verifică PMax; limitele sunt de aici, pentru redactare.

### TikTok Ads — doar ce e confirmat oficial

**Neverificat oficial:** limita de caractere a textului reclamei (surse vechi dau „maximum 100", cu
„4–60 recomandat", dar fără confirmare actuală), limita numelui de brand afișat și politicile detaliate
(paginile oficiale nu au putut fi citite integral). Nu scrie cifre pentru TikTok ca fapt; verifică în
Ads Manager înainte de producție. `check-reclame.py` **nu** are modul TikTok: un `Text:` fără
`--platform` primește limitele Meta, deci nu rula scriptul pe reclame TikTok.

Confirmat (pagina de configurare a reclamei, actualizată iunie 2026,
https://ads.tiktok.com/resources/help/article/ad-set-up): numele afișat trebuie să corespundă brandului,
produsului sau firmei. CTA-urile standard sunt în engleză în interfață (Learn More, Shop Now, Sign Up,
Order Now, Contact Us, Book Now etc.); lista exactă depinde de obiectiv și format.

**Sfat, nu regulă:** textul reclamei TikTok se scrie scurt și nativ, ca un caption; fără promisiuni
de rezultat și fără ascunderea caracterului comercial (vezi `voce.md`).

## Formatul fișierului de anunț

Textele se scriu în Markdown cu linii etichetate. Platforma e recunoscută din
heading-ul anterior („Google", „Meta/Facebook/Instagram") sau forțată cu
`--platform google|meta`. Fără etichete, scriptul tace — fișierul nu e anunț.

```markdown
# Campanie „Toamna pielii" — Google Search

H1: Creme naturale cu măsline
H2: Hidratare 24h, fără parfum
H3: Lucrate în România, lot mic
D1: Șapte uleiuri cold-pressed pentru ten uscat.
D2: Livrare în 24 de ore, oriunde în țară.
Cale1: creme-naturale
Cale2: reduceri

# Campanie Instagram — Meta

Text: Creme cu 7 uleiuri cold-pressed, fără parfum sintetic. Lot mic, dată fabricației pe cutie.
Titlu: Hidratare 24 de ore
Descriere: Testează-l dimineața
```

Etichete canonice: `H1…H15`, `D1…D4`, `Cale1/Cale2` (Google); `Text`, `Titlu`,
`Descriere` (Meta). Alias acceptate: `Headline`→H, `Description`→D, `Path`→Cale,
`Primary text`→Text. Caracterele se numără exact cum le afișează platforma:
`len()` pe textul curățat de spațiile marginale; diacriticele = 1 caracter.

## Ce NU verifică scriptul de reclame

Limbajul general — clișee, pleonasme, forme nonnormative, numerale fără „de" —
nu se duplică aici: le prind `check-tipare.py` și `check-modelisme.py`, rulate
de `verifica.py` pe orice text, anunțuri incluse. Scriptul de reclame adaugă
doar ce e dependent de gen: limite, politici de platformă și semnăturile
afirmărilor goale (vezi `../limba/anti-tipare-ai.md` §J pentru regula generală
și testul în 3 întrebări).
