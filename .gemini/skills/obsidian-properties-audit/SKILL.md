---
name: obsidian-properties-audit
description: 自动审查并修复库中所有笔记的 YAML Properties。确保没有错误的换行，每个笔记都包含必需的 tags (并且格式为列表) 和 date，且拥有状态标签（status/inbox 或 status/permanent）。
---

# Obsidian Properties Audit (属性审查与修复) 规范

## 核心原则
- **格式一致性**：所有笔记的 YAML Frontmatter 必须格式正确，且与正文之间有正确的空行分隔。
- **标签完整性**：所有笔记必须包含 `tags` 列表。
- **状态追踪**：所有笔记必须具有状态标签（`status/inbox` 或 `status/permanent`）。如果未指定，根据笔记所在的文件夹自动分配默认状态（在 `zettlekasten` 文件夹中的笔记默认分配 `status/permanent`，其他默认为 `status/inbox`）。
- **时间戳**：所有笔记必须包含 `date` 属性（ISO 8601 格式）。如果缺失，将自动使用文件的创建/修改时间填充。

## 核心流程
1. **执行脚本**：运行 `python .gemini/skills/obsidian-properties-audit/scripts/audit_properties.py`。
2. **自动检测与修复**：
   - 检查 `---` 之后是否有错误的连字或缺失的换行。
   - 解析 YAML。如果因存在不合法字符（如双链 `[[...]]` 包裹了 date）导致解析失败，脚本会尝试修复。
   - 检查 `tags` 属性是否存在且为列表格式。
   - 检查是否包含 `status/` 开头的标签。如果没有，自动追加。
   - 检查是否包含 `date` 属性。如果没有，自动追加。
3. **安全保存**：如果笔记被修改，它会被使用标准的 YAML 格式重新写入，保持正文不受影响。

## 注意事项
- 此脚本排除了 `.obsidian`、`.git` 和 `templates` 文件夹。
- 建议定期执行，特别是在大量导入笔记后。
