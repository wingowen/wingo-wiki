---
title: "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩 - 介绍"
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [anthropic, benchmark, evaluation]
sources: []
---

# 介绍

SWE-bench 是一个 AI 评估基准（Benchmark），用于评估模型完成真实世界软件工程任务的能力。具体而言，它测试模型能否解决来自热门开源 Python 仓库的 GitHub Issue。对于基准中的每个任务，AI 模型会获得一个配置好的 Python 环境以及该仓库在 Issue 被解决之前的 Checkout（本地工作副本）。模型随后需要理解、修改并测试代码，最终提交其解决方案。

每个解决方案都会与关闭原始 GitHub Issue 的 Pull Request（PR，拉取请求）中的真实单元测试进行对比评分。这测试了 AI 模型是否能够实现与原始 PR 人类作者相同的功能。

SWE-bench 不仅仅评估孤立的 AI 模型，而是评估整个「Agent」系统。在此语境下，「Agent」指的是 AI 模型与其周围软件脚手架（Scaffolding）的组合。脚手架负责生成输入模型的 Prompt（提示词）、解析模型输出以执行操作，以及管理交互循环——即将模型上一次操作的结果纳入下一次 Prompt 中。即使使用相同的底层 AI 模型，Agent 在 SWE-bench 上的表现也可能因脚手架的不同而有显著差异。

💡 术语解释：Agent（智能体）——在 AI 领域，Agent 指的是能够自主感知环境、做出决策并执行行动的系统。在本文语境中，Agent = AI 模型 + 工具 + 脚手架代码。

评估大语言模型（Large Language Model，LLM）编码能力的基准有很多，但 SWE-bench 因以下几个原因而日益流行：

  1. 它使用来自真实项目的实际工程任务，而非竞赛或面试风格的问题；

  2. 它尚未饱和（Saturated）——仍有很大的提升空间。目前还没有任何模型在 SWE-bench Verified 上突破 50% 的完成率（不过截至本文撰写时，升级版 Claude 3.5 Sonnet 已达到 49%）；

  3. 它衡量的是整个「Agent」而非孤立的模型。开源开发者和初创公司在优化脚手架方面取得了巨大成功，能够在相同模型基础上大幅提升性能。

💡 术语解释：饱和（Saturated）——指基准测试中模型的得分已经接近满分，难以再通过改进来区分不同模型的优劣。SWE-bench 目前远未饱和，这意味着它仍然是一个有效的评估工具。

需要注意的是，原始 SWE-bench 数据集中包含一些在没有 GitHub Issue 之外的额外上下文（例如关于应返回的特定错误信息）的情况下无法解决的任务。SWE-bench Verified 是 SWE-bench 的一个包含 500 个问题的子集，经过人工审核确保它们都是可解决的，因此提供了对编码 Agent 性能最清晰的衡量标准。本文后续将统一指代这一基准。