# Python 生成 DOCX 方案對比

以下整理適用於 docflow 的常見 Python 產生 DOCX 作法，聚焦在「模板化填寫」「保持樣式」與「批次輸出」三個面向。

## python-docx
- **定位**：基礎 API，從零組裝 Word 檔。
- **優點**：
  - 功能齊全（段落、表格、圖片、頁眉腳等）。
  - 對於需要程式化排版、動態組裝版面時彈性最高。
- **缺點**：
  - 修改既有 `.docx` 範本較繁瑣，欄位填充需自己找定位點。
  - 若要批次套版，需自行設計 placeholder 與尋址邏輯，易出錯。
- **適合情境**：需要純程式控制版面，或尚未決定固定範本時。

## python-docxtpl（推薦）
- **定位**：在 Word 範本內放置 Jinja2 樣板變數，程式只負責提供資料。
- **優點**：
  - 直接在 Word 範本中使用 `{{ variable }}`、`{% for %}`、`{% if %}` 等語法，非工程背景也能調整版面。
  - 保留原始樣式與排版，適合 docflow 既有「reference.docx + 欄位化 Markdown」流程。
  - 支援批次渲染，速度可應付數百份輸出。
- **缺點**：
  - 需要先建立並維護範本檔（若版型多，需控管版本）。
  - 在複雜的段落/表格巢狀情境下，Jinja2 樣板調試成本較高。
- **適合情境**：大量填寫固定欄位（稿件欄位→Word），或要讓編輯直接調整 Word 範本。

## Aspose.Words for Python
- **定位**：商業授權的高階 DOCX/格式處理套件。
- **優點**：
  - 功能最完整，含 mail merge、PDF 轉換、保護、巨集等。
  - 對跨格式（DOCX ↔ PDF ↔ HTML）與複雜樣式支援成熟。
- **缺點**：
  - 需付費授權，部署需處理 license；套件體積較大。
  - 生態系封閉，程式碼可攜性較差。
- **適合情境**：企業內部已有授權、需要 mail merge 或進階保護/批註功能。

## Pandoc
- **定位**：格式轉換工具（Markdown ↔ DOCX 等）。
- **優點**：
  - 轉換格式多，適合把 Markdown 初稿轉成 DOCX 以供人工微調。
  - 可搭配 `reference.docx` 提供基本樣式參考。
- **缺點**：
  - 不以「資料填充」為設計目標，不支援模板邏輯。
  - 轉換後如需套用欄位或表格，仍需其他程式處理。
- **適合情境**：單次格式轉換或作為前置/後置步驟，而非批次套版。

## docflow 的建議策略
- **首選**：`python-docxtpl` 負責「把欄位化 Markdown/JSON → Word 範本」，符合本專案的欄位式輸出與 `reference.docx` 流程。
- **輔助**：`pandoc` 可在前期將使用者提供的 Markdown 轉成暫時的 DOCX 預覽；或在沒有範本時提供簡單輸出。
- **備選**：
  - 若需完全程式化組版或特殊控制，局部使用 `python-docx` 處理細節，最終仍可交給 `docxtpl`/`reference.docx` 套版。
  - 企業內若已有 Aspose 授權，可作為進階功能（如 mail merge、自動批註）但不作為社群預設依賴。

## 未來整合方向
- 封裝 `scripts/` 中的轉檔流程，提供：
  - `render_docx.py`：讀取欄位 JSON/Markdown，調用 `python-docxtpl` 套版。
  - `convert_md_to_docx.py`：利用 pandoc 轉換並套用 `reference.docx` 作為 fallback。
- 在 `templates/` 維護範本管理規則（命名、欄位說明、版本），方便編輯與 AI 協作。
