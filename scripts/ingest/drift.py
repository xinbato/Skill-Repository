#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Skill Drift Detection & State Tracking Engine for Skill-Repository.
Manages .sync-state.json and tracks content hashes (SHA-256) of upstream skills
to detect drift and trigger safe automatic updates.
"""

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union
import urllib.error
import urllib.request

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SCRIPTS_DIR.parent
DEFAULT_STATE_FILE = REPO_ROOT / ".sync-state.json"


@dataclass
class DriftReport:
    skill_name: str
    category: str
    source_repo: str
    source_path: str
    branch: str
    has_drift: bool
    local_sha: str
    upstream_sha: str
    downloaded_dir: Optional[Path] = None
    details: str = ""

    def to_markdown(self) -> str:
        """Format drift result for markdown reporting in PR scorecard."""
        badge = "⚠️ PHÁT HIỆN BIẾN ĐỘNG (DRIFT)" if self.has_drift else "✅ ĐÃ ĐỒNG BỘ"
        lines = [
            f"- **Trạng thái biến động**: {badge}",
            f"- **SHA Cục bộ (Local SHA)**: `{self.local_sha[:12] if self.local_sha else 'Chưa có'}`",
            f"- **SHA Thượng nguồn (Upstream SHA)**: `{self.upstream_sha[:12] if self.upstream_sha else 'Chưa có'}`",
        ]
        if self.details:
            lines.append(f"- **Chi tiết**: {self.details}")
        return "\n".join(lines)


def github_api_get(url: str, token: Optional[str] = None) -> Any:
    """Fetch JSON from GitHub API with rate limit detection."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Skill-Repository-Sync-Bot")
    req.add_header("Accept", "application/vnd.github.v3+json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code in (403, 429):
            remaining = e.headers.get("X-RateLimit-Remaining", "0")
            reset = e.headers.get("X-RateLimit-Reset", "unknown")
            print(f"[ERROR] GitHub API Rate Limit Reached (HTTP {e.code}). Remaining: {remaining}, Reset: {reset}")
        raise


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
    """Recursively download directory contents from GitHub via contents API, handling path separators."""
    clean_path = path.replace("\\", "/").strip("/")
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{clean_path}?ref={ref}"
    try:
        items = github_api_get(url, token)
    except Exception as e:
        print(f"[ERROR] Failed to fetch folder {clean_path} from {owner}/{repo}: {e}")
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


def compute_skill_content_sha(skill_dir: Union[str, Path]) -> str:
    """
    Computes a deterministic SHA-256 hash across all content files in a skill directory.
    - Excludes cache, temporary files, and OS artifacts.
    - Normalizes relative paths in POSIX format and sorts them.
    - Normalizes CRLF line endings to LF for consistent hashes across Windows and Linux.
    """
    skill_path = Path(skill_dir).resolve()
    if not skill_path.exists() or not skill_path.is_dir():
        return ""

    hasher = hashlib.sha256()

    excluded_names = {
        "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache",
        ".DS_Store", "Thumbs.db", "desktop.ini", ".git",
    }
    excluded_extensions = {".pyc", ".pyo", ".pyd", ".swp", ".swo", ".tmp", ".bak", ".orig"}

    file_entries: List[Tuple[str, Path]] = []
    for root, dirs, files in os.walk(skill_path):
        dirs[:] = [d for d in dirs if d not in excluded_names and not d.endswith(".egg-info")]
        for file in files:
            if file in excluded_names:
                continue
            if any(file.endswith(ext) for ext in excluded_extensions):
                continue
            full_file_path = Path(root) / file
            rel_path = full_file_path.relative_to(skill_path).as_posix()
            file_entries.append((rel_path, full_file_path))

    file_entries.sort(key=lambda x: x[0])

    for rel_posix, full_path in file_entries:
        hasher.update(rel_posix.encode("utf-8"))
        try:
            content = full_path.read_bytes()
            content = content.replace(b"\r\n", b"\n")
            hasher.update(content)
        except Exception:
            pass

    return hasher.hexdigest()


def load_sync_state(state_file: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """Load sync state from .sync-state.json or return default initialized structure."""
    target_file = Path(state_file).resolve() if state_file else DEFAULT_STATE_FILE
    if target_file.exists():
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                state = json.load(f)
                if isinstance(state, dict):
                    if "$schema" not in state:
                        state["$schema"] = "https://json-schema.org/draft/2020-12/schema"
                    if "version" not in state:
                        state["version"] = "1.0.0"
                    if "tracked_skills" not in state or not isinstance(state["tracked_skills"], dict):
                        state["tracked_skills"] = {}
                    return state
        except Exception as e:
            print(f"[WARN] Failed to read {target_file}: {e}")

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "version": "1.0.0",
        "tracked_skills": {},
    }


def save_sync_state(state: Dict[str, Any], state_file: Optional[Union[str, Path]] = None) -> None:
    """Save sync state to .sync-state.json formatted as pretty JSON."""
    target_file = Path(state_file).resolve() if state_file else DEFAULT_STATE_FILE
    target_file.parent.mkdir(parents=True, exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def register_skill(
    skill_name: str,
    category: str,
    source_repo: str,
    source_path: str = "",
    branch: str = "main",
    local_dir: Optional[Union[str, Path]] = None,
    content_sha: Optional[str] = None,
    commit_sha: Optional[str] = None,
    state_file: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """Register or update an ingested/updated skill in .sync-state.json."""
    if not content_sha and local_dir:
        content_sha = compute_skill_content_sha(local_dir)

    repo_only = source_repo
    path_only = source_path
    if not path_only and source_repo and "/" in source_repo:
        parts = source_repo.split("/")
        if len(parts) > 2:
            repo_only = f"{parts[0]}/{parts[1]}"
            path_only = "/".join(parts[2:])

    state = load_sync_state(state_file)
    entry = {
        "skill_name": skill_name,
        "category": category,
        "source_repo": repo_only,
        "source_path": path_only,
        "branch": branch,
        "content_sha": content_sha or "",
        "commit_sha": commit_sha or "",
        "last_sync": datetime.now(timezone.utc).isoformat(),
    }
    state["tracked_skills"][skill_name] = entry
    save_sync_state(state, state_file)
    return entry


def check_drift_for_skill(
    skill_name: str,
    category: str,
    source_repo: str,
    source_path: str,
    branch: str = "main",
    local_dir: Optional[Union[str, Path]] = None,
    tracked_sha: Optional[str] = None,
    candidate_dir: Optional[Union[str, Path]] = None,
    token: Optional[str] = None,
    repo_root: Optional[Union[str, Path]] = None,
) -> DriftReport:
    """
    Check if an upstream skill has drifted compared to the local copy / tracked content SHA.
    If candidate_dir is provided, uses it directly; otherwise downloads from GitHub.
    """
    root = Path(repo_root).resolve() if repo_root else REPO_ROOT
    loc_dir = Path(local_dir).resolve() if local_dir else (root / "skills" / category / skill_name)

    local_sha = ""
    if loc_dir.exists() and loc_dir.is_dir():
        local_sha = compute_skill_content_sha(loc_dir)
    elif tracked_sha:
        local_sha = tracked_sha

    # Case A: candidate_dir already downloaded and passed in
    if candidate_dir:
        cand_path = Path(candidate_dir).resolve()
        if cand_path.exists() and cand_path.is_dir():
            upstream_sha = compute_skill_content_sha(cand_path)
            if not upstream_sha:
                return DriftReport(
                    skill_name=skill_name,
                    category=category,
                    source_repo=source_repo,
                    source_path=source_path,
                    branch=branch,
                    has_drift=False,
                    local_sha=local_sha,
                    upstream_sha="",
                    downloaded_dir=cand_path,
                    details="Thư mục ứng viên rỗng hoặc không tính được SHA."
                )
            has_drift = (local_sha != upstream_sha)
            details = (
                f"Nội dung thượng nguồn đã thay đổi (cục bộ: {local_sha[:8]}, thượng nguồn: {upstream_sha[:8]})."
                if has_drift else "Nội dung khớp với thượng nguồn."
            )
            return DriftReport(
                skill_name=skill_name,
                category=category,
                source_repo=source_repo,
                source_path=source_path,
                branch=branch,
                has_drift=has_drift,
                local_sha=local_sha,
                upstream_sha=upstream_sha,
                downloaded_dir=cand_path,
                details=details
            )

    # Case B: Download upstream from GitHub
    if not source_repo or "/" not in source_repo:
        return DriftReport(
            skill_name=skill_name,
            category=category,
            source_repo=source_repo,
            source_path=source_path,
            branch=branch,
            has_drift=False,
            local_sha=local_sha,
            upstream_sha="",
            details=f"Cấu hình repo không hợp lệ: '{source_repo}'"
        )

    parts = source_repo.split("/", 1)
    owner, repo_name = parts[0], parts[1]
    temp_dir = tempfile.mkdtemp(prefix=f"drift_{skill_name}_")
    tmp_path = Path(temp_dir) / skill_name
    tmp_path.mkdir(parents=True, exist_ok=True)

    try:
        success = download_github_folder(owner, repo_name, source_path, tmp_path, token=token, ref=branch)
        if not success or not any(tmp_path.iterdir()):
            shutil.rmtree(temp_dir, ignore_errors=True)
            return DriftReport(
                skill_name=skill_name,
                category=category,
                source_repo=source_repo,
                source_path=source_path,
                branch=branch,
                has_drift=False,
                local_sha=local_sha,
                upstream_sha="",
                details=f"Không thể tải nội dung thượng nguồn từ {source_repo}/{source_path}."
            )

        upstream_sha = compute_skill_content_sha(tmp_path)
        has_drift = (local_sha != upstream_sha) and bool(upstream_sha)
        details = (
            f"Nội dung thượng nguồn đã thay đổi (cục bộ: {local_sha[:8]}, thượng nguồn: {upstream_sha[:8]})."
            if has_drift else "Nội dung khớp với thượng nguồn."
        )
        return DriftReport(
            skill_name=skill_name,
            category=category,
            source_repo=source_repo,
            source_path=source_path,
            branch=branch,
            has_drift=has_drift,
            local_sha=local_sha,
            upstream_sha=upstream_sha,
            downloaded_dir=tmp_path,
            details=details
        )
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return DriftReport(
            skill_name=skill_name,
            category=category,
            source_repo=source_repo,
            source_path=source_path,
            branch=branch,
            has_drift=False,
            local_sha=local_sha,
            upstream_sha="",
            details=f"Lỗi khi kiểm tra drift: {e}"
        )


def scan_all_drifts(
    repo_root: Optional[Union[str, Path]] = None,
    state_file: Optional[Union[str, Path]] = None,
    sources_file: Optional[Union[str, Path]] = None,
    token: Optional[str] = None,
    limit: int = 5,
) -> List[DriftReport]:
    """
    Scans tracked skills for drift against upstream repositories.
    If tracked_skills is empty in .sync-state.json, attempts to discover existing skills
    matching trusted sources in sources.json.
    Returns a list of DriftReports that have has_drift == True, up to limit.
    """
    root = Path(repo_root).resolve() if repo_root else REPO_ROOT
    state = load_sync_state(state_file)
    tracked_skills = state.get("tracked_skills", {})

    drifts: List[DriftReport] = []

    # If we have tracked skills, scan them first
    if tracked_skills:
        print(f"[DRIFT] Đang quét {len(tracked_skills)} skill được theo dõi trong .sync-state.json...")
        for name, info in tracked_skills.items():
            cat = info.get("category", "general")
            repo = info.get("source_repo", "")
            path = info.get("source_path", "")
            branch = info.get("branch", "main")
            tracked_sha = info.get("content_sha", "")

            rep = check_drift_for_skill(
                skill_name=name,
                category=cat,
                source_repo=repo,
                source_path=path,
                branch=branch,
                tracked_sha=tracked_sha,
                token=token,
                repo_root=root,
            )
            if rep.has_drift:
                print(f"  [DRIFT DETECTED] Skill '{name}' có biến động nội dung!")
                drifts.append(rep)
                if len(drifts) >= limit:
                    return drifts
            else:
                if rep.downloaded_dir and rep.downloaded_dir.parent.exists():
                    shutil.rmtree(rep.downloaded_dir.parent, ignore_errors=True)

    # If tracked_skills was empty or had fewer drifts than limit, check sources.json
    src_file = Path(sources_file).resolve() if sources_file else (root / "scripts" / "ingest" / "sources.json")
    if src_file.exists() and len(drifts) < limit:
        try:
            with open(src_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            trusted = config.get("trusted_sources", [])

            for src in trusted:
                if not src.get("enabled", True):
                    continue
                repo = src.get("repo", "")
                base_path = src.get("path", "skills").replace("\\", "/").strip("/")
                branch = src.get("branch", "main")
                category = src.get("target_category", "general")

                cat_dir = root / "skills" / category
                if not cat_dir.exists():
                    continue

                for local_skill in cat_dir.iterdir():
                    if not local_skill.is_dir() or local_skill.name.startswith("."):
                        continue
                    skill_name = local_skill.name
                    if skill_name in tracked_skills:
                        continue  # already checked above

                    source_path = f"{base_path}/{skill_name}"
                    rep = check_drift_for_skill(
                        skill_name=skill_name,
                        category=category,
                        source_repo=repo,
                        source_path=source_path,
                        branch=branch,
                        local_dir=local_skill,
                        token=token,
                        repo_root=root,
                    )
                    if rep.has_drift:
                        print(f"  [DRIFT DETECTED] Skill '{skill_name}' có biến động nội dung!")
                        drifts.append(rep)
                        if len(drifts) >= limit:
                            return drifts
                    else:
                        if rep.downloaded_dir and rep.downloaded_dir.parent.exists():
                            shutil.rmtree(rep.downloaded_dir.parent, ignore_errors=True)
        except Exception as e:
            print(f"[WARN] Error scanning sources for drift: {e}")

    return drifts


def main():
    parser = argparse.ArgumentParser(description="Skill Drift Detection CLI")
    parser.add_argument("--scan-all", action="store_true", help="Scan all tracked and existing skills for drift")
    parser.add_argument("--skill", type=str, help="Check drift for a specific skill name")
    parser.add_argument("--category", type=str, default="general", help="Category for specific skill")
    parser.add_argument("--repo", type=str, help="Upstream repo for specific skill")
    parser.add_argument("--path", type=str, help="Upstream path for specific skill")
    parser.add_argument("--state-file", type=str, help="Custom state file path")
    parser.add_argument("--limit", type=int, default=5, help="Limit number of drifts to report")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if args.scan_all or (not args.skill):
        drifts = scan_all_drifts(state_file=args.state_file, token=token, limit=args.limit)
        print(f"\nPhát hiện {len(drifts)} skill có drift.")
        for d in drifts:
            print(f"- {d.skill_name} ({d.category}): {d.details}")
            if d.downloaded_dir and d.downloaded_dir.parent.exists():
                shutil.rmtree(d.downloaded_dir.parent, ignore_errors=True)
    else:
        state = load_sync_state(args.state_file)
        info = state.get("tracked_skills", {}).get(args.skill, {})
        cat = args.category or info.get("category", "general")
        repo = args.repo or info.get("source_repo", "")
        path = args.path or info.get("source_path", f"skills/{args.skill}")
        branch = info.get("branch", "main")
        rep = check_drift_for_skill(args.skill, cat, repo, path, branch, token=token)
        print(rep.to_markdown())
        if rep.downloaded_dir and rep.downloaded_dir.parent.exists():
            shutil.rmtree(rep.downloaded_dir.parent, ignore_errors=True)


if __name__ == "__main__":
    main()
