<#
.SYNOPSIS
    Installs the Antigravity Review Loop Plugin into Global or Workspace configuration.

.DESCRIPTION
    Installs the review-loop plugin, rules, and skills into Google Antigravity.
    Supports Global installation (~/.gemini/config/plugins/review-loop) and
    Workspace installation (.agents/plugins/review-loop).

.PARAMETER Scope
    Installation target scope: 'Global' (default) or 'Workspace'.

.PARAMETER DryRun
    Dry-run mode. Shows what would happen without making modifications.

.EXAMPLE
    .\install.ps1
    .\install.ps1 -Scope Workspace
    .\install.ps1 -DryRun
#>

param(
    [ValidateSet("Global", "Workspace")]
    [string]$Scope = "Global",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Google Antigravity Review Loop Plugin Installer       " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Determine destination directory
if ($Scope -eq "Global") {
    $UserHome = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)
    $TargetDir = Join-Path $UserHome ".gemini\config\plugins\review-loop"
    $ConfigJsonPath = Join-Path $UserHome ".gemini\config\config.json"
} else {
    $TargetDir = Join-Path (Get-Location) ".agents\plugins\review-loop"
    $ConfigJsonPath = $null
}

Write-Host "[*] Scope: $Scope" -ForegroundColor Green
Write-Host "[*] Source: $ScriptDir" -ForegroundColor Gray
Write-Host "[*] Destination: $TargetDir" -ForegroundColor Gray

if ($DryRun) {
    Write-Host "[!] DryRun Mode active: No files will be modified." -ForegroundColor Yellow
    return
}

# Ensure parent directory exists
$TargetParent = Split-Path -Parent $TargetDir
if (-not (Test-Path $TargetParent)) {
    New-Item -ItemType Directory -Path $TargetParent -Force | Out-Null
}

# Copy plugin files
Write-Host "[*] Installing plugin files..." -ForegroundColor Gray
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

$ItemsToCopy = @("plugin.json", "rules", "skills")
foreach ($item in $ItemsToCopy) {
    $src = Join-Path $ScriptDir $item
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $TargetDir -Recurse -Force
        Write-Host "    [OK] Installed $item" -ForegroundColor DarkGreen
    }
}

# Enable in config.json if Global scope
if ($ConfigJsonPath -and (Test-Path $ConfigJsonPath)) {
    try {
        $jsonContent = Get-Content $ConfigJsonPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if (-not $jsonContent.plugins) {
            $jsonContent | Add-Member -NotePropertyName "plugins" -NotePropertyValue (New-Object PSObject)
        }
        $existingProp = $jsonContent.plugins.PSObject.Properties["review-loop"]
        if (-not $existingProp) {
            $pluginEntry = [PSCustomObject]@{ enabled = $true }
            $jsonContent.plugins | Add-Member -NotePropertyName "review-loop" -NotePropertyValue $pluginEntry
            $jsonContent | ConvertTo-Json -Depth 10 | Set-Content $ConfigJsonPath -Encoding UTF8
            Write-Host "    [OK] Enabled 'review-loop' in $ConfigJsonPath" -ForegroundColor DarkGreen
        } else {
            Write-Host "    [OK] 'review-loop' already enabled in config.json" -ForegroundColor DarkGreen
        }
    } catch {
        Write-Host "    [!] Note: Could not auto-update config.json: $_" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!                                " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "You can now use /review-loop across your Antigravity sessions:" -ForegroundColor White
Write-Host "  start /reviewLoop PM 8-4 DR 90%-3" -ForegroundColor Yellow
Write-Host "  /review-loop" -ForegroundColor Yellow
Write-Host ""
