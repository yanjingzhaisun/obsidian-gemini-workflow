---
name: zettel-linker
description: Analyzes atomic notes and suggests relevant links to other notes in the Obsidian vault to strengthen the Zettelkasten network.
---

# Zettel-Linker Guide

## Goal
The goal of this skill is to help the user connect new notes to existing knowledge in the vault. This follows the Zettelkasten principle of "making connections is as important as taking notes."

## Workflow
1. **Identify Target Note**: Select a note that needs linking (usually in `inbox/` or recently added to `zettlekasten/`).
2. **Scan Context**: Read the note's content and existing tags/metadata.
3. **Search for Connections**: Search the vault for semantically related notes, MOCs, or keywords.
4. **Propose Links**: Suggest links to be added to the note, explaining *why* they are relevant.

## Guidelines
- **Semantic Relevance**: Don't just link based on keyword matching; look for conceptual connections.
- **Link Types**: 
    - **Upward**: Link to a broader MOC.
    - **Sideways**: Link to related atomic notes at the same level of granularity.
    - **Downward**: Link to specific examples or supporting notes.
- **Explanation**: Always provide a brief reason for each suggested link.

## Tools
- `scripts/zettel_linker.py`: A script that uses Gemini to analyze a note and suggest links based on the current vault state.
