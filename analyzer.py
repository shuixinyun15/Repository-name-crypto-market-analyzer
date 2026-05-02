#!/usr/bin/env python3
"""
币安市场分析器
用于分析加密货币市场数据
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

class CryptoMarketAnalyzer:
    """加密货币市场分析器"""
    
    def __init__(self, data_source):
        self.data_source = data_source
        self.data = None
        self.analysis_results = {}
        
    def load_data(self):
        """加载数据"""
        if isinstance(self.data_source, str):
            path = Path(self.data_source)
            if path.suffix == '.json':
                with open(path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            elif path.suffix == '.md':
                # 解析Markdown报告
                self.data = self.parse_markdown_report(path)
        elif isinstance(self.data_source, dict):
            self.data = self.data_source
        
        return self
    
    def parse_markdown_report(self, path):
        """解析Markdown报告"""
        # 这里可以调用parse_report.py的功能
        # 简化版本，直接返回空数据结构
        return {
            'major_coins': [],
            'mainboard_others': [],
            'meme_coins': [],
            'eth_ecosystem': []
        }
    
    def analyze_major_coins(self):
        """分析大盘核心币种"""
        if not self.data or 'major_coins' not in self.data:
            return {}
        
        coins = self.data['major_coins']
        analysis = {
            'total': len(coins),
            'above_both_lines': 0,
            'above_ema60_only': 0,
            'below_both_lines': 0,
            'strongest': None,
            'weakest': None
        }
        
        for coin in coins:
            if coin.get('above_ema60') and coin.get('above_ema120'):
                analysis['above_both_lines'] += 1
            elif coin.get('above_ema60'):
                analysis['above_ema60_only'] += 1
            else:
                analysis['below_both_lines'] += 1
        
        # 找出最强和最弱
        if coins:
            sorted_by_change = sorted(coins, key=lambda x: float(x.get('change_24h', '0%').replace('%', '')), reverse=True)
            analysis['strongest'] = sorted_by_change[0] if sorted_by_change else None
            analysis['weakest'] = sorted_by_change[-1] if sorted_by_change else None
        
        return analysis
    
    def analyze_meme_coins(self):
        """分析MEME板块"""
        if not self.data or 'meme_coins' not in self.data:
            return {}
        
        coins = self.data['meme_coins']
        analysis = {
            'total': len(coins),
            'strongest': [],
            'neutral': [],
            'weakest': []
        }
        
        for coin in coins:
            if coin.get('above_ema60') and coin.get('above_ema120'):
                analysis['strongest'].append(coin)
            elif coin.get('above_ema60'):
                analysis['neutral'].append(coin)
            else:
                analysis['weakest'].append(coin)
        
        return analysis
    
    def calculate_market_sentiment(self):
        """计算市场情绪"""
        sentiment = {
            'score': 5.0,
            'status': '中性',
            'factors': []
        }
        
        # 分析大盘核心
        major_analysis = self.analyze_major_coins()
        
        if major_analysis.get('above_both_lines', 0) >= 3:
            sentiment['score'] += 2
            sentiment['factors'].append('大盘核心多数站上双线')
        elif major_analysis.get('below_both_lines', 0) >= 3:
            sentiment['score'] -= 2
            sentiment['factors'].append('大盘核心多数双线之下')
        
        # 分析MEME板块
        meme_analysis = self.analyze_meme_coins()
        
        if meme_analysis.get('strongest', []):
            sentiment['score'] += 1
            sentiment['factors'].append('MEME板块有强势币种')
        
        # 限制分数范围
        sentiment['score'] = max(0, min(10, sentiment['score']))
        
        # 根据分数确定状态
        if sentiment['score'] >= 7:
            sentiment['status'] = '偏多'
        elif sentiment['score'] <= 3:
            sentiment['status'] = '偏空'
        else:
            sentiment['status'] = '中性'
        
        return sentiment
    
    def run(self):
        """运行完整分析"""
        self.load_data()
        
        self.analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'major_coins_analysis': self.analyze_major_coins(),
            'meme_coins_analysis': self.analyze_meme_coins(),
            'market_sentiment': self.calculate_market_sentiment()
        }
        
        return self.analysis_results
    
    def export_json(self, output_path):
        """导出JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)
        return output_path
    
    def generate_report(self):
        """生成分析报告"""
        results = self.analysis_results
        sentiment = results.get('market_sentiment', {})
        major = results.get('major_coins_analysis', {})
        
        report = f"""
📊 币安市场分析报告
========================

📅 分析时间: {results.get('timestamp', 'N/A')}

🎯 市场情绪: {sentiment.get('score', 'N/A')}/10 ({sentiment.get('status', 'N/A')})

💰 大盘核心分析:
  - 总币种数: {major.get('total', 0)}
  - 双线之上: {major.get('above_both_lines', 0)}
  - 仅EMA60: {major.get('above_ema60_only', 0)}
  - 双线之下: {major.get('below_both_lines', 0)}

⚡ 关键信号:
"""
        
        for factor in sentiment.get('factors', []):
            report += f"  - {factor}\n"
        
        if major.get('strongest'):
            strongest = major['strongest']
            report += f"\n📈 最强币种: {strongest.get('symbol', 'N/A')} ({strongest.get('change_24h', 'N/A')})\n"
        
        if major.get('weakest'):
            weakest = major['weakest']
            report += f"📉 最弱币种: {weakest.get('symbol', 'N/A')} ({weakest.get('change_24h', 'N/A')})\n"
        
        report += "\n========================\n"
        
        return report


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python analyzer.py <数据文件路径>")
        sys.exit(1)
    
    data_path = sys.argv[1]
    
    print(f"📊 正在分析数据: {data_path}")
    
    analyzer = CryptoMarketAnalyzer(data_path)
    results = analyzer.run()
    
    # 生成报告
    report = analyzer.generate_report()
    print(report)
    
    # 导出JSON
    output_path = Path('output/analysis_result.json')
    output_path.parent.mkdir(exist_ok=True)
    analyzer.export_json(str(output_path))
    
    print(f"✅ 分析完成!")
    print(f"📊 JSON输出: {output_path}")


if __name__ == '__main__':
    main()
