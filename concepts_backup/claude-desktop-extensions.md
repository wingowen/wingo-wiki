---
title: "桌面扩展：Claude Desktop 一键安装 MCP 服务器"
created: 2025-06-26
updated: 2025-06-26
type: concept
tags: [anthropic]
sources: [raw/articles/claude-desktop-extensions.md]
notion_id: 34267b21-8207-8197-b8ca-d8f11d3ca649
---

## 桌面扩展：Claude Desktop 一键安装 MCP 服务器

Desktop Extensions（.mcpb 文件）是 Anthropic 推出的 MCP 服务器打包格式，让安装变得像点击按钮一样简单。传统安装需要 Node.js、手动编辑 JSON 配置文件和处理依赖问题，而 Desktop Extensions 将整个 MCP 服务器（包括所有依赖）打包成一个可安装文件，双击即可完成安装。

Desktop Extension 本质是一个 ZIP 压缩包，包含 manifest.json（扩展元数据和配置）、server/（MCP 服务器实现）和 dependencies/（所有必需包/库）。manifest.json 是唯一必需文件，其中定义了服务器类型（node/python/binary）、入口点、用户配置模板和平台特定设置。

## 核心要点

- **.mcpb 格式**：ZIP 打包格式，包含服务器、依赖和 manifest.json
- **内置运行时**：Claude Desktop 自带 Node.js，消除外部依赖
- **自动更新**：有新版本时自动更新
- **安全密钥存储**：API Key 等敏感信息存储在 OS Keychain 中
- **模板变量**：${__dirname}、${user_config.key} 等支持运行时值替换

## 相关链接

[[mcp]] | [[claude-code]]
