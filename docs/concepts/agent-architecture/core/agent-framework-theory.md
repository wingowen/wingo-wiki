---
title: "AI Agent 框架理论篇 | Agent Framework Theory"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent]
sources: ["raw/articles/agent-framework-theory.md"]
notion_id: 34367b21-8207-8106-9972-f0d42cf861ef
---

# AI Agent 框架理论篇

> **来源**：腾讯技术工程

---

## 核心公式

**Agent = Reasoning + Acting**

### 三种基础模式

**1. ReAct 模式**（2022年，Yao等）
推理（Reasoning）+ 执行（Acting）+ 观察（Observation）循环。CoT 提升推理能力但缺少外部反馈，ReAct 弥补了这一缺陷。

**2. Plan-and-Execute 模式**（2023年，Langchain）
先制定完整分步计划，再按步骤执行。适合复杂且任务关系明确的长期任务，缺点是缺乏动态调整能力。

**3. Reflection 模式**
通过语言反馈强化 Agent。Reflexion（Shunyu Yao）维护反思文本；Self-Refine 通过迭代反馈改进；CRITIC 结合外部工具验证输出。

## Agent 框架三大部分

1. **LLM Call**：API 管理，兼容各大厂商 API
2. **Tools Call**：Function Call → MCP → 代码执行等外部工具
3. **Context Engineering**：提示词工程 + 工具与提示词结合（核心变量）

## Agent Loop

本质是一个 While 循环：初始化上下文 → LLM 推理 → 解析响应 → 执行工具 → 更新上下文 → 循环直到任务完成。

**核心结论**：Agent 框架设计的核心就是在 Agent Loop 中设计如何管理上下文。

## 相关链接

[react](../../other/core/react.md) | [agent-architecture](agent-architecture.md)
