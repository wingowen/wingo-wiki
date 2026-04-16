---
title: "2.3 Agent 框架代码实现"
created: 2026-04-15
updated: 2026-04-16
type: concept
tags: [agent, architecture, tool-use]
sources: [raw/articles/agent-framework-from-scratch.md]
---

## 2.3 Agent 框架代码实现

### 2.3.1 第一部分：Agent Loop 与 上下文

- 基础流程： LLM call → parse tool_calls → execute → append results to messages → loop or exit
- 安全设置：为while循环设置了一个迭代的安全上限：20 轮（MAX_TURNS=200）
- 使用全局变量message作为上下文的载体，累积系统提示词、用户消息、助手响应和工具结果

其中，变量message按如下规则更新：
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

### 2.3.2 第二部分：Tools 实现与注册

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

### 2.3.3 第三部分：System Prompt

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

## 相关链接

[[agent-framework-practice-modular|AI Agent 框架实践篇（模块化版本）]] | [[agent-framework-practice-section-elements|2.2 Agent 框架三大要素设计]] | [[agent-framework-practice-section-application|2.4 基于极简 Agent 框架的极简 Agent 应用]]
