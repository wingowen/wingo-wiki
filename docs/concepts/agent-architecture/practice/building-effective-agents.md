---
title: "构建高效 Agent | Building effective agents"
created: 2024-12-19
updated: 2024-12-19
type: concept
tags: [agent, anthropic, architecture]
sources: ["raw/articles/building-effective-agents.md"]
notion_id: 34267b21-8207-81b1-a412-df36f5a33826
---

## 构建高效 Agent

> 原文: Building effective agents
> 作者: Erik Schluntz, Barry Zhang（Anthropic）
> 发布日期: 2024-12-19

---

### 核心概念

**Agent** 指的是能够自主使用工具、规划步骤并执行任务以达成目标的 AI 系统。Anthropic 将 Agentic Systems 分为两类：

- **Workflows（工作流）**：通过预定义代码路径编排 LLM 和工具，适合明确定义的任务
- **Agents（智能体）**：LLM 动态指导自身流程和工具使用，适合需要灵活性的场景

**核心原则**：只有复杂性被证明能改善结果时才增加复杂性。

### 五种工作流模式

1. **Prompt Chaining（提示链）**：任务分解为固定序列步骤，每步处理前一步输出，适合可拆分为固定子任务
2. **Routing（路由分发）**：分类输入引导到专门后续任务，适合有明显不同类别的复杂任务
3. **Parallelization（并行化）**：分段（独立子任务并行）或投票（多次运行多样化输出）
4. **Orchestrator-Workers**：中央 LLM 动态分解任务，委派给工作者 LLM，适合无法预分子任务的复杂任务
5. **Evaluator-Optimizer**：一个 LLM 生成响应，另一个循环提供评估和反馈，适合有明确评估标准的迭代改进

### Agent 注意事项

Agent 的自主性意味着更高的成本和复合错误的潜在风险。建议在沙箱环境中广泛测试，并配合适当的护栏。

### 框架建议

开发者应首先直接使用 LLM API——许多模式只需几行代码即可实现。如果使用框架，务必理解底层代码。

## 相关链接

[ai-agent](../../entities/ai-agent.md) | [claude-code](../../entities/claude-code.md)
