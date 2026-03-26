Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

param(
    [string]$Message
)

$repoRoot = (& git -C $PSScriptRoot rev-parse --show-toplevel 2>$null)
if (-not $repoRoot) {
    Write-Error "错误：无法定位 Git 仓库。"
}

if (-not $Message) {
    $Message = "notes update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

Write-Host "[push] repo: $repoRoot"
& git -C $repoRoot add -A

& git -C $repoRoot diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "[push] 没有可提交改动。"
    exit 0
}

& git -C $repoRoot commit -m $Message
& git -C $repoRoot push
Write-Host "[push] 完成。"
