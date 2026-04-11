# startup.fish - Fish startup script for Gemini Obsidian Bridge

# 1. Load .env file
if test -f .env
    for line in (grep -v '^#' .env | grep -v '^\s*$')
        set -l var (string split -m 1 "=" $line)
        set -gx $var[1] (string trim -c '"' $var[2])
    end
else
    echo "Warning: .env file not found. Please copy .env.example to .env and configure it."
end

# 2. Activate uv virtual environment
if test -d .venv
    source .venv/bin/activate.fish
else
    echo "Virtual environment not found. Run 'uv venv' first."
end

# 3. Abbreviations/Aliases
abbr -a g-obsidian "uv run python scripts/obsidian_client.py"
abbr -a g-mocs "uv run python scripts/list_mocs.py"
abbr -a g-validate "uv run python scripts/validate_frontmatter.py"

echo "Gemini Obsidian Bridge environment loaded."
