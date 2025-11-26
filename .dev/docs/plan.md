整個流程拆成三層：

1. **專案目錄與模板規格**（人定義）
2. **CLI 型 AI 依照規格產出標準化的 `腳本.md` / `採訪稿.md`**
3. **Python + pandoc 做「Markdown → Word / Google Docs + 欄位說明 JSON」自動化**


測試檔案  放在 input/09_化學署專刊_中華民國化學應變協會  何大成理事長-文稿_二版.docx

---

## 一、專案目錄結構設計

建議專案根目錄類似這樣：

```bash
project_root/
  AGENTS.md                  # 定義 AI 角色（編輯 / 採訪 / 格式轉換）
  docs/
    guidelines/              # 格式規範
      腳本_格式說明.md
      採訪稿_格式說明.md
    sources/                 # 原始資料（訪綱、逐字稿、既有文稿）
      09_化學署專刊_中華民國化學應變協會_何大成理事長-文稿_二版.md
  templates/                 # 給 AI 看的模板（Markdown）
    腳本_template.md
    採訪稿_template.md
  outputs/
    腳本/
      # 每次任務可以再建立子資料夾
    採訪稿/
  scripts/
    generate_doc_outputs.py  # Python 腳本，產生 doc / json / md
```

工作流就會變成：

1. 人準備 / 更新 `guidelines` & `templates`
2. 用 CLI AI（Gemini / Claude Code…）在此專案目錄操作

   * 先讀 `AGENTS.md`
   * 再讀 `docs/guidelines/*.md` 和 `docs/sources/*.md`
   * 依 `templates/*.md` 輸出 `outputs/腳本/腳本.md` 或 `outputs/採訪稿/採訪稿.md`
3. 跑 `scripts/generate_doc_outputs.py` 自動產出：

   * `腳本_templete.doc`（實際用 docx）
   * `腳本欄位說明.json`
   * `腳本.md`（AI 產的原稿，直接沿用）
   * `採訪稿_templete.doc`
   * `採訪稿說明.json`
   * `採訪稿.md`

---

## 二、「腳本 / 採訪稿」的段落目錄怎麼訂？

### 1. 用你的實際文稿抽出欄位

你提供的文稿本身就已經有很好用的欄位結構：
（主標 / 眉標 / 經歷 / 摘要 / 段一～段四）

可以抽象成共用欄位：

* 主標（headline）
* 眉標／座右銘（subhead / motto）
* 受訪者基本資料 / 經歷（bio）
* 摘要（summary）
* 內文段落（sections）

  * 段落標題
  * 段落內容

### 2. 腳本（Script）建議目錄

**腳本.md 用來給內部排版 / 採訪規劃用**，比較偏「規劃稿」：

```markdown
---
type: "腳本"
version: "v1"
document_title: "化學署專刊：CERA 何大成理事長專題"
source: "09_化學署專刊_中華民國化學應變協會 何大成理事長-文稿_二版"
---

# 1. 基本資訊
- 任務代碼：
- 刊物名稱：
- 目標讀者：
- 文體風格：專訪報導 / 專題故事 / 社論...

# 2. 受訪者資訊
- 姓名：
- 職稱與單位：
- 關鍵身分標籤：例：毒化災應變專家、CERA 理事長
- 精簡經歷摘要（3–5 行）：

# 3. 主標與眉標
- 主標：
- 眉標（或座右銘）：
- 備選主標（選填）：
- 備選眉標（選填）：

# 4. 核心訊息（Key Messages）
- 核心訊息 1：
- 核心訊息 2：
- 核心訊息 3：

# 5. 內容結構大綱
## 段一：取鏡世界 惠及臺灣
- 段落目的：
- 要帶出的故事／案例：
- 必須出現的關鍵句：

## 段二：以人命為基準下 企業責任才是應變的保護傘
- 段落目的：
- 重點說明：

## 段三：人命為優先的情況之下，有能力就有責任不能不做
- 段落目的：
- 重點說明：

## 段四：應變種子已成長 需要共同來澆灌扶持
- 段落目的：
- 重點說明：

# 6. 版面與語氣指引
- 語氣設定：
- 行文節奏：
- 是否保留第一人稱／引言口語感：

# 7. 校對與禁忌
- 專有名詞列表：
- 必須確認的數據／日期：
- 禁用用語：
```

### 3. 採訪稿（成品文稿）建議目錄

**採訪稿.md 就是最後要給化學署專刊排版的成品文字：**

```markdown
---
type: "採訪稿"
version: "v1"
document_title: "建立臺灣應變自我品牌，鼎足世界一同守護未來"
subject_person: "何大成"
subject_role: "中華民國化學應變協會（CERA）理事長"
source_script: "../腳本/腳本.md"
---

# 主標
建立臺灣應變自我品牌，鼎足世界一同守護未來

# 眉標（座右銘）
我不能祈求老天爺的幫助，把弟兄安全帶回是我的責任  
能夠讓每個人安全，能夠避免人員跟環境的污染，那才是最完整的應變

# 受訪者經歷
- 現職：
  - 中華民國化學應變協會（CERA）理事長
  - 財團法人工業技術研究院化災應變研究室 技術經理
  - 環境部環境事故應變諮詢中心 資深諮詢員
- 重要經歷：
  - （照原文整理成條列）

# 摘要
（用 3–5 行，濃縮整篇故事的精神）

# 段一　取鏡世界 惠及臺灣
（內文）

# 段二　以人命為基準下 企業責任才是應變的保護傘
（內文）

# 段三　人命為優先的情況之下，有能力就有責任不能不做
（內文）

# 段四　應變種子已成長 需要共同來澆灌扶持
（內文）

# 結語（可選）
（如果需要額外編輯部總結）
```

---

## 三、欄位說明 JSON 設計

### 1. 腳本欄位說明（`腳本欄位說明.json`）範例

```json
{
  "type": "腳本",
  "version": "v1",
  "description": "專刊或專訪文章的規劃腳本欄位說明",
  "fields": [
    {
      "id": "document_title",
      "label": "文件標題",
      "required": true,
      "description": "腳本檔本身的名稱或任務說明，方便追蹤版本。",
      "example": "化學署專刊：CERA 何大成理事長專題"
    },
    {
      "id": "headline",
      "label": "主標",
      "required": true,
      "description": "文章最醒目的標題，應清楚帶出主題與價值。",
      "example": "建立臺灣應變自我品牌，鼎足世界一同守護未來"
    },
    {
      "id": "subhead",
      "label": "眉標／座右銘",
      "required": false,
      "description": "補充主標的精神，或引用受訪者的關鍵一句話。",
      "example": "我不能祈求老天爺的幫助，把弟兄安全帶回是我的責任..."
    },
    {
      "id": "subject_person",
      "label": "受訪者姓名",
      "required": true,
      "description": "本篇報導的主角或主要受訪者姓名。",
      "example": "何大成"
    },
    {
      "id": "subject_roles",
      "label": "受訪者職稱與單位",
      "required": true,
      "description": "目前主要職位與單位，可有多筆。",
      "example": [
        "中華民國化學應變協會（CERA）理事長",
        "財團法人工業技術研究院化災應變研究室 技術經理"
      ]
    },
    {
      "id": "summary",
      "label": "摘要",
      "required": true,
      "description": "濃縮全文精神的短文，通常 100–200 字。",
      "example": "雖然臺灣應變體系起步較晚，但在政府與民間共同努力下..."
    },
    {
      "id": "sections",
      "label": "段落結構",
      "required": true,
      "description": "文章各段的標題與重點。",
      "example": [
        {
          "title": "取鏡世界 惠及臺灣",
          "goal": "說明早期出國取經的歷程與思維轉折",
          "key_points": [
            "臺灣早期毒化災領域落後",
            "從美國、德國學習但需因地制宜"
          ]
        }
      ]
    }
  ]
}
```

### 2. 採訪稿說明（`採訪稿說明.json`）結構可以類似，只是：

* `type` 改為 `"採訪稿"`
* `fields.sections` 中的元素，多一個 `content` 欄位（實際段落文字）

---

## 四、AGENTS.md 與 Prompt 設計

### 1. `AGENTS.md` 範例（給 CLI AI 讀）

```markdown
# Agent：專刊文稿編輯 AI

你的任務：
- 你是一位熟悉報導寫作與採訪編輯的文字編輯。
- 你要依照 `docs/guidelines/` 下的規範，以及 `templates/` 下的範本，產生一致格式的 Markdown 文稿。
- 所有輸出一律使用 UTF-8 編碼的 Markdown。

工作流程：
1. 先閱讀本檔（AGENTS.md）了解你的角色。
2. 再閱讀呼叫方指定的 guidelines 檔案，例如：
   - `docs/guidelines/腳本_格式說明.md`
   - `docs/guidelines/採訪稿_格式說明.md`
3. 再閱讀來源資料，例如：
   - `docs/sources/09_化學署專刊_中華民國化學應變協會_何大成理事長-文稿_二版.md`
4. 最後依照對應的 template：
   - `templates/腳本_template.md`
   - `templates/採訪稿_template.md`
   產出對應的 `outputs/` 檔案。

輸出規則：
- 僅輸出單一完整 Markdown 文件，不要解釋與多餘敘述。
- 嚴格遵守 template 的段落順序與標題層級。
- 若缺資料，請在欄位填入 `TODO：` 開頭說明需人工補充。
```

### 2. 產生「腳本」的 Prompt 範本

給 CLI（貼進 Prompt，或存成 `prompts/generate_script.txt`）：

```text
任務：請依專案資料產出一份「腳本.md」。

請在目前專案目錄下依序執行：

1. 閱讀 `AGENTS.md` 理解你的角色與輸出規則。
2. 閱讀 `docs/guidelines/腳本_格式說明.md`，了解腳本欄位定義。
3. 閱讀 `docs/sources/09_化學署專刊_中華民國化學應變協會_何大成理事長-文稿_二版.md`。
4. 閱讀 `templates/腳本_template.md`，視為你要填寫的框架。

請根據來源文稿內容，完成一份「腳本」：

- 產出一個 **完整的 Markdown 檔**，內容格式要完全符合 `templates/腳本_template.md` 的標題與欄位。
- 針對每一段（段一～段四），補上：
  - 段落目的
  - 要帶出的故事／案例
  - 必須出現的關鍵句（可直接引用來源文句）
- 若來源文中沒有的資訊，以 `TODO：` 標註，留給人工補寫。

最後輸出時：
- 檔名假設為 `腳本.md`，將內容輸出即可（由外部程式負責存檔）。
- 不要加上任何解釋文字。
```

### 3. 產生「採訪稿」的 Prompt 範本

```text
任務：請依專案資料產出一份「採訪稿.md」（成品文稿）。

請在目前專案目錄下依序執行：

1. 閱讀 `AGENTS.md` 理解你的角色。
2. 閱讀 `docs/guidelines/採訪稿_格式說明.md`。
3. 閱讀 `docs/sources/09_化學署專刊_中華民國化學應變協會_何大成理事長-文稿_二版.md`，
   理解原始內容與段落精神。
4. 閱讀 `templates/採訪稿_template.md`，將其視為需填寫的框架。

輸出要求：

- 以 `templates/採訪稿_template.md` 的段落結構輸出完整 Markdown：
  - 主標
  - 眉標
  - 受訪者經歷（整理成條列）
  - 摘要
  - 段一～段四（保持原段落主題，但允許你微調語句，使之更流暢）
  - 必要時可補一段簡短結語
- 語氣：專刊報導風格，保留適度口語感，但句子要完整通順。
- 對專有名詞（ERIC、CERA 等）需維持一致拼法。

最後輸出時：
- 僅輸出一份完整 Markdown 內容，不加解說。
```

> 對不同 CLI（Gemini CLI / Chat Codex CLI / Claude Code），你只要確保它「有權讀專案目錄」並把上述 Prompt 丟給它即可；各家 CLI 的參數名稱不同，但概念是一樣的。

---

## 五、Python + pandoc 自動產出 doc / json / md

### 1. 腳本說明

這支腳本的功能：

* 讀一個來源 `*.md`（已由 AI 產生好）
* 根據類型（腳本 / 採訪稿）決定輸出檔名
* 用 `pandoc` 轉成 Word（建議 `.docx`，你可以再改名成 `.doc`）
* 簡單用 regex 從 Markdown 抓出主標 / 眉標 / 段落標題，寫進欄位說明 JSON

> 副作用 / 缺點：
>
> * 依賴系統已安裝 `pandoc`
> * regex 解析非常脆弱，標題寫法改掉就抓不到（後面可以再慢慢強化）
> * 只做最基本欄位萃取，不會做進階自然語言理解（那部分仍交給 AI）

### 2. `scripts/generate_doc_outputs.py` 範例程式碼

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依據 AI 產生的 Markdown，輸出：
- 腳本_templete.docx / 採訪稿_templete.docx
- 腳本欄位說明.json / 採訪稿說明.json
- 腳本.md / 採訪稿.md（複製來源或覆寫）
"""

import argparse
import json
import pathlib
import re
import subprocess
from typing import Dict, Any, List


def md_to_docx(md_path: pathlib.Path, docx_path: pathlib.Path) -> None:
    """使用 pandoc 將 Markdown 轉為 Word"""
    cmd = ["pandoc", str(md_path), "-o", str(docx_path)]
    subprocess.run(cmd, check=True)


def extract_fields_from_md(md_text: str) -> Dict[str, Any]:
    """
    非常簡單的欄位萃取：
    - 主標：行內包含「主標」
    - 眉標：行內包含「眉標」或「座右銘」
    - 章節：Markdown 二階標題 (##)
    之後可以再依實際情況強化。
    """
    fields: Dict[str, Any] = {}

    # 主標
    m_headline = re.search(r"[主主]\s*標[:：]\s*(.+)", md_text)
    if m_headline:
        fields["headline"] = m_headline.group(1).strip()

    # 眉標或座右銘
    m_subhead = re.search(r"(眉標|座右銘)[:：]\s*(.+)", md_text)
    if m_subhead:
        fields["subhead"] = m_subhead.group(2).strip()

    # 受訪者姓名（簡單從 frontmatter 抓 subject_person）
    m_subject = re.search(r"subject_person:\s*\"?(.+?)\"?\s*$", md_text, re.MULTILINE)
    if m_subject:
        fields["subject_person"] = m_subject.group(1).strip()

    # 段落標題（## 開頭）
    sections: List[Dict[str, Any]] = []
    for m in re.finditer(r"^##\s+(.+)$", md_text, flags=re.MULTILINE):
        title = m.group(1).strip()
        sections.append({"title": title})
    if sections:
        fields["sections"] = sections

    return fields


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        choices=["腳本", "採訪稿"],
        required=True,
        help="指定輸出類型（腳本 / 採訪稿）"
    )
    parser.add_argument(
        "src_md",
        help="來源 Markdown 檔路徑（由 AI 產出的腳本.md 或 採訪稿.md）"
    )
    parser.add_argument(
        "--out-dir",
        default="outputs",
        help="輸出根目錄，預設為 ./outputs"
    )
    args = parser.parse_args()

    src_path = pathlib.Path(args.src_md).resolve()
    if not src_path.exists():
        raise FileNotFoundError(f"來源檔不存在：{src_path}")

    out_root = pathlib.Path(args.out_dir).resolve()
    type_dir = out_root / args.type  # ./outputs/腳本 或 ./outputs/採訪稿
    type_dir.mkdir(parents=True, exist_ok=True)

    # 決定輸出檔名
    if args.type == "腳本":
        md_out = type_dir / "腳本.md"
        doc_out = type_dir / "腳本_templete.docx"  # 產出 docx，比 doc 現代
        json_out = type_dir / "腳本欄位說明.json"
    else:
        md_out = type_dir / "採訪稿.md"
        doc_out = type_dir / "採訪稿_templete.docx"
        json_out = type_dir / "採訪稿說明.json"

    # 讀來源 Markdown
    md_text = src_path.read_text(encoding="utf-8")

    # 直接把來源 md 複製到標準檔名
    md_out.write_text(md_text, encoding="utf-8")

    # 呼叫 pandoc 產出 Word
    md_to_docx(md_out, doc_out)

    # 簡單解析欄位，產出 JSON
    fields = extract_fields_from_md(md_text)
    payload = {
        "type": args.type,
        "source_markdown": str(src_path),
        "generated_markdown": str(md_out),
        "generated_docx": str(doc_out),
        "fields": fields
    }
    json_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"[OK] Markdown：{md_out}")
    print(f"[OK] Word：{doc_out}")
    print(f"[OK] 欄位說明 JSON：{json_out}")


if __name__ == "__main__":
    main()
```

使用方式（例）：

```bash
# 1. 先用 CLI AI 產出 ./outputs/腳本/腳本_raw.md
#   （或任何你指定的地方）

# 2. 轉成標準檔名與 docx + json
python scripts/generate_doc_outputs.py --type 腳本 outputs/腳本/腳本_raw.md

python scripts/generate_doc_outputs.py --type 採訪稿 outputs/採訪稿/採訪稿_raw.md
```

> 如果你真的一定要 `.doc` 而不是 `.docx`：
>
> * pandoc 會產 `.docx`，你可以：
>
>   * 手動改副檔名（多數版本 Word 還是會開得起來，但不推薦），或
>   * 在後續流程再用 LibreOffice / Word COM 轉舊 `.doc`（多一層轉檔，風險是格式跑掉）。

---

## 六、Google Docs 的部分（high-level）

* **簡單作法**：維持現在流程，只產出 `.docx`，
  然後人工或另外一支程式用 Google Drive API 上傳，勾「轉成 Google 文件格式」即可。
* **自動化缺點**：

  * 需要 OAuth / service account，部署與權限管理比較麻煩。
  * 每個專案可能要不同的目錄 / 權限設定。

建議先把：

1. CLI AI → 標準 Markdown
2. Python + pandoc → Word / JSON

這兩層打穩，再來考慮 Drive / Docs API。

---

## 七、總結 + 可能坑

**優點：**

* 用 AGENTS + guidelines + templates 把「寫作規則」固化，AI 可替換（Claude / Gemini 都能用）。
* Markdown 是統一中介格式，易 diff、易版控。
* `腳本 / 採訪稿` 有清楚的欄位與目錄，後續別的專刊也能複用。

**缺點 / Side effect：**

* `generate_doc_outputs.py` 目前欄位解析很陽春，標題命名稍微改就抓不到，需要你之後依實際 Markdown 結構加強。
* pandoc 轉 Word 雖然穩定，但版面細節（字型、段落樣式）若有嚴格 DTP 要求，可能還是得在 Word 模板（reference docx）上再微調。
