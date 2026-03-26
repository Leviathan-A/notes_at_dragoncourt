Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

param(
    [string]$Message
)

& "$PSScriptRoot/pull.ps1"
& "$PSScriptRoot/push.ps1" -Message $Message
Write-Host "[sync] 完成。"
