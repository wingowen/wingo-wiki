---
title: "使用 Claude Agent SDK 构建 Agent | Building agents with the Claude Agent SDK"
created: 2025-09-29
updated: 2025-09-29
type: concept
tags: [agent, anthropic]
sources: [../raw/articles/claude-agent-sdk.md]
notion_id: 34267b21-8207-8141-8638-c436b190d370
---

Claude Agent SDK 是 Anthropic 提供的 Agent 开发工具集，前身为 Claude Code SDK。核心设计理念是"给 Claude 一台电脑"——通过终端访问让 Agent 获得与人类程序员相同的工作环境（文件编辑、bash 命令、代码执行等）。

Agent 循环是 SDK 的核心框架：**收集上下文 → 执行操作 → 验证工作 → 重复**。通过这个反馈循环，Agent 能够自主完成任务并在迭代中改进。

SDK 支持 Subagent（并行化和上下文隔离）、MCP 外部服务集成、代码生成能力，以及上下文自动压缩（compact）功能。

## 核心要点

- **工具设计**：工具应是 Agent 主要操作的体现，设计时应最大化上下文效率
- **上下文管理**：文件系统 + Agent 搜索优于纯语义搜索，Subagent 使用隔离 Context Window
- **验证机制**：基于规则的反馈（linting）优于模糊评判，视觉反馈对 UI 任务有帮助
- **渐进式迭代**：从 Agent 搜索开始，仅在需要时添加语义搜索层
- **测试方法**：构建代表性测试集，程序化评估 Agent 性能随功能的变化

## 相关链接

[[claude-code]] | [[anthropic]]
