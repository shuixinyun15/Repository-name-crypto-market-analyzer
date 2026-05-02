---
name: crypto-market-analyzer
description: |
  加密货币市场综合分析工具。当用户提到以下场景时触发：
  - "分析币安市场""看看加密货币行情""BTC/ETH怎么样"
  - "meme币分析""DeFi代币分析""ETH生态分析"
  - "市场情绪如何""现在能抄底吗""加密货币投资建议"
  - "技术分析""EMA/均线分析""成交量分析"
  - 任何包含币种代码(BTC, ETH, SOL, BNB, DOGE等)的市场分析请求
  
  支持币安现货市场数据获取、技术指标计算(EMA/RSI/量比)、板块分析(MEME/DeFi/大盘)、市场情绪评分和操作建议生成。
  数据来源：Binance API + CoinGecko API。
---

# 加密货币市场分析器

## 概述

基于币安现货市场数据，提供全面的加密货币市场技术分析、板块分析和情绪判断。

## 核心能力

### 1. 市场总览
- 主板币种统计（排除Alpha区）
- 24h成交量分布
- 涨跌分布统计
- EMA均线站上率（EMA60/EMA120）

### 2. 大盘核心分析
重点跟踪：BTC、ETH、SOL、BNB
- 价格与均线位置关系
- 24h成交量与市值
- 距ATH（历史最高价）回撤幅度
- 多空关键位判断

### 3. 板块分析
- **MEME板块**：DOGE、SHIB、PEPE、PENGU等22个币种
- **ETH生态**：LINK、AAVE、UNI、LDO、ARB等DeFi/L2代币
- **主板其他**：按成交量排序的42个主板币种

### 4. 技术指标
- **EMA60/EMA120**：指数移动平均线，判断短中期趋势
- **RSI**：相对强弱指标，判断超买超卖
- **量比**：当前成交量/20日均量，判断量能真实性
- **流通市值 vs FDV**：评估未来抛压风险

### 5. 市场情绪评分
综合评分维度（0-10分）：
- 大盘均线格局
- 涨跌分布
- BTC/ETH状态
- 板块强弱
- 成交量集中度

## 分析流程

```
用户请求
    │
    ▼
┌─────────────────┐
│ 识别分析类型    │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    ▼         ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│ 大盘  │ │ 板块  │ │ 个股  │ │ 情绪  │
│ 核心  │ │ 分析  │ │ 技术  │ │ 评分  │
└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    │         │         │         │
    └─────────┴────┬────┴─────────┘
                   ▼
          ┌─────────────────┐
          │ 生成分析报告    │
          │ - 数据表格      │
          │ - 关键信号      │
          │ - 操作建议    │
          └─────────────────┘
```

## 数据获取

### Binance API
```bash
# 24h行情数据
curl "https://api.binance.com/api/v3/ticker/24hr"

# K线数据（计算EMA）
curl "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=150"
```

### CoinGecko API
```bash
# 市值/FDV/ATH数据
curl "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
```

## 技术指标计算

### EMA (指数移动平均线)
```python
# EMA60: 约3个月趋势
# EMA120: 约6个月趋势
# 站上EMA60 = 短中期偏多
# 站上EMA120 = 中长期趋势确立
# 双线之下 = 下行趋势
```

### RSI (相对强弱指标)
```
>70: 超买，回调风险
30-70: 中性
<30: 超卖，反弹可能
```

### 量比
```
>1.5: 放量，趋势确认
0.5-1.5: 正常
<0.5: 缩量，动能衰竭
```

## 板块分类规则

### MEME板块
包含：DOGE, SHIB, PEPE, PENGU, LUNC, TRUMP, NOT, BONK, WIF, NEIRO, FLOKI, 1000CHEEMS, MEME, BANANAS31, VIRTUAL, ACT, BERA, PNUT, BOME, TURBO, DOGS, BANANA

### ETH生态
包含：LINK, AAVE, UNI, LDO, ENA, ONDO, ARB, SNX, DYDX, CHZ, SAND, AXS, APE, WLD

### 大盘核心
BTC, ETH, SOL, BNB

## 输出格式

### 标准报告结构
```markdown
# 币安现货市场综合分析报告

## 一、总览统计
[市场整体数据表格]

## 二、大盘核心
[BTC/ETH/SOL/BNB详细分析]

## 三、板块分析
[MEME/ETH生态/主板其他]

## 四、市场情绪
[综合评分与判断]

## 五、操作建议
[具体策略框架]

## 六、指标说明
[EMA/RSI/量比等解释]
```

## 风险提示

1. **数据延迟**：CoinGecko数据有约15分钟延迟
2. **API限制**：Binance API有访问频率限制
3. **市场风险**：加密货币市场波动极大，分析仅供参考
4. **不构成投资建议**：所有分析仅为技术参考，决策自负盈亏

## 脚本

- `scripts/fetch_binance_data.py` — 获取Binance市场数据
- `scripts/calculate_indicators.py` — 计算EMA/RSI/量比
- `scripts/generate_report.py` — 生成分析报告
- `scripts/classify_sectors.py` — 板块分类

## 参考文档

- `references/technical-indicators.md` — 技术指标详细说明
- `references/sector-classification.md` — 板块分类标准
- `references/api-docs.md` — API接口文档