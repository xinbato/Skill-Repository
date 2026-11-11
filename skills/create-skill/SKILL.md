---
name: create-skill
description: Scaffolds and standardizes new Agent Skills adhering to the agentskills.io open standard with complete directory structure (SKILL.md, scripts, references, assets), progressive disclosure principles, and valid frontmatter. Use whenever the user asks to create, scaffold, generate, or structure a new agent skill.
---

# Create Skill

## Overview
This skill guides an AI Agent in creating new, standard-compliant Agent Skills. It ensures every generated skill follows the open standard defined by `agentskills.io`, including the 3-stage progressive disclosure lifecycle (Discovery -> Activation -> Execution), clean directory organization, and high-quality instruction authoring.

## When to Use
- The user requests: *"Tạo cho tôi một skill mới...", "Tạo skill [tên]...", "Create a skill for..."*
- Scaffolding a new capability, workflow, or toolset into an Agent Skill folder.
- Standardizing or refactoring an informal prompt/instruction into a formal skill format.

---

## Standard Structure of an Agent Skill

Every skill generated must conform to this hierarchy:
```text
<skill-name>/
├── SKILL.md              # [REQUIRED] YAML frontmatter + structured instructions
├── scripts/              # [OPTIONAL] Helper scripts (Python, Bash, JS) for deterministic tasks
├── references/           # [OPTIONAL] Deep documentation, API specs, schemas loaded on demand
└── assets/               # [OPTIONAL] Templates, boilerplate files, sample data
```

---

## Step-by-Step Workflow for the Agent

### Step 1: Gather Requirements & Clarify Scope
1. **Skill Name**: Ensure it is in `kebab-case` (lowercase letters, numbers, hyphens only, e.g. `docker-deployer`, `api-tester`).
2. **Skill Purpose & Triggers**:
   - What task does this skill accomplish?
   - What specific user requests or keywords should trigger it?
3. **Components needed**:
   - Does it need executable helper scripts in `scripts/`?
   - Does it need external reference documentation in `references/`?
   - Does it need templates or configuration assets in `assets/`?

### Step 2: Execute Scaffolding
Run the built-in generator script `scripts/init_skill.py` to create the standardized folder structure:

```bash
python skills/create-skill/scripts/init_skill.py \
  --name "<skill-name>" \
  --description "<Concise description with clear activation triggers>" \
  --dest "skills"
```

*(Note: Flags `--no-scripts`, `--no-references`, or `--no-assets` can be passed if any component is not required).*

### Step 3: Author the New `SKILL.md`
Tailor the generated `SKILL.md` with domain-specific knowledge:
1. **YAML Frontmatter**:
   - `name`: Must match the directory name.
   - `description`: 1–3 sentences explaining **what** the skill does and **explicit trigger conditions** (critical for the *Discovery* stage).
2. **Body**:
   - **Overview**: 1-2 sentences on capability.
   - **When to Use**: Specific bullet points with trigger phrases.
   - **Step-by-Step Workflow**: Action-oriented, sequential instructions for the agent.
   - **Validation / Verification**: Explicit checks for the agent to confirm completion.
   - **Cross-references**: Point to files in `references/` or scripts in `scripts/`.

### Step 4: Populate Subdirectories
- **`scripts/`**: Add scripts for tasks that should be automated deterministically (e.g., data conversion, API polling, linting).
- **`references/`**: Move large manuals, detailed API guides, or cheat sheets here to avoid cluttering context during the *Activation* stage.
- **`assets/`**: Provide templates, boilerplate snippets, or mock files that the user or agent can copy/fill.

### Step 5: Verification Checklist
Before completing the task, verify:
- [ ] Directory name matches `name` in frontmatter.
- [ ] Frontmatter contains valid YAML between triple hyphens `---`.
- [ ] `description` clearly specifies both the action and trigger conditions.
- [ ] All referenced scripts or files exist and are executable/readable.

---

## Detailed References
- For complete specification rules, refer to [specification.md](references/specification.md).
- For prompting best practices in `SKILL.md`, refer to [prompting_guidelines.md](references/prompting_guidelines.md).
- For base templates, check `assets/` within this skill.
