#!/usr/bin/env python3
"""
单元测试
"""

import unittest
from src.analyzer import CryptoMarketAnalyzer

class TestCryptoMarketAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = {
            'major_coins': [
                {
                    'symbol': 'BTC',
                    'price': 77633,
                    'change_24h': '-0.55%',
                    'above_ema60': True,
                    'above_ema120': True
                },
                {
                    'symbol': 'ETH',
                    'price': 2313,
                    'change_24h': '-0.74%',
                    'above_ema60': True,
                    'above_ema120': False
                }
            ],
            'meme_coins': [
                {
                    'symbol': 'DOGE',
                    'price': 0.0981,
                    'change_24h': '-0.32%',
                    'above_ema60': True,
                    'above_ema120': False
                }
            ]
        }
        self.analyzer = CryptoMarketAnalyzer(self.sample_data)
    
    def test_load_data(self):
        """测试数据加载"""
        self.analyzer.load_data()
        self.assertIsNotNone(self.analyzer.data)
        self.assertEqual(len(self.analyzer.data['major_coins']), 2)
    
    def test_analyze_major_coins(self):
        """测试大盘核心分析"""
        self.analyzer.load_data()
        result = self.analyzer.analyze_major_coins()
        
        self.assertEqual(result['total'], 2)
        self.assertEqual(result['above_both_lines'], 1)
        self.assertEqual(result['above_ema60_only'], 1)
        self.assertEqual(result['below_both_lines'], 0)
    
    def test_calculate_market_sentiment(self):
        """测试市场情绪计算"""
        self.analyzer.load_data()
        sentiment = self.analyzer.calculate_market_sentiment()
        
        self.assertIn('score', sentiment)
        self.assertIn('status', sentiment)
        self.assertGreaterEqual(sentiment['score'], 0)
        self.assertLessEqual(sentiment['score'], 10)
    
    def test_generate_report(self):
        """测试报告生成"""
        self.analyzer.run()
        report = self.analyzer.generate_report()
        
        self.assertIn('币安市场分析报告', report)
        self.assertIn('BTC', report)

if __name__ == '__main__':
    unittest.main()
