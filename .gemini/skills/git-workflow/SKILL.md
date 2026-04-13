---
name: git-workflow
description: 规范化 Git 提交流程。包括状态检查、差异对比、编写符合规范的提交信息以及推送代码。
---

# Git Workflow (Git 提交工作流) 规范

## 核心流程
1. **状态检查**：运行 `git status` 确认待提交的文件。
2. **变更回顾**：运行 `git diff HEAD` 审查代码改动，确保没有调试代码或敏感信息。
3. **分批暂存**：使用 `git add <file>` 针对性地暂存相关改动。
4. **提交信息**：编写清晰、简洁的 Commit Message。格式建议：`<type>(<scope>): <subject>`
   - `feat`: 新功能
   - `fix`: 修复问题
   - `refactor`: 代码重构（无功能变化）
   - `docs`: 文档更新
   - `chore`: 构建过程或辅助工具的变动
5. **推送**：确认无误后运行 `git push`。

## 注意事项
- **禁止暂存敏感文件**：如 `.env`, `.git` 文件夹或个人私密配置。
- **关联 Skill**：如果改动涉及 Skill 的更新，应在 commit 信息中注明。
- **原子提交**：尽量保持每个 commit 只负责一个逻辑上的改动。
