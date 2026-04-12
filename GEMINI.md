# GEMINI.md - Obsidian Bridge (Tools Repo)

This repository is the central logic hub for managing an external Obsidian Vault. Its primary purpose is to provide automation, metadata auditing, and AI-driven linking for notes stored in a separate location.

## 🛠️ Project Identity & Role
1. **Bridge Function**: This repo (the "Bridge") contains only management scripts and AI configurations. It **does not** contain the knowledge notes themselves.
2. **Vault Ownership**: The actual Obsidian Vault is a separate entity (likely another git repo) located at the path defined by the `${OBSIDIAN_VAULT_PATH}` environment variable.

## ⚙️ Operational Principles
1. **Source of Truth**: Always use `${OBSIDIAN_VAULT_PATH}` for vault access. This allows the bridge to remain portable across different computers (Linux/Windows).
2. **Official CLI Power**: **Obsidian has an official CLI (`obsidian <command>`)**. Note that **Obsidian must be open** for these commands to work, as they communicate with the running app.
3. **Direct Management**: You (Gemini) have direct read/write access to the vault because `${OBSIDIAN_VAULT_PATH}` is included in the CLI's workspace via `settings.json`.
4. **Tool-First Approach**: For custom automation, use scripts in `scripts/` (which wrap the `ObsidianClient` and the official CLI).
5. **Reproducibility**: Use `uv` for all Python dependencies to ensure consistent behavior across environments.

## 📂 Project Structure
- `.gemini/`: AI workspace configuration.
  - `settings.json`: Dynamically maps `${OBSIDIAN_VAULT_PATH}` as an included directory.
  - `skills/`: Specialized skills (Zettelkasten, MOCs, Metadata) to be activated for vault management.
- `scripts/`: Python logic for vault operations (see `ObsidianClient` in `obsidian_client.py`).
- `startup.fish` / `startup.ps1`: One-click environment loaders that export `${OBSIDIAN_VAULT_PATH}` and launch the Gemini session.

## 🎯 Core Workflows
1. **Metadata Audits**: Identify notes with missing or inconsistent frontmatter.
2. **Semantic Linking**: Suggest connections between atomic notes in the vault.
3. **MOC Orchestration**: Maintain "Maps of Content" as central hubs for related notes.

## ⚠️ Constraints
- **Preserve Configuration**: Never modify the `.obsidian/` internal folder within the vault.
- **Path Portability**: Avoid hardcoding absolute paths. Always resolve against the current environment's `${OBSIDIAN_VAULT_PATH}`.
