# Gemini Obsidian Bridge

A specialized tools repository designed to automate and enhance an Obsidian vault using the Gemini CLI and Python-based utilities. This repo acts as a "Bridge" between raw knowledge notes and advanced AI-driven management.

## 🚀 Quick Start

### Prerequisites
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [Gemini CLI](https://github.com/google/gemini-cli)
- [Obsidian](https://obsidian.md/) with CLI enabled (v1.12+)

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/gemini-obsidian.git
    cd gemini-obsidian
    ```
2.  **Initialize Environment**:
    ```bash
    uv sync
    ```
3.  **Configure Vault Path**:
    Create a `.env` file in the root directory:
    ```env
    OBSIDIAN_VAULT_PATH="D:\Path\To\Your\Vault"
    ```
4.  **Activate Shell Environment**:
    - **Windows (PowerShell)**: `.\startup.ps1`
    - **Linux/macOS (Fish)**: `source startup.fish`

## 🛠️ Core Features

- **Metadata Audits**: Scan your vault for missing frontmatter, tags, or incorrect date formats using `g-validate`.
- **MOC Management**: Automatically discover and list all Maps of Content (MOCs) with `g-mocs`.
- **Zettelkasten Linking**: Leverage Gemini to suggest semantic connections between atomic notes.
- **Cross-OS Compatibility**: Harmonized environment setup for both Windows and Linux environments.

## 📂 Project Structure

- `.gemini/`: Configuration and specialized AI skills.
- `scripts/`: Python logic powered by `uv` and `ObsidianClient`.
- `startup.*`: Shell-specific environment loaders and aliases.
- `PLAN.md`: Roadmap for future vault automation features.

## ⌨️ Available Aliases (via Startup Scripts)

| Alias | Description |
| :--- | :--- |
| `g-obsidian` | Interact with the Obsidian CLI wrapper |
| `g-mocs` | List all Maps of Content in the vault |
| `g-validate` | Run the frontmatter validation suite |

## 📜 License
MIT
