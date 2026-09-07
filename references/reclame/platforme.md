# Platforme de reclamă — limite, politici, format

Sursele de mai jos și data verificării. Când platformele își schimbă limitele,
actualizează aici și constantele din capul `scripts/check-reclame.py` (un singur
loc). Verificat: 2026-09-07.

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
| Text principal (Primary text) | 125 caractere — vizibil înainte de „Vezi mai mult" | 2200 |
| Titlu (Headline) | 40 caractere — trunchiat vizual | 255 |
| Descriere (Description) | 25 caractere — apare doar pe unele plasamente | 255 |

Hashtag-uri: maximum trei; restul sufocă mesajul și scad credibilitatea.

## Formatul fișierului de anunț

Textele se scriu în Markdown cu linii etichetate. Platforma e recunoscută din
heading-ul anterior („Google", „Meta/Facebook/Instagram") sau forțată cu
`--platform google|meta`. Fără etichete, scriptul tace — fișierul nu e anunț.

```markdown
# Campanie „Toamna pielii" — Google Search

H1: Creme naturale cu ulei de măsline
H2: Hidratare 24h, fără parfum sintetic
H3: Lucrate în România, lot mic
D1: Șapte uleiuri cold-pressed pentru ten uscat.
D2: Livrare în 24 de ore, oriunde în țară.
Cale1: creme-naturale
Cale2: reduceri

# Campanie Instagram — Meta

Text: Creme cu 7 uleiuri cold-pressed, fără parfum sintetic. Lot mic, dată fabricației pe cutie.
Titlu: Hidratare 24 de ore
Descriere: Testează setul de dimineață
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
