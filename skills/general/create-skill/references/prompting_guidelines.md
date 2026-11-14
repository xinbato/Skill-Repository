# Guidelines for Authoring Agent Instructions in SKILL.md

When writing `SKILL.md`, the objective is to guide an AI agent reliably and concisely through complex workflows without wasting context window tokens.

---

## 1. Crafting the Description (Discovery Stage)

The `description` field is the single gatekeeper for whether your skill gets loaded.
- **Use imperative phrasing**: Frame the description as an instruction to the agent: *"Use this skill when..."* rather than *"This skill does..."*.
- **Focus on user intent, not internal code**: Match against what the user asks, not how the skill works internally.
- **Be pushy about implicit intent**: Mention triggers where the user might not state the domain directly (e.g. *"even if the user does not explicitly mention 'CSV' or 'email'"*).
- **Define clear negative boundaries**: Clarify what the skill does NOT cover to prevent false triggers on near-miss queries.
- **Strict length limit**: Stay within 1 to 1024 characters.

---

## 2. Structuring the Body (Activation Stage)

Keep `SKILL.md` under **500 lines** and **5,000 tokens**. A well-structured body should feature:

1. **Overview**: 1-2 sentence statement of what this skill achieves.
2. **When to Use**: Concrete triggers, file formats, and boundary conditions.
3. **Step-by-Step Workflow**: Numbered sequential steps using imperative language.
4. **Gotchas**: Non-obvious project facts, common mistakes, or silent failure modes.
5. **Validation / Verification**: Concrete checks (scripts or checklist) before reporting completion.

---

## 3. High-Value Instruction Patterns

### A. Gotchas Sections
The highest-value content in many skills is a list of gotchas — project-specific facts that defy general assumptions:
```markdown
## Gotchas
- The user table uses soft deletes; always include `WHERE deleted_at IS NULL`.
- The endpoint returns HTTP 200 even on logical errors; inspect the `status` JSON field.
```

### B. Defaults, Not Menus
Do not present multiple equivalent libraries or approaches. Pick a solid default and provide a brief fallback:
```markdown
Use `pdfplumber` for text extraction. For scanned documents requiring OCR, fall back to `pdf2image` with `pytesseract`.
```

### C. Validation Loops
Instruct the agent to inspect its own work before proceeding:
```markdown
1. Apply edits.
2. Run validation: `python scripts/validate.py`.
3. If errors occur, inspect stderr, fix the issues, and re-run.
4. Only proceed once validation succeeds.
```

### D. Plan-Validate-Execute
For batch or destructive operations:
1. Generate an intermediate plan in structured format (`plan.json`).
2. Run validation against the source of truth (`python scripts/verify_plan.py plan.json`).
3. Execute only after the plan passes validation.

---

## 4. Writing Agentic Scripts (`scripts/`)

- **Non-interactive**: Never invoke `input()`, prompt menus, or TTY dialogs. Accept all inputs via CLI flags or arguments.
- **PEP 723 metadata**: For Python, declare dependencies inline:
  ```python
  # /// script
  # requires-python = ">=3.9"
  # dependencies = ["requests", "pyyaml"]
  # ///
  ```
- **Stream separation**: Write parseable structured data (JSON/CSV) to `stdout`; send diagnostic logs and progress messages to `stderr`.

---

## 5. Tone and Presentation
- Avoid unnecessary emojis. Use emojis only where functional (e.g. standard alert callouts), avoiding decorative emoji lists.
- Keep prose concise, technical, and directly actionable.
