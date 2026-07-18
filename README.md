# Scrie Românește

> Skill pentru generarea și revizuirea de text în limba română care sună natural și uman, nu ca text produs de un model lingvistic.

**Author:** Dan Mutu — [adcelerum.ro](https://adcelerum.ro)

## What it does

Combines Romanian language rules (grammar, style, anti-AI patterns) with SEO/GEO optimization — so one doesn't break the other. Use it whenever you need to write, rewrite, edit, or review text in Romanian: articles, product descriptions, web pages, blog content, social posts.

### Key features

- **Anti-AI patterns** — catches mechanical transitions ("în concluzie", "prin urmare"), corporate jargon, hedging, Romgleză (Romanian-English calques)
- **Grammar & style** — punctuation, agreement, spelling, diathesis, language registers, common mistakes (400+ rules extracted from Romanian school manuals)
- **Writing techniques** — rhythm, conciseness, structure, audience calibration (230+ lines from writing methodology)
- **SEO/GEO** — on-page, technical, e-commerce, local, keyword research, structured data, AI optimization for generative search (460+ rules from current Google documentation)
- **Verification scripts** — `check-tipare.py` (pattern scanner) and `check-seo.py` (heading/keyword checks)

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
│   │   ├── anti-tipare-ai.md       # AI clichés, Romgleză, tone — check always
│   │   ├── gramatica-stil.md       # Agreement, punctuation, spelling, pleonasms
│   │   ├── scris-eficient.md       # Process techniques: draft/edit, rhythm, concision
│   │   └── scoring-checklist.md    # 1-10 rubric, language criteria (1-3)
│   └── seo/
│       ├── seo-geo.md              # SEO technical/on-page/e-commerce/blog/local + GEO
│       └── scoring-checklist.md    # 1-10 rubric, SEO criteria (4-5)
└── scripts/
    ├── check-tipare.py             # Scan text for AI clichés
    └── check-seo.py                # Check headings and keyword stuffing
```

## Verification scripts

```bash
# Scan a file for AI patterns
python3 scripts/check-tipare.py <file>

# Check SEO structure
python3 scripts/check-seo.py <file>
```

Exit 0 = clean, exit 1 = issues found. Use `--help` for details.

## Version

- **v0.1.0-alpha** — Initial release. Grammar/style from 7 Romanian school manuals, writing techniques from efficiency methodology, SEO/GEO from current Google documentation.

## License

MIT
