# 层级导航实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现点击标题就能导航到下一级页面的功能，形成完整的层级导航链。

**Architecture:** 修改所有顶级分类的 index.md 文件和子分类的 _index.md 文件，将标题修改为指向子页面的链接。

**Tech Stack:** MkDocs, Markdown

---

## 文件结构

### 需要修改的文件：

#### 顶级分类页面：
- `/workspace/docs/concepts/agent-architecture/index.md`
- `/workspace/docs/concepts/context-engineering/index.md`
- `/workspace/docs/concepts/rag/index.md`
- `/workspace/docs/concepts/tool-use/index.md`
- `/workspace/docs/concepts/multi-agent/index.md`
- `/workspace/docs/concepts/mcp/index.md`
- `/workspace/docs/concepts/claude/index.md`
- `/workspace/docs/concepts/other/index.md`

#### 子分类页面：
- `/workspace/docs/concepts/agent-architecture/core/_index.md`
- `/workspace/docs/concepts/agent-architecture/interview/_index.md`
- `/workspace/docs/concepts/agent-architecture/practice/_index.md`
- `/workspace/docs/concepts/context-engineering/core/_index.md`
- `/workspace/docs/concepts/context-engineering/interview/_index.md`
- `/workspace/docs/concepts/context-engineering/practice/_index.md`
- `/workspace/docs/concepts/rag/core/_index.md`
- `/workspace/docs/concepts/rag/interview/_index.md`
- `/workspace/docs/concepts/tool-use/core/_index.md`
- `/workspace/docs/concepts/tool-use/practice/_index.md`
- `/workspace/docs/concepts/multi-agent/core/_index.md`
- `/workspace/docs/concepts/multi-agent/practice/_index.md`
- `/workspace/docs/concepts/mcp/core/_index.md`
- `/workspace/docs/concepts/mcp/practice/_index.md`
- `/workspace/docs/concepts/claude/practice/_index.md`
- `/workspace/docs/concepts/other/core/_index.md`
- `/workspace/docs/concepts/other/practice/_index.md`

---

## 任务分解

### 任务 1: 修改 Agent Architecture 相关页面

**Files:**
- Modify: `/workspace/docs/concepts/agent-architecture/index.md`
- Modify: `/workspace/docs/concepts/agent-architecture/core/_index.md`
- Modify: `/workspace/docs/concepts/agent-architecture/interview/_index.md`
- Modify: `/workspace/docs/concepts/agent-architecture/practice/_index.md`

- [ ] **Step 1: 修改 Agent Architecture 顶级页面**

```markdown
---
title: "代理架构"
created: "2026-04-16"
type: section
tags: [agent, architecture]
---

# [代理架构](core/)

代理架构相关的核心概念、理论和实践指南。
```

- [ ] **Step 2: 修改 Agent Architecture 核心概念页面**

```markdown
---
title: "核心概念"
created: "2026-04-16"
type: section
tags: [core]
---

# [核心概念](agent-architecture.md)

代理架构的核心概念和理论基础。
```

- [ ] **Step 3: 修改 Agent Architecture 面试相关页面**

```markdown
---
title: "面试相关"
created: "2026-04-16"
type: section
tags: [interview]
---

# [面试相关](interview-agent-arch.md)

代理架构相关的面试问题和解答。
```

- [ ] **Step 4: 修改 Agent Architecture 实践应用页面**

```markdown
---
title: "实践应用"
created: "2026-04-16"
type: section
tags: [practice]
---

# [实践应用](agent-framework-practice.md)

代理架构的实践应用和案例。
```

- [ ] **Step 5: 提交更改**

```bash
git add /workspace/docs/concepts/agent-architecture/index.md /workspace/docs/concepts/agent-architecture/core/_index.md /workspace/docs/concepts/agent-architecture/interview/_index.md /workspace/docs/concepts/agent-architecture/practice/_index.md
git commit -m "feat: add hierarchical navigation for agent-architecture"
```

### 任务 2: 修改 Context Engineering 相关页面

**Files:**
- Modify: `/workspace/docs/concepts/context-engineering/index.md`
- Modify: `/workspace/docs/concepts/context-engineering/core/_index.md`
- Modify: `/workspace/docs/concepts/context-engineering/interview/_index.md`
- Modify: `/workspace/docs/concepts/context-engineering/practice/_index.md`

- [ ] **Step 1: 修改 Context Engineering 顶级页面**

```markdown
---
title: "上下文工程"
created: "2026-04-16"
type: section
tags: [context, engineering]
---

# [上下文工程](core/)

上下文工程相关的核心概念、理论和实践指南。
```

- [ ] **Step 2: 修改 Context Engineering 核心概念页面**

```markdown
---
title: "核心概念"
created: "2026-04-16"
type: section
tags: [core]
---

# [核心概念](context-engineering.md)

上下文工程的核心概念和理论基础。
```

- [ ] **Step 3: 修改 Context Engineering 面试相关页面**

```markdown
---
title: "面试相关"
created: "2026-04-16"
type: section
tags: [interview]
---

# [面试相关](interview-context-mgmt.md)

上下文工程相关的面试问题和解答。
```

- [ ] **Step 4: 修改 Context Engineering 实践应用页面**

```markdown
---
title: "实践应用"
created: "2026-04-16"
type: section
tags: [practice]
---

# [实践应用](effective-context-engineering.md)

上下文工程的实践应用和案例。
```

- [ ] **Step 5: 提交更改**

```bash
git add /workspace/docs/concepts/context-engineering/index.md /workspace/docs/concepts/context-engineering/core/_index.md /workspace/docs/concepts/context-engineering/interview/_index.md /workspace/docs/concepts/context-engineering/practice/_index.md
git commit -m "feat: add hierarchical navigation for context-engineering"
```

### 任务 3: 修改 RAG 相关页面

**Files:**
- Modify: `/workspace/docs/concepts/rag/index.md`
- Modify: `/workspace/docs/concepts/rag/core/_index.md`
- Modify: `/workspace/docs/concepts/rag/interview/_index.md`

- [ ] **Step 1: 修改 RAG 顶级页面**

```markdown
---
title: "RAG"
created: "2026-04-16"
type: section
tags: [rag]
---

# [RAG](core/)

检索增强生成相关的核心概念、理论和实践指南。
```

- [ ] **Step 2: 修改 RAG 核心概念页面**

```markdown
---
title: "核心概念"
created: "2026-04-16"
type: section
tags: [core]
---

# [核心概念](contextual-retrieval.md)

RAG 的核心概念和理论基础。
```

- [ ] **Step 3: 修改 RAG 面试相关页面**

```markdown
---
title: "面试相关"
created: "2026-04-16"
type: section
tags: [interview]
---

# [面试相关](interview-hyde.md)

RAG 相关的面试问题和解答。
```

- [ ] **Step 4: 提交更改**

```bash
git add /workspace/docs/concepts/rag/index.md /workspace/docs/concepts/rag/core/_index.md /workspace/docs/concepts/rag/interview/_index.md
git commit -m "feat: add hierarchical navigation for rag"
```

### 任务 4: 修改 Tool Use 相关页面

**Files:**
- Modify: `/workspace/docs/concepts/tool-use/index.md`
- Modify: `/workspace/docs/concepts/tool-use/core/_index.md`
- Modify: `/workspace/docs/concepts/tool-use/practice/_index.md`

- [ ] **Step 1: 修改 Tool Use 顶级页面**

```markdown
---
title: "工具使用"
created: "2026-04-16"
type: section
tags: [tool, use]
---

# [工具使用](core/)

工具使用相关的核心概念、理论和实践指南。
```

- [ ] **Step 2: 修改 Tool Use 核心概念页面**

```markdown
---
title: "核心概念"
created: "2026-04-16"
type: section
tags: [core]
---

# [核心概念](advanced-tool-use.md)

工具使用的核心概念和理论基础。
```

- [ ] **Step 3: 修改 Tool Use 实践应用页面**

```markdown
---
title: "实践应用"
created: "2026-04-16"
type: section
tags: [practice]
---

# [实践应用](think-tool.md)

工具使用的实践应用和案例。
```

- [ ] **Step 4: 提交更改**

```bash
git add /workspace/docs/concepts/tool-use/index.md /workspace/docs/concepts/tool-use/core/_index.md /workspace/docs/concepts/tool-use/practice/_index.md
git commit -m "feat: add hierarchical navigation for tool-use"
```

### 任务 5: 修改 Multi-Agent 相关页面

**Files:**
- Modify: `/workspace/docs/concepts/multi-agent/index.md`
- Modify: `/workspace/docs/concepts/multi-agent/core/_index.md`
- Modify: `/workspace/docs/concepts/multi-agent/practice/_index.md`

- [ ] **Step 1: 修改 Multi-Agent 顶级页面**

```markdown
---
title: "多智能体"
created: "2026-04-16"
type: section
tags: [multi, agent]
---

# [多智能体](core/)

多智能体系统相关的核心概念、理论和实践指南。
```

- [ ] **Step 2: 修改 Multi-Agent 核心概念页面**

```markdown
---
title: "核心概念"
created: "2026-04-16"
type: section
tags: [core]
---

# [核心概念](multi-agent.md)

多智能体系统的核心概念和理论基础。
```

- [ ] **Step 3: 修改 Multi-Agent 实践应用页面**

```markdown
---
title: "实践应用"
created: "2026-04-16"
type: section
tags: [practice]
---

# [实践应用](multi-agent-research.md)

多智能体系统的实践应用和案例。
```

- [ ] **Step 4: 提交更改**

```bash
git add /workspace/docs/concepts/multi-agent/index.md /workspace/docs/concepts/multi-agent/core/_index.md /workspace/docs/concepts/multi-agent/practice/_index.md
git commit -m "feat: add hierarchical navigation for multi-agent"
```

### 任务 6: 修改 MCP 相关页面

**Files:**
- Modify: `/workspace/docs/concepts/mcp/index.md`
- Modify: `/workspace/docs/concepts/mcp/core/_index.md`
- Modify: `/workspace/docs/concepts/mcp/practice/_index.md`

- [ ] **Step 1: 修改 MCP 顶级页面**

```markdown
---
title: "MCP"
created: "2026-04-16"
type: section
tags: [mcp]
---

# [MCP](core/)

模型上下文协议相关的核心概念、理论和实践指南。
```

- [ ] **Step 2: 修改 MCP 核心概念页面**

```markdown
---
title: "核心概念"
created: "2026-04-16"
type: section
tags: [core]
---

# [核心概念](mcp.md)

MCP 的核心概念和理论基础。
```

- [ ] **Step 3: 修改 MCP 实践应用页面**

```markdown
---
title: "实践应用"
created: "2026-04-16"
type: section
tags: [practice]
---

# [实践应用](mcp-code-execution.md)

MCP 的实践应用和案例。
```

- [ ] **Step 4: 提交更改**

```bash
git add /workspace/docs/concepts/mcp/index.md /workspace/docs/concepts/mcp/core/_index.md /workspace/docs/concepts/mcp/practice/_index.md
git commit -m "feat: add hierarchical navigation for mcp"
```

### 任务 7: 修改 Claude 相关页面

**Files:**
- Modify: `/workspace/docs/concepts/claude/index.md`
- Modify: `/workspace/docs/concepts/claude/practice/_index.md`

- [ ] **Step 1: 修改 Claude 顶级页面**

```markdown
---
title: "Claude"
created: "2026-04-16"
type: section
tags: [claude]
---

# [Claude](practice/)

Claude 相关的核心概念、理论和实践指南。
```

- [ ] **Step 2: 修改 Claude 实践应用页面**

```markdown
---
title: "实践应用"
created: "2026-04-16"
type: section
tags: [practice]
---

# [实践应用](claude-agent-sdk.md)

Claude 的实践应用和案例。
```

- [ ] **Step 3: 提交更改**

```bash
git add /workspace/docs/concepts/claude/index.md /workspace/docs/concepts/claude/practice/_index.md
git commit -m "feat: add hierarchical navigation for claude"
```

### 任务 8: 修改 其他 相关页面

**Files:**
- Modify: `/workspace/docs/concepts/other/index.md`
- Modify: `/workspace/docs/concepts/other/core/_index.md`
- Modify: `/workspace/docs/concepts/other/practice/_index.md`

- [ ] **Step 1: 修改 其他 顶级页面**

```markdown
---
title: "其他"
created: "2026-04-16"
type: section
tags: [other]
---

# [其他](core/)

其他概念相关的核心概念、理论和实践指南。
```

- [ ] **Step 2: 修改 其他 核心概念页面**

```markdown
---
title: "核心概念"
created: "2026-04-16"
type: section
tags: [core]
---

# [核心概念](langgraph.md)

其他概念的核心概念和理论基础。
```

- [ ] **Step 3: 修改 其他 实践应用页面**

```markdown
---
title: "实践应用"
created: "2026-04-16"
type: section
tags: [practice]
---

# [实践应用](agent-skills.md)

其他概念的实践应用和案例。
```

- [ ] **Step 4: 提交更改**

```bash
git add /workspace/docs/concepts/other/index.md /workspace/docs/concepts/other/core/_index.md /workspace/docs/concepts/other/practice/_index.md
git commit -m "feat: add hierarchical navigation for other"
```

### 任务 9: 测试导航功能

**Files:**
- N/A

- [ ] **Step 1: 启动 MkDocs 服务器**

```bash
cd /workspace && mkdocs serve
```

- [ ] **Step 2: 测试导航链**

1. 访问 http://127.0.0.1:8000/concepts/
2. 点击 "Agent Architecture" 链接，应导航到 `/concepts/agent-architecture/`
3. 点击页面标题 "代理架构"，应导航到 `/concepts/agent-architecture/core/`
4. 点击页面标题 "核心概念"，应导航到 `/concepts/agent-architecture/core/agent-architecture/`
5. 对其他顶级分类重复上述测试

- [ ] **Step 3: 验证所有链接**

```bash
cd /workspace && python -c "
import os
import re

# 检查所有修改的文件中的链接
files_to_check = [
    # 顶级分类页面
    'docs/concepts/agent-architecture/index.md',
    'docs/concepts/context-engineering/index.md',
    'docs/concepts/rag/index.md',
    'docs/concepts/tool-use/index.md',
    'docs/concepts/multi-agent/index.md',
    'docs/concepts/mcp/index.md',
    'docs/concepts/claude/index.md',
    'docs/concepts/other/index.md',
    # 子分类页面
    'docs/concepts/agent-architecture/core/_index.md',
    'docs/concepts/agent-architecture/interview/_index.md',
    'docs/concepts/agent-architecture/practice/_index.md',
    'docs/concepts/context-engineering/core/_index.md',
    'docs/concepts/context-engineering/interview/_index.md',
    'docs/concepts/context-engineering/practice/_index.md',
    'docs/concepts/rag/core/_index.md',
    'docs/concepts/rag/interview/_index.md',
    'docs/concepts/tool-use/core/_index.md',
    'docs/concepts/tool-use/practice/_index.md',
    'docs/concepts/multi-agent/core/_index.md',
    'docs/concepts/multi-agent/practice/_index.md',
    'docs/concepts/mcp/core/_index.md',
    'docs/concepts/mcp/practice/_index.md',
    'docs/concepts/claude/practice/_index.md',
    'docs/concepts/other/core/_index.md',
    'docs/concepts/other/practice/_index.md'
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # 查找标题链接
        title_link = re.search(r'# \[(.*?)\]\((.*?)\)', content)
        if title_link:
            link_text = title_link.group(1)
            link_url = title_link.group(2)
            # 检查链接是否指向存在的文件或目录
            base_dir = os.path.dirname(file_path)
            target_path = os.path.join(base_dir, link_url)
            if os.path.exists(target_path) or os.path.exists(target_path + '.md'):
                print(f'✓ {file_path}: 链接 "{link_text}" 指向有效的路径')
            else:
                print(f'✗ {file_path}: 链接 "{link_text}" 指向无效的路径: {target_path}')
        else:
            print(f'✗ {file_path}: 未找到标题链接')
    else:
        print(f'✗ {file_path}: 文件不存在')
"
```

- [ ] **Step 4: 提交最终更改**

```bash
git add .
git commit -m "feat: complete hierarchical navigation implementation"
```

---

## 自我审查

1. **规范覆盖**：所有规范要求都已覆盖，包括：
   - 点击顶级分类标题导航到顶级分类页面
   - 点击顶级分类页面标题导航到子分类页面
   - 点击子分类页面标题导航到内容页面
   - 形成完整的导航链

2. **占位符检查**：无占位符，所有步骤都有具体的实现内容。

3. **类型一致性**：所有链接和文件路径都保持一致。

## 执行方式

**Plan complete and saved to `docs/superpowers/plans/2026-04-16-hierarchical-navigation-implementation.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**