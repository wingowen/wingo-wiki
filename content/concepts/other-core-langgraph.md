---
title: "LangGraph | 语言图"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, architecture, langgraph]
sources: []
---

# LangGraph

## Overview

LangGraph 是由 LangChain 团队开发的一个用于构建有状态、多 actor 应用的框架，核心用于创建 Agent 和 Multi-Agent 系统。

## 核心概念

- **State**: 在图节点间传递的共享状态
- **Node**: 执行特定任务的函数
- **Edge**: 定义状态如何从一个节点转移到下一个
- **Checkpoint**: 状态持久化，支持恢复和回溯

## LangGraph vs ReAct

| 维度 | LangGraph | ReAct |
|------|-----------|-------|
| 状态管理 | 内置状态机 | 隐式状态 |
| 流程控制 | 显式图定义 | 自然语言推理 |
| 多轮对话 | 支持复杂状态 | 简单循环 |
| 可视化 | 流程图可视化 | 黑盒 |

## 代码示例

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_edge("agent", END)
app = workflow.compile()
```

## 相关链接

[[agent-architecture]] | [[ai-agent]] | [[long-running-agents]] | [[mcp-deep-dive]] | [[multi-agent]] | [[react]]
