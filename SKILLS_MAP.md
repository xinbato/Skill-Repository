# 🗺️ Central Agent Skills Map & Dynamic Router

> **Repository**: [xinbato/Skill-Repository](https://github.com/xinbato/Skill-Repository)  
> **Standard**: [agentskills.io](https://agentskills.io)  
> **Version**: 1.0.0

---

## 🤖 Instructions for AI Agents (System Directive)

You are an AI Agent reading this dynamic skills router. This file connects you to the centralized **Skill Repository** hosted at `https://github.com/xinbato/Skill-Repository`.

### Operational Protocol
Whenever the user asks you to perform a task:
1. **Scan**: Consult the [Skill Catalog](#-skill-catalog) below to see if an available skill matches the user's intent.
2. **Detect**: Check whether the skill already exists in the local workspace (typically in `.skills/<skill-name>/` or `skills/<skill-name>/`).
3. **Fetch on Demand**: If the skill is not yet installed locally, download its `SKILL.md` (and any scripts/references) using one of the [Dynamic Fetch Commands](#-dynamic-fetch-commands) or by fetching the Raw GitHub URL directly.
4. **Activate**: Read the downloaded `SKILL.md` into your context (Progressive Disclosure - Activation stage).
5. **Execute**: Follow the instructions in `SKILL.md` to complete the user's request.

---

## 📚 Skill Catalog

| Skill Name | Description & Trigger Keywords | Category | Direct Raw URL |
| :--- | :--- | :--- | :--- |
| **`create-skill`** | **Tạo và chuẩn hóa Agent Skill mới**. Sử dụng khi người dùng yêu cầu: *"Tạo skill mới"*, *"Khởi tạo skill [tên]"*, *"Scaffold skill"*, *"Viết SKILL.md theo chuẩn"*. Tự động tạo cấu trúc thư mục, script CLI, tài liệu tham khảo và metadata hợp lệ. | Developer Tooling | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/create-skill/SKILL.md) |
| **`git-workflow`** | **Chuẩn hóa quy trình Git & Conventional Commits**. Sử dụng khi người dùng yêu cầu: *"Commit code"*, *"Tạo commit message"*, *"Chuẩn bị PR"*, *"Kiểm tra git diff"*, *"Tạo nhánh mới"*. Tự động phân tích git status/diff, chặn commit lộ secret, viết commit message chuẩn và sinh mẫu PR description. | Version Control / DevOps | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/git-workflow/SKILL.md) |

*(More skills will be added here as the repository grows).*

---

## ⚡ Dynamic Fetch Commands

When you need to pull a skill into the current workspace, run any of the following commands:

### Option 1: Universal Python One-Liner (Cross-Platform)
```bash
python -c "import urllib.request, os; name='create-skill'; os.makedirs(f'.skills/{name}', exist_ok=True); urllib.request.urlretrieve(f'https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/{name}/SKILL.md', f'.skills/{name}/SKILL.md'); print(f'Installed {name}')"
```

### Option 2: PowerShell (Windows Native)
```powershell
$name = "create-skill"; New-Item -ItemType Directory -Force -Path ".skills/$name" | Out-Null; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/$name/SKILL.md" -OutFile ".skills/$name/SKILL.md"; Write-Host "Installed $name"
```

### Option 3: Bash / cURL (macOS / Linux)
```bash
NAME="create-skill" && mkdir -p ".skills/$NAME" && curl -sSL "https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/$NAME/SKILL.md" -o ".skills/$NAME/SKILL.md" && echo "Installed $NAME"
```

### Option 4: Full Skill Clone via Git Sparse-Checkout
If the skill requires its `scripts/`, `references/`, and `assets/` subdirectories:
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/xinbato/Skill-Repository.git .temp-skills
cd .temp-skills && git sparse-checkout set skills/create-skill
# Move to your desired directory, e.g. .skills/create-skill
```

---

## 📝 Updating this Map
When adding a new skill to `https://github.com/xinbato/Skill-Repository`:
1. Place the skill inside `skills/<new-skill-name>/`.
2. Add a new row to the table in this file with its name, triggers, and Raw URL link.
