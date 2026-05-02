#!/usr/bin/env python3
"""
获取Binance现货市场数据
"""

import requests
import json
import sys
from datetime import datetime, timedelta

BASE_URL = "https://api.binance.com"

def get_24h_ticker():
    """获取24小时行情数据"""
    endpoint = f"{BASE_URL}/api/v3/ticker/24hr"
    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching 24h ticker: {e}", file=sys.stderr)
        return None

def get_klines(symbol, interval="1d", limit=150):
    """获取K线数据用于计算EMA"""
    endpoint = f"{BASE_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching klines for {symbol}: {e}", file=sys.stderr)
        return None

def get_usdt_pairs(ticker_data):
    """筛选USDT交易对"""
    usdt_pairs = []
    for item in ticker_data:
        symbol = item['symbol']
        if symbol.endswith('USDT') and not symbol.startswith('USD'):
            # 排除稳定币和杠杆代币
            if not any(x in symbol for x in ['UP', 'DOWN', 'BULL', 'BEAR']):
                usdt_pairs.append(item)
    return usdt_pairs

def calculate_ema(prices, period):
    """计算指数移动平均线"""
    if len(prices) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = prices[0]
    
    for price in prices[1:]:
        ema = (price - ema) * multiplier + ema
    
    return ema

def main():
    print("正在获取Binance市场数据...")
    
    # 获取24h行情
    ticker_data = get_24h_ticker()
    if not ticker_data:
        print("获取数据失败")
        sys.exit(1)
    
    usdt_pairs = get_usdt_pairs(ticker_data)
    print(f"获取到 {len(usdt_pairs)} 个USDT交易对")
    
    # 获取BTC的K线数据示例
    btc_klines = get_klines("BTCUSDT")
    if btc_klines:
        closes = [float(k[4]) for k in btc_klines]
        ema60 = calculate_ema(closes[-60:], 60)
        ema120 = calculate_ema(closes[-120:], 120)
        print(f"BTC EMA60: {ema60:.2f}, EMA120: {ema120:.2f}")
    
    # 保存数据到文件
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_pairs": len(usdt_pairs),
        "data": usdt_pairs[:10]  # 只保存前10个作为示例
    }
    
    with open("binance_data.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("数据已保存到 binance_data.json")

if __name__ == "__main__":
    main()