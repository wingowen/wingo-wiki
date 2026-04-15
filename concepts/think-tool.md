---
title: ""Think" 工具：让 Claude 在复杂工具使用场景中停下来思考 | The think tool"
created: 2025-03-20
updated: 2025-03-20
type: translation
tags: [agent, anthropic, reasoning]
sources: []
notion_id: 34267b21-8207-813d-bba1-e5e25ef455a2
---

## "Think" 工具：让 Claude 在复杂工具使用场景中停下来思考

> 原文链接：https://www.anthropic.com/engineering/claude-think-tool

> 作者：Anthropic Engineering Team

> 发布日期：2025-03-20

> 翻译日期：2026-04-14

---

一种提升 Claude 复杂问题解决性能的新工具

随着我们不断提升 Claude 的复杂问题解决能力，我们发现了一种特别有效的方法：一个「think（思考）」工具，它能在复杂任务中为结构化思考创建专属空间。

这种简单却强大的技术——正如我们将在下文解释的，它与 Claude 新的「Extended Thinking（扩展思考）」能力不同——已经在 Claude 的 Agent（智能体）工具使用能力方面取得了显著的提升。这包括遵循策略、做出一致决策以及处理多步骤问题，而实现开销极小。

💡 术语解释：Agent（智能体）是指能够自主使用工具、与环境交互并完成复杂任务的 AI 系统。Claude 作为 Agent 时，可以通过调用外部工具（如搜索、数据库查询、API 调用等）来完成任务。

在本文中，我们将探讨如何在不同应用中实现「think」工具，并基于已验证的基准测试结果为开发者分享实用指导。

### 什么是「think」工具？

通过「think」工具，我们赋予 Claude 在得出最终答案的过程中加入一个额外思考步骤的能力——并拥有自己专属的思考空间。

虽然它听起来与 Extended Thinking 类似，但这是一个不同的概念。Extended Thinking 关注的是 Claude 在开始生成响应之前所做的事情。使用 Extended Thinking 时，Claude 会在采取行动之前深入考虑并迭代其计划。而「think」工具则是让 Claude 在开始生成响应之后，添加一个停下来思考的步骤，反思自己是否已经拥有继续推进所需的全部信息。这在执行长链工具调用或与用户进行冗长的多步骤对话时特别有帮助。

💡 举例说明：想象一个客服场景——Claude 需要帮用户取消航班。Extended Thinking 是 Claude 在回复用户之前，先在内部深入思考整个取消流程；而「think」工具则是 Claude 在查询了航班信息、用户身份等工具返回结果之后，停下来想一想：「我已经收集了所有必要信息吗？取消政策允许吗？还需要确认什么？」

这使得「think」工具更适合 Claude 无法仅凭用户查询就获得足够信息来构建响应的场景，即需要处理外部信息（例如工具调用结果中的信息）的情况。Claude 使用「think」工具进行的推理不如 Extended Thinking 那样全面，而是更加聚焦于模型发现的新信息。

我们建议在较简单的工具使用场景中使用 Extended Thinking，例如非顺序工具调用或简单的指令遵循。当你不需要 Claude 调用工具时，Extended Thinking 也适用于编程、数学和物理等用例。而「think」工具更适合 Claude 需要调用复杂工具、在长链工具调用中仔细分析工具输出、在规则繁多的环境中导航详细指南，或进行顺序决策（每一步都建立在前一步之上且错误代价高昂）的场景。

以下是使用来自 τ-Bench 的标准工具规范格式的示例实现：

```json
{
 "name": "think",
 "description": "Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.",
 "input_schema": {
 "type": "object",
 "properties": {
 "thought": {
 "type": "string",
 "description": "A thought to think about."
 }
 },
 "required": ["thought"]
 }
}
```

### 在 τ-Bench 上的性能表现

我们使用 τ-bench（tau-bench）评估了「think」工具，这是一个综合基准测试，旨在测试模型在真实客户服务场景中使用工具的能力，其中「think」工具是评估标准环境的一部分。

τ-bench 评估 Claude 的以下能力：

  - 与模拟用户进行真实对话

  - 始终如一地遵循复杂的客服 Agent 策略指南

  - 使用各种工具访问和操作环境数据库

τ-bench 中使用的主要评估指标是 pass^k，它衡量对于给定任务，所有 k 次独立任务试验都成功的概率，并在所有任务上取平均值。与其他 LLM 评估中常见的 pass@k 指标（衡量 k 次试验中是否至少有一次成功）不同，pass^k 评估的是一致性和可靠性——这是客户服务应用中至关重要的品质，因为始终如一地遵守策略是必不可少的。

💡 术语解释：pass^k 指标衡量的是 k 次独立尝试全部成功的概率。例如 pass^1 表示单次尝试的成功率，pass^5 表示连续 5 次尝试全部成功的概率。该指标对 Agent 的可靠性要求更高——不是偶尔成功一次就行，而是要稳定地反复成功。

#### 性能分析

我们的评估比较了几种不同的配置：

  1. 基线（无「think」工具，无 Extended Thinking 模式）

  2. 仅 Extended Thinking 模式

  3. 仅「think」工具

  4. 「think」工具 + 优化提示词（针对航空领域）

结果显示，当 Claude 3.7 有效使用「think」工具时，在基准测试的「航空」和「零售」客户服务领域均取得了显著提升：

  - 航空领域：「think」工具配合优化提示词在 pass^1 指标上达到 0.570，而基线仅为 0.370——相对提升 54%；

  - 零售领域：仅「think」工具就达到 0.812，而基线为 0.783。

Claude 3.7 Sonnet 在 Tau-Bench 评估「航空」领域的性能表现

四种不同配置的评估结果。分数为比例值。

航空领域的最佳性能是通过将「think」工具与优化提示词配对实现的，该提示词提供了分析客户请求时应使用的推理方法示例。以下是优化提示词的示例：

```javascript
## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness 

Here are some examples of what to iterate over inside the think tool:
<think_tool_example_1>
User wants to cancel flight ABC123
- Need to verify: user ID, reservation ID, reason
- Check cancellation rules:
 * Is it within 24h of booking?
 * If not, check ticket class and insurance
- Verify no segments flown or are in the past
- Plan: collect missing info, verify rules, get confirmation
</think_tool_example_1>

<think_tool_example_2>
User wants to book 3 tickets to NYC with 2 checked bags each
- Need user ID to check:
 * Membership tier for baggage allowance
 * Which payments methods exist in profile
- Baggage calculation:
 * Economy class × 3 passengers
 * If regular member: 1 free bag each → 3 extra bags = $150
 * If silver member: 2 free bags each → 0 extra bags = $0
 * If gold member: 3 free bags each → 0 extra bags = $0
- Payment rules to verify:
 * Max 1 travel certificate, 1 credit card, 3 gift cards
 * All payment methods must be in profile
 * Travel certificate remainder goes to waste
- Plan:
1. Get user ID
2. Verify membership level for bag fees
3. Check which payment methods in profile and if their combination is allowed
4. Calculate total: ticket price + any bag fees
5. Get explicit confirmation for booking
</think_tool_example_2>
```

特别有趣的是不同方法之间的比较。「think」工具配合优化提示词取得了显著优于 Extended Thinking 模式的结果（后者的表现与未加提示词的「think」工具相似）。仅使用「think」工具（不加提示词）相比基线有所提升，但仍不及优化方案。

「think」工具与优化提示词的组合以显著优势实现了最强性能，这可能是由于基准测试中航空策略部分的高复杂度，模型从获得如何「思考」的示例中获益最多。

在零售领域，我们也测试了各种配置以了解每种方法的具体影响。

Claude 3.7 Sonnet 在 Tau-Bench 评估「零售」领域的性能表现

三种不同配置的评估结果。分数为比例值。

「think」工具即使在没有额外提示词的情况下也达到了最高的 pass^1 分数 0.812。与航空领域相比，零售策略明显更容易导航，Claude 仅凭拥有一个思考空间就能获得提升，无需进一步指导。

#### τ-Bench 分析的关键洞察

我们的详细分析揭示了几个有助于有效实现「think」工具的模式：

  1. 在困难领域中提示词至关重要。仅仅让「think」工具可用可能会在一定程度上提升性能，但将其与优化提示词配对在困难领域产生了显著更好的结果。然而，较简单的领域可能仅凭拥有「think」工具就能受益。

  2. 跨试验的一致性提升。使用「think」工具的改进在 pass^k（k 最高到 5）上得到了保持，表明该工具帮助 Claude 更有效地处理边缘情况和异常场景。

### 在 SWE-Bench 上的性能表现

在评估 Claude 3.7 Sonnet 时，一个类似的「think」工具被添加到我们的 SWE-bench 设置中，为达到 0.623 的最先进（State-of-the-Art）分数做出了贡献。适配后的「think」工具定义如下：

```json
{
 "name": "think",
 "description": "Use the tool to think about something. It will not obtain new information or make any changes to the repository, but just log the thought. Use it when complex reasoning or brainstorming is needed. For example, if you explore the repo and discover the source of a bug, call this tool to brainstorm several unique ways of fixing the bug, and assess which change(s) are likely to be simplest and most effective. Alternatively, if you receive some test results, call this tool to brainstorm ways to fix the failing tests.",
 "input_schema": {
 "type": "object",
 "properties": {
 "thought": {
 "type": "string",
 "description": "Your thoughts."
 }
 },
 "required": ["thought"]
 }
}
```

💡 术语解释：SWE-Bench 是一个评估 AI 系统解决真实软件工程问题能力的基准测试。它包含来自 GitHub 的真实 issue 和对应的代码修复任务，衡量模型能否自主定位 bug 并提交正确的代码修复。

我们的实验（使用「think」工具 n=30 个样本，不使用 n=144 个样本）显示，单独添加此工具使性能平均提升了 1.6%（Welch's t-检验：t(38.89) = 6.71，p < .001，d = 1.47）。

### 何时使用「think」工具

基于这些评估结果，我们确定了 Claude 最能从「think」工具中受益的具体场景：

  1. 工具输出分析。当 Claude 需要在采取行动之前仔细处理先前工具调用的输出，并且可能需要回溯其方法时；

  2. 策略繁重的环境。当 Claude 需要遵循详细指南并验证合规性时；

  3. 顺序决策。当每个行动都建立在前一个行动之上且错误代价高昂时（常见于多步骤领域）。

### 实现最佳实践

为了在使用 Claude 时最大化「think」工具的效果，我们基于 τ-bench 实验推荐以下实现实践。

#### 1. 提供领域特定的推理示例进行策略性提示

最有效的方法是提供关于何时以及如何使用「think」工具的清晰指令，例如用于 τ-bench 航空领域的指令。提供针对你的特定用例定制的示例，能显著改善模型使用「think」工具的效果：

  - 推理过程中期望的详细程度；

  - 如何将复杂指令分解为可执行步骤；

  - 处理常见场景的决策树；

  - 如何检查是否已收集所有必要信息。

#### 2. 将复杂指导放在系统提示中

我们发现，当指令较长和/或较复杂时，将关于「think」工具的指令放在系统提示（System Prompt）中比放在工具描述本身中更有效。这种方法提供了更广泛的上下文，帮助模型更好地将思考过程整合到其整体行为中。

💡 术语解释：System Prompt（系统提示）是在对话开始前发送给模型的指令，用于设定模型的角色、行为规则和约束条件。与工具描述（仅在使用该工具时可见）不同，系统提示在整个对话过程中始终可见。

### 何时不应该使用「think」工具

虽然「think」工具可以带来显著提升，但它并不适用于所有工具使用场景，并且会增加提示词长度和输出 Token 的开销。具体来说，我们发现「think」工具在以下用例中不会带来任何改进：

  1. 非顺序工具调用。如果 Claude 只需要进行单次工具调用或多次并行调用来完成任务，添加「think」不太可能带来任何改进。

  2. 简单指令遵循。当 Claude 不需要遵守太多约束，且其默认行为已经足够好时，额外的「思考」不太可能带来收益。

### 快速上手

「think」工具是对你的 Claude 实现的一个简单补充，只需几个步骤就能产生有意义的改进：

  1. 在 Agent 工具使用场景中测试。从具有挑战性的用例开始——即 Claude 目前在策略合规性或长链工具调用中的复杂推理方面存在困难的场景。

  2. 添加工具定义。实现一个为你的领域定制的「think」工具。它需要最少的代码，但能实现更结构化的推理。同时考虑将关于何时以及如何使用该工具的指令连同与你领域相关的示例一起添加到系统提示中。

  3. 监控和优化。观察 Claude 在实践中如何使用该工具，并调整你的提示词以鼓励更有效的思考模式。

最好的部分是，添加此工具在性能结果方面的 downside 极小。除非 Claude 决定使用它，否则它不会改变外部行为，也不会干扰你现有的工具或工作流。

### 结论

我们的研究表明，「think」工具可以显著提升 Claude 3.7 Sonnet 在需要策略合规性和长链工具调用推理的复杂任务上的性能[1]。「Think」不是一刀切的解决方案，但对于正确的用例，它能提供实质性的收益，且实现复杂度极低。

我们期待看到你如何使用「think」工具与 Claude 构建更有能力、更可靠、更透明的 AI 系统。

[1]: 虽然我们的 τ-Bench 结果聚焦于 Claude 3.7 Sonnet 配合「think」工具的改进，但我们的实验表明 Claude 3.5 Sonnet (New) 也能在与 3.7 Sonnet 相同的配置下获得性能提升，说明这种改进可以推广到其他 Claude 模型。

---

### 译者注

  1. 关于标题翻译：原文标题为 "The 'think' tool: Enabling Claude to stop and think in complex tool use situations"，中文翻译在保留核心含义的同时，对语句结构进行了适当调整以符合中文表达习惯。

  2. 关于 Extended Thinking 与 Think Tool 的区别：这是本文最重要的概念区分。Extended Thinking 是 Anthropic 在 2025 年推出的模型内置能力，让模型在生成响应前进行深度推理（类似 OpenAI 的 o1 思维链）；而 Think Tool 是一种通过工具定义注入的外部机制，让模型在响应过程中可以随时暂停反思。两者可以互补使用。

  3. 关于 τ-Bench：τ-Bench（Tau-Bench）是由 Sierra Research 开发的 Agent 评估基准，专注于测试模型在真实客户服务场景中的工具使用能力。其航空领域因策略复杂度高而成为测试模型推理能力的理想场景。

  4. 关于数据解读：航空领域中「Think + 提示词」配置的 pass^1 从基线的 0.332 提升至 0.584，相对提升约 76%（原文正文提及 54% 是与 pass^1 = 0.370 的对比，表格中基线为 0.332，此处以表格数据为准）。

  5. 术语保留：文中如 τ-Bench、SWE-Bench、pass^k、System Prompt 等专业术语保留了英文原文或中英对照，以便读者查阅原始资料。

## 相关链接

[[claude-code]] | [[tool-use]]
