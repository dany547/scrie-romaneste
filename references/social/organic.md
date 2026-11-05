# Postări organice

Postarea organică nu plătește pentru atenție: cititorul derulează și o oprește doar dacă primul rând îi
spune ceva. Regulile de mai jos sunt de voce și de structură. Cifrele sunt doar cele confirmate oficial.

## Limite confirmate (sursă, dată citire)

| Platformă | Limită | Sursă |
|---|---|---|
| Instagram | caption 2.200 de caractere; carusel max 20 de elemente | documentația Instagram Graph API (pagina nu are dată; citită 2026-11-05) |
| Instagram | 5 hashtag-uri per postare, aplicat treptat din decembrie 2025 | declarație Instagram citată de presa de specialitate; pagina API încă spune 30, deci tratează 5 ca plafon practic |
| LinkedIn | 3.000 de caractere; hashtag-urile consumă din ele | LinkedIn Help (citită 2026-11-05) |
| TikTok | caption 2.200 (UTF-16) prin API de publicare | documentația TikTok pentru dezvoltatori (pagina nu are dată) |

**Neverificat:** punctul exact în care „mai mult" / „vezi mai mult" taie textul (depinde de aplicație și
dispozitiv), limita de hashtag-uri pe Facebook, LinkedIn și TikTok, politicile actuale despre
engagement bait pe LinkedIn și TikTok. Nu scrie cifre pentru ele. Verifică în aplicație.

## Principii comune

- **Prima linie poartă postarea.** Tot ce e după „mai mult" poate să nu fie citit: ideea, nu salutul.
- **Un mesaj, un singur îndemn.** Cere un lucru concret și verificabil sau nu cere nimic.
- **Fără interacțiune artificială.** „Salută-mă în comentarii", „dă share dacă", „taguiește un prieten",
  „distribuie, te rog" sunt formule de platformă, fără legătură cu textul. Meta a anunțat (2017, vechi, dar
  singura sursă oficială găsită) că reduce distribuirea postărilor care cer reacții, share sau tag.
  O întrebare reală („ce hotel recomandați în Sibiu?") rămâne firească.
  `check-tipare.py` o semnalează ca `engagement_bait` (`minor`, de recitit în context).
- **Emoji: cu măsură.** Unul poate ține loc de ton; un rând de emoji în loc de informație nu. Nu le folosi
  ca marcatori de listă.
- **Hashtag-uri: puține, relevante, la final.** Hashtag-urile ajută la categorisire, nu la reach
  (declarațiile conducerii Instagram, citate de presă). Trei sau cinci bune bat zece generice.
  Hashtag-urile românești se scriu cum se caută: `#Romania` și `#Bucuresti` fără diacritice sunt etichetele
  folosite; pentru restul alege forma pe care o folosește comunitatea. Compuse: CamelCase
  (`#ViațăLentă`), pentru lizibilitate.
- **Mărturia personală se confirmă.** „Testat pe mine timp de o lună" apare doar dacă autorul chiar a
  făcut-o și adaugă rezultatul. Altfel se taie (`testat_pe_mine`, vezi `../limba/human-voice-validator.md`).
- **Fapte inventate: niciodată.** Nume, cifre, citate, adrese: `[DE COMPLETAT: …]` dacă lipsesc.
- **Diacriticele rămân în text.** Un text fără diacritice (`diacritice_lipsa`) arată neglijent chiar și pe
  rețele.

## Pe platformă

**Instagram.** Caption scurt pentru carusel: slide-urile fac munca, caption-ul dă contextul. Un slide, o
idee. Coperta promite ceva concret. Link-ul nu e clicabil în caption; spune unde e („link în bio") doar
dacă e adevărat.

**Facebook (pagină/grup).** Mesaj autonom, cu context înaintea link-ului. Link în text versus în primul
comentariu: nu există o regulă oficială; testează pe propria pagină, nu presupune o penalizare.
Pe grupuri, scrie ca un membru, nu ca o pagină.

**LinkedIn.** Primele rânduri spun concluzia sau tensiunea profesională; urmează exemplul sau datele.
Paragrafe scurte, fără jargon corporatist (`../limba/anti-tipare-ai.md` §C). Nu simula o poveste
personală pentru a vinde.

**TikTok.** Caption-ul e scurt și completează clipul; hook-ul stă în primele secunde ale clipului, nu în
text. Pentru script: situația concretă, acțiunea, rezultatul, fără prezentarea brandului la început.

**Forum și comunități.** Scrie ca un om cu o problemă sau o experiență: context scurt, ce ai încercat,
întrebarea clară. Fără tonul de promovare; comunitățile îl simt imediat. Respectă regulile grupului.

## Prost / mai bine

| Prost | De ce | Mai bine |
|---|---|---|
| „Salută-mă în comentarii cu ce bei azi 👇" | cerere de interacțiune fără legătură cu textul | încheie pe un detaliu al dimineții; întreabă doar dacă ai ce face cu răspunsurile |
| „Trei schimbări simple, testate pe mine timp de o lună" | experiență personală neconfirmată | numește schimbările și ce s-a întâmplat, sau scoate afirmația |
| „Distribuie, te rog. Poate ajunge la cineva care are nevoie." | cerere de share fără motiv | spune cui îi folosește informația și unde o găsește |
| „#dimineata #cafea #liniste #zilebune #slowmorning #povestidinbucatarie" | lanț de etichete generice | două sau trei relevante, la final |
