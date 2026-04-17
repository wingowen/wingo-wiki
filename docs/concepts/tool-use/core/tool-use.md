---
title: "Tool Use | 工具使用"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, anthropic]
sources: []
---

# Tool Use

## Overview

Tool Use（工具使用）是 Agent 与外部世界交互的核心能力。通过调用外部工具，Agent 可以执行搜索、代码执行、文件操作等任务。

## 核心原则 (Anthropic)

来自 Anthropic 官方文档的最佳实践：

1. **让模型控制工具调用** - 模型决定何时以及如何调用工具
2. **工具设计要清晰明确** - 每个工具应有明确的输入输出定义
3. **错误处理要完善** - 工具应返回有意义的错误信息
4. **考虑工具调用的成本** - 每次 API 调用都有成本，需要优化

## Think Tool

Think Tool 是 Anthropic 引入的特殊工具，允许模型在复杂决策前进行静默推理。

```python
# Think Tool 示例
result = llm.invoke(
    messages,
    tools=[search, calculator, think_tool]
)
```

## 工具设计模式

- **Parallel Tool Use**: 模型可同时调用多个独立工具
- **Sequential Tool Use**: 工具结果作为下一个工具的输入
- **Tool Error Recovery**: 工具失败时模型自动重试或改用其他工具

## 相关链接

[advanced-tool-use](advanced-tool-use.md) | [agent-skills](../../other/practice/agent-skills.md) | [beyond-permission-prompts](../../other/practice/beyond-permission-prompts.md) | [mcp](../../mcp/core/mcp.md) | [prompt-injection](../../other/core/prompt-injection.md) | [think-tool](../practice/think-tool.md) | [writing-effective-tools](../practice/writing-effective-tools.md)
