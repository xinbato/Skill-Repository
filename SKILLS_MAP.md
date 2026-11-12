# Central Agent Skills Map & Dynamic Router

> **Repository**: [xinbato/Skill-Repository](https://github.com/xinbato/Skill-Repository)  
> **Standard**: [agentskills.io](https://agentskills.io)  
> **Version**: 1.1.0

---

## Instructions for AI Agents (System Directive)

You are an AI Agent reading this dynamic skills router. This file connects you to the centralized **Skill Repository** hosted at `https://github.com/xinbato/Skill-Repository`.

### Operational Protocol
Whenever the user asks you to perform a task:
1. **Scan**: Consult the [Skill Catalog](#skill-catalog) below to see if an available skill matches the user's intent.
2. **Detect**: Check whether the skill already exists in the workspace (standard cross-client location: `.agents/skills/<skill-name>/` or `.skills/<skill-name>/`).
3. **Fetch on Demand**: If the skill is not yet installed locally, download its `SKILL.md` (and any scripts/references) using one of the [Dynamic Fetch Commands](#dynamic-fetch-commands) or by fetching the Raw GitHub URL directly into `.agents/skills/<skill-name>/`.
4. **Activate**: Read the downloaded `SKILL.md` into your context (Progressive Disclosure - Activation stage).
5. **Execute**: Follow the instructions in `SKILL.md` to complete the user's request.

---

## Skill Catalog

| Skill Name | Description & Trigger Keywords | Category | Direct Raw URL |
| :--- | :--- | :--- | :--- |
| **`create-skill`** | **Tạo và chuẩn hóa Agent Skill mới**. Sử dụng khi người dùng yêu cầu: *"Tạo skill mới"*, *"Khởi tạo skill [tên]"*, *"Scaffold skill"*, *"Viết SKILL.md theo chuẩn"*. Tự động tạo cấu trúc thư mục, script CLI, tài liệu tham khảo, bộ kiểm thử evals và metadata hợp lệ. | Developer Tooling | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/create-skill/SKILL.md) |
| **`git-workflow`** | **Chuẩn hóa quy trình Git & Conventional Commits**. Sử dụng khi người dùng yêu cầu: *"Commit code"*, *"Tạo commit message"*, *"Chuẩn bị PR"*, *"Kiểm tra git diff"*, *"Tạo nhánh mới"*. Tự động phân tích git status/diff, chặn commit lộ secret, viết commit message chuẩn và sinh mẫu PR description. | Version Control / DevOps | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/git-workflow/SKILL.md) |
| **`email-teacher`** | **Soạn thư/email chuẩn mực gửi Thầy Cô/Giảng viên**. Kích hoạt khi: *"Xin nghỉ học"*, *"Xin hoãn/gia hạn deadline"*, *"Hỏi bài/thắc mắc môn học"*, *"Leave request"*, *"Deadline extension"*. Tự động nhận diện ý định ngay cả khi không có từ "email", tự động điều chỉnh ngôn ngữ đầu ra theo ngôn ngữ người dùng. | Academic / Communication | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/email-teacher/SKILL.md) |
| **`pdf`** | **Xử lý tài liệu PDF toàn diện**. Trích xuất văn bản, bảng biểu, gộp file, tách trang, xoay trang, đóng dấu watermark, điền form PDF và nhận dạng ký tự OCR. | Document Processing | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/pdf/SKILL.md) |
| **`docx`** | **Tạo, đọc và chỉnh sửa file Word (.docx, .dotx)**. Tạo báo cáo, thư từ, biểu mẫu có mục lục, bảng biểu chuẩn xác, chèn ảnh, tìm kiếm thay thế và theo dõi tracked changes. | Document Processing | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/docx/SKILL.md) |
| **`xlsx`** | **Thao tác bảng tính Excel (.xlsx, .xlsm, .csv)**. Mở, phân tích, tính toán công thức, format ô, vẽ biểu đồ, dọn dẹp dữ liệu dạng bảng lộn xộn thành bảng tính chuyên nghiệp. | Data & Spreadsheets | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/xlsx/SKILL.md) |
| **`pptx`** | **Tạo và biên tập slide thuyết trình PowerPoint (.pptx, .potx)**. Tạo bài thuyết trình, pitch deck, đọc trích xuất nội dung slide, sửa bố cục, thêm ghi chú người thuyết trình (speaker notes). | Presentation / Office | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/pptx/SKILL.md) |
| **`mcp-builder`** | **Xây dựng máy chủ Model Context Protocol (MCP)**. Thiết kế công cụ và tài nguyên chuẩn cho LLM bằng Python (FastMCP) hoặc Node/TypeScript MCP SDK để tích hợp dịch vụ ngoài. | AI Engineering / MCP | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/mcp-builder/SKILL.md) |
| **`playwright`** | **Tự động hóa trình duyệt web thực tế từ dòng lệnh**. Điều hướng trang, điền form, chụp ảnh màn hình, cào dữ liệu và debug giao diện web tự động. | Testing & Automation | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/playwright/SKILL.md) |
| **`webapp-testing`** | **Kiểm thử tự động giao diện ứng dụng web cục bộ (localhost)**. Sử dụng Playwright để xác thực tính năng frontend, debug hành vi UI và bắt lỗi qua ảnh chụp màn hình. | Testing & Automation | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/webapp-testing/SKILL.md) |
| **`security-threat-model`** | **Mô hình hóa mối đe dọa bảo mật theo mã nguồn**. Nhận diện ranh giới tin cậy (trust boundaries), tài sản dữ liệu, kịch bản tấn công và đề xuất giải pháp phòng ngừa theo chuẩn AppSec. | Security | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/security-threat-model/SKILL.md) |
| **`security-best-practices`** | **Rà soát mã nguồn theo tiêu chuẩn bảo mật chuyên sâu**. Đánh giá bảo mật cho Python, JS/TS, Go; phát hiện lỗ hổng SQLi, XSS, token handling và đề xuất code sửa chuẩn. | Security | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/security-best-practices/SKILL.md) |
| **`frontend-design`** | **Chỉ dẫn tư duy thiết kế giao diện UI/UX đặc sắc**. Định hướng thẩm mỹ, phân cấp typography, bảng màu có chủ đích, tránh giao diện bị khuôn mẫu AI generic. | UI/UX & Design | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/frontend-design/SKILL.md) |
| **`theme-factory`** | **Bộ công cụ áp dụng theme định sẵn**. Áp dụng 10 theme màu sắc và typography đồng bộ cho slide, tài liệu báo cáo và landing page. | UI/UX & Design | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/theme-factory/SKILL.md) |
| **`algorithmic-art`** | **Sáng tạo nghệ thuật thuật toán bằng p5.js**. Tạo generative art tương tác, xử lý flow field và số ngẫu nhiên có kiểm soát (seeded randomness). | Creative & Art | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/algorithmic-art/SKILL.md) |
| **`canvas-design`** | **Thiết kế đồ họa canvas và poster xuất ra PNG/PDF**. Ứng dụng triết lý thiết kế thị giác, căn chỉnh lưới và typography chặt chẽ cho poster, ấn phẩm tĩnh. | Creative & Art | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/canvas-design/SKILL.md) |

---

## Dynamic Fetch Commands

When you need to pull a skill into the current workspace, run any of the following commands:

### Option 1: Universal Python One-Liner (Cross-Platform)
```bash
python -c "import urllib.request, os; name='create-skill'; os.makedirs(f'.agents/skills/{name}', exist_ok=True); urllib.request.urlretrieve(f'https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/{name}/SKILL.md', f'.agents/skills/{name}/SKILL.md'); print(f'Installed {name}')"
```

### Option 2: PowerShell (Windows Native)
```powershell
$name = "create-skill"; New-Item -ItemType Directory -Force -Path ".agents/skills/$name" | Out-Null; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/$name/SKILL.md" -OutFile ".agents/skills/$name/SKILL.md"; Write-Host "Installed $name"
```

### Option 3: Bash / cURL (macOS / Linux)
```bash
NAME="create-skill" && mkdir -p ".agents/skills/$NAME" && curl -sSL "https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/$NAME/SKILL.md" -o ".agents/skills/$NAME/SKILL.md" && echo "Installed $NAME"
```

### Option 4: Full Skill Clone via Git Sparse-Checkout
If the skill requires its `scripts/`, `references/`, and `assets/` subdirectories:
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/xinbato/Skill-Repository.git .temp-skills
cd .temp-skills && git sparse-checkout set skills/create-skill
# Move to .agents/skills/create-skill or skills/create-skill
```

---

## Updating this Map
When adding a new skill to `https://github.com/xinbato/Skill-Repository`:
1. Place the skill inside `skills/<new-skill-name>/`.
2. Add a new row to the table in this file with its name, triggers, category, and Raw URL link.
