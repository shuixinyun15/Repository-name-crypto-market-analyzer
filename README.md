# 加密货币市场分析器 (Crypto Market Analyzer)

基于币安现货市场数据的综合分析工具，提供技术指标计算、板块分析和市场情绪判断。

## 功能特点

- 📊 **市场总览**：24h成交量、涨跌分布、均线站上率
- 🎯 **大盘核心**：BTC/ETH/SOL/BNB 关键位置分析
- 🚀 **板块分析**：MEME、DeFi、ETH生态等专项分析
- 📈 **技术指标**：EMA60/120、RSI、量比、流通市值/FDV
- 🎭 **情绪评分**：0-10分综合市场情绪判断
- ⚡ **操作建议**：具体策略框架

## 安装方法

```bash
npx skills add 你的用户名/crypto-market-analyzer
```

## 使用方法

安装后，直接对 AI 说：
- "分析一下币安市场"
- "BTC现在怎么样"
- "meme币行情如何"
- "ETH生态分析"
- "市场情绪如何"

## 数据来源

- **Binance API**：实时行情、K线数据
- **CoinGecko API**：市值、FDV、ATH数据

## 技术指标说明

### EMA (指数移动平均线)
- **EMA60**：约3个月趋势，站上=短中期偏多
- **EMA120**：约6个月趋势，站上=中长期趋势确立
- **双线之下**：下行趋势，反弹视为技术性修复

### RSI (相对强弱指标)
- >70：超买区，回调风险
- 30-70：中性区间
- <30：超卖区，反弹可能

### 量比
- >1.5：放量，趋势确认
- 0.5-1.5：正常波动
- <0.5：缩量，动能衰竭

## 板块分类

### MEME板块
DOGE, SHIB, PEPE, PENGU, LUNC, TRUMP, NOT, BONK, WIF 等

### ETH生态
LINK, AAVE, UNI, LDO, ARB, SNX, DYDX 等 DeFi/L2 代币

### 大盘核心
BTC, ETH, SOL, BNB

## 风险提示

1. 数据延迟：CoinGecko数据有约15分钟延迟
2. API限制：Binance API有访问频率限制
3. 市场风险：加密货币市场波动极大，分析仅供参考
4. **不构成投资建议**：所有分析仅为技术参考，决策自负盈亏

## 文件结构

```
crypto-market-analyzer/
├── SKILL.md                          # 技能定义与使用说明
├── scripts/
│   ├── fetch_binance_data.py         # 获取Binance市场数据
│   ├── calculate_indicators.py      # 计算EMA/RSI/量比
│   └── generate_report.py           # 生成分析报告
└── references/
    ├── technical-indicators.md      # 技术指标详细说明
    └── sector-classification.md     # 板块分类标准
```

## 许可证

MIT License © 2026

---

**注意**：本工具仅供参考学习，不构成任何投资建议。加密货币市场风险极高，请谨慎决策。