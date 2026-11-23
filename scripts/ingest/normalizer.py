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
import unicodedata
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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
    """Sanitize name to lowercase alphanumeric with single hyphens, handling unicode/accents."""
    normalized = unicodedata.normalize("NFKD", raw_name).encode("ascii", "ignore").decode("ascii")
    cleaned = normalized.lower().strip()
    cleaned = re.sub(r"[^a-z0-9]+", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    cleaned = cleaned[:64].rstrip("-")
    return cleaned


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """
    Parse YAML frontmatter preserving multiline descriptions, lists, and nested metadata.
    """
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    fm_raw = parts[1]
    body = parts[2]

    lines = fm_raw.splitlines()
    data: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    SPEC_KEYS = {"name", "description", "license", "compatibility", "allowed-tools"}

    i = 0
    n = len(lines)

    def parse_block(base_indent: int) -> Any:
        nonlocal i
        while i < n and not lines[i].strip():
            i += 1
        if i >= n:
            return None

        line = lines[i]
        curr_indent = len(line) - len(line.lstrip(" "))
        if curr_indent < base_indent:
            return None

        # Check if list block
        if line.lstrip(" ").startswith("- "):
            res_list = []
            while i < n:
                if not lines[i].strip():
                    i += 1
                    continue
                ind = len(lines[i]) - len(lines[i].lstrip(" "))
                if ind < curr_indent:
                    break
                s = lines[i].lstrip(" ")
                if s.startswith("- "):
                    val = s[2:].strip().strip('"').strip("'")
                    i += 1
                    res_list.append(val)
                else:
                    break
            return res_list

        # Check if dict block
        if ":" in line:
            res_dict = {}
            while i < n:
                if not lines[i].strip():
                    i += 1
                    continue
                ind = len(lines[i]) - len(lines[i].lstrip(" "))
                if ind < curr_indent:
                    break
                if ind > curr_indent:
                    i += 1
                    continue
                s = lines[i].strip()
                if not s or s.startswith("#") or ":" not in s:
                    i += 1
                    continue

                k, v = s.split(":", 1)
                k = k.strip()
                v = v.strip()
                i += 1

                if not v:
                    sub_val = parse_block(curr_indent + 1)
                    res_dict[k] = sub_val if sub_val is not None else ""
                elif v in (">", ">-", "|", "|-"):
                    is_folded = v.startswith(">")
                    scalar_lines = []
                    while i < n:
                        s_line = lines[i]
                        if not s_line.strip():
                            scalar_lines.append("")
                            i += 1
                            continue
                        s_ind = len(s_line) - len(s_line.lstrip(" "))
                        if s_ind <= curr_indent:
                            break
                        scalar_lines.append(s_line.strip())
                        i += 1
                    if is_folded:
                        res_dict[k] = " ".join(l for l in scalar_lines if l).strip()
                    else:
                        res_dict[k] = "\n".join(scalar_lines).strip()
                elif (v.startswith('"') and not v.endswith('"')) or (v.startswith("'") and not v.endswith("'")):
                    quote_char = v[0]
                    quoted_lines = [v[1:]]
                    while i < n:
                        q_line = lines[i].strip()
                        i += 1
                        if q_line.endswith(quote_char):
                            quoted_lines.append(q_line[:-1])
                            break
                        else:
                            quoted_lines.append(q_line)
                    res_dict[k] = " ".join(quoted_lines).strip()
                else:
                    if v.startswith("[") and v.endswith("]"):
                        items = [item.strip().strip('"').strip("'") for item in v[1:-1].split(",") if item.strip()]
                        res_dict[k] = items
                    else:
                        res_dict[k] = v.strip('"').strip("'")
            return res_dict

        # Multiline plain text
        text_lines = []
        while i < n:
            if not lines[i].strip():
                i += 1
                continue
            ind = len(lines[i]) - len(lines[i].lstrip(" "))
            if ind < base_indent:
                break
            text_lines.append(lines[i].strip())
            i += 1
        return " ".join(text_lines)

    root_dict = parse_block(0) or {}

    for k, v in root_dict.items():
        if k in SPEC_KEYS:
            data[k] = v
        elif k == "metadata":
            if isinstance(v, dict):
                metadata.update(v)
            elif isinstance(v, str) and v:
                metadata["info"] = v
        else:
            metadata[k] = v

    if metadata:
        data["metadata"] = metadata

    return data, body


def _format_yaml_value(val: Any, indent: int = 0) -> List[str]:
    sp = " " * indent
    lines: List[str] = []
    if isinstance(val, dict):
        for k, v in val.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{sp}{k}:")
                lines.extend(_format_yaml_value(v, indent + 2))
            else:
                lines.extend(_format_yaml_key_val(k, v, indent))
    elif isinstance(val, list):
        for item in val:
            if isinstance(item, (dict, list)):
                lines.append(f"{sp}-")
                lines.extend(_format_yaml_value(item, indent + 2))
            else:
                clean_item = str(item).strip()
                if any(c in clean_item for c in ('"', ':', '\n', '#')):
                    esc = clean_item.replace('"', '\\"')
                    lines.append(f'{sp}- "{esc}"')
                else:
                    lines.append(f"{sp}- {clean_item}")
    return lines


def _format_yaml_key_val(key: str, val: Any, indent: int = 0) -> List[str]:
    sp = " " * indent
    if isinstance(val, list):
        res = [f"{sp}{key}:"]
        res.extend(_format_yaml_value(val, indent + 2))
        return res
    if isinstance(val, dict):
        res = [f"{sp}{key}:"]
        res.extend(_format_yaml_value(val, indent + 2))
        return res

    v_str = str(val).strip()
    if "\n" in v_str:
        res = [f"{sp}{key}: |"]
        for line in v_str.splitlines():
            res.append(f"{sp}  {line}")
        return res

    if any(c in v_str for c in ('"', ':', '#', '{', '}', '[', ']')):
        esc = v_str.replace('"', '\\"')
        return [f'{sp}{key}: "{esc}"']
    else:
        return [f"{sp}{key}: {v_str}"]


def format_frontmatter(data: Dict[str, Any]) -> str:
    """Format dictionary back into valid Agent Skills specification YAML frontmatter."""
    lines = ["---"]
    spec_order = ["name", "description", "license", "compatibility", "allowed-tools"]
    for k in spec_order:
        if k in data and data[k] is not None:
            lines.extend(_format_yaml_key_val(k, data[k], 0))

    meta = data.get("metadata")
    if meta:
        if isinstance(meta, dict):
            lines.append("metadata:")
            lines.extend(_format_yaml_value(meta, 2))
        elif isinstance(meta, str) and meta.strip():
            lines.append(f"metadata: {meta.strip()}")

    lines.append("---")
    return "\n".join(lines)


def replace_links_in_markdown(md_text: str, replacements: Dict[str, str]) -> str:
    """
    Replace links to renamed supporting files in markdown without corrupting partial matches,
    anchors, query parameters, or plain text prose. Handles both raw and percent-encoded paths.
    """
    for old_name, new_name in replacements.items():
        variants = {
            old_name,
            urllib.parse.quote(old_name),
            old_name.replace("_", " "),
            urllib.parse.quote(old_name.replace("_", " ")),
            old_name.replace(" ", "_"),
            urllib.parse.quote(old_name.replace(" ", "_")),
        }
        escaped_variants = "|".join(re.escape(v) for v in sorted(variants, key=len, reverse=True))

        def repl_url(match):
            prefix = match.group(1)
            target = match.group(2)
            suffix = match.group(3)

            m = re.match(r"^([^?#]*)([?][^#]*)?([#].*)?$", target)
            if not m:
                return match.group(0)
            path, query, fragment = m.groups()
            query = query or ""
            fragment = fragment or ""

            pattern = re.compile(r"(^|[\/\\])(" + escaped_variants + r")$")
            if pattern.search(path):
                def sub_fn(p_match):
                    sep = p_match.group(1)
                    return sep + new_name
                path = pattern.sub(sub_fn, path)

            return f"{prefix}{path}{query}{fragment}{suffix}"

        # Markdown links: [text](target)
        md_text = re.sub(r"(\[[^\]]*\]\()([^\)]+)(\))", repl_url, md_text)
        # HTML links: <a href="target">
        md_text = re.sub(r'(<a\s+[^>]*href=["\'])([^"\']+)(["\'])', repl_url, md_text)

        # Path references in code/prose: references/old_name.md or ../../references/old_name.md
        def repl_path_ref(match):
            prefix = match.group(1)
            tail = match.group(3) or ""
            return f"{prefix}{new_name}{tail}"

        md_text = re.sub(
            r"((?:\.\.\/)*references\/)(" + escaped_variants + r")([?#][^\s\'\"\)\`\]]*)?(?=[^\w-]|$)",
            repl_path_ref,
            md_text,
            flags=re.IGNORECASE
        )

    return md_text


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
    5. Kebab-case filenames and link consistency
    """
    changes: List[str] = []
    skill_name = expected_name or skill_dir.name

    if not skill_name or not NAME_PATTERN.match(skill_name):
        sanitized = sanitize_skill_name(skill_name) if skill_name else "unnamed-skill"
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

    desc = fm.get("description", "")
    if not desc:
        fm["description"] = f"Automated skill for {skill_name}. Use when working with {skill_name}."
        fm_modified = True
        changes.append("Bổ sung 'description' mặc định kèm trigger")
    else:
        if not re.search(r"\buse (this )?when\b|\buse (before|after|during)\b", desc, re.I):
            clean_term = skill_name.replace("-", " ")
            desc = desc.strip().rstrip(".") + f". Use when you need assistance with {clean_term}."
            fm["description"] = desc
            fm_modified = True
            changes.append("Bổ sung 'Use when ...' trigger vào description")
        if len(fm["description"]) > MAX_DESC_LENGTH:
            fm["description"] = fm["description"][:MAX_DESC_LENGTH - 3].rstrip() + "..."
            fm_modified = True
            changes.append(f"Cắt gọn description dưới {MAX_DESC_LENGTH} ký tự")

    if not fm.get("license"):
        fm["license"] = default_license
        fm_modified = True
        changes.append(f"Bổ sung license '{default_license}'")

    if fm_modified:
        new_content = format_frontmatter(fm) + "\n\n" + body.strip() + "\n"
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
                    parts = py_text.split("\n", 1)
                    rest = parts[1] if len(parts) > 1 else ""
                    new_py_text = header + rest
                else:
                    new_py_text = header + py_text
                py_file.write_text(new_py_text, encoding="utf-8")
                changes.append(f"Tự động thêm PEP 723 header vào scripts/{py_file.name}")

    # 4. Enforce lowercase-hyphen-separated naming on supporting markdown files
    replacements: Dict[str, str] = {}
    for sub in skill_dir.iterdir():
        if sub.is_dir() and sub.name not in ("evals", "__pycache__", ".git"):
            for md_file in sub.rglob("*.md"):
                stem = md_file.stem
                clean_stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode("ascii")
                clean_stem = re.sub(r"[^a-z0-9]+", "-", clean_stem.lower()).strip("-")
                clean_stem = re.sub(r"-+", "-", clean_stem)
                clean_name = f"{clean_stem}.md"
                if clean_name != md_file.name:
                    replacements[md_file.name] = clean_name
                    target_file = md_file.parent / clean_name
                    if target_file.exists():
                        target_file.unlink()
                    md_file.rename(target_file)
                    try:
                        rel_path = md_file.parent.relative_to(skill_dir)
                    except ValueError:
                        rel_path = md_file.parent.name
                    changes.append(f"Đổi tên file sang kebab-case: {rel_path}/{md_file.name} -> {clean_name}")

    if replacements:
        for md_path in skill_dir.rglob("*.md"):
            try:
                md_text = md_path.read_text(encoding="utf-8", errors="replace")
                new_text = replace_links_in_markdown(md_text, replacements)
                if new_text != md_text:
                    md_path.write_text(new_text, encoding="utf-8")
            except Exception:
                pass

    return True, changes
