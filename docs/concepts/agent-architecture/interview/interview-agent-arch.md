---
title: "【面试专题】Agent 架构设计：从传统开发到智能体 | Agent Architecture Interview"
created: 2026-04-15
updated: 2026-04-15
type: summary
tags: [agent, architecture, interview]
sources: ["raw/articles/interview-agent-arch.md"]
notion_id: 34367b21-8207-8163-9cdf-c8c77b1efa54
---

## Agent 架构设计：从传统开发到智能体

> 难度：⭐⭐⭐⭐ | 面试频率：高 | 关联：👉 LangGraph 核心原理与 ReAct 对比 👉 上下文管理：短期记忆与长期记忆

---

### 什么是 Agent？

Agent 是能够自主使用工具、规划步骤并执行任务以达成目标的 AI 系统。与传统开发的"输入确定则输出确定"不同，Agent 的每一步都是 LLM 动态决策的，同样的输入可能产生不同的执行路径。

Agent 思维模型：用户目标 → 感知意图 → 规划分解 → 选择工具执行 → 观察反馈 → 反思调整 → 循环直到目标达成。

### 核心架构组件

**感知层（Perception）**：理解用户意图，提取关键信息，将非结构化输入转为结构化状态。

**决策层（Decision）**：基于当前状态（可用工具、历史消息）由 LLM 决定下一步行动。

**行动层（Action）**：执行具体工具调用，返回结果供下一轮推理使用。

### C 端用户偏好实现

用户画像通过行为数据（click/favorite/book）动态更新兴趣权重，向量化后进行相似度匹配推荐。冷启动时可采用：显式偏好收集、人口统计学推荐、探索-利用策略、迁移学习等方案。

### 面试要点

- **安全性**：多层防护包括工具白名单、参数校验、沙箱执行、Human-in-the-loop、人工审核
- **成本控制**：减少不必要 LLM 调用、大小模型路由、优化 Prompt 长度、设置 MAX_TURNS
- **效果评估**：任务完成率、工具调用效率、用户满意度、延迟、成本

## 相关链接

[agent-architecture](../core/agent-architecture.md) | [interview-qa-overview](../../queries/interview-qa-overview.md)
