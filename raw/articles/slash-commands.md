---
title: "自定义 Slash 命令 Hook 设计方案"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent]
sources: []
notion_id: 34367b21-8207-81d2-afd3-cd5fe531fbc6
---

# 自定义 Slash 命令 Hook 设计方案

### 1. 问题分析

通过对项目代码的分析，发现当前项目存在以下问题：

1. 缺乏自定义 Slash 命令的扩展机制：当前的 slash 命令是硬编码在 command/builtin.py 中的，用户无法通过配置或插件的方式添加自定义命令。
1. Hook 系统不支持 Slash 命令：当前的 AgentHook 系统主要关注 agent 执行的生命周期，没有提供针对 slash 命令的特定 hook 点。
1. 命令路由硬编码：命令路由逻辑在 AgentLoop 初始化时硬编码注册，没有提供动态注册的机制。
### 2. 当前系统分析

#### 2.1 命令路由系统

当前的命令路由系统基于 CommandRouter 类，支持三种类型的命令：

- priority：优先级命令，在锁之外处理（如 /stop, /restart）
- exact：精确匹配命令，在锁内处理
- prefix：前缀匹配命令，按最长前缀优先
- interceptors：拦截器，作为最后的回退机制
命令注册通过 register_builtin_commands 函数硬编码注册到 CommandRouter 实例中。

#### 2.2 Hook 系统

当前的 hook 系统基于 AgentHook 类，支持以下生命周期事件：

- wants_streaming：是否需要流式输出
- before_iteration：每次迭代前
- on_stream：流式输出时
- on_stream_end：流式输出结束时
- before_execute_tools：执行工具前
- after_iteration：每次迭代后
- finalize_content：最终内容处理
#### 2.3 执行流程

1. 消息进入 AgentLoop._dispatch 方法
1. 检查是否为优先级命令，若是则直接处理
1. 否则创建任务执行 _process_message 方法
1. 在 _process_message 方法中：检查是否为 slash 命令，若是则通过 commands.dispatch 处理；否则进行正常的 agent 处理流程
### 3. 解决方案

#### 3.1 自定义 Slash 命令扩展机制

3.1.1 命令注册 API

添加一个公共 API 允许用户注册自定义 slash 命令：

```python
class AgentLoop:
    def register_command(self, cmd: str, handler: Handler, type: str = "exact"):
        """Register a custom slash command.
        
        Args:
            cmd: Command string (e.g. "/mycommand")
            handler: Command handler function
            type: Command type ("priority", "exact", "prefix")
        """
        if type == "priority":
            self.commands.priority(cmd, handler)
        elif type == "exact":
            self.commands.exact(cmd, handler)
        elif type == "prefix":
            self.commands.prefix(cmd, handler)
```

3.1.2 命令执行 Hook

扩展 AgentHook 类，添加针对 slash 命令的 hook 点：

```python
class AgentHook:
    # 现有方法...
    
    async def before_command(self, ctx: CommandContext) -> OutboundMessage | None:
        """Called before executing a slash command.
        
        Return an OutboundMessage to bypass the command execution.
        """
        return None
    
    async def after_command(self, ctx: CommandContext, result: OutboundMessage | None) -> OutboundMessage | None:
        """Called after executing a slash command.
        
        Can modify or replace the result.
        """
        return result
```

### 4. 实现建议

#### 4.1 命令注册机制

1. 扩展 AgentLoop 类：添加 register_command 和 unregister_command 方法
1. 修改 CommandRouter 类：添加 remove 方法支持命令注销
1. 添加命令元数据：支持命令描述、权限等元数据
### 5. 测试策略

#### 5.1 功能测试

- 测试自定义命令注册和执行
- 测试命令 hook 的调用
- 测试命令拦截器的功能
### 6. 预期效果

通过实施上述解决方案，预期可以：

1. 提高系统的可扩展性：允许用户通过多种方式添加自定义 slash 命令
1. 增强系统的灵活性：通过 hook 机制允许用户自定义命令的行为
1. 简化命令管理：通过配置和插件系统简化命令的注册和管理
1. 保持向后兼容性：确保现有命令和系统不受影响
### 7. 结论

当前项目不支持自定义 slash 命令的 hook，但通过实施上述设计方案，可以为系统添加灵活的命令扩展机制。这将使 nanobot 更加可定制，能够更好地适应不同用户的需求。

设计方案考虑了系统的现有架构，通过最小化的修改来实现功能扩展，同时保持系统的稳定性和可维护性。

## 相关链接

[[claude-code]] | [[tool-use]]
