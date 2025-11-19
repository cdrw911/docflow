# Scripts 目錄說明

本目錄包含 docflow 專案的各種轉換與處理腳本。

## 主要腳本

### 1. generate_doc_outputs.py

**用途**：將 AI 產生的 Markdown 文稿轉換為 Word 文件，並提取欄位資訊為 JSON。

**前置需求**：
- Python 3.6+
- pandoc（需額外安裝）

**安裝 pandoc**：
```bash
# Ubuntu/Debian
sudo apt-get install pandoc

# macOS
brew install pandoc

# Windows
# 從 https://pandoc.org/installing.html 下載安裝
```

**使用方式**：
```bash
# 轉換腳本
python scripts/generate_doc_outputs.py --type 腳本 outputs/腳本/腳本.md

# 轉換採訪稿
python scripts/generate_doc_outputs.py --type 採訪稿 outputs/採訪稿/採訪稿.md

# 使用 reference.docx 套用樣式
python scripts/generate_doc_outputs.py --type 採訪稿 \
    outputs/採訪稿/採訪稿.md \
    --reference reference/專刊版型_reference.docx
```

**輸出**：
- `{類型}.md`：標準化的 Markdown 文稿
- `{類型}_templete.docx`：Word 文件
- `{類型}欄位說明.json`：欄位資訊 JSON

### 2. convert_docx_to_md.py

**用途**：將 Word 文件（.docx）轉換為 Markdown 格式。

**使用方式**：
```bash
# 基本轉換（輸出與輸入同名，副檔名改為 .md）
python scripts/convert_docx_to_md.py input/原稿.docx

# 指定輸出路徑
python scripts/convert_docx_to_md.py input/原稿.docx -o docs/sources/原稿.md
```

**用途場景**：
- 將使用者提供的 docx 原稿轉為 Markdown，供 AI 讀取
- 整理既有的 Word 文稿

## 工作流程範例

### 完整流程：從 docx 到 Word 成品

```bash
# Step 1: 將原始 docx 轉為 Markdown
python scripts/convert_docx_to_md.py \
    input/09_化學署專刊_中華民國化學應變協會_何大成理事長-文稿_二版.docx \
    -o docs/sources/何大成理事長-原稿.md

# Step 2: 使用 AI（例如 Claude Code）閱讀並產生標準化文稿
# （這一步由 AI 執行，參考 AGENTS.md）
# AI 會產生 outputs/採訪稿/採訪稿.md

# Step 3: 轉換為 Word 文件
python scripts/generate_doc_outputs.py \
    --type 採訪稿 \
    outputs/採訪稿/採訪稿.md \
    --reference reference/專刊版型_reference.docx
```

## 常見問題

### Q: 為什麼需要安裝 pandoc？

A: pandoc 是一個通用的文件轉換工具，支援 Markdown、Word、PDF 等多種格式互轉。本專案使用它來處理：
- Markdown → Word (.docx)
- Word (.docx) → Markdown

### Q: 轉換後的 Word 格式跑掉了怎麼辦？

A: 有幾種解決方式：
1. 使用 `--reference` 參數指定 reference.docx 樣式檔
2. 在 reference.docx 中預先設定好段落樣式、字型等
3. 轉換後在 Word 中微調（這是正常的，自動化無法 100% 完美）

### Q: 可以轉換 PDF 嗎？

A: pandoc 對 PDF 的支援有限。建議：
- 如果是文字 PDF：先用其他工具（如 Adobe Acrobat、pdf2txt）轉為文字
- 如果是掃描 PDF：需要 OCR 工具（如 Tesseract）先辨識文字

### Q: 轉換時出現編碼錯誤怎麼辦？

A: 確保所有 Markdown 檔案使用 UTF-8 編碼。如果是從其他來源產生的檔案，可能需要先轉換編碼。

## 技術細節

### generate_doc_outputs.py 的欄位提取邏輯

腳本使用正則表達式提取以下欄位：

- **主標**：一級標題包含「主標」
- **眉標**：一級標題包含「眉標」或「座右銘」
- **段落**：一級標題符合「段一」「段二」等格式
- **受訪者經歷**：一級標題包含「經歷」
- **摘要**：一級標題包含「摘要」
- **Front matter**：YAML 格式的 metadata

### 自訂欄位提取

如果需要提取其他欄位，可以修改 `extract_fields_from_md()` 函數，新增對應的正則表達式。

## 未來擴充

計劃新增的腳本：

- `upload_to_gdocs.py`：上傳並轉換為 Google Docs
- `batch_convert.py`：批次轉換多個檔案
- `validate_md.py`：驗證 Markdown 格式是否符合規範

## 授權

本專案腳本採用 MIT 授權。
