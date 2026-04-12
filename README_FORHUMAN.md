# README_FORHUMAN.md - The Bridge Guide

## What is this?
Welcome to the **Gemini Obsidian Bridge**. Think of this as the "control center" for your knowledge. Instead of manually editing hundreds of notes, this bridge allows you to automate tasks like organizing metadata, finding links, and summarizing your daily thoughts.

## Why use a "Bridge"?
This repository is **separate** from your Obsidian vault.
1.  **Safety**: Your notes are stored in their own vault repo, and these tools live here. You don't have to clutter your knowledge base with scripts.
2.  **Portability**: If you move your vault, you just update one line in a file (`.env`), and all your automation "follows" you.
3.  **Reproducibility**: We use `uv` and Python to make sure these tools work exactly the same on any computer you own.

## How to use it
1.  **Connect to your Vault**: Copy `.env.example` to `.env` and fill in the absolute path to your Obsidian vault.
2.  **One-Click Start**:
    - **On Linux (Fish)**: Just run `./startup.fish`.
    - **On Windows (PowerShell)**: Just run `.\startup.ps1`.
    That's it! Gemini CLI will start, and it will already have access to your vault notes.

## Smooth Cross-Computer Setup
When you switch computers:
1.  **Install `uv`**: The only global requirement.
2.  **Run `uv sync`**: Installs all tools.
3.  **Update `.env`**: Point it to the vault path on your new machine.
4.  **Run the script**: `./startup.fish` (or `.\startup.ps1`). No settings files need changing.

## Roadmap
- [x] **Phase 1-2**: Foundation & Core tools (MOCs, Metadata).
- [x] **Phase 3 (Ongoing)**: Smart Linking (letting the AI suggest connections).
- [ ] **Phase 4**: Smooth cross-computer setup.

## Pro-tip
You can ask me (Gemini CLI) to "work on the PLAN.md" anytime to see where we are or to add new features to your vault automation.
