#!/usr/bin/env python3
"""
币安实时数据获取工具
通过Binance API获取最新市场数据并生成分析报告
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

class BinanceDataFetcher:
    """币安数据获取器"""
    
    def __init__(self):
        self.base_url = "https://api.binance.com"
        self.session = requests.Session()
        
    def get_ticker_24h(self, symbol=None):
        """获取24小时行情数据"""
        endpoint = "/api/v3/ticker/24hr"
        params = {}
        if symbol:
            params['symbol'] = symbol
            
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ 获取24h行情失败: {e}")
            return None
            
    def get_klines(self, symbol, interval='1d', limit=150):
        """获取K线数据用于计算EMA"""
        endpoint = "/api/v3/klines"
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ 获取K线数据失败 ({symbol}): {e}")
            return None
            
    def calculate_ema(self, prices, period):
        """计算指数移动平均线"""
        if len(prices) < period:
            return None
            
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema
            
        return ema
        
    def analyze_symbol(self, symbol):
        """分析单个币种"""
        print(f"📊 分析 {symbol}...")
        
        # 获取24h行情
        ticker = self.get_ticker_24h(symbol)
        if not ticker:
            return None
            
        # 获取K线数据
        klines = self.get_klines(symbol)
        if not klines:
            return None
            
        # 提取收盘价
        closes = [float(k[4]) for k in klines]
        
        # 计算EMA
        ema60 = self.calculate_ema(closes[-60:], 60) if len(closes) >= 60 else None
        ema120 = self.calculate_ema(closes, 120) if len(closes) >= 120 else None
        
        current_price = float(ticker['lastPrice'])
        
        analysis = {
            'symbol': symbol,
            'price': current_price,
            'change_24h': f"{float(ticker['priceChangePercent']):.2f}%",
            'volume_24h': float(ticker['quoteVolume']),
            'ema60': ema60,
            'ema120': ema120,
            'above_ema60': current_price > ema60 if ema60 else None,
            'above_ema120': current_price > ema120 if ema120 else None,
            'high_24h': float(ticker['highPrice']),
            'low_24h': float(ticker['lowPrice'])
        }
        
        return analysis
        
    def generate_markdown_report(self, symbols, output_path='data/latest_report.md'):
        """生成Markdown格式报告"""
        
        report_time = datetime.now().strftime("%Y-%m-%d %H:%M CST")
        
        report = f"""# 币安(Binance.com)现货市场综合分析报告 (实时)

**数据时间**: {report_time}
**数据来源**: Binance API (实时行情/K线)
**⚠️ 注意**: 本报告基于实时API数据生成
**筛选条件**: USDT交易对

---

# 一、总览统计

| 指标 | 数值 | 说明 |
|------|------|------|
| 分析币种数 | **{len(symbols)}** | |
| 数据状态 | 实时 | |

---

# 二、大盘核心分析

"""
        
        # 分析每个币种
        results = []
        for symbol in symbols:
            analysis = self.analyze_symbol(symbol)
            if analysis:
                results.append(analysis)
            time.sleep(0.1)  # 避免请求过快
            
        # 生成大盘核心表格
        report += "| # | 币种 | 价格($) | 24h涨跌 | 24h量($M) | EMA60 | EMA120 | >MA60 | >MA120 |\n"
        report += "|---|------|---------|---------|-----------|-------|--------|-------|--------|\n"
        
        for i, result in enumerate(results[:4], 1):
            symbol = result['symbol'].replace('USDT', '')
            price = result['price']
            change = result['change_24h']
            volume = result['volume_24h'] / 1e6  # 转换为百万
            ema60 = result['ema60']
            ema120 = result['ema120']
            above60 = "✅" if result['above_ema60'] else "❌"
            above120 = "✅" if result['above_ema120'] else "❌"
            
            report += f"| {i} | **{symbol}** | {price:,.2f} | {change} | {volume:.1f} | {ema60:,.2f if ema60 else 'N/A'} | {ema120:,.2f if ema120 else 'N/A'} | {above60} | {above120} |\n"
            
        report += f"""
---

# 三、市场情绪总结

## 📊 综合情绪仪表盘

| 维度 | 数据 | 评分 | 解读 |
|------|------|------|------|
| **数据新鲜度** | 实时 | 🟢 10/10 | API实时数据 |
| **币种覆盖** | {len(symbols)}个 | 🟢 8/10 | 主要币种 |

## ⚡ 关键信号

- 数据获取时间: {report_time}
- 数据来源: Binance API

## 📋 操作建议框架

| 场景 | 建议 |
|------|------|
| **实时数据** | 关注EMA交叉信号 |
| **趋势判断** | 结合多时间周期分析 |

---

*报告生成时间: {report_time} | 数据来源: Binance API*
"""
        
        # 保存报告
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"✅ 报告已保存到: {output_file}")
        return output_file


def main():
    """主函数"""
    print("🚀 开始获取币安实时数据...\n")
    
    # 主要交易对
    symbols = [
        'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT',
        'DOGEUSDT', 'XRPUSDT', 'ADAUSDT', 'AVAXUSDT',
        'LINKUSDT', 'DOTUSDT', 'MATICUSDT', 'UNIUSDT'
    ]
    
    fetcher = BinanceDataFetcher()
    
    # 生成报告
    report_path = fetcher.generate_markdown_report(symbols)
    
    if report_path:
        print(f"\n✅ 实时报告生成完成!")
        print(f"📄 文件位置: {report_path}")
    else:
        print(f"\n❌ 报告生成失败!")


if __name__ == "__main__":
    main()
