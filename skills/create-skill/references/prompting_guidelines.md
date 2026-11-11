# Guidelines for Authoring Agent Instructions in SKILL.md

When writing `SKILL.md`, the objective is to guide an AI agent reliably and concisely through complex workflows.

---

## 1. Crafting the Description (Discovery Stage)

The `description` field is the single gatekeeper for whether your skill gets loaded.
- **State clear triggers**: Always state what the user wants or says when this skill is needed.
  - *Good*: "Scaffolds a new Agent Skill following the agentskills.io specification. Use this skill when the user asks to create, initialize, or generate a new skill."
  - *Bad*: "Tool for making skills."
- **Mention negative triggers (if applicable)**: Clarify what the skill is NOT meant for if ambiguity exists (e.g., "Do not use for editing existing git repos").

---

## 2. Structuring the Body (Activation Stage)

A well-structured `SKILL.md` body should have:

1. **Overview / Purpose**: A 1-2 sentence statement of what this skill achieves.
2. **Prerequisites & Environment**: Required tools, CLIs, Python version, or packages.
3. **Step-by-Step Workflow**: Numbered, sequential steps using imperative language:
   - *Good*: "1. Ask the user for the skill name. 2. Verify kebab-case format. 3. Run the generator script."
   - *Bad*: "You could think about what the user might want, and then maybe create a directory..."
4. **Tool / Script Usage**: Clear guidance on which scripts to execute, with sample commands and argument explanations.
5. **Validation & Verification**: How the agent should verify success before reporting back to the user.
6. **Error Handling & Edge Cases**: What to do when commands fail, files exist, or inputs are invalid.

---

## 3. Minimizing Token Consumption

- Avoid dumping raw code or extensive documentation directly inside `SKILL.md`.
- Keep `SKILL.md` under 200-300 lines when possible.
- Move large reference docs to `references/<topic>.md` and instruct the agent: *"Read `references/<topic>.md` only when handling <specific edge case>."*
