#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Normalizer for candidate skills adhering to agentskills.io and Skill-Repository standards.
Enforces naming parity, valid frontmatter, PEP 723 headers, and creates default evals if missing.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_DESC_LENGTH = 1024

DEFAULT_EVALS_TEMPLATE = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "description": "Evaluation test cases for {skill_name}",
    "evals": [
        {
            "id": "eval-smoke-test-1",
            "prompt": "Activate and test basic usage of {skill_name}",
            "expected_outcome": "Skill executes instructions without error",
            "assertions": [
                {
                    "type": "contains_keywords",
                    "keywords": ["{skill_name}"]
                }
            ]
        }
    ]
}


def sanitize_skill_name(raw_name: str) -> str:
    """Sanitize name to lowercase alphanumeric with single hyphens."""
    cleaned = raw_name.lower().strip()
    cleaned = re.sub(r"[^a-z0-9]+", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned[:64]


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Parse YAML frontmatter and return (dict, remaining_body)."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    fm_raw = parts[1]
    body = parts[2]
    data = {}
    for line in fm_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            data[k] = v

    return data, body


def format_frontmatter(data: Dict[str, str]) -> str:
    """Format dictionary back into YAML frontmatter string."""
    lines = ["---"]
    for k, v in data.items():
        if "\n" in v or '"' in v or ":" in v:
            lines.append(f'{k}: "{v}"')
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def normalize_skill_directory(
    skill_dir: Path,
    expected_name: Optional[str] = None,
    default_license: str = "MIT"
) -> Tuple[bool, List[str]]:
    """
    Ensure the skill directory adheres to repo standards:
    1. Directory name valid
    2. SKILL.md frontmatter exists with name matching dir
    3. evals/evals.json exists (scaffolds if missing)
    4. Python scripts in scripts/ have PEP 723 headers
    """
    changes: List[str] = []
    skill_name = expected_name or skill_dir.name

    if not NAME_PATTERN.match(skill_name):
        sanitized = sanitize_skill_name(skill_name)
        return False, [f"Tên skill '{skill_name}' không hợp lệ. Đề xuất: '{sanitized}'"]

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, ["Không tìm thấy file SKILL.md để chuẩn hóa."]

    content = skill_md.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_frontmatter(content)

    # 1. Frontmatter normalization
    fm_modified = False
    if fm.get("name") != skill_name:
        fm["name"] = skill_name
        fm_modified = True
        changes.append(f"Cập nhật frontmatter 'name' thành '{skill_name}'")

    if not fm.get("description"):
        fm["description"] = f"Automated skill for {skill_name}"
        fm_modified = True
        changes.append("Bổ sung 'description' mặc định")
    elif len(fm["description"]) > MAX_DESC_LENGTH:
        fm["description"] = fm["description"][:MAX_DESC_LENGTH - 3] + "..."
        fm_modified = True
        changes.append(f"Cắt gọn description dưới {MAX_DESC_LENGTH} ký tự")

    if not fm.get("license"):
        fm["license"] = default_license
        fm_modified = True
        changes.append(f"Bổ sung license '{default_license}'")

    if fm_modified:
        new_content = format_frontmatter(fm) + "\n" + body.lstrip("\r\n")
        skill_md.write_text(new_content, encoding="utf-8")

    # 2. Ensure evals/evals.json exists
    evals_dir = skill_dir / "evals"
    evals_file = evals_dir / "evals.json"
    if not evals_file.exists():
        evals_dir.mkdir(parents=True, exist_ok=True)
        eval_data_str = json.dumps(DEFAULT_EVALS_TEMPLATE, indent=2).replace("{skill_name}", skill_name)
        evals_file.write_text(eval_data_str, encoding="utf-8")
        changes.append("Tự động sinh evals/evals.json theo chuẩn repository")

    # 3. Ensure PEP 723 in Python scripts
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        for py_file in scripts_dir.glob("*.py"):
            py_text = py_file.read_text(encoding="utf-8", errors="replace")
            if "# /// script" not in py_text:
                header = (
                    "#!/usr/bin/env python3\n"
                    "# /// script\n"
                    '# requires-python = ">=3.9"\n'
                    "# dependencies = []\n"
                    "# ///\n"
                )
                if py_text.startswith("#!"):
                    # Replace shebang
                    first_line, rest = py_text.split("\n", 1)
                    new_py_text = header + rest
                else:
                    new_py_text = header + py_text
                py_file.write_text(new_py_text, encoding="utf-8")
                changes.append(f"Tự động thêm PEP 723 header vào scripts/{py_file.name}")

    return True, changes
