---
title: "用 Claude 3.5 Sonnet 提升 SWE-bench 成绩 - Agent 行为示例"
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [anthropic, benchmark, evaluation]
sources: []
---

# Agent 行为示例

在运行基准测试时，我们使用 SWE-Agent 框架作为 Agent 代码的基础。在下面的日志中，我们将 Agent 的文本输出、工具调用和工具响应分别渲染为 THOUGHT、ACTION 和 OBSERVATION，尽管我们并未将模型限制为固定的顺序。

下面的代码块将展示 Sonnet 3.5 解决 SWE-bench 问题的一个典型案例。

在第一个代码块中，你可以看到给模型的部分初始 Prompt，其中 {pr_description} 已填入 SWE-bench 任务的真实值。重要的是，该任务包含复现问题的步骤，这为模型提供了一个宝贵的调查起点。

```javascript
<uploading_files>
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
</pr_description>
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