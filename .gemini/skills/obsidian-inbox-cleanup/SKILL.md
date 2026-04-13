---
name: obsidian-inbox-cleanup
description: 整理 Obsidian 的 inbox 文件夹。识别已标记为 status/permanent 的笔记并将其移动至 zettlekasten 文件夹中，确保存放位置与状态属性一致。
---

# Obsidian Inbox Cleanup (整理 Inbox) 规范

## 核心原则
`inbox/` 文件夹仅用于存放临时笔记、待处理的速记或 `status/inbox` 状态的内容。
所有经过整理、达到永久笔记标准的 `status/permanent` 内容必须存放在 `zettlekasten/` 文件夹下。

## 核心流程
1. **识别状态**：分析 `inbox/` 下所有 `.md` 文件的 YAML Frontmatter。
2. **执行移动**：运行 `python .gemini/skills/obsidian-inbox-cleanup/scripts/move_permanent_notes.py`。
   - 脚本会自动检查带有 `status/permanent` 标签的文件。
   - 如果文件位于 `inbox/`，将其移动到 `zettlekasten/`。
3. **冲突处理**：如果 `zettlekasten/` 已存在同名文件，脚本会跳过并发出警告，需人工介入重命名。

## 注意事项
- **双链完整性**：Obsidian 会自动处理文件移动后的双向链接更新，但建议在移动后运行 `obsidian search` 验证关键链接。
- **模板检查**：确保新移动的文件符合 `obsidian-metadata` 规范。
