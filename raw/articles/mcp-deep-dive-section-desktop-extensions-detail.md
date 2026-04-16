---
title: "桌面扩展：Claude Desktop 一键安装 MCP 服务器"
created: 2025-06-26
updated: 2026-04-16
type: concept
tags: [mcp, agent, architecture]
sources: []
---

## 桌面扩展：Claude Desktop 一键安装 MCP 服务器 | Desktop Extensions
发布于 2025 年 6 月 26 日
Desktop Extensions（桌面扩展）让安装 MCP 服务器变得像点击按钮一样简单。本文将分享其技术架构以及创建优秀扩展的实用建议。
- 文件扩展名更新
去年当我们发布 Model Context Protocol（模型上下文协议，简称 MCP）时，我们看到开发者构建了令人惊叹的本地服务器，让 Claude 能够访问从文件系统到数据库的各种资源。但我们反复听到同样的反馈：安装过程太复杂了。用户需要安装开发者工具、手动编辑配置文件，还经常被依赖问题卡住。
今天，我们推出了 Desktop Extensions（桌面扩展）——一种全新的打包格式，让安装 MCP 服务器变得像点击按钮一样简单。

### 解决 MCP 安装难题
本地 MCP 服务器为 Claude Desktop 用户解锁了强大的能力。它们可以与本地应用交互、访问私有数据、与开发工具集成——同时所有数据都保留在用户的机器上。然而，当前的安装流程造成了显著的障碍：
- 需要开发者工具：用户需要安装 Node.js、Python 或其他运行时（Runtime）
  - 手动配置：每个服务器都需要编辑 JSON 配置文件
  - 依赖管理：用户必须自行解决包冲突和版本不匹配问题
  - 缺乏发现机制：寻找有用的 MCP 服务器需要在 GitHub 上搜索
  - 更新复杂：保持服务器最新意味着需要手动重新安装

💡 术语解释：运行时（Runtime）是指运行程序所需的软件环境。例如，Node.js 就是 JavaScript 代码的运行时环境，Python 则是 Python 代码的运行时环境。

这些摩擦点意味着，尽管 MCP 服务器功能强大，但对非技术用户来说基本无法使用。

### 介绍 Desktop Extensions
Desktop Extensions（.mcpb 文件）通过将整个 MCP 服务器——包括所有依赖——打包成一个可安装的包来解决这些问题。以下是用户体验的变化：

之前：
```javascript
# 先安装 Node.js
npm install -g @example/mcp-server
# 手动编辑 ~/.claude/claude_desktop_config.json
# 重启 Claude Desktop
# 祈祷它能正常工作
```

之后：
1. 下载一个 .mcpb 文件
  1. 双击用 Claude Desktop 打开
  1. 点击"安装"

就这样。不需要终端，不需要配置文件，没有依赖冲突。

## 相关链接

[[mcp-deep-dive-modular|MCP 深度解析（模块化版本）]] | [[mcp-deep-dive-section-desktop-extensions|Desktop Extensions（桌面扩展）]] | [[mcp-deep-dive-section-architecture-overview|架构概览]]
