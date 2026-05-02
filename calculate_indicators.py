#!/usr/bin/env python3
"""
计算技术指标：EMA、RSI、量比
"""

import numpy as np
from typing import List, Optional

def calculate_ema(prices: List[float], period: int) -> Optional[float]:
    """
    计算指数移动平均线 (EMA)
    
    Args:
        prices: 价格列表（收盘价）
        period: 周期（60或120）
    
    Returns:
        EMA值
    """
    if len(prices) < period:
        return None
    
    prices_array = np.array(prices[-period:])
    multiplier = 2 / (period + 1)
    
    ema = prices_array[0]
    for price in prices_array[1:]:
        ema = (price - ema) * multiplier + ema
    
    return float(ema)

def calculate_ema_series(prices: List[float], period: int) -> List[float]:
    """
    计算EMA序列
    """
    if len(prices) < period:
        return []
    
    ema_series = []
    multiplier = 2 / (period + 1)
    
    # 使用SMA作为初始EMA
    ema = sum(prices[:period]) / period
    ema_series.append(ema)
    
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
        ema_series.append(ema)
    
    return ema_series

def calculate_rsi(prices: List[float], period: int = 14) -> Optional[float]:
    """
    计算相对强弱指标 (RSI)
    
    Args:
        prices: 价格列表
        period: RSI周期（默认14）
    
    Returns:
        RSI值 (0-100)
    """
    if len(prices) < period + 1:
        return None
    
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return float(rsi)

def calculate_volume_ratio(volumes: List[float]) -> Optional[float]:
    """
    计算量比（当前成交量 / 20日平均成交量）
    
    Args:
        volumes: 成交量列表（最近21日，最后一个是今日）
    
    Returns:
        量比值
    """
    if len(volumes) < 21:
        return None
    
    current_volume = volumes[-1]
    avg_volume = np.mean(volumes[-21:-1])  # 过去20日平均
    
    if avg_volume == 0:
        return None
    
    return float(current_volume / avg_volume)

def check_ma_position(current_price: float, ema60: float, ema120: float) -> dict:
    """
    检查价格与均线的位置关系
    
    Returns:
        {
            'above_ema60': bool,
            'above_ema120': bool,
            'trend': str  # 'bullish', 'bearish', 'neutral'
        }
    """
    above_ema60 = current_price > ema60
    above_ema120 = current_price > ema120
    
    if above_ema60 and above_ema120:
        trend = 'bullish'
    elif not above_ema60 and not above_ema120:
        trend = 'bearish'
    else:
        trend = 'neutral'
    
    return {
        'above_ema60': above_ema60,
        'above_ema120': above_ema120,
        'trend': trend,
        'distance_to_ema60': (current_price - ema60) / ema60 * 100,
        'distance_to_ema120': (current_price - ema120) / ema120 * 100
    }

def main():
    """测试计算"""
    # 模拟BTC价格数据（最近150日）
    np.random.seed(42)
    base_price = 75000
    prices = [base_price]
    
    for _ in range(149):
        change = np.random.normal(0, 0.02)  # 2%日波动
        new_price = prices[-1] * (1 + change)
        prices.append(new_price)
    
    # 计算指标
    ema60 = calculate_ema(prices, 60)
    ema120 = calculate_ema(prices, 120)
    rsi = calculate_rsi(prices)
    
    current_price = prices[-1]
    position = check_ma_position(current_price, ema60, ema120)
    
    print(f"当前价格: ${current_price:.2f}")
    print(f"EMA60: ${ema60:.2f}")
    print(f"EMA120: ${ema120:.2f}")
    print(f"RSI(14): {rsi:.2f}")
    print(f"趋势: {position['trend']}")
    print(f"距EMA60: {position['distance_to_ema60']:.2f}%")
    print(f"距EMA120: {position['distance_to_ema120']:.2f}%")

if __name__ == "__main__":
    main()