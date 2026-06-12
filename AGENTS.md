# AGENTS.md - PDF-combine

> 所有代理在開始處理本專案任何任務前，都必須先讀取本檔案。

PDF-combine 是一個小型 Python 桌面 / CLI 工具，用於將圖片合併成 PDF，或將 PDF 頁面轉成 PNG 圖檔。

## 專案入口

| 項目 | 內容 |
|---|---|
| 專案 | PDF-combine |
| 主要工作目錄 | `G:\我的雲端硬碟\Antigravity\PDF-combine` |
| 主程式 | `PDF-Combine.py` |
| 預設分支 | `main` |
| 執行環境 | Python 3.6+ |
| 主要套件 | Pillow, PyMuPDF, tkinter |

## 工作模式

- 固定專案規則、代理路由、canonical spec 決策與工作邊界放在本檔案。
- 進度、下一步、收工紀錄、阻塞點與踩坑筆記放在 Obsidian 專案駕駛艙。
- 新工作不要再使用 `ConversationRecord.txt` 或 `ConversationRecord.md` 作為進度主檔。
- 除非使用者明確要求，否則不要 commit、push、pull、刪除、搬移或覆蓋使用者變更。
- 不要寫入 API key、token、密碼、私人客戶資料或私人學生資料。

## Obsidian 對應

主要 Obsidian vault：

```text
G:\我的雲端硬碟\secondbrain\secondbrain
```

專案駕駛艙路徑：

```text
PDF-combine\專案工作流程.md
```

寫入 vault 內筆記時，內容優先使用 vault-relative path。跨設備同步的 Obsidian 筆記不要硬寫本機磁碟代號，除非該筆記明確是設備專用說明。

## 開工規則

當使用者說 `開工`、`start work`，或要求繼續本專案時：

1. 讀取本檔 `AGENTS.md`。
2. 讀取 Obsidian 駕駛艙：`PDF-combine\專案工作流程.md`。
3. 檢查 Git 狀態。
4. 回報目前狀態與下一個具體步驟。
5. 不要自動 pull、commit、push 或修改檔案。

## 收工規則

當使用者說 `收工`、`wrap up`，或要求結束本次工作時：

1. 摘要本次完成內容與驗證結果。
2. 更新 Obsidian 駕駛艙，記錄進度、下一步、阻塞點與踩坑筆記。
3. 只有固定專案規則變更時，才更新本 `AGENTS.md`。
4. 檢查 Git 狀態，並區分 Codex 本次變更與既有使用者變更。
5. 只有使用者明確要求時才 commit 或 push。

## Canonical API / Data Spec

本專案目前沒有服務端 API、資料庫 schema、外部 endpoint contract 或 canonical API spec。

- canonical API spec 路徑：目前不適用。
- canonical CLI spec 路徑：`docs/cli_spec.md`。
- README 放使用者導向說明；`docs/cli_spec.md` 放穩定 CLI 合約；實作位於 `PDF-Combine.py`。
- 若未來新增服務端 API、資料庫或結構化設定 schema，請先在 `docs/api_spec.md` 建立唯一 canonical API/data spec，並先在本檔記錄該決策，再新增其他規格文件。

## 廢棄功能

```yaml
deprecated_features:
  - id: repo_conversation_log_as_active_progress
    cancelled_date: "2026-06-12"
    keywords:
      - ConversationRecord.txt
      - ConversationRecord.md
      - repo progress log
      - 對話紀錄
    action: REJECT
    rejection_message: "不要再使用 repo 內的 ConversationRecord 檔案作為目前進度主檔。新進度請寫入 Obsidian 專案駕駛艙。"
```

## 代理註冊表

```yaml
agent_registry:
  - id: agent-orchestrator
    role: COORDINATOR
  - id: agent-python-tooling
    role: IMPLEMENTER
    layer: application
  - id: agent-qa
    role: VALIDATOR
  - id: agent-docs
    role: DOCUMENTER

routing_priority:
  1: deprecated_features
  2: single_layer_match
  3: validation_or_docs
  4: fallback
```

## Orchestrator Agent

### Agent Schema

```yaml
agent_schema:
  id: agent-orchestrator
  role: COORDINATOR
  description: >
    負責將 PDF-combine 任務路由到正確的專職代理。它可以把需求拆成實作、
    驗證與文件工作，但不直接撰寫程式碼。在派工前，必須先檢查廢棄功能
    與專案治理規則。
  input_types:
    - user_request
    - project_status
  output_types:
    - task_assignment
    - final_summary
    - clarification_request
  triggers:
    - pattern: "所有使用者輸入都先進入此代理，再進行專職路由"
  excludes:
    - "未經路由直接實作"
    - "要求覆蓋不相關的使用者變更"
  depends_on: []
  can_parallel: false
  confidence_threshold: 0.75
  pending_decisions:
    - id: conversation_record_encoding_cleanup
      description: "部分歷史 ConversationRecord 紀錄有 mojibake 亂碼，清理前需先確認來源編碼。"
      status: BLOCKED_PENDING_CONFIRMATION
      affects: [agent-docs]
```

### 路由規則

- `PDF-Combine.py` 的功能或 bug 工作交給 `agent-python-tooling`。
- 測試設計、人工驗證、相依套件檢查與回歸風險檢查交給 `agent-qa`。
- README、changelog、駕駛艙更新與治理筆記交給 `agent-docs`。
- 跨層工作流程為：`agent-python-tooling` -> `agent-qa` -> `agent-docs`。

### Pipeline Templates

```yaml
pipeline_templates:
  bug_fix:
    description: "重現或檢查問題，修補受影響的 Python 工具程式碼，然後驗證。"
    dag:
      - step: 1
        agent: agent-qa
        task_type: bug_reproduction
        can_parallel: false
      - step: 2
        agent: agent-python-tooling
        task_type: implementation
        depends_on: [agent-qa]
        can_parallel: false
      - step: 3
        agents: [agent-qa, agent-docs]
        task_type: [verification, documentation]
        depends_on: [agent-python-tooling]
        can_parallel: true
  docs_only:
    description: "不修改程式碼的文件或治理變更。"
    dag:
      - step: 1
        agent: agent-docs
        task_type: documentation
        can_parallel: true
  query_only:
    description: "只讀檢查或狀態回報。"
    dag:
      - step: 1
        agent: agent-qa
        task_type: inspection
        can_parallel: true
```

## Python Tooling Agent

### Agent Schema

```yaml
agent_schema:
  id: agent-python-tooling
  role: IMPLEMENTER
  layer: application
  description: >
    負責 PDF-Combine.py 的 Python 實作。維護 tkinter GUI 流程、argparse CLI 行為、
    Pillow 圖片轉 PDF、PyMuPDF PDF 轉 PNG、Windows 打包相容性與檔案系統驗證。
  input_types:
    - python_bug_report
    - cli_requirement
    - gui_requirement
    - file_conversion_requirement
    - packaging_requirement
  output_types:
    - python_patch
    - cli_behavior_change
    - gui_behavior_change
    - implementation_notes
  triggers:
    - keywords: ["PDF-Combine.py", "Python", "tkinter", "argparse", "Pillow", "PyMuPDF", "fitz"]
    - keywords: ["images-to-pdf", "pdf-to-png", "PDF", "PNG", "DPI", "page range", "頁碼", "圖片合併"]
    - pattern: "任務涉及轉換行為、GUI 提示、CLI 選項或打包相容性"
  excludes:
    - "純文件變更"
    - "不涉及程式碼變更的 GitHub 發布或 release 管理"
    - "使用 repo ConversationRecord 檔案作為目前進度主檔"
  depends_on: []
  can_parallel: false
  confidence_threshold: 0.75
  known_apis:
    - name: "images_to_pdf"
      signature: "images_to_pdf(image_folder, output_pdf, notify=True)"
      location: "PDF-Combine.py"
      status: ACTIVE
    - name: "pdf_to_png"
      signature: "pdf_to_png(input_pdf, output_folder, dpi=200, pages='', notify=True)"
      location: "PDF-Combine.py"
      status: ACTIVE
    - name: "parse_page_selection"
      signature: "parse_page_selection(selection, page_count)"
      location: "PDF-Combine.py"
      status: ACTIVE
```

### 職責

- 除非使用者明確選擇單一模式，否則 GUI 與 CLI 行為需保持一致。
- 修改 stdout、錯誤處理或訊息顯示時，保留 Windows no-console 相容性。
- 轉換前需驗證輸出路徑與使用者選取的檔案。
- 除非使用者明確要求，避免修改 `dist/`、`build/`、PDF、PNG 輸出或 `.spec` 等產物檔。

### 輸入格式

```text
任務：
受影響行為：
允許編輯的檔案：
需要驗證的項目：
```

### 輸出格式

```text
變更檔案：
行為摘要：
已執行驗證：
風險或後續事項：
```

## QA Agent

### Agent Schema

```yaml
agent_schema:
  id: agent-qa
  role: VALIDATOR
  description: >
    負責驗證這個小型 Python 轉換工具的行為。檢查頁碼解析、錯誤處理、
    相依套件可用性、Git 乾淨程度與人工測試路徑，且不修改程式碼。
    它是只讀檢查任務的預設代理。
  input_types:
    - implemented_feature
    - bug_report
    - validation_request
    - git_status
    - dependency_check
  output_types:
    - verification_report
    - manual_test_script
    - risk_report
    - bug_analysis
  triggers:
    - keywords: ["test", "verify", "validation", "QA", "Git status", "dependency", "requirements"]
    - keywords: ["pytest", "manual test", "smoke test", "regression", "檢查", "驗證"]
    - pattern: "任務詢問目前專案狀態是否安全、完整或可運作"
  excludes:
    - "實作 Python 變更"
    - "以撰寫文件作為主要交付"
  depends_on: []
  can_parallel: true
  confidence_threshold: 0.70
```

### 職責

- 若有範例檔，優先使用輕量 smoke test 驗證轉換函式。
- 分開回報既有 Git 變更與本次任務造成的變更。
- 檢查換行、編碼與打包風險。

### 輸入格式

```text
驗證目標：
已知變更檔案：
允許執行的命令：
預期行為：
```

### 輸出格式

```text
結果：
執行命令：
發現事項：
殘留風險：
```

## Docs Agent

### Agent Schema

```yaml
agent_schema:
  id: agent-docs
  role: DOCUMENTER
  description: >
    負責人類可讀文件與專案治理筆記。更新 README、AGENTS.md、Obsidian 駕駛艙摘要
    與 changelog 類紀錄，同時保持固定規則與進度筆記分離。它不修改應用程式碼。
  input_types:
    - documentation_request
    - governance_update
    - feature_completion
    - progress_summary
    - cockpit_update
  output_types:
    - readme_update
    - governance_note
    - cockpit_entry
    - changelog_entry
    - progress_report
  triggers:
    - keywords: ["README", "AGENTS.md", "Obsidian", "專案工作流程", "documentation", "docs"]
    - keywords: ["開工", "收工", "progress", "changelog", "governance", "治理"]
    - pattern: "任務是在記錄專案知識、工作流程或使用者文件"
  excludes:
    - "修改 PDF 轉換實作"
    - "執行 release 打包"
  depends_on: []
  can_parallel: true
  confidence_threshold: 0.65
  known_issues:
    - id: conversation_record_mojibake
      severity: P2
      description: "部分歷史 ConversationRecord 紀錄有 mojibake 亂碼，不應在未確認前靜默改寫。"
      status: PENDING_CONFIRMATION
      assigned_fix: agent-docs
```

### 職責

- 專案固定規則放在 `AGENTS.md`。
- 進度、下一步、阻塞點與踩坑筆記放在 Obsidian 駕駛艙。
- 保留歷史紀錄；不確定或損壞的紀錄需標記為待確認。

### 輸入格式

```text
文件目標：
來源事實：
允許編輯的檔案：
語氣或格式限制：
```

### 輸出格式

```text
變更文件：
摘要：
待確認問題：
```

## Context Firewall

```yaml
context_firewall:
  rules:
    - id: CONTEXT_ISOLATION
      description: "代理只接收其負責層所需的檔案與事實。"
    - id: NO_DIRECT_COMMUNICATION
      description: "子代理一律透過 orchestrator 回報結果。"
    - id: SECRET_EXCLUSION
      description: "prompt 或筆記中不得包含 secrets、tokens、密碼、私人客戶資料或私人學生資料。"
    - id: LAYER_BOUNDARY
      description: "代理只能編輯其被指派的檔案與責任範圍。"
    - id: RESULT_ONLY_REPORT
      description: "代理回報結果、變更檔案、驗證與風險，不傾倒不必要的中間推理。"
```

## 自動路由演算法

```text
STEP 1  讀取 AGENTS.md 並檢查 deprecated_features。
STEP 2  若命中廢棄功能，拒絕或要求使用者確認例外。
STEP 3  擷取任務特徵：目標檔案、要求輸出、關鍵字與風險等級。
STEP 4  依 trigger 命中減去 excludes，替每個代理評分。
STEP 5  單一強匹配時，派工給該代理。
STEP 6  多代理工作依 pipeline_templates 建立 DAG。
STEP 7  沒有足夠信心的匹配時，向使用者提出一個精簡釐清問題。
STEP 8  最終回覆需報告變更檔案、驗證結果與剩餘風險。
```

## 版本紀錄

| 版本 | 日期 | 變更 |
|---|---|---|
| v1.0 | 2026-06-12 | 建立初版 Codex 工作模式治理、代理路由、Obsidian 駕駛艙對應與 API spec 決策。 |
| v1.1 | 2026-06-12 | 補充 canonical CLI spec 路徑，區分 CLI contract 與 API/data spec。 |
| v1.2 | 2026-06-12 | 依 PyMuPDF 需求同步文件建議 Python 版本為 3.9+。 |
