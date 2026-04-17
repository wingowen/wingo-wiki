---
title: "MCP 核心原理 | MCP Deep Dive"
created: 2025-06-26
updated: 2025-06-26
type: concept
tags: [anthropic, mcp]
sources: [raw/articles/mcp-deep-dive.md]
notion_id: 34367b21-8207-8199-83e2-4f68f4d7e0b7
---

# MCP 核心原理

## Overview

MCP（Model Context Protocol）是 Anthropic 提出的开放协议，用于标准化 AI 模型与外部工具、数据的连接。

## 架构

┌─────────────┐     MCP      ┌─────────────┐
│   Claude    │◄────────────►│  MCP Server │
│   (Client)  │              │ (File, DB,  │
└─────────────┘              │  Web, etc.) │
                             └─────────────┘

## 核心优势

- **标准化**: 一次开发，多处使用
- **安全**: 数据不离开本地
- **简化安装**: Desktop Extensions 实现一键安装

MCP 核心原理涵盖了 Desktop Extensions（桌面扩展）和代码执行两大主题。Desktop Extensions 通过 .mcpb 打包格式简化了 MCP 服务器的安装，用户只需双击文件即可完成安装，无需配置命令行或依赖管理。代码执行则解决了工具定义过多导致的 token 消耗问题——Agent 可以通过编写代码按需加载工具，将工具从"直接调用"转变为"代码 API"模式，token 使用量可减少 85-98%。

## 核心要点

- **MCP 协议**：开放标准，连接 AI 模型与外部工具/数据，支持文件系统、数据库、Web 等多种服务器
- **Desktop Extensions**：.mcpb 打包格式，内置运行时、自动更新、安全密钥存储，一键安装 MCP 服务器
- **代码执行模式**：将 MCP 工具生成为代码文件，Agent 按需加载而非预先加载，减少 85% token 消耗
- **渐进式披露**：工具按需发现，只加载当前任务所需的工具定义
- **隐私保护**：通过令牌化技术，PII 数据可在工具间流转而不进入模型上下文

## 相关链接

[[claude-desktop-extensions]] | [[tool-use]]
