---
name: create-skill
description: Scaffolds and standardizes new Agent Skills adhering to the agentskills.io open standard with complete directory structure (SKILL.md, scripts, references, assets, evals), progressive disclosure principles, and valid frontmatter. Use whenever the user asks to create, scaffold, generate, or structure a new agent skill.
license: MIT
---

# Create Skill

## Overview
This skill guides an AI Agent in creating new, standard-compliant Agent Skills. It ensures every generated skill follows the open standard defined by agentskills.io, including the 3-stage progressive disclosure lifecycle (Discovery -> Activation -> Execution), clean directory organization, strict frontmatter validation, and evaluation test suites.

## When to Use
- The user requests: "Tạo cho tôi một skill mới...", "Tạo skill [tên]...", "Create a skill for..."
- Scaffolding a new capability, workflow, or toolset into an Agent Skill folder.
- Standardizing or refactoring an informal prompt/instruction into a formal skill format.
- When NOT to use: For editing general non-skill codebases or simple one-off prompts that do not need to be reusable.

---

## Standard Structure of an Agent Skill

Every skill generated must conform to this hierarchy:
```text
<skill-name>/
├── SKILL.md              # [REQUIRED] YAML frontmatter + structured instructions (< 500 lines)
├── evals/                # [RECOMMENDED] Test cases (evals.json) and verifiable assertions
├── scripts/              # [OPTIONAL] Non-interactive helper scripts (Python PEP 723, Bash, JS)
├── references/           # [OPTIONAL] Deep documentation, API specs, schemas loaded on demand
└── assets/               # [OPTIONAL] Templates, boilerplate files, sample data
```

---

## Step-by-Step Workflow for the Agent

### Step 1: Gather Requirements & Clarify Scope
1. **Skill Name**:
   - 1 to 64 characters.
   - Lowercase alphanumeric characters and single hyphens (`kebab-case`).
   - Must NOT contain consecutive hyphens (`--`), and must not start or end with a hyphen.
   - Must match the directory name.
2. **Skill Description**:
   - 1 to 1024 characters.
   - Use imperative phrasing ("Use this skill when...") and explicit trigger keywords.
3. **Components needed**:
   - Helper scripts in `scripts/` (ensure non-interactive execution).
   - Test cases in `evals/evals.json`.
   - External reference documentation in `references/`.
   - Boilerplates or templates in `assets/`.

### Step 2: Execute Scaffolding
Run the built-in generator script `scripts/init_skill.py`:

```bash
python skills/create-skill/scripts/init_skill.py \
  --name "<skill-name>" \
  --description "<Concise description with clear activation triggers>" \
  --dest "skills"
```

*(Note: Flags `--no-scripts`, `--no-references`, `--no-assets`, or `--no-evals` can be passed if not needed).*

### Step 3: Author the New `SKILL.md`
Tailor the generated `SKILL.md`:
1. **YAML Frontmatter**:
   - `name`: Must match the directory name.
   - `description`: 1–3 sentences explaining what the skill does and explicit trigger conditions.
   - Optional: `license`, `compatibility`, `metadata`.
2. **Body**:
   - **Overview**: 1-2 sentences on capability.
   - **When to Use**: Specific bullet points with trigger phrases.
   - **Step-by-Step Workflow**: Action-oriented, sequential instructions for the agent.
   - **Gotchas**: Non-obvious edge cases, environment quirks, or common agent pitfalls.
   - **Verification Checklist**: Explicit checks for the agent to confirm completion.

### Step 4: Add Evaluation Suite (`evals/evals.json`)
Define 2-3 realistic prompts, expected outputs, and objective assertions to enable test-driven verification.

### Step 5: Gotchas
- Avoid interactive prompts in scripts (no `input()` or TTY confirmation prompts).
- Do not repeat basic domain knowledge (e.g. explaining what JSON or Git is). Focus strictly on project conventions.
- Keep `SKILL.md` under 500 lines. Move large manuals to `references/`.
- Restrict emoji usage: use emojis only where strictly necessary, avoiding excessive decoration.

---

## Detailed References
- Specification rules: [specification.md](references/specification.md)
- Prompting best practices: [prompting_guidelines.md](references/prompting_guidelines.md)
- Base templates: `assets/`
