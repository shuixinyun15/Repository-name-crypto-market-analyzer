#!/usr/bin/env python3
"""
使用示例
"""

from src.analyzer import CryptoMarketAnalyzer

# 创建分析器
analyzer = CryptoMarketAnalyzer('data/Binance.com数据模板.md')

# 运行分析
results = analyzer.run()

# 打印报告
report = analyzer.generate_report()
print(report)

# 导出JSON
analyzer.export_json('output/analysis_result.json')
