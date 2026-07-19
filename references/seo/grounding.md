# Grounding — date care nu se inventă

O bună parte din regulile de aici cer date reale despre afacere. Nu le presupune și
nu le completa cu exemple plauzibile — un NAP inventat, un preț aproximat sau un
autor fictiv într-un `Article` sunt erori mai grave decât lipsa lor. Se aplică
aceeași regulă ca la fapte și cifre din `references/limba/tipare-ro.md`
(`sursa_fabricata`).

### Găsirea grounding-ului

Datele astea există aproape întotdeauna undeva — problema e că fiecare proiect le
ține altfel. **Nu căuta un nume de fișier; caută conținutul.** Grounding valid e
orice sursă care conține date de business confirmate de utilizator, indiferent de
format: Markdown, `.txt`, YAML, JSON, PDF de la client, export dintr-un CMS,
un tichet, o pagină „Despre noi" deja publicată, sau chiar un mesaj anterior din
conversație.

Ordinea de căutare, înainte de a scrie conținut cu destinație comercială:

1. **Ce a indicat utilizatorul explicit.** Dacă a numit un fișier, o pagină sau un
   folder, aia e sursa autoritativă și bate orice altceva ai găsi singur. Dacă a
   lipit datele direct în conversație, la fel.
2. **Instrucțiuni permanente ale proiectului** — `CLAUDE.md`, `AGENTS.md`,
   `.cursorrules` sau echivalent. Conțin des numele brandului, publicul și tonul.
3. **Un fișier de brif, sub orice nume.** Caută după conținut, nu după denumire:
   grep după numele brandului, după „NAP", „ton", „public țintă", „cuvinte-cheie",
   `hreflang`, un CUI sau un prefix de telefon. Verifică rădăcina, `docs/`,
   `content/`, `.seo/`, un folder pe client. Numele uzuale (`BRIEF.md`,
   `CONTEXT.md`, `brand.md`) sunt doar puncte de plecare, nu o listă închisă.
4. **Date deja prezente în cod și pe site** — schema JSON-LD existentă, sitemap,
   `robots.txt`, `package.json`, footer, pagina de contact. Sursa cea mai de
   încredere pentru NAP e chiar site-ul live, dacă există.
5. **Dacă tot nu găsești, întreabă** — o singură dată, grupat, doar câmpurile
   necesare pentru textul cerut. Nu porni un interogatoriu pentru câmpuri care nu
   apar în ce ai de scris.

**Când proiectul are mai multe surse care se contrazic** (schema de pe site spune
un telefon, brif-ul altul), nu alege tu. Semnalează conflictul și întreabă care e
corectă — datele de contact greșite sunt exact genul de eroare care costă bani.

### Salvează ce afli

După ce utilizatorul îți dă datele, **oferă-te să le scrii într-un fișier de
grounding** pentru rulările viitoare — altfel le va reintroduce de fiecare dată.
Reguli:

- Scrie doar câmpurile **confirmate**. Un fișier de grounding cu câmpuri goale sau
  cu exemple e mai rău decât unul inexistent: la următoarea rulare arată a date
  reale și ajunge publicat.
- Respectă formatul proiectului. Dacă restul documentației e YAML, scrie YAML; dacă
  e un `CLAUDE.md`, adaugă o secțiune acolo. Nu impune un format nou.
- Notează **sursa și data** fiecărui câmp („telefon — confirmat de client,
  2026-07-18"). Prețurile, programul și politicile expiră.
- Nu pune în fișier date sensibile care nu au ce căuta într-un repo (date bancare,
  contacte personale ale angajaților).

Din acest motiv skill-ul nu livrează un șablon de brif gol: un formular
pe jumătate completat produce exact tipul de date plauzibile-dar-false pe care
secțiunea asta le interzice. Brif-ul se naște din prima conversație reală, cu
datele pe care utilizatorul le-a confirmat efectiv.

**Câmpuri care necesită confirmare, pe tip de conținut**:

| Ai nevoie de… | Când |
|---|---|
| nume brand, domeniu, URL canonic | orice pagină |
| public țintă și nivelul lui de expertiză | orice text |
| cuvântul-cheie principal + 2-3 secundare, cu volume | pagină optimizată |
| autor real (nume, funcție, credențiale) | `Article`, semnal E-E-A-T |
| NAP complet: denumire exactă, adresă, telefon | local SEO, `LocalBusiness` |
| program de funcționare, inclusiv zile speciale | Google Business Profile |
| preț, monedă, disponibilitate, SKU/GTIN | `Product`, pagini de produs |
| politici de retur, livrare, garanție | e-commerce, `Organization` |
| profiluri oficiale pentru `sameAs` | dezambiguizare entitate |
| date proprii (studii, teste, statistici interne) | conținut non-commodity, GEO |

**Ce faci când lipsesc**: scrie textul fără porțiunea afectată și semnalează
explicit ce lipsește, cu marcaj vizibil (`[DE COMPLETAT: telefon sediu]`).
Niciodată placeholder-e care arată a date reale („0721 123 456",
„Str. Exemplu nr. 1") — ajung publicate.

Excepție: dacă utilizatorul cere explicit un exemplu, un șablon sau o demonstrație,
datele fictive sunt în regulă — marchează-le ca atare.

