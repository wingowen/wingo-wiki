---
title: "AI Agent 框架实践篇 | Agent Framework Practice"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, architecture, tool-use]
sources: [raw/articles/agent-framework-practice.md]
---

## AI Agent 框架实践篇

AI Agent 框架的核心是在 Agent Loop（While 循环）中设计如何管理上下文。框架主要由三大要素构成：LLM Call（调用大语言模型）、Tool Call（工具调用解析）和 Context Engineering（上下文工程）。

极简 Agent 框架采用 DeepSeek 模型作为 LLM Provider，通过 OpenAI 兼容的 SDK 进行调用，支持同步非流式调用以保证代码可读性。工具层仅包含四个基础工具：shell_exec（执行 shell 命令）、file_read（读取文件）、file_write（写入文件）和 python_exec（执行 Python 代码）。Tools 注册采用手动维护的字典映射方式，遵循 OpenAI Function Calling 标准格式。

## 核心要点

- **Agent Loop 模式**：LLM call → parse tool_calls → execute → append results → loop or exit，循环驱动推理与工具调用
- **极简工具集**：四个核心工具（shell/file/python）即可实现强大的 Agent 能力
- **上下文管理**：messages 列表累积系统提示词、用户消息、助手响应和工具结果
- **OpenAI Function Schema**：Tools 定义遵循标准格式，name → (function, schema) 的映射关系
- **安全上限**：MAX_TURNS=20 防止无限循环，确保 Agent 可控退出

## 相关链接

[ai-agent](../../entities/ai-agent.md) | [agent-architecture](../core/agent-architecture.md) | [tool-use](../../tool-use/core/tool-use.md)
