# Human Voice Validator

Validator separat pentru voce umană în conținut românesc. Nu stabilește autorul
unui text și nu rescrie: găsește câteva reflexe mecanice cu probabilitate bună,
apoi cere o decizie editorială. Rulează-l **după** verificarea de limbă, nu în
locul ei.

## Principii

- Un semnal nu este verdict. Păstrează formula când genul, persoana sau un fapt
din context o justifică.
- Nu căuta sinonime pentru a „păcăli” detectorul; repară numai pasajul care nu
spune nimic concret.
- Metafora literară, tonul colocvial, un slogan de marcă real și autobiografia
susținută de repere verificabile sunt alegeri posibile, nu erori automate.
- `garbage`, contaminarea conversațională și placeholderele sunt blocere: nu se
publică până nu dispar.

## Categorii A–J

| Cod | Categorie | Ce semnalează | Tratament |
|---|---|---|---|
| A | filler conversațional | „hai să”, „să lămurim”, „merită menționat”, „ține minte” | citește în context |
| B | punchlines | „asta e tot ce contează”, „regretele devin scumpe” | păstrează numai dacă finalul adaugă sens |
| C | metafore de copywriter | „busola ta”, „puntea către succes”, „farul”, „superputerea” | nu atinge metafora literară legitimă |
| D | autobiografie nesusținută | experiență personală generică, fără episod sau reper | semnal manual/contextual |
| E | structură repetitivă | „în primul rând… în al doilea… în al treilea” | păstrează doar ordinea necesară |
| F | concluzii evidente/redundanță | „pe scurt”, „în esență”, „răspunsul se vede singur” | încheie cu o idee nouă |
| G | promoțional | sloganuri și promisiuni de tip „descoperă secretul” | cere un fapt verificabil |
| H | română nenaturală/calcuri | „face sens”, „în termeni de”, „rol crucial” | formulează românește, direct |
| I | simetrie excesivă/adresare mecanică | „fie că ești…”, „indiferent de…”, „pentru oricine” | numește cazul concret |
| J | garbage/contamination | CAPS, text corupt, `answear`, `fashiondays`, prompt/JSON/chat/placeholder | **blocer** pentru corupție, contaminare și placeholder |


Detectorul de la D verifică doar contextul local: acceptă o experiență când
există date, timp, episod sau consecință. El nu poate valida adevărul unei
biografii; acesta rămâne un control uman și de surse.

## Scor, status și blocere

`AI_PATTERN_SCORE` este o penalizare, nu o probabilitate și nu o notă de
„umanitate”. Are intervalul `0/30`; fiecare categorie A-J contribuie o singură
dată, ca repetarea aceluiași tic să nu domine rezultatul. Statusul este:

- `PASS` — scor `0–5`;
- `EDITED` — scor `6–10`;
- `REWRITE` — scor `11+` sau orice blocker: garbage, contaminare ori placeholder.

Categoria J are strict `0` sau `3` puncte: CAPS singur este un semnal
editorial J cu `0` puncte; garbage, contaminarea sau un placeholder îi dau
categoria J greutatea unică de `3` puncte și activează blocker-ul. Scriptul nu
poate verifica adevărul unei autobiografii; la D verifică doar dacă lipsesc
repere locale. O poveste cu dată, episod sau consecință nu este marcată automat
și trebuie evaluată manual.

Schema JSON a fluxului integrat este:

```json
{
  "human_voice": {
    "AI_PATTERN_SCORE": 0,
    "STATUS": "PASS",
    "FABRICATED_EXPERIENCE": "NO",
    "CONTAMINATION_FOUND": "NO",
    "PATTERNS_REMOVED": 0,
    "ai_pattern_maxim": 30,
    "blockers": [],
    "potriviri": [
      {"categorie": "G", "subcategorie": "promotional", "severitate": "important", "puncte": 3, "linie": 4, "fragment": "…", "sugestie": "…"}
    ]
  }
}
```

Outputul text are aceleași valori ca linii separate:
`AI_PATTERN_SCORE=…/30`, `STATUS=…`, `FABRICATED_EXPERIENCE=YES|NO`,
`CONTAMINATION_FOUND=YES|NO`, `PATTERNS_REMOVED=0` și
`HUMAN_VOICE_BLOCKERS=…`. `PATTERNS_REMOVED` este mereu `0` în detector;
editorul îl completează după editare.

## Procedura în 7 pași

1. Rulează mai întâi fluxul existent: `python3 scripts/verifica.py text.md`.
2. Rulează auditul de voce separat: `python3 scripts/verifica.py text.md --human-voice`.
3. Dacă statusul este `REWRITE`, recitește toate semnalele înainte de editare.
Un blocker oprește livrarea necondiționat: elimină contaminarea, garbage-ul sau
placeholderul.
4. Pentru `PASS`, `EDITED` sau semnalele neblocante din `REWRITE`, citește
citatul și paragraful, apoi decide dacă semnalul are funcție de voce, gen sau
dovadă concretă.
5. Editează minim; nu uniformiza metafore, dialoguri sau autobiografii legitime.
6. Rulează din nou ambele audituri pe textul editat, inclusiv cu `--json` când
rezultatul este consumat de un agent.
7. Un reviewer independent verifică doar deciziile rămase: contextul, faptele,
registrul și blocerele. Nu rescrie pasaje curate.

Comenzi utile:

```bash
python3 scripts/check-human-voice.py text.md
python3 scripts/check-human-voice.py text.md --json
python3 scripts/verifica.py text.md --human-voice --json
```
