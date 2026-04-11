# startup.ps1 - PowerShell startup script for Gemini Obsidian Bridge

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

# 2. Activate uv virtual environment
if (Test-Path ".venv\Scripts\Activate.ps1") {
    & .venv\Scripts\Activate.ps1
} else {
    Write-Warning "Virtual environment not found. Run 'uv venv' first."
}

# 3. Aliases
function g-obsidian { uv run python scripts/obsidian_client.py @args }
function g-mocs { uv run python scripts/list_mocs.py @args }
function g-validate { uv run python scripts/validate_frontmatter.py @args }

Write-Host "Gemini Obsidian Bridge environment loaded." -ForegroundColor Cyan
