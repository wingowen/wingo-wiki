---
title: "AI Agent 框架实践篇 | Agent Framework Practice"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [agent, architecture, tool-use]
sources: [raw/articles/agent-framework-from-scratch.md]
---

## AI Agent 框架实践篇

承接上篇：Agent框架设计的核心是在Agent Loop这个While循环中设计如何管理上下文，本篇即围绕这个核心论点展开。

2.1 Agent 框架架构图一览

```plain text
┌─────────────────────────────────────────────────────────────────────┐
│                User Interface（CLI REPL Layer ）                     │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────────┐ │
│  │  User Input  │   │    Exit/     │   │   Message History        │ │
│  │   Handler    │   │   Clear Cmd  │   │   Management             │ │
│  └──────┬───────┘   └──────────────┘   └──────────────────────────┘ │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Agent Loop Core                          │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │   │
│  │  │   LLM Call   │───▶│  Tool Call   │───▶│   Tool Exec  │   │   │
│  │  │  (DeepSeek)  │    │   Parser     │    │   Engine     │   │   │
│  │  └──────────────┘    └──────────────┘    └──────────────┘   │   │
│  │         │                                    │              │   │
│  │         │◀──────────────────────────────────┘              │   │
│  │         │ (Tool Results Feedback)                          │   │
│  │         ▼                                                   │   │
│  │  ┌──────────────┐    ┌──────────────┐                     │   │
│  │  │  Response    │───▶│   Context    │                     │   │
│  │  │  Formatter   │    │   Manager    │                     │   │
│  │  └──────────────┘    └──────────────┘                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                             │                                     │
│                             ▼                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                  Tools Registry (TOOLS)                    │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │   │
│  │  │ shell_  │ │ file_   │ │ file_   │ │ python_ │          │   │
│  │  │  exec   │ │  read   │ │  write  │ │  exec   │          │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │   │
│  │      │            │            │            │              │   │
│  │      ▼            ▼            ▼            ▼              │   │
│  │  [Function]   [Function]   [Function]   [Function]        │   │
│  │  [Schema]     [Schema]     [Schema]     [Schema]          │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

再review一下工作流：

```plain text
初始上下文（系统提示词+用户请求）
    ↓[agent loop开始]
    ↓agent读取上下文 → 思考 → 决定行动
    ↓执行工具/行动 → 获得结果
    ↓结果追加到上下文
    ↓[循环继续或结束]
```

2.2 Agent 框架三大要素设计

2.2.1 LLM Call

采用极简设计，以DeepSeek模型示例说明

- LLM Provider：使用DeepSeek deepseek-chat 模型
- LLM Call API：使用标准化OpenAI SDK
为保证代码的最大可读性，这里使用同步非流式调用。

2.2.2 Tools Call

采用极简的工具集，操作对象包含文件、Shell和Python代码执行

1）Tools 实现：总共支持4个工具函数

- shell_exec：执行shell命令并返回输出
- file_read：读取文件内容
- file_write：写入文件内容（自动创建目录）
- python_exec：在子进程中执行Python代码并返回输出
2）Tools 注册：这里选择的是手动维护字典映射的方式 name → (function, OpenAI function schema) ，这一步是为了解析llm call 的response时可以根据name匹配需要具体执行哪个tool

Tools 的定义遵循的是 OpenAI Function Calling 的标准格式（也称 OpenAI Tools API schema）

2.2.3 Context Engineering

- System Prompt：极简系统提示词，告知LLM可用工具和ReAct思考方式
- 用户Session管理：使用messages 列表方式（OpenAI chat 格式），它是核心状态，累积系统提示词、用户消息、助手响应和工具结果
2.3 Agent 框架代码实现

2.3.1 第一部分：Agent Loop 与 上下文

- 基础流程： LLM call → parse tool_calls → execute → append results to messages → loop or exit
- 安全设置：为while循环设置了一个迭代的安全上限：20 轮（MAX_TURNS=200）
- 使用全局变量message作为上下文的载体，累积系统提示词、用户消息、助手响应和工具结果
其中，变量message按如下规则更新

- 使用System Prompt初始化：{"role": "system", "content": system_prompt}
- 追增User Message：{"role": "user", "content": user_message}
- 追加Tool Results：{"role": "tool", "content": result}
```python
# ============================================================
# Agent Loop — 核心
# ============================================================

MAX_TURNS = 20

def agent_loop(user_message: str, messages: list, client: OpenAI) -> str:
    """
    Agent Loop：while 循环驱动 LLM 推理与工具调用。
    流程：
      1. 将用户消息追加到 messages
      2. 调用 LLM
      3. 若 LLM 返回 tool_calls → 逐个执行 → 结果追加到 messages → 继续循环
      4. 若 LLM 直接返回文本（无 tool_calls）→ 退出循环，返回文本
      5. 安全上限 MAX_TURNS 轮
    """
    messages.append({"role": "user", "content": user_message})
    tool_schemas = [t["schema"] for t in TOOLS.values()]

    for turn in range(1, MAX_TURNS + 1):
        # --- LLM Call ---
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tool_schemas,
        )
        choice = response.choices[0]
        assistant_msg = choice.message

        # 将 assistant 消息追加到上下文
        messages.append(assistant_msg.model_dump())

        # --- 终止条件：无 tool_calls ---
        if not assistant_msg.tool_calls:
            return assistant_msg.content or ""

        # --- 执行每个 tool_call ---
        for tool_call in assistant_msg.tool_calls:
            name = tool_call.function.name
            raw_args = tool_call.function.arguments
            print(f"  [tool] {name}({raw_args})")

            # 解析参数并调用工具
            try:
                args = json.loads(raw_args)
            except json.JSONDecodeError:
                args = {}

            tool_entry = TOOLS.get(name)
            if tool_entry is None:
                result = f"[error] unknown tool: {name}"
            else:
                result = tool_entry["function"](**args)

            # 将工具结果追加到上下文
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    return "[agent] reached maximum turns, stopping."
```

注：这里使用的模型为deepseek-chat，主要考量因素是模型支持Tool Calls，并且完全兼容OpenAI的SDK。

2.3.2 第二部分：Tools 实现与注册

这里主要实现四个工具函数: shell_exec, file_read, file_write, python_exec

```python
# ============================================================
# Tools 实现 — 4 个工具函数
# ============================================================

def shell_exec(command: str) -> str:
    """执行 shell 命令并返回 stdout + stderr。"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
        if result.stderr:
            output += "\n[stderr]\n" + result.stderr
        if result.returncode != 0:
            output += f"\n[exit code: {result.returncode}]"
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return "[error] command timed out after 30s"
    except Exception as e:
        return f"[error] {e}"

def file_read(path: str) -> str:
    """读取文件内容。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"[error] {e}"

def file_write(path: str, content: str) -> str:
    """将内容写入文件（自动创建父目录）。"""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"OK — wrote {len(content)} chars to {path}"
    except Exception as e:
        return f"[error] {e}"

def python_exec(code: str) -> str:
    """在子进程中执行 Python 代码并返回输出。"""
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
        if result.stderr:
            output += "\n[stderr]\n" + result.stderr
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return "[error] execution timed out after 30s"
    except Exception as e:
        return f"[error] {e}"
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
```

工具实现好了下一步就是注册，方便Agent Loop可以根据LLM的返回结果执行具体的工具方法（实际上就是一个字典映射name → {function, OpenAI schema}）

```python
# ============================================================
# Tools 注册 — name → (function, OpenAI function schema)
# ============================================================

TOOLS = {
    "shell_exec": {
        "function": shell_exec,
        "schema": {
            "type": "function",
            "function": {
                "name": "shell_exec",
                "description": "Execute a shell command and return its output.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command to execute.",
                        }
                    },
                    "required": ["command"],
                },
            },
        },
    },
    "file_read": {
        "function": file_read,
        "schema": {
            "type": "function",
            "function": {
                "name": "file_read",
                "description": "Read the contents of a file at the given path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Absolute or relative file path.",
                        }
                    },
                    "required": ["path"],
                },
            },
        },
    },
    "file_write": {
        "function": file_write,
        "schema": {
            "type": "function",
            "function": {
                "name": "file_write",
                "description": "Write content to a file (creates parent directories if needed).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Absolute or relative file path.",
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write.",
                        },
                    },
                    "required": ["path", "content"],
                },
            },
        },
    },
    "python_exec": {
        "function": python_exec,
        "schema": {
            "type": "function",
            "function": {
                "name": "python_exec",
                "description": "Execute Python code in a subprocess and return its output.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Python source code to execute.",
                        }
                    },
                    "required": ["code"],
                },
            },
        },
    },
}
```

Tools 的定义遵循的是 OpenAI Function Calling 的标准格式（也称 OpenAI Tools API schema）。

具体来说，Agent 中每个工具的 schema 字段的结构如下：

```json
{
    "type": "function",
    "function": {
        "name": "...",
        "description": "...",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "..."
                }
            },
            "required": ["param1"]
        }
    }
}
```

2.3.3 第三部分：System Prompt

这里定义System Prompt，每一次与LLM交互都需要带上它。

```python
# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """You are a helpful AI assistant with access to the following tools:

1. shell_exec — run shell commands
2. file_read — read file contents
3. file_write — write content to files
4. python_exec — execute Python code

When you need to use a tool, respond with a tool call in the appropriate format.
Think step by step. First reason about what to do, then take action."""
```

明确告知：你是一个AI助手，当需要的时候可以使用哪些工具。

至此一个极简的Agent框架就此实现完成，单文件搞定，全部代码279行。

2.4 基于极简 Agent 框架的极简 Agent 应用

2.4.1 用户交互界面设计 - Python CLI REPL

框架实现完成之后，距离Agent应用就剩下最后一个用户交互界面了。

避免增加读者认知负担，从极简思想出发，这里使用Python CLI REPL 即Python的交互式命令行作为Agent的入口：

```python
def main():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: please set DEEPSEEK_API_KEY environment variable.")
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    messages: list = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Agent CLI (type 'exit' to quit)\n")

    while True:
        try:
            user_input = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break
        if user_input.lower() == "clear":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Session cleared.\n")
            continue

        print()
        response = agent_loop(user_input, messages, client)
        print(f"Agent > {response}\n")


if __name__ == "__main__":
    main()
```

2.4.2 DeepSeek 注册，获取 API Key

由于本文Agent框架的LLM Provider是基于DeepSeek实现的，所以需要获取DeepSeek模型（deepseek-chat模型）的API key才能使用。

- 注册： [https://platform.deepseek.com](https://platform.deepseek.com/)
- 获取API Keys： [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
2.4.3 极简 Agent 应用体验

使用之前设置API key

```bash
export DEEPSEEK_API_KEY="***"
```

先来问候一下：

输出的基本上是System Prompt中的内容，符合预期。

1）第1个问题

帮我查一下当前目录都有哪些文件

2）第2个问题

让它执行一个统计任务：帮我统计下当前目录下的代码行数以及token数

可以看到Agent Loop里在持续地调用Tools、写代码以及执行代码

最终的统计结果：

做完任务，使用exit命令退出当前session

可以看到实现的Agent应用，虽然实现极简，但是功能可以一点不简单（当Agent拥有文件读写权限，外加Shell工具以及代码生成与执行权限，它在本机上真的可以"为所欲为"）。

要知道OpenClaw的底层Agent Core（Pi Agent）的Tools层也是有且仅包含四个工具方法：读文件（Read）、写文件（Write）、编辑文件（Edit）、命令行（Shell），其他的丰富且强大能力均靠事件机制及Skills扩展而来。

三、写在后面的话

- 毫无疑问，当前极简版的AI Agent框架在程序健壮性、安全性、功能性（如流式输出）以及优雅性（如Tools注册）都有很大改进空间，但是不容否认的是它五脏俱全，简单清晰，可以帮助我们摒除那些复杂冗长的组件库，看清Agent的本质。
- 为什么需要极简？一方面是为了方便论述清楚Agent的关键点；另一方面是现实考量，代码库（本质也是文件）也将逐渐成为上下文工程的一部分，代码库越简单上下文越清晰（信息噪声越少），Agent则越智能。
- Agent框架之外，Agent应用之内，上下文工程是智能的核心（短期/长期记忆、主动/被动记忆、用户Session管理、动态RAG等等），也是Agent商业上应用的关键。框架提供基础工具，上下文工程提供环境，搭配商业领域的Skills，Agent就能发挥出巨大的潜力。

## 相关链接

[[ai-agent]] | [[agent-architecture]] | [[tool-use]]
