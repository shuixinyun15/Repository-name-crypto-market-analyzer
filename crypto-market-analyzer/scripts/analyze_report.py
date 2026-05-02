#!/usr/bin/env python3
"""
币安市场分析脚本
用法: python analyze_report.py [报告文件路径]
"""

import sys
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from analyzer import CryptoMarketAnalyzer

def main():
    """主函数"""
    # 默认报告路径
    default_path = Path(__file__).parent.parent / 'data' / 'Binance.com数据模板.md'
    
    # 支持命令行参数
    if len(sys.argv) > 1:
        report_path = sys.argv[1]
    else:
        report_path = default_path
        
    print(f"📊 币安市场分析工具")
    print(f"{'='*50}")
    print(f"报告路径: {report_path}\n")
    
    # 创建分析器并运行
    analyzer = CryptoMarketAnalyzer(report_path)
    
    if analyzer.run():
        # 导出JSON
        output_path = Path(__file__).parent.parent / 'output' / 'analysis_result.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        analyzer.export_json(output_path)
        print(f"\n✅ 分析完成!")
        print(f"📤 JSON输出: {output_path}")
    else:
        print(f"\n❌ 分析失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()
