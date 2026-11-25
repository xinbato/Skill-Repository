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

import fnmatch
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest.normalizer import parse_frontmatter as _parse_frontmatter_full

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / "skills"
AGENTS_DIR = ROOT_DIR / "agents"
COMMANDS_DIR = ROOT_DIR / "commands"
REFERENCES_DIR = ROOT_DIR / "references"

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_DESC_LENGTH = 1024

FORBIDDEN_TRACKED_PATTERNS = [
    # OS debris
    ".DS_Store",
    ".DS_Store?",
    "._*",
    "Thumbs.db",
    "ehthumbs.db",
    "desktop.ini",
    # IDE / Editor leftovers
    ".vscode/*",
    ".idea/*",
    "*.swp",
    "*.swo",
    "*~",
    "*.orig",
    "*.rej",
    "*.bak",
    "*.tmp",
    # Runtime / build / compiler garbage
    "__pycache__/*",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "node_modules/*",
    ".pytest_cache/*",
    ".coverage",
    "htmlcov/*",
    "*.log",
    # Evaluation outputs
    "*/evals/output/*",
    "*/evals/results/*",
    # Ephemeral CI / Ingestion artifacts
    "pr_scorecard.md",
    "pr_scorecard*.md",
    # Credentials
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.crt",
    "*.pfx",
    "*.p12",
]

SECRET_PATTERNS = [
    (re.compile(r"\bghp_[A-Za-z0-9_]{36}\b"), "GitHub Personal Access Token"),
    (re.compile(r"\bAIzaSy[A-Za-z0-9_-]{33}\b"), "Google API Key"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"), "OpenAI Secret Key"),
    (re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"), "Private Key Block"),
]

CONFLICT_PATTERNS = [
    re.compile(r"^<{7}\s", re.M),
    re.compile(r"^={7}$", re.M),
    re.compile(r"^>{7}\s", re.M),
]

FORBIDDEN_EXEC_EXTS = {".exe", ".dll", ".so", ".dylib", ".bin", ".obj", ".o", ".a", ".lib"}


def validate_hygiene() -> tuple[list[str], list[str], int]:
    """Validate repository cleanliness, absence of junk/secrets, and spec compliance."""
    errors = []
    warnings = []

    try:
        out = subprocess.check_output(["git", "ls-files"], cwd=ROOT_DIR, text=True)
        tracked_files = [f.strip() for f in out.splitlines() if f.strip()]
    except Exception as exc:
        warnings.append(f"Could not retrieve git ls-files: {exc}")
        return errors, warnings, 0

    for file_path in tracked_files:
        posix_path = file_path.replace("\\", "/")
        basename = Path(file_path).name

        for pattern in FORBIDDEN_TRACKED_PATTERNS:
            if fnmatch.fnmatch(posix_path, pattern) or fnmatch.fnmatch(basename, pattern):
                errors.append(f"hygiene: Forbidden tracked file '{file_path}' matches '{pattern}'")

        if posix_path.startswith("skills/") or posix_path.startswith("commands/"):
            ext = Path(file_path).suffix.lower()
            if ext in FORBIDDEN_EXEC_EXTS:
                errors.append(f"hygiene: Forbidden executable/binary file '{file_path}'")

        full_path = ROOT_DIR / file_path
        if full_path.exists() and full_path.is_file():
            try:
                content = full_path.read_text(encoding="utf-8", errors="ignore")
                for pat in CONFLICT_PATTERNS:
                    if pat.search(content):
                        errors.append(f"hygiene: Merge conflict marker in '{file_path}'")
                        break

                if "staged-secret-scan-test.js" not in posix_path and "evals/fixtures" not in posix_path:
                    for pat, label in SECRET_PATTERNS:
                        m = pat.search(content)
                        if m:
                            errors.append(f"hygiene: Secret leak ({label}) in '{file_path}'")
            except Exception:
                pass

    return errors, warnings, len(tracked_files)


def parse_frontmatter(content: str) -> dict:
    """Extract frontmatter key-value pairs from markdown content."""
    fm, _ = _parse_frontmatter_full(content)
    return fm


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
            elif not NAME_PATTERN.match(name):
                errors.append(f"{cat.name}/{skill_name}: Name '{name}' does not match pattern {NAME_PATTERN.pattern}")

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
                for py_file in sorted(scripts_dir.glob("*.py")):
                    if py_file.name == "__init__.py":
                        continue
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
            elif fm.get("name") != agent_file.stem:
                errors.append(f"agents/{agent_file.name}: Frontmatter name '{fm.get('name')}' != file stem '{agent_file.stem}'")
            if not fm.get("description"):
                errors.append(f"agents/{agent_file.name}: Missing 'description' in frontmatter")

    # Repository hygiene check
    hygiene_errs, hygiene_warns, tracked_count = validate_hygiene()
    errors.extend(hygiene_errs)
    warnings.extend(hygiene_warns)

    print(f"Validated {checked_skills} skills across {len(categories)} categories, {checked_agents} personas, and repository hygiene ({tracked_count} tracked files).")
    
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
