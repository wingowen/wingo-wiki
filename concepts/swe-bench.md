---
title: "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩 | Raising the bar on SWE-bench Verified"
created: 2025-01-06
updated: 2025-01-06
type: concept
tags: [anthropic, benchmark, evaluation]
sources: []
notion_id: 34267b21-8207-812d-8ba2-e62bfbdca0aa
---

> 原文链接：Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet

> 作者：Anthropic Engineering（Erik Schluntz 等人）

> 发布日期：2025-01-06

> 翻译日期：2026-04-14

## 用 Claude 3.5 Sonnet 提升 SWE-bench 成绩

我们最新的升级版 Claude 3.5 Sonnet 在 SWE-bench Verified（一项软件工程评估基准）上达到了 49% 的成绩，超越了之前 SOTA（State-of-the-Art，当前最优）模型的 45%。本文将介绍我们围绕该模型构建的「Agent（智能体）」，旨在帮助开发者充分发挥 Claude 3.5 Sonnet 的性能潜力。

SWE-bench 是一个 AI 评估基准（Benchmark），用于评估模型完成真实世界软件工程任务的能力。具体而言，它测试模型能否解决来自热门开源 Python 仓库的 GitHub Issue。对于基准中的每个任务，AI 模型会获得一个配置好的 Python 环境以及该仓库在 Issue 被解决之前的 Checkout（本地工作副本）。模型随后需要理解、修改并测试代码，最终提交其解决方案。

每个解决方案都会与关闭原始 GitHub Issue 的 Pull Request（PR，拉取请求）中的真实单元测试进行对比评分。这测试了 AI 模型是否能够实现与原始 PR 人类作者相同的功能。

SWE-bench 不仅仅评估孤立的 AI 模型，而是评估整个「Agent」系统。在此语境下，「Agent」指的是 AI 模型与其周围软件脚手架（Scaffolding）的组合。脚手架负责生成输入模型的 Prompt（提示词）、解析模型输出以执行操作，以及管理交互循环——即将模型上一次操作的结果纳入下一次 Prompt 中。即使使用相同的底层 AI 模型，Agent 在 SWE-bench 上的表现也可能因脚手架的不同而有显著差异。

💡 术语解释：Agent（智能体）——在 AI 领域，Agent 指的是能够自主感知环境、做出决策并执行行动的系统。在本文语境中，Agent = AI 模型 + 工具 + 脚手架代码。

评估大语言模型（Large Language Model，LLM）编码能力的基准有很多，但 SWE-bench 因以下几个原因而日益流行：

  1. 它使用来自真实项目的实际工程任务，而非竞赛或面试风格的问题；

  2. 它尚未饱和（Saturated）——仍有很大的提升空间。目前还没有任何模型在 SWE-bench Verified 上突破 50% 的完成率（不过截至本文撰写时，升级版 Claude 3.5 Sonnet 已达到 49%）；

  3. 它衡量的是整个「Agent」而非孤立的模型。开源开发者和初创公司在优化脚手架方面取得了巨大成功，能够在相同模型基础上大幅提升性能。

💡 术语解释：饱和（Saturated）——指基准测试中模型的得分已经接近满分，难以再通过改进来区分不同模型的优劣。SWE-bench 目前远未饱和，这意味着它仍然是一个有效的评估工具。

需要注意的是，原始 SWE-bench 数据集中包含一些在没有 GitHub Issue 之外的额外上下文（例如关于应返回的特定错误信息）的情况下无法解决的任务。SWE-bench Verified 是 SWE-bench 的一个包含 500 个问题的子集，经过人工审核确保它们都是可解决的，因此提供了对编码 Agent 性能最清晰的衡量标准。本文后续将统一指代这一基准。

### 达到 SOTA

#### 工具型 Agent

我们在为升级版 Claude 3.5 Sonnet 创建优化的 Agent 脚手架时，设计理念是尽可能将控制权交给语言模型本身，同时保持脚手架的最小化。该 Agent 包含一个 Prompt、一个用于执行 bash 命令的 Bash Tool（Bash 工具）和一个用于查看和编辑文件及目录的 Edit Tool（编辑工具）。我们持续采样，直到模型自行决定完成，或超出其 200k 上下文长度。这种脚手架允许模型运用自身判断力来决定如何推进问题，而非被硬编码为特定的模式或工作流。

Prompt 为模型概述了建议的处理方法，但对于此任务而言并不过长或过于详细。模型可以自由选择如何在各步骤之间过渡，而非遵循严格的离散转换。如果你不敏感于 Token 消耗，显式鼓励模型生成长篇回复会有所帮助。

以下代码展示了我们 Agent 脚手架中的 Prompt：

```javascript
<uploaded_files>
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
 "description": "Run commands in a bash shell\n
* When invoking this tool, the contents of the \"command\" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* State is persistent across command calls and discussions with the user.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output.\n
* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.",
 "input_schema": {
 "type": "object",
 "properties": {
 "command": {
 "type": "string",
 "description": "The bash command to run."
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
 "description": "Custom editing tool for viewing, creating and editing files\n
* State is persistent across command calls and discussions with the user\n
* If `path` is a file, `view` displays the result of applying `cat -n`. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep\n
* The `create` command cannot be used if the specified `path` already exists as a file\n
* If a `command` generates a long output, it will be truncated and marked with `<response clipped>` \n
* The `undo_edit` command will revert the last edit made to the file at `path`\n
\n
Notes for using the `str_replace` command:\n
* The `old_str` parameter should match EXACTLY one or more consecutive lines from the original file. Be mindful of whitespaces!\n
* If the `old_str` parameter is not unique in the file, the replacement will not be performed. Make sure to include enough context in `old_str` to make it unique\n
* The `new_str` parameter should contain the edited lines that should replace the `old_str`",
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

### 结果

总体而言，升级版 Claude 3.5 Sonnet 在推理、编码和数学能力方面均优于我们之前的模型以及之前的 SOTA模型。它还展示了改进的 Agentic（智能体）能力：工具和脚手架帮助将这些增强的能力发挥到最佳水平。

我们部分模型在 SWE-bench Verified 上的得分，均使用此 Agent 脚手架。

### Agent 行为示例

在运行基准测试时，我们使用 SWE-Agent 框架作为 Agent 代码的基础。在下面的日志中，我们将 Agent 的文本输出、工具调用和工具响应分别渲染为 THOUGHT、ACTION 和 OBSERVATION，尽管我们并未将模型限制为固定的顺序。

下面的代码块将展示 Sonnet 3.5 解决 SWE-bench 问题的一个典型案例。

在第一个代码块中，你可以看到给模型的部分初始 Prompt，其中 {pr_description} 已填入 SWE-bench 任务的真实值。重要的是，该任务包含复现问题的步骤，这为模型提供了一个宝贵的调查起点。

```javascript
<uploaded_files>
/repo
</uploaded_files>
I've uploaded a python code repository in the directory /repo (not in /tmp/inputs). Consider the following PR description:

<pr_description>
linear_model.RidgeClassifierCV's Parameter store_cv_values issue
#### Description
Parameter store_cv_values error on sklearn.linear_model.RidgeClassifierCV

#### Steps/Code to Reproduce
import numpy as np
from sklearn import linear_model as lm

#test database
n = 100
x = np.random.randn(n, 30)
y = np.random.normal(size = n)

rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True,
 store_cv_values = True).fit(x, y)

#### Expected Results
Expected to get the usual ridge regression model output, keeping the cross validation predictions as attribute.

#### Actual Results
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'

lm.RidgeClassifierCV actually has no parameter store_cv_values, even though some attributes depends on it.
```

模型做出响应，首先使用 Edit Tool 查看仓库结构。你可以在 THOUGHT 和 ACTION 下看到模型的文本输出和工具调用参数，在 OBSERVATION 下看到工具的部分输出：

```javascript
THOUGHT:
I'll help you implement the changes to satisfy the PR description. Let's follow the steps you outlined.

1. First, let's explore the repo structure:
ACTION (str_replace_editor):
command:
view

path:
/repo

OBSERVATION:
Here's the files and directories up to 2 levels deep in /repo, excluding hidden items:
/repo
/repo/PULL_REQUEST_TEMPLATE.md
/repo/ISSUE_TEMPLATE.md
/repo/sklearn
/repo/sklearn/decomposition
/repo/sklearn/kernel_ridge.py
/repo/sklearn/model_selection
/repo/sklearn/covariance
/repo/sklearn/cluster
/repo/sklearn/base.py
/repo/sklearn/dummy.py
/repo/sklearn/naive_bayes.py
...
```

现在模型对仓库结构有了更好的了解，它使用 Edit Tool 创建了一个新脚本，用于复现问题并测试其修复方案：

```javascript
THOUGHT:
Based on the repository structure, we'll need to modify the Ridge Classifier in the `sklearn/linear_model` directory.

Let's create a script to reproduce the error:
ACTION (str_replace_editor):
command:
create

path:
/repo/reproduce_error.py

file_text:
import numpy as np
from sklearn import linear_model as lm

#test database
n = 100
x = np.random.randn(n, 30)
y = np.random.normal(size = n)

rr = lm.RidgeClassifierCV(alphas=np.arange(0.1, 1000, 0.1), normalize=True,
 store_cv_values=True).fit(x, y)

OBSERVATION:
File created successfully at: /repo/reproduce_error.py
```

模型随后使用 Bash Tool 执行其编写的脚本，成功复现了任务中的问题：

```javascript
THOUGHT:
Let's verify that we can reproduce the error:
ACTION (bash):
command:
python3 /repo/reproduce_error.py

OBSERVATION:
Traceback (most recent call last):
 File "/repo/reproduce_error.py", line 10, in <module>
 store_cv_values=True).fit(x, y)
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
```

此后，模型使用 Edit Tool 修改仓库中的源代码，并重新运行其脚本以验证更改是否解决了问题：

```javascript
THOUGHT:
The error is reproducible. Looking at the code, I can see that the issue is that while the `RidgeClassifierCV` class inherits from `_BaseRidgeCV`, it fails to pass the `store_cv_values` parameter from its constructor through to the base class constructor.

Let's fix this:
ACTION (str_replace_editor):
command:
str_replace

path:
/repo/sklearn/linear_model/ridge.py

old_str:
 def __init__(self, alphas=(0.1, 1.0, 10.0), fit_intercept=True,
 normalize=False, scoring=None, cv=None, class_weight=None):
 super(RidgeClassifierCV, self).__init__(
 alphas=alphas, fit_intercept=fit_intercept, normalize=normalize,
 scoring=scoring, cv=cv)

 self.class_weight = class_weight

new_str:
 def __init__(self, alphas=(0.1, 1.0, 10.0), fit_intercept=True,
 normalize=False, scoring=None, cv=None, class_weight=None,
 store_cv_values=False):
 super(RidgeClassifierCV, self).__init__(
 alphas=alphas, fit_intercept=fit_intercept, normalize=normalize,
 scoring=scoring, cv=cv, store_cv_values=store_cv_values)

 self.class_weight = class_weight
```

在这个特定示例中，模型运行了 12 个步骤后决定准备提交。任务的测试随后成功运行，验证了模型的解决方案确实解决了问题。有些任务模型在提交解决方案前需要超过 100 轮；而在另一些任务中，模型会一直尝试直到上下文耗尽。

通过对比升级版 Claude 3.5 Sonnet 与旧版模型的尝试记录，我们发现新版 3.5 Sonnet 进行自我纠正的频率更高。它还展现出尝试多种不同解决方案的能力，而非陷入反复犯同样错误的困境。

### 挑战

SWE-bench Verified 是一个强大的评估基准，但运行起来也比简单的单轮评估（Single-turn Eval）复杂得多。以下是我们在使用它时面临的一些挑战——其他 AI 开发者可能也会遇到类似问题。

运行时长和高 Token 成本。 上面的示例来自一个在 12 个步骤内成功完成的案例。然而，许多成功运行需要数百轮才能解决，消耗超过 100k 个 Token。升级版 Claude 3.5 Sonnet 非常坚韧（Tenacious）：给定足够的时间，它通常能找到解决问题的方法，但这可能代价高昂；

评分。 在检查失败任务时，我们发现了一些模型行为正确但存在环境配置问题，或安装补丁被重复应用的情况。解决这些系统问题对于准确了解 AI Agent 的性能至关重要；

隐藏测试。 由于模型无法看到用于评分的测试，它经常在自己认为已经成功时，任务实际上却是失败的。其中一些失败是因为模型在错误的抽象层级上解决了问题（打补丁而非深度重构）。其他一些失败则显得不太公平：它们解决了问题，但与原始任务的单元测试不匹配；

多模态。 尽管升级版 Claude 3.5 Sonnet 拥有出色的视觉和多模态能力，我们并未实现让它查看保存到文件系统或以 URL 引用的文件的功能。这使得调试某些任务（尤其是来自 Matplotlib 的任务）特别困难，也容易导致模型产生幻觉（Hallucination）。对于开发者来说，这里肯定有容易摘到的果实可以改进——SWE-bench 也已推出了一项专注于多模态任务的新评估。我们期待在不久的将来看到开发者使用 Claude 在这项评估上取得更高的分数。

💡 术语解释：幻觉（Hallucination）——指 AI 模型生成看似合理但实际上不正确或虚构的内容。在代码调试场景中，模型可能「想象」出错误的代码行为或输出结果。

升级版 Claude 3.5 Sonnet 凭借一个简单的 Prompt 和两个通用工具，在 SWE-bench Verified 上达到了 49%，超越了之前的 SOTA（45%）。我们相信，使用新版 Claude 3.5 Sonnet 构建的开发者将很快找到新的、更好的方法来超越我们在此初步展示的 SWE-bench 成绩。

### 致谢

Erik Schluntz 优化了 SWE-bench Agent 并撰写了这篇博文。Simon Biggs、Dawn Drain 和 Eric Christiansen 协助实现了基准测试。Shauna Kravec、Dawn Drain、Felipe Rosso、Nova DasSarma、Ven Chandrasekaran 以及许多其他人参与了训练 Claude 3.5 Sonnet，使其在 Agent 编码方面表现出色。

---

### 译者注

  1. 本文是 Anthropic 工程博客系列中关于 SWE-bench 的重要技术文章，详细介绍了其 Agent 架构设计思路。文章强调的核心观点是：工具设计和脚手架的优化与模型本身的能力同等重要。

  2. 文中提到的「SWE-bench Verified」是 OpenAI 与 Princeton 等机构联合推出的子集基准，500 个问题均经过人工验证可解，是目前衡量编码 Agent 能力的主流标准之一。

  3. 值得注意的是，本文发表于 2025 年 1 月，当时 Claude 3.5 Sonnet 以 49% 创下纪录。截至翻译日期（2026 年 4 月），SWE-bench 的分数可能已有进一步提升。

  4. 文章中 Agent 的 THOUGHT/ACTION/OBSERVATION 模式虽然未被强制约束，但这一格式清晰展示了 Agent 的推理-行动-观察循环，对理解 Agent 工作原理很有帮助。

  5. 关于工具设计的关键启示：要求绝对路径、使用字符串替换而非行号编辑、在工具描述中预判并防止常见错误——这些经验对构建可靠的 AI Agent 具有普遍参考价值。

## 相关链接

[[anthropic]] | [[claude-code]]
