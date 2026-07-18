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
│   │   ├── tipare-ro.md            # Romanian-specific failure modes
│   │   ├── gramatica-stil.md       # Agreement, punctuation, spelling, pleonasms
│   │   ├── scris-eficient.md       # Process techniques: draft/edit, rhythm, concision
│   │   └── scoring-checklist.md    # 1-10 rubric, language criteria (1-3)
│   └── seo/
│       ├── seo-geo.md              # SEO technical/on-page/e-commerce/blog/local + GEO
│       └── scoring-checklist.md    # 1-10 rubric, SEO criteria (4-5)
├── scripts/
│   ├── check-tipare.py             # AI clichés, calques, generation artefacts
│   ├── check-ritm.py               # Sentence/paragraph uniformity (stylometry)
│   └── check-seo.py                # Headings and keyword stuffing
└── tests/                          # Fixtures + unittest suite (stdlib only)
```

## Verification scripts

```bash
python3 scripts/check-tipare.py <file>     # AI clichés and calques
python3 scripts/check-ritm.py <file>       # rhythm uniformity
python3 scripts/check-seo.py <file>        # SEO structure

python3 scripts/check-tipare.py <file> --scor   # signal score only
python3 scripts/check-tipare.py <file> --prag 8 # occurrences per 1000 words
python3 scripts/check-tipare.py <file> --tot    # include sub-threshold matches
```

Exit 0 = clean, 1 = issues found, 2 = input error. Use `--help` for details.

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

- **v0.3.1** — Grounding discovery is now format-agnostic: the skill looks for business data by content across any file type, published page or prior message, rather than matching a fixed list of filenames. Adds handling for contradictory sources, and a flow for saving confirmed data back into the project's own format. No blank brief template ships on purpose — a half-filled one produces plausible-but-false data.
- **v0.3.0** — SEO/GEO refresh for 2026. Corrected deprecated structured data guidance (FAQ rich results retired May 2026, `HowTo` since 2023) and documented schema's new role as a trust/entity signal for AI Mode. Added evidence-backed GEO tactics from the Princeton/KDD 2024 study and large-corpus analyses, kept distinct from Google's official position. New Romanian-specific SEO section: diacritics in queries vs. body text vs. slugs, romgleză in keyword research, `ro-RO`/`ro-MD` targeting. New §0 on business data that must be sourced or asked for, never invented, wired into the workflow as a CONTEXT step. `check-seo.py` gained cedilla, URL-diacritic and section-length checks, and its first tests. CI on Python 3.9/3.11/3.13.
- **v0.2.0** — Three modes (rewrite/audit/edit), two-pass self-correction, voice profiles. Diacritic-insensitive and morphology-aware pattern matching (previously, text without diacritics went entirely undetected). Severity levels and density thresholds instead of binary bans. New `tipare-ro.md` covering Romanian-specific failure modes. New stylometric rhythm analyser. Test suite added.
- **v0.1.0-alpha** — Initial release. Grammar/style from 7 Romanian school manuals, writing techniques from efficiency methodology, SEO/GEO from current Google documentation.

## License

MIT
