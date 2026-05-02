import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time

class BinanceAPI:
    """Binance API client for market data"""
    
    BASE_URL = "https://api.binance.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoMarketAnalyzer/1.0'
        })
    
    def get_24h_ticker(self, symbol=None):
        """Get 24 hour price change statistics"""
        endpoint = f"{self.BASE_URL}/api/v3/ticker/24hr"
        params = {}
        if symbol:
            params['symbol'] = symbol
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching 24h ticker: {e}")
            return None
    
    def get_klines(self, symbol, interval='1d', limit=150):
        """Get kline/candlestick data"""
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
        except Exception as e:
            print(f"Error fetching klines for {symbol}: {e}")
            return None
    
    def get_exchange_info(self):
        """Get exchange information including trading pairs"""
        endpoint = f"{self.BASE_URL}/api/v3/exchangeInfo"
        
        try:
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching exchange info: {e}")
            return None


class CoinGeckoAPI:
    """CoinGecko API client for market cap and FDV data"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoMarketAnalyzer/1.0'
        })
    
    def get_coins_markets(self, ids=None, vs_currency='usd', per_page=250):
        """Get coins market data including market cap and FDV"""
        endpoint = f"{self.BASE_URL}/coins/markets"
        params = {
            'vs_currency': vs_currency,
            'order': 'market_cap_desc',
            'per_page': per_page,
            'page': 1,
            'sparkline': 'false',
            'price_change_percentage': '24h'
        }
        
        if ids:
            params['ids'] = ','.join(ids)
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching CoinGecko markets: {e}")
            return None
    
    def get_coin_data(self, coin_id):
        """Get detailed coin data including ATH"""
        endpoint = f"{self.BASE_URL}/coins/{coin_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'market_data': 'true',
            'community_data': 'false',
            'developer_data': 'false'
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching coin data for {coin_id}: {e}")
            return None
