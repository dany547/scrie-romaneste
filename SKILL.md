---
name: scrie-romaneste
description: >
  Genereaza si rescrie text in limba romana natural, uman, fluent, fara
  cliseele tipice modelelor AI (tranzitii mecanice, "in concluzie", romgleza,
  hedging) si respectand regulile SEO/GEO. Foloseste acest skill cand
  utilizatorul cere sa scrii, rescrii, editezi sau revizuiesti orice text in
  limba romana - articole, descrieri de produs, pagini web, continut blog,
  postari - sau cand mentioneaza explicit "scrie romaneste", clisee AI,
  ton natural, romgleza, SEO/GEO in limba romana.
---

# Scrie Românește

Skill pentru generarea și revizuirea de text în limba română care sună natural și uman,
nu ca text produs de un model lingvistic. Combină reguli de limbă (gramatică, stil,
anti-tipare AI) cu reguli de optimizare SEO/GEO — fără ca una să o strice pe cealaltă.

## Reguli critice (rezumat — detalii în references/)

**Interzis** (vezi `references/limba/anti-tipare-ai.md` pentru lista completă):
- Tranziții mecanice: „în concluzie", „prin urmare", „de asemenea", „totodată", „mai mult
  decât atât", „pe de o parte... pe de altă parte".
- Introduceri formulaice: „în lumea de astăzi", „în era digitală", „în societatea modernă".
- Umpluturi meta-text: „este important de menționat că", „merită subliniat faptul că".
- Adjective corporatiste/dramatice: „revoluționar", „impresionant", „remarcabil"; sintagme
  ca „adoptă o abordare", „schimbare de paradigmă", „un pilon fundamental".
- Cuantificări vagi: „o serie de", „un număr semnificativ", „o gamă largă de".
- Hedging: „este posibil ca", „s-ar putea ca" — fii asertiv.
- Romgleză: „face sens" → „are sens"; „joacă un rol crucial" → „are un rol esențial"/„e
  determinant"; „la sfârșitul zilei" → „în cele din urmă"; „în termeni de" → „în ceea ce
  privește".
- „Capcana concluziei" — nu încheia texte cu un rezumat forțat care repetă ce s-a spus deja.
- Paragrafe simetrice și ritm monoton — variază lungimea frazelor (burstiness).

**Obligatoriu**:
- Diateza activă în locul pasivului birocratic (vezi `references/limba/gramatica-stil.md`).
- Un cititor-țintă concret în minte înainte de a scrie (vezi `references/limba/scris-eficient.md`).
- Verifică sursele înainte de a afirma fapte/statistici/citate.

## Fluxul de lucru

1. **LOAD** — citește cerința. Dacă textul are destinație online/comercială, încarcă și
   `references/seo/seo-geo.md`; dacă e text pur literar, sari peste partea SEO.
2. **DRAFT** — scrie dintr-o trecere completă, fără să te oprești să corectezi propoziție
   cu propoziție (vezi `references/limba/scris-eficient.md` §1).
3. **SELF-CORRECTION** — scanează draftul după `references/limba/anti-tipare-ai.md`.
   Opțional: rulează `scripts/check-tipare.py <fișier>` pentru o verificare mecanică
   rapidă a tiparelor, și — pentru conținut destinat publicării — `scripts/check-seo.py
   <fișier>` pentru structura de heading-uri și keyword stuffing.
4. **EVALUATE** — acordă un scor intern conform rubricilor din `references/limba/scoring-checklist.md`
   (naturalitate, ritm, gramatică) și `references/seo/scoring-checklist.md` (SEO/GEO,
   densitate informație). Prag minim: **8/10**. Sub prag → refactorizează și reevaluează.
5. **OUTPUT** — livrează textul final, curat, fără metacomentarii („Iată textul rescris
   conform regulilor..."). Livrează direct textul.

## Structura references/

```
references/
├── limba/
│   ├── anti-tipare-ai.md      # clișee AI, romgleză, ton — verifică mereu
│   ├── gramatica-stil.md      # acord, punctuație, ortografie, pleonasm
│   ├── scris-eficient.md      # tehnici de proces: draft/editare, ritm, concizie
│   └── scoring-checklist.md   # rubrica 1-10, criteriile de limbă (1-3)
└── seo/
    ├── seo-geo.md             # SEO tehnic/on-page/e-commerce/blog/local + GEO
    └── scoring-checklist.md   # rubrica 1-10, criteriile SEO (4-5)
```

Încarcă doar fișierele relevante pentru sarcina curentă — nu e nevoie să citești tot
`references/` pentru o singură propoziție de rescris.

## scripts/

- `check-tipare.py` — scanează un text pentru clișeele din `anti-tipare-ai.md`. Exit 0
  = curat, exit 1 = găsite potriviri. `--help` pentru detalii.
- `check-seo.py` — verifică heading-uri (H1 unic, fără sărituri de nivel) și keyword
  stuffing într-un fișier Markdown/HTML. Exit 0/1 la fel. `--help` pentru detalii.

Ambele sunt instrumente de sprijin pentru pasul SELF-CORRECTION — nu înlocuiesc judecata
asupra ritmului, naturaleții sau relevanței reale a conținutului.
