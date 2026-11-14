# Skill-Repository

> A standardized, portable hub of production-ready AI Agent Skills and engineering workflows.  
> Built according to the open [agentskills.io](https://agentskills.io) and [agent-plugins.org](https://agent-plugins.org) specifications.

[![Standard: agentskills.io](https://img.shields.io/badge/Standard-agentskills.io-blue.svg)](https://agentskills.io)
[![Standard: agent-plugins.org](https://img.shields.io/badge/Plugin-agent--plugins.org-purple.svg)](https://agent-plugins.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/xinbato/Skill-Repository?style=social)](https://github.com/xinbato/Skill-Repository)

---

## Overview

**Skill-Repository** is a centralized library of reusable, version-controlled **Agent Skills**, **Personas**, and **Lifecycle Commands**. It encapsulates procedural engineering knowledge, executable scripts, and reference documentation into a clean format that any AI Agent (Claude Code, Cursor, Antigravity, OpenHands, Copilot, Codex, etc.) can discover and execute.

### Key Highlights
- **Full Engineering Lifecycle (SDLC)**: Covers requirements extraction (`interview-me`), specification (`spec-driven-development`), planning (`planning-and-task-breakdown`), test-driven implementation (`test-driven-development`), 5-axis review (`code-review-and-quality`), and shipping (`shipping-and-launch`).
- **Zero-Bloat Progressive Disclosure**: Agents load skills in 3 stages (*Discovery* -> *Activation* -> *Execution*), preserving context tokens.
- **The Portable Map (`SKILLS_MAP.md`)**: Drop `SKILLS_MAP.md` into any project, and your AI Agent will discover and pull skills from GitHub on demand.
- **Three-Tier Architecture**: Clean separation between **Skills** (*How*), **Personas** (*Who*), and **Commands** (*When*).
- **Universal Multi-Agent Compatibility**: Native adapters and manifests for Claude Code (`.claude/`), Gemini CLI / Antigravity (`.gemini/`), Codex (`.codex-plugin/`), and generic agents (`.agents/`).

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
├── .claude/                          # Claude Code adapter (commands & rules)
├── .gemini/                          # Gemini CLI / Antigravity adapter
├── .codex-plugin/                    # OpenAI Codex adapter
├── plugin.json                       # Agent Plugins standard manifest
├── AGENTS.md                         # Agent instructions and system navigation guide
├── SKILLS_MAP.md                     # Portable dynamic router for AI agents
├── README.md                         # Repository documentation and guide
├── LICENSE                           # Open source MIT license
├── agents/                           # Expert personas for multi-agent workflows
│   ├── code-reviewer.md
│   ├── security-auditor.md
│   ├── test-engineer.md
│   └── web-performance-auditor.md
├── commands/                         # Lifecycle slash commands
│   ├── spec.toml
│   ├── plan.toml
│   ├── build.toml
│   ├── test.toml
│   ├── review.toml
│   ├── code-simplify.toml
│   └── ship.toml
├── references/                       # Shared authoritative engineering checklists
│   ├── definition-of-done.md
│   ├── orchestration-patterns.md
│   ├── security-checklist.md
│   ├── performance-checklist.md
│   ├── testing-patterns.md
│   └── accessibility-checklist.md
├── docs/                             # Platform setup and anatomy guides
│   ├── skill-anatomy.md
│   ├── antigravity-setup.md
│   ├── cursor-setup.md
│   ├── claude-code-setup.md
│   └── codex-setup.md
├── scripts/                          # Automated quality gates and linters
│   ├── validate_skills.py
│   ├── validate-skills.js
│   ├── validate-commands.js
│   └── validate-reference-links.js
└── skills/
    ├── general/                      # SDLC discipline, meta-skills & custom tooling
    │   ├── create-skill/
    │   ├── create-skill-v2/
    │   ├── git-workflow/
    │   ├── email-teacher/
    │   ├── interview-me/
    │   ├── spec-driven-development/
    │   ├── planning-and-task-breakdown/
    │   ├── incremental-implementation/
    │   ├── test-driven-development/
    │   ├── debugging-and-error-recovery/
    │   ├── code-review-and-quality/
    │   ├── code-simplification/
    │   ├── source-driven-development/
    │   └── shipping-and-launch/
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

## Lifecycle Commands

Pre-configured slash commands for the development lifecycle:

| Lifecycle Phase | Command | Description |
| :--- | :--- | :--- |
| **DEFINE** | `/spec` | Extracts intent and drafts specification PRD before coding. |
| **PLAN** | `/plan` | Breaks requirements into small, ordered, atomic tasks. |
| **BUILD** | `/build` | Builds incrementally one thin slice at a time. |
| **VERIFY** | `/test` | Enforces test-driven development (Red-Green-Refactor). |
| **REVIEW** | `/review` | Conducts 5-axis code review (Correctness, Readability, Architecture, Security, Performance). |
| **SIMPLIFY** | `/code-simplify` | Refactors for maximum clarity without behavioral changes. |
| **SHIP** | `/ship` | Synthesizes persona reports and verifies pre-launch gates. |

---

## Available Skills

### General & Engineering Lifecycle (`skills/general/`)

| Skill | Description | Category | Link |
| :--- | :--- | :--- | :--- |
| **[`interview-me`](skills/general/interview-me/)** | Extracts underlying user intent through one-question-at-a-time interview before spec or code. | Requirements & Discovery | [Explore](skills/general/interview-me/SKILL.md) |
| **[`spec-driven-development`](skills/general/spec-driven-development/)** | Creates PRD and requirements specification with clear acceptance criteria before coding. | Requirements & PRD | [Explore](skills/general/spec-driven-development/SKILL.md) |
| **[`planning-and-task-breakdown`](skills/general/planning-and-task-breakdown/)** | Breaks specifications into ordered, atomic tasks optimized for context efficiency. | Planning & Tasks | [Explore](skills/general/planning-and-task-breakdown/SKILL.md) |
| **[`incremental-implementation`](skills/general/incremental-implementation/)** | Delivers changes incrementally in thin, verifiable slices with frequent commits. | Implementation | [Explore](skills/general/incremental-implementation/SKILL.md) |
| **[`test-driven-development`](skills/general/test-driven-development/)** | Drives development with tests using the red-green-refactor loop. | Testing & Quality | [Explore](skills/general/test-driven-development/SKILL.md) |
| **[`debugging-and-error-recovery`](skills/general/debugging-and-error-recovery/)** | Systematic root-cause debugging: reproduce, isolate, fix, and verify without guessing. | Debugging & Diagnostics | [Explore](skills/general/debugging-and-error-recovery/SKILL.md) |
| **[`code-review-and-quality`](skills/general/code-review-and-quality/)** | Multi-axis code review evaluating correctness, readability, architecture, security, performance. | Code Review & QA | [Explore](skills/general/code-review-and-quality/SKILL.md) |
| **[`code-simplification`](skills/general/code-simplification/)** | Simplifies code for maximum clarity and reduces complexity without breaking behavior. | Refactoring | [Explore](skills/general/code-simplification/SKILL.md) |
| **[`source-driven-development`](skills/general/source-driven-development/)** | Grounds implementation decisions in official framework documentation and source code. | Architecture & Grounding | [Explore](skills/general/source-driven-development/SKILL.md) |
| **[`shipping-and-launch`](skills/general/shipping-and-launch/)** | Prepares production releases with deployment checklists, migration plans, and rollback gates. | Release & Operations | [Explore](skills/general/shipping-and-launch/SKILL.md) |
| **[`create-skill-v2`](skills/general/create-skill-v2/)** | Next-gen skill generator with dynamic templates, Windows-safe eval runner, and HTML reports. | Developer Tooling | [Explore](skills/general/create-skill-v2/SKILL.md) |
| **[`create-skill`](skills/general/create-skill/)** | Scaffolds standard-compliant Agent Skills with directory structure, metadata, and scripts. | Developer Tooling | [Explore](skills/general/create-skill/SKILL.md) |
| **[`git-workflow`](skills/general/git-workflow/)** | Analyzes git diffs, enforces Conventional Commits, prevents secret leaks, and prepares PRs. | Version Control / DevOps | [Explore](skills/general/git-workflow/SKILL.md) |
| **[`email-teacher`](skills/general/email-teacher/)** | Drafts respectful, academic-grade correspondence to professors for leaves and extensions. | Academic / Communication | [Explore](skills/general/email-teacher/SKILL.md) |

### Anthropic Ecosystem (`skills/anthropic/`)

| Skill | Description | Category | Link |
| :--- | :--- | :--- | :--- |
| **[`pdf`](skills/anthropic/pdf/)** | Comprehensive PDF manipulation: extract text/tables, merge, split, rotate, watermark, OCR, fill forms. | Document Processing | [Explore](skills/anthropic/pdf/SKILL.md) |
| **[`docx`](skills/anthropic/docx/)** | Creates, reads, edits, and formats Word documents (.docx/.dotx) with tables and styled templates. | Document Processing | [Explore](skills/anthropic/docx/SKILL.md) |
| **[`xlsx`](skills/anthropic/xlsx/)** | Reads, edits, recalculates formulas, cleans messy data, and formats Excel spreadsheets (.xlsx/.csv). | Data & Spreadsheets | [Explore](skills/anthropic/xlsx/SKILL.md) |
| **[`pptx`](skills/anthropic/pptx/)** | Generates, parses, edits slide decks, pitch decks, layouts, and speaker notes for PowerPoint (.pptx). | Presentation / Office | [Explore](skills/anthropic/pptx/SKILL.md) |
| **[`mcp-builder`](skills/anthropic/mcp-builder/)** | Guides building Model Context Protocol (MCP) servers using FastMCP (Python) or TypeScript SDK. | AI Engineering / MCP | [Explore](skills/anthropic/mcp-builder/SKILL.md) |
| **[`webapp-testing`](skills/anthropic/webapp-testing/)** | Tests local web applications using Playwright, verifying UI behavior and capturing screenshots. | Testing & Automation | [Explore](skills/anthropic/webapp-testing/SKILL.md) |
| **[`frontend-design`](skills/anthropic/frontend-design/)** | Provides intentional aesthetic direction, typography scale, and cohesive palettes. | UI/UX & Design | [Explore](skills/anthropic/frontend-design/SKILL.md) |
| **[`theme-factory`](skills/anthropic/theme-factory/)** | Styles artifacts, slides, reports, and HTML pages with 10 pre-set designer themes. | UI/UX & Design | [Explore](skills/anthropic/theme-factory/SKILL.md) |
| **[`algorithmic-art`](skills/anthropic/algorithmic-art/)** | Generates interactive algorithmic art using p5.js, flow fields, and seeded randomness. | Creative & Art | [Explore](skills/anthropic/algorithmic-art/SKILL.md) |
| **[`canvas-design`](skills/anthropic/canvas-design/)** | Creates posters and visual documents exported to PNG/PDF adhering to strict grid principles. | Creative & Art | [Explore](skills/anthropic/canvas-design/SKILL.md) |

### OpenAI Ecosystem (`skills/openai/`)

| Skill | Description | Category | Link |
| :--- | :--- | :--- | :--- |
| **[`playwright`](skills/openai/playwright/)** | Automates real browsers from terminal: navigation, form filling, snapshots, screenshots, and scraping. | Testing & Automation | [Explore](skills/openai/playwright/SKILL.md) |
| **[`security-threat-model`](skills/openai/security-threat-model/)** | Grounded AppSec threat modeling: enumerates trust boundaries, assets, attacker capabilities, mitigations. | Security | [Explore](skills/openai/security-threat-model/SKILL.md) |
| **[`security-best-practices`](skills/openai/security-best-practices/)** | Reviews code for language and framework security best practices (SQLi, XSS, tokens) with fix diffs. | Security | [Explore](skills/openai/security-best-practices/SKILL.md) |

---

## How to Use

### Method 1: The Portable Map Mode (Recommended)
In any project workspace:
1. Download [`SKILLS_MAP.md`](SKILLS_MAP.md) into your project root.
2. Tell your AI Agent: *"Read `SKILLS_MAP.md` and use the relevant skills to solve my task."*
3. The Agent will scan the catalog, fetch the required skill into `.agents/skills/`, and execute it.

### Method 2: Plugin Mode (Claude Code / Codex / Antigravity)
Install as a native plugin:
```bash
# In Claude Code
/plugin install xinbato-skills@skill-repository
```

### Method 3: Full Repository Clone
```bash
git clone https://github.com/xinbato/Skill-Repository.git
cd Skill-Repository
```

---

## License

This project is licensed under the [MIT License](LICENSE).
Open standard compliant with [agentskills.io](https://agentskills.io) and [agent-plugins.org](https://agent-plugins.org).
