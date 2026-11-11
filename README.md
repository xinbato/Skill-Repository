# ⚡ Skill-Repository

> **A standardized, portable hub of production-ready AI Agent Skills.**  
> Built according to the open [agentskills.io](https://agentskills.io) specification.

[![Standard: agentskills.io](https://img.shields.io/badge/Standard-agentskills.io-blue.svg)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/xinbato/Skill-Repository?style=social)](https://github.com/xinbato/Skill-Repository)

---

## 🌟 Overview

**Skill-Repository** is a centralized library of reusable, version-controlled **Agent Skills**. Each skill encapsulates procedural knowledge, executable scripts, and reference documentation into a clean, portable format that any AI Agent (Cursor, Claude Code, Antigravity, OpenHands, Copilot, etc.) can discover and execute.

### Key Highlights
- **Zero-Bloat Progressive Disclosure**: Agents load skills in 3 stages (*Discovery* -> *Activation* -> *Execution*), preserving context tokens.
- **🗺️ The Portable Map (`SKILLS_MAP.md`)**: You don't need to clone the whole repository. Simply drop `SKILLS_MAP.md` into any project, and your AI Agent will automatically discover and pull skills from GitHub on demand.
- **Universal Compatibility**: Works on any OS (Windows, macOS, Linux) and across various agentic development tools.

---

## 🏗️ Architecture

```
                                  ┌──────────────────────────────────────────────┐
                                  │   GitHub: xinbato/Skill-Repository           │
                                  │   (Central Skills Hub)                       │
                                  └──────────────────────┬───────────────────────┘
                                                         │
                                  ┌──────────────────────▼───────────────────────┐
                                  │              SKILLS_MAP.md                   │
                                  │   (Lightweight Router / Index File)          │
                                  └──────────────────────┬───────────────────────┘
                                                         │
                       ┌─────────────────────────────────┴─────────────────────────────────┐
                       ▼                                                                   ▼
       ┌───────────────────────────────┐                                   ┌───────────────────────────────┐
       │     Project A (Local PC)      │                                   │     Project B (Remote Server) │
       │  - Has: SKILLS_MAP.md         │                                   │  - Has: SKILLS_MAP.md         │
       │  - Agent reads map            │                                   │  - Agent reads map            │
       │  - Pulls skills on demand     │                                   │  - Pulls skills on demand     │
       └───────────────────────────────┘                                   └───────────────────────────────┘
```

---

## 📁 Repository Structure

```text
Skill-Repository/
├── SKILLS_MAP.md                     # 🗺️ Portable dynamic router for AI agents
├── README.md                         # 📖 Repository documentation & guide
└── skills/                           # 📦 Collection of Agent Skills
    └── create-skill/                 # 🛠️ Skill 1: Automated Skill Generator
        ├── SKILL.md                  # YAML metadata & execution instructions
        ├── scripts/
        │   └── init_skill.py         # Cross-platform CLI scaffolding tool
        ├── references/
        │   ├── specification.md      # agentskills.io standard spec
        │   └── prompting_guidelines.md # Prompt & instruction best practices
        └── assets/
            ├── template_SKILL.md     # Reusable SKILL.md template
            ├── template_script.py    # Reusable Python script template
            └── template_reference.md # Reusable reference guide template
```

---

## 🚀 How to Use

### Method 1: The "Portable Map" Mode (Recommended ⭐)
You do **not** need to clone this repository. In any project workspace:
1. Download only the [`SKILLS_MAP.md`](SKILLS_MAP.md) file into your project root.
2. In your prompt to your AI Agent, simply mention:
   > *"Read `SKILLS_MAP.md` and use the relevant skills to solve my task."*
3. The Agent will scan the catalog, fetch the required skill from GitHub, and execute it seamlessly.

### Method 2: Full Repository Clone
If you want all skills stored locally:
```bash
git clone https://github.com/xinbato/Skill-Repository.git
cd Skill-Repository
```

### Method 3: Selective Skill Download (Sparse Checkout)
If you only need a single skill (e.g., `create-skill`):
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/xinbato/Skill-Repository.git my-skills
cd my-skills
git sparse-checkout set skills/create-skill
```

---

## 📦 Available Skills

| Skill | Description | Category | Link |
| :--- | :--- | :--- | :--- |
| **[`create-skill`](skills/create-skill/)** | Generates standard-compliant Agent Skills with directory structures, metadata, scripts, and references. | Developer Tooling | [Explore](skills/create-skill/SKILL.md) |

---

## 🛠️ Deep Dive: `create-skill`

The first skill in this repository is **`create-skill`** — a meta-skill designed to build new skills.

### What it does:
- Validates skill naming (`kebab-case`).
- Sets up standard subdirectories: `scripts/`, `references/`, `assets/`.
- Authors valid YAML frontmatter optimized for the **Discovery** stage.
- Includes `scripts/init_skill.py` to automate folder generation.

### CLI Usage:
```bash
python skills/create-skill/scripts/init_skill.py \
  --name "pdf-parser" \
  --description "Extracts tabular data and text from PDF documents. Trigger when user uploads or mentions PDF analysis." \
  --dest "skills"
```

---

## 🤝 Contributing New Skills

We welcome contributions to expand the catalog!

1. Fork this repository: `https://github.com/xinbato/Skill-Repository`.
2. Use `create-skill` to scaffold your new skill:
   ```bash
   python skills/create-skill/scripts/init_skill.py --name "your-skill-name" --description "Clear trigger description" --dest "skills"
   ```
3. Implement instructions in `skills/<your-skill-name>/SKILL.md`.
4. Add helper scripts into `scripts/` and reference guides into `references/` if necessary.
5. Register your new skill in [`SKILLS_MAP.md`](SKILLS_MAP.md).
6. Submit a Pull Request!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Built with ❤️ for the AI Agent community.
