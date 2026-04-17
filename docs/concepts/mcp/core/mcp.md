---
title: "MCP | 模型上下文协议"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [anthropic, mcp]
sources: []
---

# MCP (Model Context Protocol)

## Overview

MCP 是 Anthropic 提出的开放协议，用于标准化 AI 模型与外部工具、数据的连接。

## 架构

```
┌─────────────┐     MCP      ┌─────────────┐
│   Claude    │◄────────────►│  MCP Server │
│   (Client)  │              │ (File, DB,  │
└─────────────┘              │  Web, etc.) │
                             └─────────────┘
```

## 核心优势

- **标准化**: 一次开发，多处使用
- **安全**: 数据不离开本地
- **简化安装**: Desktop Extensions 实现一键安装

## Desktop Extensions

.mcpb 文件格式允许一键安装 MCP 服务器，包含所有依赖。

## 相关链接

[anthropic](../../entities/anthropic.md) | [claude-code](../../entities/claude-code.md) | [claude-desktop-extensions](../../claude/practice/claude-desktop-extensions.md) | [mcp-code-execution](../practice/mcp-code-execution.md) | [mcp-deep-dive](../practice/mcp-deep-dive.md) | [tool-use](../../tool-use/core/tool-use.md)
