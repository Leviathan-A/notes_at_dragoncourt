Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (& git -C $PSScriptRoot rev-parse --show-toplevel 2>$null)
if (-not $repoRoot) {
    Write-Error "错误：无法定位 Git 仓库。"
}

Write-Host "[pull] repo: $repoRoot"
& git -C $repoRoot pull --rebase
Write-Host "[pull] 完成。"
