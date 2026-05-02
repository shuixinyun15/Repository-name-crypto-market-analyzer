# 加密货币市场分析器测试

import sys
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from analyzer import CryptoMarketAnalyzer

def test_load_report():
    """测试报告加载"""
    print("测试1: 报告加载")
    
    report_path = Path(__file__).parent.parent / 'data' / 'Binance.com数据模板.md'
    analyzer = CryptoMarketAnalyzer(report_path)
    
    assert analyzer.load_report() == True
    print("✅ 报告加载测试通过")
    
def test_extract_metadata():
    """测试元数据提取"""
    print("\n测试2: 元数据提取")
    
    report_path = Path(__file__).parent.parent / 'data' / 'Binance.com数据模板.md'
    analyzer = CryptoMarketAnalyzer(report_path)
    
    if analyzer.load_report():
        analyzer.extract_metadata()
        
        assert 'report_time' in analyzer.parsed_data
        assert 'data_source' in analyzer.parsed_data
        print("✅ 元数据提取测试通过")
        
def test_extract_overview():
    """测试总览统计提取"""
    print("\n测试3: 总览统计提取")
    
    report_path = Path(__file__).parent.parent / 'data' / 'Binance.com数据模板.md'
    analyzer = CryptoMarketAnalyzer(report_path)
    
    if analyzer.load_report():
        analyzer.extract_overview_stats()
        
        overview = analyzer.parsed_data.get('overview', {})
        assert 'total_coins' in overview
        assert 'falling_24h' in overview
        print("✅ 总览统计提取测试通过")
        
def test_full_analysis():
    """测试完整分析流程"""
    print("\n测试4: 完整分析流程")
    
    report_path = Path(__file__).parent.parent / 'data' / 'Binance.com数据模板.md'
    analyzer = CryptoMarketAnalyzer(report_path)
    
    result = analyzer.run()
    
    assert result == True
    assert 'market_sentiment' in analyzer.analysis
    assert 'major_coins_analysis' in analyzer.analysis
    print("✅ 完整分析流程测试通过")

def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("🧪 运行测试套件")
    print("="*60)
    
    try:
        test_load_report()
        test_extract_metadata()
        test_extract_overview()
        test_full_analysis()
        
        print("\n" + "="*60)
        print("✅ 所有测试通过!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
