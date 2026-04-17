---
title: "用 Agent Skills 装备 Agent 应对真实世界 | Equipping agents with Agent Skills"
created: 2025-10-16
updated: 2025-10-16
type: concept
tags: [agent, anthropic]
sources: [../raw/articles/agent-skills.md]
notion_id: 34267b21-8207-8154-b45a-d542679a17a0
---

Agent Skills 是 Anthropic 提出的 Agent 专业化方案，通过有组织的指令、脚本和资源文件夹，让通用 Agent 获得领域专业知识。核心理念是 Progressive Disclosure（渐进式披露）——像组织良好的手册一样，让 Agent 只在需要时加载信息。

Skill 结构分三层：**元数据**（name + description，预加载到系统提示词）、**SKILL.md 正文**（按需加载）、**附加文件**（选择性发现）。这种方式使 Context Window 可以处理无限量的专业知识。

Skills 还可包含预编写脚本供 Agent 执行，确保工作流的一致性和可重复性。开发时应从评估开始，为规模构建，从 Claude 视角迭代。

## 核心要点

- **渐进式披露**：元数据 → SKILL.md → 附加文件，三层结构避免信息过载
- **Skill 结构**：包含 SKILL.md 的目录，YAML frontmatter 定义 name 和 description
- **代码执行**：Skill 可包含确定性脚本，Claude 可自行调用而无需加载到上下文
- **安全注意**：只从可信来源安装 Skills，使用前审计外部网络连接指令
- **开发迭代**：观察 Claude 实际使用方式，特别关注 name/description 的触发效果

## 相关链接

[tool-use](../../tool-use/core/tool-use.md)
