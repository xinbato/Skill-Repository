---
name: create-skill-v2
description: Next-generation Agent Skill creator and eval-driven optimizer. Scaffolds standard-compliant skills (agentskills.io) using dynamic templates, runs cross-platform evaluation loops (Windows/macOS/Linux), and benchmarks trigger accuracy. Use when the user asks to create, scaffold, benchmark, evaluate, or optimize an agent skill.
license: MIT
---

# Create Skill (v2)

## Overview
This skill guides the AI Agent in scaffolding, testing, and optimizing production-grade Agent Skills adhering to the open [agentskills.io](https://agentskills.io) standard. Building upon the strengths of Anthropic's eval methodology and user-centric ergonomics, v2 incorporates dynamic template loading, Windows-safe evaluation runners, and automated HTML reporting.

## When to Use
- User requests: "Tạo skill mới...", "Tạo skill v2...", "Scaffold skill [tên]...", "Chạy eval cho skill...", "Tối ưu hóa skill".
- Scaffolding a new capability, workflow, or toolset into an Agent Skill folder.
- Measuring skill reliability and assertion pass-rates using automated test suites.
- When NOT to use: For editing general non-skill source code or executing simple one-off ad-hoc prompts.

---

## Standard Structure of an Agent Skill (v2)

```text
<skill-name>/
├── SKILL.md              # [REQUIRED] YAML metadata + instructions (< 500 lines)
├── evals/                # [RECOMMENDED] Test queries, assertions, and evaluation reports
│   ├── evals.json        # Test cases and expected outcomes
│   └── output/           # grading.json, report.html, benchmark summaries
├── scripts/              # [OPTIONAL] Non-interactive helper scripts (PEP 723)
├── references/           # [OPTIONAL] Deep documentation loaded on demand
└── assets/               # [OPTIONAL] Static resources, templates, boilerplates
```

---

## Step-by-Step Workflow for the Agent

### Step 1: Clarify Scope & Requirements
1. **Skill Name**:
   - 1 to 64 characters.
   - Lowercase alphanumeric characters and single hyphens (`kebab-case`).
   - Must NOT contain consecutive hyphens (`--`), and must not start or end with a hyphen.
   - Must match the directory name.
2. **Skill Description**:
   - 1 to 1024 characters.
   - Use imperative phrasing ("Use this skill when...") and explicit trigger keywords.
   - Define clear negative boundaries (when NOT to trigger).
3. **Components needed**:
   - Does it need executable helper scripts in `scripts/`?
   - Does it need external reference documentation in `references/`?
   - Does it need templates or configuration assets in `assets/`?

### Step 2: Execute Scaffolding
Run the v2 generator script `scripts/init_skill.py`:

```bash
python skills/create-skill-v2/scripts/init_skill.py \
  --name "<skill-name>" \
  --description "<Concise description with clear activation triggers>" \
  --dest "skills"
```

*(Optional flags: `--no-scripts`, `--no-references`, `--no-assets`, `--no-evals`, `--dry-run`).*

### Step 3: Author Domain Knowledge in `SKILL.md`
1. Tailor the generated `SKILL.md`:
   - Keep total lines strictly **under 500 lines** and **< 5,000 tokens**.
   - Include a concrete **`## Gotchas`** section listing non-obvious failure modes and environment quirks.
   - Follow **Defaults, Not Menus**: recommend a single primary tool/library rather than a list of options.
   - Use **Checklists** (`- [ ] Step 1...`) for multi-step tasks.

### Step 4: Run Cross-Platform Verification & Evals
Execute the Windows-safe evaluation runner to test assertions and verify output:

```bash
python skills/create-skill-v2/scripts/run_eval.py \
  --eval-file "skills/<skill-name>/evals/evals.json" \
  --output-dir "skills/<skill-name>/evals/output"
```

### Step 5: Generate Visual HTML Report (Optional)
Generate an interactive, standalone HTML report for review:

```bash
python skills/create-skill-v2/scripts/generate_report.py \
  --grading-file "skills/<skill-name>/evals/output/grading.json" \
  --output "skills/<skill-name>/evals/output/report.html"
```

---

## Gotchas
- **Windows Process Execution**: Never use `select.select()` on anonymous pipes when building eval runners. Use `subprocess.run()` with `timeout` or thread-safe queues.
- **Non-Interactive Execution**: Never invoke interactive TTY prompts (`input()`, confirmation dialogs) in scripts; pass all configuration via CLI flags.
- **Stream Separation**: Always send parseable data (JSON/CSV) to `stdout` and diagnostic logs/progress messages to `stderr`.
- **Restricted Emoji Usage**: Avoid decorative emojis across headings and body copy; maintain a clean, professional engineering style.

---

## References & Resources
- Specification details: [specification.md](references/specification.md)
- Prompting best practices: [prompting_guidelines.md](references/prompting_guidelines.md)
- Evaluation methodology: [eval_methodology.md](references/eval_methodology.md)
- Base templates: `assets/`
