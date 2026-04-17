---
title: "Agent 架构设计：从传统开发到智能体 | Agent Architecture Design"
created: "2026-04-15"
updated: "2026-04-15T10:08:00.000Z"
type: concept
tags: [agent, architecture, interview]
sources: ["raw/articles/agent-architecture.md"]
notion_id: "34367b21-8207-8163-9cdf-c8c77b1efa54"
---

> **难度**：⭐⭐⭐⭐ | **面试频率**：高 | **关联**：[langgraph](../../other/core/langgraph.md) [context-management](../../context-engineering/core/context-management.md) [mcp](../../mcp/core/mcp.md)

# Agent 架构设计：从传统开发到智能体

## 智能体 vs 传统开发：根本区别

| 维度 | 传统开发 | Agent 开发 |
|------|---------|-----------|
| 决策主体 | 开发者预设规则 | LLM 动态决策 |
| 执行路径 | 输入确定 → 输出确定 | 同样输入 → 不同路径 |
| 核心范式 | if-else 分支 | 感知→规划→行动→观察→反思 |

## Key Points

- **Agent 思维模型**：用户目标 → 感知意图 → 规划分解 → 选择工具执行 → 观察反馈 → 反思调整 → 循环直到目标达成
- **核心组件**：感知层（理解意图）、决策层（LLM 选择下一步）、行动层（执行工具）
- **C 端偏好实现**：行为数据更新兴趣权重 + Embedding 相似度匹配；冷启动用显式收集、人口统计学、探索-利用策略

## Interview Q&A

**Q: Agent 的"不可预测性"如何保证安全？**
A: 工具层白名单、参数校验、沙箱执行、Human-in-the-loop、日志审计。

**Q: 如何评估 Agent 的效果？**
A: 任务完成率、工具调用效率、用户满意度、延迟、成本。

## Related

[langgraph](../../other/core/langgraph.md) | [context-management](../../context-engineering/core/context-management.md) | [mcp](../../mcp/core/mcp.md)
