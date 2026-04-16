---
title: "自定义 Slash 命令 Hook 设计方案 | Slash Commands"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent]
sources: [../raw/articles/slash-commands.md]
notion_id: 34367b21-8207-81d2-afd3-cd5fe531fbc6
---

本文分析了 nanobot 项目中自定义 Slash 命令扩展机制的设计方案。当前系统存在三个问题：命令硬编码在 builtin.py 中无法扩展、Hook 系统不支持 slash 命令、命令路由无动态注册机制。

解决方案是为 AgentLoop 添加 `register_command` 和 `unregister_command` 方法，支持 priority/exact/prefix 三种命令类型。同时扩展 AgentHook 类，添加 `before_command` 和 `after_command` hook 点。

该方案通过最小化修改实现功能扩展，保持向后兼容性，使 nanobot 更具可定制性。

## 核心要点

- **命令注册 API**：`AgentLoop.register_command(cmd, handler, type)` 支持动态注册
- **命令类型**：priority（锁外处理）、exact（锁内精确匹配）、prefix（前缀匹配）
- **Hook 扩展**：添加 `before_command` 和 `after_command` 生命周期 hook
- **向后兼容**：现有命令和系统不受影响
- **路由系统**：基于 CommandRouter，支持拦截器作为最后回退机制

## 相关链接

[[claude-code]] | [[tool-use]]
