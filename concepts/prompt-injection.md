---
title: "系统提示词注入分析"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent]
sources: []
notion_id: 34367b21-8207-8140-9199-e7fefb5ffb3c
---

# 系统提示词注入分析

## 系统提示词注入分析

### 1. 概述

本文档详细分析了 nanobot 系统中注入的提示词（Prompts），包括硬编码的提示词和通过文件注入的提示词。

### 2. 通过文件注入的提示词

#### 2.1 核心引导文件（BOOTSTRAP_FILES）

这些文件在系统启动时被加载，构成了代理的基本指令集：

```markdown
| 文件名 | 路径 | 作用 |
|--------|------|------|
| AGENTS.md | nanobot/templates/AGENTS.md | 代理指令，包含提醒和心跳任务的使用指南 |
| SOUL.md | nanobot/templates/SOUL.md | 定义代理的人格、价值观和沟通风格 |
| USER.md | nanobot/templates/USER.md | 用户配置文件，包含用户基本信息和偏好设置 |
| TOOLS.md | nanobot/templates/TOOLS.md | 工具使用说明和约束 |
```

#### 2.2 代理模板文件

这些文件定义了代理的身份和行为：

```markdown
| 文件名 | 路径 | 作用 |
|--------|------|------|
| identity.md | nanobot/templates/agent/identity.md | 核心身份信息，包含运行时环境和工作空间信息 |
| platform_policy.md | nanobot/templates/agent/platform_policy.md | 平台特定的政策和指导 |
| skills_section.md | nanobot/templates/agent/skills_section.md | 技能部分的模板 |
| consolidator_archive.md | nanobot/templates/agent/consolidator_archive.md | 整合器存档模板 |
| dream_phase1.md | nanobot/templates/agent/dream_phase1.md | 梦想阶段1模板 |
| dream_phase2.md | nanobot/templates/agent/dream_phase2.md | 梦想阶段2模板 |
| evaluator.md | nanobot/templates/agent/evaluator.md | 评估器模板 |
| max_iterations_message.md | nanobot/templates/agent/max_iterations_message.md | 最大迭代消息模板 |
| subagent_announce.md | nanobot/templates/agent/subagent_announce.md | 子代理公告模板 |
| subagent_system.md | nanobot/templates/agent/subagent_system.md | 子代理系统模板 |
| untrusted_content.md | nanobot/templates/agent/_snippets/untrusted_content.md | 不可信内容处理指南 |
```

#### 2.3 内存和心跳模板

```markdown
| 文件名 | 路径 | 作用 |
|--------|------|------|
| MEMORY.md | nanobot/templates/memory/MEMORY.md | 长期记忆模板 |
| HEARTBEAT.md | nanobot/templates/HEARTBEAT.md | 心跳任务模板 |
```

### 3. 硬编码的提示词

#### 3.1 核心系统硬编码提示词

```markdown
| 位置 | 提示词内容 | 作用 |
|------|-----------|------|
| ContextBuilder._RUNTIME_CONTEXT_TAG | [Runtime Context — metadata only, not instructions] | 运行时上下文标签 |
| ContextBuilder._build_runtime_context | 构建包含当前时间、通道和聊天ID的运行时上下文 | 提供运行时元数据 |
```

#### 3.2 工具相关硬编码提示词

```markdown
| 工具 | 提示词内容 | 作用 |
|------|-----------|------|
| CronTool | Tool to schedule reminders and recurring tasks. | cron 工具描述 |
| CronTool 参数说明 | 详细的参数说明和示例 | 指导用户如何使用 cron 工具 |
```

### 4. 提示词注入流程

1. 核心身份：加载 identity.md 模板，包含运行时环境和工作空间信息
1. 引导文件：加载 AGENTS.md、SOUL.md、USER.md、TOOLS.md
1. 记忆上下文：从内存存储中获取记忆上下文
1. 技能信息：加载始终激活的技能和技能摘要
1. 运行时上下文：在用户消息前注入运行时元数据
### 5. 总结

```markdown
| 类型 | 数量 | 位置 | 可定制性 |
|------|------|------|----------|
| 通过文件注入的提示词 | 16+ | nanobot/templates/ 目录 | 高（可编辑） |
| 硬编码的提示词 | 5+ | 代码中直接定义 | 低（需修改代码） |
```

nanobot 系统采用了混合的提示词注入方式，既通过文件系统提供了高度可定制的提示词模板，又在代码中硬编码了一些核心的系统提示词。这种设计使得系统既灵活又稳定，用户可以根据自己的需求定制代理行为，同时系统核心功能保持一致。

## 相关链接

[[tool-use]]
