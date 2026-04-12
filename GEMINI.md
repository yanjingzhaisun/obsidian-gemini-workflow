# GEMINI.md - Obsidian Bridge (Tools Repo)

This repository is the central logic hub for managing the Obsidian Vault at `/home/zed/Documents/default_vault`.

## ?? Project Structure
- `.gemini/`: Standard Gemini CLI configuration.
  - `skills/`: Custom Gemini skills for vault management.
  - `settings.json`: Configuration pointing to the vault.
- `scripts/`: Python tools managed by `uv`.
- `PLAN.md`: The roadmap for vault automation.

## ??? Operational Principles
1. **Bridge Role:** This repo acts as a bridge. It does not contain knowledge notes; it contains the tools to *process* knowledge notes.
2. **Environment Sensitive:** Always use the path defined in `OBSIDIAN_VAULT_PATH` (currently `/home/zed/Documents/default_vault`) to refer to the vault's absolute path.
3. **Vault Access:** When performing tasks, search and modify files directly in the vault path.
4. **Reproducibility:** Use `uv` for all Python dependencies to ensure cross-platform consistency (Windows/Linux).

## ??? Core Workflows
1. **Metadata Audits:** Scan the vault for missing frontmatter or tags.
2. **Linking Suggestions:** Use Gemini to suggest connections between notes.
3. **Daily Management:** Automate the creation and archiving of daily notes.

## ?? Constraints
- Never modify the `.obsidian/` folder in the vault repo.
- Ensure all Python scripts are cross-platform compatible.
