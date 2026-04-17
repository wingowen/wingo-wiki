---
title: "Agent 架构设计：从传统开发到智能体 | Agent Architecture Design"
created: "2026-04-15"
updated: "2026-04-15T10:08:00.000Z"
type: concept
tags: [agent, architecture, interview]
sources: ["raw/articles/agent-architecture.md"]
notion_id: "34367b21-8207-8163-9cdf-c8c77b1efa54"
---

> **难度**：⭐⭐⭐⭐ | **面试频率**：高 | **关联**：[langgraph-vs-react](../../comparisons/langgraph-vs-react.md) [context-management](../../context-engineering/core/context-management.md)

---

# Agent 架构设计：从传统开发到智能体

## 一、智能体 vs 传统开发：根本区别

| 维度 | 传统开发 | Agent 开发 |
|------|---------|-----------|
| 决策主体 | 开发者预设规则 | LLM 动态决策 |
| 执行路径 | 输入确定 → 输出确定 | 同样输入 → 不同路径 |
| 核心范式 | if-else 分支 | 感知→规划→行动→观察→反思 |

---

### 核心要点

**Agent 的思维模型**

```javascript
用户目标 → Agent 感知（理解意图）
         → Agent 规划（分解任务、制定计划）
         → Agent 行动（选择工具、执行操作）
         → Agent 观察（获取反馈）
         → Agent 反思（评估结果、调整策略）
         → 循环直到目标达成
```

**核心组件**
- **Perception（感知层）**：理解用户意图，提取关键信息
- **Decision（决策层）**：基于当前状态规划任务和选择工具
- **Action（行动层）**：执行具体的工具调用

**C端用户偏好实现**
- 用户画像构建：根据行为（click/favorite/book）更新兴趣权重
- 向量化与推荐：使用 Embedding 计算用户-物品相似度
- 冷启动问题：显式偏好收集、基于人口统计学、探索-利用策略

**面试高频追问**

Q: Agent 的"不可预测性"如何保证安全？
A: 工具层白名单、参数校验、沙箱执行、Human-in-the-loop、日志审计。

Q: 如何评估 Agent 的效果？
A: 任务完成率、工具调用效率、用户满意度、延迟、成本。

## 相关链接

[langgraph-vs-react](../../comparisons/langgraph-vs-react.md) | [context-management](../../context-engineering/core/context-management.md) | [agent-framework-practice](../practice/agent-framework-practice.md)