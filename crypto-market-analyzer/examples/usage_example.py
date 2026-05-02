#!/usr/bin/env python3
"""
使用示例 - 展示如何使用CryptoMarketAnalyzer
"""

import sys
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from analyzer import CryptoMarketAnalyzer

def example_basic_usage():
    """基础使用示例"""
    print("="*60)
    print("示例1: 基础分析")
    print("="*60)
    
    # 创建分析器
    report_path = Path(__file__).parent.parent / 'data' / 'Binance.com数据模板.md'
    analyzer = CryptoMarketAnalyzer(report_path)
    
    # 运行分析
    if analyzer.run():
        # 导出JSON数据
        output_path = Path(__file__).parent.parent / 'output' / 'example_output.json'
        analyzer.export_json(output_path)
        print(f"\n✅ 分析完成，数据已导出到: {output_path}")
    
def example_custom_analysis():
    """自定义分析示例"""
    print("\n" + "="*60)
    print("示例2: 自定义分析")
    print("="*60)
    
    report_path = Path(__file__).parent.parent / 'data' / 'Binance.com数据模板.md'
    analyzer = CryptoMarketAnalyzer(report_path)
    
    # 手动加载和解析
    if analyzer.load_report():
        analyzer.extract_metadata()
        analyzer.extract_overview_stats()
        analyzer.extract_major_coins()
        
        # 访问解析的数据
        print(f"\n📅 报告时间: {analyzer.parsed_data.get('report_time')}")
        print(f"📊 总览统计: {analyzer.parsed_data.get('overview', {})}")
        print(f"💰 大盘币种数: {len(analyzer.parsed_data.get('major_coins', []))}")
        
        # 获取特定币种信息
        for coin in analyzer.parsed_data.get('major_coins', []):
            print(f"\n{coin['symbol']}:")
            print(f"  价格: ${coin['price']:,.2f}")
            print(f"  24h变化: {coin['change_24h']}")
            print(f"  EMA60: ${coin['ema60']:,.2f}")
            print(f"  EMA120: ${coin['ema120']:,.2f}")
            print(f"  趋势: {'强势' if coin['above_ema60'] and coin['above_ema120'] else '弱势'}")

def example_data_export():
    """数据导出示例"""
    print("\n" + "="*60)
    print("示例3: 数据导出")
    print("="*60)
    
    report_path = Path(__file__).parent.parent / 'data' / 'Binance.com数据模板.md'
    analyzer = CryptoMarketAnalyzer(report_path)
    
    if analyzer.run():
        # 导出到不同位置
        import json
        
        # 获取分析数据
        data = {
            'metadata': {
                'report_time': analyzer.parsed_data.get('report_time'),
                'data_source': analyzer.parsed_data.get('data_source')
            },
            'market_sentiment': analyzer.analysis.get('market_sentiment'),
            'key_signals': analyzer.analysis.get('key_signals'),
            'recommendations': analyzer.analysis.get('recommendations')
        }
        
        # 保存为JSON
        output_path = Path(__file__).parent.parent / 'output' / 'custom_export.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"\n✅ 自定义导出完成: {output_path}")
        print(f"📊 导出内容:")
        print(f"  - 市场情绪评分: {data['market_sentiment']['score']}/10")
        print(f"  - 关键信号数: {len(data['key_signals'])}")
        print(f"  - 建议数: {len(data['recommendations'])}")

if __name__ == "__main__":
    print("🚀 CryptoMarketAnalyzer 使用示例\n")
    
    example_basic_usage()
    example_custom_analysis()
    example_data_export()
    
    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
