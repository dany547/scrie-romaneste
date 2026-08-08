# Scrie Românește

> Skill pentru generarea și revizuirea de text în limba română care sună natural și uman, nu ca text produs de un model lingvistic.

**Author:** Dan Mutu — [adcelerum.ro](https://adcelerum.ro)

## What it does

Combines Romanian language rules (grammar, style, anti-AI patterns) with SEO/GEO optimization — so one doesn't break the other. Use it whenever you need to write, rewrite, edit, or review text in Romanian: articles, product descriptions, web pages, blog content, social posts.

### Key features

- **Three modes** — `rescriere` (clean output), `audit` (report patterns without rewriting), `editare` (minimal targeted edits)
- **Anti-AI patterns** — mechanical transitions, corporate jargon, hedging, vague quantifiers. Each entry has a **replacement** and a **threshold**: some phrases are always wrong, others only when they cluster. One "de asemenea" in a 2000-word article is fine; six are not.
- **Romanian-specific failure modes** — the part an English skill cannot have: long-distance agreement, prepositional government, inflection errors, syntactic calques, false friends, borrowed-word articulation, diacritic restoration
- **Grammar & style** — punctuation, agreement, spelling, diathesis, language registers (400+ rules from Romanian school manuals)
- **Positive voice models** — annotated before/after rewrites per register, so the skill shows what to write, not only what to delete
- **Writing techniques** — rhythm, conciseness, structure, audience calibration
- **SEO/GEO** — on-page, technical, e-commerce, local, keyword research, structured data, AI optimization for generative search
- **Verification scripts** — pattern scanner (diacritic-insensitive, morphology-aware), stylometric rhythm analyser, SEO structure checker

## Installation

### Claude Code

Copy the skill folder into your project:

```bash
# In your project root
mkdir -p .claude/skills
cp -r /path/to/scrie-romaneste .claude/skills/scrie-romaneste
```

Or install globally:

```bash
mkdir -p ~/.claude/skills
cp -r /path/to/scrie-romaneste ~/.claude/skills/scrie-romaneste
```

The skill activates automatically when you mention writing Romanian text.

### OpenAI Codex CLI

```bash
# In your project root
mkdir -p .agents/skills
cp -r /path/to/scrie-romaneste .agents/skills/scrie-romaneste
```

Or install globally:

```bash
mkdir -p ~/.agents/skills
cp -r /path/to/scrie-romaneste ~/.agents/skills/scrie-romaneste
```

### Kilo CLI

```bash
# In your project root
mkdir -p .claude/skills
cp -r /path/to/scrie-romaneste .claude/skills/scrie-romaneste
```

Kilo reuses the `.claude/skills/` directory structure. The skill loads via the `skill` tool.

### Cursor

```bash
# In your project root
mkdir -p .cursor/rules
```

Then create `.cursor/rules/scrie-romaneste.md` containing:

```markdown
---
globs: "*.md,*.txt,*.html"
alwaysApply: false
description: "Romanian text generation and review skill"
---
```

Copy the contents of `SKILL.md` into that file, or reference it:

```bash
cp /path/to/scrie-romaneste/SKILL.md .cursor/rules/scrie-romaneste.md
```

### Windsurf / Devin Desktop

```bash
# In your project root
mkdir -p .windsurf/rules
cp /path/to/scrie-romaneste/SKILL.md .windsurf/rules/scrie-romaneste.md
```

Or for Devin:

```bash
mkdir -p .devin/rules
cp /path/to/scrie-romaneste/SKILL.md .devin/rules/scrie-romaneste.md
```

### Cline

Cline reads multiple skill formats natively:

```bash
# As a skill (recommended)
mkdir -p .cline/skills
cp -r /path/to/scrie-romaneste .cline/skills/scrie-romaneste

# Or as rules
mkdir -p .clinerules
cp /path/to/scrie-romaneste/SKILL.md .clinerules/scrie-romaneste.md
```

Cline also reads `.claude/skills/` and `.cursorrules`, so if you already have it installed for another tool, Cline will pick it up.

### Continue.dev

```bash
mkdir -p .continue/rules
cp /path/to/scrie-romaneste/SKILL.md .continue/rules/scrie-romaneste.md
```

### Aider

```bash
# Copy the skill contents to your project
cp -r /path/to/scrie-romaneste ./CONVENTIONS.md

# Or reference it in .aider.conf.yml:
# read: [scrie-romaneste/SKILL.md]
```

Aider loads conventions via `--read` or `.aider.conf.yml`.

### GitHub Copilot

```bash
mkdir -p .github
cp /path/to/scrie-romaneste/SKILL.md .github/copilot-instructions.md
```

For path-specific instructions:

```bash
mkdir -p .github/instructions
cp /path/to/scrie-romaneste/SKILL.md .github/instructions/romanian-text.instructions.md
```

Add `applyTo: "*.md"` to the frontmatter to scope it.

### Hermes Agent

```bash
mkdir -p ~/.config/hermes/docs
cp -r /path/to/scrie-romaneste ~/.config/hermes/docs/scrie-romaneste
```

## File structure

```
scrie-romaneste/
├── SKILL.md                        # Main skill definition (load this)
├── references/
│   ├── limba/
│   │   ├── anti-tipare-ai.md       # AI clichés with replacements + thresholds
│   │   ├── exemple-voce.md         # Annotated before/after rewrites, by register
│   │   ├── flux-exemplu.md         # One complete run: request → contract → draft → report → delivery
│   │   ├── tipare-ro.md            # Romanian-specific failure modes
│   │   ├── gramatica-stil.md       # Agreement, punctuation, spelling, pleonasms
│   │   ├── scris-eficient.md       # Process techniques: draft/edit, rhythm, concision
│   │   ├── modelisme.md            # Etymological pleonasms, anglicisms, paronyms
│   │   └── scoring-checklist.md    # Pre-delivery language checklist
│   └── seo/                        # Split by topic so agents load only what a task needs
│       ├── core.md                 # Technical, on-page, content, Romanian-specific
│       ├── grounding.md            # Business data that must never be invented
│       ├── geo.md                  # Generative Engine Optimization (AI search)
│       ├── schema.md               # JSON-LD / structured data
│       ├── ecommerce.md            # Product and category pages
│       ├── blog-keyword.md         # Blog content + keyword research
│       ├── local.md                # NAP, Google Business Profile
│       ├── avansat.md              # Link building, advanced technical, audits
│       └── scoring-checklist.md    # Pre-delivery SEO/information-density checklist
├── scripts/
│   ├── verifica.py                 # Orchestrator: all checks, one call, combined score
│   ├── check-tipare.py             # AI clichés, calques, generation artefacts
│   ├── check-ritm.py               # Sentence/paragraph uniformity (stylometry)
│   ├── check-modelisme.py          # Etymological pleonasms, anglicisms, paronyms
│   ├── check-seo.py                # Headings and keyword stuffing
│   └── _comun.py                   # Shared scanning engine (not a CLI)
└── tests/                          # Fixtures + unittest suite (stdlib only)
```

## Verification scripts

```bash
python3 scripts/verifica.py <file>          # all checks in one pass + combined score
python3 scripts/verifica.py <file> --json   # structured output for programmatic use
python3 scripts/verifica.py <file> --scor   # scores only
python3 scripts/verifica.py <file> --fara-seo  # skip SEO checks (literary text)

python3 scripts/check-tipare.py <file>      # AI clichés and calques only
python3 scripts/check-ritm.py <file>        # rhythm uniformity only
python3 scripts/check-modelisme.py <file>   # pleonasms/paronyms only
python3 scripts/check-seo.py <file>         # SEO structure only
```

Exit 0 = clean, 1 = issues found, 2 = input error. Use `--help` for details.
Where a pattern has a canonical fix, the report includes it inline after the
quote (`|→ are sens`), so an agent can correct without loading the reference
files first.

Matching ignores diacritics, so text written without them — or with the legacy
cedilla `ş/ţ` instead of the correct comma-below `ș/ț` — is scanned correctly.
Patterns cover inflected forms, not just dictionary forms.

**On `check-ritm.py`**: its thresholds derive from English-language corpora and
over-flag formal registers. Published false-positive rates for this class of
detector exceed 60% on non-native writers. Treat a bad score as "worth
rereading", never as proof of machine authorship.

```bash
python3 -m unittest discover tests
```

## Version

- **v0.5.2** — Fixed a silent matching bug: any multi-word pattern that fell
  across a line break was missed entirely. `_comun.py` now treats a literal space
  in a pattern as "space, or a single line break that does not start a new
  paragraph", leaving spaces inside character classes untouched (the dash pattern
  deliberately excludes `\n` so it never matches list markers). Measured on
  wrapped Romanian prose: at 80 columns the old engine missed ~1 in 6 detections,
  at 40 columns half of them — the same text scored differently depending on
  where the line wrap happened to land. Added a documentation-reference guard
  test: every `file.md` and `§N` mentioned in `SKILL.md` or `references/` must
  resolve, and every reference file must be routed from `SKILL.md`. That test
  covers the class of bug fixed by hand in 0.5.0 and 0.5.1. New
  `references/limba/flux-exemplu.md`: one complete run from request to delivery,
  with the scripts' real output and the decision taken on each signal, including
  the four problems the scripts do not catch. `SKILL.md` gained a rule for
  requests that ask for audit and rewrite at once, a `--json` recommendation for
  programmatic use, and a note for shells without heredoc. Tests 53 → 60.
- **v0.5.1** — SEO templates and agent ergonomics. The planned `sablon_seo`
  category was dropped: three of its phrases ("atunci când vine vorba de", "nu în
  ultimul rând", "nu e vorba doar de") belong in the existing `structura` table,
  one ("în funcție de nevoile") carries almost no signal, and a bare `fie că… fie
  că` is an ordinary correlative conjunction. What replaces it is the actual
  pattern: `simetrie_de_acoperire`, the sentence that addresses everyone so it
  ranks for every query ("Fie că ești începător sau profesionist…"). It requires
  sentence-initial position *plus* second-person address, counts per family, and
  stays out of the score. New `core.md` section on the Romanian agency-content
  register — mandatory opening definition, decorative FAQ, politeness sign-off,
  keyword forced into every H2, padding to a word count — none of which Google
  penalises and all of which readers recognise. SEO section numbering fixed
  (`core.md` jumped 3 → 13, leftovers from the `seo-geo.md` split). `SKILL.md`
  gained an operational section for weaker agents: where the scripts actually
  live, how to pipe text in via stdin, that exit 1 is a normal result rather than
  a failure, how to read the pipe-delimited report by severity, and what to do
  when `python3` is missing. Tests 51 → 53.
- **v0.5.0** — Naturalness over checklist compliance. New `CONTRACT` step in the
  workflow: genre, reader, channel, register and address form are fixed before
  the draft, not inferred after it. The global **8/10 score gate is gone** — it
  mixed a manual rubric with `verifica.py`'s deterministic penalty count and was
  unreachable for any text that skips SEO; both scoring checklists are now
  pre-delivery reading lists with explicit blockers. New
  `references/limba/exemple-voce.md` with annotated before/after rewrites, in
  neutral and colloquial variants, so one register does not become the universal
  model. `scris-eficient.md` cut from 237 to ~110 lines: the blogger-habit
  material (timed sprints, coffee, post-its, writing with the screen covered) is
  gone, and its contradictions with the anti-pattern rules — automatic summary
  endings, unconditional praise for lists and bold — are resolved. New
  `copula_evitata` and `referinta_vaga` detectors count *per family* rather than
  per pattern, which is what catches nominal register ("reprezintă" twice plus
  "constituie" once); neither feeds the score. Paronyms are now informative
  (`minor`, unscored): the detector sees co-occurrence, not meaning, and flagged
  sentences that use both words correctly. Pleonasm matching window narrowed
  80 → 25 chars so it stops crossing clause boundaries. Tests 39 → 51.
- **v0.4.0** — Agent-efficiency release. New `verifica.py` orchestrator runs all
  checks in one call with a combined deterministic score (`X/13`), `--json`
  output and `--fara-seo`. Reports now include the canonical fix inline
  (`|→ are sens`; paronyms get sense explanations), so audits no longer require
  loading the reference files. `seo-geo.md` (43KB) split into 8 topic files with
  a routing table in SKILL.md — a blog task loads ~23KB instead of 43KB. Shared
  scanning engine extracted to `_comun.py` (~150 duplicated lines removed). New
  `check-modelisme.py` for etymological pleonasms/anglicisms/paronyms, with dead
  diacritic branches and guaranteed false positives ("caut să adopt", "de aceea")
  fixed. Test suite 24 → 39: modelisme coverage, orchestrator tests, a pattern
  hygiene test (no diacritics in folded regexes) and a SKILL↔script drift guard.
- **v0.3.1** — Grounding discovery is now format-agnostic: the skill looks for business data by content across any file type, published page or prior message, rather than matching a fixed list of filenames. Adds handling for contradictory sources, and a flow for saving confirmed data back into the project's own format. No blank brief template ships on purpose — a half-filled one produces plausible-but-false data.
- **v0.3.0** — SEO/GEO refresh for 2026. Corrected deprecated structured data guidance (FAQ rich results retired May 2026, `HowTo` since 2023) and documented schema's new role as a trust/entity signal for AI Mode. Added evidence-backed GEO tactics from the Princeton/KDD 2024 study and large-corpus analyses, kept distinct from Google's official position. New Romanian-specific SEO section: diacritics in queries vs. body text vs. slugs, romgleză in keyword research, `ro-RO`/`ro-MD` targeting. New §0 on business data that must be sourced or asked for, never invented, wired into the workflow as a CONTEXT step. `check-seo.py` gained cedilla, URL-diacritic and section-length checks, and its first tests. CI on Python 3.9/3.11/3.13.
- **v0.2.0** — Three modes (rewrite/audit/edit), two-pass self-correction, voice profiles. Diacritic-insensitive and morphology-aware pattern matching (previously, text without diacritics went entirely undetected). Severity levels and density thresholds instead of binary bans. New `tipare-ro.md` covering Romanian-specific failure modes. New stylometric rhythm analyser. Test suite added.
- **v0.1.0-alpha** — Initial release. Grammar/style from 7 Romanian school manuals, writing techniques from efficiency methodology, SEO/GEO from current Google documentation.

## License

MIT
