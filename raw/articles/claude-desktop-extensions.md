---
title: "桌面扩展：Claude Desktop 一键安装 MCP 服务器 | Desktop Extensions"
created: 2025-06-26
updated: 2025-06-26
type: concept
tags: [anthropic]
sources: []
notion_id: 34267b21-8207-8197-b8ca-d8f11d3ca649
---

# 桌面扩展：Claude Desktop 一键安装 MCP 服务器 | Desktop Extensions
> 原文链接：Desktop Extensions: One-click MCP server installation for Claude Desktop
> 作者：Anthropic Engineering Team
> 发布日期：2025-06-26
> 翻译日期：2026-04-14
## 桌面扩展：Claude Desktop 一键安装 MCP 服务器 | Desktop Extensions
发布于 2025 年 6 月 26 日
Desktop Extensions（桌面扩展）让安装 MCP 服务器变得像点击按钮一样简单。本文将分享其技术架构以及创建优秀扩展的实用建议。
- 文件扩展名更新
去年当我们发布 Model Context Protocol（模型上下文协议，简称 MCP）时，我们看到开发者构建了令人惊叹的本地服务器，让 Claude 能够访问从文件系统到数据库的各种资源。但我们反复听到同样的反馈：安装过程太复杂了。用户需要安装开发者工具、手动编辑配置文件，还经常被依赖问题卡住。
今天，我们推出了 Desktop Extensions（桌面扩展）——一种全新的打包格式，让安装 MCP 服务器变得像点击按钮一样简单。
#### 解决 MCP 安装难题
本地 MCP 服务器为 Claude Desktop 用户解锁了强大的能力。它们可以与本地应用交互、访问私有数据、与开发工具集成——同时所有数据都保留在用户的机器上。然而，当前的安装流程造成了显著的障碍：
- 需要开发者工具：用户需要安装 Node.js、Python 或其他运行时（Runtime）
  - 手动配置：每个服务器都需要编辑 JSON 配置文件
  - 依赖管理：用户必须自行解决包冲突和版本不匹配问题
  - 缺乏发现机制：寻找有用的 MCP 服务器需要在 GitHub 上搜索
  - 更新复杂：保持服务器最新意味着需要手动重新安装
💡 术语解释：运行时（Runtime）是指运行程序所需的软件环境。例如，Node.js 就是 JavaScript 代码的运行时环境，Python 则是 Python 代码的运行时环境。
这些摩擦点意味着，尽管 MCP 服务器功能强大，但对非技术用户来说基本无法使用。
#### 介绍 Desktop Extensions
Desktop Extensions（.mcpb 文件）通过将整个 MCP 服务器——包括所有依赖——打包成一个可安装的包来解决这些问题。以下是用户体验的变化：
之前：
```javascript
# 先安装 Node.js
npm install -g @example/mcp-server
# 手动编辑 ~/.claude/claude_desktop_config.json
# 重启 Claude Desktop
# 祈祷它能正常工作
```
之后：
1. 下载一个 .mcpb 文件
  1. 双击用 Claude Desktop 打开
  1. 点击"安装"
就这样。不需要终端，不需要配置文件，没有依赖冲突。
### 架构概览
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
💡 术语解释：Semantic Versioning（语义化版本）是一种版本号命名规范，格式为 主版本号.次版本号.修订号（如 1.0.0）。主版本号变更表示不兼容的 API 修改，次版本号变更表示向后兼容的功能新增，修订号变更表示向后兼容的问题修复。
manifest 规范中有许多便捷选项，旨在简化本地 MCP 服务器的安装和配置。服务器配置对象可以以模板字面量（Template Literal）的形式定义用户自定义配置，同时支持平台特定的覆盖。扩展开发者可以详细定义他们希望从用户那里收集什么样的配置。
让我们看一个具体示例，了解 manifest 如何辅助配置。在下面的 manifest 中，开发者声明用户需要提供一个 api_key。在用户提供该值之前，Claude 不会启用该扩展，会自动将其保存在操作系统的密钥库中，并在启动服务器时将 ${user_config.api_key} 透明地替换为用户提供的值。类似地，${__dirname} 会被替换为扩展解压目录的完整路径。
```javascript
{
  "mcpb_version": "0.1",
  "name": "my-extension",
  "version": "1.0.0",
  "description": "A simple MCP extension",
  "author": {
    "name": "Extension Author"
  },
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {
        "API_KEY": "${user...key}"
      }
    }
  },
  "user_config": {
    "api_key": {
      "type": "string",
      "title": "API Key",
      "description": "Your API key for authentication",
      "sensitive": true,
      "required": true
    }
  }
}
```
💡 举例说明：${user_config.api_key} 是一个模板变量。当 Claude Desktop 启动服务器时，它会自动将这个占位符替换为用户在配置界面中实际输入的 API Key 值。这样开发者就不需要在代码中硬编码敏感信息。
一个包含大部分可选字段的完整 manifest.json 可能如下所示：
```javascript
{
  "mcpb_version": "0.1",
  "name": "My MCP Extension",
  "display_name": "My Awesome MCP Extension",
  "version": "1.0.0",
  "description": "A brief description of what this extension does",
  "long_description": "A detailed description that can include multiple paragraphs explaining the extension's functionality, use cases, and features. It supports basic markdown.",
  "author": {
    "name": "Your Name",
    "email": "yourname@example.com",
    "url": "https://your-website.com"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/your-username/my-mcp-extension"
  },
  "homepage": "https://example.com/my-extension",
  "documentation": "https://docs.example.com/my-extension",
  "support": "https://github.com/your-username/my-mcp-extension/issues",
  "icon": "icon.png",
  "screenshots": [
    "assets/screenshots/screenshot1.png",
    "assets/screenshots/screenshot2.png"
  ],
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {
        "ALLOWED_DIRECTORIES": "${user_config.allowed_directories}"
      }
    }
  },
  "tools": [
    {
      "name": "search_files",
      "description": "Search for files in a directory"
    }
  ],
  "prompts": [
    {
      "name": "poetry",
      "description": "Have the LLM write poetry",
      "arguments": ["topic"],
      "text": "Write a creative poem about the following topic: ${arguments.topic}"
    }
  ],
  "tools_generated": true,
  "keywords": ["api", "automation", "productivity"],
  "license": "MIT",
  "compatibility": {
    "claude_desktop": ">=1.0.0",
    "platforms": ["darwin", "win32", "linux"],
    "runtimes": {
      "node": ">=16.0.0"
    }
  },
  "user_config": {
    "allowed_directories": {
      "type": "directory",
      "title": "Allowed Directories",
      "description": "Directories the server can access",
      "multiple": true,
      "required": true,
      "default": ["${HOME}/Desktop"]
    },
    "api_key": {
      "type": "string",
      "title": "API Key",
      "description": "Your API key for authentication",
      "sensitive": true,
      "required": false
    },
    "max_file_size": {
      "type": "number",
      "title": "Maximum File Size (MB)",
      "description": "Maximum file size to process",
      "default": 10,
      "min": 1,
      "max": 100
    }
  }
}
```
要查看扩展和 manifest 的示例，请参阅 MCPB 仓库中的示例。
manifest.json 中所有必需和可选字段的完整规范可以在我们的开源工具链中找到。
#### 构建你的第一个扩展
让我们逐步将一个现有的 MCP 服务器打包为 Desktop Extension。我们将以一个简单的文件系统服务器为例。
首先，为你的服务器初始化一个 manifest：
```javascript
npx @anthropic-ai/mcpb init
```
这个交互式工具会询问关于你服务器的信息，并生成一个完整的 manifest.json。如果你想快速生成最基本的 manifest.json，可以使用 --yes 参数运行命令。
如果你的服务器需要用户输入（如 API Key 或允许访问的目录），请在 manifest 中声明：
```javascript
"user_config": {
  "allowed_directories": {
    "type": "directory",
    "title": "Allowed Directories",
    "description": "Directories the server can access",
    "multiple": true,
    "required": true,
    "default": ["${HOME}/Documents"]
  }
}
```
Claude Desktop 将会：
- 显示用户友好的配置界面
  - 在启用扩展之前验证输入
  - 安全存储敏感值
  - 根据开发者配置，将配置作为参数或环境变量传递给你的服务器
在下面的示例中，我们将用户配置作为环境变量传递，但它也可以作为参数传递。
```javascript
"server": {
  "type": "node",
  "entry_point": "server/index.js",
  "mcp_config": {
    "command": "node",
    "args": ["${__dirname}/server/index.js"],
    "env": {
      "ALLOWED_DIRECTORIES": "${user_config.allowed_directories}"
    }
  }
}
```
将所有内容打包成一个 .mcpb 文件：
```javascript
npx @anthropic-ai/mcpb pack
```
此命令会：
1. 验证你的 manifest
  1. 生成 .mcpb 压缩包
将你的 .mcpb 文件拖入 Claude Desktop 的设置窗口。你会看到：
- 关于你扩展的人类可读信息
  - 所需的权限和配置
  - 一个简单的"安装"按钮
#### 高级功能
扩展可以适配不同的操作系统：
```javascript
"server": {
  "type": "node",
  "entry_point": "server/index.js",
  "mcp_config": {
    "command": "node",
    "args": ["${__dirname}/server/index.js"],
    "platforms": {
      "win32": {
        "command": "node.exe",
        "env": {
          "TEMP_DIR": "${TEMP}"
        }
      },
      "darwin": {
        "env": {
          "TEMP_DIR": "${TMPDIR}"
        }
      }
    }
  }
}
```
💡 术语解释：darwin 是 macOS 的内部系统名称（源自 Darwin 操作系统），win32 是 Windows 平台的标识符（即使 64 位系统也使用此名称），linux 则是 Linux 平台的标识符。
使用模板字面量处理运行时值：
- ${__dirname}：扩展的安装目录
  - ${user_config.key}：用户提供的配置
  - ${HOME}, ${TEMP}：系统环境变量
帮助用户提前了解扩展的能力：
```javascript
"tools": [
  {
    "name": "read_file",
    "description": "Read contents of a file"
  }
],
"prompts": [
  {
    "name": "code_review",
    "description": "Review code for best practices",
    "arguments": ["file_path"]
  }
]
```
#### 扩展目录
我们正在推出一个内置于 Claude Desktop 的精选扩展目录。用户可以浏览、搜索并一键安装——无需搜索 GitHub 或审查代码。
虽然我们预期 Desktop Extension 规范以及 Claude 在 macOS 和 Windows 上的实现会随时间不断演进，但我们期待看到扩展以各种富有创意的方式扩展 Claude 的能力。
提交你的扩展：
1. 确保它遵循提交表单中的指南
  1. 在 Windows 和 macOS 上进行跨平台测试
  1. 提交你的扩展
  1. 我们的团队将进行质量和安全审查
#### 构建开放生态系统
我们致力于围绕 MCP 服务器构建开放生态系统，并相信其被多个应用和服务广泛采用的能力造福了整个社区。秉承这一承诺，我们将 Desktop Extension 规范、工具链以及 Claude 在 macOS 和 Windows 上用于实现桌面扩展支持所使用的 Schema（模式定义）和关键函数进行开源。我们希望 MCPB 格式不仅能让本地 MCP 服务器在 Claude 中更具可移植性，也能在其他 AI 桌面应用中发挥作用。
我们正在开源的内容包括：
- 完整的 MCPB 规范
  - 打包和验证工具

## 相关链接

[[mcp]] | [[claude-code]]
