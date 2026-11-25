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

# Suspicious patterns in prompts / markdown: (pattern, message, is_critical)
SUSPICIOUS_PROMPT_PATTERNS = [
    (
        re.compile(r"[\u200B\u200C\u200D\uFEFF]"),
        "Phát hiện ký tự Unicode ẩn (Zero-width spaces) có thể dùng cho Prompt Injection",
        True
    ),
    (
        re.compile(
            r"(?:https?://|[^\w]|^)(?:[a-zA-Z0-9.-]+\.)?(?:webhook\.site|requestbin\.(?:net|com)|ngrok-free\.app|burpcollaborator\.net|pipedream\.net|oastify\.com|interactsh\.com|beeceptor\.com)",
            re.I
        ),
        "Phát hiện URL webhook/exfiltration đáng ngờ",
        True
    ),
    (
        re.compile(
            r"(?:cat|read|curl|upload|type|Get-Content|scp|nc|ncat|netcat)[^\n]*?(?:\.env|\.ssh[/\\].*|\.aws[/\\].*|\.gemini[/\\].*|\.git-credentials)",
            re.I
        ),
        "Chỉ dẫn cố gắng đọc hoặc trích xuất secret/file nhạy cảm",
        True
    ),
    (
        re.compile(r"(?:rm\s+-rf\s+(?:/|/\*|~|\$HOME)|del\s+/[fFqsS]+\s+[cC]:\\|rd\s+/[sS]\s+/[qQ]\s+[cC]:\\)", re.I),
        "Lệnh xóa hệ thống cực kỳ nguy hiểm (rm -rf /)",
        True
    ),
    (
        re.compile(r"(?:format\s+[c-z]:|mkfs\.[a-z0-9]+)", re.I),
        "Lệnh format ổ đĩa / partition",
        True
    ),
    (
        re.compile(r"(?:\:\{\s*\:\s*\|\s*\:\s*\&\s*\}\;\s*\:)", re.I),
        "Fork bomb script",
        True
    ),
    (
        re.compile(r"(?:bash\s+-i\s+>&|nc\s+-[e|c]\s+|ncat\s+-[e|c]\s+)", re.I),
        "Lệnh reverse shell nguy hiểm",
        True
    ),
]


@dataclass
class SecurityReport:
    skill_name: str
    is_safe: bool = True
    critical_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        if not self.is_safe:
            items = "\n".join(f"- [CRITICAL]: {err}" for err in self.critical_errors)
            warns = "\n".join(f"- [WARNING]: {w}" for w in self.warnings)
            return (
                f"### Bao cao Bao mat: KHONG AN TOAN (FAILED)\n"
                f"{items}\n"
                f"{warns if warns else ''}"
            )
        elif self.warnings:
            warns = "\n".join(f"- [WARNING]: {w}" for w in self.warnings)
            return (
                f"### Bao cao Bao mat: CANH BAO (PASSED WITH WARNINGS)\n"
                f"{warns}"
            )
        else:
            return (
                f"### Bao cao Bao mat: AN TOAN (PASSED)\n"
                f"- Không phát hiện mã độc, lệnh nguy hiểm hoặc dấu hiệu prompt injection ẩn."
            )


def scan_markdown_content(content: str, filename: str = "SKILL.md") -> Tuple[List[str], List[str]]:
    """Scan markdown file for hidden unicode, injection vectors, or suspicious exfiltration."""
    criticals = []
    warnings = []

    for pattern, message, is_critical in SUSPICIOUS_PROMPT_PATTERNS:
        match = pattern.search(content)
        if match:
            matched_snippet = match.group(0)[:60].replace("\n", " ")
            formatted = f"{filename}: {message} -> `{matched_snippet}`"
            if is_critical:
                criticals.append(formatted)
            else:
                warnings.append(formatted)

    return criticals, warnings


class PythonASTVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.criticals: List[str] = []
        self.warnings: List[str] = []
        self.subprocess_aliases = {"subprocess"}
        self.os_aliases = {"os"}
        self.subprocess_funcs = set()
        self.os_funcs = set()

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name == "subprocess":
                self.subprocess_aliases.add(alias.asname or "subprocess")
            elif alias.name == "os":
                self.os_aliases.add(alias.asname or "os")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module == "subprocess":
            for alias in node.names:
                self.subprocess_funcs.add(alias.asname or alias.name)
        elif node.module == "os":
            for alias in node.names:
                self.os_funcs.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # 1. Eval / Exec / getattr evasion
        if isinstance(node.func, ast.Name):
            if node.func.id in ("eval", "exec"):
                self.criticals.append(
                    f"{self.filename}:{node.lineno}: Sử dụng hàm nguy hiểm '{node.func.id}()'"
                )
            elif node.func.id == "__import__":
                self.warnings.append(
                    f"{self.filename}:{node.lineno}: Dynamic import '__import__()' được phát hiện"
                )
            elif node.func.id == "getattr":
                if (
                    len(node.args) >= 2
                    and isinstance(node.args[1], ast.Constant)
                    and node.args[1].value in ("eval", "exec")
                ):
                    self.criticals.append(
                        f"{self.filename}:{node.lineno}: Sử dụng getattr nguy hiểm lấy hàm '{node.args[1].value}()'"
                    )
            elif node.func.id in self.os_funcs:
                if node.func.id in ("system", "popen"):
                    self.criticals.append(
                        f"{self.filename}:{node.lineno}: os.{node.func.id}() không an toàn."
                    )
            elif node.func.id in self.subprocess_funcs:
                self._check_subprocess_shell(node)

        elif isinstance(node.func, ast.Attribute):
            attr = node.func.attr
            # Check builtins.eval / __builtins__.eval / any_obj.eval
            if attr in ("eval", "exec"):
                self.criticals.append(
                    f"{self.filename}:{node.lineno}: Sử dụng hàm nguy hiểm '{attr}()'"
                )

            if isinstance(node.func.value, ast.Name):
                val_id = node.func.value.id
                if val_id in self.os_aliases:
                    if attr in (
                        "system", "popen", "spawnl", "spawnle", "spawnlp",
                        "spawnlpe", "spawnp", "spawnv", "spawnve", "spawnvp", "spawnvpe"
                    ):
                        self.criticals.append(
                            f"{self.filename}:{node.lineno}: os.{attr}() không an toàn. Hãy dùng subprocess có validation."
                        )
                elif val_id in self.subprocess_aliases:
                    if attr in ("run", "Popen", "call", "check_output", "check_call"):
                        self._check_subprocess_shell(node)
                elif val_id == "importlib" and attr in ("import_module", "__import__"):
                    self.warnings.append(
                        f"{self.filename}:{node.lineno}: Dynamic import '{val_id}.{attr}()' được phát hiện"
                    )

        self.generic_visit(node)

    def _check_subprocess_shell(self, node: ast.Call):
        func_name = getattr(node.func, "attr", getattr(node.func, "id", "subprocess"))
        for kw in node.keywords:
            if kw.arg == "shell":
                if isinstance(kw.value, ast.Constant):
                    if bool(kw.value.value):
                        self.warnings.append(
                            f"{self.filename}:{node.lineno}: {func_name}() gọi với shell={kw.value.value}. Tiềm ẩn nguy cơ command injection."
                        )
                else:
                    self.warnings.append(
                        f"{self.filename}:{node.lineno}: {func_name}() gọi với dynamic shell argument. Tiềm ẩn nguy cơ command injection."
                    )


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

    # 2. Scan references/ (recursive)
    ref_dir = skill_dir / "references"
    if ref_dir.exists() and ref_dir.is_dir():
        for md_file in ref_dir.rglob("*.md"):
            rel = md_file.relative_to(skill_dir).as_posix()
            content = md_file.read_text(encoding="utf-8", errors="replace")
            crits, warns = scan_markdown_content(content, rel)
            report.critical_errors.extend(crits)
            report.warnings.extend(warns)

    # 3. Scan scripts/ (recursive)
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        for py_file in scripts_dir.rglob("*.py"):
            crits, warns = scan_python_script(py_file)
            report.critical_errors.extend(crits)
            report.warnings.extend(warns)

        for sh_file in scripts_dir.rglob("*.sh"):
            rel = sh_file.relative_to(skill_dir).as_posix()
            content = sh_file.read_text(encoding="utf-8", errors="replace")
            if re.search(r"(?:curl|wget)\s+[^\n|;]+?\|\s*(?:sudo\s+)?(?:/bin/)?(?:bash|sh)", content, re.I):
                report.critical_errors.append(f"{rel}: Phát hiện pattern nguy hiểm 'curl/wget | bash'")

        for win_script in list(scripts_dir.rglob("*.ps1")) + list(scripts_dir.rglob("*.bat")) + list(scripts_dir.rglob("*.cmd")):
            rel = win_script.relative_to(skill_dir).as_posix()
            content = win_script.read_text(encoding="utf-8", errors="replace")
            if re.search(r"(?:iex|Invoke-Expression)[^\n]*?(?:DownloadString|DownloadFile|WebRequest|WebClient|curl|iwr)", content, re.I):
                report.critical_errors.append(f"{rel}: Phát hiện pattern nguy hiểm tải và thực thi mã từ xa")

        for js_file in list(scripts_dir.rglob("*.js")) + list(scripts_dir.rglob("*.mjs")) + list(scripts_dir.rglob("*.ts")):
            rel = js_file.relative_to(skill_dir).as_posix()
            content = js_file.read_text(encoding="utf-8", errors="replace")
            if re.search(r"\b(?:eval|Function)\s*\(", content):
                report.critical_errors.append(f"{rel}: Phát hiện hàm thực thi mã động nguy hiểm (eval/Function)")
            if re.search(r"child_process|execSync\s*\(|exec\s*\(", content):
                report.warnings.append(f"{rel}: Phát hiện lệnh gọi tiến trình con (child_process/exec)")

    if report.critical_errors:
        report.is_safe = False

    return report


if __name__ == "__main__":
    import sys
    test_target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("skills/general/git-workflow")
    rep = scan_skill_directory(test_target)
    print(rep.to_markdown())
