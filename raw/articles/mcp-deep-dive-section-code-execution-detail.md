---
title: "通过 MCP 实现代码执行：构建更高效的 Agent"
created: 2025-11-04
updated: 2026-04-16
type: concept
tags: [mcp, agent, architecture]
sources: []
---

## 通过 MCP 实现代码执行：构建更高效的 Agent
直接的工具调用会为每个定义和结果消耗上下文。Agent 通过编写代码来调用工具，能够更好地扩展规模。以下是它在 MCP 中的工作方式。

Model Context Protocol（模型上下文协议，简称 MCP） 是一个连接 AI Agent 与外部系统的开放标准。传统上，将 Agent 连接到工具和数据需要为每一对组合构建自定义集成，这导致了碎片化和重复劳动，使得构建真正互联的系统变得困难。MCP 提供了一个通用协议——开发者只需在 Agent 中实现一次 MCP，即可解锁整个集成生态系统。

自 2024 年 11 月发布 MCP 以来，其采用速度非常迅速：社区已经构建了数千个 MCP 服务器，SDK 已覆盖所有主流编程语言，业界也已将 MCP 作为连接 Agent 与工具和数据的实际标准。

如今，开发者通常会构建能够访问跨数十个 MCP 服务器的数百或数千个工具的 Agent。然而，随着连接工具数量的增长，预先加载所有工具定义并将中间结果通过上下文窗口传递，会拖慢 Agent 的速度并增加成本。

在这篇博客中，我们将探讨代码执行如何让 Agent 更高效地与 MCP 服务器交互，在处理更多工具的同时使用更少的 token。

## 相关链接

[[mcp-deep-dive-modular|MCP 深度解析（模块化版本）]] | [[mcp-deep-dive-section-code-execution|通过 MCP 实现代码执行]] | [[mcp-deep-dive-section-token-issue|工具消耗过多 token 导致 Agent 效率降低]]
