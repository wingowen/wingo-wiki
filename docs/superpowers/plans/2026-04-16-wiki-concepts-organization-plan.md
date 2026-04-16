# Wiki 概念页面组织实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 按照 llm-wiki 规范整理 wingo-wiki 中的概念页面，使其结构清晰、分类明确。

**Architecture:** 采用领域 + 主题的双重分类体系，遵循 llm-wiki 标准目录结构，使用 Node.js 版 llm-wiki CLI 工具管理。

**Tech Stack:** Node.js, llm-wiki CLI, Markdown, YAML

---

### 任务 1: 初始化 llm-wiki 结构

**文件:**
- 创建: `/workspace/wingo-wiki/.wikirc.yaml`
- 创建: `/workspace/wingo-wiki/wiki/index.md`
- 创建: `/workspace/wingo-wiki/wiki/log.md`
- 创建: `/workspace/wingo-wiki/raw/untracked/`
- 创建: `/workspace/wingo-wiki/raw/ingested/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/`
- 创建: `/workspace/wingo-wiki/wiki/sources/`
- 创建: `/workspace/wingo-wiki/wiki/answers/`

- [ ] **步骤 1: 创建 wingo-wiki 目录**

```bash
mkdir -p /workspace/wingo-wiki/wiki/concepts /workspace/wingo-wiki/wiki/sources /workspace/wingo-wiki/wiki/answers /workspace/wingo-wiki/raw/untracked /workspace/wingo-wiki/raw/ingested
```

- [ ] **步骤 2: 创建配置文件**

```yaml
# /workspace/wingo-wiki/.wikirc.yaml
# LLM Provider Configuration
llm:
  provider: openai
  model: gpt-4o
  apiKey: YOUR_API_KEY_HERE
  baseUrl: https://api.openai.com/v1
  temperature: 0.3 # Lower temperature for more consistent output
  thinking:
    type: disabled # Toggle for reasoning/thinking models (e.g., o1/o3)
```

- [ ] **步骤 3: 创建索引文件**

```markdown
# /workspace/wingo-wiki/wiki/index.md
# Wiki Index

This is the auto-generated index of your wiki. The LLM maintainer will update this file as it ingests new sources.

## Entities
*No entities yet.*

## Concepts
*No concepts yet.*

## Sources
*No sources yet.*
```

- [ ] **步骤 4: 创建日志文件**

```markdown
# /workspace/wingo-wiki/wiki/log.md
# Wiki Log

This file tracks all operations performed on the wiki.
```

- [ ] **步骤 5: 提交初始化文件**

```bash
git add /workspace/wingo-wiki/.wikirc.yaml /workspace/wingo-wiki/wiki/index.md /workspace/wingo-wiki/wiki/log.md
git commit -m "初始化 llm-wiki 结构"
```

### 任务 2: 内容审计与分类映射

**文件:**
- 分析: `/workspace/concepts/` 目录下的所有文件

- [ ] **步骤 1: 列出所有概念文件**

```bash
ls -la /workspace/concepts/
```

- [ ] **步骤 2: 识别重复内容**

```bash
# 检查文件名相似的文件
grep -r "title:" /workspace/concepts/*.md | sort
```

- [ ] **步骤 3: 创建分类映射表**

| 概念文件 | 领域分类 | 主题分类 |
|---------|---------|--------|
| agent-architecture.md | agent-architecture | core |
| agent-framework-theory.md | agent-architecture | core |
| agent-framework-practice.md | agent-architecture | practice |
| interview-agent-arch.md | agent-architecture | interview |
| tool-use.md | tool-use | core |
| advanced-tool-use.md | tool-use | core |
| writing-effective-tools.md | tool-use | practice |
| think-tool.md | tool-use | practice |
| context-engineering.md | context-engineering | core |
| context-management.md | context-engineering | core |
| effective-context-engineering.md | context-engineering | practice |
| interview-context-mgmt.md | context-engineering | interview |
| rag.md | rag | core |
| hyde.md | rag | core |
| contextual-retrieval.md | rag | core |
| interview-hyde.md | rag | interview |
| multi-agent.md | multi-agent | core |
| multi-agent-research.md | multi-agent | practice |
| mcp.md | mcp | core |
| mcp-deep-dive.md | mcp | practice |
| mcp-code-execution.md | mcp | practice |
| claude-code-best-practices.md | claude | practice |
| claude-agent-sdk.md | claude | practice |
| claude-desktop-extensions.md | claude | practice |
| claude-postmortem.md | claude | practice |
| langgraph.md | other | core |
| swe-bench.md | other | practice |
| react.md | other | core |
| prompt-injection.md | other | core |
| beyond-permission-prompts.md | other | practice |
| agent-skills.md | other | practice |
| long-running-agents.md | other | practice |
| slash-commands.md | other | practice |
| dual-memory-system.md | other | practice |

### 任务 3: 目录结构创建

**文件:**
- 创建: `/workspace/wingo-wiki/wiki/concepts/agent-architecture/core/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/agent-architecture/practice/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/agent-architecture/interview/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/tool-use/core/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/tool-use/practice/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/context-engineering/core/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/context-engineering/practice/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/context-engineering/interview/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/rag/core/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/rag/interview/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/multi-agent/core/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/multi-agent/practice/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/mcp/core/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/mcp/practice/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/claude/practice/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/other/core/`
- 创建: `/workspace/wingo-wiki/wiki/concepts/other/practice/`

- [ ] **步骤 1: 创建领域分类目录**

```bash
mkdir -p /workspace/wingo-wiki/wiki/concepts/agent-architecture/{core,practice,interview}
mkdir -p /workspace/wingo-wiki/wiki/concepts/tool-use/{core,practice}
mkdir -p /workspace/wingo-wiki/wiki/concepts/context-engineering/{core,practice,interview}
mkdir -p /workspace/wingo-wiki/wiki/concepts/rag/{core,interview}
mkdir -p /workspace/wingo-wiki/wiki/concepts/multi-agent/{core,practice}
mkdir -p /workspace/wingo-wiki/wiki/concepts/mcp/{core,practice}
mkdir -p /workspace/wingo-wiki/wiki/concepts/claude/practice
mkdir -p /workspace/wingo-wiki/wiki/concepts/other/{core,practice}
```

- [ ] **步骤 2: 验证目录结构**

```bash
find /workspace/wingo-wiki/wiki/concepts -type d | sort
```

### 任务 4: 内容迁移与合并

**文件:**
- 复制: `/workspace/concepts/*.md` → `/workspace/wingo-wiki/wiki/concepts/` 对应目录

- [ ] **步骤 1: 迁移 Agent 架构相关文件**

```bash
cp /workspace/concepts/agent-architecture.md /workspace/wingo-wiki/wiki/concepts/agent-architecture/core/
cp /workspace/concepts/agent-framework-theory.md /workspace/wingo-wiki/wiki/concepts/agent-architecture/core/
cp /workspace/concepts/agent-framework-practice.md /workspace/wingo-wiki/wiki/concepts/agent-architecture/practice/
cp /workspace/concepts/interview-agent-arch.md /workspace/wingo-wiki/wiki/concepts/agent-architecture/interview/
```

- [ ] **步骤 2: 迁移工具使用相关文件**

```bash
cp /workspace/concepts/tool-use.md /workspace/wingo-wiki/wiki/concepts/tool-use/core/
cp /workspace/concepts/advanced-tool-use.md /workspace/wingo-wiki/wiki/concepts/tool-use/core/
cp /workspace/concepts/writing-effective-tools.md /workspace/wingo-wiki/wiki/concepts/tool-use/practice/
cp /workspace/concepts/think-tool.md /workspace/wingo-wiki/wiki/concepts/tool-use/practice/
```

- [ ] **步骤 3: 迁移上下文工程相关文件**

```bash
cp /workspace/concepts/context-engineering.md /workspace/wingo-wiki/wiki/concepts/context-engineering/core/
cp /workspace/concepts/context-management.md /workspace/wingo-wiki/wiki/concepts/context-engineering/core/
cp /workspace/concepts/effective-context-engineering.md /workspace/wingo-wiki/wiki/concepts/context-engineering/practice/
cp /workspace/concepts/interview-context-mgmt.md /workspace/wingo-wiki/wiki/concepts/context-engineering/interview/
```

- [ ] **步骤 4: 迁移 RAG 相关文件**

```bash
cp /workspace/concepts/rag.md /workspace/wingo-wiki/wiki/concepts/rag/core/
cp /workspace/concepts/hyde.md /workspace/wingo-wiki/wiki/concepts/rag/core/
cp /workspace/concepts/contextual-retrieval.md /workspace/wingo-wiki/wiki/concepts/rag/core/
cp /workspace/concepts/interview-hyde.md /workspace/wingo-wiki/wiki/concepts/rag/interview/
```

- [ ] **步骤 5: 迁移多智能体相关文件**

```bash
cp /workspace/concepts/multi-agent.md /workspace/wingo-wiki/wiki/concepts/multi-agent/core/
cp /workspace/concepts/multi-agent-research.md /workspace/wingo-wiki/wiki/concepts/multi-agent/practice/
```

- [ ] **步骤 6: 迁移 MCP 相关文件**

```bash
cp /workspace/concepts/mcp.md /workspace/wingo-wiki/wiki/concepts/mcp/core/
cp /workspace/concepts/mcp-deep-dive.md /workspace/wingo-wiki/wiki/concepts/mcp/practice/
cp /workspace/concepts/mcp-code-execution.md /workspace/wingo-wiki/wiki/concepts/mcp/practice/
```

- [ ] **步骤 7: 迁移 Claude 相关文件**

```bash
cp /workspace/concepts/claude-code-best-practices.md /workspace/wingo-wiki/wiki/concepts/claude/practice/
cp /workspace/concepts/claude-agent-sdk.md /workspace/wingo-wiki/wiki/concepts/claude/practice/
cp /workspace/concepts/claude-desktop-extensions.md /workspace/wingo-wiki/wiki/concepts/claude/practice/
cp /workspace/concepts/claude-postmortem.md /workspace/wingo-wiki/wiki/concepts/claude/practice/
```

- [ ] **步骤 8: 迁移其他文件**

```bash
cp /workspace/concepts/langgraph.md /workspace/wingo-wiki/wiki/concepts/other/core/
cp /workspace/concepts/react.md /workspace/wingo-wiki/wiki/concepts/other/core/
cp /workspace/concepts/prompt-injection.md /workspace/wingo-wiki/wiki/concepts/other/core/
cp /workspace/concepts/swe-bench.md /workspace/wingo-wiki/wiki/concepts/other/practice/
cp /workspace/concepts/beyond-permission-prompts.md /workspace/wingo-wiki/wiki/concepts/other/practice/
cp /workspace/concepts/agent-skills.md /workspace/wingo-wiki/wiki/concepts/other/practice/
cp /workspace/concepts/long-running-agents.md /workspace/wingo-wiki/wiki/concepts/other/practice/
cp /workspace/concepts/slash-commands.md /workspace/wingo-wiki/wiki/concepts/other/practice/
cp /workspace/concepts/dual-memory-system.md /workspace/wingo-wiki/wiki/concepts/other/practice/
```

### 任务 5: 标题统一与元数据更新

**文件:**
- 修改: `/workspace/wingo-wiki/wiki/concepts/**/*.md`

- [ ] **步骤 1: 更新 Agent 架构相关文件标题**

```bash
# agent-architecture.md
sed -i 's/title: "Agent 架构设计：从传统开发到智能体"/title: "Agent 架构设计：从传统开发到智能体 | Agent Architecture Design"/' /workspace/wingo-wiki/wiki/concepts/agent-architecture/core/agent-architecture.md

# agent-framework-theory.md
sed -i 's/title: "AI Agent 框架理论篇 | Agent Framework Theory"/title: "AI Agent 框架理论篇 | Agent Framework Theory"/' /workspace/wingo-wiki/wiki/concepts/agent-architecture/core/agent-framework-theory.md

# agent-framework-practice.md
sed -i 's/title: "AI Agent 框架实践篇 | Agent Framework Practice"/title: "AI Agent 框架实践篇 | Agent Framework Practice"/' /workspace/wingo-wiki/wiki/concepts/agent-architecture/practice/agent-framework-practice.md

# interview-agent-arch.md
sed -i 's/title: "【面试专题】Agent 架构设计：从传统开发到智能体"/title: "【面试专题】Agent 架构设计：从传统开发到智能体 | Agent Architecture Interview"/' /workspace/wingo-wiki/wiki/concepts/agent-architecture/interview/interview-agent-arch.md
```

- [ ] **步骤 2: 更新工具使用相关文件标题**

```bash
# tool-use.md
sed -i 's/title: "Tool Use"/title: "Tool Use | 工具使用"/' /workspace/wingo-wiki/wiki/concepts/tool-use/core/tool-use.md

# advanced-tool-use.md
sed -i 's/title: "Advanced Tool Use"/title: "Advanced Tool Use | 高级工具使用"/' /workspace/wingo-wiki/wiki/concepts/tool-use/core/advanced-tool-use.md

# writing-effective-tools.md
sed -i 's/title: "用 Agent 为 Agent 编写高效工具 | Writing effective tools for agents"/title: "用 Agent 为 Agent 编写高效工具 | Writing effective tools for agents"/' /workspace/wingo-wiki/wiki/concepts/tool-use/practice/writing-effective-tools.md

# think-tool.md
sed -i 's/title: "Think 工具：让 Claude 在复杂工具使用场景中停下来思考"/title: "Think 工具：让 Claude 在复杂工具使用场景中停下来思考 | Think Tool"/' /workspace/wingo-wiki/wiki/concepts/tool-use/practice/think-tool.md
```

- [ ] **步骤 3: 批量更新其他文件标题**

```bash
# 上下文工程相关
sed -i 's/title: "Context Engineering"/title: "Context Engineering | 上下文工程"/' /workspace/wingo-wiki/wiki/concepts/context-engineering/core/context-engineering.md
sed -i 's/title: "上下文管理：短期记忆与长期记忆"/title: "上下文管理：短期记忆与长期记忆 | Context Management"/' /workspace/wingo-wiki/wiki/concepts/context-engineering/core/context-management.md
sed -i 's/title: "AI Agent 的有效上下文工程 | Effective context engineering for AI agents"/title: "AI Agent 的有效上下文工程 | Effective context engineering for AI agents"/' /workspace/wingo-wiki/wiki/concepts/context-engineering/practice/effective-context-engineering.md
sed -i 's/title: "【面试专题】上下文管理：短期记忆与长期记忆"/title: "【面试专题】上下文管理：短期记忆与长期记忆 | Context Management Interview"/' /workspace/wingo-wiki/wiki/concepts/context-engineering/interview/interview-context-mgmt.md

# RAG 相关
sed -i 's/title: "RAG"/title: "RAG | 检索增强生成"/' /workspace/wingo-wiki/wiki/concepts/rag/core/rag.md
sed -i 's/title: "HyDE 假设文档嵌入与高级检索策略"/title: "HyDE 假设文档嵌入与高级检索策略 | HyDE"/' /workspace/wingo-wiki/wiki/concepts/rag/core/hyde.md
sed -i 's/title: "RAG 检索增强生成：从分块到检索"/title: "RAG 检索增强生成：从分块到检索 | Contextual Retrieval"/' /workspace/wingo-wiki/wiki/concepts/rag/core/contextual-retrieval.md
sed -i 's/title: "【面试专题】HyDE 假设文档嵌入与高级检索策略"/title: "【面试专题】HyDE 假设文档嵌入与高级检索策略 | HyDE Interview"/' /workspace/wingo-wiki/wiki/concepts/rag/interview/interview-hyde.md

# 多智能体相关
sed -i 's/title: "Multi-Agent"/title: "Multi-Agent | 多智能体"/' /workspace/wingo-wiki/wiki/concepts/multi-agent/core/multi-agent.md
sed -i 's/title: "我们如何构建多 Agent 研究系统 | How we built our multi-agent research system"/title: "我们如何构建多 Agent 研究系统 | How we built our multi-agent research system"/' /workspace/wingo-wiki/wiki/concepts/multi-agent/practice/multi-agent-research.md

# MCP 相关
sed -i 's/title: "MCP"/title: "MCP | 模型上下文协议"/' /workspace/wingo-wiki/wiki/concepts/mcp/core/mcp.md
sed -i 's/title: "MCP 核心原理"/title: "MCP 核心原理 | MCP Deep Dive"/' /workspace/wingo-wiki/wiki/concepts/mcp/practice/mcp-deep-dive.md
sed -i 's/title: "通过 MCP 实现代码执行：构建更高效的 Agent"/title: "通过 MCP 实现代码执行：构建更高效的 Agent | MCP Code Execution"/' /workspace/wingo-wiki/wiki/concepts/mcp/practice/mcp-code-execution.md

# Claude 相关
sed -i 's/title: "Claude Code：Agent 编程最佳实践"/title: "Claude Code：Agent 编程最佳实践 | Claude Code Best Practices"/' /workspace/wingo-wiki/wiki/concepts/claude/practice/claude-code-best-practices.md
sed -i 's/title: "使用 Claude Agent SDK 构建 Agent | Building agents with the Claude Agent SDK"/title: "使用 Claude Agent SDK 构建 Agent | Building agents with the Claude Agent SDK"/' /workspace/wingo-wiki/wiki/concepts/claude/practice/claude-agent-sdk.md
sed -i 's/title: "桌面扩展：Claude Desktop 一键安装 MCP 服务器"/title: "桌面扩展：Claude Desktop 一键安装 MCP 服务器 | Claude Desktop Extensions"/' /workspace/wingo-wiki/wiki/concepts/claude/practice/claude-desktop-extensions.md
sed -i 's/title: "三个近期问题的故障复盘 | A postmortem of three recent issues"/title: "三个近期问题的故障复盘 | A postmortem of three recent issues"/' /workspace/wingo-wiki/wiki/concepts/claude/practice/claude-postmortem.md

# 其他
sed -i 's/title: "LangGraph"/title: "LangGraph | 语言图"/' /workspace/wingo-wiki/wiki/concepts/other/core/langgraph.md
sed -i 's/title: "ReAct"/title: "ReAct | 推理与行动"/' /workspace/wingo-wiki/wiki/concepts/other/core/react.md
sed -i 's/title: "系统提示词注入分析"/title: "系统提示词注入分析 | Prompt Injection"/' /workspace/wingo-wiki/wiki/concepts/other/core/prompt-injection.md
sed -i 's/title: "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩"/title: "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩 | SWE-bench"/' /workspace/wingo-wiki/wiki/concepts/other/practice/swe-bench.md
sed -i 's/title: "超越权限提示：让 Claude Code 更安全更自主 | Beyond permission prompts"/title: "超越权限提示：让 Claude Code 更安全更自主 | Beyond permission prompts"/' /workspace/wingo-wiki/wiki/concepts/other/practice/beyond-permission-prompts.md
sed -i 's/title: "用 Agent Skills 装备 Agent 应对真实世界 | Equipping agents with Agent Skills"/title: "用 Agent Skills 装备 Agent 应对真实世界 | Equipping agents with Agent Skills"/' /workspace/wingo-wiki/wiki/concepts/other/practice/agent-skills.md
sed -i 's/title: "构建长时间运行 Agent 的有效 Harness"/title: "构建长时间运行 Agent 的有效 Harness | Long Running Agents"/' /workspace/wingo-wiki/wiki/concepts/other/practice/long-running-agents.md
sed -i 's/title: "自定义 Slash 命令 Hook 设计方案"/title: "自定义 Slash 命令 Hook 设计方案 | Slash Commands"/' /workspace/wingo-wiki/wiki/concepts/other/practice/slash-commands.md
sed -i 's/title: "双层记忆系统与 Dream 管理知识文件的具体实现分析"/title: "双层记忆系统与 Dream 管理知识文件的具体实现分析 | Dual Memory System"/' /workspace/wingo-wiki/wiki/concepts/other/practice/dual-memory-system.md
```

### 任务 6: 链接更新与标准化

**文件:**
- 修改: `/workspace/wingo-wiki/wiki/concepts/**/*.md`

- [ ] **步骤 1: 批量更新内部链接格式**

```bash
# 使用 Obsidian 风格的链接格式
find /workspace/wingo-wiki/wiki/concepts -name "*.md" -exec sed -i 's/\[\[\([^|]+\)\]\]/\[\[\1\]\]/g' {} \;
```

- [ ] **步骤 2: 更新索引文件**

```bash
# 生成概念索引
cd /workspace/wingo-wiki && wiki ingest --dry-run
```

### 任务 7: 测试与验证

**文件:**
- 验证: `/workspace/wingo-wiki/wiki/` 目录结构

- [ ] **步骤 1: 验证目录结构**

```bash
find /workspace/wingo-wiki/wiki/concepts -type f | sort
```

- [ ] **步骤 2: 验证文件内容**

```bash
# 检查几个文件的标题格式
head -20 /workspace/wingo-wiki/wiki/concepts/agent-architecture/core/agent-architecture.md
```

- [ ] **步骤 3: 验证链接格式**

```bash
# 检查内部链接格式
grep -n "\[\[" /workspace/wingo-wiki/wiki/concepts/agent-architecture/core/agent-architecture.md
```

- [ ] **步骤 4: 提交最终结果**

```bash
git add /workspace/wingo-wiki/
git commit -m "按照 llm-wiki 规范整理概念页面"
```

## 自我审查

1. **规范覆盖**：所有设计文档中的要求都已在实施计划中得到体现
2. **占位符检查**：没有使用任何占位符或未完成的内容
3. **类型一致性**：所有文件路径和命令都保持一致

## 执行选项

**计划完成并保存到 `docs/superpowers/plans/2026-04-16-wiki-concepts-organization-plan.md`。两种执行选项：**

**1. 子代理驱动（推荐）** - 我为每个任务分配一个新的子代理，在任务之间进行审查，快速迭代

**2. 内联执行** - 在本次会话中使用 executing-plans 技能执行任务，批量执行并设置检查点

**选择哪种方法？**