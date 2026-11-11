#!/usr/bin/env python3
"""
Scaffolding CLI tool to initialize a new Agent Skill following the agentskills.io format.
"""

import argparse
import os
import re
import sys
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_name(name: str) -> bool:
    """Validate that the skill name is strictly kebab-case lowercase."""
    return bool(NAME_PATTERN.match(name))


def create_skill(
    name: str,
    description: str,
    dest_dir: Path,
    with_scripts: bool = True,
    with_references: bool = True,
    with_assets: bool = True,
    title: str = None,
) -> Path:
    """Creates the skill directory structure and initial files."""
    if not validate_name(name):
        raise ValueError(
            f"Invalid skill name '{name}'. Must be lowercase alphanumeric with hyphens (e.g. 'my-awesome-skill')."
        )

    skill_root = dest_dir / name
    if skill_root.exists():
        raise FileExistsError(f"Directory already exists: {skill_root}")

    skill_root.mkdir(parents=True, exist_ok=False)

    display_title = title if title else name.replace("-", " ").title()

    # Create SKILL.md
    skill_md_content = f"""---
name: {name}
description: {description}
---

# {display_title}

## Overview
Briefly describe the purpose of {name} and what capabilities it provides.

## When to Use
- Use this skill when the user asks to ...
- Triggers: key phrases, specific file types, or distinct tasks.

## Workflow

### Step 1: Input Verification
Identify required inputs and validate preconditions:
- Verify necessary parameters are provided.

### Step 2: Execution
Follow systematic steps to accomplish the task:
1. Run relevant commands or scripts:
   ```bash
   python scripts/run.py
   ```
2. Process results.

### Step 3: Verification & Reporting
- Check outputs against requirements.
- Present clean, concise results to the user.

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
\"\"\"
Helper script for {name}.
\"\"\"

import sys

def main():
    print("Executing {name} helper script...")
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
The agent reads this file only on demand during execution.
"""
        (ref_dir / "guide.md").write_text(sample_ref, encoding="utf-8")

    if with_assets:
        assets_dir = skill_root / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        sample_asset = f"""# Sample configuration / template for {name}
key: value
"""
        (assets_dir / "sample.yaml").write_text(sample_asset, encoding="utf-8")

    return skill_root


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Agent Skill adhering to the agentskills.io standard."
    )
    parser.add_argument(
        "--name",
        "-n",
        required=True,
        help="Skill identifier in kebab-case (e.g. code-auditor, pdf-extractor).",
    )
    parser.add_argument(
        "--description",
        "-d",
        required=True,
        help="Concise description explaining what the skill does and when the agent should trigger it.",
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
            title=args.title,
        )
        print(f"✅ Successfully created skill at: {created_path}")
        print("📁 Directory structure:")
        for root, dirs, files in os.walk(created_path):
            rel_root = os.path.relpath(root, dest_path)
            depth = rel_root.count(os.sep)
            indent = "  " * depth
            print(f"{indent}├── {os.path.basename(root)}/")
            for f in files:
                print(f"{indent}  └── {f}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
