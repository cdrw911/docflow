#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docflow - 文稿轉換工具

依據 AI 產生的 Markdown，輸出：
- 腳本_templete.docx / 採訪稿_templete.docx
- 腳本欄位說明.json / 採訪稿說明.json
- 腳本.md / 採訪稿.md（複製來源或覆寫）

使用方式：
    python scripts/generate_doc_outputs.py --type 腳本 input_file.md
    python scripts/generate_doc_outputs.py --type 採訪稿 input_file.md
"""

import argparse
import json
import pathlib
import re
import subprocess
import sys
from typing import Dict, Any, List


def md_to_docx(md_path: pathlib.Path, docx_path: pathlib.Path, reference_docx: pathlib.Path = None) -> None:
    """使用 pandoc 將 Markdown 轉為 Word"""
    cmd = ["pandoc", str(md_path), "-o", str(docx_path)]

    # 如果有 reference.docx，使用它來套用樣式
    if reference_docx and reference_docx.exists():
        cmd.extend(["--reference-doc", str(reference_docx)])

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ 已轉換為 Word：{docx_path}")
    except subprocess.CalledProcessError as e:
        print(f"✗ pandoc 轉換失敗：{e.stderr}", file=sys.stderr)
        raise
    except FileNotFoundError:
        print("✗ 找不到 pandoc，請先安裝 pandoc", file=sys.stderr)
        print("  安裝方式：https://pandoc.org/installing.html", file=sys.stderr)
        raise


def extract_yaml_frontmatter(md_text: str) -> Dict[str, Any]:
    """提取 YAML front matter"""
    frontmatter = {}

    # 匹配 YAML front matter (在文件開頭的 --- 包圍區塊)
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.search(pattern, md_text, re.DOTALL | re.MULTILINE)

    if match:
        yaml_content = match.group(1)
        # 簡單解析 YAML (只處理 key: value 格式)
        for line in yaml_content.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                frontmatter[key] = value

    return frontmatter


def extract_fields_from_md(md_text: str, doc_type: str) -> Dict[str, Any]:
    """
    從 Markdown 提取欄位

    提取邏輯：
    - 主標：一級標題包含「主標」
    - 眉標：一級標題包含「眉標」或「座右銘」
    - 段落：一級標題包含「段一」「段二」等
    - 受訪者經歷：一級標題包含「經歷」
    - 摘要：一級標題包含「摘要」
    """
    fields: Dict[str, Any] = {}

    # 提取 front matter
    frontmatter = extract_yaml_frontmatter(md_text)
    if frontmatter:
        fields["frontmatter"] = frontmatter

    # 主標
    m_headline = re.search(r'^#\s+主標\s*\n+(.+?)(?=\n#|\Z)', md_text, re.MULTILINE | re.DOTALL)
    if m_headline:
        fields["headline"] = m_headline.group(1).strip()

    # 眉標或座右銘
    m_subhead = re.search(r'^#\s+(眉標|座右銘|眉標\(座右銘\)|眉標（座右銘）)\s*\n+(.+?)(?=\n#|\Z)',
                          md_text, re.MULTILINE | re.DOTALL)
    if m_subhead:
        fields["subhead"] = m_subhead.group(2).strip()

    # 受訪者
    if "subject_person" in frontmatter:
        fields["subject_person"] = frontmatter["subject_person"]

    # 受訪者經歷
    m_bio = re.search(r'^#\s+受訪者經歷\s*\n+(.+?)(?=\n#|\Z)', md_text, re.MULTILINE | re.DOTALL)
    if m_bio:
        fields["bio"] = m_bio.group(1).strip()

    # 摘要
    m_summary = re.search(r'^#\s+摘要\s*\n+(.+?)(?=\n#|\Z)', md_text, re.MULTILINE | re.DOTALL)
    if m_summary:
        fields["summary"] = m_summary.group(1).strip()

    # 段落標題（段一、段二、段三、段四等）
    sections: List[Dict[str, Any]] = []
    section_pattern = r'^#\s+(段[一二三四五六七八九十]+)[\s　]+(.+?)$'

    for m in re.finditer(section_pattern, md_text, flags=re.MULTILINE):
        section_num = m.group(1)  # 段一、段二等
        section_title = m.group(2).strip()  # 段落標題

        # 提取該段落的內容（從這個標題到下一個一級標題之前）
        section_start = m.end()
        next_header = re.search(r'\n#\s+', md_text[section_start:])

        if next_header:
            section_end = section_start + next_header.start()
        else:
            section_end = len(md_text)

        section_content = md_text[section_start:section_end].strip()

        sections.append({
            "number": section_num,
            "title": section_title,
            "content": section_content[:200] + "..." if len(section_content) > 200 else section_content
        })

    if sections:
        fields["sections"] = sections

    # 針對腳本類型，額外提取核心訊息
    if doc_type == "腳本":
        core_messages = []
        core_msg_pattern = r'[-•]\s*核心訊息\s*[1234][:：]\s*(.+)'
        for m in re.finditer(core_msg_pattern, md_text, flags=re.MULTILINE):
            core_messages.append(m.group(1).strip())
        if core_messages:
            fields["core_messages"] = core_messages

    return fields


def main():
    parser = argparse.ArgumentParser(
        description="將 Markdown 轉換為 Word 文件並產生欄位說明 JSON",
        epilog="""
範例：
  python scripts/generate_doc_outputs.py --type 腳本 outputs/腳本/腳本.md
  python scripts/generate_doc_outputs.py --type 採訪稿 outputs/採訪稿/採訪稿.md --reference reference/專刊版型_reference.docx
        """
    )
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
    parser.add_argument(
        "--reference",
        help="reference.docx 路徑（選填），用於套用 Word 樣式"
    )
    args = parser.parse_args()

    # 檢查來源檔案
    src_path = pathlib.Path(args.src_md).resolve()
    if not src_path.exists():
        print(f"✗ 來源檔不存在：{src_path}", file=sys.stderr)
        sys.exit(1)

    # 設定輸出目錄
    out_root = pathlib.Path(args.out_dir).resolve()
    type_dir = out_root / args.type  # ./outputs/腳本 或 ./outputs/採訪稿
    type_dir.mkdir(parents=True, exist_ok=True)

    # 決定輸出檔名
    if args.type == "腳本":
        md_out = type_dir / "腳本.md"
        doc_out = type_dir / "腳本_templete.docx"
        json_out = type_dir / "腳本欄位說明.json"
    else:
        md_out = type_dir / "採訪稿.md"
        doc_out = type_dir / "採訪稿_templete.docx"
        json_out = type_dir / "採訪稿說明.json"

    # 處理 reference.docx
    reference_docx = None
    if args.reference:
        reference_docx = pathlib.Path(args.reference).resolve()
        if not reference_docx.exists():
            print(f"⚠ 警告：指定的 reference.docx 不存在：{reference_docx}", file=sys.stderr)
            reference_docx = None

    print(f"\n{'='*60}")
    print(f"docflow - 文稿轉換工具")
    print(f"{'='*60}")
    print(f"類型：{args.type}")
    print(f"來源：{src_path}")
    print(f"輸出目錄：{type_dir}")
    if reference_docx:
        print(f"參考樣式：{reference_docx}")
    print(f"{'='*60}\n")

    # 讀來源 Markdown
    md_text = src_path.read_text(encoding="utf-8")

    # 1. 複製 Markdown 到標準檔名
    md_out.write_text(md_text, encoding="utf-8")
    print(f"✓ Markdown：{md_out}")

    # 2. 呼叫 pandoc 產出 Word
    try:
        md_to_docx(md_out, doc_out, reference_docx)
    except Exception as e:
        print(f"✗ Word 轉換失敗，但會繼續產生 JSON", file=sys.stderr)

    # 3. 簡單解析欄位，產出 JSON
    fields = extract_fields_from_md(md_text, args.type)
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
    print(f"✓ 欄位說明 JSON：{json_out}")

    print(f"\n{'='*60}")
    print(f"✓ 轉換完成！")
    print(f"{'='*60}\n")

    # 顯示提取的欄位摘要
    print("📋 提取的欄位摘要：")
    if "headline" in fields:
        print(f"  主標：{fields['headline'][:50]}...")
    if "subhead" in fields:
        print(f"  眉標：{fields['subhead'][:50]}...")
    if "subject_person" in fields:
        print(f"  受訪者：{fields['subject_person']}")
    if "sections" in fields:
        print(f"  段落數：{len(fields['sections'])}")
        for sec in fields['sections']:
            print(f"    - {sec['number']}　{sec['title']}")
    print()


if __name__ == "__main__":
    main()
