# docflow   Word/Docs 自動化產稿專案
AI + Script 驅動的 Word / Google Docs 產稿流程


SPEC  讀取   ./dev/docs/spec.md
初期想法  讀取    ./dev/docs/plan.md 

---


本專案的目標是：  
在「需要大量產出 Word / Google Docs 文稿」的情境下，  
用 **人 + CLI 型 AI（例如 Claude Code / Gemini CLI / Chat Codex CLI）+ script** 的方式，把重複、機械的流程自動化，只留下需要人判斷的部分給編輯處理。

---

## 為什麼需要這個專案？（痛點）

- 實務上需要**大量產生 Word 檔**（報導、專刊、採訪稿、官方稿等）。
- 一般 AI 雖然擅長產生文字，但：
  - 對 **Word 格式** 不穩定（樣式、段落、頁首頁尾常會跑掉）。
  - 無法直接吃進現有的 `.docx` / Google Docs 版型來「套用」，人類仍要手動整理。
  - 不同 AI / 不同回合的輸出格式不一致，**後期整理成本非常高**。

因此，本專案希望建立一個「**標準中介格式（Markdown + 欄位結構）**」，再透過 script 統一轉成各種版本的 Word / Docs，讓 AI 專心寫內容，腳本專心做轉檔。

---

## 專案在解決什麼需求？

### 1. 模板（template / reference.docx）建立

- **使用者會提供一份或多份 Word `.docx` 範本**（現有刊物版型、現有專刊樣式）。
- 我們要：
  1. 協助把這些 `.docx` 轉成：
     - AI 可理解的「**欄位化模板（Markdown / JSON）**」
     - Word 的 **`reference.docx`**（做為排版樣式參考檔）
  2. 讓 CLI 型 AI 能依這些欄位寫出標準化的 `*.md` 文稿。
- 目標：
  - 不直接叫 AI「幫我產生一個漂亮的 Word」，而是：
    - 先讓 AI 填好「標準欄位」→ `稿件.md`
    - 再用 script + `reference.docx` 把 `稿件.md` 安全轉成符合樣式的 `.docx`。

### 2. docx / PDF / Google Docs 的互轉流程

- **使用者提供原始文稿**（可能來自 docx / PDF / Google Docs），格式通常不一致。
- 流程設計：
  1. Script 或人工先把原始檔轉成「可讀文字」（例如 Markdown 或純文字）。
  2. CLI AI 讀取這些原稿，並依照「模板欄位定義」進行：
     - 拆段
     - 重組
     - 填入標準欄位（例如：主標、眉標、摘要、段一～段四等）
  3. Script 再把 AI 生成的標準 `*.md` 檔：
     - 轉成 `.docx`（套版）
     - 視需求轉成：
       - PDF
       - 上傳並轉為 Google Docs
- 目標：
  - **輸入可以是多種格式**
  - **輸出也可以是多種格式**
  - 中間都統一走「欄位化 Markdown + JSON」這一層，方便維護與版控。

---

## 整體架構概念

系統主要由三個角色組成：

1. **人（編輯 / 企劃）**
   - 決定文稿目的、受眾、風格。
   - 提供範本 Word 檔（專刊版型、舊稿）。
   - 最終校對內容與格式，修正 AI 無法處理的細節。

2. **AI（CLI 型態的 AI，如 Claude Code / Gemini CLI / Chat Codex CLI）**
   - 讀取 `AGENTS.md`，理解自己在專案中的角色（例如「專刊編輯 AI」）。
   - 讀取 `docs/`、`templates/`、`sources/` 內的資料。
   - 依格式規範產生：
     - 標準化的「腳本」Markdown（例如 `腳本.md`）
     - 標準化的「採訪稿」或「成品稿」Markdown（例如 `採訪稿.md`）

3. **Script（Python 等）**
   - 把標準化的 `*.md` 轉成：
     - Word（`.docx`，搭配 `reference.docx`）
     - PDF
     - Google Docs（若有串 Google API）
   - 用 JSON 輸出欄位摘要（例如 `腳本欄位說明.json`），方便系統或人查閱。

> 原則：  
> **AI 與 Script 無法解決的部分（高度主觀判斷、領域敏感用語等），一律回到人工處理。**

---

## 典型資料流程

以下是從「原稿」到「成品 Word / Docs」的標準流程。

### Step 0. 準備專案目錄

建議結構（範例）：

```bash
project_root/
  README.md
  AGENTS.md

  docs/
    guidelines/
      腳本_格式說明.md
      採訪稿_格式說明.md
    sources/
      # 使用者提供的原始文稿，可能已先轉成 md
      09_化學署專刊_中華民國化學應變協會_何大成理事長-文稿_二版.md

  templates/
    腳本_template.md
    採訪稿_template.md

  reference/
    # 從使用者給的 Word 範本抽出的 reference.docx
    專刊版型_reference.docx

  outputs/
    腳本/
      # AI + script 產生的檔案會放這裡
    採訪稿/
      # 同上

  scripts/
    # 各種工具腳本，例如：
    generate_doc_outputs.py
    convert_google_docs.py
````

> 這個目錄結構可以被 AI CLI 直接閱讀，
> 也方便人類用 Git 管版。

---

### Step 1. 使用者提供 Word 範本（建立 template/reference）

1. 使用者提供一份或多份 `.docx`：

   * 例如：既有的專刊版型、既有報導樣式。
2. 人工或 script 先做一次整理：

   * 定義這個版型對應的欄位（例如：主標、眉標、摘要、段一～段四、小標等）。
   * 撰寫對應的 `*_template.md` 與 `*_格式說明.md`。
   * 若需要特別的 Word 樣式：

     * 把這份 `.docx` 作為 `reference.docx`。
3. 限制／ Side effect：

   * 不同刊物、不同版型可能需要不同 `reference.docx` 和不同 template。
   * 這一步通常需要**人類**決定哪些內容是「欄位」、哪些是「純裝飾」。

---

### Step 2. 使用者提供原稿（docx / PDF / Google Docs）

1. 使用者把原稿交給系統：

   * docx：可以用 pandoc 轉成 Markdown。
   * PDF：視品質可能需要 OCR / 手動清理。
   * Google Docs：

     * 可透過 API 匯出為 `.docx` 或 `.txt`，再轉換。
2. Script 或人工整理：

   * 把原稿放到 `docs/sources/` 下。
   * 若有需要，補上基本 metadata（例如：作者、日期、主題）。

限制／ Side effect：

* PDF 的轉換品質差異很大（掃描 PDF → OCR 可能有錯字）。
* 原稿結構不佳時，AI 需要更多提示才能拆段正確。

---

### Step 3. AI（CLI）讀取專案資料並產生標準 Markdown

在專案根目錄執行 CLI 型 AI，例如：Claude Code / Gemini CLI / Chat Codex CLI。
典型流程：

1. AI 讀取 `AGENTS.md`：

   * 知道自己是「專刊編輯 AI」，輸出規則為：

     * 僅輸出 Markdown
     * 嚴格依 `templates/` 的段落與欄位

2. AI 讀取相關 guideline：

   * `docs/guidelines/腳本_格式說明.md`
   * `docs/guidelines/採訪稿_格式說明.md`

3. AI 讀取原稿：

   * 例如 `docs/sources/09_化學署專刊_中華民國化學應變協會_何大成理事長-文稿_二版.md`

4. AI 讀取對應 template：

   * 例如：`templates/採訪稿_template.md`

5. AI 依照 template 填寫出一份完整的：

   * `腳本.md` 或 `採訪稿.md`（放在 `outputs/` 下）

限制／ Side effect：

* 各家 CLI 對「直接讀檔」的支援方式不同，有些需要手動貼文字，有些可以指定路徑。
* 若 template 寫得不清楚，AI 仍然可能產生不一致的欄位名稱或標題層級。

---

### Step 4. Script 將 Markdown 轉成 docx / PDF / Google Docs

接著由 script 接手，負責 **純技術性的轉檔工作**。

例：使用 `generate_doc_outputs.py`：

* 輸入：`outputs/採訪稿/採訪稿.md`
* 動作：

  1. 用 `pandoc` 套用 `reference/專刊版型_reference.docx`，產生：

     * `outputs/採訪稿/採訪稿_templete.docx`
  2. 解析 Markdown，輸出欄位摘要 JSON，例如：

     * `outputs/採訪稿/採訪稿說明.json`
       3.（選配）輸出 PDF 或給下一支 script 上傳到 Google Docs。

限制／ Side effect：

* 轉檔高度依賴 `pandoc` 與 `reference.docx` 設定：

  * 若 `reference.docx` 設計不佳，版面容易跑。
* Google Docs 的自動化上傳需要額外設定 OAuth / Service Account：

  * 在企業環境中，權限管理與審核流程可能較複雜。

---

### Step 5. 人工檢查與最後調整

即使整個流程自動化：

* **文字層面**：

  * 檢查 AI 是否誤解領域專有名詞。
  * 修正邏輯不順、語氣不合的地方。
* **排版層面**：

  * 微調行距、字型、標題樣式等細節。
  * 新增圖片／表格／註腳等 AI 不易處理的元素。

原則：

> 「程式 + AI」負責**80% 可標準化的工作**，
> 剩下 **20% 高價值判斷** 保留給編輯與專家。

---

## 未來可擴充方向

* 增加更多模板類型：

  * 報新聞稿、Q&A 專訪、年報專章、簡報講稿等。
* 更智慧的欄位萃取：

  * 讓 script 或額外 AI 自動從 Markdown 掃描出：主標、摘要、段落結構，而不是只用 regex。
* 整合 CI / CD：

  * 每次有新稿 push 上 Git repo，即自動跑轉檔流程，在 outputs/ 產出最新版 Word / PDF。

---

## 總結

這個專案不是要讓 AI「直接生出完美的 Word 檔」，而是：

1. 用 **模板 + 欄位結構** 把寫作與版型拆開。
2. 讓 AI 透過 CLI 模式，專心在「填寫欄位、重組內容、符合規範」。
3. 交由 script 做「格式轉換」與「套用 reference.docx」。
4. 最後由人類編輯做最終把關。

如此一來，大量 Word / Docs 文稿的產出可以高度自動化，同時保留必要的人類專業判斷與細緻調整。

```
```
