---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}}
license: MIT
---

# {{SKILL_TITLE}}

## Overview
{{SKILL_OVERVIEW}} Keep this section under 2-3 sentences.

## When to Use
- Explicit user requests: {{TRIGGER_PHRASES}}
- Implicit tasks: When handling specific file types, schemas, or workflows.
- When NOT to use: {{NEGATIVE_TRIGGERS}}

## Workflow

### Step 1: Pre-execution & Input Verification
Validate inputs and verify required preconditions:
- Check required files, environment variables, or CLI tools exist.

### Step 2: Execution
Follow systematic steps to perform the task:
1. Run helper script or commands:
   ```bash
   python scripts/run.py --input "$INPUT"
   ```
2. Process results and inspect output.

### Step 3: Verification & Reporting
- Verify output against success criteria.
- Present clean, structured results to the user.

## Gotchas
- Gotcha 1: Non-obvious edge cases, environment quirks, or silent failure modes.
- Gotcha 2: Common assumptions the agent might make that are incorrect for this task.

## References & Assets
- See `references/` for detailed domain knowledge.
- See `assets/` for templates and sample configurations.
- See `evals/evals.json` for validation test cases.
