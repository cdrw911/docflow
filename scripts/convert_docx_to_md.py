#!/usr/bin/env python3
"""
docx 轉 Markdown 工具

將 Word 文件（.docx）轉換為 Markdown 格式，以便後續處理。

使用方式：
    python scripts/convert_docx_to_md.py input.docx
    python scripts/convert_docx_to_md.py input.docx -o output.md
"""

import argparse
import pathlib
import subprocess
import sys


def docx_to_md(docx_path: pathlib.Path, md_path: pathlib.Path = None) -> pathlib.Path:
    """
    使用 pandoc 將 docx 轉為 Markdown

    Args:
        docx_path: 輸入的 docx 檔案路徑
        md_path: 輸出的 md 檔案路徑（若未指定，則與 docx 同名但副檔名為 .md）

    Returns:
        輸出的 md 檔案路徑
    """
    if md_path is None:
        md_path = docx_path.with_suffix(".md")

    cmd = [
        "pandoc",
        str(docx_path),
        "-f",
        "docx",
        "-t",
        "markdown",
        "-o",
        str(md_path),
        "--wrap=none",  # 不自動換行
        "--extract-media=.",  # 提取圖片到當前目錄
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ 已轉換為 Markdown：{md_path}")
        return md_path
    except subprocess.CalledProcessError as e:
        print(f"✗ pandoc 轉換失敗：{e.stderr}", file=sys.stderr)
        raise
    except FileNotFoundError:
        print("✗ 找不到 pandoc，請先安裝 pandoc", file=sys.stderr)
        print("  安裝方式：https://pandoc.org/installing.html", file=sys.stderr)
        raise


def main():
    parser = argparse.ArgumentParser(
        description="將 Word 文件轉換為 Markdown 格式",
        epilog="""
範例：
  python scripts/convert_docx_to_md.py input/原稿.docx
  python scripts/convert_docx_to_md.py input/原稿.docx -o docs/sources/原稿.md
        """,
    )
    parser.add_argument("docx_file", help="輸入的 Word 文件（.docx）")
    parser.add_argument("-o", "--output", help="輸出的 Markdown 檔案路徑（選填，預設與輸入檔同名）")
    args = parser.parse_args()

    # 檢查輸入檔案
    docx_path = pathlib.Path(args.docx_file).resolve()
    if not docx_path.exists():
        print(f"✗ 檔案不存在：{docx_path}", file=sys.stderr)
        sys.exit(1)

    if docx_path.suffix.lower() not in [".docx", ".doc"]:
        print(f"✗ 檔案格式錯誤：{docx_path.suffix}（需要 .docx 或 .doc）", file=sys.stderr)
        sys.exit(1)

    # 設定輸出路徑
    md_path = pathlib.Path(args.output).resolve() if args.output else None

    print(f"\n{'='*60}")
    print("docx → Markdown 轉換工具")
    print(f"{'='*60}")
    print(f"輸入：{docx_path}")
    if md_path:
        print(f"輸出：{md_path}")
    print(f"{'='*60}\n")

    # 執行轉換
    try:
        result_path = docx_to_md(docx_path, md_path)

        print(f"\n{'='*60}")
        print("✓ 轉換完成！")
        print(f"{'='*60}")
        print(f"輸出檔案：{result_path}")
        print(f"檔案大小：{result_path.stat().st_size:,} bytes")
        print()

    except Exception as e:
        print(f"\n✗ 轉換失敗：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
