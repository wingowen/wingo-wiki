---
title: "用 Agent Skills 装备 Agent 应对真实世界 | Equipping agents with Agent Skills"
created: 2025-10-16
updated: 2025-10-16
type: concept
tags: [agent, anthropic]
sources: []
notion_id: 34267b21-8207-8154-b45a-d542679a17a0
---

## 用 Agent Skills 装备 Agent 应对真实世界

> 原文: Equipping agents for the real world with Agent Skills

> 作者: Barry Zhang, Keith Lazuka, Mahesh Murag（Anthropic）

> 发布日期: 2025-10-16

> 翻译日期: 2026-04-14

---

### 概述

Claude 很强大，但真实工作需要程序性知识和组织上下文。Agent Skills 是一种新方式，通过文件和文件夹构建专业化 Agent。

随着模型能力的提升，我们现在可以构建与完整计算环境交互的通用 Agent。但随着这些 Agent 变得更强大，我们需要更可组合、可扩展、可移植的方式来为它们配备领域专业知识。

这促使我们创建了 Agent Skills：有组织的指令、脚本和资源文件夹，Agent 可以动态发现和加载以在特定任务上表现更好。Skills 通过将你的专业知识打包为可组合的资源来扩展 Claude 的能力，将通用 Agent 转变为适合你需求的专业化 Agent。

> 💡 通俗理解:

> 为 Agent 构建 Skill 就像为新员工编写入职指南。你不需要为每个用例构建碎片化的、定制设计的 Agent，而是可以通过捕获和共享程序性知识来用可组合的能力专业化你的 Agent。

---

### Skill 的结构

让我们通过一个真实示例来了解 Skills：驱动 Claude 最近推出的文档编辑功能 的技能之一。Claude 已经很了解如何理解 PDF，但在直接操作 PDF（例如填写表单）方面能力有限。这个 PDF Skill 让我们能够赋予 Claude 这些新能力。

在最简单的形式中，一个 Skill 是一个包含 SKILL.md 文件的目录。该文件必须以包含一些必需元数据的 YAML frontmatter 开头：name 和 description。启动时，Agent 会将每个已安装 Skill 的 name 和 description 预加载到其系统提示词中。

#### Progressive Disclosure（渐进式披露）

这是 Agent Skills 的核心设计原则。就像一本组织良好的手册——从目录开始，然后是特定章节，最后是详细的附录——Skills 让 Claude 只在需要时加载信息：

  1. 第一层：YAML 元数据（name + description）——Agent 启动时预加载，提供足够信息让 Claude 知道何时使用每个 Skill

  2. 第二层：SKILL.md 的正文——当 Claude 认为 Skill 与当前任务相关时，加载完整内容

  3. 第三层及以后：Skill 目录中的额外文件——Claude 可以根据需要选择性地导航和发现

> 💡 术语解释 - Progressive Disclosure（渐进式披露）:

> 一种信息设计原则，只在用户需要时才展示详细信息。就像餐厅菜单——先看分类（第一层），再看具体菜品（第二层），最后看配料和过敏原信息（第三层）。这样避免了信息过载。

> 🔑 关键优势: 拥有文件系统和代码执行工具的 Agent 不需要将 Skill 的全部内容读入其 Context Window。这意味着可以打包到 Skill 中的上下文量实际上是无限的。

#### Skills 和代码执行

Skills 还可以包含供 Claude 自行决定作为工具执行的代码。

> 💡 举例说明:

> 在 PDF Skill 中，包含一个预编写的 Python 脚本来读取 PDF 并提取所有表单字段。Claude 可以运行此脚本而无需将脚本或 PDF 加载到上下文中。而且因为代码是确定性的，这个工作流是一致且可重复的。

---

### Skills 和 Context Window 的交互

当用户的消息触发 Skill 时，Context Window 的变化序列：

  1. 初始状态：Context Window 包含核心系统提示词和每个已安装 Skill 的元数据，以及用户的初始消息

  2. Claude 通过调用 Bash 工具读取 pdf/SKILL.md 的内容来触发 PDF Skill

  3. Claude 选择读取 Skill 附带的 forms.md 文件

  4. Claude 现在已经加载了 PDF Skill 的相关指令，继续处理用户的任务

---

### 开发和评估 Skills 的最佳实践

  - 从评估开始：通过在代表性任务上运行 Agent 并观察其困难之处或需要额外上下文的地方，识别 Agent 能力中的具体差距。然后逐步构建 Skills 来解决这些不足

  - 为规模而构建：当 SKILL.md 文件变得过于庞大时，将其内容拆分为单独的文件并引用它们。如果某些上下文互斥或很少一起使用，保持路径分离将减少 token 使用量

  - 从 Claude 的角度思考：监控 Claude 在实际场景中如何使用你的 Skill 并根据观察进行迭代：注意意外的轨迹或对某些上下文的过度依赖。特别关注 Skill 的 name 和 description——Claude 在决定是否触发 Skill 时会使用这些信息

  - 与 Claude 一起迭代：在与 Claude 一起处理任务时，让 Claude 将其成功的方法和常见错误捕获到 Skill 中可复用的上下文和代码中。如果 Claude 在使用 Skill 完成任务时偏离轨道，让它自我反思哪里出了问题

---

### 使用 Skills 时的安全注意事项

Skills 通过指令和代码为 Claude 提供新能力。虽然这使它们强大，但也意味着恶意 Skills 可能会在使用环境中引入漏洞，或指示 Claude 泄露数据并采取意外操作。

> ⚠️ 建议: 只从可信来源安装 Skills。从不太可信的来源安装 Skill 时，在使用前彻底审计它。特别注意 Skill 中指示 Claude 连接到潜在不可信的外部网络源的指令或代码。

---

### Skills 的未来

Agent Skills 目前已在 Claude.ai、Claude Code、Claude Agent SDK 和 Claude Developer Platform 上得到支持。

展望未来，我们希望让 Agent 能够自主创建、编辑和评估 Skills，让它们将自己的行为模式编码为可复用的能力。

Skills 是一个简单概念，具有相应简单的格式。这种简单性使组织、开发者和最终用户更容易构建定制化 Agent 并赋予它们新能力。

---

> 📝 译者注: Agent Skills 的核心理念是 Progressive Disclosure（渐进式披露）——通过三层信息结构（元数据 → SKILL.md → 附加文件），让 Agent 只在需要时加载信息，有效解决了 Context Window 有限但专业知识无限的矛盾。这种设计模式不仅适用于 Claude，也可以应用于任何 AI Agent 系统的知识管理。

## 相关链接

[[tool-use]] | [[ai-agent]]
