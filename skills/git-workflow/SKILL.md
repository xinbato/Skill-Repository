---
name: git-workflow
description: Streamlines Git operations: analyzes diff and status, generates Conventional Commit messages, crafts Pull Request descriptions, and guides safe branching. Use when the user asks to commit changes, write commit messages, review git diff, prepare PRs, or handle git workflow tasks.
license: MIT
---

# Git Workflow & Commit Helper

## Overview
This skill guides the AI Agent and user through clean, production-grade Git practices. It automates status analysis, enforces Conventional Commits (`feat:`, `fix:`, `docs:`, etc.), safeguards sensitive files from accidental commits, and structures clear Pull Requests.

## When to Use
- User asks: "Commit code giúp tôi", "Tạo commit message", "Chuẩn bị PR", "Kiểm tra git diff", "Tạo nhánh mới".
- After finishing a development task and changes are ready to be saved to version control.
- When generating changelogs or reviewing modified files.
- When NOT to use: For general Git tutorial questions that do not involve interacting with an actual repository.

---

## Standard Workflow for the Agent

### Step 1: Analyze Current Git State
1. Check repository status and changes:
   ```bash
   python skills/git-workflow/scripts/git_diff_summary.py
   ```
   *(Or run `git status` and `git diff --stat` directly).*
2. Inspect the modified, added, and untracked files.

### Step 2: Safety & Secret Guard Check
Before staging files, verify that **NO sensitive files** are included:
- Check for `.env`, `*.pem`, `*.key`, `id_rsa`, `credentials.json`, `node_modules/`, etc.
- If an untracked sensitive file is found, warn the user immediately and ensure it is added to `.gitignore`.

### Step 3: Formulate Conventional Commit Message
Construct a message following [conventional_commits.md](references/conventional_commits.md):
- **Format**: `<type>(<optional-scope>): <imperative summary>`
- **Type Selection**:
  - `feat`: New features or capabilities.
  - `fix`: Bug fixes.
  - `docs`: Documentation only changes.
  - `refactor`: Code reorganization without behavior change.
  - `chore`: Tooling, dependencies, or configuration updates.
  - `test`: Adding or updating test cases.
- **Rule**: Lowercase, no trailing period, imperative mood (e.g. `feat: add user profile endpoint`).

### Step 4: Stage & Commit
1. Stage the verified files:
   ```bash
   git add <specific-files>
   ```
2. Commit with the formatted message:
   ```bash
   git commit -m "<type>(<scope>): <summary>"
   ```

### Step 5: Branching & Pull Requests (When Requested)
- **Feature Branch Naming**: `feat/<short-name>`, `fix/<issue-number>-<name>`.
- **Pull Request Description**: Use the template in [pull_request_template.md](assets/pull_request_template.md) to draft a clear description including summary, type of change, and test verification.

---

## Gotchas
- On Windows, Git may warn about LF/CRLF replacement (`warning: LF will be replaced by CRLF`). This is normal and harmless; do not treat it as a build failure.
- Never run blanket `git add .` without checking untracked files for secrets, tokens, or large binary artifacts.
- When working with detached HEAD or rebase conflicts, inspect `git status` before attempting further commits.

---

## References & Assets
- Commit Standards: [conventional_commits.md](references/conventional_commits.md)
- PR Markdown Template: [pull_request_template.md](assets/pull_request_template.md)
- Helper Script: `scripts/git_diff_summary.py`
- Test Suite: `evals/evals.json`
