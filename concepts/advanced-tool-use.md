---
title: "在 Claude 开发者平台引入高级工具使用 | Introducing advanced tool use on the Claude Developer Platform"
created: 2025-11-24
updated: 2025-11-24
type: translation
tags: [agent, anthropic]
sources: []
notion_id: 34267b21-8207-81a2-b94a-f7ba3a444a5f
---

## 在 Claude 开发者平台引入高级工具使用 | Introducing advanced tool use on the Claude Developer Platform

> 原文链接：https://www.anthropic.com/engineering/advanced-tool-use

> 作者：Bin Wu（Anthropic Claude 开发者平台团队）

> 发布日期：2025-11-24

> 翻译日期：2026-04-14

---

我们新增了三个 Beta 功能，让 Claude 能够动态地发现、学习和执行工具。以下是它们的工作原理。

AI Agent（智能体）的未来是模型能够无缝地在数百甚至数千个工具之间协作。一个集成 Git 操作、文件操作、包管理器、测试框架和部署流水线的 IDE 助手。一个同时连接 Slack、GitHub、Google Drive、Jira、公司数据库和数十个 MCP（Model Context Protocol，模型上下文协议）服务器的运维协调器。

要构建高效的 Agent，它们需要能够在不将每个工具定义都预先塞入上下文的情况下，使用无限的工具库。我们之前关于代码执行与 MCP 结合使用的博客文章讨论了工具结果和定义有时在 Agent 读取请求之前就会消耗 50,000+ 个 Token（令牌）。Agent 应该按需发现和加载工具，只保留与当前任务相关的内容。

Agent 还需要能够从代码中调用工具的能力。当使用自然语言工具调用时，每次调用都需要一次完整的推理过程（Inference Pass），而中间结果无论是否有用都会堆积在上下文中。代码天然适合编排逻辑，如循环、条件判断和数据转换。Agent 需要根据手头的任务灵活选择代码执行还是推理。

Agent 还需要从示例中学习正确的工具使用方式，而不仅仅是 Schema（模式）定义。JSON Schema 定义了结构上什么是有效的，但无法表达使用模式：何时包含可选参数、哪些组合是合理的，或者你的 API 期望什么约定。

今天，我们发布了三个让这一切成为可能的功能：

  - Tool Search Tool（工具搜索工具），允许 Claude 使用搜索工具访问数千个工具，而不会消耗其上下文窗口

  - Programmatic Tool Calling（编程式工具调用），允许 Claude 在代码执行环境中调用工具，减少对模型上下文窗口的影响

  - Tool Use Examples（工具使用示例），提供一种通用标准来演示如何有效地使用特定工具

在内部测试中，我们发现这些功能帮助我们构建了使用传统工具使用模式无法实现的东西。例如，Claude for Excel 使用 Programmatic Tool Calling 来读取和修改包含数千行的电子表格，而不会使模型的上下文窗口过载。

基于我们的经验，我们相信这些功能为使用 Claude 构建应用开辟了新的可能性。

### Tool Search Tool（工具搜索工具）

#### 挑战

MCP 工具定义提供了重要的上下文，但随着更多服务器连接，这些 Token 会不断累加。考虑一个五服务器的设置：

  - GitHub：35 个工具（约 26K Token）

  - Slack：11 个工具（约 21K Token）

  - Sentry：5 个工具（约 3K Token）

  - Grafana：5 个工具（约 3K Token）

  - Splunk：2 个工具（约 2K Token）

这是 58 个工具在对话开始之前就消耗了大约 55K Token。再加上更多服务器如 Jira（仅它就使用约 17K Token），你很快就会接近 100K+ Token 的开销。在 Anthropic，我们曾看到工具定义在优化前消耗了 134K Token。

但 Token 成本并不是唯一的问题。最常见的失败是选错工具和参数不正确，尤其是当工具名称相似时，比如 notification-send-user 与 notification-send-channel。

#### 我们的解决方案

Tool Search Tool 不是预先加载所有工具定义，而是按需发现工具。Claude 只看到它当前任务实际需要的工具。

Tool Search Tool 保留了 191,300 个 Token 的上下文，而 Claude 传统方法仅为 122,800 个。

传统方法：

  - 所有工具定义预先加载（50+ 个 MCP 工具约 72K Token）

  - 对话历史和系统提示争夺剩余空间

  - 总上下文消耗：在任何工作开始前约 77K Token

使用 Tool Search Tool：

  - 仅预先加载 Tool Search Tool（约 500 Token）

  - 工具按需发现（3-5 个相关工具，约 3K Token）

  - 总上下文消耗：约 8.7K Token，保留了 95% 的上下文窗口

这代表了 Token 使用量减少 85%，同时保持对完整工具库的访问。内部测试表明，在使用大型工具库进行 MCP 评估时，准确性有显著提升。Opus 4 从 49% 提升到 74%，Opus 4.5 从 79.5% 提升到 88.1%（启用 Tool Search Tool 后）。

#### Tool Search Tool 的工作原理

Tool Search Tool 让 Claude 能够动态发现工具，而不是预先加载所有定义。你将所有工具定义提供给 API，但通过 defer_loading: true 标记工具使其可按需发现。延迟加载的工具最初不会加载到 Claude 的上下文中。Claude 只能看到 Tool Search Tool 本身以及标记为 defer_loading: false 的工具（你最关键、最常用的工具）。

当 Claude 需要特定能力时，它会搜索相关工具。Tool Search Tool 返回匹配工具的引用，这些引用会在 Claude 的上下文中展开为完整定义。

例如，如果 Claude 需要与 GitHub 交互，它搜索 "github"，只有 github.createPullRequest 和 github.listIssues 会被加载——而不是你来自 Slack、Jira 和 Google Drive 的其他 50+ 个工具。

💡 术语解释：defer_loading（延迟加载）是一种策略，将工具定义从初始提示中排除，仅在 Claude 主动搜索时才加载到上下文中。这类似于数据库中的"懒加载"概念。

这样，Claude 可以访问你的完整工具库，同时只为它实际需要的工具支付 Token 成本。

Prompt Caching（提示缓存）说明：Tool Search Tool 不会破坏提示缓存，因为延迟加载的工具完全从初始提示中排除。它们仅在 Claude 搜索后才被添加到上下文中，因此你的系统提示和核心工具定义保持可缓存。

💡 术语解释：Prompt Caching 是 Anthropic API 的一项功能，可以缓存提示的前缀部分，避免在多轮对话中重复处理相同的内容，从而降低延迟和成本。

实现方式：

```json
{
  "tools": [
    // Include a tool search tool (regex, BM25, or custom)
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},

    // Mark tools for on-demand discovery
    {
      "name": "github.createPullRequest",
      "description": "Create a pull request",
      "input_schema": {...},
      "defer_loading": true
    }
    // ... hundreds more deferred tools with defer_loading: true
  ]
}
```

对于 MCP 服务器，你可以延迟加载整个服务器，同时保持特定高频使用的工具始终加载：

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-drive",
  "default_config": {"defer_loading": true},
  "configs": {
    "search_files": {
      "defer_loading": false
    }
  }
}
```

Claude 开发者平台开箱即用地提供了基于 Regex（正则表达式）和 BM25 的搜索工具，但你也可以使用 Embedding（嵌入向量）或其他策略实现自定义搜索工具。

💡 术语解释：BM25 是一种经典的文本检索排序算法，基于词频和文档频率对搜索结果进行排序。相比简单的关键词匹配，BM25 能更好地理解查询与文档之间的相关性。

#### 何时使用 Tool Search Tool

像任何架构决策一样，启用 Tool Search Tool 也涉及权衡。该功能在工具调用前增加了一个搜索步骤，因此当上下文节省和准确性提升超过额外延迟时，它才能提供最佳的投资回报率（ROI）。

推荐使用场景：

  - 工具定义消耗 >10K Token

  - 遇到工具选择准确性问题

  - 构建基于 MCP 的多服务器系统

  - 有 10+ 个可用工具

不太适合的场景：

  - 小型工具库（<10 个工具）

  - 所有工具在每个会话中频繁使用

  - 工具定义很紧凑

### Programmatic Tool Calling（编程式工具调用）

#### 挑战

随着工作流变得更加复杂，传统工具调用会产生两个根本性问题：

  - 来自中间结果的上下文污染：当 Claude 分析一个 10MB 的日志文件以查找错误模式时，整个文件都会进入其上下文窗口，尽管 Claude 只需要错误频率的摘要。当跨多个表获取客户数据时，每条记录无论是否相关都会在上下文中累积。这些中间结果消耗大量的 Token 预算，甚至可能将重要信息完全挤出上下文窗口。

  - 推理开销和手动综合：每次工具调用都需要一次完整的模型推理过程。收到结果后，Claude 必须"目测"数据以提取相关信息，推理各部分如何组合，并决定下一步——所有这些都通过自然语言处理来完成。一个涉及五个工具的工作流意味着五次推理过程，加上 Claude 解析每个结果、比较数值和综合结论。这既慢又容易出错。

#### 我们的解决方案

Programmatic Tool Calling 使 Claude 能够通过代码而非单独的 API 往返来编排工具。Claude 不再逐个请求工具并将每个结果返回到其上下文中，而是编写代码来调用多个工具、处理它们的输出，并控制哪些信息实际进入其上下文窗口。

Claude 擅长编写代码，通过让它在 Python 中表达编排逻辑而非通过自然语言工具调用，你可以获得更可靠、更精确的控制流。循环、条件判断、数据转换和错误处理在代码中都是显式的，而非隐含在 Claude 的推理中。

考虑一个常见的业务任务："哪些团队成员超出了他们的 Q3 差旅预算？"

你有三个可用工具：

  - get_team_members(department) - 返回团队成员列表，包含 ID 和级别

  - get_expenses(user_id, quarter) - 返回用户的费用明细项

  - get_budget_by_level(level) - 返回员工级别的预算限额

传统方法：

  - 获取团队成员 → 20 人

  - 为每个人获取 Q3 费用 → 20 次工具调用，每次返回 50-100 条明细（机票、酒店、餐饮、收据）

  - 按员工级别获取预算限额

  - 所有这些都进入 Claude 的上下文：2,000+ 条费用明细（50 KB+）

  - Claude 手动汇总每个人的费用，查找其预算，将费用与预算限额进行比较

  - 更多的模型往返，显著的上下文消耗

使用 Programmatic Tool Calling：

Claude 不再让每个工具结果返回到自身，而是编写一个 Python 脚本来编排整个工作流。该脚本在 Code Execution 工具（一个沙箱环境）中运行，当需要你的工具结果时会暂停。当你通过 API 返回工具结果时，它们由脚本处理而非被模型消费。脚本继续执行，Claude 只看到最终输出。

Programmatic Tool Calling 使 Claude 能够通过代码而非单独的 API 往返来编排工具，允许并行工具执行。

以下是 Claude 为预算合规任务编写的编排代码：

```python
team = await get_team_members("engineering")

# Fetch budgets for each unique level
levels = list(set(m["level"] for m in team))
budget_results = await asyncio.gather(*[
    get_budget_by_level(level) for level in levels
])

# Create a lookup dictionary: {"junior": budget1, "senior": budget2, ...}
budgets = {level: budget for level, budget in zip(levels, budget_results)}

# Fetch all expenses in parallel
expenses = await asyncio.gather(*[
    get_expenses(m["id"], "Q3") for m in team
])

# Find employees who exceeded their travel budget
exceeded = []
for member, exp in zip(team, expenses):
    budget = budgets[member["level"]]
    total = sum(e["amount"] for e in exp)
    if total > budget["travel_limit"]:
        exceeded.append({
            "name": member["name"],
            "spent": total,
            "limit": budget["travel_limit"]
        })

print(json.dumps(exceeded))
```

Claude 的上下文只收到最终结果：两三个超出预算的人。2,000+ 条明细、中间汇总和预算查找都不会影响 Claude 的上下文，将消耗从 200KB 的原始费用数据减少到仅 1KB 的结果。

效率提升是显著的：

  - Token 节省：通过将中间结果排除在 Claude 的上下文之外，PTC（Programmatic Tool Calling）大幅减少了 Token 消耗。平均使用量从 43,588 降至 27,297 个 Token，在复杂研究任务上减少了 37%。

  - 降低延迟：每次 API 往返都需要模型推理（数百毫秒到数秒）。当 Claude 在单个代码块中编排 20+ 次工具调用时，你消除了 19+ 次推理过程。API 处理工具执行而无需每次都返回模型。

  - 提高准确性：通过编写显式的编排逻辑，Claude 比在自然语言中处理多个工具结果时犯更少的错误。内部知识检索从 25.6% 提升到 28.5%；GIA 基准测试从 46.5% 提升到 51.2%。

生产工作流涉及杂乱的数据、条件逻辑和需要扩展的操作。Programmatic Tool Calling 让 Claude 能够以编程方式处理这种复杂性，同时保持对可操作结果的关注，而非原始数据处理。

#### Programmatic Tool Calling 的工作原理

## 相关链接

[[tool-use]] | [[mcp]]
