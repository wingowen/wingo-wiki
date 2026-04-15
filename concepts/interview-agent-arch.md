---
title: "【面试专题】Agent 架构设计：从传统开发到智能体"
created: 2026-04-15
updated: 2026-04-15
type: summary
tags: [agent, architecture, interview]
sources: []
notion_id: 34367b21-8207-8163-9cdf-c8c77b1efa54
---

## Agent 架构设计：从传统开发到智能体

> 难度：⭐⭐⭐⭐ | 面试频率：高 | 关联：👉 LangGraph 核心原理与 ReAct 对比 👉 上下文管理：短期记忆与长期记忆

---

### 一、智能体 vs 传统开发：根本区别

#### 1.1 核心差异对比

#### 1.2 传统开发的思维模型

```javascript
用户请求 → Controller → Service → DAO → Database → 返回结果
```

每一步都是开发者预设的，输入确定则输出确定。

#### 1.3 Agent 的思维模型

```javascript
用户目标 → Agent 感知（理解意图）
         → Agent 规划（分解任务、制定计划）
         → Agent 行动（选择工具、执行操作）
         → Agent 观察（获取反馈）
         → Agent 反思（评估结果、调整策略）
         → 循环直到目标达成
```

每一步都是 LLM 动态决策的，同样的输入可能产生不同的执行路径。

---

### 二、Agent 架构核心组件

#### 2.1 Perception（感知层）

```python
# 感知层：理解用户意图
class AgentPerception:
    def understand_intent(self, user_input: str) -> dict:
        """理解用户意图，提取关键信息"""
        response = llm.invoke(
            f"分析以下用户输入的意图和关键信息：\n"
            f"输入：{user_input}\n"
            f"请返回 JSON 格式：{{'intent': '...', 'entities': {{...}}, 'urgency': '...'}}"
        )
        return json.loads(response.content)
```

#### 2.2 Decision（决策层）

```python
# 决策层：规划任务和选择工具
class AgentDecision:
    def plan_and_decide(self, state: AgentState) -> dict:
        """基于当前状态做出决策"""
        # 可用工具列表
        tools = [
            {"name": "search_flights", "description": "搜索航班"},
            {"name": "book_hotel", "description": "预订酒店"},
            {"name": "get_weather", "description": "查询天气"},
        ]

        # LLM 决定下一步行动
        response = llm.invoke(
            messages=state["messages"],
            tools=tools,
        )
        return response
```

#### 2.3 Action（行动层）

```python
# 行动层：执行工具调用
class AgentAction:
    def execute_tool(self, tool_name: str, args: dict) -> str:
        """执行具体的工具调用"""
        tool = self.tools.get(tool_name)
        if not tool:
            return f"错误：未知工具 {tool_name}"

        try:
            result = tool.execute(**args)
            return str(result)
        except Exception as e:
            return f"工具执行失败：{str(e)}"
```

---

### 三、C端用户偏好实现

#### 3.1 用户画像构建

```python
class UserProfile:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.preferences = {}  # 兴趣标签
        self.history = []       # 行为历史

    def update_from_behavior(self, behavior: dict):
        """根据用户行为更新画像"""
        action = behavior["action"]  # click / favorite / book
        item = behavior["item"]      # 景点/酒店/餐厅
        category = behavior["category"]  # 自然风光/历史文化/美食

        # 更新兴趣权重
        if category not in self.preferences:
            self.preferences[category] = 0.0

        weight_map = {"click": 0.1, "favorite": 0.3, "book": 0.5}
        self.preferences[category] += weight_map.get(action, 0.1)

        # 记录行为
        self.history.append({
            "timestamp": time.time(),
            "action": action,
            "item": item,
            "category": category
        })

    def get_top_interests(self, k: int = 5) -> list:
        """获取 Top-K 兴趣标签"""
        sorted_prefs = sorted(
            self.preferences.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [tag for tag, score in sorted_prefs[:k]]
```

#### 3.2 向量化与推荐

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

def recommend_by_preference(user_profile: UserProfile, items: list) -> list:
    """基于用户偏好向量进行推荐"""
    # 将用户偏好转为文本描述
    interests = user_profile.get_top_interests(5)
    user_desc = f"用户偏好：{'、'.join(interests)}"

    # 用户偏好向量化
    user_vector = embeddings.embed_query(user_desc)

    # 计算每个推荐项与用户偏好的相似度
    scored_items = []
    for item in items:
        item_vector = embeddings.embed_query(item["description"])
        similarity = cosine_similarity(user_vector, item_vector)
        scored_items.append((item, similarity))

    # 按相似度排序
    scored_items.sort(key=lambda x: x[1], reverse=True)
    return [item for item, score in scored_items[:10]]
```

#### 3.3 冷启动问题

新用户没有历史行为时如何推荐？

  1. 显式偏好收集：注册时让用户选择兴趣标签

  2. 基于人口统计学：根据年龄、性别、地域推荐热门内容

  3. 探索-利用策略：初期推荐多样化内容，快速收集用户反馈

  4. 迁移学习：利用相似用户群体的偏好作为初始画像

---

### 四、面试高频追问

#### Q: Agent 的"不可预测性"如何保证安全？

A: 多层防护：1）工具层白名单：只允许调用预定义的安全工具；2）参数校验：对 LLM 生成的工具参数进行类型和范围校验；3）沙箱执行：代码执行等危险操作在沙箱中运行；4）人工审核：关键操作（如支付、删除）需要人类确认（Human-in-the-loop）；5）日志审计：记录所有 Agent 行为，便于事后追溯。

#### Q: Agent 的成本如何控制？

A: 1）减少不必要的 LLM 调用（缓存、路由判断）；2）使用小模型处理简单任务，大模型处理复杂任务；3）优化 Prompt 长度（减少 token 消耗）；4）设置 Agent Loop 的最大轮次（MAX_TURNS）；5）使用流式输出提升用户体验的同时降低首字延迟。

#### Q: 如何评估 Agent 的效果？

A: 1）任务完成率：Agent 是否成功达成了用户目标；2）工具调用效率：平均需要多少轮工具调用才能完成任务；3）用户满意度：用户对 Agent 回答的评价；4）延迟：从用户输入到最终回答的时间；5）成本：每次交互的平均 token 消耗和 API 费用。

#### Q: 智能体旅游项目中，如何处理多轮对话中的上下文丢失？

A: 1）使用 LangGraph 的 Checkpointer 持久化会话状态；2）在 System Prompt 中维护任务状态摘要（如"用户已选择目的地：三亚，预算：5000元"）；3）关键信息提取后存入 State 的结构化字段（而非仅依赖 messages）；4）当对话轮次过多时，使用摘要化策略压缩旧消息。

## 相关链接

[[agent-architecture]] | [[interview-qa-overview]]
