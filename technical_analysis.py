import numpy as np
import pandas as pd

class TechnicalAnalyzer:
    """Technical analysis calculations"""
    
    @staticmethod
    def calculate_ema(prices, period):
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return None
        
        prices = np.array(prices, dtype=float)
        multiplier = 2 / (period + 1)
        ema = np.zeros_like(prices)
        ema[0] = prices[0]
        
        for i in range(1, len(prices)):
            ema[i] = (prices[i] - ema[i-1]) * multiplier + ema[i-1]
        
        return ema[-1]
    
    @staticmethod
    def calculate_rsi(prices, period=14):
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return None
        
        prices = np.array(prices, dtype=float)
        deltas = np.diff(prices)
        
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def calculate_volume_ratio(volumes, current_volume, period=20):
        """Calculate volume ratio (current vs average)"""
        if len(volumes) < period:
            return None
        
        avg_volume = np.mean(volumes[-period:])
        if avg_volume == 0:
            return 1.0
        
        return current_volume / avg_volume
    
    @staticmethod
    def calculate_ath_distance(current_price, ath_price):
        """Calculate distance from ATH in percentage"""
        if ath_price == 0 or ath_price is None:
            return None
        
        return ((current_price - ath_price) / ath_price) * 100
    
    @staticmethod
    def analyze_trend(price, ema60, ema120):
        """Analyze trend based on EMA positions"""
        above_ema60 = price > ema60 if ema60 else False
        above_ema120 = price > ema120 if ema120 else False
        
        if above_ema60 and above_ema120:
            return "bullish", "✅", "✅"
        elif above_ema60 and not above_ema120:
            return "neutral_bullish", "✅", "❌"
        elif not above_ema60 and above_ema120:
            return "neutral_bearish", "❌", "✅"
        else:
            return "bearish", "❌", "❌"
    
    @staticmethod
    def calculate_ema_distance(price, ema):
        """Calculate distance from EMA in percentage"""
        if ema is None or ema == 0:
            return None
        
        return ((price - ema) / ema) * 100
    
    @staticmethod
def calculate_market_sentiment(metrics):
        """Calculate overall market sentiment score (0-10)"""
        scores = []
        
        # EMA120 standing rate
        ema120_rate = metrics.get('ema120_standing_rate', 0)
        if ema120_rate > 60:
            scores.append(8)
        elif ema120_rate > 40:
            scores.append(6)
        elif ema120_rate > 25:
            scores.append(4)
        else:
            scores.append(2)
        
        # 24h change distribution
        rising_rate = metrics.get('rising_rate', 0)
        if rising_rate > 60:
            scores.append(8)
        elif rising_rate > 40:
            scores.append(6)
        elif rising_rate > 25:
            scores.append(4)
        else:
            scores.append(2)
        
        # BTC status
        btc_above_ema120 = metrics.get('btc_above_ema120', False)
        scores.append(5 if btc_above_ema120 else 2)
        
        # Volume concentration
        top5_ratio = metrics.get('top5_volume_ratio', 0)
        if top5_ratio > 60:
            scores.append(3)
        elif top5_ratio > 40:
            scores.append(4)
        else:
            scores.append(6)
        
        return np.mean(scores) if scores else 5.0
