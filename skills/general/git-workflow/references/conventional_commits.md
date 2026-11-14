# Conventional Commits Reference Specification

Specification based on [Conventional Commits v1.0.0](https://www.conventionalcommits.org/).

---

## 1. Structure

A conventional commit message should follow this structure:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

---

## 2. Types

| Type | When to Use | SemVer Impact |
| :--- | :--- | :--- |
| **`feat`** | Adds a new feature or user capability | MINOR |
| **`fix`** | Patches a bug or resolves an issue | PATCH |
| **`docs`** | Documentation only changes (README, guides, docstrings) | None |
| **`style`** | Code formatting, missing semicolons, whitespace (no logic changes) | None |
| **`refactor`** | Code change that neither fixes a bug nor adds a feature | None |
| **`perf`** | Performance improvement | PATCH |
| **`test`** | Adding missing tests or correcting existing tests | None |
| **`build`** | Changes to build system or external dependencies (npm, pip, docker) | None / PATCH |
| **`ci`** | Changes to CI configuration files and scripts (GitHub Actions, GitLab CI) | None |
| **`chore`** | Other changes that don't modify src or test files | None |
| **`revert`** | Reverts a previous commit | Depends |

---

## 3. Formatting Rules

1. **Header Line**:
   - Limit to 50–72 characters.
   - Use the **imperative mood** in the description: *"add feature"* (not *"added"* or *"adds"*).
   - Do **NOT** capitalize the first letter of the description.
   - Do **NOT** put a period (`.`) at the end of the subject line.
2. **Body**:
   - Separate from header with a blank line.
   - Wrap at ~72 characters.
   - Explain the **motivation** for the change and **what** was changed (not repeating *how* the code does it).
3. **Breaking Changes**:
   - Include an exclamation mark `!` before the colon: `feat(api)!: remove deprecated v1 endpoint`
   - Or include `BREAKING CHANGE: <explanation>` in the footer.
   - SemVer impact: MAJOR.

---

## 4. Examples

### Simple Feature
```text
feat(auth): add google oauth2 login provider
```

### Bug Fix with Issue Reference
```text
fix(parser): resolve null pointer exception on empty lines

Closes #142
```

### Breaking Change
```text
feat(api)!: redesign authentication tokens schema

BREAKING CHANGE: Authorization header now requires 'Bearer <jwt>' instead of raw token.
```
