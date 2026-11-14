#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Universal Python Validator for Skill-Repository.
Validates skill frontmatter, directory parity, description limits, evals existence,
PEP 723 metadata in Python scripts, and agent personas.
"""

import os
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / "skills"
AGENTS_DIR = ROOT_DIR / "agents"
COMMANDS_DIR = ROOT_DIR / "commands"
REFERENCES_DIR = ROOT_DIR / "references"

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_DESC_LENGTH = 1024


def parse_frontmatter(content: str) -> dict:
    """Extract frontmatter key-value pairs from markdown content."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1]
    res = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            res[k] = v
    return res


def validate_skills() -> int:
    errors = []
    warnings = []
    checked_skills = 0

    if not SKILLS_DIR.exists():
        print(f"[ERROR] Skills directory not found at {SKILLS_DIR}")
        return 1

    categories = [d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]

    for cat in sorted(categories):
        subdirs = [d for d in cat.iterdir() if d.is_dir() and not d.name.startswith(".")]
        for skill_dir in sorted(subdirs):
            skill_name = skill_dir.name
            skill_md = skill_dir / "SKILL.md"
            checked_skills += 1

            if not skill_md.exists():
                errors.append(f"{cat.name}/{skill_name}: Missing SKILL.md")
                continue

            content = skill_md.read_text(encoding="utf-8", errors="replace")
            fm = parse_frontmatter(content)

            if not fm:
                errors.append(f"{cat.name}/{skill_name}: Missing or malformed YAML frontmatter")
                continue

            # Parity check
            name = fm.get("name", "")
            if not name:
                errors.append(f"{cat.name}/{skill_name}: Missing 'name' in frontmatter")
            elif name != skill_name:
                errors.append(f"{cat.name}/{skill_name}: Frontmatter name '{name}' != dir '{skill_name}'")

            # Description length check
            desc = fm.get("description", "")
            if not desc:
                errors.append(f"{cat.name}/{skill_name}: Missing 'description' in frontmatter")
            elif len(desc) > MAX_DESC_LENGTH:
                errors.append(f"{cat.name}/{skill_name}: Description length {len(desc)} > {MAX_DESC_LENGTH}")

            # Evals existence check
            evals_file = skill_dir / "evals" / "evals.json"
            if not evals_file.exists():
                warnings.append(f"{cat.name}/{skill_name}: Missing evals/evals.json")

            # Python script PEP 723 check
            scripts_dir = skill_dir / "scripts"
            if scripts_dir.exists() and scripts_dir.is_dir():
                for py_file in scripts_dir.glob("*.py"):
                    py_text = py_file.read_text(encoding="utf-8", errors="replace")
                    if "# /// script" not in py_text:
                        warnings.append(f"{cat.name}/{skill_name}: Python script '{py_file.name}' missing PEP 723 header")

    # Personas check
    checked_agents = 0
    if AGENTS_DIR.exists():
        for agent_file in sorted(AGENTS_DIR.glob("*.md")):
            if agent_file.name.lower() == "readme.md":
                continue
            checked_agents += 1
            content = agent_file.read_text(encoding="utf-8", errors="replace")
            fm = parse_frontmatter(content)
            if not fm.get("name"):
                errors.append(f"agents/{agent_file.name}: Missing 'name' in frontmatter")
            if not fm.get("description"):
                errors.append(f"agents/{agent_file.name}: Missing 'description' in frontmatter")

    print(f"Validated {checked_skills} skills across {len(categories)} categories and {checked_agents} personas.")
    
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN] {w}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  [ERROR] {e}")
        return 1

    print("\n[SUCCESS] All skills and personas passed structural validation!")
    return 0


if __name__ == "__main__":
    sys.exit(validate_skills())
