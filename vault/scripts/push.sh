#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || true)"

if [ -z "$REPO_ROOT" ]; then
  echo "错误：无法定位 Git 仓库。" >&2
  exit 1
fi

MESSAGE="${1:-notes update: $(date '+%Y-%m-%d %H:%M:%S')}"

echo "[push] repo: $REPO_ROOT"
git -C "$REPO_ROOT" add -A

if git -C "$REPO_ROOT" diff --cached --quiet; then
  echo "[push] 没有可提交改动。"
  exit 0
fi

git -C "$REPO_ROOT" commit -m "$MESSAGE"
git -C "$REPO_ROOT" push

echo "[push] 完成。"
