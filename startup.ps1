# startup.ps1 - Launcher for Gemini Obsidian Bridge

# 1. Load .env file
if (Test-Path ".env") {
    foreach ($line in Get-Content ".env") {
        if ($line -match "^([^#=]+)=(.*)$") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"').Trim("'")
            [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
} else {
    Write-Warning ".env file not found. Copy .env.example to .env and configure it."
}

$vaultPath = [System.Environment]::GetEnvironmentVariable("OBSIDIAN_VAULT_PATH")
if ($vaultPath) {
    $vaultName = Split-Path $vaultPath -Leaf
    
    # 2. Check if Obsidian is running
    $obsidianProcess = Get-Process -Name "Obsidian" -ErrorAction SilentlyContinue
    if (-not $obsidianProcess) {
        Write-Host "Obsidian is not running. Attempting to start it with vault: $vaultName..." -ForegroundColor Yellow
        Start-Process "obsidian://open?vault=$vaultName"
        Write-Host "Waiting for Obsidian to initialize (5s)..." -ForegroundColor Gray
        Start-Sleep -Seconds 5
    } else {
        Write-Host "Obsidian is already running." -ForegroundColor Green
    }
}

# 3. Activate uv virtual environment
if (Test-Path ".venv\Scripts\Activate.ps1") {
    & .venv\Scripts\Activate.ps1
} else {
    Write-Warning "Virtual environment not found. Run 'uv venv' first."
}

# 4. Gemini Command
function Start-GeminiObsidian {
    Write-Host "Launching Gemini Obsidian Bridge..." -ForegroundColor Cyan
    gemini $args
}

# 5. Updated Aliases (pointing to modularized skill scripts)
Set-Alias g-chat Start-GeminiObsidian
function g-obsidian { uv run python scripts/obsidian_client.py @args }
function g-mocs { uv run python .gemini/skills/obsidian-moc/scripts/list_mocs.py @args }
function g-audit { uv run python .gemini/skills/obsidian-properties-audit/scripts/audit_properties.py @args }
function g-tags { uv run python .gemini/skills/obsidian-tag-cleanup/scripts/analyze_tags.py @args }
function g-links { uv run python .gemini/skills/obsidian-link-generator/scripts/generate_links.py @args }

Write-Host "Gemini Obsidian Bridge environment loaded." -ForegroundColor Cyan
Write-Host "Use 'g-chat' to start a session or aliases like 'g-audit', 'g-tags', 'g-links'." -ForegroundColor Cyan

# 6. Auto-start Gemini
Start-GeminiObsidian
