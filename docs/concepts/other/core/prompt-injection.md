---
title: "系统提示词注入分析 | Prompt Injection"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent]
sources: [../raw/articles/prompt-injection.md]
notion_id: 34367b21-8207-8140-9199-e7fefb5ffb3c
---

本文分析 nanobot 系统的提示词注入机制，采用**混合方式**：通过文件系统注入可定制模板（16+ 文件），代码中硬编码核心提示词（5+ 处）。

文件注入的提示词分为三类：**引导文件**（AGENTS.md、SOUL.md、USER.md、TOOLS.md）、**代理模板**（identity.md、platform_policy.md 等）、**内存心跳**（MEMORY.md、HEARTBEAT.md）。

注入流程：加载身份 → 加载引导文件 → 获取记忆上下文 → 加载技能信息 → 注入运行时元数据。这种设计使系统既灵活又稳定。

## 核心要点

- **文件注入提示词**：16+ 个模板文件位于 nanobot/templates/，可编辑定制
- **硬编码提示词**：5+ 处位于代码中（如 ContextBuilder._RUNTIME_CONTEXT_TAG）
- **引导文件**：AGENTS.md（代理指令）、SOUL.md（人格价值观）、USER.md（用户偏好）、TOOLS.md（工具约束）
- **代理模板**：包含 identity.md（核心身份）、skills_section.md（技能）、dream_phase1/2.md（梦想阶段）等
- **注入顺序**：身份 → 引导 → 记忆 → 技能 → 运行时元数据

## 相关链接

[tool-use](../../tool-use/core/tool-use.md)
