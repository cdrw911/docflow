# Input 目錄說明

本目錄用於存放待處理的原始文稿。

## 使用方式

### 1. 放入原始文稿

將您的 Word 文件（.docx）放入此目錄：

```bash
cp /path/to/your/file.docx input/
```

**注意**：由於 .gitignore 設定，大型 .docx 檔案不會提交到 Git。

### 2. 轉換為 Markdown

```bash
python3 scripts/convert_docx_to_md.py input/您的文件.docx -o docs/sources/您的文件.md
```

### 3. 使用 AI 整理（參考 AGENTS.md）

### 4. 轉換為標準 Word 文件

```bash
python3 scripts/generate_doc_outputs.py --type 採訪稿 outputs/採訪稿/採訪稿.md
```

## 測試檔案

原計劃的測試檔案：
- `09_化學署專刊_中華民國化學應變協會 何大成理事長-文稿_二版.docx`

如果您沒有此檔案，可以使用已提供的範例：
- `docs/sources/範例_採訪稿.md` - 完整的範例採訪稿

## 範例工作流程

```bash
# 使用範例文稿測試
python3 scripts/generate_doc_outputs.py --type 採訪稿 docs/sources/範例_採訪稿.md

# 查看輸出
ls -lh outputs/採訪稿/
```
