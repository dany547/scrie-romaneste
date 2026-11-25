# Checklist SEO/GEO și densitate de informație

Listă de citit înainte de livrare, partea online. Pentru limbă și ritm vezi
`references/limba/scoring-checklist.md`.

Criteriul 1 se aplică **doar** conținutului cu destinație online sau comercială.
Criteriul 2 (densitatea informației) se aplică oricărui text informativ, inclusiv fără
SEO. Pentru text pur literar sări peste tot fișierul.

## 1. Aderență la SEO/GEO, fără a strica stilul
   Verifică față de `core.md`: titlu unic și descriptiv, ierarhie de heading-uri
   coerentă (un singur H1, fără sărituri de nivel), fără keyword stuffing, structură
   scanabilă când conținutul o cere (liste, bold cu moderație).

   Pentru conținut destinat publicării, verifică suplimentar (`geo.md`,
   fără cote fixe de lungime sau de cuvinte-cheie):
   - Răspunsul la întrebarea sau decizia principală apare devreme, în deschidere,
     fără paragrafe de încălzire.
   - Lungimea secțiunilor urmează subiectul — fără pereți masivi de text și fără
     fragmentare artificială.
   - Subtitlurile reflectă ce caută sau decide cititorul, nu un cuprins plat.
   - Referenții sunt clari (fără „Acest lucru înseamnă că…" ambiguu), păstrând
     proza legată și incertitudinea reală unde datele au limite.
   - Termenii centrali sunt definiți clar doar unde cititorul are nevoie de asta.

   Specific pentru română (`core.md`, secțiunea specifică românei): text cu diacritice, diacritice cu
   virgulă (`ș`/`ț`) nu cu sedilă, slug-uri transliterate ASCII, romgleză doar
   acolo unde e cerută de interogarea reală.

## 2. Valoare și densitate de informație

   Fiecare propoziție adaugă ceva; nimic nu repetă o idee deja spusă doar ca umplutură.
   Vezi regula reducerii cu 10% din `references/limba/scris-eficient.md` §6.

   **Densitate factuală**: cifre concrete și dovezi confirmate din brief în locul
   cuantificărilor vagi, surse atribuite pe nume, perspectivă proprie care nu se
   găsește în primele zece rezultate pe același subiect, cu incertitudinea reală
   declarată onest unde există. Sunt exact elementele care fac textul util și
   citabil.

   **Fără să inventezi nimic.** O statistică fabricată, o sursă inexistentă sau un
   preț aproximat blochează livrarea, indiferent cât de bine sună textul. Dacă
   datele reale lipsesc, textul rămâne mai sărac și se marchează
   `[DE COMPLETAT: …]` — vezi `grounding.md`.

## 3. Titlu, subtitluri, deschidere și final

   SEO title, H1, meta descrierea, excerptul separat (dacă există) și fiecare
   H2/H3 trec prin revizia pe câmpuri din `references/limba/revizie-contextuala.md`
   (citite ca snippet/outline și confruntate cu secțiunea reală și decizia
   cititorului). Titlul are o promisiune concretă și corpul o plătește. Nu e
   etichetă („Centrale termice pe gaz") și nu e clickbait de tabloid. Subtitlurile
   citite în șir spun povestea articolului, nu cuprinsul unui manual. Deschiderea
   nu e încălzire — promisiunea titlului se atinge în primele propoziții. Finalul
   nu e rezumat și nu e formulă de politețe. Există cel puțin o propoziție care nu
   putea fi scrisă de altcineva.

   Detalii: `titluri.md`, `flux-articol.md`. Intrare mecanică, grosieră:
   `scripts/check-seo.py` (clickbait, șablon, etichetă, subtitluri plate).

## Blocante

Date de business inventate — nume, adrese, prețuri, autori, statistici proprii — opresc
livrarea. Nu e o problemă de punctaj: rescrie fără ele, marchează `[DE COMPLETAT: …]` și
cere-i utilizatorului ce lipsește (`grounding.md`).

Structura greșită (H1 multiplu, sărituri de nivel, keyword stuffing) se corectează, nu se
cântărește — `scripts/check-seo.py` o găsește singur.

Restul — lungimea secțiunilor, formularea subtitlurilor, autonomia paragrafelor — se
judecă în context. Un text scurt nu are nevoie de subtitluri ca să fie citabil.
