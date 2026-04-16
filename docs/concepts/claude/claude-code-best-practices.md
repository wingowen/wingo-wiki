---
title: "Claude Code：Agent 编程最佳实践 | Claude Code Best Practices"
created: 2025-04-18
updated: 2025-04-18
type: concept
tags: [agent, anthropic]
sources: [raw/articles/claude-code-best-practices.md]
notion_id: 34267b21-8207-8192-a0d4-cff1c99ff3d2
---

## Claude Code：Agent 编程最佳实践

Claude Code 是 Anthropic 推出的 Agent 编程命令行工具，设计为底层且不预设偏好，提供接近原始模型的访问权限。核心设置包括创建 CLAUDE.md 文件记录常用命令、代码风格和测试说明，以及精心管理允许工具列表平衡安全性和功能性。

Claude Code 支持 MCP 协议连接扩展工具，通过自定义斜杠命令自动化重复工作流。有效工作流包括：探索→规划→编码→提交（先研究再动手）、TDD 测试驱动开发（写测试→失败→写代码→通过）、视觉目标迭代（截图→修改→迭代）。

## 核心要点

- **CLAUDE.md**：特殊文件，启动时自动拉取，记录命令、风格、仓库规范等信息
- **MCP 集成**：Claude Code 同时作为 MCP 服务器和客户端，支持扩展工具连接
- **工作流选择**：探索→规划→编码→提交（适合复杂任务）、TDD（适合测试验证场景）
- **允许工具管理**：平衡安全性，可选择始终允许、/permissions 命令或配置文件管理
- **YOLO 模式**：--dangerously-skip-permissions 绕过权限检查，适合 lint 修复等低风险任务

## 相关链接

[[claude-code]] | [[tool-use]]
