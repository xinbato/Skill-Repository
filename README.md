# Skill-Repository

> A standardized, portable hub of production-ready AI Agent Skills and engineering workflows.  
> Built according to the open [agentskills.io](https://agentskills.io) and [agent-plugins.org](https://agent-plugins.org) specifications.

[![Standard: agentskills.io](https://img.shields.io/badge/Standard-agentskills.io-blue.svg)](https://agentskills.io)
[![Standard: agent-plugins.org](https://img.shields.io/badge/Plugin-agent--plugins.org-purple.svg)](https://agent-plugins.org)
[![CI Validation](https://github.com/xinbato/Skill-Repository/actions/workflows/validate.yml/badge.svg)](https://github.com/xinbato/Skill-Repository/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/xinbato/Skill-Repository?style=social)](https://github.com/xinbato/Skill-Repository)

---

## Overview

**Skill-Repository** is a centralized library of reusable, version-controlled **Agent Skills**, **Personas**, and **Lifecycle Commands**. It encapsulates procedural engineering knowledge, executable scripts, and reference documentation into a clean format that any AI Agent (Claude Code, Cursor, Antigravity, OpenHands, Copilot, Codex, etc.) can discover and execute.

### Key Highlights
- **Full Engineering Lifecycle (SDLC)**: Covers requirements extraction (`interview-me`), specification (`spec-driven-development`), planning (`planning-and-task-breakdown`), test-driven implementation (`test-driven-development`), 5-axis review (`code-review-and-quality`), and shipping (`shipping-and-launch`).
- **Automated Skill Ingestion & Quality Gates**: 4-gate automated ingestion pipeline (`scripts/sync_skills.py`) featuring semantic deduplication, static security scanning (prompt injection & SAST), and automated Pull Request scorecards.
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
│   ├── planning.toml
│   ├── build.toml
│   ├── test.toml
│   ├── review.toml
│   ├── code-simplify.toml
│   ├── constraints.toml
│   ├── webperf.toml
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
│   ├── gemini-cli-setup.md
│   └── codex-setup.md
├── scripts/                          # Automated quality gates and linters
│   ├── validate_skills.py
│   ├── validate-skills.js
│   ├── validate-commands.js
│   └── validate-reference-links.js
└── skills/                           # Modular engineering capabilities by ecosystem (How)
    ├── general/                      # Universal engineering lifecycle (SDLC) & custom tooling
    ├── anthropic/                    # Document processing, UI design, generative art & MCP
    ├── openai/                       # Browser automation & application security
    └── google/                       # Cloud infrastructure, Gemini API & developer tools
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
| **CONSTRAIN** | `/constraints` | Defines and enforces project quality bars, sane defaults, and CONSTRAINTS.md. |
| **AUDIT** | `/webperf` | Runs a web performance audit via the web-performance-auditor persona. |
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
| **[`find-skills`](skills/general/find-skills/)** | Discovers and installs skills from the open ecosystem using `npx skills` when capabilities are needed. | Developer Tooling / Discovery | [Explore](skills/general/find-skills/SKILL.md) |
| **[`create-skill-v2`](skills/general/create-skill-v2/)** | Next-gen skill generator with dynamic templates, Windows-safe eval runner, and HTML reports. | Developer Tooling | [Explore](skills/general/create-skill-v2/SKILL.md) |
| **[`create-skill`](skills/general/create-skill/)** | Scaffolds standard-compliant Agent Skills with directory structure, metadata, and scripts. | Developer Tooling | [Explore](skills/general/create-skill/SKILL.md) |
| **[`git-workflow`](skills/general/git-workflow/)** | Analyzes git diffs, enforces Conventional Commits, prevents secret leaks, and prepares PRs. | Version Control / DevOps | [Explore](skills/general/git-workflow/SKILL.md) |
| **[`email-teacher`](skills/general/email-teacher/)** | Drafts respectful, academic-grade correspondence to professors for leaves and extensions. | Academic / Communication | [Explore](skills/general/email-teacher/SKILL.md) |
| **[`composition-patterns`](skills/general/composition-patterns/)** | React composition patterns that scale. Use when refactoring components with boolean prop proliferation, building flexible component libraries, or d... | General | [Explore](skills/general/composition-patterns/SKILL.md) |

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
| **[`brand-guidelines`](skills/anthropic/brand-guidelines/)** | Applies Anthropic official brand colors, typography, and styling standards to artifacts, slides, and docs. | UI/UX & Design | [Explore](skills/anthropic/brand-guidelines/SKILL.md) |
| **[`academy-guide`](skills/anthropic/academy-guide/)** | Check this skill before finishing replies to questions about how to use Claude or a Claude product — it recommends matching courses, tutorials, and... | Anthropic Ecosystem | [Explore](skills/anthropic/academy-guide/SKILL.md) |
| **[`claude-api`](skills/anthropic/claude-api/)** | Reference for the Claude API / Anthropic SDK — model ids, pricing, params, streaming, tool use, MCP, agents, caching, token counting, model migrati... | Anthropic Ecosystem | [Explore](skills/anthropic/claude-api/SKILL.md) |
| **[`discernment-nudge`](skills/anthropic/discernment-nudge/)** | After you give a substantive answer or draft that the user may act on — advice or recommendations, drafted artifacts such as goals, plans, pitches,... | Anthropic Ecosystem | [Explore](skills/anthropic/discernment-nudge/SKILL.md) |
| **[`doc-coauthoring`](skills/anthropic/doc-coauthoring/)** | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, d... | Anthropic Ecosystem | [Explore](skills/anthropic/doc-coauthoring/SKILL.md) |
| **[`internal-comms`](skills/anthropic/internal-comms/)** | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this sk... | Anthropic Ecosystem | [Explore](skills/anthropic/internal-comms/SKILL.md) |
| **[`skill-creator`](skills/anthropic/skill-creator/)** | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or ... | Anthropic Ecosystem | [Explore](skills/anthropic/skill-creator/SKILL.md) |
| **[`slack-gif-creator`](skills/anthropic/slack-gif-creator/)** | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when us... | Anthropic Ecosystem | [Explore](skills/anthropic/slack-gif-creator/SKILL.md) |
| **[`web-artifacts-builder`](skills/anthropic/web-artifacts-builder/)** | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn... | Anthropic Ecosystem | [Explore](skills/anthropic/web-artifacts-builder/SKILL.md) |

### OpenAI Ecosystem (`skills/openai/`)

| Skill | Description | Category | Link |
| :--- | :--- | :--- | :--- |
| **[`playwright`](skills/openai/playwright/)** | Automates real browsers from terminal: navigation, form filling, snapshots, screenshots, and scraping. | Testing & Automation | [Explore](skills/openai/playwright/SKILL.md) |
| **[`security-threat-model`](skills/openai/security-threat-model/)** | Grounded AppSec threat modeling: enumerates trust boundaries, assets, attacker capabilities, mitigations. | Security | [Explore](skills/openai/security-threat-model/SKILL.md) |
| **[`security-best-practices`](skills/openai/security-best-practices/)** | Reviews code for language and framework security best practices (SQLi, XSS, tokens) with fix diffs. | Security | [Explore](skills/openai/security-best-practices/SKILL.md) |
| **[`aspnet-core`](skills/openai/aspnet-core/)** | Build, review, refactor, or architect ASP.NET Core web applications using current official guidance for .NET web development. Use when working on B... | OpenAI Ecosystem | [Explore](skills/openai/aspnet-core/SKILL.md) |
| **[`chatgpt-apps`](skills/openai/chatgpt-apps/)** | Build, scaffold, refactor, and troubleshoot ChatGPT Apps SDK applications that combine an MCP server and widget UI. Use when Codex needs to design ... | OpenAI Ecosystem | [Explore](skills/openai/chatgpt-apps/SKILL.md) |
| **[`cli-creator`](skills/openai/cli-creator/)** | Build a composable CLI for Codex from API docs, an OpenAPI spec, existing curl examples, an SDK, a web app, an admin tool, or a local script. Use w... | OpenAI Ecosystem | [Explore](skills/openai/cli-creator/SKILL.md) |
| **[`cloudflare-deploy`](skills/openai/cloudflare-deploy/)** | Deploy applications and infrastructure to Cloudflare using Workers, Pages, and related platform services. Use when the user asks to deploy, host, p... | OpenAI Ecosystem | [Explore](skills/openai/cloudflare-deploy/SKILL.md) |
| **[`define-goal`](skills/openai/define-goal/)** | Help the user define a concrete, measurable goal before starting work, especially when they ask to use the goal tool, create a goal, set an objecti... | OpenAI Ecosystem | [Explore](skills/openai/define-goal/SKILL.md) |
| **[`figma`](skills/openai/figma/)** | Use the Figma MCP server to fetch design context, screenshots, variables, and assets from Figma, and to translate Figma nodes into production code.... | OpenAI Ecosystem | [Explore](skills/openai/figma/SKILL.md) |
| **[`figma-code-connect-components`](skills/openai/figma-code-connect-components/)** | Connects Figma design components to code components using Code Connect mapping tools. Use when user says \"code connect\", \"connect this component... | OpenAI Ecosystem | [Explore](skills/openai/figma-code-connect-components/SKILL.md) |
| **[`figma-create-design-system-rules`](skills/openai/figma-create-design-system-rules/)** | Generates custom design system rules for the user's codebase. Use when user says \"create design system rules\", \"generate rules for my project\",... | OpenAI Ecosystem | [Explore](skills/openai/figma-create-design-system-rules/SKILL.md) |
| **[`figma-create-new-file`](skills/openai/figma-create-new-file/)** | Create a new blank Figma file. Use when the user wants to create a new Figma design or FigJam file, or when you need a new file before calling use_... | OpenAI Ecosystem | [Explore](skills/openai/figma-create-new-file/SKILL.md) |
| **[`figma-generate-design`](skills/openai/figma-generate-design/)** | Use this skill alongside figma-use when the task involves translating an application page, view, or multi-section layout into Figma. Triggers: 'wri... | OpenAI Ecosystem | [Explore](skills/openai/figma-generate-design/SKILL.md) |
| **[`figma-generate-library`](skills/openai/figma-generate-library/)** | Build or update a professional-grade design system in Figma from a codebase. Use when the user wants to create variables/tokens, build component li... | OpenAI Ecosystem | [Explore](skills/openai/figma-generate-library/SKILL.md) |
| **[`figma-implement-design`](skills/openai/figma-implement-design/)** | Translates Figma designs into production-ready application code with 1:1 visual fidelity. Use when implementing UI code from Figma files, when user... | OpenAI Ecosystem | [Explore](skills/openai/figma-implement-design/SKILL.md) |
| **[`figma-use`](skills/openai/figma-use/)** | **MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `use_figma` tool call. NEVER call `use_figma` directly without loading this sk... | OpenAI Ecosystem | [Explore](skills/openai/figma-use/SKILL.md) |
| **[`gh-address-comments`](skills/openai/gh-address-comments/)** | Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authentic... | OpenAI Ecosystem | [Explore](skills/openai/gh-address-comments/SKILL.md) |
| **[`gh-fix-ci`](skills/openai/gh-fix-ci/)** | Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions; use `gh` to inspect checks and logs, summarize failure co... | OpenAI Ecosystem | [Explore](skills/openai/gh-fix-ci/SKILL.md) |
| **[`hatch-pet`](skills/openai/hatch-pet/)** | Create, repair, validate, visually QA, and package Codex-compatible animated pets and pet spritesheets from character art, generated images, compan... | OpenAI Ecosystem | [Explore](skills/openai/hatch-pet/SKILL.md) |
| **[`imagegen`](skills/openai/imagegen/)** | Generate or edit raster images when the task benefits from AI-created bitmap visuals such as photos, illustrations, textures, sprites, mockups, or ... | OpenAI Ecosystem | [Explore](skills/openai/imagegen/SKILL.md) |
| **[`jupyter-notebook`](skills/openai/jupyter-notebook/)** | Use when the user asks to create, scaffold, or edit Jupyter notebooks (`.ipynb`) for experiments, explorations, or tutorials; prefer the bundled te... | OpenAI Ecosystem | [Explore](skills/openai/jupyter-notebook/SKILL.md) |
| **[`linear`](skills/openai/linear/)** | Manage issues, projects & team workflows in Linear. Use when the user wants to read, create or updates tickets in Linear. | OpenAI Ecosystem | [Explore](skills/openai/linear/SKILL.md) |
| **[`migrate-to-codex`](skills/openai/migrate-to-codex/)** | Migrate supported instruction files, skills, agents, and MCP config into Codex project and global files. Use when you need assistance with migrate ... | OpenAI Ecosystem | [Explore](skills/openai/migrate-to-codex/SKILL.md) |
| **[`netlify-deploy`](skills/openai/netlify-deploy/)** | Deploy web projects to Netlify using the Netlify CLI (`npx netlify`). Use when the user asks to deploy, host, publish, or link a site/repo on Netli... | OpenAI Ecosystem | [Explore](skills/openai/netlify-deploy/SKILL.md) |
| **[`notion-knowledge-capture`](skills/openai/notion-knowledge-capture/)** | Capture conversations and decisions into structured Notion pages; use when turning chats/notes into wiki entries, how-tos, decisions, or FAQs with ... | OpenAI Ecosystem | [Explore](skills/openai/notion-knowledge-capture/SKILL.md) |
| **[`notion-meeting-intelligence`](skills/openai/notion-meeting-intelligence/)** | Prepare meeting materials with Notion context and Codex research; use when gathering context, drafting agendas/pre-reads, and tailoring materials t... | OpenAI Ecosystem | [Explore](skills/openai/notion-meeting-intelligence/SKILL.md) |
| **[`notion-research-documentation`](skills/openai/notion-research-documentation/)** | Research across Notion and synthesize into structured documentation; use when gathering info from multiple Notion sources to produce briefs, compar... | OpenAI Ecosystem | [Explore](skills/openai/notion-research-documentation/SKILL.md) |
| **[`notion-spec-to-implementation`](skills/openai/notion-spec-to-implementation/)** | Turn Notion specs into implementation plans, tasks, and progress tracking; use when implementing PRDs/feature specs and creating Notion plans + tas... | OpenAI Ecosystem | [Explore](skills/openai/notion-spec-to-implementation/SKILL.md) |
| **[`openai-docs`](skills/openai/openai-docs/)** | Use when the user asks how to build with OpenAI products or APIs, asks about Codex itself or choosing Codex surfaces, needs up-to-date official doc... | OpenAI Ecosystem | [Explore](skills/openai/openai-docs/SKILL.md) |
| **[`playwright-interactive`](skills/openai/playwright-interactive/)** | Persistent browser and Electron interaction through `js_repl` for fast iterative UI debugging. Use when you need assistance with playwright interac... | OpenAI Ecosystem | [Explore](skills/openai/playwright-interactive/SKILL.md) |
| **[`plugin-creator`](skills/openai/plugin-creator/)** | Create and scaffold plugin directories for Codex with a required `.codex-plugin/plugin.json`, optional plugin folders/files, and baseline placehold... | OpenAI Ecosystem | [Explore](skills/openai/plugin-creator/SKILL.md) |
| **[`render-deploy`](skills/openai/render-deploy/)** | Deploy applications to Render by analyzing codebases, generating render.yaml Blueprints, and providing Dashboard deeplinks. Use when the user wants... | OpenAI Ecosystem | [Explore](skills/openai/render-deploy/SKILL.md) |
| **[`screenshot`](skills/openai/screenshot/)** | Use when the user explicitly asks for a desktop or system screenshot (full screen, specific app or window, or a pixel region), or when tool-specifi... | OpenAI Ecosystem | [Explore](skills/openai/screenshot/SKILL.md) |
| **[`security-ownership-map`](skills/openai/security-ownership-map/)** | Analyze git repositories to build a security ownership topology (people-to-file), compute bus factor and sensitive-code ownership, and export CSV/J... | OpenAI Ecosystem | [Explore](skills/openai/security-ownership-map/SKILL.md) |
| **[`sentry`](skills/openai/sentry/)** | Use when the user asks to inspect Sentry issues or events, summarize recent production errors, or pull basic Sentry health data via the Sentry CLI;... | OpenAI Ecosystem | [Explore](skills/openai/sentry/SKILL.md) |
| **[`skill-installer`](skills/openai/skill-installer/)** | Install Codex skills into $CODEX_HOME/skills from a curated list or a GitHub repo path. Use when a user asks to list installable skills, install a ... | OpenAI Ecosystem | [Explore](skills/openai/skill-installer/SKILL.md) |
| **[`speech`](skills/openai/speech/)** | Use when the user asks for text-to-speech narration or voiceover, accessibility reads, audio prompts, or batch speech generation via the OpenAI Aud... | OpenAI Ecosystem | [Explore](skills/openai/speech/SKILL.md) |
| **[`transcribe`](skills/openai/transcribe/)** | Transcribe audio files to text with optional diarization and known-speaker hints. Use when a user asks to transcribe speech from audio/video, extra... | OpenAI Ecosystem | [Explore](skills/openai/transcribe/SKILL.md) |
| **[`vercel-deploy`](skills/openai/vercel-deploy/)** | Deploy applications and websites to Vercel. Use when the user requests deployment actions like \"deploy my app\", \"deploy and give me the link\", ... | OpenAI Ecosystem | [Explore](skills/openai/vercel-deploy/SKILL.md) |
| **[`winui-app`](skills/openai/winui-app/)** | Bootstrap, develop, and design modern WinUI 3 desktop applications with C# and the Windows App SDK using official Microsoft guidance, WinUI Gallery... | OpenAI Ecosystem | [Explore](skills/openai/winui-app/SKILL.md) |
| **[`yeet`](skills/openai/yeet/)** | Use only when the user explicitly asks to stage, commit, push, and open a GitHub pull request in one flow using the GitHub CLI (`gh`). Use when you... | OpenAI Ecosystem | [Explore](skills/openai/yeet/SKILL.md) |

### Google Ecosystem (`skills/google/`)

| Skill | Description | Category | Link |
| :--- | :--- | :--- | :--- |
| **[`gemini-api`](skills/google/gemini-api/)** | Use when the user asks about using Gemini in an enterprise environment or explicitly mentions Vertex AI, Google Cloud, or Agent Platform. Guides th... | Google Ecosystem | [Explore](skills/google/gemini-api/SKILL.md) |
| **[`agent-platform-access-audit`](skills/google/agent-platform-access-audit/)** | Audits AI agent data access, blast radius, and blocked policy operations in Google Cloud by querying Cloud Audit Logs via BigQuery. Use when invest... | Google Ecosystem | [Explore](skills/google/agent-platform-access-audit/SKILL.md) |

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
