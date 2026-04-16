---
title: "三个近期问题的故障复盘 | A postmortem of three recent issues"
created: 2025-09-17
updated: 2025-09-17
type: concept
tags: [anthropic]
sources: ["raw/articles/claude-postmortem.md"]
notion_id: 34267b21-8207-819b-b24d-e80f17fa0201
---

## 三个近期问题的故障复盘

> 原文：Anthropic Engineering | 发布日期：2025-09-17

---

### 事件概述

2025年8月至9月初，三个基础设施 Bug 间歇性降低了 Claude 响应质量。问题根源：Context Window 路由错误、输出损坏、XLA:TPU 编译错误。

**声明**：Anthropic 绝不会因需求量、时段或服务器负载降低模型质量。

### 三个 Bug 分析

**1. Context Window 路由错误**
8月5日引入，Sonnet 4 请求被错误路由到 1M Context Window 服务器。8月29日负载均衡变更后，影响扩大到 16%。

**2. 输出损坏**
8月25日 TPU 服务器错误配置，导致 token 生成时分配概率出错（英文提示出现泰语/中文字符）。

**3. Approximate top-k XLA:TPU 编译错误**
混合精度算术不匹配导致概率最高 token 有时从候选列表消失，行为随机不一致。

### 教训与改进

- 更敏感的评估方法，持续在生产系统运行评估
- 开发更快调试工具，不牺牲用户隐私
- 用户反馈至关重要（/bug 命令、"踩"按钮）
- 评估有噪声，需要多种方式互补验证

## 相关链接

[[anthropic]] | [[claude-code]]
