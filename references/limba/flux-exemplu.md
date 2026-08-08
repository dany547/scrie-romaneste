# Un traseu complet, de la cerere la livrare

Exemplu de lucru pentru fluxul din `SKILL.md`. Rapoartele de mai jos sunt
ieșirea reală a scripturilor, nu reconstituiri.

Produsul și cifrele lui sunt inventate pentru exemplu. Într-o sarcină reală ele
vin din fișa tehnică a clientului — dacă lipsesc, textul iese mai sărac și
marchezi `[DE COMPLETAT: …]`, nu completezi cu ce sună plauzibil.

## Cererea

> Scrie descrierea de produs pentru rucsacul Vertex 38L de pe site.

## Pasul 2 — contractul intern

Nu se livrează, nu se anunță. Se stabilește în gând, în zece secunde:

- **scop:** cititorul înțelege dacă rucsacul i se potrivește și adaugă în coș;
- **cititor:** om care merge pe munte de câteva ori pe an, nu alpinist; compară
  două-trei modele în tab-uri deschise;
- **canal și gen:** pagină de produs, magazin online;
- **registru:** direct, persoana a II-a, `tu`;
- **lungime:** 80-120 de cuvinte;
- **fapte confirmate:** volum 38 l, greutate, material, preț — **toate din fișa
  tehnică a clientului.** Ce nu e acolo nu intră în text.

Contractul decide deja jumătate din rezultat: „compară două-trei modele" înseamnă
că textul trebuie să spună ce e *diferit*, nu ce e bun.

## Pasul 4 — draftul

```text
În lumea de astăzi, echipamentul potrivit reprezintă diferența dintre o tură
reușită și una ratată. Fie că ești la prima drumeție sau ai deja experiență pe
munte, Vertex 38L este alegerea care nu te dezamăgește.

Rucsacul se remarcă prin utilizarea unor materiale de ultimă generație și
printr-o gamă largă de soluții de organizare. Sistemul de ventilație constituie
un element important, iar spatele reglabil se adaptează în funcție de nevoile
fiecărui utilizator.
```

## Pasul 5 — verificarea

```bash
python3 <cale-skill>/scripts/verifica.py - --fara-seo <<'TEXT'
…draftul…
TEXT
```

(`--fara-seo` fiindcă e un fragment de text, nu pagina întreagă cu heading-uri.)

```text
== tipare AI
critic|introduceri|L1|În lumea de astăzi, echipamentul potrivit reprezintă difer|→ elimină; începe cu subiectul concret
important|cuantificari_vagi|L6|materiale de ultimă generație și printr-o gamă largă de soluții de organizare|→ enumeră 2-3 exemple concrete
---
total=2 (critic=1, important=1) | 72 cuvinte | densitate=27.8/1000cuv
== ritm: text prea scurt pentru statistica (4 fraze)
---
scor_automat=1/13 (tipare=1/6, ritm=0/3, modelisme=0/4)
```

## Ce faci cu raportul

Scriptul a găsit **două** probleme. Draftul are **șase**. Asta e proporția
normală, și e motivul pentru care pasul 7 nu e „scor mic → livrează".

| Ce | De unde | Decizie |
|---|---|---|
| „În lumea de astăzi" | `critic`, din raport | tăiat, fără discuție |
| „o gamă largă de soluții" | `important`, din raport | înlocuit cu ce conține concret |
| „reprezintă", „constituie" | sub pragul de familie (2 < 3) | înlocuite cu „este" / verbul real |
| „Fie că ești la prima drumeție sau…" | sub prag (1 apariție) | tăiat — se adresa tuturor |
| „se remarcă prin" | `la_aglomerare`, o apariție | reformulat |
| „materiale de ultimă generație" | neprins de niciun tipar | înlocuit cu materialul propriu-zis |

Ultimele patru nu apar în raport fiindcă, izolate, nu sunt tipare — pragurile
sunt calibrate să nu semnaleze uzul normal. Le prinde recitirea, nu scriptul.

Un detaliu care contează: „materiale de ultimă generație" nu se poate înlocui
fără să știi materialul. Dacă fișa tehnică nu-l dă, nu-l inventezi — scrii mai
puțin sau lași `[DE COMPLETAT: material]` și îl semnalezi la livrare.

## Rezultatul

```text
Vertex 38L e rucsacul pentru turele de o zi și weekendurile scurte, unde 38 de
litri ajung fix cât trebuie: schimburi, mâncare, o geacă de ploaie.

Spatele are plasă tensionată, deci nu-l porți lipit de tine pe caniculă. Se
reglează pe înălțimea torsului, între 42 și 52 de centimetri — contează mai mult
decât pare, un rucsac reglat prost te doare de la umeri în două ore.

Cântărește 1,3 kg gol și are husă de ploaie în buzunarul de jos.
```

Ce s-a schimbat de fapt: prima frază spune **cui** i se potrivește și **de ce**
tocmai 38 de litri; fiecare afirmație are un număr sau o consecință în spate;
ultima frază închide pe fapt, nu pe formulă.

## Pasul 7 — poarta

Reverifici textul final (`scor_automat=0/13`), apoi treci lista din `SKILL.md`:
fapte confirmate, fără placeholdere rămase, contractul respectat — registru
direct, `tu`, 81 de cuvinte, cititorul care compară. Livrezi textul curat, fără
metacomentarii, și semnalezi separat orice `[DE COMPLETAT: …]`.
