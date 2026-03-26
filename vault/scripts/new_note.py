#!/usr/bin/env python3
"""Create project/knowledge/area note from templates."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

TYPE_TO_DIR = {
    "project": "02-Projects",
    "knowledge": "03-Knowledge",
    "area": "04-Areas",
}

TYPE_TO_TEMPLATE = {
    "project": "project.md",
    "knowledge": "knowledge.md",
    "area": "area.md",
}


def clean_file_name(title: str) -> str:
    cleaned = title.strip()
    cleaned = re.sub(r"[\\/:*?\"<>|]", "-", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip(" .")
    return cleaned


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_vault = script_dir.parent

    parser = argparse.ArgumentParser(description="创建项目/知识/领域笔记")
    parser.add_argument("--type", required=True, choices=sorted(TYPE_TO_DIR.keys()))
    parser.add_argument("--title", required=True)
    parser.add_argument("--dir", help="自定义目录（相对 vault 根目录）")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--vault", type=Path, default=default_vault)
    return parser.parse_args()


def load_template(vault_root: Path, note_type: str) -> str:
    template_path = vault_root / "Templates" / TYPE_TO_TEMPLATE[note_type]
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return "# {{title}}\n\n"


def main() -> int:
    args = parse_args()
    vault_root = args.vault.resolve()

    safe_title = clean_file_name(args.title)
    if not safe_title:
        print("错误：标题无效，无法生成文件名")
        return 1

    if args.dir:
        target_dir = Path(args.dir)
        if not target_dir.is_absolute():
            target_dir = vault_root / target_dir
    else:
        target_dir = vault_root / TYPE_TO_DIR[args.type]

    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{safe_title}.md"

    if target_path.exists():
        print(f"已存在，不覆盖：{target_path}")
        return 1

    content = load_template(vault_root, args.type)
    content = content.replace("{{title}}", args.title).replace("{{date}}", args.date)

    target_path.write_text(content, encoding="utf-8")
    print(f"已创建笔记：{target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
