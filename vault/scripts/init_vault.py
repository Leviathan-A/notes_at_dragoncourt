#!/usr/bin/env python3
"""Initialize and verify required vault directories (idempotent)."""

from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_DIRS = [
    "00-Inbox",
    "01-Daily",
    "02-Projects",
    "03-Knowledge",
    "04-Areas",
    "05-Resources",
    "90-Indexes",
    "Templates",
    "Assets",
    "scripts",
    "docs",
]


def ensure_vault_structure(vault_root: Path) -> tuple[list[Path], list[Path]]:
    created: list[Path] = []
    existing: list[Path] = []

    for rel in REQUIRED_DIRS:
        target = vault_root / rel
        if target.exists():
            existing.append(target)
            continue
        target.mkdir(parents=True, exist_ok=True)
        created.append(target)

    return created, existing


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_vault = script_dir.parent

    parser = argparse.ArgumentParser(description="检查并补齐 vault 目录结构")
    parser.add_argument(
        "--vault",
        type=Path,
        default=default_vault,
        help=f"vault 根目录，默认：{default_vault}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    vault_root = args.vault.resolve()
    vault_root.mkdir(parents=True, exist_ok=True)

    created, existing = ensure_vault_structure(vault_root)

    print(f"Vault 路径: {vault_root}")
    print(f"已存在目录: {len(existing)}")
    print(f"新建目录: {len(created)}")

    if created:
        print("本次补齐目录:")
        for item in created:
            print(f"- {item.relative_to(vault_root)}")
    else:
        print("目录结构完整，无需补齐。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
