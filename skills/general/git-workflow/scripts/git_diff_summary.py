#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Inspects git status and diff, providing a structured breakdown
to help AI agents or developers craft accurate Conventional Commit messages.
"""

import os
import subprocess
import sys


def run_git_cmd(args):
    try:
        res = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
            errors="replace",
        )
        return res.stdout
    except subprocess.CalledProcessError:
        return ""
    except FileNotFoundError:
        print("[ERROR] Git is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)


def analyze_changes():
    status_output = run_git_cmd(["status", "--porcelain"])
    if not status_output:
        print("No changes detected in working tree.")
        return

    staged_files = []
    unstaged_files = []
    untracked_files = []

    for line in status_output.splitlines():
        if len(line) < 3:
            continue
        staged_indicator = line[0]
        unstaged_indicator = line[1]
        filepath = line[3:].strip()

        if line.startswith("??"):
            untracked_files.append(filepath)
        else:
            if staged_indicator not in (" ", "?"):
                staged_files.append((staged_indicator, filepath))
            if unstaged_indicator not in (" ", "?"):
                unstaged_files.append((unstaged_indicator, filepath))

    diff_stat = run_git_cmd(["diff", "--stat"])
    staged_diff_stat = run_git_cmd(["diff", "--cached", "--stat"])

    all_files = (
        [f for _, f in staged_files]
        + [f for _, f in unstaged_files]
        + untracked_files
    )

    # Heuristic guess for conventional commit type
    suggested_type = "chore"
    suggested_scope = ""

    extensions = [os.path.splitext(f)[1].lower() for f in all_files]
    dirs = [
        os.path.dirname(f).split(os.sep)[0]
        for f in all_files
        if os.path.dirname(f)
    ]

    if dirs:
        suggested_scope = dirs[0]

    all_docs = all(ext in (".md", ".txt", ".rst") for ext in extensions)
    all_tests = any("test" in f.lower() for f in all_files)
    all_configs = all(
        ext in (".json", ".yaml", ".yml", ".toml", ".ini", ".lock")
        for ext in extensions
    )

    if all_docs:
        suggested_type = "docs"
    elif all_tests and len(all_files) == 1:
        suggested_type = "test"
    elif all_configs:
        suggested_type = "chore"
    elif any("fix" in f.lower() or "bug" in f.lower() for f in all_files):
        suggested_type = "fix"
    else:
        suggested_type = "feat"

    print("=== GIT CHANGE SUMMARY ===")
    print(f"Staged changes ({len(staged_files)}):")
    for status, f in staged_files:
        print(f"  [{status}] {f}")

    print(f"\nUnstaged changes ({len(unstaged_files)}):")
    for status, f in unstaged_files:
        print(f"  [{status}] {f}")

    print(f"\nUntracked files ({len(untracked_files)}):")
    for f in untracked_files:
        print(f"  [?] {f}")

    if staged_diff_stat:
        print(f"\n--- Staged Diff Stat ---\n{staged_diff_stat}")
    elif diff_stat:
        print(f"\n--- Unstaged Diff Stat ---\n{diff_stat}")

    scope_str = f"({suggested_scope})" if suggested_scope else ""
    print(
        f"\n[SUGGESTION] Commit Header: {suggested_type}{scope_str}: <imperative description>"
    )


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    analyze_changes()


if __name__ == "__main__":
    main()
