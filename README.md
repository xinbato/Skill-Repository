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
- **Multi-Ecosystem Categorization**: Skills are organized cleanly by source ecosystem (`anthropic/`, `openai/`) alongside a dedicated section for universal synthesized and custom skills (`general/`).
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
├── AGENTS.md                         # Agent instructions and system navigation guide
├── SKILLS_MAP.md                     # Portable dynamic router for AI agents
├── README.md                         # Repository documentation and guide
├── LICENSE                           # Open source MIT license
└── skills/
    ├── general/                      # Custom, community, and universal skills
    │   ├── create-skill/
    │   ├── create-skill-v2/
    │   ├── git-workflow/
    │   └── email-teacher/
    ├── anthropic/                    # Document processing, UI design, art & MCP
    │   ├── pdf/
    │   ├── docx/
    │   ├── xlsx/
    │   ├── pptx/
    │   ├── mcp-builder/
    │   ├── webapp-testing/
    │   ├── frontend-design/
    │   ├── theme-factory/
    │   ├── algorithmic-art/
    │   └── canvas-design/
    └── openai/                       # Browser automation & application security
        ├── playwright/
        ├── security-threat-model/
        └── security-best-practices/
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
If you only need a single skill (e.g., `create-skill-v2`):
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/xinbato/Skill-Repository.git my-skills
cd my-skills
git sparse-checkout set skills/general/create-skill-v2
```

---

## Available Skills

### General & Synthesized (`skills/general/`)

| Skill | Description | Category | Link |
| :--- | :--- | :--- | :--- |
| **[`create-skill-v2`](skills/general/create-skill-v2/)** | Next-gen skill generator with dynamic templates, Windows-safe eval runner (`run_eval.py`), and HTML reports. | Developer Tooling | [Explore](skills/general/create-skill-v2/SKILL.md) |
| **[`create-skill`](skills/general/create-skill/)** | Generates standard-compliant Agent Skills with directory structures, metadata, scripts, evals, and references. | Developer Tooling | [Explore](skills/general/create-skill/SKILL.md) |
| **[`git-workflow`](skills/general/git-workflow/)** | Analyzes git diffs, enforces Conventional Commits (`feat:`, `fix:`, etc.), prevents secret leaks, and prepares PRs. | Version Control / DevOps | [Explore](skills/general/git-workflow/SKILL.md) |
| **[`email-teacher`](skills/general/email-teacher/)** | Drafts respectful, academic-grade correspondence to professors and teachers for leaves, extensions, and questions. | Academic / Communication | [Explore](skills/general/email-teacher/SKILL.md) |

### Anthropic Ecosystem (`skills/anthropic/`)

| Skill | Description | Category | Link |
| :--- | :--- | :--- | :--- |
| **[`pdf`](skills/anthropic/pdf/)** | Comprehensive PDF manipulation: extract text/tables, merge, split, rotate, watermark, OCR, and fill forms. | Document Processing | [Explore](skills/anthropic/pdf/SKILL.md) |
| **[`docx`](skills/anthropic/docx/)** | Creates, reads, edits, and formats Word documents (.docx/.dotx) with tables of contents, styled tables, and images. | Document Processing | [Explore](skills/anthropic/docx/SKILL.md) |
| **[`xlsx`](skills/anthropic/xlsx/)** | Reads, edits, recalculates formulas, cleans messy tabular data, and formats Excel spreadsheets (.xlsx/.csv). | Data & Spreadsheets | [Explore](skills/anthropic/xlsx/SKILL.md) |
| **[`pptx`](skills/anthropic/pptx/)** | Generates, parses, edits slide decks, pitch decks, layouts, and speaker notes for PowerPoint (.pptx/.potx). | Presentation / Office | [Explore](skills/anthropic/pptx/SKILL.md) |
| **[`mcp-builder`](skills/anthropic/mcp-builder/)** | Guides building high-quality Model Context Protocol (MCP) servers using FastMCP (Python) or TypeScript SDK. | AI Engineering / MCP | [Explore](skills/anthropic/mcp-builder/SKILL.md) |
| **[`webapp-testing`](skills/anthropic/webapp-testing/)** | Tests local web applications using Playwright, verifying frontend behavior and capturing debug screenshots. | Testing & Automation | [Explore](skills/anthropic/webapp-testing/SKILL.md) |
| **[`frontend-design`](skills/anthropic/frontend-design/)** | Provides intentional aesthetic direction, typography scale, and cohesive palettes avoiding generic AI styles. | UI/UX & Design | [Explore](skills/anthropic/frontend-design/SKILL.md) |
| **[`theme-factory`](skills/anthropic/theme-factory/)** | Styles artifacts, slides, reports, and HTML pages with 10 pre-set designer themes (colors and fonts). | UI/UX & Design | [Explore](skills/anthropic/theme-factory/SKILL.md) |
| **[`algorithmic-art`](skills/anthropic/algorithmic-art/)** | Generates interactive algorithmic art using p5.js, flow fields, and seeded randomness. | Creative & Art | [Explore](skills/anthropic/algorithmic-art/SKILL.md) |
| **[`canvas-design`](skills/anthropic/canvas-design/)** | Creates posters and visual documents exported to PNG/PDF adhering to strict grid and typography principles. | Creative & Art | [Explore](skills/anthropic/canvas-design/SKILL.md) |

### OpenAI Ecosystem (`skills/openai/`)

| Skill | Description | Category | Link |
| :--- | :--- | :--- | :--- |
| **[`playwright`](skills/openai/playwright/)** | Automates real browsers from terminal: navigation, form filling, snapshots, screenshots, and scraping. | Testing & Automation | [Explore](skills/openai/playwright/SKILL.md) |
| **[`security-threat-model`](skills/openai/security-threat-model/)** | Grounded AppSec threat modeling: enumerates trust boundaries, assets, attacker capabilities, and mitigations. | Security | [Explore](skills/openai/security-threat-model/SKILL.md) |
| **[`security-best-practices`](skills/openai/security-best-practices/)** | Reviews code for language and framework security best practices (SQLi, XSS, tokens) with remediation diffs. | Security | [Explore](skills/openai/security-best-practices/SKILL.md) |

---

## Deep Dive: `create-skill-v2`

The flagship meta-skill in this repository is **`create-skill-v2`** — designed to build, evaluate, and optimize standard-compliant Agent Skills.

### Key Enhancements over v1:
- **Dynamic Asset Templates**: Replaces hardcoded strings by dynamically loading from `assets/template_*`.
- **Windows-Safe Evaluation Runner (`scripts/run_eval.py`)**: Runs evaluation suites cross-platform without Unix-only pipe issues (`WinError 10038`).
- **Interactive Visual Reporting (`scripts/generate_report.py`)**: Generates standalone HTML dashboards from `grading.json`.
- **Dry-run Support**: Preview planned directory structures before writing (`--dry-run`).

### CLI Usage:
```bash
python skills/general/create-skill-v2/scripts/init_skill.py \
  --name "pdf-parser" \
  --description "Extracts tabular data and text from PDF documents. Trigger when user uploads or mentions PDF analysis." \
  --dest "skills/general"
```

---

## Contributing New Skills

1. Fork this repository: `https://github.com/xinbato/Skill-Repository`.
2. Use `create-skill-v2` to scaffold your new skill into its target directory:
   ```bash
   python skills/general/create-skill-v2/scripts/init_skill.py \
     --name "your-skill-name" \
     --description "Clear trigger description" \
     --dest "skills/general"
   ```
3. Implement instructions in `skills/<ecosystem>/<your-skill-name>/SKILL.md`.
4. Add helper scripts into `scripts/`, reference guides into `references/`, and evaluation queries into `evals/`.
5. Register your new skill in [`SKILLS_MAP.md`](SKILLS_MAP.md).
6. Submit a Pull Request.

---

## License

This project is licensed under the [MIT License](LICENSE).
Open standard compliant with [agentskills.io](https://agentskills.io).
