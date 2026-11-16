# Central Agent Skills Map & Dynamic Router

> **Repository**: [xinbato/Skill-Repository](https://github.com/xinbato/Skill-Repository)  
> **Standard**: [agentskills.io](https://agentskills.io) & [agent-plugins.org](https://agent-plugins.org)  
> **Version**: 1.2.0

---

## Instructions for AI Agents (System Directive)

You are an AI Agent reading this dynamic skills router. This repository provides a complete software engineering ecosystem: **Skills** (*How*), **Personas** (*Who*), **Commands** (*When*), and **Shared Checklists** (*References*).

### Operational Protocol
Whenever the user asks you to perform a task:
1. **Scan**: Consult the [Skill Catalog](#skill-catalog) below to see if an available skill matches the user's intent.
2. **Detect**: Check whether the skill already exists in the workspace (standard cross-client location: `.agents/skills/<skill-name>/` or `.skills/<skill-name>/`).
3. **Fetch on Demand**: If the skill is not yet installed locally, download its `SKILL.md` (and any scripts/references) using one of the [Dynamic Fetch Commands](#dynamic-fetch-commands) or by fetching the Raw GitHub URL directly into `.agents/skills/<skill-name>/`.
4. **Activate**: Read the downloaded `SKILL.md` into your context (Progressive Disclosure - Activation stage).
5. **Execute**: Follow the instructions in `SKILL.md` to complete the user's request.

---

## Skill Catalog

### 1. General & Engineering Lifecycle Skills (`skills/general/`)

Universal skills covering the complete Software Development Lifecycle (SDLC) from intent discovery to shipping.

| Skill Name | Description & Trigger Keywords | Category | Direct Raw URL |
| :--- | :--- | :--- | :--- |
| **`interview-me`** | **Phỏng vấn làm rõ mong muốn cốt lõi của người dùng**. Đặt từng câu hỏi kèm giả định (hypothesis) để tìm ra bản chất yêu cầu trước khi viết spec hoặc code. Kích hoạt khi: *"Interview me"*, *"Grill me"*, *"Làm rõ yêu cầu"*, *"Hỏi tôi trước khi làm"*. | Requirements & Discovery | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/interview-me/SKILL.md) |
| **`spec-driven-development`** | **Viết đặc tả yêu cầu (PRD/Spec) trước khi lập trình**. Đảm bảo mọi tính năng đều có mục tiêu, use cases, ranh giới và tiêu chí nghiệm thu rõ ràng. Kích hoạt khi: *"Tạo spec"*, *"Viết PRD"*, *"Đặc tả tính năng"*, *"Spec before code"*. | Requirements & PRD | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/spec-driven-development/SKILL.md) |
| **`planning-and-task-breakdown`** | **Phân rã đặc tả thành các công việc nguyên tử (atomic tasks)**. Sắp xếp thứ tự thực thi hợp lý, tối ưu cho context window của Agent. Kích hoạt khi: *"Lập kế hoạch"*, *"Chia nhỏ task"*, *"Task breakdown"*, *"Plan implementation"*. | Planning & Tasks | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/planning-and-task-breakdown/SKILL.md) |
| **`incremental-implementation`** | **Triển khai tính năng theo từng lát cắt mỏng (thin vertical slices)**. Code và kiểm chứng từng phần nhỏ, commit liên tục, không bao giờ code dồn đống lớn. Kích hoạt khi: *"Incremental build"*, *"Code từng bước"*, *"Thin slice"*. | Implementation | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/incremental-implementation/SKILL.md) |
| **`test-driven-development`** | **Phát triển hướng kiểm thử (TDD) theo chu trình Red-Green-Refactor**. Viết test chứng minh lỗi trước khi viết code xử lý. Kích hoạt khi: *"TDD"*, *"Viết test trước"*, *"Red-green-refactor"*, *"Test-driven"*. | Testing & Quality | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/test-driven-development/SKILL.md) |
| **`debugging-and-error-recovery`** | **Quy trình gỡ lỗi có hệ thống tìm nguyên nhân gốc rễ (Root Cause)**. Tái hiện lỗi -> Cô lập phạm vi -> Sửa chữa có kiểm chứng, chấm dứt sửa mò. Kích hoạt khi: *"Debug lỗi"*, *"Fix bug"*, *"Root cause analysis"*, *"Bị crash"*. | Debugging & Diagnostics | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/debugging-and-error-recovery/SKILL.md) |
| **`code-review-and-quality`** | **Rà soát mã nguồn toàn diện theo 5 trục chất lượng**. Đánh giá Tính đúng đắn, Khả năng đọc, Kiến trúc, Bảo mật, Hiệu năng theo các cấp độ Critical/Required/Optional/Nit. Kích hoạt khi: *"Review code"*, *"Đánh giá PR"*, *"Code health check"*. | Code Review & QA | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/code-review-and-quality/SKILL.md) |
| **`code-simplification`** | **Tối giản hóa và làm trong sáng mã nguồn**. Loại bỏ over-engineering, làm phẳng logic lồng nhau mà không thay đổi hành vi code. Kích hoạt khi: *"Simplify code"*, *"Tối giản code"*, *"Refactor cho gọn"*, *"Clarity over cleverness"*. | Refactoring | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/code-simplification/SKILL.md) |
| **`source-driven-development`** | **Căn cứ mọi quyết định kỹ thuật trên tài liệu và mã nguồn chính thức**. Đọc code framework và docs chuẩn để chống ảo giác (hallucination). Kích hoạt khi: *"Kiểm tra tài liệu chính thức"*, *"Ground in source"*, *"Verify against framework docs"*. | Architecture & Grounding | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/source-driven-development/SKILL.md) |
| **`shipping-and-launch`** | **Chuẩn bị phát hành phần mềm lên môi trường production**. Checklist nghiệm thu kỹ thuật, kế hoạch di chuyển dữ liệu (migration) và rollback an toàn. Kích hoạt khi: *"Chuẩn bị ship"*, *"Release to production"*, *"Pre-launch checklist"*. | Release & Operations | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/shipping-and-launch/SKILL.md) |
| **`find-skills`** | **Tìm kiếm và cài đặt Agent Skills từ hệ sinh thái mở toàn cầu**. Khai thác `npx skills` và skills.sh để mở rộng năng lực cho Agent khi gặp tác vụ mới chưa có skill nội bộ. Kích hoạt khi: *"Tìm skill cho X"*, *"How do I do X"*, *"Search skills"*, *"Cài đặt skill"*. | Developer Tooling / Discovery | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/find-skills/SKILL.md) |
| **`create-skill-v2`** | **Tạo và tối ưu hóa Agent Skill thế hệ mới (v2)**. Nạp template động từ `assets/`, tích hợp runner đo kiểm eval đa nền tảng không lỗi trên Windows (`run_eval.py`), xuất báo cáo HTML (`generate_report.py`). | Developer Tooling | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/create-skill-v2/SKILL.md) |
| **`create-skill`** | **Tạo và chuẩn hóa Agent Skill mới (v1)**. Khởi tạo cấu trúc thư mục, script CLI, tài liệu tham khảo và metadata hợp lệ theo chuẩn agentskills.io. | Developer Tooling | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/create-skill/SKILL.md) |
| **`git-workflow`** | **Chuẩn hóa quy trình Git & Conventional Commits**. Phân tích git status/diff, chặn commit lộ secret, viết commit message chuẩn và sinh mẫu PR description. | Version Control / DevOps | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/git-workflow/SKILL.md) |
| **`email-teacher`** | **Soạn thư/email chuẩn mực gửi Thầy Cô/Giảng viên**. Kích hoạt khi: Xin nghỉ học, xin gia hạn deadline, hỏi bài tập, thắc mắc môn học. Tự động thích ứng ngôn ngữ. | Academic / Communication | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/general/email-teacher/SKILL.md) |

### 2. Anthropic Ecosystem Skills (`skills/anthropic/`)

Document processing, UI design, generative art, and protocol servers originating from Anthropic.

| Skill Name | Description & Trigger Keywords | Category | Direct Raw URL |
| :--- | :--- | :--- | :--- |
| **`pdf`** | **Xử lý tài liệu PDF toàn diện**. Trích xuất văn bản, bảng biểu, gộp file, tách trang, xoay trang, đóng dấu watermark, điền form PDF và nhận dạng ký tự OCR. | Document Processing | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/pdf/SKILL.md) |
| **`docx`** | **Tạo, đọc và chỉnh sửa file Word (.docx, .dotx)**. Tạo báo cáo, thư từ, biểu mẫu có mục lục, bảng biểu chuẩn xác, chèn ảnh, tìm kiếm thay thế và theo dõi tracked changes. | Document Processing | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/docx/SKILL.md) |
| **`xlsx`** | **Thao tác bảng tính Excel (.xlsx, .xlsm, .csv)**. Mở, phân tích, tính toán công thức, format ô, vẽ biểu đồ, dọn dẹp dữ liệu dạng bảng lộn xộn thành bảng tính chuyên nghiệp. | Data & Spreadsheets | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/xlsx/SKILL.md) |
| **`pptx`** | **Tạo và biên tập slide thuyết trình PowerPoint (.pptx, .potx)**. Tạo bài thuyết trình, pitch deck, đọc trích xuất nội dung slide, sửa bố cục, thêm ghi chú người thuyết trình (speaker notes). | Presentation / Office | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/pptx/SKILL.md) |
| **`mcp-builder`** | **Xây dựng máy chủ Model Context Protocol (MCP)**. Thiết kế công cụ và tài nguyên chuẩn cho LLM bằng Python (FastMCP) hoặc Node/TypeScript MCP SDK để tích hợp dịch vụ ngoài. | AI Engineering / MCP | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/mcp-builder/SKILL.md) |
| **`webapp-testing`** | **Kiểm thử tự động giao diện ứng dụng web cục bộ (localhost)**. Sử dụng Playwright để xác thực tính năng frontend, debug hành vi UI và bắt lỗi qua ảnh chụp màn hình. | Testing & Automation | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/webapp-testing/SKILL.md) |
| **`frontend-design`** | **Chỉ dẫn tư duy thiết kế giao diện UI/UX đặc sắc**. Định hướng thẩm mỹ, phân cấp typography, bảng màu có chủ đích, tránh giao diện bị khuôn mẫu AI generic. | UI/UX & Design | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/frontend-design/SKILL.md) |
| **`theme-factory`** | **Bộ công cụ áp dụng theme định sẵn**. Áp dụng 10 theme màu sắc và typography đồng bộ cho slide, tài liệu báo cáo và landing page. | UI/UX & Design | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/theme-factory/SKILL.md) |
| **`algorithmic-art`** | **Sáng tạo nghệ thuật thuật toán bằng p5.js**. Tạo generative art tương tác, xử lý flow field và số ngẫu nhiên có kiểm soát (seeded randomness). | Creative & Art | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/algorithmic-art/SKILL.md) |
| **`canvas-design`** | **Thiết kế đồ họa canvas và poster xuất ra PNG/PDF**. Ứng dụng triết lý thiết kế thị giác, căn chỉnh lưới và typography chặt chẽ cho poster, ấn phẩm tĩnh. | Creative & Art | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/canvas-design/SKILL.md) |
| **`brand-guidelines`** | **brand-guidelines**: Applies Anthropic official brand colors and typography to any sort of artifact that may benefit from having Anthropic look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design a... | Anthropic Ecosystem | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/anthropic/brand-guidelines/SKILL.md) |
### 3. OpenAI Ecosystem Skills (`skills/openai/`)

Browser automation and application security skills from OpenAI.

| Skill Name | Description & Trigger Keywords | Category | Direct Raw URL |
| :--- | :--- | :--- | :--- |
| **`playwright`** | **Tự động hóa trình duyệt web thực tế từ dòng lệnh**. Điều hướng trang, điền form, chụp ảnh màn hình, cào dữ liệu và debug giao diện web tự động. | Testing & Automation | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/openai/playwright/SKILL.md) |
| **`security-threat-model`** | **Mô hình hóa mối đe dọa bảo mật theo mã nguồn**. Nhận diện ranh giới tin cậy (trust boundaries), tài sản dữ liệu, kịch bản tấn công và đề xuất giải pháp phòng ngừa theo chuẩn AppSec. | Security | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/openai/security-threat-model/SKILL.md) |
| **`security-best-practices`** | **Rà soát mã nguồn theo tiêu chuẩn bảo mật chuyên sâu**. Đánh giá bảo mật cho Python, JS/TS, Go; phát hiện lỗ hổng SQLi, XSS, token handling và đề xuất code sửa chuẩn. | Security | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/openai/security-best-practices/SKILL.md) |

### 4. Google Ecosystem Skills (`skills/google/`)

Official enterprise cloud infrastructure, Gemini API, BigQuery, and developer platform skills from Google.

| Skill Name | Description & Trigger Keywords | Category | Direct Raw URL |
| :--- | :--- | :--- | :--- |
| **`gemini-api`** | **gemini-api**: Use when the user asks about using Gemini in an enterprise environment or explicitly mentions Vertex AI, Google Cloud, or Agent Platform. Guides the usage of the Gemini API on Agent Platform with the Google Gen AI SDK... | Google Ecosystem | [Fetch Raw](https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/google/gemini-api/SKILL.md) |

---

## Shared Engineering References (`references/`)

Repo-wide authoritative checklists and standards located at `references/`:
- [`definition-of-done.md`](references/definition-of-done.md): The project-wide Definition of Done that every task clears.
- [`orchestration-patterns.md`](references/orchestration-patterns.md): Endorsed multi-agent orchestration patterns (Parallel Fan-out with Merge).
- [`security-checklist.md`](references/security-checklist.md): Core application security review checklist.
- [`performance-checklist.md`](references/performance-checklist.md): Frontend, backend, and database performance checklist.
- [`testing-patterns.md`](references/testing-patterns.md): Concrete testing patterns (Jest, RTL, Supertest, Playwright).
- [`accessibility-checklist.md`](references/accessibility-checklist.md): Web accessibility and WCAG compliance checks.

---

## Expert Personas (`agents/`)

Specialized expert roles designed for parallel subagent invocation:
- **`code-reviewer`** ([`agents/code-reviewer.md`](agents/code-reviewer.md)): Senior Staff Engineer evaluating correctness, readability, architecture, security, and performance.
- **`security-auditor`** ([`agents/security-auditor.md`](agents/security-auditor.md)): Security specialist auditing input validation, auth, secrets, and trust boundaries.
- **`test-engineer`** ([`agents/test-engineer.md`](agents/test-engineer.md)): QA engineer evaluating test coverage, boundary conditions, and test reliability.
- **`web-performance-auditor`** ([`agents/web-performance-auditor.md`](agents/web-performance-auditor.md)): Web performance auditor focusing on Core Web Vitals and resource budgets.

---

## Slash Commands (`commands/`)

Pre-packaged lifecycle commands that activate skills automatically:
- `/spec`: Defines requirements and generates PRD (`commands/spec.toml`).
- `/plan`: Breaks requirements into ordered tasks (`commands/planning.toml`).
- `/build`: Incrementally implements tasks one slice at a time (`commands/build.toml`).
- `/test`: Verifies behavior using test-driven development (`commands/test.toml`).
- `/review`: Executes a five-axis code review before merge (`commands/review.toml`).
- `/code-simplify`: Refactors code for maximum clarity (`commands/code-simplify.toml`).
- `/ship`: Merges reports from multiple personas and prepares production release (`commands/ship.toml`).

---

## Dynamic Fetch Commands

When you need to pull a skill into the current workspace, run any of the following commands:
### Option 1: Universal Python One-Liner (Cross-Platform)
```bash
python -c "import urllib.request, os; group='general'; name='interview-me'; os.makedirs(f'.agents/skills/{name}', exist_ok=True); urllib.request.urlretrieve(f'https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/{group}/{name}/SKILL.md', f'.agents/skills/{name}/SKILL.md'); print(f'Installed {name}')"
```

### Option 2: PowerShell (Windows Native)
```powershell
$group = "general"; $name = "interview-me"; New-Item -ItemType Directory -Force -Path ".agents/skills/$name" | Out-Null; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/$group/$name/SKILL.md" -OutFile ".agents/skills/$name/SKILL.md"; Write-Host "Installed $name"
```

### Option 3: Bash / cURL (macOS / Linux)
```bash
GROUP="general" && NAME="interview-me" && mkdir -p ".agents/skills/$NAME" && curl -sSL "https://raw.githubusercontent.com/xinbato/Skill-Repository/main/skills/$GROUP/$NAME/SKILL.md" -o ".agents/skills/$NAME/SKILL.md" && echo "Installed $NAME"
```
