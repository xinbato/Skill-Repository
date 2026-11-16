# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
test_hygiene.py — Repository hygiene and anti-bloat test suite.

Verifies that:
1. No OS debris, editor leftovers, build caches, or temporary files are tracked.
2. No binary executables exist inside skills/ or commands/.
3. No merge conflict markers exist in tracked files.
4. No hardcoded secret tokens or private keys are exposed.
5. .gitignore comprehensively blocks all forbidden patterns.
6. Skill directories adhere to agentskills.io specifications without bloat.
"""

import fnmatch
import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / "skills"
COMMANDS_DIR = ROOT_DIR / "commands"

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


def get_tracked_files() -> list[str]:
    """Retrieve list of files tracked by git."""
    try:
        out = subprocess.check_output(["git", "ls-files"], cwd=ROOT_DIR, text=True)
        return [f.strip() for f in out.splitlines() if f.strip()]
    except Exception as exc:
        raise RuntimeError(f"Failed to run git ls-files: {exc}")


class TestRepositoryHygiene(unittest.TestCase):
    """Automated enforcement of repository cleanliness, hygiene, and anti-bloat."""

    @classmethod
    def setUpClass(cls):
        cls.tracked_files = get_tracked_files()

    def test_no_tracked_forbidden_artifacts(self):
        """Verify that no OS junk, IDE files, build caches, or credentials are tracked."""
        violations = []
        for file_path in self.tracked_files:
            posix_path = file_path.replace("\\", "/")
            basename = Path(file_path).name

            for pattern in FORBIDDEN_TRACKED_PATTERNS:
                if fnmatch.fnmatch(posix_path, pattern) or fnmatch.fnmatch(basename, pattern):
                    violations.append((file_path, pattern))

        self.assertEqual(
            violations,
            [],
            f"Found {len(violations)} forbidden tracked files:\n"
            + "\n".join(f"  - {f} (matched pattern: {p})" for f, p in violations),
        )

    def test_no_binary_executables_in_skills_or_commands(self):
        """Verify no compiled binaries or executables exist inside skills/ or commands/."""
        violations = []
        for file_path in self.tracked_files:
            posix = file_path.replace("\\", "/")
            if not (posix.startswith("skills/") or posix.startswith("commands/")):
                continue

            ext = Path(file_path).suffix.lower()
            if ext in FORBIDDEN_EXEC_EXTS:
                violations.append((file_path, f"forbidden extension {ext}"))
                continue

            # Check executable magic bytes
            full_path = ROOT_DIR / file_path
            if full_path.exists() and full_path.is_file():
                try:
                    with open(full_path, "rb") as f:
                        magic = f.read(4)
                        if magic.startswith(b"MZ") or magic.startswith(b"\x7fELF"):
                            violations.append((file_path, f"binary executable header: {magic!r}"))
                        elif magic in (b"\xfe\xed\xfa\xce", b"\xfe\xed\xfa\xcf", b"\xce\xfa\xed\xfe", b"\xcf\xfa\xed\xfe"):
                            violations.append((file_path, f"Mach-O binary header: {magic!r}"))
                except Exception:
                    pass

        self.assertEqual(
            violations,
            [],
            f"Found {len(violations)} executable/binary files in skills or commands:\n"
            + "\n".join(f"  - {f}: {reason}" for f, reason in violations),
        )

    def test_no_merge_conflict_markers(self):
        """Verify no unmerged git conflict markers exist in tracked files."""
        violations = []
        for file_path in self.tracked_files:
            full_path = ROOT_DIR / file_path
            if not full_path.exists() or not full_path.is_file():
                continue

            try:
                content = full_path.read_text(encoding="utf-8", errors="ignore")
                for pat in CONFLICT_PATTERNS:
                    if pat.search(content):
                        violations.append(file_path)
                        break
            except Exception:
                pass

        self.assertEqual(
            violations,
            [],
            f"Found {len(violations)} files with merge conflict markers:\n"
            + "\n".join(f"  - {f}" for f in violations),
        )

    def test_no_hardcoded_secrets(self):
        """Verify that tracked files do not expose live credentials, API keys, or private keys."""
        violations = []
        for file_path in self.tracked_files:
            full_path = ROOT_DIR / file_path
            if not full_path.exists() or not full_path.is_file():
                continue

            # Skip test fixtures that intentionally test secret scanners
            posix = file_path.replace("\\", "/")
            if "scripts/staged-secret-scan-test.js" in posix or "evals/fixtures" in posix:
                continue

            try:
                content = full_path.read_text(encoding="utf-8", errors="ignore")
                for pat, label in SECRET_PATTERNS:
                    m = pat.search(content)
                    if m:
                        masked = m.group(0)[:8] + "..."
                        violations.append((file_path, f"{label} ({masked})"))
            except Exception:
                pass

        self.assertEqual(
            violations,
            [],
            f"Found {len(violations)} potential secret leaks in tracked files:\n"
            + "\n".join(f"  - {f}: {reason}" for f, reason in violations),
        )

    def test_gitignore_rules(self):
        """Verify .gitignore contains comprehensive coverage blocking forbidden artifacts."""
        gitignore_path = ROOT_DIR / ".gitignore"
        self.assertTrue(gitignore_path.exists(), ".gitignore must exist")

        content = gitignore_path.read_text(encoding="utf-8")
        required_patterns = [
            "__pycache__/",
            "*.py[cod]",
            ".DS_Store",
            "Thumbs.db",
            "desktop.ini",
            ".vscode/",
            ".idea/",
            "node_modules/",
            ".pytest_cache/",
            ".coverage",
            "*.log",
            ".env",
            "*.pem",
            "*.key",
            "*.exe",
            "*.dll",
            "**/evals/output/",
            "**/evals/results/",
        ]

        missing = [p for p in required_patterns if p not in content]
        self.assertEqual(
            missing,
            [],
            f"Missing required patterns in .gitignore:\n"
            + "\n".join(f"  - {p}" for p in missing),
        )

    def test_general_skills_spec_directory_compliance(self):
        """Verify general skills strictly adhere to agentskills.io standard directories."""
        general_dir = SKILLS_DIR / "general"
        if not general_dir.exists():
            return

        allowed_entries = {"SKILL.md", "references", "scripts", "assets", "evals"}
        violations = []

        for skill_dir in general_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue

            for item in skill_dir.iterdir():
                if item.name not in allowed_entries:
                    violations.append(f"{skill_dir.name}/{item.name}")

            # Verify no evals/output directory exists
            output_dir = skill_dir / "evals" / "output"
            if output_dir.exists():
                violations.append(f"{skill_dir.name}/evals/output (runtime artifact)")

        self.assertEqual(
            violations,
            [],
            f"Found {len(violations)} non-standard entries in general skills:\n"
            + "\n".join(f"  - {v}" for v in violations),
        )


if __name__ == "__main__":
    unittest.main()
