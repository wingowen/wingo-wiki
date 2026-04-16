---
title: "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩（模块化版本）"
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [anthropic, benchmark, evaluation]
sources: []
---

# 用 Claude 3.5 Sonnet 提升 SWE-bench 成绩

我们最新的升级版 Claude 3.5 Sonnet 在 SWE-bench Verified（一项软件工程评估基准）上达到了 49% 的成绩，超越了之前 SOTA（State-of-the-Art，当前最优）模型的 45%。本文将介绍我们围绕该模型构建的「Agent（智能体）」，旨在帮助开发者充分发挥 Claude 3.5 Sonnet 的性能潜力。

## 目录

- [[swe-bench-section-intro|介绍]]
- [[swe-bench-section-sota|达到 SOTA]]
- [[swe-bench-section-tools|工具型 Agent]]
- [[swe-bench-section-results|结果]]
- [[swe-bench-section-example|Agent 行为示例]]
- [[swe-bench-section-challenges|挑战]]
- [[swe-bench-section-acknowledgements|致谢]]
- [[swe-bench-section-translator-note|译者注]]
- [[swe-bench-section-related-links|相关链接]]

---

> 原文链接：Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet
> 作者：Anthropic Engineering（Erik Schluntz 等人）
> 发布日期：2025-01-06
> 翻译日期：2026-04-14