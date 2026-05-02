#!/usr/bin/env python3
"""
生成加密货币市场分析报告
"""

import json
import sys
from datetime import datetime
from typing import List, Dict

def generate_market_overview(data: List[Dict]) -> str:
    """生成市场总览"""
    total_pairs = len(data)
    
    # 统计涨跌
    up_count = sum(1 for item in data if float(item.get('priceChangePercent', 0)) > 0)
    down_count = total_pairs - up_count
    
    # 计算总成交量
    total_volume = sum(float(item.get('quoteVolume', 0)) for item in data)
    
    # 找出Top5成交量
    sorted_by_volume = sorted(data, key=lambda x: float(x.get('quoteVolume', 0)), reverse=True)
    top5 = sorted_by_volume[:5]
    top5_volume = sum(float(item.get('quoteVolume', 0)) for item in top5)
    top5_ratio = (top5_volume / total_volume * 100) if total_volume > 0 else 0
    
    report = f"""# 币安现货市场综合分析报告

**数据时间**: {datetime.now().strftime('%Y-%m-%d %H:%M CST')}
**数据来源**: Binance API
**筛选条件**: USDT交易对

---

# 一、总览统计

| 指标 | 数值 | 说明 |
|------|------|------|
| 主板币种总数 | **{total_pairs}** | USDT交易对 |
| 总24h成交量 | **${total_volume/1e6:.1f}M** | |
| 24h上涨 | {up_count}/{total_pairs} (**{up_count/total_pairs*100:.1f}%**) | |
| 24h下跌 | {down_count}/{total_pairs} (**{down_count/total_pairs*100:.1f}%**) | |
| Top5成交量占比 | **{top5_ratio:.1f}%** | 头部集中度 |

"""
    
    # 市场判断
    if down_count / total_pairs > 0.7:
        trend = "🔴 市场整体偏空，多数币种下跌"
    elif up_count / total_pairs > 0.6:
        trend = "🟢 市场整体偏多，多数币种上涨"
    else:
        trend = "🟡 市场震荡，涨跌分化"
    
    report += f"> **核心判断**: {trend}\n\n"
    
    return report

def generate_large_cap_analysis(data: List[Dict]) -> str:
    """生成大盘核心分析"""
    large_caps = ['BTC', 'ETH', 'SOL', 'BNB']
    
    report = "# 二、大盘核心 — BTC / ETH / SOL / BNB\n\n"
    report += "| 币种 | 价格($) | 24h涨跌 | 24h量($M) | 市值($B) | 趋势 |\n"
    report += "|------|---------|---------|-----------|----------|------|\n"
    
    for symbol in large_caps:
        item = next((x for x in data if x['symbol'] == f"{symbol}USDT"), None)
        if item:
            price = float(item.get('lastPrice', 0))
            change = float(item.get('priceChangePercent', 0))
            volume = float(item.get('quoteVolume', 0)) / 1e6
            market_cap = price * float(item.get('circulatingSupply', 0)) / 1e9 if 'circulatingSupply' in item else 0
            
            trend = "🟢" if change > 0 else "🔴" if change < -2 else "🟡"
            
            report += f"| {symbol} | ${price:,.0f} | {change:+.2f}% | {volume:.1f} | {market_cap:.1f} | {trend} |\n"
    
    report += "\n### 大盘关键信号\n\n"
    report += "- **BTC**: 市场风向标，关注$75,000-$80,000区间\n"
    report += "- **ETH**: DeFi生态核心，关注$2,000-$2,500支撑\n"
    report += "- **SOL**: 高性能公链代表，关注$80-$100区间\n"
    report += "- **BNB**: 平台币龙头，关注$600-$700支撑\n\n"
    
    return report

def generate_sector_analysis(data: List[Dict]) -> str:
    """生成板块分析"""
    
    # MEME板块
    meme_coins = ['DOGE', 'SHIB', 'PEPE', 'PENGU', 'LUNC', 'TRUMP', 'NOT', 'BONK', 'WIF']
    
    report = "# 三、板块分析\n\n"
    report += "## MEME板块\n\n"
    report += "| 币种 | 价格($) | 24h% | 24h量($M) | 市值($M) |\n"
    report += "|------|---------|------|-----------|----------|\n"
    
    for symbol in meme_coins:
        item = next((x for x in data if x['symbol'] == f"{symbol}USDT"), None)
        if item:
            price = float(item.get('lastPrice', 0))
            change = float(item.get('priceChangePercent', 0))
            volume = float(item.get('quoteVolume', 0)) / 1e6
            
            # 简化市值计算
            market_cap = 0
            
            report += f"| {symbol} | ${price:.6f}" if price < 0.01 else f"| {symbol} | ${price:.2f}"
            report += f" | {change:+.2f}% | {volume:.1f} | {market_cap:.0f} |\n"
    
    return report

def generate_sentiment_score(data: List[Dict]) -> str:
    """生成市场情绪评分"""
    
    # 简单评分逻辑
    up_count = sum(1 for item in data if float(item.get('priceChangePercent', 0)) > 0)
    total = len(data)
    
    score = (up_count / total) * 10 if total > 0 else 5
    
    report = "# 四、市场情绪总结\n\n"
    report += f"## 📊 综合情绪仪表盘\n\n"
    report += f"| 维度 | 数据 | 评分 |\n"
    report += f"|------|------|------|\n"
    report += f"| **涨跌分布** | {up_count}/{total}上涨 | {'🟢' if score > 6 else '🔴' if score < 4 else '🟡'} {score:.1f}/10 |\n\n"
    
    report += "### 核心观点\n\n"
    if score > 7:
        report += "🟢 **偏多**: 多数币种上涨，市场情绪积极\n"
    elif score < 3:
        report += "🔴 **偏空**: 多数币种下跌，市场情绪谨慎\n"
    else:
        report += "🟡 **震荡**: 涨跌分化，等待明确方向\n"
    
    report += "\n### ⚡ 操作建议框架\n\n"
    report += "| 场景 | 建议 |\n"
    report += "|------|------|\n"
    report += "| 观望为主 | 等待 clearer signal |\n"
    report += "| 轻仓试多 | 仅限站上EMA60的强势币种 |\n"
    report += "| 严格止损 | 任何仓位都需设好止损位 |\n\n"
    
    return report

def generate_full_report(data: List[Dict]) -> str:
    """生成完整报告"""
    report = ""
    report += generate_market_overview(data)
    report += generate_large_cap_analysis(data)
    report += generate_sector_analysis(data)
    report += generate_sentiment_score(data)
    
    report += "---\n\n"
    report += "*免责声明: 本报告仅供参考，不构成投资建议。加密货币市场风险极高，投资需谨慎。*\n"
    
    return report

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python generate_report.py <数据文件>")
        print("示例: python generate_report.py binance_data.json")
        sys.exit(1)
    
    data_file = sys.argv[1]
    
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取数据文件失败: {e}")
        sys.exit(1)
    
    # 生成报告
    report = generate_full_report(data.get('data', []))
    
    # 输出到文件
    output_file = f"crypto_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"报告已生成: {output_file}")
    print("\n" + "="*50)
    print(report[:500] + "...")

if __name__ == "__main__":
    main()
