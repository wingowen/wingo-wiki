---
title: "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩 - 工具型 Agent"
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [anthropic, benchmark, evaluation]
sources: []
---

# 工具型 Agent

我们在为升级版 Claude 3.5 Sonnet 创建优化的 Agent 脚手架时，设计理念是尽可能将控制权交给语言模型本身，同时保持脚手架的最小化。该 Agent 包含一个 Prompt、一个用于执行 bash 命令的 Bash Tool（Bash 工具）和一个用于查看和编辑文件及目录的 Edit Tool（编辑工具）。我们持续采样，直到模型自行决定完成，或超出其 200k 上下文长度。这种脚手架允许模型运用自身判断力来决定如何推进问题，而非被硬编码为特定的模式或工作流。

Prompt 为模型概述了建议的处理方法，但对于此任务而言并不过长或过于详细。模型可以自由选择如何在各步骤之间过渡，而非遵循严格的离散转换。如果你不敏感于 Token 消耗，显式鼓励模型生成长篇回复会有所帮助。

以下代码展示了我们 Agent 脚手架中的 Prompt：

```javascript
<uploading_files>
{location}
</uploaded_files>
I've uploaded a python code repository in the directory {location} (not in /tmp/inputs). Consider the following PR description:

<pr_description>
{pr_description}
</pr_description>

Can you help me implement the necessary changes to the repository so that the requirements specified in the <pr_description> are met?
I've already taken care of all changes to any of the test files described in the <pr_description>. This means you DON'T have to modify the testing logic or any of the tests in any way!

Your task is to make the minimal changes to non-tests files in the {location} directory to ensure the <pr_description> is satisfied.

Follow these steps to resolve the issue:
1. As a first step, it might be a good idea to explore the repo to familiarize yourself with its structure.
2. Create a script to reproduce the error and execute it with `python <filename.py>` using the BashTool, to confirm the error
3. Edit the sourcecode of the repo to resolve the issue
4. Rerun your reproduce script and confirm that the error is fixed!
5. Think about edgecases and make sure your fix handles them as well

Your thinking should be thorough and so it's fine if it's very long.
```

模型的第一个工具用于执行 Bash 命令。其 Schema（模式定义）很简单，只需接收要在环境中运行的命令。然而，工具的描述（Description）更为重要。它包含面向模型的更详细指令，包括输入转义、无互联网访问以及如何在后台运行命令等。

接下来，我们展示 Bash Tool 的规范：

```javascript
{
 "name": "bash",
 "description": "Run commands in a bash shell\n\n* When invoking this tool, the contents of the \"command\" parameter does NOT need to be XML-escaped.\n\n* You don't have access to the internet via this tool.\n\n* You do have access to a mirror of common linux and python packages via apt and pip.\n\n* State is persistent across command calls and discussions with the user.\n\n* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n\n* Please avoid commands that may produce a very large amount of output.\n\n* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.",
 "input_schema": {
 "type": "object",
 "properties": {
 "command": {
 "type": "string",
 "description": "The bash command to run."
 }
 }
 },
 "required": ["command"]
 }
}
```

模型的第二个工具（Edit Tool）要复杂得多，包含了模型查看、创建和编辑文件所需的一切。同样，我们的工具描述包含面向模型的关于如何使用该工具的详细信息。

我们在各种 Agent 任务中对这些工具的描述和规范投入了大量精力。我们进行了测试以发现模型可能误解规范的方式或使用工具可能遇到的陷阱，然后编辑描述以预先防止这些问题。我们认为，应该投入更多注意力来为模型设计工具接口，就像为人类设计工具接口需要投入大量注意力一样。

💡 举例说明：工具描述的重要性——想象你给一个人一把瑞士军刀，但不告诉他每个刀片的功能。他可能会用错工具。同样，给 AI 模型提供工具时，工具描述就是「使用说明书」。描述越清晰，模型使用工具时出错的可能性越低。

以下代码展示了我们 Edit Tool 的描述：

```javascript
{
 "name": "str_replace_editor",
 "description": "Custom editing tool for viewing, creating and editing files\n\n* State is persistent across command calls and discussions with the user\n\n* If `path` is a file, `view` displays the result of applying `cat -n`. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep\n\n* The `create` command cannot be used if the specified `path` already exists as a file\n\n* If a `command` generates a long output, it will be truncated and marked with `<response clipped>` \n\n* The `undo_edit` command will revert the last edit made to the file at `path`\n\n\nNotes for using the `str_replace` command:\n\n* The `old_str` parameter should match EXACTLY one or more consecutive lines from the original file. Be mindful of whitespaces!\n\n* If the `old_str` parameter is not unique in the file, the replacement will not be performed. Make sure to include enough context in `old_str` to make it unique\n\n* The `new_str` parameter should contain the edited lines that should replace the `old_str`",
...
```

我们提升性能的一种方式是让工具「防错」（Error-proof）。例如，有时模型在 Agent 离开根目录后会搞乱相对文件路径。为防止这种情况，我们直接让工具始终要求使用绝对路径（Absolute Path）。

💡 术语解释：绝对路径 vs 相对路径——绝对路径是从文件系统根目录开始的完整路径（如 /repo/sklearn/linear_model/ridge.py），而相对路径是相对于当前工作目录的路径（如 ../sklearn/ridge.py）。使用绝对路径可以避免因目录切换导致的路径错误。

我们尝试了多种不同的策略来指定对现有文件的编辑，最终发现字符串替换（String Replacement）的可靠性最高——模型指定 old_str 并在给定文件中用 new_str 替换它。仅当 old_str 恰好有一个匹配时才会执行替换。如果匹配数量多于或少于一个，模型会看到相应的错误消息以便重试。

以下是我们 Edit Tool 的规范：

```javascript
...
 "input_schema": {
 "type": "object",
 "properties": {
 "command": {
 "type": "string",
 "enum": ["view", "create", "str_replace", "insert", "undo_edit"],
 "description": "The commands to run. Allowed options are: `view`, `create`, `str_replace`, `insert`, `undo_edit`."
 },
 "file_text": {
 "description": "Required parameter of `create` command, with the content of the file to be created.",
 "type": "string"
 },
 "insert_line": {
 "description": "Required parameter of `insert` command. The `new_str` will be inserted AFTER the line `insert_line` of `path`.",
 "type": "integer"
 },
 "new_str": {
 "description": "Required parameter of `str_replace` command containing the new string. Required parameter of `insert` command containing the string to insert.",
 "type": "string"
 },
 "old_str": {
 "description": "Required parameter of `str_replace` command containing the string in `path` to replace.",
 "type": "string"
 },
 "path": {
 "description": "Absolute path to file or directory, e.g. `/repo/file.py` or `/repo`.",
 "type": "string"
 },
 "view_range": {
 "description": "Optional parameter of `view` command when `path` points to a file. If none is given, the full file is shown. If provided, the file will be shown in the indicated line number range, e.g. [11, 12] will show lines 11 and 12. Indexing at 1 to start. Setting `[start_line, -1]` shows all lines from `start_line` to the end of the file.",
 "items": {
 "type": "integer"
 },
 "type": "array"
 }
 },
 "required": ["command", "path"]
 }
}
```