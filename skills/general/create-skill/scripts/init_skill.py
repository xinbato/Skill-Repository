#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Scaffolding CLI tool to initialize a new Agent Skill following the agentskills.io format.
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Spec constraints: 1-64 chars, lowercase alphanumeric and hyphens, no consecutive hyphens, no leading/trailing hyphen
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_name(name: str) -> bool:
    """Validate that the skill name strictly adheres to the agentskills.io specification."""
    if not name or len(name) > 64:
        return False
    if "--" in name:
        return False
    return bool(NAME_PATTERN.match(name))


def create_skill(
    name: str,
    description: str,
    dest_dir: Path,
    with_scripts: bool = True,
    with_references: bool = True,
    with_assets: bool = True,
    with_evals: bool = True,
    title: str = None,
) -> Path:
    """Creates the skill directory structure and initial files."""
    if not validate_name(name):
        raise ValueError(
            f"Invalid skill name '{name}'. Must be 1-64 chars, lowercase alphanumeric with hyphens, "
            f"no consecutive hyphens ('--'), and cannot start or end with a hyphen (e.g. 'code-review')."
        )

    if len(description.strip()) > 1024:
        raise ValueError("Description must be at most 1024 characters as per agentskills.io specification.")

    skill_root = dest_dir / name
    if skill_root.exists():
        raise FileExistsError(f"Directory already exists: {skill_root}")

    skill_root.mkdir(parents=True, exist_ok=False)

    display_title = title if title else name.replace("-", " ").title()

    # Create SKILL.md
    skill_md_content = f"""---
name: {name}
description: {description}
license: MIT
---

# {display_title}

## Overview
Briefly describe the purpose of {name} and what capabilities it provides. Keep this section under 2-3 sentences.

## When to Use
- Trigger 1: Explicit user request or task type.
- Trigger 2: Mention of relevant domain keywords or file extensions.
- When NOT to use: Boundary cases where another tool or general knowledge suffices.

## Workflow

### Step 1: Input Verification
Identify required inputs and validate preconditions:
- Verify necessary parameters or input files exist.

### Step 2: Execution
Follow systematic steps to accomplish the task:
1. Run relevant commands or scripts:
   ```bash
   python scripts/run.py
   ```
2. Process results.

### Step 3: Verification & Output
- Check outputs against requirements.
- Present clean, concise results to the user.

## Gotchas
- Gotcha 1: Non-obvious edge cases, environment quirks, or silent failure modes.
- Gotcha 2: Common assumptions the agent might make that are incorrect for this task.

## References & Assets
- See `references/` for detailed domain knowledge.
- See `assets/` for templates and sample configurations.
"""
    (skill_root / "SKILL.md").write_text(skill_md_content, encoding="utf-8")

    # Optional subdirectories
    if with_scripts:
        scripts_dir = skill_root / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        sample_script = f"""#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
\"\"\"
Helper script for {name}.
\"\"\"

import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Helper script for {name}")
    parser.add_argument("--input", "-i", help="Path to input file")
    return parser.parse_args()


def main():
    args = parse_args()
    # Ensure stdout is clean for data, diagnostics go to stderr
    print("[INFO] Executing {name} helper script...", file=sys.stderr)
    print('{{"status": "success", "skill": "{name}"}}')
    sys.exit(0)


if __name__ == "__main__":
    main()
"""
        (scripts_dir / "run.py").write_text(sample_script, encoding="utf-8")

    if with_references:
        ref_dir = skill_root / "references"
        ref_dir.mkdir(parents=True, exist_ok=True)
        sample_ref = f"""# {display_title} Reference Guide

## Detailed Guidelines
Put reference manuals, API specifications, and detailed documentation here.
The agent reads this file only on demand during execution to preserve context tokens.
"""
        (ref_dir / "guide.md").write_text(sample_ref, encoding="utf-8")

    if with_assets:
        assets_dir = skill_root / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        sample_asset = f"""# Sample configuration / template for {name}
key: value
"""
        (assets_dir / "sample.yaml").write_text(sample_asset, encoding="utf-8")

    if with_evals:
        evals_dir = skill_root / "evals"
        evals_dir.mkdir(parents=True, exist_ok=True)
        sample_evals = f"""{{
  "skill_name": "{name}",
  "evals": [
    {{
      "id": 1,
      "prompt": "Example user query that should trigger this skill",
      "expected_output": "Description of expected successful output",
      "assertions": [
        "The output addresses the primary task",
        "No internal errors occurred"
      ]
    }}
  ]
}}
"""
        (evals_dir / "evals.json").write_text(sample_evals, encoding="utf-8")

    return skill_root


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Initialize a new Agent Skill adhering to the agentskills.io standard."
    )
    parser.add_argument(
        "--name",
        "-n",
        required=True,
        help="Skill identifier in kebab-case (e.g. code-auditor, pdf-extractor). Max 64 chars.",
    )
    parser.add_argument(
        "--description",
        "-d",
        required=True,
        help="Concise description explaining what the skill does and when the agent should trigger it. Max 1024 chars.",
    )
    parser.add_argument(
        "--dest",
        "-o",
        default=".",
        help="Destination directory where the skill folder will be created (defaults to current dir).",
    )
    parser.add_argument(
        "--title",
        "-t",
        default=None,
        help="Human-readable title (defaults to capitalized name).",
    )
    parser.add_argument(
        "--no-scripts",
        action="store_true",
        help="Omit the scripts/ directory.",
    )
    parser.add_argument(
        "--no-references",
        action="store_true",
        help="Omit the references/ directory.",
    )
    parser.add_argument(
        "--no-assets",
        action="store_true",
        help="Omit the assets/ directory.",
    )
    parser.add_argument(
        "--no-evals",
        action="store_true",
        help="Omit the evals/ directory.",
    )

    args = parser.parse_args()
    dest_path = Path(args.dest).resolve()

    try:
        created_path = create_skill(
            name=args.name,
            description=args.description,
            dest_dir=dest_path,
            with_scripts=not args.no_scripts,
            with_references=not args.no_references,
            with_assets=not args.no_assets,
            with_evals=not args.no_evals,
            title=args.title,
        )
        print(f"[SUCCESS] Created skill at: {created_path}")
        print("Directory structure:")
        for root, dirs, files in os.walk(created_path):
            rel_root = os.path.relpath(root, dest_path)
            depth = rel_root.count(os.sep)
            indent = "  " * depth
            print(f"{indent}+-- {os.path.basename(root)}/")
            for f in sorted(files):
                print(f"{indent}    +-- {f}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
