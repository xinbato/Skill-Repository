# Agent Skills Specification Reference

This document summarizes the open standard specification for Agent Skills as defined by [agentskills.io](https://agentskills.io).

---

## 1. Directory Structure

An Agent Skill is packaged as a self-contained directory with a standardized layout:

```text
<skill-name>/
├── SKILL.md              # [REQUIRED] Metadata and core instructions
├── scripts/              # [OPTIONAL] Executable scripts (Python, Bash, Node.js, etc.)
├── references/           # [OPTIONAL] Deep documentation, API specs, domain guidelines
├── assets/               # [OPTIONAL] Templates, static resources, configuration samples
└── ...                   # Any additional files or resources required by the skill
```

---

## 2. The `SKILL.md` File

`SKILL.md` is the only mandatory file. It contains two parts:
1. **YAML Frontmatter**: Metadata read during the **Discovery** stage.
2. **Markdown Body**: Detailed instructions read during the **Activation** stage.

### Frontmatter Schema

The YAML frontmatter MUST be at the top of `SKILL.md`, enclosed by triple hyphens `---`.

```yaml
---
name: my-skill-name
description: A clear explanation of what this skill does and specifically when the agent should activate it.
---
```

#### Fields:
- `name` *(Required)*:
  - String.
  - Naming rule: Lowercase alphanumeric with hyphens (`kebab-case`), e.g., `data-analysis`, `code-review`.
  - Should be concise and descriptive of the skill's domain.
- `description` *(Required)*:
  - String (1 to 3 sentences recommended).
  - Crucial for **Discovery**: The agent matches user prompts against this description.
  - Must clearly specify **what** the skill does and **when** it should be triggered (e.g., *"Use this skill when the user asks to..."*).
- `version` *(Optional)*: Semantic version string (e.g., `1.0.0`).
- `tags` *(Optional)*: Array of keywords.

---

## 3. The Progressive Disclosure Lifecycle

Agent Skills work via a 3-stage progressive disclosure model to keep the agent's context window lightweight:

1. **Stage 1: Discovery (Startup / System Index)**
   - Only `name` and `description` from the YAML frontmatter are indexed in the agent's context.
   - Minimal token footprint.
2. **Stage 2: Activation (Match & Load)**
   - When a user request matches the `description` criteria, the agent reads the full `SKILL.md`.
3. **Stage 3: Execution (On-Demand Deep Dives)**
   - While following instructions, the agent executes scripts in `scripts/` or reads specific files in `references/` and `assets/` only when needed.

---

## 4. Best Practices for Subdirectories

- **`scripts/`**: Place deterministic, repetitive, or complex programmatic tasks here (e.g., formatters, validators, scrapers, data converters).
- **`references/`**: Place large manuals, API documentations, cheat sheets, or edge-case handling rules here so they don't clutter `SKILL.md`.
- **`assets/`**: Place boilerplate files, configuration templates, or mock datasets here.
