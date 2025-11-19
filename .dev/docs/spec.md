# SPEC：AI + Script 驅動的 Word / Google Docs 產稿流程

## 1. 專案目標

在需要大量產出 Word / Google Docs 文稿的情境下，本專案要達成：

- 讓 **AI（CLI 型，如 Claude Code / Gemini CLI / Chat Codex CLI）** 負責：
  - 讀取原始文稿（例如：`09_化學署專刊_中華民國化學應變協會 何大成理事長-文稿_二版`）
  - 依照定義好的欄位與模板，產出標準化的 Markdown 文稿（腳本 / 採訪稿）
- 讓 **Script** 負責：
  - Markdown ↔ docx / PDF / Google Docs 之間的轉換
  - 使用 `reference.docx` 套用版面
  - 產生欄位說明 JSON
- **人類編輯** 負責：
  - 定義模板與欄位
  - 提供範本 Word
  - 最終校稿與處理 AI 無法準確判斷的內容

目標是建立一個穩定可重複的「流水線」：  
**人（定規則） → AI（產標準化 Markdown） → Script（轉格式） → 人（最後確認）**。

---

## 2. 主要痛點與解法

### 痛點

1. 需要大量產生 Word 檔，但：
   - AI 直接產 `.docx` 容易跑版、樣式不一致。
   - 不同 AI / 不同回合輸出的格式不穩定。
2. 使用者已有大量 `.docx` / PDF / Google Docs 文稿與範本，但：
   - 難以讓 AI「套用既有版型」。
   - 人工轉格式成本高。

### 解法概要

1. **建立標準中介格式**：  
   所有內容統一先變成 **欄位化 Markdown + JSON**。
2. **模板 / reference.docx 抽象化**：  
   利用使用者提供的 Word 範本，建立：
   - AI 用的模板（`templates/*.md`）
   - Script 用的 `reference.docx`（排版樣式）
3. **CLI AI 只處理內容，不處理版型**：  
   AI 嚴格依模板填欄位，由 Script 做最後轉成 Word / PDF / Google Docs。

---

## 3. 使用情境（Use Cases）

1. **專刊採訪稿產出**
   - 使用者提供：  
     - 原始採訪文稿（docx / PDF / Google Docs）  
     - 專刊 Word 範本（排版樣式）
   - AI：  
     - 讀專案說明（`AGENTS.md`）+ 格式說明 + 原稿  
     - 產 `腳本.md`（規劃稿）與 `採訪稿.md`（成品文稿）
   - Script：  
     - `採訪稿.md` → `.docx`（套用 `reference.docx`）→ PDF / Google Docs

2. **既有 Word 文稿標準化**
   - 使用者提供：多篇雜亂 Word 文稿
   - Script：轉成 Markdown 初稿
   - AI：依模板重整成欄位化 Markdown（含主標、眉標、摘要、段落結構）
   - Script：再轉回新版 Word（統一版型）

3. **跨格式轉換**
   - Input：docx / PDF / Google Docs
   - 中繼：Markdown + JSON
   - Output：docx / PDF / Google Docs  
   （同樣走模板流程，保持欄位一致）

---

## 4. 系統角色與邊界

### 4.1 人類（Editor / PM）

- 決定專案需求與欄位：
  - 例如：主標、眉標、摘要、段一〜段四、小標、經歷等。
- 提供 `.docx` 範例做為版型來源。
- 改寫 `templates/*.md`、`docs/guidelines/*.md`。
- 最後審查 AI 生成的內容與轉出結果。

### 4.2 AI（CLI 型態）

- 代表工具：Claude Code / Gemini CLI / Chat Codex CLI / 其他支援讀檔的 CLI。
- 能力：
  - 讀取專案目錄中的 Markdown / 文稿。
  - 依 `AGENTS.md` 的角色與 `templates/*.md` 的格式產出 Markdown。
- 限制：
  - 不直接負責 `.docx` 版面。
  - 不直接操控 Google Docs API（交給 Script 層）。

### 4.3 Script（Python / 其他）

- 功能：
  - 利用 pandoc 等工具完成 Markdown ↔ docx / PDF 轉換。
  - 套用 `reference.docx` 確保樣式一致。
  - 根據 `*.md` 解析欄位，產生 `*_欄位說明.json`。
  - 選配：與 Google Drive / Docs API 整合。
- 限制：
  - 無法保證所有複雜版面百分之百無損。
  - PDF / 掃描文件仍可能需要人工修正。

---

## 5. 目錄結構規格

> 下列為建議初始結構，可依實務調整。

```bash
project_root/
  README.md
  SPEC.md
  AGENTS.md          # AI 角色與工作流程說明

  docs/
    guidelines/      # 格式規範（給 AI 看）
      腳本_格式說明.md
      採訪稿_格式說明.md
    sources/         # 原始文稿（使用者提供）
      09_化學署專刊_中華民國化學應變協會_何大成理事長-文稿_二版.md
      # 其他來源資料

  templates/         # AI 輸出用範本（Markdown）
    腳本_template.md
    採訪稿_template.md

  reference/         # Word 版面樣式
    專刊版型_reference.docx
    # 其他版型的 reference.docx

  outputs/
    腳本/
      腳本.md
      腳本_templete.docx
      腳本欄位說明.json
    採訪稿/
      採訪稿.md
      採訪稿_templete.docx
      採訪稿說明.json

  scripts/
    generate_doc_outputs.py    # Markdown → docx + JSON
    convert_to_md.py           # 原始 docx / pdf / gdocs → Markdown（可選）
    upload_to_gdocs.py         # 將 docx/Markdown 上傳並轉為 Google Docs（可選）
````

---

## 6. 檔案與格式規格

### 6.1 Markdown 文稿（腳本 / 採訪稿）

* 皆採用 UTF-8 編碼。
* 上方可使用 YAML front-matter 作為 metadata，例如：

```yaml
---
type: "採訪稿"
version: "v1"
document_title: "建立臺灣應變自我品牌，鼎足世界一同守護未來"
subject_person: "何大成"
subject_role: "中華民國化學應變協會（CERA）理事長"
source: "09_化學署專刊_中華民國化學應變協會 何大成理事長-文稿_二版"
---
```

* 主體內容依 template 固定結構，例如：

  * `# 主標`
  * `# 眉標`
  * `# 受訪者經歷`
  * `# 摘要`
  * `# 段一 …`
  * `# 段二 …` 等。

### 6.2欄位說明 JSON

* `*_欄位說明.json` 用來描述從 Markdown 解析出的欄位，格式範例：

```json
{
  "type": "採訪稿",
  "source_markdown": "outputs/採訪稿/採訪稿.md",
  "generated_docx": "outputs/採訪稿/採訪稿_templete.docx",
  "fields": {
    "headline": "建立臺灣應變自我品牌，鼎足世界一同守護未來",
    "subhead": "我不能祈求老天爺的幫助，把弟兄安全帶回是我的責任...",
    "subject_person": "何大成",
    "sections": [
      { "title": "取鏡世界 惠及臺灣" },
      { "title": "以人命為基準下 企業責任才是應變的保護傘" }
    ]
  }
}
```

* 初期欄位解析可用簡單 regex，後續視需求改為更強的 parser 或再交給 AI 強化欄位提取。

---

## 7. 流程設計

### 7.1 Template / reference 建立流程

1. 使用者提供範本 `.docx`（例如：化學署專刊版型）。
2. 人工確認版面與欄位：

   * 哪些內容是固定樣式（logo、頁眉、頁碼）
   * 哪些內容是變動欄位（標題、內文、作者）
3. 產生：

   * `reference/專刊版型_reference.docx`（供 pandoc 使用）
   * `templates/腳本_template.md` & `templates/採訪稿_template.md`
   * `docs/guidelines/腳本_格式說明.md` & `docs/guidelines/採訪稿_格式說明.md`

> 這一步高度依賴人類決策，AI 只用來輔助說明欄位，不做最後定案。

### 7.2 文稿產出流程（以採訪稿為例）

1. 使用者把原稿放入 `docs/sources/` 下（docx/PDF/GDocs → Markdown 後亦可）。

2. 開啟 CLI AI，指定專案根目錄。

3. 下達指令（或 prompt）要求：

   * 先讀 `AGENTS.md`
   * 再讀 `docs/guidelines/採訪稿_格式說明.md`
   * 再讀 `docs/sources/<原稿>.md`
   * 再讀 `templates/採訪稿_template.md`

4. AI 依模板輸出一份完整的 `採訪稿.md`：

   * 放在 `outputs/採訪稿/` 下（可由人 / script 寫入）。

5. Script 執行：

   ```bash
   python scripts/generate_doc_outputs.py --type 採訪稿 outputs/採訪稿/採訪稿.md
   ```

6. Script 輸出：

   * `採訪稿_templete.docx`
   * `採訪稿說明.json`
     -（可選）額外轉 PDF 或上傳 Google Docs。

### 7.3 人工檢查流程

* 檢查 Word：

  * 版面是否依 reference 正確套用。
  * 段落斷行是否合理。
* 檢查內容：

  * 專有名詞與數據是否正確。
  * AI 是否有誤讀原稿的情節。
* 必要時修改：

  * 直接改 Markdown 再重新轉出，或直接在 Word 上修改。

---

## 8. 非目標（Non-Goals）

* 不追求 AI 自動完成 100% 完美排版。
* 不解決所有 PDF OCR 相關問題：

  * 錯字 / 亂碼仍需人工校正。
* 不處理圖片、表格、複雜版面自動排版：

  * 圖片 / 表格插入目前仍視為人工步驟。

---

## 9. 未來擴充方向

1. CI / CD 整合：

   * Push 新 Markdown 時自動轉 `.docx` / PDF。
2. 更完整的 schema 定義：

   * 使用 JSON Schema 或 OpenAPI 方式定義欄位結構。
3. 多模板支援：

   * 同一專案中支援不同刊物 / 不同語系的版型。
4. 更智慧的欄位提取：

   * Script 與第二層 AI 結合，從 Free-form Markdown 自動萃取欄位。

---

```

---
