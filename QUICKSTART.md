# docflow 快速開始指南

本指南幫助你快速上手 docflow 文稿自動化產出系統。

## 前置需求

### 必要安裝

1. **Python 3.6+**
   ```bash
   python3 --version
   ```

2. **pandoc**（文件轉換工具）
   ```bash
   # Ubuntu/Debian
   sudo apt-get install pandoc

   # macOS
   brew install pandoc

   # Windows
   # 從 https://pandoc.org/installing.html 下載安裝
   ```

   驗證安裝：
   ```bash
   pandoc --version
   ```

### 選用工具

- **Git**（版本控制）
- **Claude Code / Gemini CLI**（AI 輔助寫作）

## 專案結構概覽

```
docflow/
├── AGENTS.md                    # AI 角色定義
├── README.md                    # 專案說明
├── QUICKSTART.md               # 本檔案
├── docs/
│   ├── guidelines/             # 格式規範（給 AI 看）
│   │   ├── 腳本_格式說明.md
│   │   └── 採訪稿_格式說明.md
│   └── sources/                # 原始文稿
│       └── 範例_採訪稿.md
├── templates/                  # AI 輸出範本
│   ├── 腳本_template.md
│   └── 採訪稿_template.md
├── reference/                  # Word 樣式參考檔
├── scripts/                    # 轉換腳本
│   ├── generate_doc_outputs.py
│   ├── convert_docx_to_md.py
│   └── README.md
├── outputs/                    # 輸出目錄
│   ├── 腳本/
│   └── 採訪稿/
└── input/                      # 輸入檔案
```

## 快速開始

### 方法一：測試範例（最快）

使用內建的範例文稿進行測試：

```bash
# 1. 轉換範例採訪稿為 Word
python3 scripts/generate_doc_outputs.py \
    --type 採訪稿 \
    docs/sources/範例_採訪稿.md

# 2. 查看輸出
ls -lh outputs/採訪稿/
```

你會得到：
- `採訪稿.md`：標準化 Markdown
- `採訪稿_templete.docx`：Word 文件
- `採訪稿說明.json`：欄位資訊

### 方法二：從 Word 原稿開始

如果你有 Word 原稿：

```bash
# 1. 將 Word 轉為 Markdown
python3 scripts/convert_docx_to_md.py \
    input/你的文稿.docx \
    -o docs/sources/你的文稿.md

# 2. 使用 AI 整理（見下方 AI 工作流程）

# 3. 轉換為 Word
python3 scripts/generate_doc_outputs.py \
    --type 採訪稿 \
    outputs/採訪稿/採訪稿.md
```

## AI 工作流程（使用 Claude Code）

### 步驟 1：準備原稿

將原稿放入 `docs/sources/` 目錄。

### 步驟 2：讓 AI 產出標準化文稿

在 Claude Code 中執行以下提示：

```
請依專案資料產出一份採訪稿.md（成品文稿）。

請在目前專案目錄下依序執行：

1. 閱讀 AGENTS.md 理解你的角色
2. 閱讀 docs/guidelines/採訪稿_格式說明.md
3. 閱讀 docs/sources/[你的原稿].md
4. 閱讀 templates/採訪稿_template.md

輸出要求：
- 以 templates/採訪稿_template.md 的段落結構輸出完整 Markdown
- 語氣：專刊報導風格，保留適度口語感
- 對專有名詞需維持一致拼法
- 將輸出儲存到 outputs/採訪稿/採訪稿.md
```

### 步驟 3：轉換為 Word

```bash
python3 scripts/generate_doc_outputs.py \
    --type 採訪稿 \
    outputs/採訪稿/採訪稿.md
```

## 使用 reference.docx 套用樣式

如果你有特定的 Word 樣式需求：

### 1. 準備 reference.docx

將你的 Word 範本放入 `reference/` 目錄：

```bash
cp 你的範本.docx reference/專刊版型_reference.docx
```

### 2. 使用 reference 轉換

```bash
python3 scripts/generate_doc_outputs.py \
    --type 採訪稿 \
    outputs/採訪稿/採訪稿.md \
    --reference reference/專刊版型_reference.docx
```

## 產出腳本（規劃文件）

腳本用於內部規劃，流程類似：

```bash
# 1. 讓 AI 產出腳本
# （在 Claude Code 中提示產出腳本，參考 AGENTS.md）

# 2. 轉換
python3 scripts/generate_doc_outputs.py \
    --type 腳本 \
    outputs/腳本/腳本.md
```

## 常見使用情境

### 情境 1：批次處理多篇文稿

```bash
# 假設你有多個原稿在 input/ 目錄

# 轉換所有 docx 為 md
for file in input/*.docx; do
    python3 scripts/convert_docx_to_md.py "$file" -o "docs/sources/$(basename "$file" .docx).md"
done

# 然後使用 AI 逐一處理
# （手動或撰寫自動化腳本）
```

### 情境 2：更新既有文稿

```bash
# 1. 編輯 Markdown
vim outputs/採訪稿/採訪稿.md

# 2. 重新轉換
python3 scripts/generate_doc_outputs.py \
    --type 採訪稿 \
    outputs/採訪稿/採訪稿.md
```

### 情境 3：檢視提取的欄位

```bash
# 查看 JSON 欄位說明
cat outputs/採訪稿/採訪稿說明.json | python3 -m json.tool
```

## 疑難排解

### 問題：pandoc 找不到

```bash
# 檢查是否安裝
which pandoc

# 如果沒有，請安裝（見前置需求）
```

### 問題：轉換後的 Word 格式不對

解決方案：
1. 使用 `--reference` 參數指定樣式檔
2. 調整 reference.docx 中的樣式定義
3. 在 Word 中手動微調（這是正常的）

### 問題：AI 產出的格式不符合預期

解決方案：
1. 檢查 `templates/` 中的範本是否清楚
2. 在 `docs/guidelines/` 中補充更詳細的說明
3. 在提示中提供更明確的範例

### 問題：中文字型顯示不正確

解決方案：
在 reference.docx 中設定中文字型（例如：微軟正黑體、標楷體）

## 進階技巧

### 自訂欄位提取

編輯 `scripts/generate_doc_outputs.py` 中的 `extract_fields_from_md()` 函數，新增你需要的欄位。

### 整合版本控制

```bash
# 初始化 Git（如果還沒有）
git init

# 提交變更
git add .
git commit -m "Add new article"
```

### 自動化流程

可以撰寫 shell script 或 Makefile 來自動化整個流程。

## 下一步

- 閱讀 `README.md` 了解專案完整說明
- 閱讀 `.dev/docs/spec.md` 了解設計規格
- 查看 `scripts/README.md` 了解腳本詳細說明
- 參考 `AGENTS.md` 了解如何與 AI 協作

## 需要協助？

- 檢查 `scripts/README.md` 的常見問題
- 閱讀 `docs/guidelines/` 中的格式說明
- 查看範例文稿：`docs/sources/範例_採訪稿.md`

---

**提示**：建議先用範例文稿測試整個流程，熟悉後再處理實際文稿。
