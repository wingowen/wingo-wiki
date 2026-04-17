---
title: "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩 | SWE-bench"
created: 2025-01-06
updated: 2025-01-06
type: concept
tags: [anthropic, benchmark, evaluation]
sources: [raw/articles/swe-bench.md]
notion_id: 34267b21-8207-812d-8ba2-e62bfbdca0aa
---

## 用 Claude 3.5 Sonnet 提升 SWE-bench 成绩

SWE-bench 是评估 AI 模型完成真实软件工程任务能力的基准测试，通过 GitHub Issue 和单元测试验证模型能否像人类开发者一样修复代码。Claude 3.5 Sonnet 在 SWE-bench Verified 上达到 49%，超越之前的 SOTA 模型 45%。

SWE-bench 评估的是整个 Agent 系统（AI 模型 + 脚手架代码），而非孤立模型。Agent 包含一个 Prompt、一个 Bash Tool 和一个 Edit Tool。工具设计的关键在于：要求绝对路径避免路径错误、使用字符串替换提高编辑可靠性、在工具描述中预判并防止常见错误。

## 核心要点

- **SWE-bench Verified**：500 个经过人工验证可解决的 GitHub Issue 子集，是衡量编码 Agent 的主流标准
- **Agent = 模型 + 工具 + 脚手架**：相同模型不同脚手架可产生显著不同的性能差异
- **工具设计原则**：绝对路径防路径错误、字符串替换可靠性最高、详细描述预判陷阱
- **THOUGHT/ACTION/OBSERVATION 模式**：清晰展示 Agent 的推理-行动-观察循环
- **性能瓶颈**：运行时长和高 Token 成本（成功运行可能需要数百轮、100k+ tokens）

## 相关链接


