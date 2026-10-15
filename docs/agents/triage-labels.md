# Triage Labels

Skill-urile vorbesc în termeni de roluri canonice de triaj. Fișierul ăsta mapează rolurile pe
etichetele reale folosite în tracker-ul acestui repo.

| Rol canonic (mattpocock/skills) | Eticheta în tracker-ul nostru | Sens |
| ------------------------------ | ----------------------------- | ---- |
| `needs-triage`                 | `needs-triage`                | Maintainer-ul trebuie să evalueze issue-ul |
| `needs-info`                   | `needs-info`                  | Se așteaptă informații de la reporter |
| `ready-for-agent`              | `ready-for-agent`             | Complet specificat, gata pentru un agent autonom |
| `ready-for-human`              | `ready-for-human`             | Necesită implementare de om |
| `wontfix`                      | `wontfix`                     | Nu se va rezolva |

## Extinderi proprii (în afara setului canonic)

| Etichetă | Sens |
| -------- | ---- |
| `needs-dan` | Cere acces la DB/secrets/infra sau o decizie de business — doar maintainer-ul poate continua |

Când un skill menționează un rol (ex. „aplică eticheta de AFK-ready"), folosește string-ul
corespunzător din tabelul de mai sus. Etichetele trebuie să existe în repo (`gh label list`);
dacă lipsesc, creează-le cu `gh label create "<nume>"`.
