#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Skill Ingestion & Automation Orchestrator for Skill-Repository.
Runs the 4-Gate Ingestion Pipeline:
  Gate 1: Trusted Source & License Verification
  Gate 2: Deduplication & Semantic Overlap Check
  Gate 3: Security & Static Analysis (Prompt Injection & SAST)
  Gate 4: Normalization, Local Test Validation & PR Scorecard Generation
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add scripts directory to path to import ingestion modules
SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from ingest.dedup import (
    ExistingSkill,
    OverlapReport,
    check_candidate_overlap,
    load_existing_skills,
)
from ingest.normalizer import normalize_skill_directory, sanitize_skill_name
from ingest.security import SecurityReport, scan_skill_directory


@dataclass
class IngestionResult:
    skill_name: str
    target_category: str
    source_repo: str
    verdict: str  # "ACCEPTED", "REJECTED_DUPLICATE", "REJECTED_SECURITY", "REJECTED_VALIDATION"
    overlap_report: Optional[OverlapReport] = None
    security_report: Optional[SecurityReport] = None
    validation_passed: bool = False
    details: str = ""

    def generate_pr_body(self) -> str:
        """Generate GitHub PR body with comprehensive Scorecard."""
        status_badge = "✅ SẴN SÀNG DUYỆT" if self.verdict == "ACCEPTED" else f"⚠️ CẦN LƯU Ý ({self.verdict})"
        
        md = [
            f"## 🤖 Báo cáo Tự động Đồng bộ Skill: `{self.skill_name}`",
            "",
            f"| Thông tin | Chi tiết |",
            f"| :--- | :--- |",
            f"| **Skill** | `{self.skill_name}` |",
            f"| **Danh mục** | `skills/{self.target_category}/` |",
            f"| **Nguồn gốc** | `{self.source_repo}` |",
            f"| **Trạng thái Gate** | **{status_badge}** |",
            "",
            "---",
            "",
            "### 1. Kết quả Kiểm tra Trùng lặp (Deduplication Gate)",
        ]

        if self.overlap_report:
            md.append(self.overlap_report.to_markdown())
        else:
            md.append("- Không có dữ liệu trùng lặp.")

        md.extend([
            "",
            "---",
            "",
            "### 2. Kết quả Quét An ninh & Mã độc (Security Gate)",
        ])

        if self.security_report:
            md.append(self.security_report.to_markdown())
        else:
            md.append("- Chưa chạy quét an ninh.")

        md.extend([
            "",
            "---",
            "",
            "### 3. Kiểm tra Cấu trúc & Linter (Quality Gate)",
            f"- Chuẩn hóa cấu trúc: {'✅ Đạt chuẩn' if self.validation_passed else '❌ Có lỗi'}",
            "",
            "### 📌 Hướng dẫn Review cho Maintainer:",
            "- [ ] Xem diff nội dung hướng dẫn tại `SKILL.md`.",
            "- [ ] Kiểm tra các file script nếu có trong `scripts/`.",
            "- [ ] Nhấn **Merge pull request** nếu kỹ năng hữu ích và an toàn.",
        ])

        return "\n".join(md)


def github_api_get(url: str, token: Optional[str] = None) -> Any:
    """Fetch JSON from GitHub API with optional auth token."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Skill-Repository-Sync-Bot")
    req.add_header("Accept", "application/vnd.github.v3+json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def download_github_file(download_url: str, dest_path: Path, token: Optional[str] = None):
    """Download single raw file from GitHub."""
    req = urllib.request.Request(download_url)
    req.add_header("User-Agent", "Skill-Repository-Sync-Bot")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(req, timeout=30) as response:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_bytes(response.read())


def download_github_folder(
    owner: str,
    repo: str,
    path: str,
    target_dir: Path,
    token: Optional[str] = None,
    ref: str = "main"
) -> bool:
    """Recursively download directory contents from GitHub via contents API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}"
    try:
        items = github_api_get(url, token)
    except Exception as e:
        print(f"[ERROR] Failed to fetch folder {path} from {owner}/{repo}: {e}")
        return False

    if not isinstance(items, list):
        return False

    for item in items:
        item_type = item.get("type")
        item_path = item.get("path")
        item_name = item.get("name")

        if item_type == "file":
            download_url = item.get("download_url")
            if download_url:
                dest = target_dir / item_name
                download_github_file(download_url, dest, token)
        elif item_type == "dir":
            sub_dir = target_dir / item_name
            sub_dir.mkdir(parents=True, exist_ok=True)
            download_github_folder(owner, repo, item_path, sub_dir, token, ref)

    return True


def run_local_validation() -> bool:
    """Run existing python and node validators."""
    try:
        py_res = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "validate_skills.py")],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        if py_res.returncode != 0:
            print(f"[FAIL] validate_skills.py failed:\n{py_res.stdout}\n{py_res.stderr}")
            return False

        node_res = subprocess.run(
            ["node", str(SCRIPTS_DIR / "validate-skills.js")],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        if node_res.returncode != 0:
            print(f"[FAIL] validate-skills.js failed:\n{node_res.stdout}\n{node_res.stderr}")
            return False

        return True
    except Exception as e:
        print(f"[WARN] Error running validation script: {e}")
        return False


def update_docs_catalog(skill_name: str, desc: str, category: str):
    """Register ingested skill into SKILLS_MAP.md and README.md."""
    # 1. Update SKILLS_MAP.md
    skills_map_path = REPO_ROOT / "SKILLS_MAP.md"
    if skills_map_path.exists():
        content = skills_map_path.read_text(encoding="utf-8")
        if f"**`{skill_name}`**" not in content:
            section_headers = {
                "general": "### 1. General & Engineering Lifecycle Skills",
                "anthropic": "### 2. Anthropic Ecosystem Skills",
                "openai": "### 3. OpenAI Ecosystem Skills",
            }
            header = section_headers.get(category)
            if header and header in content:
                sec_start = content.find(header)
                next_sec = content.find("### ", sec_start + len(header))
                if next_sec == -1:
                    next_sec = content.find("---", sec_start + len(header))
                
                sec_body = content[sec_start:next_sec] if next_sec != -1 else content[sec_start:]
                lines = sec_body.splitlines()
                last_table_idx = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith("|") and line.strip().endswith("|"):
                        last_table_idx = i
                
                if last_table_idx != -1:
                    clean_desc = desc.replace("\n", " ").strip()
                    if len(clean_desc) > 220:
                        clean_desc = clean_desc[:217] + "..."
                    raw_url = f"https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/{category}/{skill_name}/SKILL.md"
                    label = "Anthropic Ecosystem" if category == "anthropic" else ("OpenAI Ecosystem" if category == "openai" else "General")
                    new_row = f"| **`{skill_name}`** | **{skill_name}**: {clean_desc} | {label} | [Fetch Raw]({raw_url}) |"
                    lines.insert(last_table_idx + 1, new_row)
                    new_sec_body = "\n".join(lines)
                    if next_sec != -1:
                        content = content[:sec_start] + new_sec_body + content[next_sec:]
                    else:
                        content = content[:sec_start] + new_sec_body
                    skills_map_path.write_text(content, encoding="utf-8")
                    print(f"-> Đã tự động cập nhật SKILLS_MAP.md cho '{skill_name}'")

    # 2. Update README.md
    readme_path = REPO_ROOT / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        if f"[`{skill_name}`]" not in content:
            section_headers = {
                "general": "### General & Engineering Lifecycle",
                "anthropic": "### Anthropic Ecosystem",
                "openai": "### OpenAI Ecosystem",
            }
            header = section_headers.get(category)
            if header and header in content:
                sec_start = content.find(header)
                next_sec = content.find("### ", sec_start + len(header))
                if next_sec == -1:
                    next_sec = content.find("---", sec_start + len(header))
                
                sec_body = content[sec_start:next_sec] if next_sec != -1 else content[sec_start:]
                lines = sec_body.splitlines()
                last_table_idx = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith("|") and line.strip().endswith("|"):
                        last_table_idx = i
                
                if last_table_idx != -1:
                    clean_desc = desc.replace("\n", " ").strip()
                    if len(clean_desc) > 150:
                        clean_desc = clean_desc[:147] + "..."
                    label = "Anthropic Ecosystem" if category == "anthropic" else ("OpenAI Ecosystem" if category == "openai" else "General")
                    new_row = f"| **[`{skill_name}`](skills/{category}/{skill_name}/)** | {clean_desc} | {label} | [Explore](skills/{category}/{skill_name}/SKILL.md) |"
                    lines.insert(last_table_idx + 1, new_row)
                    new_sec_body = "\n".join(lines)
                    if next_sec != -1:
                        content = content[:sec_start] + new_sec_body + content[next_sec:]
                    else:
                        content = content[:sec_start] + new_sec_body
                    readme_path.write_text(content, encoding="utf-8")
                    print(f"-> Đã tự động cập nhật README.md cho '{skill_name}'")


def process_candidate_skill(
    candidate_dir: Path,
    source_repo: str,
    target_category: str = "general",
    dry_run: bool = False
) -> IngestionResult:
    """Run a candidate skill through the 4-gate ingestion pipeline."""
    raw_name = candidate_dir.name
    skill_name = sanitize_skill_name(raw_name)

    print(f"\n==================================================")
    print(f"Bắt đầu kiểm duyệt Skill ứng viên: '{skill_name}'")
    print(f"Nguồn: {source_repo} | Danh mục dự kiến: skills/{target_category}/")
    print(f"==================================================")

    # Gate 1: Check SKILL.md existence
    skill_md = candidate_dir / "SKILL.md"
    if not skill_md.exists():
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_VALIDATION",
            details="Không có file SKILL.md"
        )

    # Read content & description
    content = skill_md.read_text(encoding="utf-8", errors="replace")
    desc = ""
    for line in content.splitlines()[:30]:
        if line.strip().startswith("description:"):
            desc = line.split(":", 1)[1].strip().strip('"').strip("'")
            break

    # Gate 2: Deduplication Check
    print("-> Đang kiểm tra trùng lặp với danh mục kỹ năng hiện có...")
    existing_skills = load_existing_skills(REPO_ROOT)
    overlap_rep = check_candidate_overlap(skill_name, desc, content, existing_skills)
    print(f"   [Kết quả]: {overlap_rep.verdict} (Score: {int(overlap_rep.similarity_score * 100)}%)")
    if overlap_rep.closest_skill:
        print(f"   [Gần nhất]: {overlap_rep.closest_skill}")

    if overlap_rep.verdict in ("EXACT_NAME", "HIGH_OVERLAP"):
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_DUPLICATE",
            overlap_report=overlap_rep,
            details=overlap_rep.recommendation
        )

    # Gate 3: Security & Malware Scan
    print("-> Đang quét an ninh mã độc và prompt injection...")
    sec_rep = scan_skill_directory(candidate_dir)
    if not sec_rep.is_safe:
        print("   [FAILED]: Phát hiện cảnh báo bảo mật nghiêm trọng!")
        for err in sec_rep.critical_errors:
            print(f"   - {err}")
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_SECURITY",
            overlap_report=overlap_rep,
            security_report=sec_rep,
            details="Không vượt qua bài quét bảo mật."
        )
    else:
        print("   [PASSED]: Quét an ninh thành công.")

    # Gate 4: Normalization
    print("-> Đang chuẩn hóa cấu trúc thư mục, frontmatter và evals...")
    norm_success, changes = normalize_skill_directory(candidate_dir, expected_name=skill_name)
    for ch in changes:
        print(f"   + {ch}")

    if not norm_success:
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_VALIDATION",
            overlap_report=overlap_rep,
            security_report=sec_rep,
            details="Không thể chuẩn hóa tên hoặc cấu trúc."
        )

    # Destination
    dest_category_dir = REPO_ROOT / "skills" / target_category
    dest_skill_dir = dest_category_dir / skill_name

    if dry_run:
        print(f"-> [DRY-RUN] Sẵn sàng chuyển tới: {dest_skill_dir}")
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="ACCEPTED",
            overlap_report=overlap_rep,
            security_report=sec_rep,
            validation_passed=True,
            details="Kiểm tra hoàn tất (Dry-run)."
        )

    # Copy to destination
    dest_category_dir.mkdir(parents=True, exist_ok=True)
    if dest_skill_dir.exists():
        shutil.rmtree(dest_skill_dir)
    shutil.copytree(candidate_dir, dest_skill_dir)
    print(f"-> Đã chuyển skill vào: {dest_skill_dir}")

    # Auto-register into SKILLS_MAP.md and README.md
    update_docs_catalog(skill_name, desc, target_category)

    # Run global repo validation
    print("-> Chạy bộ validator tổng thể của repository...")
    val_passed = run_local_validation()

    return IngestionResult(
        skill_name=skill_name,
        target_category=target_category,
        source_repo=source_repo,
        verdict="ACCEPTED" if val_passed else "REJECTED_VALIDATION",
        overlap_report=overlap_rep,
        security_report=sec_rep,
        validation_passed=val_passed,
        details="Đã tích hợp thành công vào repository." if val_passed else "Lỗi validation sau khi copy."
    )


def main():
    parser = argparse.ArgumentParser(description="Skill Ingestion Pipeline CLI")
    parser.add_argument("--sources-file", default=str(SCRIPTS_DIR / "ingest" / "sources.json"), help="Path to sources.json")
    parser.add_argument("--check-local", type=str, help="Check and scan a local directory")
    parser.add_argument("--category", default="general", choices=["general", "anthropic", "openai"], help="Target category")
    parser.add_argument("--dry-run", action="store_true", help="Perform checks without copying files")
    parser.add_argument("--output-pr-data", type=str, help="Path to write PR scorecard markdown / json")
    parser.add_argument("--github-repo", type=str, help="Ingest directly from GitHub repo (e.g. owner/repo)")
    parser.add_argument("--skill-path", type=str, help="Path inside GitHub repo to the skill")

    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN")

    # Write to GitHub Step Summary if running inside GitHub Actions
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        try:
            with open(step_summary, "a", encoding="utf-8") as f:
                f.write("\n" + result.generate_pr_body() + "\n")
        except Exception as e:
            print(f"[WARN] Failed to write step summary: {e}")

    # Write outputs to GITHUB_OUTPUT
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        try:
            with open(github_output, "a", encoding="utf-8") as f:
                f.write(f"verdict={result.verdict}\n")
                f.write(f"skill_name={result.skill_name}\n")
                f.write(f"has_pr={'true' if result.verdict == 'ACCEPTED' and not args.dry_run else 'false'}\n")
        except Exception as e:
            print(f"[WARN] Failed to write github output: {e}")

    # Mode 1: Check a local skill directory
    if args.check_local:
        local_path = Path(args.check_local).resolve()
        if not local_path.exists():
            print(f"[ERROR] Path does not exist: {local_path}")
            sys.exit(1)
        result = process_candidate_skill(
            candidate_dir=local_path,
            source_repo="local",
            target_category=args.category,
            dry_run=args.dry_run
        )
        if args.output_pr_data:
            Path(args.output_pr_data).write_text(result.generate_pr_body(), encoding="utf-8")
        print("\n" + result.generate_pr_body())
        sys.exit(0)

    # Mode 2: Ingest directly from a specific GitHub repo path
    if args.github_repo and args.skill_path:
        owner, repo = args.github_repo.split("/")
        skill_name = Path(args.skill_path).name
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_skill_dir = Path(tmp_dir) / skill_name
            tmp_skill_dir.mkdir(parents=True, exist_ok=True)
            print(f"Đang tải skill '{skill_name}' từ {args.github_repo} ({args.skill_path})...")
            success = download_github_folder(owner, repo, args.skill_path, tmp_skill_dir, token)
            if not success:
                print(f"[ERROR] Không thể tải skill từ GitHub.")
                sys.exit(1)

            result = process_candidate_skill(
                candidate_dir=tmp_skill_dir,
                source_repo=f"{args.github_repo}/{args.skill_path}",
                target_category=args.category,
                dry_run=args.dry_run
            )
            if args.output_pr_data:
                Path(args.output_pr_data).write_text(result.generate_pr_body(), encoding="utf-8")
            print("\n" + result.generate_pr_body())

            # Write step summary & output
            if step_summary:
                try:
                    with open(step_summary, "a", encoding="utf-8") as f:
                        f.write("\n" + result.generate_pr_body() + "\n")
                except Exception:
                    pass
            if github_output:
                try:
                    with open(github_output, "a", encoding="utf-8") as f:
                        f.write(f"verdict={result.verdict}\n")
                        f.write(f"skill_name={result.skill_name}\n")
                        f.write(f"has_pr={'true' if result.verdict == 'ACCEPTED' and not args.dry_run else 'false'}\n")
                except Exception:
                    pass

            sys.exit(0)

    # Mode 3: Sync from sources.json
    sources_file = Path(args.sources_file)
    if not sources_file.exists():
        print(f"[ERROR] Sources file not found: {sources_file}")
        sys.exit(1)

    with open(sources_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    trusted = config.get("trusted_sources", [])
    print(f"Đã nạp {len(trusted)} nguồn uy tín từ {sources_file.name}")
    print("Gợi ý: Dùng --github-repo <owner/repo> --skill-path <path> để ingest một skill cụ thể.")


if __name__ == "__main__":
    main()
