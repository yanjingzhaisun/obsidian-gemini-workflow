---
name: obsidian-synthesizer
description: Karpathy 模式的知识合成器。用于将 inbox 中的碎片信息“编译”为结构化的永久笔记（Permanent Notes），发现跨领域的潜在链接，并维护知识库的整体一致性。
---

# Obsidian Synthesizer (知识合成器)

此技能模仿 Andrej Karpathy 的 "LLM Wiki" 模式，将 Obsidian 作为 IDE，LLM 作为编译器，将原始素材转化为合成后的知识体系。

## 核心流程：Compilation (编译)

当用户要求“整理 inbox”或“合成知识”时，遵循以下步骤：

1. **摄入 (Ingestion)**：
   - 扫描 `inbox/` 文件夹中的 `.md` 文件或原始素材。
   - 提取核心事实、概念和数据点。

2. **关联 (Connection)**：
   - 使用 `grep_search` 在 `zettlekasten/` 中搜索与新概念相关的现有笔记。
   - 识别潜在的跨学科碰撞点（例如：将《战争论》的战略映射到《游戏设计》的机制中）。

3. **合成 (Synthesis)**：
   - **不要只是总结**。要创造新的、更高层级的结构化页面。
   - 遵循 `obsidian-metadata` 规范（YAML frontmatter, tags, date）。
   - 为新生成的笔记打上 `status/permanent` 标签。

4. **归档 (Archiving)**：
   - 合成完成后，将 `inbox/` 中的原始文件移动到 `archive/` 或更新其状态为 `status/processed`。

## 笔记模板：Synthesis Page

合成后的笔记应具有以下结构：

```markdown
---
date: YYYY-MM-DD
tags:
- status/permanent
- synthesis
- [相关主题标签]
---
# [合成主题名称]

## 核心综述
(AI 对该主题的深度整合描述)

## 关键概念映射
- **[概念 A]**: 源自 [[原始素材 A]]，在 [[现有笔记 B]] 中有相关应用。
- **[概念 B]**: ...

## 跨界碰撞 (Synthesis Insights)
(这是最有价值的部分：AI 发现的非直观关联)

## 待探索问题
(由本次合成引发的、尚待研究的后续方向)

---
参考来源：
- [[原始文件 1]]
- [[原始文件 2]]
```

## 使用场景
- 当 `inbox/` 积压过多碎片笔记时。
- 当需要对某一特定主题（如 "Game Design"）进行全库级别的知识重构时。
- 当用户想要“看看 AI 对我的这些想法有什么新看法”时。

## 辅助脚本
- `scripts/collect_context.py`: 自动收集 inbox 和相关 zettlekasten 笔记的文本。
