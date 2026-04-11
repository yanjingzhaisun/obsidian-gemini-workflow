# README_FORHUMAN.md - The Bridge Guide

## What is this?
Welcome to the **Gemini Obsidian Bridge**. Think of this as the "control center" for your knowledge. Instead of manually editing hundreds of notes, this bridge allows you to automate tasks like organizing metadata, finding links, and summarizing your daily thoughts.

## Why use a "Bridge"?
This repository is **separate** from your Obsidian vault.
1.  **Safety**: Your notes are stored in their own vault repo, and these tools live here. You don't have to clutter your knowledge base with scripts.
2.  **Portability**: If you move your vault, you just update one line in a file (`.env`), and all your automation "follows" you.
3.  **Reproducibility**: We use `uv` and Python to make sure these tools work exactly the same on any computer you own.

## How to use it
1.  **Connect to your Vault**: Open the `.env` file and make sure it points to your Obsidian folder.
2.  **Turn on the Bridge**:
    *   **On Windows**: Open PowerShell in this folder and type `.\startup.ps1`.
    *   **On Linux**: Open Fish and type `source startup.fish`.
3.  **Run a command**:
    *   `g-validate`: "Did I forget to add tags to that new note?" This will tell you.
    *   `g-mocs`: "What are my main topics again?" This lists your Maps of Content.
    *   `g-obsidian`: "Open this note for me." Direct control from your terminal.

## Smooth Cross-Computer Setup
When you clone this bridge repository to a new machine:
1.  **Install `uv`**: The only system-wide requirement.
2.  **Run `uv sync`**: This sets up the Python environment exactly like the original.
3.  **Setup `.env`**: Copy `.env.example` to `.env` and fill in the local path to your vault.
4.  **Source the Startup Script**: Use `startup.ps1` or `startup.fish`. Your aliases and environment will be ready instantly.

## Roadmap
- [x] **Phase 1-2**: Foundation & Core tools (MOCs, Metadata).
- [x] **Phase 3 (Ongoing)**: Smart Linking (letting the AI suggest connections).
- [ ] **Phase 4**: Smooth cross-computer setup.

## Pro-tip
You can ask me (Gemini CLI) to "work on the PLAN.md" anytime to see where we are or to add new features to your vault automation.
