# 概念页面与目录统一优化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 统一概念页面与目录导航，强化左侧导航，将概念索引页面转变为概念发现与概览页面。

**Architecture:** 利用 MkDocs Material 主题的导航特性，重构概念索引页面，清理冗余索引文件，启用新的导航特性。

**Tech Stack:** MkDocs, Material for MkDocs, JavaScript, ECharts

---

### 任务 1: 备份当前内容

**Files:**
- 所有相关文件

- [ ] **步骤 1: 备份概念目录**

```bash
cp -r /workspace/docs/concepts /workspace/docs/concepts_backup
```

- [ ] **步骤 2: 验证备份**

```bash
ls -la /workspace/docs/concepts_backup
```

- [ ] **步骤 3: 提交备份**

```bash
git add /workspace/docs/concepts_backup
git commit -m "backup: 备份概念目录"
```

### 任务 2: 更新 mkdocs.yml 启用新特性

**Files:**
- Modify: [mkdocs.yml](file:///workspace/mkdocs.yml)

- [ ] **步骤 1: 修改 mkdocs.yml**

```yaml
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.path
    - navigation.indexes
    - toc.integrate
    - search.suggest
    - search.highlight
  palette:
    scheme: slate
    primary: indigo
    accent: indigo
```

- [ ] **步骤 2: 验证配置**

```bash
cd /workspace && mkdocs build --dry-run
```

- [ ] **步骤 3: 提交更改**

```bash
git add /workspace/mkdocs.yml
git commit -m "feat: 启用新的导航特性"
```

### 任务 3: 重构 concepts/index.md 为概念概览页面

**Files:**
- Modify: [concepts/index.md](file:///workspace/docs/concepts/index.md)

- [ ] **步骤 1: 重写概念索引页面**

```markdown
---
title: "概念"
created: "2026-04-16"
type: section
tags: [concepts]
---

# 概念概览

欢迎来到概念概览页面！这里是探索各种技术概念的起点，按照不同的领域进行分类。

## 概念分类

<div class="grid cards" markdown>

-   :material-lightbulb-outline:{ .lg .middle } **Agent Architecture**
    
    代理架构相关的核心概念、理论和实践指南。
    
    [:octicons-arrow-right-24: 探索](agent-architecture/)

-   :material-cog-outline:{ .lg .middle } **Context Engineering**
    
    专注于代理上下文管理的核心概念、实践应用和面试相关内容。
    
    [:octicons-arrow-right-24: 探索](context-engineering/)

-   :material-database-search:{ .lg .middle } **RAG**
    
    涵盖上下文检索、HYDE 技术和 RAG 核心概念，以及相关面试内容。
    
    [:octicons-arrow-right-24: 探索](rag/)

-   :material-wrench-outline:{ .lg .middle } **Tool Use**
    
    包括高级工具使用、工具使用基础概念和实践应用。
    
    [:octicons-arrow-right-24: 探索](tool-use/)

-   :material-account-group:{ .lg .middle } **Multi-Agent**
    
    探索多智能体系统的核心概念和实践应用。
    
    [:octicons-arrow-right-24: 探索](multi-agent/)

-   :material-link-variant:{ .lg .middle } **MCP**
    
    详细介绍 MCP 的核心概念、代码执行和深度解析。
    
    [:octicons-arrow-right-24: 探索](mcp/)

-   :material-brain:{ .lg .middle } **Claude**
    
    包含 Claude Agent SDK、代码最佳实践、桌面扩展和事后分析。
    
    [:octicons-arrow-right-24: 探索](claude/)

-   :material-star-outline:{ .lg .middle } **其他**
    
    涵盖 LangGraph、提示注入、React 等核心概念，以及各种实践应用。
    
    [:octicons-arrow-right-24: 探索](other/)

</div>

## 快速访问

### 热门概念

- [Agent 架构设计](agent-architecture/core/agent-architecture.md)
- [RAG](rag/core/rag.md)
- [Tool Use](tool-use/core/tool-use.md)
- [Context Engineering](context-engineering/core/context-engineering.md)
- [MCP](mcp/core/mcp.md)
- [Multi-Agent](multi-agent/core/multi-agent.md)

### 最新更新

- [Agent 框架实践](agent-architecture/practice/agent-framework-practice.md)
- [MCP 深度解析](mcp/practice/mcp-deep-dive.md)
- [Claude 代码最佳实践](claude/practice/claude-code-best-practices.md)

## 概念关系图谱

<div id="graph-container" style="width: 100%; height: 600px;"></div>

<script>
  // 初始化 ECharts 实例
  var myChart = echarts.init(document.getElementById('graph-container'));
  
  // 图表配置
  var option = {
    title: {
      text: '核心概念关系图谱',
      left: 'center'
    },
    tooltip: {},
    animationDurationUpdate: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
      {
        type: 'graph',
        layout: 'force',
        force: {
          repulsion: 100,
          edgeLength: [80, 120]
        },
        roam: true,
        label: {
          show: true
        },
        data: [
          {name: 'Agent 架构', symbolSize: 50},
          {name: 'RAG', symbolSize: 40},
          {name: 'Tool Use', symbolSize: 40},
          {name: 'Context Engineering', symbolSize: 45},
          {name: 'MCP', symbolSize: 35},
          {name: 'Multi-Agent', symbolSize: 35},
          {name: 'Claude', symbolSize: 30},
          {name: 'LangGraph', symbolSize: 25}
        ],
        links: [
          {source: 'Agent 架构', target: 'Tool Use'},
          {source: 'Agent 架构', target: 'Context Engineering'},
          {source: 'Agent 架构', target: 'Multi-Agent'},
          {source: 'RAG', target: 'Context Engineering'},
          {source: 'Tool Use', target: 'MCP'},
          {source: 'Multi-Agent', target: 'Tool Use'},
          {source: 'Claude', target: 'Agent 架构'},
          {source: 'LangGraph', target: 'Agent 架构'}
        ],
        lineStyle: {
          opacity: 0.9,
          width: 2,
          curveness: 0.1
        }
      }
    ]
  };
  
  // 应用配置
  myChart.setOption(option);
  
  // 响应式调整
  window.addEventListener('resize', function() {
    myChart.resize();
  });
</script>

## 主题标签

### 核心概念

- [Agent 架构设计](agent-architecture/core/agent-architecture.md)
- [Agent 框架理论](agent-architecture/core/agent-framework-theory.md)
- [Context Engineering](context-engineering/core/context-engineering.md)
- [Context Management](context-engineering/core/context-management.md)
- [RAG](rag/core/rag.md)
- [HyDE](rag/core/hyde.md)
- [Contextual Retrieval](rag/core/contextual-retrieval.md)
- [Tool Use](tool-use/core/tool-use.md)
- [Advanced Tool Use](tool-use/core/advanced-tool-use.md)
- [Multi-Agent](multi-agent/core/multi-agent.md)
- [MCP](mcp/core/mcp.md)

### 实践应用

- [Agent 框架实践](agent-architecture/practice/agent-framework-practice.md)
- [Building Effective Agents](agent-architecture/practice/building-effective-agents.md)
- [Effective Context Engineering](context-engineering/practice/effective-context-engineering.md)
- [Think Tool](tool-use/practice/think-tool.md)
- [Writing Effective Tools](tool-use/practice/writing-effective-tools.md)
- [Multi-Agent Research](multi-agent/practice/multi-agent-research.md)
- [MCP Code Execution](mcp/practice/mcp-code-execution.md)
- [MCP Deep Dive](mcp/practice/mcp-deep-dive.md)
- [Claude Agent SDK](claude/practice/claude-agent-sdk.md)
- [Claude Code Best Practices](claude/practice/claude-code-best-practices.md)

### 面试相关

- [面试 - Agent 架构](agent-architecture/interview/interview-agent-arch.md)
- [面试 - 上下文管理](context-engineering/interview/interview-context-mgmt.md)
- [面试 - HyDE](rag/interview/interview-hyde.md)

## 如何使用

- **核心概念**：提供每个领域的基础理论和关键概念
- **实践应用**：展示如何在实际项目中应用这些概念
- **面试相关**：针对技术面试的常见问题和解答

通过浏览这些概念，您可以深入了解 AI 代理、上下文管理、检索增强生成等前沿技术领域的核心知识。
```

- [ ] **步骤 2: 验证页面格式**

```bash
cd /workspace && mkdocs build --dry-run
```

- [ ] **步骤 3: 提交更改**

```bash
git add /workspace/docs/concepts/index.md
git commit -m "feat: 重构概念索引页面为概览页面"
```

### 任务 4: 删除不必要的索引文件

**Files:**
- Delete: 多个冗余索引文件

- [ ] **步骤 1: 删除冗余索引文件**

```bash
# 删除概念根目录的 _index.md
rm /workspace/docs/concepts/_index.md

# 删除 Agent Architecture 相关的冗余文件
rm /workspace/docs/concepts/agent-architecture/index.md
rm /workspace/docs/concepts/agent-architecture/core/index.md
rm /workspace/docs/concepts/agent-architecture/core/_index.md
rm /workspace/docs/concepts/agent-architecture/interview/index.md
rm /workspace/docs/concepts/agent-architecture/interview/_index.md
rm /workspace/docs/concepts/agent-architecture/practice/index.md
rm /workspace/docs/concepts/agent-architecture/practice/_index.md

# 删除 Claude 相关的冗余文件
rm /workspace/docs/concepts/claude/index.md
rm /workspace/docs/concepts/claude/practice/index.md
rm /workspace/docs/concepts/claude/practice/_index.md

# 删除 Context Engineering 相关的冗余文件
rm /workspace/docs/concepts/context-engineering/index.md
rm /workspace/docs/concepts/context-engineering/core/index.md
rm /workspace/docs/concepts/context-engineering/core/_index.md
rm /workspace/docs/concepts/context-engineering/interview/index.md
rm /workspace/docs/concepts/context-engineering/interview/_index.md
rm /workspace/docs/concepts/context-engineering/practice/index.md
rm /workspace/docs/concepts/context-engineering/practice/_index.md

# 删除 MCP 相关的冗余文件
rm /workspace/docs/concepts/mcp/index.md
rm /workspace/docs/concepts/mcp/core/index.md
rm /workspace/docs/concepts/mcp/core/_index.md
rm /workspace/docs/concepts/mcp/practice/index.md
rm /workspace/docs/concepts/mcp/practice/_index.md

# 删除 Multi-Agent 相关的冗余文件
rm /workspace/docs/concepts/multi-agent/index.md
rm /workspace/docs/concepts/multi-agent/core/index.md
rm /workspace/docs/concepts/multi-agent/core/_index.md
rm /workspace/docs/concepts/multi-agent/practice/index.md
rm /workspace/docs/concepts/multi-agent/practice/_index.md

# 删除 Other 相关的冗余文件
rm /workspace/docs/concepts/other/index.md
rm /workspace/docs/concepts/other/core/index.md
rm /workspace/docs/concepts/other/core/_index.md
rm /workspace/docs/concepts/other/practice/index.md
rm /workspace/docs/concepts/other/practice/_index.md

# 删除 RAG 相关的冗余文件
rm /workspace/docs/concepts/rag/index.md
rm /workspace/docs/concepts/rag/core/index.md
rm /workspace/docs/concepts/rag/core/_index.md
rm /workspace/docs/concepts/rag/interview/index.md
rm /workspace/docs/concepts/rag/interview/_index.md

# 删除 Tool Use 相关的冗余文件
rm /workspace/docs/concepts/tool-use/index.md
rm /workspace/docs/concepts/tool-use/core/index.md
rm /workspace/docs/concepts/tool-use/core/_index.md
rm /workspace/docs/concepts/tool-use/practice/index.md
rm /workspace/docs/concepts/tool-use/practice/_index.md
```

- [ ] **步骤 2: 验证删除结果**

```bash
find /workspace/docs/concepts -name "index.md" | grep -v "concepts/index.md"
```

- [ ] **步骤 3: 提交更改**

```bash
git add /workspace/docs/concepts/
git commit -m "feat: 删除冗余的索引文件"
```

### 任务 5: 改进分类 _index.md 页面

**Files:**
- Modify: [agent-architecture/_index.md](file:///workspace/docs/concepts/agent-architecture/_index.md)
- Modify: [context-engineering/_index.md](file:///workspace/docs/concepts/context-engineering/_index.md)
- Modify: [rag/_index.md](file:///workspace/docs/concepts/rag/_index.md)
- Modify: [tool-use/_index.md](file:///workspace/docs/concepts/tool-use/_index.md)
- Modify: [multi-agent/_index.md](file:///workspace/docs/concepts/multi-agent/_index.md)
- Modify: [mcp/_index.md](file:///workspace/docs/concepts/mcp/_index.md)
- Modify: [claude/_index.md](file:///workspace/docs/concepts/claude/_index.md)
- Modify: [other/_index.md](file:///workspace/docs/concepts/other/_index.md)

- [ ] **步骤 1: 改进 Agent Architecture 分类页面**

```markdown
---
title: "代理架构"
created: "2026-04-16"
type: section
tags: [agent, architecture]
---

# 代理架构

代理架构相关的核心概念、理论和实践指南。

## 核心概念

- [Agent 架构设计](core/agent-architecture.md) - 从传统开发到智能体的架构设计
- [Agent 框架理论](core/agent-framework-theory.md) - AI Agent 框架的理论基础

## 实践应用

- [Agent 框架实践](practice/agent-framework-practice.md) - AI Agent 框架的实践应用
- [构建有效 Agent](practice/building-effective-agents.md) - 如何构建高效的 AI Agent

## 面试相关

- [面试 - Agent 架构](interview/interview-agent-arch.md) - Agent 架构相关的面试问题

[:octicons-arrow-left-24: 返回概念概览](../index.md)
```

- [ ] **步骤 2: 改进 Context Engineering 分类页面**

```markdown
---
title: "上下文工程"
created: "2026-04-16"
type: section
tags: [context, engineering]
---

# 上下文工程

专注于代理上下文管理的核心概念、实践应用和面试相关内容。

## 核心概念

- [Context Engineering](core/context-engineering.md) - 上下文工程的核心概念
- [上下文管理](core/context-management.md) - 短期记忆与长期记忆管理

## 实践应用

- [有效上下文工程](practice/effective-context-engineering.md) - 如何进行有效的上下文工程

## 面试相关

- [面试 - 上下文管理](interview/interview-context-mgmt.md) - 上下文管理相关的面试问题

[:octicons-arrow-left-24: 返回概念概览](../index.md)
```

- [ ] **步骤 3: 改进 RAG 分类页面**

```markdown
---
title: "RAG"
created: "2026-04-16"
type: section
tags: [rag, retrieval]
---

# RAG

涵盖上下文检索、HYDE 技术和 RAG 核心概念，以及相关面试内容。

## 核心概念

- [RAG](core/rag.md) - 检索增强生成的核心概念
- [HyDE](core/hyde.md) - 假设文档嵌入与高级检索策略
- [上下文检索](core/contextual-retrieval.md) - 从分块到检索的完整流程

## 面试相关

- [面试 - HyDE](interview/interview-hyde.md) - HyDE 相关的面试问题

[:octicons-arrow-left-24: 返回概念概览](../index.md)
```

- [ ] **步骤 4: 改进 Tool Use 分类页面**

```markdown
---
title: "工具使用"
created: "2026-04-16"
type: section
tags: [tool, use]
---

# 工具使用

包括高级工具使用、工具使用基础概念和实践应用。

## 核心概念

- [Tool Use](core/tool-use.md) - 工具使用的基础概念
- [高级工具使用](core/advanced-tool-use.md) - 高级工具使用技巧

## 实践应用

- [Think Tool](practice/think-tool.md) - 让 Claude 在复杂工具使用场景中停下来思考
- [编写有效工具](practice/writing-effective-tools.md) - 为 Agent 编写高效工具

[:octicons-arrow-left-24: 返回概念概览](../index.md)
```

- [ ] **步骤 5: 改进 Multi-Agent 分类页面**

```markdown
---
title: "多智能体"
created: "2026-04-16"
type: section
tags: [multi, agent]
---

# 多智能体

探索多智能体系统的核心概念和实践应用。

## 核心概念

- [Multi-Agent](core/multi-agent.md) - 多智能体系统的核心概念

## 实践应用

- [多智能体研究](practice/multi-agent-research.md) - 如何构建多 Agent 研究系统

[:octicons-arrow-left-24: 返回概念概览](../index.md)
```

- [ ] **步骤 6: 改进 MCP 分类页面**

```markdown
---
title: "MCP"
created: "2026-04-16"
type: section
tags: [mcp]
---

# MCP

详细介绍 MCP 的核心概念、代码执行和深度解析。

## 核心概念

- [MCP](core/mcp.md) - 模型上下文协议的核心概念

## 实践应用

- [MCP 代码执行](practice/mcp-code-execution.md) - 通过 MCP 实现代码执行
- [MCP 深度解析](practice/mcp-deep-dive.md) - MCP 核心原理深度解析

[:octicons-arrow-left-24: 返回概念概览](../index.md)
```

- [ ] **步骤 7: 改进 Claude 分类页面**

```markdown
---
title: "Claude"
created: "2026-04-16"
type: section
tags: [claude]
---

# Claude

包含 Claude Agent SDK、代码最佳实践、桌面扩展和事后分析。

## 实践应用

- [Claude Agent SDK](practice/claude-agent-sdk.md) - 使用 Claude Agent SDK 构建 Agent
- [Claude 代码最佳实践](practice/claude-code-best-practices.md) - Agent 编程最佳实践
- [Claude 桌面扩展](practice/claude-desktop-extensions.md) - 桌面扩展的使用
- [Claude 事后分析](practice/claude-postmortem.md) - 三个近期问题的故障复盘

[:octicons-arrow-left-24: 返回概念概览](../index.md)
```

- [ ] **步骤 8: 改进 其他 分类页面**

```markdown
---
title: "其他"
created: "2026-04-16"
type: section
tags: [other]
---

# 其他

涵盖 LangGraph、提示注入、React 等核心概念，以及各种实践应用。

## 核心概念

- [LangGraph](core/langgraph.md) - 语言图的核心概念
- [提示注入](core/prompt-injection.md) - 系统提示词注入分析
- [ReAct](core/react.md) - 推理与行动框架

## 实践应用

- [Agent 技能](practice/agent-skills.md) - 用 Agent Skills 装备 Agent 应对真实世界
- [超越权限提示](practice/beyond-permission-prompts.md) - 让 Claude Code 更安全更自主
- [双记忆系统](practice/dual-memory-system.md) - 双层记忆系统与 Dream 管理知识文件
- [长期运行 Agent](practice/long-running-agents.md) - 构建长时间运行 Agent 的有效 Harness
- [斜杠命令](practice/slash-commands.md) - 自定义 Slash 命令 Hook 设计方案
- [SWE Bench](practice/swe-bench.md) - 用 Claude 3.5 Sonnet 提升 SWE-bench 成绩

[:octicons-arrow-left-24: 返回概念概览](../index.md)
```

- [ ] **步骤 9: 验证所有分类页面**

```bash
cd /workspace && mkdocs build --dry-run
```

- [ ] **步骤 10: 提交更改**

```bash
git add /workspace/docs/concepts/
git commit -m "feat: 改进分类页面内容"
```

### 任务 6: 测试与验证

**Files:**
- 所有相关文件

- [ ] **步骤 1: 构建并测试**

```bash
cd /workspace && mkdocs build
```

- [ ] **步骤 2: 启动开发服务器**

```bash
cd /workspace && mkdocs serve --dev-addr 0.0.0.0:8000
```

- [ ] **步骤 3: 验证导航功能**

- 访问 http://localhost:8000/concepts/ 查看新的概念概览页面
- 测试左侧导航栏的层级结构
- 验证面包屑导航是否正常工作
- 测试所有分类链接是否正确

- [ ] **步骤 4: 最终验证**

```bash
cd /workspace && mkdocs build --strict
```

- [ ] **步骤 5: 提交最终更改**

```bash
git add /workspace/docs/
git commit -m "feat: 完成概念页面与目录统一优化"
```

## 自我审查

1. **规范覆盖**：所有设计文档中的要求都已在实施计划中得到体现
2. **占位符检查**：没有使用任何占位符或未完成的内容
3. **类型一致性**：所有文件路径和命令都保持一致

## 执行选项

**计划完成并保存到 `docs/superpowers/plans/2026-04-16-concepts-navigation-unification-implementation.md`。两种执行选项：**

**1. 子代理驱动（推荐）** - 我为每个任务分配一个新的子代理，在任务之间进行审查，快速迭代

**2. 内联执行** - 在本次会话中使用 executing-plans 技能执行任务，批量执行并设置检查点

**选择哪种方法？**