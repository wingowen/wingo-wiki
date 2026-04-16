---
title: "在 Claude 开发者平台引入高级工具使用"
created: 2025-11-24
updated: 2025-11-24
type: concept
tags: [agent, anthropic]
sources: [raw/articles/advanced-tool-use.md]
notion_id: 34267b21-8207-81a2-b94a-f7ba3a444a5f
---

## 在 Claude 开发者平台引入高级工具使用

Anthropic 发布了三个 Beta 功能让 Claude 能够动态发现、学习和执行工具：Tool Search Tool（按需发现工具）、Programmatic Tool Calling（编程式工具调用）和 Tool Use Examples（工具使用示例）。

Tool Search Tool 通过 defer_loading 机制延迟加载工具定义，Claude 只在需要时搜索和加载相关工具，Token 使用量减少 85%。Programmatic Tool Calling 让 Claude 通过代码编排工具调用，中间结果保留在执行环境中而非进入上下文，Token 消耗从 43,588 降至 27,297（减少 37%），延迟显著降低。

## 核心要点

- **Tool Search Tool**：defer_loading 延迟加载，按需搜索工具，减少 85% Token 开销
- **Programmatic Tool Calling**：代码编排工具调用，循环/条件判断在代码中显式执行而非隐含在推理中
- **Token 节省**：中间结果不进入上下文，复杂任务 Token 消耗减少 37%
- **延迟降低**：单次代码块编排 20+ 工具调用，消除 19+ 次推理过程
- **准确性提升**：显式编排逻辑减少自然语言处理错误，知识检索从 25.6% 提升到 28.5%

## 相关链接

[[tool-use]] | [[mcp]]
