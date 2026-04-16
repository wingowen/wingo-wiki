---
title: "三、写在后面的话"
created: 2026-04-15
updated: 2026-04-16
type: concept
tags: [agent, architecture, tool-use]
sources: [raw/articles/agent-framework-from-scratch.md]
---

## 三、写在后面的话

- 毫无疑问，当前极简版的AI Agent框架在程序健壮性、安全性、功能性（如流式输出）以及优雅性（如Tools注册）都有很大改进空间，但是不容否认的是它五脏俱全，简单清晰，可以帮助我们摒除那些复杂冗长的组件库，看清Agent的本质。
- 为什么需要极简？一方面是为了方便论述清楚Agent的关键点；另一方面是现实考量，代码库（本质也是文件）也将逐渐成为上下文工程的一部分，代码库越简单上下文越清晰（信息噪声越少），Agent则越智能。
- Agent框架之外，Agent应用之内，上下文工程是智能的核心（短期/长期记忆、主动/被动记忆、用户Session管理、动态RAG等等），也是Agent商业上应用的关键。框架提供基础工具，上下文工程提供环境，搭配商业领域的Skills，Agent就能发挥出巨大的潜力。

## 相关链接

[[agent-framework-practice-modular|AI Agent 框架实践篇（模块化版本）]] | [[agent-framework-practice-section-application|2.4 基于极简 Agent 框架的极简 Agent 应用]]
