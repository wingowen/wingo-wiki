---
title: "Think 工具：让 Claude 在复杂工具使用场景中停下来思考 | Think Tool"
created: 2025-03-20
updated: 2025-03-20
type: concept
tags: [agent, anthropic, reasoning]
sources: [raw/articles/think-tool.md]
notion_id: 34267b21-8207-813d-bba1-e5e25ef455a2
---

## Think 工具：让 Claude 在复杂工具使用场景中停下来思考

"Think" 工具是 Anthropic 发现的一种有效提升 Claude 复杂问题解决性能的方法，能在复杂任务中为结构化思考创建专属空间。它与 Extended Thinking 不同：Extended Thinking 是模型在生成响应前的深度推理，而 Think 工具是模型在收到工具结果后暂停反思是否已收集足够信息。

在 τ-Bench 评估中，Think 工具配合优化提示词在航空领域达到 0.570 的 pass^1 分数（基线仅 0.370），相对提升 54%。零售领域仅 Think 工具就达到 0.812。Think 工具最适合的场景包括：工具输出分析（需要仔细处理先前调用结果）、策略繁重环境（需遵循详细指南）和顺序决策（每步建立在前一步之上）。

## 核心要点

- **与 Extended Thinking 的区别**：Extended Thinking 在响应前深度推理，Think 工具在响应中反思工具结果
- **τ-Bench 基准**：测试模型在客户服务场景中使用工具的能力，pass^k 衡量 k 次尝试全部成功
- **最佳实践**：困难领域需要配合领域特定的提示词示例，提示词放系统提示比放工具描述更有效
- **适用场景**：长链工具调用、规则繁多环境、多步骤顺序决策
- **不适用场景**：单次或并行工具调用、简单指令遵循

## 相关链接

[claude-code](../../entities/claude-code.md) | [tool-use](../core/tool-use.md)
