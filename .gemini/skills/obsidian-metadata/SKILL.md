---
name: obsidian-metadata
description: 规范化使用 Obsidian YAML Frontmatter (Properties)。当需要为笔记添加标签、日期、状态或其他元数据时使用此技能，确保符合 Obsidian 的视觉化属性编辑要求。
---

# Obsidian Metadata (Properties) 规范

## 核心原则
所有永久笔记和重要总结必须包含 YAML Frontmatter。这有助于 Obsidian 插件（如 Dataview）检索，并能触发 Obsidian 的原生属性编辑器。

## 格式标准
必须位于文档的最顶端，由三条连字符 `---` 包裹。

### 必填/推荐字段
- `tags`: 使用列表格式，而不是单行字符串。例如：
  ```yaml
  tags:
    - zettel/atomic
    - game-design
    - status/inbox
  ```
- `date`: 使用 {{date}}T{{time}} (ISO 8601标准格式)

用于status的tag有两种：status/inbox和status/permanent。新建一般都是status/inbox（并且在inbox文件夹内），而status/permanent则在zettlekasten文件夹下。


## 示例
```markdown
---
tags:
  - game-design/theory
  - zettel/atomic
  - status/inbox
date: 2026-04-11T03:10
---
```

## 注意事项
1. **标签格式**：不要在 YAML 内部使用 `#`。标签应该是纯文本字符串。
2. **双链**：不要在 YAML 字段内直接使用 `[[WikiLinks]]`，除非特定字段（如 `aliases`）有明确需求，且通常建议放在正文中。
3. **冒号后空格**：YAML 要求冒号后必须有一个空格 `key: value`。
