# Skill-Repository

> A standardized, portable hub of production-ready AI Agent Skills.  
> Built according to the open [agentskills.io](https://agentskills.io) specification.

[![Standard: agentskills.io](https://img.shields.io/badge/Standard-agentskills.io-blue.svg)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/xinbato/Skill-Repository?style=social)](https://github.com/xinbato/Skill-Repository)

---

## Overview

**Skill-Repository** is a centralized library of reusable, version-controlled **Agent Skills**. Each skill encapsulates procedural knowledge, executable scripts, and reference documentation into a clean, portable format that any AI Agent (Cursor, Claude Code, Antigravity, OpenHands, Copilot, etc.) can discover and execute.

### Key Highlights
- **Zero-Bloat Progressive Disclosure**: Agents load skills in 3 stages (*Discovery* -> *Activation* -> *Execution*), preserving context tokens.
- **The Portable Map (`SKILLS_MAP.md`)**: You do not need to clone the entire repository. Simply drop `SKILLS_MAP.md` into any project, and your AI Agent will automatically discover and pull skills from GitHub on demand.
- **Universal Compatibility**: Follows cross-client conventions (`.agents/skills/`) compatible across Windows, macOS, and Linux.

---

## Architecture

```
                      +----------------------------------------------+
                      |   GitHub: xinbato/Skill-Repository           |
                      |   (Central Skills Hub)                       |
                      +----------------------+-----------------------+
                                             |
                      +----------------------v-----------------------+
                      |              SKILLS_MAP.md                   |
                      |   (Lightweight Router / Index File)          |
                      +----------------------+-----------------------+
                                             |
           +---------------------------------+---------------------------------+
           |                                                                   |
           v                                                                   v
+-------------------------------+                                   +-------------------------------+
|     Project A (Local PC)      |                                   |     Project B (Remote Server) |
|  - Has: SKILLS_MAP.md         |                                   |  - Has: SKILLS_MAP.md         |
|  - Agent reads map            |                                   |  - Agent reads map            |
|  - Pulls into .agents/skills/ |                                   |  - Pulls into .agents/skills/ |
+-------------------------------+                                   +-------------------------------+
```

---

## Repository Structure

```text
Skill-Repository/
├── SKILLS_MAP.md                     # Portable dynamic router for AI agents
├── README.md                         # Repository documentation and guide
├── LICENSE                           # Open source MIT license
└── skills/                           # Collection of Agent Skills
    ├── create-skill/                 # Meta-skill to scaffold and test new skills
    ├── git-workflow/                 # Git operations and Conventional Commits helper
    ├── email-teacher/                # Academic correspondence for students
    ├── pdf/                          # PDF document reading, splitting, merging, and forms
    ├── docx/                         # Word document creation, editing, and formatting
    ├── xlsx/                         # Excel spreadsheet manipulation and data cleaning
    ├── pptx/                         # PowerPoint slide deck generation and editing
    ├── mcp-builder/                  # Model Context Protocol server development
    ├── playwright/                   # Browser automation, navigation, and web scraping
    ├── webapp-testing/               # Local web application testing and screenshot capture
    ├── security-threat-model/        # Codebase-grounded AppSec threat modeling (STRIDE)
    ├── security-best-practices/      # Language and framework security vulnerability review
    ├── frontend-design/              # Distinctive UI/UX aesthetic, typography, and color guidance
    ├── theme-factory/                # Preset styling themes for web, slides, and reports
    ├── algorithmic-art/              # Interactive generative art using p5.js
    └── canvas-design/                # Visual poster and document canvas design to PNG/PDF
```

---

## How to Use

### Method 1: The Portable Map Mode (Recommended)
You do not need to clone this repository. In any project workspace:
1. Download only the [`SKILLS_MAP.md`](SKILLS_MAP.md) file into your project root.
2. In your prompt to your AI Agent, mention:
   > "Read `SKILLS_MAP.md` and use the relevant skills to solve my task."
3. The Agent will scan the catalog, fetch the required skill from GitHub into `.agents/skills/`, and execute it seamlessly.

### Method 2: Full Repository Clone
If you want all skills stored locally:
```bash
git clone https://github.com/xinbato/Skill-Repository.git
cd Skill-Repository
```

### Method 3: Selective Skill Download (Sparse Checkout)
If you only need a single skill (e.g., `create-skill`):
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/xinbato/Skill-Repository.git my-skills
cd my-skills
git sparse-checkout set skills/create-skill
```

---

## Available Skills

| Skill | Description | Category | Link |
| :--- | :--- | :--- | :--- |
| **[`create-skill`](skills/create-skill/)** | Generates standard-compliant Agent Skills with directory structures, metadata, scripts, evals, and references. | Developer Tooling | [Explore](skills/create-skill/SKILL.md) |
| **[`git-workflow`](skills/git-workflow/)** | Analyzes git diffs, enforces Conventional Commits (`feat:`, `fix:`, etc.), prevents secret leaks, and prepares PRs. | Version Control / DevOps | [Explore](skills/git-workflow/SKILL.md) |
| **[`email-teacher`](skills/email-teacher/)** | Drafts respectful, academic-grade correspondence to professors and teachers for leaves, extensions, and questions. | Academic / Communication | [Explore](skills/email-teacher/SKILL.md) |
| **[`pdf`](skills/pdf/)** | Comprehensive PDF manipulation: extract text/tables, merge, split, rotate, watermark, OCR, and fill forms. | Document Processing | [Explore](skills/pdf/SKILL.md) |
| **[`docx`](skills/docx/)** | Creates, reads, edits, and formats Word documents (.docx/.dotx) with tables of contents, styled tables, and images. | Document Processing | [Explore](skills/docx/SKILL.md) |
| **[`xlsx`](skills/xlsx/)** | Reads, edits, recalculates formulas, cleans messy tabular data, and formats Excel spreadsheets (.xlsx/.csv). | Data & Spreadsheets | [Explore](skills/xlsx/SKILL.md) |
| **[`pptx`](skills/pptx/)** | Generates, parses, edits slide decks, pitch decks, layouts, and speaker notes for PowerPoint (.pptx/.potx). | Presentation / Office | [Explore](skills/pptx/SKILL.md) |
| **[`mcp-builder`](skills/mcp-builder/)** | Guides building high-quality Model Context Protocol (MCP) servers using FastMCP (Python) or TypeScript SDK. | AI Engineering / MCP | [Explore](skills/mcp-builder/SKILL.md) |
| **[`playwright`](skills/playwright/)** | Automates real browsers from terminal: navigation, form filling, snapshots, screenshots, and scraping. | Testing & Automation | [Explore](skills/playwright/SKILL.md) |
| **[`webapp-testing`](skills/webapp-testing/)** | Tests local web applications using Playwright, verifying frontend behavior and capturing debug screenshots. | Testing & Automation | [Explore](skills/webapp-testing/SKILL.md) |
| **[`security-threat-model`](skills/security-threat-model/)** | Grounded AppSec threat modeling: enumerates trust boundaries, assets, attacker capabilities, and mitigations. | Security | [Explore](skills/security-threat-model/SKILL.md) |
| **[`security-best-practices`](skills/security-best-practices/)** | Reviews code for language and framework security best practices (SQLi, XSS, tokens) with remediation diffs. | Security | [Explore](skills/security-best-practices/SKILL.md) |
| **[`frontend-design`](skills/frontend-design/)** | Provides intentional aesthetic direction, typography scale, and cohesive palettes avoiding generic AI styles. | UI/UX & Design | [Explore](skills/frontend-design/SKILL.md) |
| **[`theme-factory`](skills/theme-factory/)** | Styles artifacts, slides, reports, and HTML pages with 10 pre-set designer themes (colors and fonts). | UI/UX & Design | [Explore](skills/theme-factory/SKILL.md) |
| **[`algorithmic-art`](skills/algorithmic-art/)** | Generates interactive algorithmic art using p5.js, flow fields, and seeded randomness. | Creative & Art | [Explore](skills/algorithmic-art/SKILL.md) |
| **[`canvas-design`](skills/canvas-design/)** | Creates posters and visual documents exported to PNG/PDF adhering to strict grid and typography principles. | Creative & Art | [Explore](skills/canvas-design/SKILL.md) |

---

## Deep Dive: `create-skill`

The foundational skill in this repository is **`create-skill`** — a meta-skill designed to build new skills.

### What it does:
- Validates skill naming (`kebab-case`, 1-64 chars, no consecutive hyphens).
- Sets up standard subdirectories: `scripts/`, `references/`, `assets/`, `evals/`.
- Authors valid YAML frontmatter optimized for the **Discovery** stage.
- Includes `scripts/init_skill.py` to automate folder generation.

### CLI Usage:
```bash
python skills/create-skill/scripts/init_skill.py \
  --name "pdf-parser" \
  --description "Extracts tabular data and text from PDF documents. Trigger when user uploads or mentions PDF analysis." \
  --dest "skills"
```

---

## Contributing New Skills

1. Fork this repository: `https://github.com/xinbato/Skill-Repository`.
2. Use `create-skill` to scaffold your new skill:
   ```bash
   python skills/create-skill/scripts/init_skill.py --name "your-skill-name" --description "Clear trigger description" --dest "skills"
   ```
3. Implement instructions in `skills/<your-skill-name>/SKILL.md`.
4. Add helper scripts into `scripts/`, reference guides into `references/`, and evaluation queries into `evals/`.
5. Register your new skill in [`SKILLS_MAP.md`](SKILLS_MAP.md).
6. Submit a Pull Request.

---

## License

This project is licensed under the [MIT License](LICENSE).
Open standard compliant with [agentskills.io](https://agentskills.io).
