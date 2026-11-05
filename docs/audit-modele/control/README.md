# Set de control (text uman)

Cinci texte eseistice scrise de oameni, folosite doar pentru calibrarea pragurilor detectoarelor
(fals pozitive pe text uman bun). Material de grounding intern; nu se citează și nu se
redistribuie. Limită: toate sunt eseistică culturală, nu proză, reportaj sau social media.

## Rezultate de referință (verifica.py --fara-seo --human-voice; check-cuvinte)

| fișier | cuvinte | semnale verifica | check-cuvinte (forme) |
|---|---|---|---|
| control-uman-0 | 1056 | 3 minore | 24 |
| control-uman-1 | 683 | 0 | 7 |
| control-uman-2 | 895 | 1 important | 11 |
| control-uman-3 | 1357 | 0 | 23 |
| control-uman-4 | 1251 | 1 important | 6 |

Concluzie: `check-cuvinte` dă 6–24 de forme pe text uman bun (nume proprii, vocabular cultural).
Un prag „N=3 → nu mai e PASS” ar bloca tot textul uman; pragul trebuie să țină cont de nume proprii.
Textele integrale sunt în afara skill-ului: ~/CODE/scrie-romaneste-control/ (ignorate de Git).
