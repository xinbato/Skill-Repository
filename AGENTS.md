# AGENTS.md

This file provides system guidance to AI coding agents (Antigravity, Claude Code, Cursor, Copilot, OpenCode, Codex, etc.) working with code in this repository.

> **Scope**: This document configures and guides agents interacting with the [`xinbato/Skill-Repository`](https://github.com/xinbato/Skill-Repository). The reusable assets for other projects are the skills located in `skills/`, personas in `agents/`, commands in `commands/`, checklists in `references/`, and the portable router [`SKILLS_MAP.md`](SKILLS_MAP.md).

---

## Repository Overview

**Skill-Repository** is a multi-agent compatible, open-standard skill repository adhering to the [agentskills.io](https://agentskills.io) and [agent-plugins.org](https://agent-plugins.org) specifications.

### Directory Organization

Skills are organized into four primary ecosystem categories:

```text
skills/
├── general/          # Universal engineering lifecycle, meta-skills & custom tooling
├── anthropic/        # Document processing, UI design, art & MCP from Anthropic
├── openai/           # Browser automation & application security from OpenAI
└── google/           # Cloud infrastructure, Gemini API, BigQuery & developer tools from Google
```

> **Note**: For the complete, dynamically updated catalog of all individual skills and fetch URLs, consult [`SKILLS_MAP.md`](SKILLS_MAP.md).

---

## Agent Operational Protocol

### 1. Skill-Driven Execution Model
- **Scan Before Improvising**: Before performing complex operations, inspect the repository to see if a dedicated skill exists.
- **Intent Mapping**:
  - Underspecified requirements / need discovery -> `skills/general/interview-me`
  - Write feature specification / PRD -> `skills/general/spec-driven-development`
  - Break down spec into atomic tasks -> `skills/general/planning-and-task-breakdown`
  - Incremental code delivery (thin slices) -> `skills/general/incremental-implementation`
  - Write tests / enforce TDD -> `skills/general/test-driven-development`
  - Bug investigation & root cause fix -> `skills/general/debugging-and-error-recovery`
  - Code review across 5 dimensions -> `skills/general/code-review-and-quality`
  - Code refactoring & simplification -> `skills/general/code-simplification`
  - Verify against official docs & source -> `skills/general/source-driven-development`
  - Production release readiness & checklist -> `skills/general/shipping-and-launch`
  - Discover & install open ecosystem skills -> `skills/general/find-skills`
  - Scaffold / generate a new skill -> `skills/general/create-skill-v2`
  - Git commits / Conventional Commits / PR -> `skills/general/git-workflow`
  - Academic & professional correspondence -> `skills/general/email-teacher`
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

### 2. Multi-Agent Orchestration & Personas
- **The Governing Rule**: The user (or slash command) is the orchestrator. **Personas do not invoke other personas.** Skills are mandatory hops inside a persona's workflow.
- **Endorsed Multi-Agent Pattern**: **Parallel Fan-out with Merge** (e.g., `/ship` invokes `code-reviewer`, `security-auditor`, and `test-engineer` concurrently and merges their findings into an actionable decision).
- **Available Personas**:
  - `agents/code-reviewer.md`: Staff engineer conducting 5-axis code review.
  - `agents/security-auditor.md`: AppSec specialist checking trust boundaries, auth, input validation.
  - `agents/test-engineer.md`: QA engineer checking test coverage, failure modes, assertions.
  - `agents/web-performance-auditor.md`: Web performance auditor checking Core Web Vitals and load budgets.

### 3. Shared Checklists (`references/`)
When executing reviews, definitions of done, or security audits, consult the shared checklists in `references/`:
- `references/definition-of-done.md`: Project-wide gate for declaring any increment done.
- `references/security-checklist.md`: AppSec verification criteria.
- `references/performance-checklist.md`: Performance verification criteria.
- `references/testing-patterns.md`: Concrete implementation testing patterns.
- `references/accessibility-checklist.md`: WCAG accessibility verification.
- `references/orchestration-patterns.md`: Multi-agent collaboration catalog.

### 4. Standard Compliance Rules
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
   - `skills/general/` for custom skills, community contributions, or SDLC tooling.
2. Initialize with `create-skill-v2`:
   ```bash
   python skills/general/create-skill-v2/scripts/init_skill.py \
     --name "<skill-name>" \
     --description "<trigger-description>" \
     --dest "skills/<category>"
   ```
3. Or ingest and verify from GitHub with the Automated Pipeline:
   ```bash
   # Dry-run check for duplicates and security vulnerabilities
   python scripts/sync_skills.py --check-local <path-to-skill> --dry-run

   # Ingest a skill from an upstream GitHub repository
   python scripts/sync_skills.py --github-repo <owner/repo> --skill-path <path> --category <general|anthropic|openai>
   ```
4. Run automated validation:
   ```bash
   python scripts/validate_skills.py
   node scripts/validate-skills.js
   node scripts/validate-commands.js
   node scripts/validate-reference-links.js
   node scripts/validate-versions.js
   python -m unittest scripts/test_ingestion_pipeline.py
   ```
5. Update both [`SKILLS_MAP.md`](SKILLS_MAP.md) and [`README.md`](README.md).
