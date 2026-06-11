---
name: speculation-journey
description: Knowledge base from "投机苦旅" by 许星. Use when applying 许星's speculative trading frameworks for leveraged trading (forex, commodities, indices, options). Includes real-time market data queries via akshare.
when_to_use: speculative trading, leverage trading, stop loss, position management, trend following, asymmetric opportunity, crisis alpha, value investing, trading principles, futures trading, options trading, margin trading, risk control, trading psychology, should I trade, should I stop loss, should I add position, am I trading wrong, trading decision, stock quote, etf quote, index quote, futures quote, options data, macro data
allowed-tools: Read Grep Bash(python */.claude/skills/speculation-journey/etf-data/*.py)
argument-hint: [topic, framework name, chapter number, or data query]
---

# 投机苦旅 —— 一个投机客的凤凰涅槃

**Author**: 许星 | **Pages**: ~260 | **Chapters**: 5 + 后记 | **Generated**: 2026-06-10

## How to Use This Skill

- **Without arguments** — `/speculation-journey` loads core frameworks for reference
- **With a topic** — `/speculation-journey 止损` → I find and explain the topic
- **With chapter** — `/speculation-journey ch01` → I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

### 🛠️ Practical Tools (推荐使用)

当你面临交易决策时，可以直接问：

- **开仓前检查** → "用交易前检查清单帮我看看这笔交易"
- **决策困惑** → "我不知道要不要平仓，用决策助手帮我"
- **自我诊断** → "我好像在做错什么，用错误自检帮我看看"
- **具体问题** → "我应该止损吗？" / "我应该加仓吗？" / "现在有行情吗？"

### 📊 实时数据查询 (Real-time Data)

通过 **akshare** 支持多种金融数据查询：

- **股票行情** → "600519 现在多少钱" / "茅台涨了吗"
- **ETF 行情** → "510050 的行情" / "300ETF 现在多少钱"
- **指数行情** → "上证指数怎么样" / "创业板指"
- **期货数据** → "原油期货行情" / "螺纹钢期货"
- **期权链** → "50ETF 期权链" / "300ETF 期权"
- **宏观数据** → "最新 GDP 数据" / "CPI 是多少"

**数据来源**：akshare（整合东方财富、新浪、国家统计局等100+数据源）

When you ask about a topic not covered in Core Frameworks below, I will read
the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### 投机的本质

**定义**: 投机 = 投资于非对称性机会（低风险、高收益、高胜率、高赔率）

> "我理解，投资和投机的区别在于，投资是以标的物内在价值大小为决策依据的交易行为，市值越是低于内在价值，安全边际就越足，越值得买进；投机注重价格的未来波动，价格变动幅度越大，越有投机空间。"

**关键认知**:
- 高风险 ≠ 高收益 —— 追求"低风险+高收益"机会
- 杠杆交易中，时间是你的敌人
- "富贵险中求"是断章取义 —— 原文是"富贵险中求，也在险中丢，求时十之一，丢时十之九"

**杠杆交易警示**:
> "历史一再向我们证明，几乎所有杠杆的最终归宿都是清零，即使驾驭杠杆的是绝顶聪明之人。" —— 巴菲特

---

### 投机交易十大原则

#### 原则一：交易方法自洽原则
- **核心**: 找到适合自己的方法，而非盲目模仿大师
- **要点**: 每个人只会拥有自己真正领悟到的东西
- **应用**: "价值投资"需要强大的情绪管理能力，普通人难以做到

#### 原则二：掌握交易优势原则
- **核心**: 必须掌握可重复利用的获利规律
- **两类必要优势**:
  1. 擅于发现并抓住非对称性获利机会
  2. 擅于洞察风险避免巨大亏损
- **金句**: "行稳致远，要求我们学会用两条腿走路，学会能赚钱是一条支撑腿，学会不赔大钱是另一条支撑腿。"

#### 原则三：不与市场对抗原则
- **核心**: 一旦市场通过浮亏告诉你你错了，必须立即考量风险
- **生存准则**: 避免大亏损，留在市场里，随时认错
- **警示**: "市场往往涨时涨过头，跌时跌过头" —— 牛顿："我能算准天体的运行，却无法预测人类的疯狂"

#### 原则四：试错交易原则
- **核心**: 每笔交易都假设会错，主动设置止损是标准动作
- **盈亏逻辑**: 赔多少靠人（止损），赚多少靠势（行情）
- **理想状态**: 10笔交易，8笔各赔1元，2笔各赚5元 = 净赚2元

#### 原则五：行情选择原则
- **核心**: "有所为、有所不为" —— 只参与趋势行情，不参与震荡
- **慎战三原则**: 非利不动，非得不用，非危不战

#### 原则六：非对称机会优先原则
- **核心**: 追求低风险、高收益的机会
- **时机**: 往往出现在市场极端情况时

#### 原则七：生存第一原则
- **核心**: 不被市场淘汰，才有机会盈利
- **类比**: 如同狮群捕猎，一旦受伤可能失去生存能力

#### 原则八：趋势跟随原则
- **核心**: 杠杆交易慎用价值回归策略，适用趋势跟随策略
- **理由**: 杠杆交易容错率低，价格波动是最大敌人

#### 原则九：情绪控制原则
- **核心**: 规避内心痛苦、寻求舒适感是非理性决策的根源
- **表现**: 盈利时过早平仓，亏损时死扛

#### 原则十：身心健康原则
- **核心**: 交易者身心健康是长期成功的基础
- **离场止损**: 当身心健康、情绪控制发生重大不利变化时，无条件平仓

---

### 止损六法

1. **技术指标止损** — 价格跌破20日均线或技术支撑位
2. **价格定额止损** — 跌幅达设定百分比（如2%）
3. **绝对金额止损** — 亏损达固定金额或账户比例
4. **保本止损** — 浮盈后迅速调整止损到成本价
5. **动态止损** — 浮盈后跟踪止损，如设为75%浮盈位
6. **离场止损** — 身心健康/情绪/基本面重大变化时无条件平仓

> "必须止损，错了也对。不设止损，如同开车不安装刹车系统。"

---

### 杠杆与仓位管理

**仓位分类**:
- **事实型交易** — 被理性支配，基于基本面和技术面共振
- **欲望型交易** — 被感性支配，基于希望和幻想

**金字塔加仓**: "3-2-1"方式，初期加仓、后期减仓

**凯利公式**: q = p - (1-p)/R
- p = 胜率
- R = 盈亏比

**海龟法则**: 以ATR确定仓位 — 让1ATR变动 = 账户规模的1%

**金句**: "方向决定生死，仓位决定成败"

---

### 最佳交易策略

**两大策略类别**:

| 策略 | 特点 | 胜率 | 收益分布 | 杠杆交易适用性 |
|------|------|------|----------|----------------|
| 价值回归 | 相信价值规律 | 较高 | 负偏度，左尾肥大 | ❌ 不适用 |
| 趋势跟随 | 承认无法预测 | 较低 | 正偏度，右尾肥大 | ✅ 适用 |

**理想交易策略特征**:
- 无数次小亏损 + 少数大盈利
- 胜率 < 50%，但盈亏比 > 1
- 表现为正偏度（右尾肥）

**危机阿尔法策略**:
- 利用市场危机期间的持续趋势
- 要求：屏蔽多头偏差、允许做空
- 核心：珍惜每一次危机

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-speculation-journey.md) | 误打误撞进入外盘世界 | 投机本质, 外盘交易入门 |
| [ch02](chapters/ch02-speculation-journey.md) | 新手的甜蜜时光 | 投机交易十大原则 |
| [ch03](chapters/ch03-speculation-journey.md) | 爆仓！领教市场凶险 | 止损六法 |
| [ch04](chapters/ch04-speculation-journey.md) | 风云际会，激战多空 | 实战案例分析 |
| [ch05](chapters/ch05-speculation-journey.md) | 无心胜有心，大道本无情 | 杠杆和仓位, 最佳交易策略 |

## Topic Index

- **非对称机会** → ch01, ch02
- **投机交易原则** → ch02
- **止损方法** → ch03
- **杠杆** → ch03, ch05
- **仓位管理** → ch05
- **趋势跟随** → ch05
- **价值回归** → ch05
- **危机阿尔法** → ch05

## Supporting Files

### 核心参考
- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and trading patterns
- [cheatsheet.md](cheatsheet.md) — quick reference for decision making

### 实用工具 ⭐ 新增
- [checklists.md](checklists.md) — 📋 交易前检查清单（每次开仓前必看）
- [decision-helper.md](decision-helper.md) — ❓ 决策助手（关键时刻的思考框架）
- [error-check.md](error-check.md) — 🔍 常见错误自检（识别你是否在犯错）

### 学习与成长 ⭐ 新增
- [trading-journal.md](trading-journal.md) — 📓 交易记录与复盘模板（从错误中学习）
- [quotes.md](quotes.md) — 🔑 许星语录精华（金句随时查阅）
- [faq.md](faq.md) — ❓ 常见问题FAQ（新手入门必看）

---

## Scope & Limits

This skill covers the book content only. For hands-on implementation in your trading,
combine with your own analysis and risk management. For topics beyond this book, check related skills
or ask Claude directly.

**⚠️ 重要提示**: 本书内容为作者个人经验总结，不构成投资建议。杠杆交易风险极高，可能导致本金全部损失。请根据自身风险承受能力谨慎决策。
