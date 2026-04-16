此次合并主要是创建了完整的 Wiki 概念组织结构，包含多个领域的核心概念文档和实践指南，同时添加了相关的计划和规范文件。新增内容涵盖代理架构、Claude 应用、上下文工程、MCP、多代理系统、RAG 技术和工具使用等多个技术领域。
| 文件 | 变更 |
|------|---------|
| docs/superpowers/plans/2026-04-16-wiki-concepts-organization-plan.md | - 创建 Wiki 概念组织计划，包含 400 行内容，详细规划了 Wiki 结构和概念分类 |
| docs/superpowers/specs/2026-04-16-wiki-concepts-organization-design.md | - 创建 Wiki 概念组织设计规范，包含 123 行内容，定义了 Wiki 的设计标准和实现方案 |
| test-wiki/.gitignore | - 创建测试 Wiki 的 .gitignore 文件，包含 3 行配置，指定了忽略的文件类型 |
| test-wiki/wiki/index.md | - 创建测试 Wiki 的索引文件，包含 12 行内容，自动生成的 Wiki 索引结构 |
| test-wiki/wiki/log.md | - 创建测试 Wiki 的日志文件，包含 6 行内容，跟踪 Wiki 操作记录 |
| wingo-wiki/.wikirc.yaml | - 创建 Wiki 配置文件，包含 9 行内容，定义了 Wiki 的基本配置信息 |
| wingo-wiki/wiki/concepts/agent-architecture/core/agent-architecture.md | - 创建代理架构核心概念文档，包含 60 行内容，详细介绍代理架构的基本原理 |
| wingo-wiki/wiki/concepts/agent-architecture/core/agent-framework-theory.md | - 创建代理框架理论文档，包含 46 行内容，阐述代理框架的理论基础 |
| wingo-wiki/wiki/concepts/agent-architecture/interview/interview-agent-arch.md | - 创建代理架构面试专题文档，包含 43 行内容，提供面试相关的代理架构知识 |
| wingo-wiki/wiki/concepts/agent-architecture/practice/agent-framework-practice.md | - 创建代理框架实践文档，包含 26 行内容，介绍代理框架的实际应用方法 |
| wingo-wiki/wiki/concepts/agent-architecture/practice/building-effective-agents.md | - 创建构建有效代理的实践文档，包含 46 行内容，提供构建高质量代理的指南 |
| wingo-wiki/wiki/concepts/claude/practice/claude-agent-sdk.md | - 创建 Claude 代理 SDK 文档，包含 27 行内容，介绍 Claude 代理开发工具 |
| wingo-wiki/wiki/concepts/claude/practice/claude-code-best-practices.md | - 创建 Claude 代码最佳实践文档，包含 27 行内容，提供 Claude 代码开发的最佳实践 |
| wingo-wiki/wiki/concepts/claude/practice/claude-desktop-extensions.md | - 创建 Claude 桌面扩展文档，包含 27 行内容，介绍 Claude 桌面应用的扩展功能 |
| wingo-wiki/wiki/concepts/claude/practice/claude-postmortem.md | - 创建 Claude 项目复盘文档，包含 43 行内容，分析 Claude 项目的经验教训 |
| wingo-wiki/wiki/concepts/context-engineering/core/context-engineering.md | - 创建上下文工程核心概念文档，包含 31 行内容，介绍上下文工程的基本概念 |
| wingo-wiki/wiki/concepts/context-engineering/core/context-management.md | - 创建上下文管理文档，包含 27 行内容，介绍上下文管理的方法和技巧 |
| wingo-wiki/wiki/concepts/context-engineering/interview/interview-context-mgmt.md | - 创建上下文管理面试专题文档，包含 58 行内容，提供面试相关的上下文管理知识 |
| wingo-wiki/wiki/concepts/context-engineering/practice/effective-context-engineering.md | - 创建有效上下文工程实践文档，包含 49 行内容，提供上下文工程的实践指南 |
| wingo-wiki/wiki/concepts/mcp/core/mcp.md | - 创建 MCP 核心概念文档，包含 38 行内容，介绍 MCP 的基本原理和功能 |
| wingo-wiki/wiki/concepts/mcp/practice/mcp-code-execution.md | - 创建 MCP 代码执行文档，包含 71 行内容，介绍 MCP 的代码执行功能 |
| wingo-wiki/wiki/concepts/mcp/practice/mcp-deep-dive.md | - 创建 MCP 深度解析文档，包含 43 行内容，深入分析 MCP 的工作原理 |
| wingo-wiki/wiki/concepts/multi-agent/core/multi-agent.md | - 创建多代理核心概念文档，包含 33 行内容，介绍多代理系统的基本概念 |
| wingo-wiki/wiki/concepts/multi-agent/practice/multi-agent-research.md | - 创建多代理研究文档，包含 69 行内容，介绍多代理系统的研究进展 |
| wingo-wiki/wiki/concepts/other/core/langgraph.md | - 创建 LangGraph 核心概念文档，包含 45 行内容，介绍 LangGraph 的基本原理 |
| wingo-wiki/wiki/concepts/other/core/prompt-injection.md | - 创建提示注入核心概念文档，包含 27 行内容，介绍提示注入的基本概念和防范方法 |
| wingo-wiki/wiki/concepts/other/core/react.md | - 创建 React 核心概念文档，包含 44 行内容，介绍 React 的基本原理和应用 |
| wingo-wiki/wiki/concepts/other/practice/agent-skills.md | - 创建代理技能实践文档，包含 27 行内容，介绍代理的各种技能和应用 |
| wingo-wiki/wiki/concepts/other/practice/beyond-permission-prompts.md | - 创建超越权限提示实践文档，包含 27 行内容，介绍如何设计更有效的提示 |
| wingo-wiki/wiki/concepts/other/practice/dual-memory-system.md | - 创建双重记忆系统实践文档，包含 44 行内容，介绍代理的记忆管理方法 |
| wingo-wiki/wiki/concepts/other/practice/long-running-agents.md | - 创建长期运行代理实践文档，包含 60 行内容，介绍如何构建可持续运行的代理 |
| wingo-wiki/wiki/concepts/other/practice/slash-commands.md | - 创建斜杠命令实践文档，包含 27 行内容，介绍代理的命令系统 |
| wingo-wiki/wiki/concepts/other/practice/swe-bench.md | - 创建 SWE-bench 实践文档，包含 27 行内容，介绍 Claude 在 SWE-bench 上的表现 |
| wingo-wiki/wiki/concepts/rag/core/contextual-retrieval.md | - 创建上下文检索核心概念文档，包含 60 行内容，介绍上下文检索的原理和应用 |
| wingo-wiki/wiki/concepts/rag/core/hyde.md | - 创建 HyDE 核心概念文档，包含 50 行内容，介绍假设文档嵌入的原理和应用 |
| wingo-wiki/wiki/concepts/rag/core/rag.md | - 创建 RAG 核心概念文档，包含 51 行内容，介绍检索增强生成的原理和应用 |
| wingo-wiki/wiki/concepts/rag/interview/interview-hyde.md | - 创建 HyDE 面试专题文档，包含 40 行内容，提供面试相关的 HyDE 知识 |
| wingo-wiki/wiki/concepts/tool-use/core/advanced-tool-use.md | - 创建高级工具使用核心概念文档，包含 27 行内容，介绍高级工具使用的功能和应用 |
| wingo-wiki/wiki/concepts/tool-use/core/tool-use.md | - 创建工具使用核心概念文档，包含 45 行内容，介绍工具使用的基本原理和方法 |
| wingo-wiki/wiki/concepts/tool-use/practice/think-tool.md | - 创建 Think 工具实践文档，包含 27 行内容，介绍 Think 工具的使用方法和效果 |
| wingo-wiki/wiki/concepts/tool-use/practice/writing-effective-tools.md | - 创建编写有效工具实践文档，包含 59 行内容，提供编写高质量工具的指南 |
| wingo-wiki/wiki/index.md | - 创建 Wiki 索引文件，包含 12 行内容，自动生成的 Wiki 索引结构 |
| wingo-wiki/wiki/log.md | - 创建 Wiki 日志文件，包含 3 行内容，跟踪 Wiki 操作记录 |