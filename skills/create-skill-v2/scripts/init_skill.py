#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Scaffolding CLI tool (v2) to initialize an Agent Skill adhering to agentskills.io.
Loads templates dynamically from assets/ and enforces strict naming and metadata constraints.
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Spec constraints: 1-64 chars, lowercase alphanumeric, single hyphens, no leading/trailing hyphen
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_name(name: str) -> bool:
    """Validate that the skill name strictly adheres to the agentskills.io specification."""
    if not name or len(name) > 64:
        return False
    if "--" in name:
        return False
    return bool(NAME_PATTERN.match(name))


def get_asset_template(assets_dir: Path, template_name: str, fallback_content: str) -> str:
    """Load template content from assets/ directory, falling back to default string if not found."""
    template_path = assets_dir / template_name
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return fallback_content


def create_skill(
    name: str,
    description: str,
    dest_dir: Path,
    with_scripts: bool = True,
    with_references: bool = True,
    with_assets: bool = True,
    with_evals: bool = True,
    title: str = None,
    dry_run: bool = False,
) -> Path:
    """Creates the skill directory structure and initial files using dynamic templates."""
    if not validate_name(name):
        raise ValueError(
            f"Invalid skill name '{name}'. Must be 1-64 chars, lowercase alphanumeric with hyphens, "
            f"no consecutive hyphens ('--'), and cannot start or end with a hyphen (e.g. 'code-review')."
        )

    desc_clean = description.strip()
    if not desc_clean:
        raise ValueError("Description cannot be empty.")
    if len(desc_clean) > 1024:
        raise ValueError("Description must be at most 1024 characters as per agentskills.io specification.")

    skill_root = dest_dir / name
    if skill_root.exists() and not dry_run:
        raise FileExistsError(f"Directory already exists: {skill_root}")

    display_title = title if title else name.replace("-", " ").title()

    # Locate assets template directory relative to this script
    script_assets_dir = Path(__file__).resolve().parent.parent / "assets"

    # Replacements map
    replacements = {
        "{{SKILL_NAME}}": name,
        "{{SKILL_TITLE}}": display_title,
        "{{SKILL_DESCRIPTION}}": desc_clean,
        "{{SKILL_OVERVIEW}}": f"Provides specialized capabilities for {display_title}.",
        "{{TRIGGER_PHRASES}}": f"Explicit requests to perform {name} tasks.",
        "{{NEGATIVE_TRIGGERS}}": "General tasks that do not require specialized domain handling."
    }

    def apply_replacements(content: str) -> str:
        for k, v in replacements.items():
            content = content.replace(k, v)
        return content

    # 1. Prepare SKILL.md
    skill_md_raw = get_asset_template(
        script_assets_dir,
        "template_SKILL.md",
        fallback_content="""---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}}
license: MIT
---

# {{SKILL_TITLE}}

## Overview
{{SKILL_OVERVIEW}}

## When to Use
- Trigger: {{TRIGGER_PHRASES}}

## Workflow
1. Execute task.

## Gotchas
- Note edge cases.
"""
    )
    skill_md_content = apply_replacements(skill_md_raw)

    planned_files = [(skill_root / "SKILL.md", skill_md_content)]

    # 2. Prepare scripts/
    if with_scripts:
        script_raw = get_asset_template(
            script_assets_dir,
            "template_script.py",
            fallback_content="""#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
import sys
print('Hello from {{SKILL_NAME}}')
"""
        )
        planned_files.append((skill_root / "scripts" / "run.py", apply_replacements(script_raw)))

    # 3. Prepare references/
    if with_references:
        ref_raw = get_asset_template(
            script_assets_dir,
            "template_reference.md",
            fallback_content="# {{SKILL_TITLE}} Reference\n\nReference documentation."
        )
        planned_files.append((skill_root / "references" / "guide.md", apply_replacements(ref_raw)))

    # 4. Prepare assets/
    if with_assets:
        sample_asset = f"# Configuration template for {name}\nversion: '1.0'\n"
        planned_files.append((skill_root / "assets" / "sample.yaml", sample_asset))

    # 5. Prepare evals/
    if with_evals:
        evals_raw = get_asset_template(
            script_assets_dir,
            "template_evals.json",
            fallback_content="""{
  "skill_name": "{{SKILL_NAME}}",
  "evals": [
    {
      "id": 1,
      "prompt": "Test query for {{SKILL_NAME}}",
      "expected_output": "Expected output",
      "assertions": ["Task completed"]
    }
  ]
}"""
        )
        planned_files.append((skill_root / "evals" / "evals.json", apply_replacements(evals_raw)))

    if dry_run:
        print(f"[DRY-RUN] Would create skill at: {skill_root}")
        for p, _ in planned_files:
            print(f"  + {p.relative_to(dest_dir)}")
        return skill_root

    # Perform actual file writing
    skill_root.mkdir(parents=True, exist_ok=True)
    for file_path, content in planned_files:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

    return skill_root


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Initialize an Agent Skill (v2) adhering to agentskills.io with dynamic template loading."
    )
    parser.add_argument("--name", "-n", required=True, help="Skill identifier in kebab-case (1-64 chars).")
    parser.add_argument("--description", "-d", required=True, help="Concise activation description (max 1024 chars).")
    parser.add_argument("--dest", "-o", default=".", help="Destination directory (defaults to current dir).")
    parser.add_argument("--title", "-t", default=None, help="Human-readable title.")
    parser.add_argument("--no-scripts", action="store_true", help="Omit scripts/ directory.")
    parser.add_argument("--no-references", action="store_true", help="Omit references/ directory.")
    parser.add_argument("--no-assets", action="store_true", help="Omit assets/ directory.")
    parser.add_argument("--no-evals", action="store_true", help="Omit evals/ directory.")
    parser.add_argument("--dry-run", action="store_true", help="Preview planned files without writing to disk.")

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
            dry_run=args.dry_run,
        )
        if not args.dry_run:
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
