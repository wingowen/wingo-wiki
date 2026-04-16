---
title: "双层记忆系统与 Dream 管理知识文件的具体实现分析 | Dual Memory System"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [memory]
sources: ["raw/articles/dual-memory-system.md"]
notion_id: 34267b21-8207-81a2-b887-ec73bb83404c
---

## 双层记忆系统

### 系统架构

nanobot 采用双层记忆系统，由**短期记忆**（会话消息）和**长期记忆**（知识文件）组成，通过 Consolidator 和 Dream 两个核心组件实现记忆的流动和管理。

### 记忆文件结构

- **MEMORY.md**：系统级记忆，存储核心指令、配置和系统信息
- **SOUL.md**：灵魂文件，存储核心身份、价值观和长期目标
- **USER.md**：用户档案，存储用户相关信息和偏好
- **history.jsonl**：追加式历史总结，由 Consolidator 生成

### 记忆流通过程

1. **会话消息产生** → 2. **Consolidator 处理**：轻量级压缩，生成历史总结追加到 history.jsonl → 3. **Dream 分析**：定期或手动触发，分析 history.jsonl 与长期记忆的差异 → 4. **Dream 编辑**：手术式编辑长期记忆文件 → 5. **GitStore 版本控制**：自动提交变更，记录记忆演化历史

### Dream 两阶段处理

**第一阶段（分析）**：读取 history.jsonl 和长期记忆文件，识别需要更新的记忆内容。

**第二阶段（编辑）**：根据分析结果生成编辑指令，执行精确的文件编辑，保持记忆连贯性。

### 技术特性

- 分层记忆：短期会话与长期知识分离
- 智能分析：识别记忆差异和更新需求
- 手术式编辑：精确修改记忆文件，保持结构完整
- 版本控制：GitStore 记录记忆演化历史
- 透明可控：用户可手动触发和查看记忆状态

## 相关链接

[[context-engineering]] | [[ai-agent]]
