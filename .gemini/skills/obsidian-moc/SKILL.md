---
name: obsidian-moc
description: Manage and list Maps of Content (MOCs) in the Obsidian vault. MOCs are organizational hubs that collect links to related notes.
---

# Obsidian MOC (Map of Content) Guide

## What is a MOC?
A Map of Content (MOC) is a note that serves as a central hub for a specific topic, linking to various atomic notes or other MOCs. They are used to navigate the vault's structure without relying solely on folders.

## MOC Patterns
- **Filename**: Usually ends with ` MOC` (e.g., `Game Design Theory MOC.md`).
- **Location**: Often stored in the `Map-Of-Content/` folder.
- **Content**: Typically contains a list of links (`[[Note Name]]`) grouped by sub-topics.

## Listing MOCs
To list all MOCs in the vault, use the `scripts/list_mocs.py` tool.

### Example MOC Structure
```markdown
# Topic Name MOC

## Sub-topic A
- [[Note 1]]
- [[Note 2]]

## Sub-topic B
- [[Note 3]]
```
