# Vocea în reclame — stratul de gen

Acest fișier e deliberat scurt: regulile generale de limbă și de voce trăiesc
în `../limba/` și se aplică integral și aici. Ce adaugă reclama e constrângerea:
payoff maxim în 30/90 de caractere, pe un cititor care nu te-a căutat.

## Structura unui anunț care funcționează

**Promisiune concretă → dovadă → direcție.**

- **Promisiunea** spune ce schimbă produsul, concret. Nu „pielea frumoasă",
  ci „tenul nu mai trage până la prânz".
- **Dovada** e mecanismul sau cifra: ingredient, număr, procedeu, garanție
  verificabilă. Fără dovadă, promisiunea e invitție.
- **Direcția** spune unde apucă cititorul. CTA-ul îl dau butoanele platformei;
  textul nu repeta „cumpără acum" mecanic — spune ce se întâmplă la clic
  („vezi compoziția completă", „testează setul de 7 zile").

## Testul schimbării de brand

Citește anunțul înlocuind numele brandului cu al concurentului. Dacă totul
rămâne la fel de adevărat, anunțul nu spune nimic despre brandul tău — e spațiu
plătit pentru un mesaj interschimbabil. Corecția: numele brandului, un detaliu
propriu (ingredient, origine, procedeu, cifră), o cifră care nu aparține nimănui
altcuiva. Mecanic: `check-reclame.py --brand "Nume"` semnalează textul care nu
conține brandul nicăieri.

## Referințe care se aplică integral

- **Afirmații goale / testul în 3 întrebări**: `../limba/anti-tipare-ai.md` §J.
  În anunț, redundanța de conținut nu are licență stilistică — o propoziție
  adevărată oricum („te pieptănești, părul e neted") e spațiu irosit.
- **Clișee promo și metafore de copywriter**: `../limba/human-voice-validator.md`
  (categoriile C și G).
- **Pleonasme, calcuri, forme nonnormative, numerale**: `../limba/modelisme.md`,
  `../limba/gramatica-stil.md` §3.8–3.9 — și acestea apar în anunțuri, unde
  fiecare caracter plătit trebuie să lucreze.
- **Limite și politici de platformă, format de fișier**: `platforme.md`.

## Modele pozitive

Set Google (toate headline-urile ≤ 30, descrierile ≤ 90 de caractere):

```markdown
H1: Creme cu ulei de măsline
H2: Hidratare 24h, fără parfum
H3: Lucrate în România, lot mic
H4: Pentru ten uscat și sensibil
D1: Șapte uleiuri cold-pressed. Dată fabricației pe cutie.
D2: Livrare în 24 de ore, oriunde în țară. Comenzi peste 200 de lei, gratis.
```

De ce funcționează: fiecare linie spune ceva ce un concurent nu poate copia
cuvânt cu cuvânt (7 uleiuri, lot mic, data fabricației), cifrele sunt
verificabile, nu există promisiuni fără mecanism și niciun caracter nu e
decorativ.

Set Meta (text principal ≤ 125, titlu ≤ 40, descriere ≤ 25):

```markdown
Text: Șapte uleiuri cold-pressed, zero parfum sintetic. Data fabricației, pe cutie.
Titlu: Hidratare 24 de ore
Descriere: Lot mic, livrare în 24 h
```

## Exemple înainte/după

**Înainte** (mecanic, fără sens, peste limite):
```markdown
H1: Seara cureți tenul, dimineața îl simți moale
D1: Descoperă secretul naturii! Pielea ta merită tot ce e mai bun!
```

**După** (mecanism + dovadă, în limite):
```markdown
H1: Balsam cu acid hialuronic
D1: Ține apa în ten până dimineața. Fără parfum sintetic. 50 ml, 39 lei.
```

Ce s-a schimbat: propoziția care descria o rutină (adevărată oricum) a devenit
o promisiune cu mecanism (acid hialuronic, „nu mai trage"), clișeele
(„descoperă secretul", „merită") au fost înlocuite cu cifre, iar semnele de
exclamare au dispărut — Google le respinge în headline-uri.
