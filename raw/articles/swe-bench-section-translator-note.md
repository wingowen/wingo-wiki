---
title: "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩 - 译者注"
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [anthropic, benchmark, evaluation]
sources: []
---

# 译者注

  1. 本文是 Anthropic 工程博客系列中关于 SWE-bench 的重要技术文章，详细介绍了其 Agent 架构设计思路。文章强调的核心观点是：工具设计和脚手架的优化与模型本身的能力同等重要。

  2. 文中提到的「SWE-bench Verified」是 OpenAI 与 Princeton 等机构联合推出的子集基准，500 个问题均经过人工验证可解，是目前衡量编码 Agent 能力的主流标准之一。

  3. 值得注意的是，本文发表于 2025 年 1 月，当时 Claude 3.5 Sonnet 以 49% 创下纪录。截至翻译日期（2026 年 4 月），SWE-bench 的分数可能已有进一步提升。

  4. 文章中 Agent 的 THOUGHT/ACTION/OBSERVATION 模式虽然未被强制约束，但这一格式清晰展示了 Agent 的推理-行动-观察循环，对理解 Agent 工作原理很有帮助。

  5. 关于工具设计的关键启示：要求绝对路径、使用字符串替换而非行号编辑、在工具描述中预判并防止常见错误——这些经验对构建可靠的 AI Agent 具有普遍参考价值。