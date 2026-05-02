#!/usr/bin/env python3
"""
币安实时数据获取器
用于从Binance API获取实时市场数据
"""

import requests
import json
import time
import sys
from pathlib import Path
from datetime import datetime

class BinanceDataFetcher:
    """币安数据获取器"""
    
    BASE_URL = "https://api.binance.com"
    
    def __init__(self):
        self.session = requests.Session()
        
    def get_ticker_24h(self, symbol):
        """获取24小时行情数据"""
        endpoint = f"{self.BASE_URL}/api/v3/ticker/24hr"
        params = {'symbol': symbol}
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"⚠️ 获取{symbol}数据失败: {e}")
            return None
    
    def get_klines(self, symbol, interval='1d', limit=150):
        """获取K线数据"""
        endpoint = f"{self.BASE_URL}/api/v3/klines"
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"⚠️ 获取{symbol} K线数据失败: {e}")
            return None
    
    def calculate_ema(self, prices, period):
        """计算EMA"""
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
        
        # 获取24h数据
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
        ema120 = self.calculate_ema(closes[-120:], 120) if len(closes) >= 120 else None
        
        current_price = float(ticker['lastPrice'])
        
        result = {
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
        
        return result
    
    def generate_markdown_report(self, symbols, output_path=None):
        """生成Markdown报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M CST')
        
        report = f"""# 币安(Binance.com)现货市场综合分析报告 (实时)

**数据时间**: {timestamp}
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

| # | 币种 | 价格($) | 24h涨跌 | 24h量($M) | EMA60 | EMA120 | >MA60 | >MA120 |
|---|------|---------|---------|-----------|-------|--------|-------|--------|
"""
        
        results = []
        for i, symbol in enumerate(symbols, 1):
            result = self.analyze_symbol(symbol)
            if result:
                results.append(result)
                
                price = result['price']
                change = result['change_24h']
                volume = result['volume_24h'] / 1e6  # 转换为百万
                ema60 = result['ema60']
                ema120 = result['ema120']
                above60 = "✅" if result['above_ema60'] else "❌"
                above120 = "✅" if result['above_ema120'] else "❌"
                
                ema60_str = f"{ema60:,.2f}" if ema60 else 'N/A'
                ema120_str = f"{ema120:,.2f}" if ema120 else 'N/A'
                
                report += f"| {i} | **{symbol}** | {price:,.2f} | {change} | {volume:.1f} | {ema60_str} | {ema120_str} | {above60} | {above120} |\n"
        
        report += f"""
---

# 三、市场情绪总结

## 📊 综合情绪仪表盘

| 维度 | 数据 | 评分 | 解读 |
|------|------|------|------|
| **数据新鲜度** | 实时 | 🟢 10/10 | API实时数据 |
| **币种覆盖** | {len(symbols)}个 | 🟢 8/10 | 主要币种 |

## ⚡ 关键信号

- 数据获取时间: {timestamp}
- 数据来源: Binance API

## 📋 操作建议框架

| 场景 | 建议 |
|------|------|
| **实时数据** | 关注EMA交叉信号 |
| **趋势判断** | 结合多时间周期分析 |

---

*报告生成时间: {timestamp} | 数据来源: Binance API*
"""
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 报告已保存到: {output_path}")
        
        return report
    
    def export_json(self, results, output_path):
        """导出JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON数据已导出到: {output_path}")


def main():
    """主函数"""
    # 主要交易对
    major_symbols = [
        'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT',
        'DOGEUSDT', 'XRPUSDT', 'ADAUSDT', 'AVAXUSDT',
        'LINKUSDT', 'DOTUSDT', 'MATICUSDT', 'UNIUSDT'
    ]
    
    fetcher = BinanceDataFetcher()
    
    print("🚀 开始获取币安实时数据...\n")
    
    # 生成报告
    report_path = Path('data/latest_report.md')
    report_path.parent.mkdir(exist_ok=True)
    
    report = fetcher.generate_markdown_report(major_symbols, str(report_path))
    
    # 分析所有币种
    results = []
    for symbol in major_symbols:
        result = fetcher.analyze_symbol(symbol)
        if result:
            results.append(result)
        time.sleep(0.5)  # 避免请求过快
    
    # 导出JSON
    json_path = Path('output/realtime_data.json')
    json_path.parent.mkdir(exist_ok=True)
    fetcher.export_json(results, str(json_path))
    
    print("\n✅ 实时报告生成完成!")
    print(f"📄 文件位置: {report_path}")
    print(f"📊 JSON数据: {json_path}")


if __name__ == '__main__':
    main()
