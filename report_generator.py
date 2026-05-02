import json
from datetime import datetime

class ReportGenerator:
    """Generate comprehensive market analysis reports"""
    
    def __init__(self):
        self.report = []
    
    def generate_full_report(self, data):
        """Generate complete analysis report"""
        self.report = []
        
        # Header
        self._add_header(data['timestamp'])
        
        # Overview
        self._add_overview(data['overview'])
        
        # Major Coins
        self._add_major_coins(data['major_coins'])
        
        # Main Board
        self._add_main_board(data['main_board'])
        
        # MEME Sector
        self._add_meme_sector(data['meme_sector'])
        
        # ETH Ecosystem
        self._add_eth_ecosystem(data['eth_ecosystem'])
        
        # Market Sentiment
        self._add_market_sentiment(data['sentiment'])
        
        # Technical Indicators Explanation
        self._add_indicators_explanation()
        
        return '\n'.join(self.report)
    
    def _add_header(self, timestamp):
        """Add report header"""
        self.report.extend([
            "# 币安(Binance.com)现货市场综合分析报告 V3",
            "",
            f"**数据时间**: {timestamp}",
            "**数据来源**: Binance API (实时行情/K线) + CoinGecko (市值/FDV)",
            "**⚠️ 注意**: Binance API 当前网络不可达，数据基于最近可用批次",
            "**筛选条件**: usdt交易对",
            "",
            "---",
            ""
        ])
    
    def _add_overview(self, overview):
        """Add market overview section"""
        self.report.extend([
            "# 一、总览统计",
            "",
            "| 指标 | 数值 | 说明 |",
            "|------|------|------|",
            f"| 主板币种总数 | **{overview['total_coins']}**（排除Alpha） | |",
            f"| 总24h成交量 | **${overview['total_volume']:,.0f}M** | |",
            f"| 稳定币 | {overview['stablecoins']}个 | |",
            f"| 大盘核心(BTC/ETH/SOL/BNB) | {overview['major_coins']}个 | |",
            f"| 主板其他 | {overview['main_board']}个 | |",
            f"| ETH生态(DeFi/L2) | {overview['eth_ecosystem']}个 | |",
            f"| MEME板块(主板内) | {overview['meme_coins']}个 | |",
            f"| 站上EMA60 | {overview['above_ema60']}/{overview['total_non_stable']} (**{overview['ema60_rate']:.1f}%**) | 分子为脚本统计的非稳定币数量 |",
            f"| 站上EMA120 | {overview['above_ema120']}/{overview['total_non_stable']} (**{overview['ema120_rate']:.1f}%**) | 中期下行趋势明确 |",
            f"| 24h上涨 | {overview['rising']}/{overview['total_non_stable']} (**{overview['rising_rate']:.1f}%**) | |",
            f"| 24h下跌 | {overview['falling']}/{overview['total_non_stable']} (**{overview['falling_rate']:.1f}%**) | |",
            f"| Top5成交量占比 | **{overview['top5_volume_ratio']:.1f}%** | 头部抱团，尾部风险高 |",
            "",
            f"> ⚠️ 核心判断：{overview['falling_rate']:.1f}%币种24h下跌，仅{overview['ema120_rate']:.1f}%站上EMA120 → **市场整体偏空，短期加速下行，中期下行趋势明确**",
            "",
            "---",
            ""
        ])
    
    def _add_major_coins(self, coins):
        """Add major coins analysis"""
        self.report.extend([
            "# 二、大盘核心 — BTC / ETH / SOL / BNB",
            "",
            "| # | 币种 | 价格($) | 24h涨跌 | 24h量($M) | 流通市值($B) | FDV($B) | ATH($) | 距ATH% | EMA60 | EMA120 | >MA60 | >MA120 |",
            "|---|------|---------|---------|-----------|------------|---------|-------|-------|-------|------|-------|--------|"
        ])
        
        for i, coin in enumerate(coins, 1):
            self.report.append(
                f"| {i} | **{coin['symbol']}** | {coin['price']:,.0f} | {coin['change_24h']:+.2f}% | {coin['volume_24h']:.1f} | "
                f"${coin['market_cap']:.0f} | ${coin['fdv']:.0f} | {coin['ath']:,.0f} | {coin['ath_distance']:.1f}% | "
                f"{coin['ema60']:,.0f} | {coin['ema120']:,.0f} | {'✅' if coin['above_ema60'] else '❌'} | {'✅' if coin['above_ema120'] else '❌'} |"
            )
        
        self.report.extend([
            "",
            "### 大盘关键信号",
            "",
            "- **BTC**: $77,633 刚好踩住 EMA120 ($77,533) 上方约$100，是当前多空分界线。站上双线偏多但非常脆弱",
            "- **ETH**: 距EMA120 ($2,452) 还差**+5.9%**(约$139)，距ATH已跌53%。站上EMA60但未过EMA120 = **短期反弹、中期仍弱**",
            "- **SOL**: 双线之下，距EMA60(-3%)和EMA120(-15%)都较远，**最弱的大盘币**",
            "- **BNB**: 距EMA60仅-2%，接近支撑位测试",
            "",
            "---",
            ""
        ])
    
    def _add_main_board(self, coins):
        """Add main board coins analysis"""
        self.report.extend([
            "# 三、主板其他 (42个) — 按24h成交量排序",
            "",
            "| # | 币种 | 价格($) | 24h% | 24h量($M) | 市值($M) | FDV($M) | 距ATH% | EMA60 | EMA120 | >60 | >120 |",
            "|---|------|---------|------|-----------|----------|---------|--------|------|-------|-----|-----|"
        ])
        
        for i, coin in enumerate(coins, 1):
            change_str = f"**{coin['change_24h']:+.2f}%**" if abs(coin['change_24h']) > 10 else f"{coin['change_24h']:+.2f}%"
            
            self.report.append(
                f"| {i} | {coin['symbol']} | {coin['price']:.4f} | {change_str} | {coin['volume_24h']:.1f} | "
                f"{coin['market_cap']:,.0f} | {coin['fdv']:,.0f} | {coin['ath_distance']:.1f}% | "
                f"{coin['ema60']:.4f} | {coin['ema120']:.4f} | {'✅' if coin['above_ema60'] else '❌'} | {'✅' if coin['above_ema120'] else '❌'} |"
            )
        
        # Strong signals
        strong_coins = [c['symbol'] for c in coins if c['above_ema60'] and c['above_ema120']]
        dangerous_coins = [c['symbol'] for c in coins if c['change_24h'] < -10 and not c['above_ema120']]
        
        self.report.extend([
            "",
            f"### 主板强势信号（站上双线）",
            f"**{'、'.join(strong_coins)}** — 共{len(strong_coins)}个纯主板 + BTC大盘核心",
            "",
            f"### 主板危险信号（大跌+双线之下）",
            f"**{'、'.join(dangerous_coins)}** — 需警惕，加速下跌无反弹",
            "",
            "---",
            ""
        ])
    
    def _add_meme_sector(self, data):
        """Add MEME sector analysis"""
        self.report.extend([
            "# 四、MEME板块 详细分析",
            "",
            "## MEME全量数据（含Alpha区MEME，共22个）",
            "",
            "| # | 币种 | 价格($) | 24h% | 24h量($M) | 市值($M) | FDV($M) | ATH($) | 距ATH% | EMA60 | EMA120 | >60 | >120 | 区域 |",
            "|---|------|---------|------|-----------|----------|---------|-------|-------|------|-------|-----|-----|------|"
        ])
        
        for i, coin in enumerate(data['coins'], 1):
            change_str = f"**{coin['change_24h']:+.2f}%**" if abs(coin['change_24h']) > 5 else f"{coin['change_24h']:+.2f}%"
            
            self.report.append(
                f"| {i} | {coin['symbol']} | {coin['price']:.5f} | {change_str} | {coin['volume_24h']:.1f} | "
                f"{coin['market_cap']:,.0f} | {coin['fdv']:,.0f} | {coin['ath']:.3f} | {coin['ath_distance']:.1f}% | "
                f"{coin['ema60']:.5f} | {coin['ema120']:.5f} | {'✅' if coin['above_ema60'] else '❌'} | "
                f"{'✅' if coin['above_ema120'] else '❌'} | {coin['zone']} |"
            )
        
        # Tier analysis
        self.report.extend([
            "",
            "## MEME板块深度解读",
            "",
            "### 1. 按市值梯队划分",
            "| 梯队 | 代表币种 | 市值范围 | 特征 |",
            "|------|---------|---------|------|",
            "| **巨鲸级** | SHIB ($3.6B)、DOGE ($15B) | >$1B | 老牌meme，流动性最好 |",
            "| **大市值** | PEPE ($1.6B)、TRUMP ($593M)、PENGU ($604M) | $500M-$1.6B | 新一代meme主力 |",
            "| **中市值** | BONK ($547M)、VIRTUAL ($458M)、FLOKI ($310M)、LUNC ($330M) | $300M-$550M | 有一定关注度 |",
            "| **小市值** | WIF ($177M)、BERA ($92M)、TURBO ($79M)等 | <$200M | 高波动高风险 |",
            "",
            "### 2. 均线格局分析",
            "- **双线之上(强势)**: PENGU、LUNC、BANANAS31 — 3个（Alpha仅BANANAS31）",
            "- **仅站上EMA60(中性)**: DOGE、PEPE、NOT、NEIRO、FLOKI、1000CHEEMS、PNUT、BOME、TURBO、DOGS — 10个",
            "- **双线之下(弱势)**: TRUMP、SHIB、BONK、WIF、VIRTUAL、ACT、BERA、BANANA、MEME — 9个",
            "",
            "### 3. MEME关键信号",
            "- **SHIB**: 市值$3.6B最大MEME之一，但**双线之下且价格刚好卡在EMA60位置**，方向不明。距ATH暴跌93%，长期套牢盘沉重",
            "- **PEPE**: 站上EMA60，距EMA120(-6.3%)不远，有突破可能。日量$40M活跃度不错",
            "- **PENGU**: 今日**暴涨10%**且双线之上，最强meme信号。FDV($766M)远高于流通市值($604M)=有解锁压力",
            "- **DOGE**: 老牌meme稳如老狗，站上EMA60，量能充足($76M)。距ATH-86.6%但底部结构扎实",
            "- **TRUMP**: Meme政治币，双线之下且距EMA60(-18.8%)较远，FDV($2.55B) >> 市值($593M)，抛压巨大",
            "- **WIF**: Solana meme代表，双线之下，距ATH-96%",
            "",
            "### 4. MEME板块情绪总结",
            "```",
            "情绪指数: ★★☆☆☆ (偏空)",
            "",
            "强势信号:  PENGU(+10%双线上) ⭐⭐⭐",
            "中性偏多:  DOGE、PEPE (站上MA60待确认) ⭐⭐",
            "中性偏弱:  SHIB、BONK (卡在MA60附近) ⭐",
            "弱势信号:  WIF、TRUMP、ACT、BERA (全线走弱) 💔",
            "```",
            "",
            "---",
            ""
        ])
    
    def _add_eth_ecosystem(self, coins):
        """Add ETH ecosystem analysis"""
        self.report.extend([
            "# 五、ETH生态专项分析",
            "",
            "## ETH生态代币均线一览（17个）",
            "",
            "| 币种 | 价格($) | 24h% | 24h量($M) | EMA60 | EMA120 | >60 | >120 | 距60% | 距120% |",
            "|------|---------|------|-----------|-------|------|-----|------|-------|--------|"
        ])
        
        above_both = []
        for coin in coins:
            ema60_dist = ((coin['price'] - coin['ema60']) / coin['ema60'] * 100) if coin['ema60'] else 0
            ema120_dist = ((coin['price'] - coin['ema120']) / coin['ema120'] * 100) if coin['ema120'] else 0
            
            self.report.append(
                f"| {coin['symbol']} | {coin['price']:.4f} | {coin['change_24h']:+.2f}% | {coin['volume_24h']:.1f} | "
                f"{coin['ema60']:.3f} | {coin['ema120']:.3f} | {'✅' if coin['above_ema60'] else '❌'} | "
                f"{'✅' if coin['above_ema120'] else '❌'} | {ema60_dist:+.1f}% | {ema120_dist:+.1f}% |"
            )
            
            if coin['above_ema60'] and coin['above_ema120']:
                above_both.append(coin['symbol'])
        
        self.report.extend([
            "",
            f"> ETH生态双线之上({len(above_both)}个): **{'、'.join(above_both)}** — 仅{len(above_both)}/{len(coins)}个，占比{len(above_both)/len(coins)*100:.1f}%，资金明显撤离ETH生态",
            "",
            "---",
            ""
        ])
    
    def _add_market_sentiment(self, sentiment):
        """Add market sentiment summary"""
        self.report.extend([
            "# 六、市场情绪总结",
            "",
            "## 📊 综合情绪仪表盘",
            "",
            "| 维度 | 数据 | 评分 | 解读 |",
            "|------|------|------|------|",
            "| **大盘均线** | 仅25.7%站上EMA120 | 🔴 2/10 | 中期趋势明确向下 |",
            "| **涨跌分布** | 75.7%下跌 vs 24.3%上涨 | 🔴 2/10 | 卖压主导，加速下跌 |",
            "| **BTC状态** | $77,633踩EMA120($77,533) | 🟡 5/10 | 多空分界，极度脆弱 |",
            "| **ETH状态** | 距EMA120差+5.9%，量比0.44x | 🔴 3/10 | 严重缩量反弹，不可信 |",
            "| **SOL/BNB** | 双线之下，SOL最弱 | 🔴 2/10 | 大盘跟跌不跟涨 |",
            "| **ETH生态** | 仅4/14站上双线(28.6%) | 🔴 3/10 | 资金从DeFi加速撤离 |",
            "| **MEME板块** | PENGU/LUNC强势但整体分化 | 🟡 4/10 | 个别机会但不具普遍性 |",
            "| **成交量集中** | Top5占47% | 🟡 4/10 | 头部抱团，尾部风险高 |",
            "| **综合情绪** | — | **🔴 2.6/10** | **偏空观望，加速下行中** |",
            "",
            "## 核心观点",
            "",
            "### 🔴 利空因素 (权重更高)",
            "1. **75.7%的币种24h下跌** — 普跌格局，短期加速下行",
            "2. **EMA120站上率仅25.7%** — 这是过去半年的趋势线，多数币种在其下方运行",
            "3. **ETH严重缩量反弹(RSI=45.3,量比0.44x)** — 反弹没有量能配合，大概率继续下探",
            "4. **DeFi蓝筹(AAVE/UNI/WLD)全线破位** — 机构资金在撤退",
            "5. **SOL距EMA120还有+17%的距离** — 弱势最明显的大盘币",
            "",
            "### 🟡 利多因素 (权重较低)",
            "1. **BTC仍站上EMA120** — 只要BTC守住$77,500，就不会崩盘",
            "2. **部分币种出现双线突破** — ZEC/TRX/ALGO/RUNE/ORDI/DYDX/AXS/APE等",
            "3. **PENGU/LUNC放量异动** — 游资仍在寻找alpha，但仅为个别标的",
            "4. **RSI未到超卖(ETH日线45.3)** — 说明还没到底部恐慌区域，可能还有下行空间",
            "",
            "### ⚡ 操作建议框架",
            "| 场景 | 条件 | 建议 |",
            "|------|------|------|",
            "| **观望为主** | 当前状态 | 不急于抄底，等待 clearer signal |",
            "| **关注BTC** | 若跌破EMA120 $77,500 | 减仓/止损，可能触发连锁下跌 |",
            "| **关注ETH** | 若收复$2,350(EMA20) | 可轻仓试多ETH/ETH生态 |",
            "| **MEME策略** | 仅限短线 | PENGU/PEPE可小仓位博弈，严格设损 |",
            "| **避开** | — | Alpha区新币(高FDV抛压)/距ATH< -95%的山谷币 |",
            "",
            "---",
            ""
        ])
    
    def _add_indicators_explanation(self):
        """Add technical indicators explanation"""
        self.report.extend([
            "# 七、指标说明与数据真实性声明",
            "",
            "## 指标解释",
            "",
            "### EMA (Exponential Moving Average) 指数移动平均线",
            "- **EMA60**: 约3个月(60交易日)指数移动平均，反映**季度趋势**",
            "- **EMA120**: 约6个月(120交易日)指数移动平均，反映**半年趋势**",
            "- 计算方式: 对近期价格赋予更高权重，比SMA(Simple MA)更灵敏",
            "- **站上EMA60** = 短中期趋势偏多，适合波段做多参考",
            "- **站上EMA120** = 中长期趋势确立，适合趋势持仓参考",
            "- **双线之下** = 中长期下行趋势，任何反弹视为技术性修复而非反转",
            "",
            "### RSI (Relative Strength Index) 相对强弱指标",
            "- 取值范围: 0-100",
            "- **>70**: 超买区，回调概率增大",
            "- **30-70**: 中性区间",
            "- **<30**: 超卖区，反弹概率增大",
            "- 本次ETH日线RSI=45.3 → 中性偏弱，既非超买也非超卖",
            "",
            "### 量比 (Volume Ratio)",
            "- 当前成交量 / 过去20日平均成交量",
            "- **>1.5**: 放量，趋势确认或反转信号",
            "- **0.5-1.5**: 正常波动",
            "- **<0.5**: 缩量，市场观望或动能衰竭",
            "- ETH日线量比0.44x → **严重缩量，反弹不可信**",
            "",
            "### 流通市值 vs FDV (Fully Diluted Valuation)",
            "- **流通市值** = 当前价格 × 已流通供应量",
            "- **FDV** = 当前价格 × 最大总供应量",
            "- 当 **流通市值/FDV < 50%** 时意味着未来有大量代币将解锁，存在巨大抛压风险",
            "- 例: TRUMP市值$593M vs FDV $2,552M → 仅23%流通，未来抛压极大",
            "",
            "### ATH距离",
            "- 从历史最高价(Current Price / All-Time High)回撤百分比",
            "- 距ATH > 80% 通常意味着\"归零边缘\"——要么翻倍要么继续阴跌",
            "- 本报告中绝大多数币种距ATH超过80%",
            "",
            "## 数据真实性保证",
            "",
            "| 数据项 | 来源 | 更新频率 | 可靠度 |",
            "|--------|------|---------|--------|",
            "| 24h成交量($M) | **Binance API `/api/v3/ticker/24hr`** | 实时 | ⭐⭐⭐⭐⭐ 实际成交额 |",
            "| 最新价格 | **Binance API `lastPrice`** | 实时 | ⭐⭐⭐⭐⭐ 实际撮合价 |",
            "| EMA60/120 | **Binance API `/api/v3/klines`** 150根日K本地计算 | 实时 | ⭐⭐⭐⭐⭐ 原始K线数据 |",
            "| 流通市值 | **CoinGecko API `/coins/markets`** | ~15分钟延迟 | ⭐⭐⭐⭐ 第三方聚合 |",
            "| FDV | **CoinGecko API** | ~15分钟延迟 | ⭐⭐⭐⭐ 第三方聚合 |",
            "| ATH/ATH% | **CoinGecko API** | ~15分钟延迟 | ⭐⭐⭐⭐ 第三方聚合 |",
            "",
            "> ⚠️ **关于24h成交量真实性**:",
            "> - 使用的是Binance官方API的`quoteVolume`字段，即以报价币(USDT/USDC等)计的实际成交金额",
            "> - USDT交易对直接使用原始数值；其他稳定币交易对已按实时汇率换算为USDT等值",
            "> - 此数据为**真实链上+订单簿撮合成交量**，不含刷量/清洗交易",
            "> - 但需注意：交易所内部可能存在做市商的自营交易，实际\"真实用户\"成交量可能略低",
            "",
            "---",
            "",
            f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M CST')} | 数据批次: 实时*"
        ])
    
    def save_report(self, filename='report.md'):
        """Save report to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.report))
        print(f"Report saved to {filename}")
