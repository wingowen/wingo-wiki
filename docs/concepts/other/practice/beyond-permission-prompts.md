---
title: "超越权限提示：让 Claude Code 更安全更自主 | Beyond permission prompts"
created: 2025-10-20
updated: 2025-10-20
type: concept
tags: [anthropic]
sources: [../raw/articles/beyond-permission-prompts.md]
notion_id: 34267b21-8207-81cb-b299-d66221d93419
---

Anthropic 为 Claude Code 推出的沙箱化（Sandboxing）技术，通过**文件系统隔离**和**网络隔离**两个边界，大幅减少权限提示（内部测试减少 84%），同时提升安全性。

沙箱化基于 OS 级原语（Linux bubblewrap、MacOS seatbelt）实现：文件系统隔离限制 Agent 只读写工作目录；网络隔离通过 Unix Domain Socket 代理限制连接域名。两者缺一不可——缺少任一都会让提示注入攻击有逃逸路径。

该沙箱运行时已开源，Claude Code on the web 也采用相同架构，通过代理服务处理 git 凭据，确保敏感信息永不存入沙箱。

## 核心要点

- **双重隔离**：文件系统隔离 + 网络隔离必须同时启用，缺一不可
- **OS 级原语**：使用 Linux bubblewrap 和 MacOS seatbelt 在内核层面强制执行
- **权限大幅减少**：沙箱化技术安全地将权限提示减少 84%
- **Git 安全**：Claude Code on the web 通过代理服务 + 范围限定凭据保护 git 访问
- **开源可用**：sandbox-runtime 已开源，其他团队可复用此安全基础设施

## 相关链接

[claude-code](../../entities/claude-code.md) | [tool-use](../../tool-use/core/tool-use.md)
