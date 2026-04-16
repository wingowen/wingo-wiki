---
title: "架构概览"
created: 2025-06-26
updated: 2026-04-16
type: concept
tags: [mcp, agent, architecture]
sources: []
---

## 架构概览
Desktop Extension 是一个 ZIP 压缩包，包含本地 MCP 服务器以及一个 manifest.json，后者描述了 Claude Desktop 和其他支持桌面扩展的应用所需了解的一切信息。

```javascript
extension.mcpb (ZIP 压缩包)
├── manifest.json # 扩展元数据和配置
├── server/ # MCP 服务器实现
│   └── [服务器文件]
├── dependencies/ # 所有必需的包/库
└── icon.png # 可选：扩展图标

# 示例：Node.js 扩展
extension.mcpb
├── manifest.json # 必需：扩展元数据和配置
├── server/ # 服务器文件
│   └── index.js # 主入口文件
├── node_modules/ # 打包的依赖
├── package.json # 可选：NPM 包定义
└── icon.png # 可选：扩展图标

# 示例：Python 扩展
extension.mcpb (ZIP 文件)
├── manifest.json # 必需：扩展元数据和配置
├── server/ # 服务器文件
│   ├── main.py # 主入口文件
│   └── utils.py # 附加模块
├── lib/ # 打包的 Python 包
├── requirements.txt # 可选：Python 依赖列表
└── icon.png # 可选：扩展图标
```

Desktop Extension 中唯一必需的文件就是 manifest.json。Claude Desktop 处理所有复杂性：
- 内置运行时：我们随 Claude Desktop 一起附带 Node.js，消除了外部依赖
  - 自动更新：当有新版本可用时，扩展会自动更新
  - 安全密钥存储：API Key 等敏感配置存储在操作系统密钥链（OS Keychain）中

💡 术语解释：OS Keychain（操作系统密钥链）是操作系统提供的一种安全存储机制，用于保存密码、API Key 等敏感信息。macOS 使用 Keychain，Windows 使用 Credential Manager，Linux 使用 Secret Service API。

manifest 包含人类可读的信息（如名称、描述或作者）、功能声明（工具、提示词）、用户配置和运行时需求。大多数字段是可选的，因此最小版本非常简短，尽管在实际中，我们预期所有三种支持的扩展类型（Node.js、Python 和经典二进制/可执行文件）都会包含文件：

```javascript
{
  "mcpb_version": "0.1", // 此 manifest 遵循的 MCPB 规范版本
  "name": "my-extension", // 机器可读名称（用于 CLI、API）
  "version": "1.0.0", // 扩展的语义化版本
  "description": "A simple MCP extension", // 扩展功能的简要描述
  "author": { // 作者信息（必需）
    "name": "Extension Author" // 作者姓名（必需字段）
  },
  "server": { // 服务器配置（必需）
    "type": "node", // 服务器类型："node"、"python" 或 "binary"
    "entry_point": "server/index.js", // 主服务器文件的路径
    "mcp_config": { // MCP 服务器配置
      "command": "node", // 运行服务器的命令
      "args": [ // 传递给命令的参数
        "${__dirname}/server/index.js" // ${__dirname} 会被替换为扩展的目录
      ]
    }
  }
}
```

## 相关链接

[[mcp-deep-dive-modular|MCP 深度解析（模块化版本）]] | [[mcp-deep-dive-section-desktop-extensions-detail|桌面扩展：Claude Desktop 一键安装 MCP 服务器]] | [[mcp-deep-dive-section-code-execution|通过 MCP 实现代码执行]]
