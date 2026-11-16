#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Automated Security & Malware Scanner for Candidate Skills.
Performs Static Analysis (SAST) and Prompt Injection checks on SKILL.md and scripts.
"""

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

# Suspicious patterns in prompts / markdown
SUSPICIOUS_PROMPT_PATTERNS = [
    (re.compile(r"[\u200B\u200C\u200D\uFEFF]"), "Phát hiện ký tự Unicode ẩn (Zero-width spaces) có thể dùng cho Prompt Injection"),
    (re.compile(r"(?:curl|wget|fetch|axios|http)\s+[^\n]*?(?:webhook\.site|requestbin|ngrok-free\.app|burpcollaborator)", re.I), "Phát hiện URL webhook/exfiltration đáng ngờ"),
    (re.compile(r"(?:cat|read|curl|upload)[^\n]*?(?:\.env|\.ssh/id_rsa|\.aws/credentials|\.gemini/config)", re.I), "Chỉ dẫn cố gắng đọc hoặc trích xuất secret/file nhạy cảm"),
    (re.compile(r"rm\s+-rf\s+(?:/|/\*|~|\$HOME)", re.I), "Lệnh xóa hệ thống cực kỳ nguy hiểm (rm -rf /)"),
    (re.compile(r"(?:format\s+[c-z]:|mkfs\.[a-z0-9]+)", re.I), "Lệnh format ổ đĩa / partition"),
    (re.compile(r"(?:\:\{\s*\:\s*\|\s*\:\s*\&\s*\}\;\s*\:)", re.I), "Fork bomb script"),
]

# Ast checks for python scripts
DANGEROUS_CALLS = {"eval", "exec"}


@dataclass
class SecurityReport:
    skill_name: str
    is_safe: bool = True
    critical_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        if not self.is_safe:
            items = "\n".join(f"- 🔴 **Critical**: {err}" for err in self.critical_errors)
            warns = "\n".join(f"- ⚠️ **Warning**: {w}" for w in self.warnings)
            return (
                f"### 🛡️ Báo cáo Bảo mật: ❌ KHÔNG AN TOÀN (FAILED)\n"
                f"{items}\n"
                f"{warns if warns else ''}"
            )
        elif self.warnings:
            warns = "\n".join(f"- ⚠️ **Warning**: {w}" for w in self.warnings)
            return (
                f"### 🛡️ Báo cáo Bảo mật: ⚠️ CẢNH BÁO (PASSED WITH WARNINGS)\n"
                f"{warns}"
            )
        else:
            return (
                f"### 🛡️ Báo cáo Bảo mật: ✅ AN TOÀN (PASSED)\n"
                f"- Không phát hiện mã độc, lệnh nguy hiểm hoặc dấu hiệu prompt injection ẩn."
            )


def scan_markdown_content(content: str, filename: str = "SKILL.md") -> Tuple[List[str], List[str]]:
    """Scan markdown file for hidden unicode, injection vectors, or suspicious exfiltration."""
    criticals = []
    warnings = []

    for pattern, message in SUSPICIOUS_PROMPT_PATTERNS:
        match = pattern.search(content)
        if match:
            if "Zero-width" in message or "exfiltration" in message or "nguy hiểm" in message:
                criticals.append(f"{filename}: {message} -> `{match.group(0)[:60]}`")
            else:
                warnings.append(f"{filename}: {message}")

    return criticals, warnings


class PythonASTVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.criticals: List[str] = []
        self.warnings: List[str] = []

    def visit_Call(self, node: ast.Call):
        # Check eval() / exec()
        if isinstance(node.func, ast.Name):
            if node.func.id in DANGEROUS_CALLS:
                self.criticals.append(
                    f"{self.filename}:{node.lineno}: Sử dụng hàm nguy hiểm '{node.func.id}()'"
                )
            elif node.func.id == "__import__":
                self.warnings.append(
                    f"{self.filename}:{node.lineno}: Dynamic import '__import__()' được phát hiện"
                )

        # Check os.system(...)
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                module_name = node.func.value.id
                method_name = node.func.attr
                if module_name == "os" and method_name == "system":
                    self.criticals.append(
                        f"{self.filename}:{node.lineno}: os.system() không an toàn. Hãy dùng subprocess có validation."
                    )
                elif module_name == "subprocess" and method_name in ("run", "Popen", "call"):
                    # Check for shell=True
                    for kw in node.keywords:
                        if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                            self.warnings.append(
                                f"{self.filename}:{node.lineno}: subprocess gọi với shell=True. Tiềm ẩn nguy cơ command injection."
                            )

        self.generic_visit(node)


def scan_python_script(py_path: Path) -> Tuple[List[str], List[str]]:
    """Scan a Python script using AST and check for PEP 723."""
    criticals = []
    warnings = []
    rel_name = py_path.name

    try:
        content = py_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        criticals.append(f"Không thể đọc file {rel_name}: {e}")
        return criticals, warnings

    if "# /// script" not in content:
        warnings.append(f"{rel_name}: Thiếu header PEP 723 (# /// script)")

    try:
        tree = ast.parse(content, filename=str(py_path))
        visitor = PythonASTVisitor(rel_name)
        visitor.visit(tree)
        criticals.extend(visitor.criticals)
        warnings.extend(visitor.warnings)
    except SyntaxError as e:
        criticals.append(f"{rel_name}:{e.lineno}: Lỗi cú pháp Python (SyntaxError) - {e.msg}")

    return criticals, warnings


def scan_skill_directory(skill_dir: Path) -> SecurityReport:
    """Run full security scan across the entire skill directory."""
    skill_name = skill_dir.name
    report = SecurityReport(skill_name=skill_name)

    # 1. Scan SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8", errors="replace")
        crits, warns = scan_markdown_content(content, "SKILL.md")
        report.critical_errors.extend(crits)
        report.warnings.extend(warns)
    else:
        report.critical_errors.append("Không tìm thấy file SKILL.md")

    # 2. Scan references/
    ref_dir = skill_dir / "references"
    if ref_dir.exists() and ref_dir.is_dir():
        for md_file in ref_dir.glob("*.md"):
            content = md_file.read_text(encoding="utf-8", errors="replace")
            crits, warns = scan_markdown_content(content, f"references/{md_file.name}")
            report.critical_errors.extend(crits)
            report.warnings.extend(warns)

    # 3. Scan scripts/
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        for py_file in scripts_dir.glob("*.py"):
            crits, warns = scan_python_script(py_file)
            report.critical_errors.extend(crits)
            report.warnings.extend(warns)

        for sh_file in scripts_dir.glob("*.sh"):
            content = sh_file.read_text(encoding="utf-8", errors="replace")
            if "curl " in content and "| bash" in content:
                report.critical_errors.append(f"scripts/{sh_file.name}: Phát hiện pattern nguy hiểm 'curl | bash'")
            if "wget " in content and "| sh" in content:
                report.critical_errors.append(f"scripts/{sh_file.name}: Phát hiện pattern nguy hiểm 'wget | sh'")

    if report.critical_errors:
        report.is_safe = False

    return report


if __name__ == "__main__":
    import sys
    test_target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("skills/general/git-workflow")
    rep = scan_skill_directory(test_target)
    print(rep.to_markdown())
