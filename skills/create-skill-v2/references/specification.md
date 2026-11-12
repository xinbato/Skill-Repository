# Agent Skills Specification Reference (v2)

This document summarizes the open standard specification for Agent Skills as defined by [agentskills.io](https://agentskills.io).

---

## 1. Directory Structure

An Agent Skill is packaged as a self-contained directory with a standardized layout:

```text
<skill-name>/
├── SKILL.md              # [REQUIRED] Metadata and core instructions (< 500 lines)
├── evals/                # [RECOMMENDED] Evaluation queries and verifiable assertions
│   └── evals.json
├── scripts/              # [OPTIONAL] Non-interactive executable scripts
├── references/           # [OPTIONAL] Deep documentation, API specs, domain guidelines
├── assets/               # [OPTIONAL] Templates, static resources, configuration samples
└── ...                   # Any additional files or resources required by the skill
```

---

## 2. The `SKILL.md` File

`SKILL.md` contains two parts:
1. **YAML Frontmatter**: Metadata read during the **Discovery** stage.
2. **Markdown Body**: Detailed instructions read during the **Activation** stage.

### Frontmatter Schema

```yaml
---
name: my-skill-name
description: A clear explanation of what this skill does and specifically when the agent should activate it.
license: MIT
compatibility: Requires Python 3.10+, uv, git
metadata:
  author: xinbato
  version: "2.0"
allowed-tools: Bash(git:*) Read
---
```

#### Field Constraints:

| Field | Required | Constraints |
| :--- | :---: | :--- |
| `name` | **Yes** | 1 to 64 characters. Lowercase alphanumeric (`a-z`, `0-9`) and single hyphens (`-`). Must NOT start or end with a hyphen. Must NOT contain consecutive hyphens (`--`). Must match the parent directory name. |
| `description` | **Yes** | 1 to 1024 characters. Non-empty. Must describe what the skill does and when the agent should activate it. Use imperative phrasing. |
| `license` | No | License identifier (e.g. `MIT`, `Apache-2.0`) or reference to bundled license file. |
| `compatibility` | No | 1 to 500 characters. Environment requirements (runtime versions, CLI tools, network requirements). |
| `metadata` | No | Arbitrary string-to-string key-value mapping for additional metadata. |
| `allowed-tools`| No | Space-separated list of pre-approved tools the skill may run. (Experimental) |

---

## 3. The Progressive Disclosure Lifecycle

1. **Stage 1: Discovery (Startup / System Index)**: Only `name` and `description` are indexed. Budget: ~50 to 100 tokens per skill.
2. **Stage 2: Activation (Match & Load)**: When user task matches `description`, agent reads full `SKILL.md`. Budget: < 500 lines and < 5,000 tokens.
3. **Stage 3: Execution (On-Demand Deep Dives)**: Agent runs scripts or loads files from `references/` and `assets/` only when needed.

---

## 4. Cross-Client Discovery Standards

Compliant agentic clients scan standardized directory locations:

| Scope | Path | Precedence |
| :--- | :--- | :--- |
| Project | `<project>/.agents/skills/` | Highest (overrides user-level) |
| Project (Client-native) | `<project>/.<client>/skills/` | High |
| User | `~/.agents/skills/` | Base |
| User (Client-native) | `~/.<client>/skills/` | Base |
