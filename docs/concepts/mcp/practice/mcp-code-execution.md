---
title: "通过 MCP 实现代码执行：构建更高效的 Agent | MCP Code Execution"
created: 2025-06-26
updated: 2025-06-26
type: concept
tags: [agent, anthropic]
sources: ["raw/articles/mcp-code-execution.md"]
notion_id: 34267b21-8207-8138-b312-c3d319f17b5a
---

# 通过 MCP 实现代码执行：构建更高效的 Agent

> 原文：Code execution with MCP: Building more efficient agents
> 作者：Adam Jones, Conor Kelly
> 发布日期：2025-11-04

### 为什么工具消耗过多 token 会降低 Agent 效率？

随着 MCP 工具数量的增长，两种模式会增加成本和延迟：

1. **工具定义过载上下文窗口**：预先加载所有工具定义到上下文，数千个工具可能消耗数十万 token
2. **中间工具结果重复传递**：每个中间结果（如大型文档）都需要经过模型，可能超出上下文限制

### 核心解决方案：代码执行模式

将 MCP 服务器作为代码 API 而非直接工具调用。Agent 编写代码与 MCP 服务器交互，而非逐个调用工具。

**Token 节省效果**：从 150,000 → 2,000 tokens（节省 98.7%）。

### 核心要点

**渐进式披露（Progressive Disclosure）**
- 模型通过探索文件系统按需读取工具定义，而非一次性全部加载
- 可通过 search_tools 工具查找相关定义，控制详细程度

**上下文高效的工具结果**
- Agent 可以在代码中过滤和转换数据再返回，只将高信号信息传给模型
- 循环、条件判断和错误处理使用熟悉的代码模式

**隐私保护操作**
- 中间结果默认保留在执行环境中，不会进入模型上下文
- 可对 PII（个人身份信息）进行令牌化处理，防止敏感数据泄露

**状态持久化和 Skills**
- 具有文件系统访问权限的代码执行允许 Agent 在操作之间维护状态
- Agent 可将代码保存为可重用函数，形成结构化的 Skills 供将来使用

---

### 总结

MCP 为 Agent 连接许多工具和系统提供了基础协议。当工具数量过多时，通过代码执行方式（Code Mode）可以让 Agent 使用熟悉的编程构造来更高效地与 MCP 服务器交互，同时实现渐进式披露、隐私保护和状态持久化。

## 相关链接

[mcp](../core/mcp.md)