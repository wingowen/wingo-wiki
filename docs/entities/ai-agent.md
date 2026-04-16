---
title: "AI Agent"
created: 2026-04-15
updated: 2026-04-15
type: entity
tags: [agent, anthropic, architecture]
sources: []
---
是一种能够自主理解目标、规划和执行多步骤任务的 AI 系统。与传统程序不同，Agent 通过 LLM 进行动态决策，而非预设固定流程。

## 核心能力

| 能力 | 描述 | 相关技术 |
|------|------|----------|
| **感知 (Perception)** | 理解用户意图，提取关键信息 | Intent Detection |
| **规划 (Planning)** | 分解任务，制定执行计划 | ReAct, Chain-of-Thought |
| **行动 (Action)** | 选择并执行工具 | Tool Use, MCP |
| **观察 (Observation)** | 获取工具执行结果 | Feedback Loop |
| **反思 (Reflection)** | 评估结果，调整策略 | Self-Correction |

## Agent vs 传统开发

| 维度 | 传统开发 | AI Agent |
|------|----------|----------|
| 决策方式 | 预设逻辑 | LLM 动态决策 |
| 执行路径 | 固定 | 可能多样 |
| 输入-输出 | 确定映射 | 概率性 |
| 错误处理 | 显式代码 | 自我反思 |

## 架构模式

- **ReAct**: 结合推理与行动的循环模式
- **LangGraph**: 基于状态机的多阶段 Agent 框架
- **Agentic RAG**: 带记忆的检索增强生成

## 相关链接

[[advanced-tool-use]] | [[agent-framework-practice]] | [[agent-framework-theory]] | [[agent-skills]] | [[building-effective-agents]] | [[context-engineering]] | [[effective-context-engineering]] | [[langgraph]] | [[mcp]] | [[multi-agent]] | [[react]] | [[tool-use]]
