# PLAN.md - Roadmap for Vault Automation

## Phase 1: Foundations
- [x] Create the bridge repository at `E:\Repo\gemini-obsidian`.
- [x] Migrate existing Gemini config.
- [x] Initialize Python environment with `uv`.
- [x] Establish environment variables for cross-machine vault mapping.

## Phase 2: Python Integrations
- [x] Implement obsidian-cli wrapper in Python.
- [x] Create a skill to list all MOCs (Maps of Content).
- [x] Script for automated frontmatter validation (YAML standards).

## Phase 3: Gemini Skills (Current)
- [x] **Skill: Zettel-Linker:** Suggests links based on atomic note analysis.
- [ ] **Skill: Daily-Reviewer:** Summarizes previous daily notes.
- [ ] **Skill: Inbox-Processor:** Helps classify notes in the `inbox/` folder.

## Phase 4: Cross-OS Optimization
- [x] Finalize Fish and PowerShell startup scripts for this bridge repo.
- [x] Implement smooth cross-computer setup (gitignore, .env.example, README).
- [ ] Test on Linux setup.

