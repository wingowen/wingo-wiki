---
title: "Claude Code：Agent 编程最佳实践 | Claude Code best practices"
created: 2025-04-18
updated: 2025-04-18
type: concept
tags: [agent, anthropic]
sources: []
notion_id: 34267b21-8207-8192-a0d4-cff1c99ff3d2
---

> 原文链接：Claude Code: Best practices for agentic coding

> 作者：Anthropic Engineering Team

> 发布日期：2025-04-18

> 翻译日期：2026-04-14

---

## Claude Code：Agent 编程最佳实践

Claude Code 是一个用于 Agent 编程（Agentic Coding）的命令行工具。本文涵盖了在各种代码库、语言和环境中使用 Claude Code 时被证明有效的技巧和最佳实践。

我们最近发布了 Claude Code，一个用于 Agent 编程的命令行工具。作为研究项目开发的 Claude Code，为 Anthropic 的工程师和研究人员提供了一种更原生的方式，将 Claude 集成到他们的编码工作流中。

Claude Code 有意设计为底层且不预设偏好的（unopinionated），提供接近原始模型的访问权限，而不强制使用特定的工作流。这种设计理念创造了一个灵活、可定制、可脚本化且安全的强大工具。虽然功能强大，但这种灵活性对于刚接触 Agent 编程工具的工程师来说也存在学习曲线——至少在他们发展出自己的最佳实践之前是这样。

本文概述了在 Anthropic 内部团队以及使用 Claude Code 的外部工程师中已被证明有效的一般模式，涵盖各种代码库、语言和环境。这份清单中的任何内容都不是一成不变的，也并非普遍适用；请将这些建议视为起点。我们鼓励你进行实验，找到最适合自己的方式！

想要更详细的信息？我们在 claude.ai/code 的综合文档涵盖了本文提到的所有功能，并提供了额外的示例、实现细节和高级技巧。

### 1. 自定义你的设置

Claude Code 是一个 Agent 编程助手，会自动将上下文（context）拉取到提示词（prompt）中。这种上下文收集会消耗时间和 token，但你可以通过环境调优来优化它。

#### a. 创建 CLAUDE.md 文件

CLAUDE.md 是一个特殊文件，Claude 在启动对话时会自动将其拉取到上下文中。这使其成为记录以下内容的理想位置：

  - 常用的 bash 命令

  - 核心文件和工具函数

  - 代码风格指南

  - 测试说明

  - 仓库规范（例如，分支命名、merge vs. rebase 等）

  - 开发者环境设置（例如，pyenv 使用、哪些编译器可用）

  - 项目特有的任何意外行为或警告

  - 其他你希望 Claude 记住的信息

CLAUDE.md 文件没有必需的格式。我们建议保持简洁且人类可读。例如：

```javascript
# Bash commands
- npm run build: Build the project
- npm run typecheck: Run the typechecker

# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

你可以在以下几个位置放置 CLAUDE.md 文件：

  - 仓库根目录，或你运行 claude 的任何位置（最常见的用法）。将其命名为 CLAUDE.md 并提交到 git，以便在会话之间和团队之间共享（推荐），或命名为 CLAUDE.local.md 并将其添加到 .gitignore

  - 运行 claude 的目录的任何父目录。这对 monorepo（单体仓库）最有用，你可能从 root/foo 运行 claude，而在 root/CLAUDE.md 和 root/foo/CLAUDE.md 中都有 CLAUDE.md 文件。这两个文件都会被自动拉取到上下文中

  - 运行 claude 的目录的任何子目录。这与上述情况相反，在这种情况下，当你在子目录中处理文件时，Claude 会按需拉取 CLAUDE.md 文件

当你运行 /init 命令时，Claude 会自动为你生成一个 CLAUDE.md。

#### b. 调优你的 CLAUDE.md 文件

你的 CLAUDE.md 文件会成为 Claude 提示词的一部分，因此应该像任何频繁使用的提示词一样进行优化。一个常见的错误是添加了大量内容却没有迭代验证其有效性。花时间进行实验，确定什么能产生最佳的指令遵循效果。

你可以手动将内容添加到 CLAUDE.md，也可以按 # 键给 Claude 一条指令，它会自动将其合并到相关的 CLAUDE.md 中。许多工程师在编码时频繁使用 # 来记录命令、文件和风格指南，然后将 CLAUDE.md 的变更包含在提交中，使团队成员也能受益。

在 Anthropic，我们偶尔会通过 prompt improver（提示词优化器） 运行 CLAUDE.md 文件，并经常调优指令（例如，添加 "IMPORTANT" 或 "YOU MUST" 来强调）以提高遵循度。

#### c. 精心管理 Claude 的允许工具列表

默认情况下，Claude Code 对任何可能修改系统的操作都会请求权限：文件写入、许多 bash 命令、MCP 工具等。我们故意以这种保守的方式设计 Claude Code，以优先考虑安全性。你可以自定义允许列表（allowlist），以允许你知道是安全的额外工具，或者允许容易撤销的潜在不安全工具（例如，文件编辑、git commit）。

有四种方式来管理允许的工具：

  - 选择"始终允许"：在会话期间被提示时选择

  - /permissions 命令：例如，允许使用 Puppeteer MCP 服务器进行导航

  - 手动编辑你的 .claude/settings.json 或 ~/.claude.json（我们建议将前者提交到源代码控制以与团队共享）

  - 使用 --allowedTools CLI 标志：用于特定会话的权限

#### d. 如果使用 GitHub，请安装 gh CLI

Claude 知道如何使用 gh CLI 与 GitHub 交互，用于创建 issue、打开 pull request、阅读评论等。如果没有安装 gh，Claude 仍然可以使用 GitHub API 或 MCP 服务器（如果你安装了的话）。

### 2. 给 Claude 更多工具

Claude 可以访问你的 shell 环境，你可以像为自己构建一样，为它构建便捷脚本和函数集。它还可以通过 MCP（Model Context Protocol，模型上下文协议）和 REST API 利用更复杂的工具。

💡 术语解释：MCP（Model Context Protocol）是一种开放协议，允许 AI 模型与外部工具和数据源进行标准化交互。你可以把它理解为 AI 的"USB 接口"——任何支持 MCP 的工具都可以即插即用地连接到 Claude。

#### a. 将 Claude 与 bash 工具配合使用

Claude Code 继承你的 bash 环境，可以访问你所有的工具。虽然 Claude 知道常见的工具如 unix 工具和 gh，但如果没有指令，它不会知道你的自定义 bash 工具：

  1. 告诉 Claude 工具名称和使用示例

  2. 告诉 Claude 运行 --help 来查看工具文档

  3. 在 CLAUDE.md 中记录常用工具

#### b. 将 Claude 与 MCP 配合使用

Claude Code 同时作为 MCP 服务器和客户端运行。作为客户端，它可以通过三种方式连接到任意数量的 MCP 服务器来访问它们的工具：

  - 在项目配置中（在该目录下运行 Claude Code 时可用）

  - 在全局配置中（在所有项目中可用）

  - 在提交到版本控制的 .mcp.json 文件中（对任何在你的代码库中工作的人都可用）。例如，你可以将 Puppeteer 和 Sentry 服务器添加到 .mcp.json 中，这样每个在你的仓库中工作的工程师都可以开箱即用

在使用 MCP 时，使用 --mcp-debug 标志启动 Claude 也有助于识别配置问题。

#### c. 使用自定义斜杠命令

对于重复的工作流——调试循环、日志分析等——将提示词模板存储在 .claude/commands 文件夹中的 Markdown 文件里。当你输入 / 时，这些模板会通过斜杠命令菜单变为可用。你可以将这些命令提交到 git，使团队其他成员也能使用。

自定义斜杠命令可以包含特殊关键字 $ARGUMENTS 来传递命令调用时的参数。

例如，以下是一个你可以用来自动拉取和修复 GitHub issue 的斜杠命令：

```javascript
Please analyze and fix the GitHub issue: $ARGUMENTS.

Follow these steps:

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR

Remember to use the GitHub CLI (`gh`) for all GitHub-related tasks.
```

然后使用 /fix-issue 1234 来让 Claude 修复 issue #1234。类似地，你可以将自己的个人命令添加到 ~/.claude/commands 文件夹中，以便在所有会话中使用。

### 3. 尝试常见工作流

Claude Code 不强加特定的工作流，给你灵活使用它的自由。在这种灵活性所赋予的空间内，我们的用户社区中已经涌现出几种有效使用 Claude Code 的成功模式：

#### a. 探索 → 规划 → 编码 → 提交

这种多功能的工作流适用于许多问题：

  1. 让 Claude 探索代码库，提供一般性指引（"阅读处理日志的文件"）或具体文件名（"阅读 logging.py"），但明确告诉它暂时不要编写任何代码。

  2. 让 Claude 制定计划。我们建议使用 "think" 这个词来触发 Extended Thinking（扩展思考）模式，这会给 Claude 额外的计算时间来更彻底地评估备选方案。这些特定短语直接映射到系统中递增的思考预算（thinking budget）级别："think" < "think hard" < "think harder" < "ultrathink"。每个级别为 Claude 分配逐渐增多的思考预算。

  3. 让 Claude 用代码实现其解决方案。这也是一个好时机，可以要求它在实现解决方案的各个部分时明确验证其方案的合理性。

  4. 让 Claude 提交结果并创建 pull request。如果相关，这也是让 Claude 更新任何 README 或 changelog 来解释它刚刚做了什么的好时机。

第 1-2 步至关重要——没有它们，Claude 倾向于直接跳到编写解决方案的代码。虽然有时这正是你想要的，但对于需要预先深入思考的问题，让 Claude 先研究和规划可以显著提高性能。

#### b. 写测试、提交；写代码、迭代、提交

这是 Anthropic 最喜欢的工作流，适用于可以通过单元测试、集成测试或端到端测试轻松验证的变更。测试驱动开发（TDD，Test-Driven Development）在 Agent 编程中变得更加强大：

  1. 让 Claude 根据预期的输入/输出对编写测试。明确说明你正在做测试驱动开发，这样它就会避免创建模拟实现，即使对于代码库中尚不存在的功能也是如此。

  2. 告诉 Claude 运行测试并确认它们失败。明确告诉它在这个阶段不要编写任何实现代码通常是有帮助的。

  3. 当你对测试满意时，让 Claude 提交测试。

  4. 让 Claude 编写实现代码，指示它不要修改测试。告诉 Claude 继续进行直到所有测试通过。通常需要几次迭代：Claude 编写代码、运行测试、调整代码、再次运行测试。

  5. 当你对变更满意时，让 Claude 提交代码。

Claude 在有明确目标可以迭代时表现最佳——无论是视觉模型、测试用例还是其他类型的输出。通过提供测试等预期输出，Claude 可以进行更改、评估结果并逐步改进，直到成功。

#### c. 写代码、截图结果、迭代

与测试工作流类似，你可以为 Claude 提供视觉目标：

  1. 给 Claude 一种截取浏览器截图的方式（例如，使用 Puppeteer MCP server、iOS 模拟器 MCP server，或手动复制/粘贴截图到 Claude 中）。

  2. 给 Claude 一个视觉模型，通过复制/粘贴或拖放图片，或给 Claude 图片文件路径。

  3. 让 Claude 用代码实现设计，截取结果的截图，并迭代直到其结果与模型匹配。

  4. 当你满意时，让 Claude 提交。

和人类一样，Claude 的输出在迭代后会显著改善。虽然第一个版本可能不错，但在 2-3 次迭代后通常会好得多。给 Claude 查看其输出的工具以获得最佳结果。

#### d. 安全 YOLO 模式

💡 术语解释：YOLO 是 "You Only Live Once" 的缩写，在编程语境中表示跳过确认直接执行。Claude Code 的 --dangerously-skip-permissions 标志会绕过所有权限检查，让 Claude 无人值守地工作直到完成。

与其监督 Claude，你可以使用 claude --dangerously-skip-permissions 来绕过所有权限检查，让 Claude 不间断地工作直到完成。这适用于修复 lint 错误或生成样板代码等工作流。

让 Claude 运行任意命令是有风险的，可能导致数据丢失、系统损坏甚至数据泄露（例如，通过提示注入攻击）。为了最小化这些风险，请在没有互联网访问的容器中使用 --dangerously-skip-permissions。你可以参考这个使用 Docker Dev Containers 的参考实现。

#### e. 代码库问答

在入职新代码库时，使用 Claude Code 进行学习和探索。你可以向 Claude 提出与结对编程时向项目上另一位工程师提出的相同类型的问题。Claude 可以自主搜索代码库来回答一般性问题，例如：

  - 日志系统是如何工作的？

  - 如何创建一个新的 API 端点？

  - foo.rs 第 134 行的 async move { ... } 是什么意思？

  - CustomerOnboardingFlowImpl 处理了哪些边缘情况？

  - 为什么我们在第 333 行调用 foo() 而不是 bar()？

  - baz.py 第 334 行在 Java 中的等价写法是什么？

在 Anthropic，以这种方式使用 Claude Code 已成为我们的核心入职工作流，显著缩短了上手时间并减少了对其他工程师的负担。不需要特殊的提示词！只需提问，Claude 就会探索代码来找到答案。

## 相关链接

[[claude-code]] | [[tool-use]]
