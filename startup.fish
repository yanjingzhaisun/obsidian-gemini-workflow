# startup.fish - Launcher for Gemini Obsidian Bridge

# 1. Load .env file
if test -f .env
    for line in (grep -v '^#' .env | grep -v '^\s*$')
        set -l var (string split -m 1 "=" $line)
        if set -q var[2]
            set -gx $var[1] (string trim -c '"' -c "'" $var[2])
        end
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

# 3. Gemini Command
function gemini-obsidian
    # This function launches Gemini with the current project as context
    # and makes sure the vault path is available.
    echo "Launching Gemini Obsidian Bridge..."
    gemini $argv
end

# 4. Abbreviations/Aliases
abbr -a g-obsidian "uv run python scripts/obsidian_client.py"
abbr -a g-mocs "uv run python scripts/list_mocs.py"
abbr -a g-validate "uv run python scripts/validate_frontmatter.py"
abbr -a g-chat "gemini-obsidian"

echo "Gemini Obsidian Bridge environment loaded."
echo "Use 'g-chat' to start a session or 'g-obsidian' to run the client."

# 5. Auto-start Gemini if not sourced
if not status is-interactive
    gemini
end
