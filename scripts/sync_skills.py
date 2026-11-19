#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Skill Ingestion & Automation Orchestrator for Skill-Repository.
Runs the 4-Gate Ingestion Pipeline & Dual-Phase Synchronization Engine:
  Phase 1 (Ingest): Ingests new skills via 4-gate verification
    Gate 1: Trusted Source & License Verification
    Gate 2: Deduplication & Semantic Overlap Check
    Gate 3: Security & Static Analysis (Prompt Injection & SAST)
    Gate 4: Normalization, Local Test Validation & PR Scorecard Generation
  Phase 2 (Drift Update): Detects upstream content drift and safely updates existing skills
    Gate 3: Security & Malware Scan
    Gate 4: Normalization & Structural Validation
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
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
from ingest.drift import (
    DriftReport,
    check_drift_for_skill,
    compute_skill_content_sha,
    download_github_file,
    download_github_folder,
    github_api_get,
    load_sync_state,
    register_skill,
    save_sync_state,
    scan_all_drifts,
)
from ingest.normalizer import NAME_PATTERN, normalize_skill_directory, parse_frontmatter, sanitize_skill_name
from ingest.security import SecurityReport, scan_skill_directory


@dataclass
class IngestionResult:
    skill_name: str
    target_category: str
    source_repo: str
    verdict: str  # "ACCEPTED", "REJECTED_DUPLICATE", "REJECTED_SECURITY", "REJECTED_VALIDATION"
    overlap_report: Optional[OverlapReport] = None
    security_report: Optional[SecurityReport] = None
    drift_report: Optional[DriftReport] = None
    action: str = "ingest"  # "ingest" or "update"
    validation_passed: bool = False
    details: str = ""

    def generate_pr_body(self) -> str:
        """Generate GitHub PR body with comprehensive Scorecard for ingest or update."""
        status_badge = "✅ SẴN SÀNG DUYỆT" if self.verdict == "ACCEPTED" else f"⚠️ CẦN LƯU Ý ({self.verdict})"

        if self.action == "update":
            md = [
                f"## 🔄 Báo cáo Tự động Cập nhật Skill (Drift Update): `{self.skill_name}`",
                "",
                f"| Thông tin | Chi tiết |",
                f"| :--- | :--- |",
                f"| **Skill** | `{self.skill_name}` |",
                f"| **Danh mục** | `skills/{self.target_category}/` |",
                f"| **Nguồn gốc** | `{self.source_repo}` |",
                f"| **Hành động** | `Cập nhật nội dung (Upstream Drift)` |",
                f"| **Trạng thái Gate** | **{status_badge}** |",
                "",
                "---",
                "",
                "### 1. Kết quả Phát hiện Biến động (Drift Detection Gate)",
            ]

            if self.drift_report:
                md.append(self.drift_report.to_markdown())
            else:
                md.append("- Đã phát hiện thay đổi nội dung từ thượng nguồn.")

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
                f"- [ ] Xem diff nội dung cập nhật tại `skills/{self.target_category}/{self.skill_name}/`.",
                "- [ ] Kiểm tra các file script nếu có trong `scripts/`.",
                "- [ ] Nhấn **Merge pull request** để đồng bộ phiên bản mới nhất từ thượng nguồn.",
            ])

            return "\n".join(md)

        # Ingest Action
        md = [
            f"## 🤖 Báo cáo Tự động Đồng bộ Skill: `{self.skill_name}`",
            "",
            f"| Thông tin | Chi tiết |",
            f"| :--- | :--- |",
            f"| **Skill** | `{self.skill_name}` |",
            f"| **Danh mục** | `skills/{self.target_category}/` |",
            f"| **Nguồn gốc** | `{self.source_repo}` |",
            f"| **Hành động** | `Nạp mới kỹ năng (New Skill Ingest)` |",
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


def emit_github_outputs(result: IngestionResult, dry_run: bool = False):
    """Write outcome to GitHub Step Summary and GITHUB_OUTPUT."""
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        try:
            with open(step_summary, "a", encoding="utf-8") as f:
                f.write("\n" + result.generate_pr_body() + "\n")
        except Exception as e:
            print(f"[WARN] Failed to write step summary: {e}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        try:
            with open(github_output, "a", encoding="utf-8") as f:
                f.write(f"verdict={result.verdict}\n")
                f.write(f"skill_name={result.skill_name}\n")
                f.write(f"category={result.target_category}\n")
                f.write(f"action={result.action}\n")
                f.write(f"has_pr={'true' if result.verdict == 'ACCEPTED' and not dry_run else 'false'}\n")
        except Exception as e:
            print(f"[WARN] Failed to write github output: {e}")


def emit_no_skills_summary():
    """Write message when auto-sync finds no new skills or updates."""
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        try:
            with open(step_summary, "a", encoding="utf-8") as f:
                f.write("\n### 🤖 Auto-Sync Skill Ingestion & Update\n- Không phát hiện skill mới cần nạp hoặc cập nhật từ các nguồn tin cậy.\n")
        except Exception as e:
            print(f"[WARN] Failed to write step summary: {e}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        try:
            with open(github_output, "a", encoding="utf-8") as f:
                f.write("verdict=NO_NEW_SKILLS\ncategory=\nskill_name=\naction=\nhas_pr=false\n")
        except Exception as e:
            print(f"[WARN] Failed to write github output: {e}")


def is_license_allowed(cand_lic: Optional[str], allowed_licenses: Optional[List[str]]) -> bool:
    """Check if candidate license is in allowed_licenses or refers to repository terms."""
    if not allowed_licenses or not cand_lic:
        return True
    if cand_lic in allowed_licenses:
        return True
    lic_lower = cand_lic.lower()
    # Support upstream repository terms like 'Complete terms in LICENSE.txt'
    if "license.txt" in lic_lower or ("terms in license" in lic_lower):
        return True
    # Support exact matching ignoring case
    if any(cand_lic.lower() == al.lower() for al in allowed_licenses):
        return True
    return False


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
                "google": "### 4. Google Ecosystem Skills",
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
                    label = (
                        "Google Ecosystem" if category == "google" else
                        "Anthropic Ecosystem" if category == "anthropic" else
                        "OpenAI Ecosystem" if category == "openai" else "General"
                    )
                    new_row = f"| **`{skill_name}`** | **{skill_name}**: {clean_desc} | {label} | [Fetch Raw]({raw_url}) |"
                    lines.insert(last_table_idx + 1, new_row)
                    new_sec_body = "\n".join(lines).rstrip() + "\n\n"
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
                "google": "### Google Ecosystem",
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
                    label = (
                        "Google Ecosystem" if category == "google" else
                        "Anthropic Ecosystem" if category == "anthropic" else
                        "OpenAI Ecosystem" if category == "openai" else "General"
                    )
                    new_row = f"| **[`{skill_name}`](skills/{category}/{skill_name}/)** | {clean_desc} | {label} | [Explore](skills/{category}/{skill_name}/SKILL.md) |"
                    lines.insert(last_table_idx + 1, new_row)
                    new_sec_body = "\n".join(lines).rstrip() + "\n\n"
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
    dry_run: bool = False,
    allowed_licenses: Optional[List[str]] = None
) -> IngestionResult:
    """Run a candidate skill through the 4-gate ingestion pipeline."""
    raw_name = candidate_dir.name
    skill_name = sanitize_skill_name(raw_name)

    if not skill_name or not NAME_PATTERN.match(skill_name):
        return IngestionResult(
            skill_name=raw_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_VALIDATION",
            action="ingest",
            details=f"Tên skill không hợp lệ: '{raw_name}'"
        )

    print(f"\n==================================================")
    print(f"Bắt đầu kiểm duyệt Skill ứng viên: '{skill_name}'")
    print(f"Nguồn: {source_repo} | Danh mục dự kiến: skills/{target_category}/")
    print(f"==================================================")

    # Gate 1: Check SKILL.md existence & License
    skill_md = candidate_dir / "SKILL.md"
    if not skill_md.exists():
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_VALIDATION",
            action="ingest",
            details="Không có file SKILL.md"
        )

    content = skill_md.read_text(encoding="utf-8", errors="replace")
    fm, _ = parse_frontmatter(content)

    # License verification if allowed_licenses specified
    cand_lic = fm.get("license")
    if not is_license_allowed(cand_lic, allowed_licenses):
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_VALIDATION",
            action="ingest",
            details=f"License '{cand_lic}' không nằm trong danh sách được phép ({allowed_licenses})."
        )

    desc = fm.get("description", "")
    if not desc:
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
            action="ingest",
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
            action="ingest",
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
            action="ingest",
            details="Không thể chuẩn hóa tên hoặc cấu trúc."
        )

    # Destination paths with safety verification
    dest_category_dir = REPO_ROOT / "skills" / target_category
    dest_skill_dir = dest_category_dir / skill_name

    if (
        not skill_name
        or dest_skill_dir == dest_category_dir
        or dest_skill_dir == REPO_ROOT
        or dest_skill_dir.parent != dest_category_dir
    ):
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_VALIDATION",
            action="ingest",
            details="Đường dẫn đích không an toàn."
        )

    if dry_run:
        print(f"-> [DRY-RUN] Sẵn sàng chuyển tới: {dest_skill_dir}")
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="ACCEPTED",
            overlap_report=overlap_rep,
            security_report=sec_rep,
            action="ingest",
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

    if val_passed:
        # Register ingested skill into .sync-state.json
        register_skill(
            skill_name=skill_name,
            category=target_category,
            source_repo=source_repo,
            local_dir=dest_skill_dir,
        )

    return IngestionResult(
        skill_name=skill_name,
        target_category=target_category,
        source_repo=source_repo,
        verdict="ACCEPTED" if val_passed else "REJECTED_VALIDATION",
        overlap_report=overlap_rep,
        security_report=sec_rep,
        action="ingest",
        validation_passed=val_passed,
        details="Đã tích hợp thành công vào repository." if val_passed else "Lỗi validation sau khi copy."
    )


def process_update_skill(
    candidate_dir: Path,
    skill_name: str,
    target_category: str,
    source_repo: str,
    source_path: str = "",
    branch: str = "main",
    drift_report: Optional[DriftReport] = None,
    dry_run: bool = False,
    allowed_licenses: Optional[List[str]] = None,
) -> IngestionResult:
    """
    Run an existing skill update through Gate 3 (Security) and Gate 4 (Normalization),
    then safely overwrite destination directory and update .sync-state.json.
    """
    print(f"\n==================================================")
    print(f"Bắt đầu quy trình Cập nhật (Drift Update): '{skill_name}'")
    print(f"Nguồn: {source_repo} ({source_path}) | skills/{target_category}/{skill_name}")
    print(f"==================================================")

    # Gate 1: Check SKILL.md existence & License
    skill_md = candidate_dir / "SKILL.md"
    if not skill_md.exists():
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_VALIDATION",
            action="update",
            drift_report=drift_report,
            details="Không có file SKILL.md trong nội dung cập nhật."
        )

    content = skill_md.read_text(encoding="utf-8", errors="replace")
    fm, _ = parse_frontmatter(content)

    cand_lic = fm.get("license")
    if not is_license_allowed(cand_lic, allowed_licenses):
        print(f"   [FAILED]: License '{cand_lic}' không nằm trong danh sách được phép ({allowed_licenses})!")
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_VALIDATION",
            action="update",
            drift_report=drift_report,
            details=f"License '{cand_lic}' không nằm trong danh sách được phép ({allowed_licenses})."
        )

    desc = fm.get("description", "")
    if not desc:
        for line in content.splitlines()[:30]:
            if line.strip().startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip('"').strip("'")
                break

    # Gate 3: Security & Malware Scan
    print("-> Đang quét an ninh mã độc và prompt injection cho bản cập nhật...")
    sec_rep = scan_skill_directory(candidate_dir)
    if not sec_rep.is_safe:
        print("   [FAILED]: Bản cập nhật chứa cảnh báo bảo mật nghiêm trọng!")
        for err in sec_rep.critical_errors:
            print(f"   - {err}")
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_SECURITY",
            security_report=sec_rep,
            drift_report=drift_report,
            action="update",
            details="Bản cập nhật không vượt qua bài quét bảo mật."
        )
    else:
        print("   [PASSED]: Quét an ninh cập nhật thành công.")

    # Gate 4: Normalization
    print("-> Đang chuẩn hóa cấu trúc thư mục, frontmatter và evals cho bản cập nhật...")
    norm_success, changes = normalize_skill_directory(candidate_dir, expected_name=skill_name)
    for ch in changes:
        print(f"   + {ch}")

    if not norm_success:
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_VALIDATION",
            security_report=sec_rep,
            drift_report=drift_report,
            action="update",
            details="Không thể chuẩn hóa cấu trúc bản cập nhật."
        )

    # Destination paths with safety verification
    dest_category_dir = REPO_ROOT / "skills" / target_category
    dest_skill_dir = dest_category_dir / skill_name

    if (
        not skill_name
        or dest_skill_dir == dest_category_dir
        or dest_skill_dir == REPO_ROOT
        or dest_skill_dir.parent != dest_category_dir
    ):
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="REJECTED_VALIDATION",
            action="update",
            drift_report=drift_report,
            details="Đường dẫn đích không an toàn."
        )

    if dry_run:
        print(f"-> [DRY-RUN] Sẵn sàng cập nhật tới: {dest_skill_dir}")
        return IngestionResult(
            skill_name=skill_name,
            target_category=target_category,
            source_repo=source_repo,
            verdict="ACCEPTED",
            security_report=sec_rep,
            drift_report=drift_report,
            action="update",
            validation_passed=True,
            details="Kiểm tra cập nhật hoàn tất (Dry-run)."
        )

    # Safe directory overwrite
    dest_category_dir.mkdir(parents=True, exist_ok=True)
    if dest_skill_dir.exists():
        shutil.rmtree(dest_skill_dir)
    shutil.copytree(candidate_dir, dest_skill_dir)
    print(f"-> Đã ghi đè cập nhật vào: {dest_skill_dir}")

    # Register updated skill into .sync-state.json
    register_skill(
        skill_name=skill_name,
        category=target_category,
        source_repo=source_repo,
        source_path=source_path,
        branch=branch,
        local_dir=dest_skill_dir,
    )

    # Run global repo validation
    print("-> Chạy bộ validator tổng thể của repository sau cập nhật...")
    val_passed = run_local_validation()

    return IngestionResult(
        skill_name=skill_name,
        target_category=target_category,
        source_repo=source_repo,
        verdict="ACCEPTED" if val_passed else "REJECTED_VALIDATION",
        security_report=sec_rep,
        drift_report=drift_report,
        action="update",
        validation_passed=val_passed,
        details="Đã cập nhật skill thành công." if val_passed else "Lỗi validation sau khi cập nhật."
    )


def auto_sync_sources(
    sources_file: Path,
    limit: int = 1,
    limit_update: int = 5,
    mode: str = "auto",
    dry_run: bool = False,
    token: Optional[str] = None
) -> List[IngestionResult]:
    """
    Dual-Phase Synchronization:
      Phase 1 (Ingestion): Scan trusted sources for un-ingested skills (skipped if mode == 'update-only').
      Phase 2 (Drift Update): If no new skills ingested in Phase 1 (or mode == 'update-only'),
                              detect drift on tracked/existing skills and apply updates (skipped if mode == 'ingest-only').
    """
    if not sources_file.exists():
        print(f"[ERROR] Sources file not found: {sources_file}")
        return []

    with open(sources_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    trusted = config.get("trusted_sources", [])
    existing_skills = load_existing_skills(REPO_ROOT)
    existing_names = {s.name.lower() for s in existing_skills}

    results: List[IngestionResult] = []

    # =========================================================================
    # Phase 1: Ingestion of New Skills
    # =========================================================================
    if mode in ("auto", "ingest-only"):
        print(f"\n=== [PHASE 1] QUÉT VÀ NẠP SKILL MỚI (Giới hạn: {limit} skill) ===")
        for src in trusted:
            if not src.get("enabled", True):
                continue

            repo = src.get("repo")
            path = src.get("path", "skills")
            branch = src.get("branch", "main")
            category = src.get("target_category", "general")
            allowed_licenses = src.get("allowed_licenses")

            print(f"\n[PHASE 1] Đang quét nguồn: {repo} (nhánh: {branch}, path: {path})...")
            try:
                owner, repo_name = repo.split("/")
            except ValueError:
                print(f"[WARN] Cấu hình repo không hợp lệ: {repo}")
                continue

            clean_path = path.replace("\\", "/").strip("/")
            url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{clean_path}?ref={branch}"

            try:
                items = github_api_get(url, token)
            except Exception as e:
                print(f"[WARN] Không thể kết nối tới {repo}: {e}")
                continue

            if not isinstance(items, list):
                continue

            for item in items:
                if item.get("type") != "dir":
                    continue

                raw_skill_name = item.get("name")
                sanitized_name = sanitize_skill_name(raw_skill_name)

                if not sanitized_name or sanitized_name in existing_names:
                    continue

                print(f"\n[PHÁT HIỆN SKILL MỚI] '{sanitized_name}' tại {repo}/{item.get('path')}")
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_skill_dir = Path(tmp_dir) / sanitized_name
                    tmp_skill_dir.mkdir(parents=True, exist_ok=True)
                    download_success = download_github_folder(
                        owner, repo_name, item.get("path"), tmp_skill_dir, token, ref=branch
                    )
                    if not download_success:
                        print(f"[ERROR] Tải thất bại cho {sanitized_name}")
                        continue

                    res = process_candidate_skill(
                        candidate_dir=tmp_skill_dir,
                        source_repo=f"{repo}/{item.get('path')}",
                        target_category=category,
                        dry_run=dry_run,
                        allowed_licenses=allowed_licenses
                    )

                    if res.verdict == "ACCEPTED":
                        print(f"-> Đã tiếp nhận thành công skill '{sanitized_name}'!")
                        results.append(res)
                        existing_names.add(sanitized_name)
                        if len(results) >= limit:
                            print(f"\n[PHASE 1] Đã đạt giới hạn ({limit} skill). Hoàn tất.")
                            return results

    # =========================================================================
    # Phase 2: Drift Detection & Safe Update
    # Triggered if Phase 1 found nothing (in auto mode) or if update-only mode.
    # =========================================================================
    if mode in ("auto", "update-only") and len(results) == 0:
        print(f"\n=== [PHASE 2] KIỂM TRA BIẾN ĐỘNG & CẬP NHẬT (DRIFT UPDATE) (Giới hạn: {limit_update} skill) ===")
        updated_results: List[IngestionResult] = []

        # Step 2a: Check tracked skills from .sync-state.json
        state = load_sync_state()
        tracked = state.get("tracked_skills", {})
        checked_skills = set()

        if tracked:
            print(f"[PHASE 2] Kiểm tra {len(tracked)} skill được theo dõi trong .sync-state.json...")
            for skill_name, info in tracked.items():
                cat = info.get("category", "general")
                repo = info.get("source_repo", "")
                item_path = info.get("source_path", "")
                branch = info.get("branch", "main")
                checked_skills.add(skill_name)

                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_skill_dir = Path(tmp_dir) / skill_name
                    tmp_skill_dir.mkdir(parents=True, exist_ok=True)
                    if not repo or "/" not in repo:
                        continue
                    owner, repo_name = repo.split("/", 1)
                    download_ok = download_github_folder(
                        owner, repo_name, item_path, tmp_skill_dir, token, ref=branch
                    )
                    if not download_ok:
                        continue

                    drift_rep = check_drift_for_skill(
                        skill_name=skill_name,
                        category=cat,
                        source_repo=repo,
                        source_path=item_path,
                        branch=branch,
                        candidate_dir=tmp_skill_dir,
                        tracked_sha=info.get("content_sha"),
                    )

                    if drift_rep.has_drift:
                        print(f"\n[PHÁT HIỆN BIẾN ĐỘNG] '{skill_name}' từ {repo}/{item_path}")
                        res = process_update_skill(
                            candidate_dir=tmp_skill_dir,
                            skill_name=skill_name,
                            target_category=cat,
                            source_repo=repo,
                            source_path=item_path,
                            branch=branch,
                            drift_report=drift_rep,
                            dry_run=dry_run,
                        )
                        if res.verdict == "ACCEPTED":
                            updated_results.append(res)
                            if len(updated_results) >= limit_update:
                                return updated_results

        # Step 2b: If limit not reached, check existing skills from trusted sources
        if len(updated_results) < limit_update:
            for src in trusted:
                if not src.get("enabled", True):
                    continue

                repo = src.get("repo")
                base_path = src.get("path", "skills")
                branch = src.get("branch", "main")
                category = src.get("target_category", "general")
                allowed_licenses = src.get("allowed_licenses")

                try:
                    owner, repo_name = repo.split("/")
                except ValueError:
                    continue

                clean_path = base_path.replace("\\", "/").strip("/")
                url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{clean_path}?ref={branch}"

                try:
                    items = github_api_get(url, token)
                except Exception as e:
                    print(f"[WARN] Không thể kết nối tới {repo}: {e}")
                    continue

                if not isinstance(items, list):
                    continue

                for item in items:
                    if item.get("type") != "dir":
                        continue

                    raw_name = item.get("name")
                    skill_name = sanitize_skill_name(raw_name)

                    if not skill_name or skill_name in checked_skills:
                        continue

                    local_dir = REPO_ROOT / "skills" / category / skill_name
                    if not local_dir.exists():
                        continue

                    checked_skills.add(skill_name)
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        tmp_skill_dir = Path(tmp_dir) / skill_name
                        tmp_skill_dir.mkdir(parents=True, exist_ok=True)
                        download_ok = download_github_folder(
                            owner, repo_name, item.get("path"), tmp_skill_dir, token, ref=branch
                        )
                        if not download_ok:
                            continue

                        drift_rep = check_drift_for_skill(
                            skill_name=skill_name,
                            category=category,
                            source_repo=repo,
                            source_path=item.get("path"),
                            branch=branch,
                            local_dir=local_dir,
                            candidate_dir=tmp_skill_dir,
                        )

                        if drift_rep.has_drift:
                            print(f"\n[PHÁT HIỆN BIẾN ĐỘNG] '{skill_name}' từ {repo}/{item.get('path')}")
                            res = process_update_skill(
                                candidate_dir=tmp_skill_dir,
                                skill_name=skill_name,
                                target_category=category,
                                source_repo=repo,
                                source_path=item.get("path"),
                                branch=branch,
                                drift_report=drift_rep,
                                dry_run=dry_run,
                                allowed_licenses=allowed_licenses,
                            )
                            if res.verdict == "ACCEPTED":
                                updated_results.append(res)
                                if len(updated_results) >= limit_update:
                                    return updated_results

        return updated_results

    return results


def main():
    parser = argparse.ArgumentParser(description="Skill Ingestion & Sync Automation CLI")
    parser.add_argument("--sources-file", default=str(SCRIPTS_DIR / "ingest" / "sources.json"), help="Path to sources.json")
    parser.add_argument("--check-local", type=str, help="Check and scan a local directory")
    parser.add_argument("--category", default="general", choices=["general", "anthropic", "openai", "google"], help="Target category")
    parser.add_argument("--dry-run", action="store_true", help="Perform checks without copying files")
    parser.add_argument("--output-pr-data", type=str, help="Path to write PR scorecard markdown / json")
    parser.add_argument("--github-repo", type=str, help="Ingest directly from GitHub repo (e.g. owner/repo)")
    parser.add_argument("--skill-path", type=str, help="Path inside GitHub repo to the skill")
    parser.add_argument("--auto-sync", action="store_true", help="Automatically scan trusted sources from sources.json")
    parser.add_argument("--limit", type=int, default=1, help="Max number of skills to ingest in auto-sync (default: 1)")
    parser.add_argument("--mode", choices=["auto", "ingest-only", "update-only"], default="auto", help="Sync mode: auto, ingest-only, update-only (default: auto)")
    parser.add_argument("--limit-update", type=int, default=5, help="Max number of skills to update in auto-sync (default: 5)")

    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN")

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
        emit_github_outputs(result, args.dry_run)
        if args.output_pr_data:
            Path(args.output_pr_data).write_text(result.generate_pr_body(), encoding="utf-8")
        print("\n" + result.generate_pr_body())
        sys.exit(0 if result.verdict == "ACCEPTED" else 1)

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
            emit_github_outputs(result, args.dry_run)
            if args.output_pr_data:
                Path(args.output_pr_data).write_text(result.generate_pr_body(), encoding="utf-8")
            print("\n" + result.generate_pr_body())
            sys.exit(0 if result.verdict == "ACCEPTED" else 1)

    # Mode 3: Auto-sync from sources.json
    sources_file = Path(args.sources_file)
    print(f"Bắt đầu quy trình Auto-Sync từ {sources_file.name} (Mode: {args.mode}, Ingest Limit: {args.limit}, Update Limit: {args.limit_update})...")
    results = auto_sync_sources(
        sources_file=sources_file,
        limit=args.limit,
        limit_update=args.limit_update,
        mode=args.mode,
        dry_run=args.dry_run,
        token=token
    )

    if results:
        first = results[0]
        emit_github_outputs(first, args.dry_run)
        if args.output_pr_data:
            Path(args.output_pr_data).write_text(first.generate_pr_body(), encoding="utf-8")
    else:
        print("\n[AUTO-SYNC] Đã quét toàn bộ nguồn. Không có kỹ năng nào cần nạp hoặc cập nhật.")
        emit_no_skills_summary()

    sys.exit(0)


if __name__ == "__main__":
    main()
