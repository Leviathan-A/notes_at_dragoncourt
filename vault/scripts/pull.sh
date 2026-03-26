#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || true)"

if [ -z "$REPO_ROOT" ]; then
  echo "错误：无法定位 Git 仓库。" >&2
  exit 1
fi

echo "[pull] repo: $REPO_ROOT"
git -C "$REPO_ROOT" pull --rebase

echo "[pull] 完成。"
