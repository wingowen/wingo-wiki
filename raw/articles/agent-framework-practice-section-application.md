---
title: "2.4 基于极简 Agent 框架的极简 Agent 应用"
created: 2026-04-15
updated: 2026-04-16
type: concept
tags: [agent, architecture, tool-use]
sources: [raw/articles/agent-framework-from-scratch.md]
---

## 2.4 基于极简 Agent 框架的极简 Agent 应用

### 2.4.1 用户交互界面设计 - Python CLI REPL

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

### 2.4.2 DeepSeek 注册，获取 API Key

由于本文Agent框架的LLM Provider是基于DeepSeek实现的，所以需要获取DeepSeek模型（deepseek-chat模型）的API key才能使用。

- 注册： [https://platform.deepseek.com](https://platform.deepseek.com/)
- 获取API Keys： [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)

### 2.4.3 极简 Agent 应用体验

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

## 相关链接

[[agent-framework-practice-modular|AI Agent 框架实践篇（模块化版本）]] | [[agent-framework-practice-section-implementation|2.3 Agent 框架代码实现]] | [[agent-framework-practice-section-conclusion|三、写在后面的话]]
