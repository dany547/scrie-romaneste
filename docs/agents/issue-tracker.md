# Issue tracker: GitHub

Issue-urile și specificațiile acestui repo trăiesc ca **GitHub Issues** în `dany547/scrie-romaneste`.
Toate operațiile se fac cu `gh` CLI.

## Convenții

- **Creează**: `gh issue create --title "..." --body "..."` (body multi-linie: fișier + `--body-file`).
- **Citește**: `gh issue view <n> --json number,title,body,labels,comments`.
- **Listează**: `gh issue list --state open --limit 50 --json number,title,body,labels,comments`.
- **Comentează**: `gh issue comment <n> --body "..."` / `--body-file <fișier>`.
- **Etichete**: `gh issue edit <n> --add-label "<etichetă>"` / `--remove-label "<etichetă>"`.
- **Închide**: `gh issue close <n> --comment "..."` (nu închide un issue deschis de altcineva fără acordul
  maintainer-ului; propune închiderea în comentariu).

Repo-ul se deduce din `git remote -v`; `gh` îl detectează singur când rulezi din clonă.

**Autentificare:** dacă `gh` nu e autentificat în mediul tău, folosește wrapperul de credențiale
documentat de mediul care rulează agentul. Niciodată nu pune tokenuri în repo, în comenzi sau în loguri.

## PR-uri ca suprafață de triaj

**PR-urile ca suprafață de cereri: nu.** _(Pune `da` dacă repo-ul ajunge să trateze PR-uri externe ca
cereri de feature; `/triage` citește acest flag.)_

GitHub împarte același spațiu de numerotare între issue-uri și PR-uri, deci un `#42` poate fi oricare:
rezolvă cu `gh pr view 42` și, dacă nu e PR, cu `gh issue view 42`.

## Când un skill zice „publică în issue tracker"

Creează un GitHub Issue. Corpul unui issue scris de un agent se semnează cu semnătura convenită de
profil (`[hermes-qa]` pentru profilul QA al acestui owner).

## Când un skill zice „ia tichetul relevant"

Citește-l ca la **Citește** mai sus.

## Reguli de lucru pe acest repo

- Fix-urile **nu** se pun direct pe `main`: branch `fix/issue-<N>-<slug>` + PR. Merge-ul îl decide
  maintainer-ul (Dan), niciodată un agent.
- Un PR care rezolvă un issue declară legătura explicit (`Closes #<N>` sau `Refs #<N>` în body) —
  altfel linkul issue↔PR nu poate fi detectat automat.
