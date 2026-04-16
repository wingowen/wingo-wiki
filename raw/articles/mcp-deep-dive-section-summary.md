---
title: "MCP 核心原理 - 总结"
created: 2025-06-26
updated: 2025-06-26
type: concept
tags: [anthropic, mcp]
sources: []
notion_id: 34367b21-8207-8199-83e2-4f68f4d7e0b7
---

# 总结

MCP 为 Agent 连接许多工具和系统提供了基础协议。然而，一旦连接了过多的服务器，工具定义和结果可能会消耗过多的 token，降低 Agent 的效率。

尽管这里的许多问题看起来很新颖——上下文管理、工具组合、状态持久化——但它们在软件工程中已有已知的解决方案。代码执行将这些成熟的模式应用于 Agent，让它们使用熟悉的编程构造来更高效地与 MCP 服务器交互。如果你实现了这种方法，我们鼓励你与 MCP 社区分享你的发现。

## 致谢

本文由 Adam Jones 和 Conor Kelly 撰写。感谢 Jeremy Fox、Jerome Swannack、Stuart Ritchie、Molly Vorwerck、Matt Samuels 和 Maggie Vo 对本文草稿的反馈。

---

> 译者注：本文介绍了 Anthropic 工程团队在 MCP 生态中发现的 token 效率问题及其解决方案。核心思路是将 MCP 服务器从"直接工具调用"模式转变为"代码 API"模式，让 Agent 通过编写代码来按需发现和调用工具。这一思路与 Cloudflare 提出的"Code Mode"不谋而合，体现了业界对 Agent 效率优化的共同探索。文中提到的渐进式披露、隐私保护令牌化、Skills 等概念，对于构建生产级 Agent 系统具有重要的参考价值。值得注意的是，代码执行方案需要配合沙箱化等安全措施使用，读者在实际应用时应充分评估安全风险。