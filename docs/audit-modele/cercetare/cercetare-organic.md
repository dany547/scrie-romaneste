# Cercetare: text românesc pentru postări organice (data: 2026-11-05)

Legendă: OFICIAL = documentație platformă; SECUNDAR = presă/blog/tool; NEVERIFICAT = fără sursă solidă. "Vechi" = sursă mai veche de 12 luni (înainte de 2025-11-05).

## Tabel limite

| Platformă | Limită | Valoare | Statut / sursă |
|---|---|---|---|
| Instagram | Caption | 2.200 caractere | OFICIAL (Graph API, pagina fără dată, exemple v27.0): https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media |
| Instagram | Hashtag-uri | 5 per post/Reel (de la 30), aplicat gradual | Declarație Instagram citată de SocialMediaToday, 2025-12-18: https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/ . Pagina API încă spune 30 (și 20 @mențiuni). Tratează 5 ca plafon practic. |
| Instagram | Carusel | max 20 itemi; caption doar pe container, nu pe slide | OFICIAL (aceeași pagină API) |
| Instagram | Reels | 3 s–15 min, max 300 MB; fără limită separată de caption | OFICIAL (aceeași pagină) |
| Instagram | Trunchiere "mai mult" | ~125 caractere în feed | SECUNDAR (Metricool/ghiduri, nu Meta); NEVERIFICAT oficial |
| Facebook | Post | 63.206 caractere | SECUNDAR, istoric (anunț 2011, vechi): https://www.nbcbayarea.com/news/local/facebook-limits-you-to-63206-characters/1906169/ |
| Facebook | Trunchiere "Vezi mai mult" | ~477 caractere (feed) | NEVERIFICAT (doar un site de tool-uri) |
| Facebook | Hashtag-uri, grup/pagină | fără limită oficială găsită | NEVERIFICAT |
| LinkedIn | Post | 3.000 caractere | OFICIAL (Help): https://www.linkedin.com/help/linkedin/answer/a528176 |
| LinkedIn | Trunchiere "...mai mult" | ~140 mobil / ~210 desktop | SECUNDAR (vendori, ex. Medium/contentin); nedocumentat oficial |
| LinkedIn | Hashtag-uri | fără limită oficială; hashtag-urile consumă din cele 3.000 | Pagina Help nu menționează hashtag-uri; API Posts (Microsoft Learn, 2026-05-07) doar arată sintaxa: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api |
| LinkedIn | Carusel organic | API: carusel doar sponsorizat; organic = Document (PDF) sau MultiImage | OFICIAL (aceeași pagină API, 2026-05-07). Nr. max de pagini/imagini: NEVERIFICAT |
| TikTok | Caption (API Direct Post) | 2.200 UTF-16 | OFICIAL: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post (data paginii: nespecificată) |
| TikTok | Caption în aplicație | ~4.000 | SECUNDAR (tool-uri); NEVERIFICAT oficial |
| TikTok | Hashtag-uri | fără plafon oficial găsit; # și @ delimitate prin spațiu/rând nou | OFICIAL pentru sintaxă; afirmațiile "primele 5 contează" / "max 30" sunt contradictorii, NEVERIFICAT |
| Forum/comunități | Orice limită | NEVERIFICAT (nu am cercetat reguli Reddit/forumuri RO) | - |

Nota Meta: limita de 5 hashtag-uri e confirmată de Instagram, dar rollout gradual; unele surse spun 3 în teste (vechi/neoficial). Recomandare de lucru: maximum 3-5.

## Instagram

Sfaturi (sursele sunt SECUNDARE, marcate):
- Sfat: hook în primele ~125 caractere, fiindcă restul se ascunde după "mai mult" (cifra e secundară).
- Sfat: hashtag-urile ajută la categorisire, nu la reach. Mosseri, citat de Hootsuite/Verge: https://blog.hootsuite.com/social-media-updates/instagram/hashtags-dont-affect-reach/ . Folosește 3-5 relevante, la final sau în caption, nu lanț.
- Sfat: carusel = format cu engagement rate de top în benchmark-urile Socialinsider 2026 (0,50-0,55%, cifre inconsistente între versiuni): https://www.socialinsider.io/blog/instagram-benchmarks/ . Caption scurt (<60 cuvinte) pentru carusel, slide-urile fac munca: https://www.socialinsider.io/blog/social-media-caption-length-best-practices/ (actualizată oct. 2026; fără eșantion confirmat). La Reels lungimea caption-ului contează puțin (PostPlanify 2026, 4.408 postări, SECUNDAR).
- Sfat: Reels 45-60 s au cel mai bun engagement rate (0,35%, Socialinsider 2026).
- Link în caption nu e clicabil pe Instagram: NEVERIFICAT oficial aici; CTA corect = "link în bio" / DM / comentariu.
- Penalizat: lanț de hashtag-uri generice (#reels, #explore) vizate explicit de limita nouă (SocialMediaToday, 2025-12-18). Engagement bait pe Instagram: NEVERIFICAT în această cercetare.

## Facebook (pagină/grup)

- Oficial (vechi, 2017-12-18, +2019-01 pentru video): Meta demotează postările care cer reacții/share/tag pentru reach ("LIKE dacă ești Berbec", concursuri de share) și mai tare paginile repetitive: https://about.fb.com/news/2017/12/news-feed-fyi-fighting-engagement-bait/ . Pagina curentă din Help Center nu a putut fi accesată (404), deci politica actuală e NEVERIFICATĂ în formulare, dar principiul se păstrează. Excepție declarată: cereri reale de ajutor/recomandări.
- Sfat: 1-2 hashtag-uri cel mult; pe Facebook nu sunt căutate activ (ghid românesc, SECUNDAR, vechime necunoscută): https://mariussescu.substack.com/p/1171678_cum-trebuie-utilizate-etichetele-pe-facebook-hashtags
- Link în text vs comentariu pe Facebook: NEVERIFICAT (nu am găsit studiu/documentație).
- Grupuri: reguli de grup diferă; recomandare rezonabilă = întrebare autentică, context personal, fără promo pur. Fără sursă: NEVERIFICAT.

## LinkedIn

- Oficial: limită 3.000; LinkedIn poate reduce vizibilitatea postărilor detectate ca inautentice/automatizate (Help, link mai sus).
- Sfat: hook în ~140-210 caractere; rândurile scurte și spațiul alb ajută cititul (vendori; fără studiu citat). SECUNDAR.
- Sfat: 3-5 hashtag-uri recomandate de vendori; ">5 = spam" e NEVERIFICAT oficial.
- Sfat: link extern în prima postare reduce distribuirea, soluția comună e link în primul comentariu. Doar anecdotic (ghiduri 2026); cifrele "60-70% mai puține click-uri" nu au origine, nu le folosi. https://www.wildandfreetools.com/blog/linkedin-post-best-practices-2026/
- Engagement bait/pod-uri pe LinkedIn: NEVERIFICAT în această cercetare.

## TikTok

- Oficial: caption 2.200 UTF-16 prin API; hashtag/mențiune delimitate prin spațiu.
- Sfat: 3-5 hashtag-uri relevante (consens vendori, recurpost etc., neverificat oficial): https://recurpost.com/tiktok-scheduler/tiktok-character-limits-and-hashtags/
- Hook: NEVERIFICAT cu sursă solidă în această cercetare; practica generală = promisiunea/întrebarea în primele cuvinte, sub 1-2 secunde. Fără cifre.
- Emoji consumă mai mult de 1 unitate UTF-16 (un emoji poate fi 2+): consecință directă a regulii "UTF-16" din documentație, deci numără cu marjă.

## Forum / comunități

NEVERIFICAT. Nu am găsit surse solide pentru reguli RO (Reddit r/Romania, grupuri FB, forumuri). Pentru skill: regula generală să fie "citește regulile comunității; fără autopromovare; fără link-uri comerciale în primul mesaj". Aceasta e judecata mea, nu fapt sursat.

## Piața RO / limba română

- Date: 12,9 mil. identități active pe social media în Romania, oct. 2025 (DataReportal/Kepios): https://datareportal.com/reports/digital-2026-romania . Facebook ~13,06 mil. utilizatori (69% din populație), iunie 2026 (NapoleonCat, SECUNDAR): https://stats.napoleoncat.com/facebook-users-in-romania/2026/03/ . Instagram/TikTok/LinkedIn: cifre NEVERIFICATE (nu au apărut în rezultate).
- Diacritice în hashtag-uri: Instagram afișează etichete cu diacritice (ex. #românia pe liste publice, SECUNDAR). Nu există documentație oficială despre indexare/căutare. Facebook: date vechi și neconcludente (forum Opera, vechime necunoscută). Recomandare practică (judecata mea, nevalidată): perechea fără diacritice pentru cele de nișă (#romania, #bucuresti), deoarece cele mai folosite etichete publice sunt fără diacritice; testează în aplicație dacă hashtag-ul cu ș/ț duce la postări.
- Hashtag-uri compuse: CamelCase (#BucurestiInfo) ajută accesibilitatea (cititoare de ecran); fără sursă citată în această cercetare, deci NEVERIFICAT.
- Ghilimele „…" românești și diacritice corecte nu afectează limitele, dar numără ca 1 caracter fiecare în Instagram/LinkedIn; pe TikTok API contează UTF-16 (ș, ț, ă sunt 1 unitate).

## Lacune rămase

Fără sursă oficială: puncte exacte "mai mult" (toate platformele), limită hashtag LinkedIn/TikTok/Facebook, politică actuală engagement bait Meta/LinkedIn/TikTok, studii de conversie link-în-text vs comentariu, reguli forum RO, număr max pagini document LinkedIn.
