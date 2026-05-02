# 加密货币市场分析器 (Crypto Market Analyzer)

基于币安(Binance)数据的加密货币市场综合分析工具，支持从Markdown报告解析、实时数据获取、自动化分析到可视化报告生成的完整工作流。

## 🚀 功能特性

- 📊 **Markdown报告解析** - 自动解析币安市场分析报告
- 🔄 **实时数据获取** - 通过Binance API获取最新市场数据
- 📈 **智能分析引擎** - EMA/RSI/量比等多维度技术指标分析
- 🎯 **市场情绪评分** - 0-10分市场情绪量化评估
- 🐕 **板块分析** - 大盘核心/MEME/ETH生态等专项分析
- 📋 **自动化报告** - 生成结构化Markdown分析报告
- 📤 **数据导出** - 支持JSON/CSV格式导出

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/shuixinyun15/Repository-name-crypto-market-analyzer.git
cd Repository-name-crypto-market-analyzer

# 安装依赖
pip install -r requirements.txt
```

## 🛠️ 使用方法

### 1. 分析现有Markdown报告

```bash
python scripts/analyze_report.py data/Binance.com数据模板.md
```

### 2. 获取实时数据并生成报告

```bash
python scripts/fetch_binance_data.py --output data/latest_report.md
```

### 3. 完整分析流程

```python
from src.analyzer import CryptoMarketAnalyzer

# 创建分析器
analyzer = CryptoMarketAnalyzer('data/Binance.com数据模板.md')

# 运行分析
analyzer.run()

# 导出JSON
analyzer.export_json('output/analysis.json')
```

## 📊 分析维度

### 大盘核心 (BTC/ETH/SOL/BNB)
- 价格走势与关键均线位置
- 24h成交量与市值分析
- 距ATH回撤幅度
- EMA60/120趋势判断

### 板块分析
- **主板其他** - 42个主流币种
- **MEME板块** - 22个MEME币专项分析
- **ETH生态** - DeFi/L2代币分析

### 技术指标
- EMA (指数移动平均线)
- RSI (相对强弱指标)
- 量比 (成交量比率)
- FDV (完全稀释估值)

## 📈 输出示例

### 市场情绪评分
```
情绪评分: 2.6/10 (极度偏空)
- 75.7%币种24h下跌
- 仅25.7%站上EMA120
- BTC勉强守住EMA120
```

### 关键信号
```
⚠️ BTC极度脆弱 - 仅高出EMA120 0.13%
🔴 ETH中期偏弱 - 距EMA120还差6%
🔴 SOL双线之下 - 最弱大盘核心币
```

## 🗂️ 项目结构

```
crypto-market-analyzer/
├── data/               # 数据文件
├── src/                # 核心源代码
├── scripts/            # 实用脚本
├── tests/              # 单元测试
└── examples/           # 使用示例
```

## ⚙️ 配置

创建 `.env` 文件配置API密钥（可选）：

```env
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
COINGECKO_API_KEY=your_coingecko_key
```

## 📝 数据说明

| 数据项 | 来源 | 更新频率 | 可靠度 |
|--------|------|---------|--------|
| 24h成交量 | Binance API | 实时 | ⭐⭐⭐⭐⭐ |
| 最新价格 | Binance API | 实时 | ⭐⭐⭐⭐⭐ |
| EMA均线 | Binance API K线 | 实时 | ⭐⭐⭐⭐⭐ |
| 流通市值 | CoinGecko API | ~15分钟 | ⭐⭐⭐⭐ |
| FDV | CoinGecko API | ~15分钟 | ⭐⭐⭐⭐ |

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## ⚠️ 免责声明

本工具仅供学习研究使用，不构成投资建议。加密货币市场风险极高，请谨慎投资。

---

**作者**: 水心云15  
**更新日期**: 2026-05-02
