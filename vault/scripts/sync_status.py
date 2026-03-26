#!/usr/bin/env python3
"""Show Git sync status with friendly Chinese output."""

from __future__ import annotations

import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main() -> int:
    cwd = Path.cwd()

    code, inside, _ = run(["git", "rev-parse", "--is-inside-work-tree"], cwd)
    if code != 0 or inside != "true":
        print("当前目录不是 Git 仓库，请先进入仓库目录。")
        return 1

    code, root, _ = run(["git", "rev-parse", "--show-toplevel"], cwd)
    repo = Path(root) if code == 0 else cwd

    _, branch, _ = run(["git", "branch", "--show-current"], repo)
    _, remotes, _ = run(["git", "remote"], repo)
    _, status_short, _ = run(["git", "status", "--short"], repo)
    _, status_branch, _ = run(["git", "status", "-sb"], repo)

    print(f"仓库路径：{repo}")
    print(f"当前分支：{branch or '(detached)'}")

    if remotes:
        print("远程仓库：已配置")
        for item in remotes.splitlines():
            print(f"- {item}")
    else:
        print("远程仓库：未配置（请手工添加 remote）")

    if status_branch:
        first_line = status_branch.splitlines()[0]
        print(f"分支同步信息：{first_line}")

    if status_short:
        print("工作区状态：有未提交改动")
        print(status_short)
    else:
        print("工作区状态：干净")

    print("建议流程：先 pull，再编辑，再 push")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
