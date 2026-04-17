---
title: "我们如何构建多 Agent 研究系统 | How we built our multi-agent research system"
created: 2025-06-13
updated: 2025-06-13
type: concept
tags: [agent, anthropic]
sources: ["raw/articles/multi-agent-research.md"]
notion_id: 34267b21-8207-81a8-9d00-fff6df2ade12
---

## 我们如何构建多 Agent 研究系统

> 原文：How we built our multi-agent research system
> 作者：Anthropic Engineering Team
> 发布日期：2025-06-13

### 什么是多 Agent 系统？

Multi-Agent System 由多个 Agent（LLM 在循环中自主使用工具）协同工作组成。Claude Research 使用 Orchestrator-Worker（编排者-工作者）模式：Lead Agent 负责协调流程，将任务委派给并行操作的专业 Subagent。

### 性能数据

- 以 Claude Opus 4 作为 Lead Agent、Sonnet 4 作为 Subagent 的多 Agent 系统，比单 Agent Opus 4 性能提升 **90.2%**
- 三个因素解释了 95% 的性能差异：Token 消耗量（80%）、工具调用次数、模型选择
- 升级到 Sonnet 4 的性能提升，比在 Sonnet 3.7 上将 Token 预算翻倍还要大

---

### 核心要点

**适用场景**
- 涉及大量并行化的任务
- 信息量超出单个上下文窗口的任务
- 需要与众多复杂工具交互的任务

**权衡取舍**
- Agent 消耗约 4 倍 Token，多 Agent 系统消耗约 15 倍 Token
- 不适合需要共享上下文或 Agent 之间有大量依赖关系的任务

**编写 Agent Prompt 的 8 条原则**

1. 像你的 Agent 一样思考 —— 使用 Console 构建模拟环境，逐步观察
2. 教会编排者如何委派 —— 每个 Subagent 需要目标、输出格式、工具指导、任务边界
3. 根据查询复杂度调整投入
4. 工具设计和选择至关重要 —— 优先使用专业工具而非通用工具
5. 让 Agent 自我改进 —— Claude 4 模型可以成为出色的 Prompt 工程师
6. 先广后深 —— 模仿专家人类研究的方式
7. 引导思考过程 —— Extended Thinking 充当可控的草稿本
8. 并行工具调用改变速度和性能 —— Lead Agent 并行启动 3-5 个 Subagent，Subagent 并行使用 3+ 工具

**Agent 的有效评估**
- 使用 LLM-as-Judge 评估输出
- 人工评估捕捉自动化遗漏的问题（如 Agent 始终选择 SEO 优化的内容农场而非权威来源）

**涌现行为（Emergent Behavior）**
- 对 Lead Agent 的微小改动可能不可预测地改变 Subagent 的行为方式
- 最好的 Prompt 不仅仅是严格的指令，而是协作框架

---

### 生产可靠性挑战

- Agent 是有状态的，错误会累积 —— 构建能从错误发生处恢复的系统
- 调试需要新方法 —— 监控 Agent 的决策模式和交互结构
- 使用彩虹部署（Rainbow Deployment）避免中断正在运行的 Agent

## 相关链接

[multi-agent](../core/multi-agent.md) | [anthropic](../../entities/anthropic.md)