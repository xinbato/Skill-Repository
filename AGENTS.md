# AGENTS.md

This file provides system guidance to AI coding agents (Antigravity, Claude Code, Cursor, Copilot, OpenCode, etc.) working with code in this repository.

> **Scope**: This document configures and guides agents interacting with the [`xinbato/Skill-Repository`](https://github.com/xinbato/Skill-Repository). The reusable assets for other projects are the skills located in `skills/` and the portable router [`SKILLS_MAP.md`](SKILLS_MAP.md).

---

## Repository Overview

**Skill-Repository** is a multi-agent compatible, open-standard skill repository adhering to the [agentskills.io](https://agentskills.io) specification.

### Directory Organization

Skills are organized into three primary ecosystem categories:

```text
skills/
├── general/          # Universal, synthesized, and custom meta-skills
│   ├── create-skill/
│   ├── create-skill-v2/
│   ├── git-workflow/
│   └── email-teacher/
├── anthropic/        # Document processing, UI design, art & MCP from Anthropic
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
└── openai/           # Browser automation & application security from OpenAI
    ├── playwright/
    ├── security-threat-model/
    └── security-best-practices/
```

---

## Agent Operational Protocol

### 1. Skill-Driven Execution Model
- **Scan Before Improvising**: Before performing complex operations (e.g. authoring skills, running git commits, writing office documents, web scraping), inspect the repository to see if a dedicated skill exists.
- **Intent Mapping**:
  - Scaffold / generate a new skill -> `skills/general/create-skill-v2`
  - Analyze diffs / Conventional Commits / PR -> `skills/general/git-workflow`
  - PDF manipulation -> `skills/anthropic/pdf`
  - Word (.docx) generation/editing -> `skills/anthropic/docx`
  - Excel (.xlsx) manipulation -> `skills/anthropic/xlsx`
  - PowerPoint (.pptx) creation -> `skills/anthropic/pptx`
  - Model Context Protocol (MCP) server -> `skills/anthropic/mcp-builder`
  - Local web app testing / Playwright UI -> `skills/anthropic/webapp-testing`
  - Real browser automation / terminal Playwright -> `skills/openai/playwright`
  - AppSec threat modeling (STRIDE) -> `skills/openai/security-threat-model`
  - Code vulnerability & security audit -> `skills/openai/security-best-practices`
  - Frontend visual design direction -> `skills/anthropic/frontend-design`
  - Consistent styling themes -> `skills/anthropic/theme-factory`
  - Generative algorithmic art (p5.js) -> `skills/anthropic/algorithmic-art`
  - Canvas graphics / poster generation -> `skills/anthropic/canvas-design`
  - Academic correspondence -> `skills/general/email-teacher`

### 2. Standard Compliance Rules
All skills in this repository must strictly adhere to the following rules:
- **Directory & Name Parity**: The `name` field in `SKILL.md` frontmatter must strictly match the immediate parent directory name (e.g., `skills/general/create-skill-v2/SKILL.md` must have `name: create-skill-v2`).
- **Naming Pattern**: 1-64 lowercase alphanumeric characters and single hyphens (`^[a-z0-9]+(-[a-z0-9]+)*$`).
- **Description Limit**: Concise and informative under 1024 characters, explicitly defining trigger criteria.
- **Standalone Scripts**: Python scripts in `scripts/` must include inline PEP 723 metadata headers:
  ```python
  # /// script
  # requires-python = ">=3.9"
  # dependencies = [...]
  # ///
  ```
- **Evaluation Suites**: Every skill must include an `evals/evals.json` file defining test prompts and evaluation criteria.

---

## Adding or Updating Skills

When contributing or refactoring skills in this repository:
1. Target the correct ecosystem directory:
   - `skills/anthropic/` for skills maintained by or originating from Anthropic.
   - `skills/openai/` for skills maintained by or originating from OpenAI.
   - `skills/general/` for custom skills, community contributions, or universal tooling.
2. Initialize with `create-skill-v2`:
   ```bash
   python skills/general/create-skill-v2/scripts/init_skill.py \
     --name "<skill-name>" \
     --description "<trigger-description>" \
     --dest "skills/<category>"
   ```
3. Update both [`SKILLS_MAP.md`](SKILLS_MAP.md) and [`README.md`](README.md) to register the new skill and its direct Raw URL.
