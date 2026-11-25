# Markup HTML și WordPress (Gutenberg) — preflight și editare sigură

Fișierul acoperă preflight-ul offline și regulile de editare când textul trăiește în HTML sau în conținut de bloc WordPress (Gutenberg). Preflight-ul mecanic și validarea în editorul WordPress sunt **două straturi separate** — nu se substituie unul pe celălalt.

## 1. Contractul helper-ului offline (`check-markup.py`)

```bash
python3 <cale-skill>/scripts/check-markup.py --mode page|fragment|wp-body <fișier|->
```

Moduri de intrare:
- `page` — document HTML complet (poate conține `<title>`, `<meta name="description">`, `<h1>`–`<h6>` și corpul paginii).
- `fragment` — fragment HTML fără `<head>` / document complet.
- `wp-body` — conținut de postare WordPress (HTML + comentarii de bloc Gutenberg `<!-- wp:... -->`).

Ieșire JSON pe `stdout`:
- `text` — proiecția în text simplu a conținutului (**include heading-urile**).
- `title` — șir sau `null` (nullable); extras **numai în modul `page`**, din `<head>`-ul explicit sau implicit relevant al documentului (în `fragment` și `wp-body` rămâne `null`).
- `meta_description` — șir sau `null` (nullable); extras **numai în modul `page`**, din `<head>`-ul explicit sau implicit relevant al documentului (în `fragment` și `wp-body` rămâne `null`).
- `headings` — listă ordonată de obiecte `{level, text, line}`.
- `issues` — constatări offline strict despre **structura heading-urilor** și **împerecherea comentariilor de bloc / sintaxa JSON din atributele de bloc**, **nu** despre validitatea HTML generală.
- `gutenberg_compatibility` — `"unverified"` pentru `wp-body`, dar **și în `page`/`fragment` ori de câte ori apar marcatori de bloc WordPress recunoscuți (`<!-- wp:... -->`)**; `"not_applicable"` doar pentru `page`/`fragment` fără marcatori WordPress recunoscuți.

Coduri de ieșire:
- `0` — fără semnale offline.
- `1` — semnale/constatări prezente (rezultat normal de diagnostic, nu eșec).
- `2` — eroare de intrare, argument invalid sau fișier/codare defectă.

## 2. Cum rulezi `verifica.py` pe conținut cu markup

Nu pasa HTML crud sau conținut `wp-body` direct la `verifica.py` — **inclusiv în modul `audit` sau pe drafturi lungi scrise pe bucăți** (această regulă are prioritate față de rețeta generică `verifica.py <fișier>`). Tag-urile, comentariile de bloc și lipsa de `<title>`/`<h1>` dintr-un fragment poluează semnalele.

1. Rulează `check-markup.py --mode <page|fragment|wp-body>` pe sursă pentru proiecția curată și constatările de markup.
2. Rulează `verifica.py --fara-seo` (și `--human-voice`, dacă e util) **independent** pe:
   - corpul proiectat (`text`), și
   - metadatele extrase (`title`, `meta_description`) sau câmpurile suplimentare WordPress.
   Flag-ul `--fara-seo` evită să amestece regulile de nivel H1/H2 sau de titlu pe fragmente ori pe câmpuri izolate.
3. Validează separat ierarhia de heading-uri (`headings`), registrul titlului/subtitlurilor (`titluri.md`) și revizia editorială pe câmpuri (`references/limba/revizie-contextuala.md`).

### Exemplu rulabil (preflight + verificare pe proiecții)

```bash
python3 - <<'PY'
import json, subprocess, sys

html = """<!doctype html><html><head><title>Montaj centrală la bloc: ce intră în factură</title>
<meta name="description" content="Vezi costurile reale și actele cerute înainte să semnezi oferta."></head>
<body><h1>Montaj centrală la bloc: ce intră în factură</h1><p>Prețul afișat nu include coșul.</p></body></html>"""

p = subprocess.run([sys.executable, "scripts/check-markup.py", "--mode", "page", "-"],
                   input=html, text=True, capture_output=True)
data = json.loads(p.stdout)
for label, chunk in [("body", data["text"]), ("title", data["title"]), ("meta", data["meta_description"])]:
    if chunk:
        r = subprocess.run([sys.executable, "scripts/verifica.py", "-", "--fara-seo"],
                           input=chunk, text=True, capture_output=True)
        print(f"=== {label} (exit {r.returncode}) ===\n{r.stdout.strip()}")
PY
```

### Câmpuri suplimentare WordPress

Modul `wp-body` acoperă doar corpul postării (`post_content`). Pentru o publicare WordPress completă, verifică separat și câmpurile externe corpului:
- **titlul postării WP** (`post_title`, de regulă randat ca H1 în temă);
- **excerpt-ul WP** (`post_excerpt`), dacă tema sau listările îl folosesc separat;
- **câmpurile specifice plugin-ului SEO** (de ex. SEO title și meta description din Yoast, Rank Math, SEOPress etc.).

Toate intră în revizia pe câmpuri din `references/limba/revizie-contextuala.md`, citite atât standalone (snippet/outline), cât și față de corpul real și decizia cititorului.

## 3. Reguli de editare în HTML și Gutenberg

- **Fără decodare pe toată sursa:** nu decoda mecanic entitățile HTML (`&amp;`, `&nbsp;`, `&lt;`, `&quot;` etc.) pe tot fișierul — păstrează codarea originală în afara fragmentului editat.
- **Editări doar de text (copy-only):** modifică strict nodurile de text vizibile; **păstrează intacte** atributele, clasele CSS, ancorele (`id`), linkurile (`href`, `rel`, `target`), shortcode-urile și comentariile de bloc (`<!-- wp:... -->`).
- **Editări structurale:** pentru adăugare, ștergere, reordonare ori conversie de blocuri, ori modificări în JSON-ul atributelor de bloc, **folosește editorul de blocuri sau serializatorul oficial de blocuri** — nu construi manual JSON-ul sau wrapper-ele complexe de bloc Gutenberg.
- **Separare de rol:** reviewer-ul editorial (`references/limba/revizie-contextuala.md`) **nu editează markup crud**; livrează citate exacte, motive și înlocuiri minime de text, pe care editorul/scriitorul le aplică respectând regulile de mai sus.

## 4. Limita verificării offline vs. editorul WordPress

Constatările `check-markup.py` (structura heading-urilor, împerecherea marcatorilor de bloc, JSON) sunt **strict preflight offline**:
- **nu** verifică și **nu** demonstrează validitate HTML generală;
- **nu** demonstrează validitate de bloc Gutenberg sau absența erorii „Attempt Block Recovery” în editor.

Pentru confirmarea compatibilității Gutenberg / plugin:
1. Folosește un **mediu de editor autorizat și disposable** (staging / sandbox local) care potrivește **atât versiunea țintă de WordPress, cât și plugin-urile țintă** active.
2. Verifică fluxul **preview → save → reopen** în editorul de blocuri pe conținutul modificat.
3. **Niciodată pe producție** pentru probe sau validare de markup.
4. Dacă nu există un mediu disposable autorizat disponibil, raportează explicit **`gutenberg_compatibility: unverified`** — nu declara compatibilitatea validată doar pe baza preflight-ului offline.
