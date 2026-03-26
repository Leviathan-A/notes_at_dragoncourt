#!/usr/bin/env python3
"""Create daily note from template with optional tags and links."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_items(raw_values: list[str] | None) -> list[str]:
    if not raw_values:
        return []
    result: list[str] = []
    for raw in raw_values:
        for item in raw.split(","):
            cleaned = item.strip()
            if cleaned:
                result.append(cleaned)
    return result


def normalize_tag(tag: str) -> str:
    return tag if tag.startswith("#") else f"#{tag}"


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_vault = script_dir.parent

    parser = argparse.ArgumentParser(description="创建日报")
    parser.add_argument("--date", help="日期，格式 YYYY-MM-DD，默认今天")
    parser.add_argument("--tag", action="append", help="可重复或逗号分隔")
    parser.add_argument("--project-link", action="append", help="可重复或逗号分隔")
    parser.add_argument("--knowledge-link", action="append", help="可重复或逗号分隔")
    parser.add_argument("--vault", type=Path, default=default_vault, help="vault 根目录")
    return parser.parse_args()


def load_template(template_path: Path) -> str:
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return (
        "# {{date}} Daily Note\n\n"
        "## 今日总结\n- \n\n"
        "## 工作内容\n- [ ] \n\n"
        "## 问题/阻塞\n- \n\n"
        "## 思考/洞察\n- \n\n"
        "## 明日计划\n- [ ] \n\n"
        "## 关联项目\n{{project_links}}\n\n"
        "## 关联知识\n{{knowledge_links}}\n\n"
        "## 标签\n{{tags_line}}\n"
    )


def render(content: str, date_str: str, tags: list[str], projects: list[str], knowledges: list[str]) -> str:
    tags_line = " ".join(tags) if tags else "#daily"

    project_links = "\n".join(f"- [[{item}]]" for item in projects) if projects else "- [[ ]]"
    knowledge_links = "\n".join(f"- [[{item}]]" for item in knowledges) if knowledges else "- [[ ]]"

    return (
        content.replace("{{date}}", date_str)
        .replace("{{generated_time}}", datetime.now().strftime("%Y-%m-%d %H:%M"))
        .replace("{{tags_line}}", tags_line)
        .replace("{{project_links}}", project_links)
        .replace("{{knowledge_links}}", knowledge_links)
    )


def main() -> int:
    args = parse_args()
    vault_root = args.vault.resolve()

    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("错误：--date 必须是 YYYY-MM-DD")
            return 1
    else:
        target_date = datetime.now()

    date_str = target_date.strftime("%Y-%m-%d")
    note_path = vault_root / "01-Daily" / f"{date_str}.md"

    if note_path.exists():
        print(f"已存在，不覆盖：{note_path}")
        return 1

    template = load_template(vault_root / "Templates" / "daily.md")

    tags = [normalize_tag(item) for item in parse_items(args.tag)]
    if "#daily" not in tags:
        tags.insert(0, "#daily")

    projects = parse_items(args.project_link)
    knowledges = parse_items(args.knowledge_link)

    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(render(template, date_str, tags, projects, knowledges), encoding="utf-8")

    print(f"已创建日报：{note_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
