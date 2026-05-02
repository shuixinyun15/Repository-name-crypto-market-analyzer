#!/usr/bin/env python3
"""
币安市场分析报告解析工具
基于 Markdown 报告文件自动生成结构化分析
"""

import re
import json
from datetime import datetime
from pathlib import Path

class CryptoMarketAnalyzer:
    """加密货币市场分析器"""
    
    def __init__(self, report_path):
        self.report_path = Path(report_path)
        self.raw_content = ""
        self.parsed_data = {}
        self.analysis = {}
        
    def load_report(self):
        """加载报告文件"""
        try:
            with open(self.report_path, 'r', encoding='utf-8') as f:
                self.raw_content = f.read()
            print(f"✅ 成功加载报告: {self.report_path}")
            return True
        except Exception as e:
            print(f"❌ 加载报告失败: {e}")
            return False
    
    def extract_metadata(self):
        """提取报告元数据"""
        # 提取数据时间
        time_match = re.search(r'\*\*数据时间\*\*:\s*(.+)', self.raw_content)
        if time_match:
            self.parsed_data['report_time'] = time_match.group(1).strip()
        
        # 提取数据来源
        source_match = re.search(r'\*\*数据来源\*\*:\s*(.+)', self.raw_content)
        if source_match:
            self.parsed_data['data_source'] = source_match.group(1).strip()
            
        # 提取筛选条件
        filter_match = re.search(r'\*\*筛选条件\*\*:\s*(.+)', self.raw_content)
        if filter_match:
            self.parsed_data['filter'] = filter_match.group(1).strip()
            
        print(f"📅 报告时间: {self.parsed_data.get('report_time', 'N/A')}")
        
    def extract_overview_stats(self):
        """提取总览统计数据"""
        overview = {}
        
        # 提取关键指标
        patterns = {
            'total_coins': r'主板币种总数\s*\|\s*\*\*(\d+)\*\*',
            'total_volume': r'总24h成交量\s*\|\s*\*\*\$?([\d,]+)M?\*\*',
            'stablecoins': r'稳定币\s*\|\s*(\d+)个',
            'above_ema60': r'站上EMA60\s*\|\s*(\d+/\d+)\s*\(\*\*(\d+\.?\d*)%\*\*\)',
            'above_ema120': r'站上EMA120\s*\|\s*(\d+/\d+)\s*\(\*\*(\d+\.?\d*)%\*\*\)',
            'rising_24h': r'24h上涨\s*\|\s*(\d+/\d+)\s*\(\*\*(\d+\.?\d*)%\*\*\)',
            'falling_24h': r'24h下跌\s*\|\s*(\d+/\d+)\s*\(\*\*(\d+\.?\d*)%\*\*\)',
            'top5_volume_ratio': r'Top5成交量占比\s*\|\s*\*\*(\d+\.?\d*)%\*\*'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, self.raw_content)
            if match:
                if key in ['above_ema60', 'above_ema120', 'rising_24h', 'falling_24h']:
                    overview[key] = {
                        'ratio': match.group(1),
                        'percentage': float(match.group(2))
                    }
                elif key == 'total_volume':
                    overview[key] = match.group(1).replace(',', '')
                else:
                    overview[key] = match.group(1)
        
        self.parsed_data['overview'] = overview
        print(f"📊 总览统计提取完成")
        
    def extract_major_coins(self):
        """提取大盘核心币种数据"""
        major_coins = []
        
        # 查找大盘核心部分
        major_section = re.search(
            r'# 二、大盘核心.*?\n\n(.*?)(?=# 三、|# 四、|$)',
            self.raw_content,
            re.DOTALL
        )
        
        if major_section:
            section_text = major_section.group(1)
            # 匹配表格行 - 处理加粗的币种名和✅/❌
            pattern = r'\|\s*(\d+)\s*\|\s*\*\*(\w+)\*\*\s*\|\s*([\d,\.]+)\s*\|\s*([\+\-]?\d+\.?\d*%)\s*\|\s*([\d\.]+)\s*\|\s*\$?([\d,\.]+)\s*\|\s*\$?([\d,\.]+)\s*\|\s*\$?([\d,\.]+)\s*\|\s*([\+\-]?\d+\.?\d*%)\s*\|\s*([\d,\.]+)\s*\|\s*([\d,\.]+)\s*\|\s*([✅❌\*]+)\s*\|\s*([✅❌\*]+)\s*\|'
            
            matches = re.findall(pattern, section_text)
            for match in matches[:4]:  # 只取前4个大盘币
                # 清理✅/❌中的加粗标记
                above_60 = '✅' in match[11]
                above_120 = '✅' in match[12]
                
                coin = {
                    'rank': match[0],
                    'symbol': match[1],
                    'price': float(match[2].replace(',', '')),
                    'change_24h': match[3],
                    'volume_24h': float(match[4]),
                    'market_cap': match[5].replace(',', ''),
                    'fdv': match[6].replace(',', ''),
                    'ath': float(match[7].replace(',', '')),
                    'from_ath': match[8],
                    'ema60': float(match[9].replace(',', '')),
                    'ema120': float(match[10].replace(',', '')),
                    'above_ema60': above_60,
                    'above_ema120': above_120
                }
                major_coins.append(coin)
                
        self.parsed_data['major_coins'] = major_coins
        print(f"💰 大盘核心币种提取完成: {len(major_coins)}个")
        
    def extract_meme_coins(self):
        """提取MEME板块数据"""
        meme_coins = []
        
        # 查找MEME板块部分
        meme_section = re.search(
            r'# 四、MEME板块.*?\n\n(.*?)(?=# 五、|# 六、|$)',
            self.raw_content,
            re.DOTALL
        )
        
        if meme_section:
            section_text = meme_section.group(1)
            # 匹配MEME表格行（处理加粗标记）
            pattern = r'\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*([\d\.]+)\s*\|\s*([\+\-]?\d+\.?\d*%)\s*\|\s*\*\*?([\d\.]+)\*\*?\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*([\d\.]+)\s*\|\s*([\+\-]?\d+\.?\d*%)\s*\|\s*([\d\.]+)\s*\|\s*([\d\.]+)\s*\|\s*([✅❌\*]+)\s*\|\s*([✅❌\*]+)\s*\|\s*(\w+)\s*\|'
            
            matches = re.findall(pattern, section_text)
            for match in matches:
                if len(match) >= 14:
                    # 清理✅/❌中的加粗标记
                    above_60 = '✅' in match[11]
                    above_120 = '✅' in match[12]
                    
                    coin = {
                        'rank': match[0],
                        'symbol': match[1],
                        'price': float(match[2]),
                        'change_24h': match[3],
                        'volume_24h': float(match[4]),
                        'market_cap': match[5].replace(',', ''),
                        'fdv': match[6].replace(',', ''),
                        'ath': float(match[7]),
                        'from_ath': match[8],
                        'ema60': float(match[9]),
                        'ema120': float(match[10]),
                        'above_ema60': above_60,
                        'above_ema120': above_120,
                        'zone': match[13]
                    }
                    meme_coins.append(coin)
                
        self.parsed_data['meme_coins'] = meme_coins
        print(f"🐕 MEME板块提取完成: {len(meme_coins)}个")
        
    def generate_analysis(self):
        """生成分析报告"""
        analysis = {
            'market_sentiment': self._analyze_market_sentiment(),
            'major_coins_analysis': self._analyze_major_coins(),
            'meme_analysis': self._analyze_meme_coins(),
            'key_signals': self._extract_key_signals(),
            'recommendations': self._generate_recommendations()
        }
        
        self.analysis = analysis
        print("📈 分析报告生成完成")
        
    def _analyze_market_sentiment(self):
        """分析市场情绪"""
        overview = self.parsed_data.get('overview', {})
        
        # 计算情绪评分
        sentiment_score = 5.0
        
        # 基于涨跌分布调整
        falling_pct = overview.get('falling_24h', {}).get('percentage', 50)
        sentiment_score -= (falling_pct - 50) / 10
        
        # 基于EMA120站上率调整
        ema120_pct = overview.get('above_ema120', {}).get('percentage', 50)
        sentiment_score -= (50 - ema120_pct) / 10
        
        sentiment_score = max(0, min(10, sentiment_score))
        
        if sentiment_score >= 7:
            sentiment = "偏多"
        elif sentiment_score >= 5:
            sentiment = "中性"
        elif sentiment_score >= 3:
            sentiment = "偏空"
        else:
            sentiment = "极度偏空"
            
        return {
            'score': round(sentiment_score, 1),
            'sentiment': sentiment,
            'falling_percentage': falling_pct,
            'above_ema120_percentage': ema120_pct
        }
        
    def _analyze_major_coins(self):
        """分析大盘核心币种"""
        major_coins = self.parsed_data.get('major_coins', [])
        analysis = []
        
        for coin in major_coins:
            coin_analysis = {
                'symbol': coin['symbol'],
                'price': coin['price'],
                'trend': self._determine_trend(coin),
                'risk_level': self._assess_risk(coin),
                'key_level': self._find_key_level(coin)
            }
            analysis.append(coin_analysis)
            
        return analysis
        
    def _determine_trend(self, coin):
        """判断币种趋势"""
        if coin['above_ema60'] and coin['above_ema120']:
            return "强势上涨"
        elif coin['above_ema60'] and not coin['above_ema120']:
            return "短期反弹，中期偏弱"
        elif not coin['above_ema60'] and coin['above_ema120']:
            return "回调测试支撑"
        else:
            return "弱势下行"
            
    def _assess_risk(self, coin):
        """评估风险等级"""
        from_ath_str = coin.get('from_ath', '-50%')
        from_ath = float(from_ath_str.replace('%', ''))
        
        if from_ath > -30:
            return "低风险"
        elif from_ath > -60:
            return "中等风险"
        elif from_ath > -80:
            return "高风险"
        else:
            return "极高风险"
            
    def _find_key_level(self, coin):
        """寻找关键价位"""
        if coin['above_ema60'] and coin['above_ema120']:
            return f"支撑位: EMA60 ${coin['ema60']:,.2f}"
        elif not coin['above_ema60']:
            return f"阻力位: EMA60 ${coin['ema60']:,.2f}"
        else:
            return f"阻力位: EMA120 ${coin['ema120']:,.2f}"
            
    def _analyze_meme_coins(self):
        """分析MEME板块"""
        meme_coins = self.parsed_data.get('meme_coins', [])
        
        strong_coins = [c for c in meme_coins if c['above_ema60'] and c['above_ema120']]
        neutral_coins = [c for c in meme_coins if c['above_ema60'] and not c['above_ema120']]
        weak_coins = [c for c in meme_coins if not c['above_ema60']]
        
        return {
            'total': len(meme_coins),
            'strong': len(strong_coins),
            'neutral': len(neutral_coins),
            'weak': len(weak_coins),
            'strong_coins': [c['symbol'] for c in strong_coins],
            'weak_coins': [c['symbol'] for c in weak_coins]
        }
        
    def _extract_key_signals(self):
        """提取关键信号"""
        signals = []
        
        # 大盘信号
        major_coins = self.parsed_data.get('major_coins', [])
        for coin in major_coins:
            if coin['symbol'] == 'BTC':
                if coin['above_ema120']:
                    distance = ((coin['price'] - coin['ema120']) / coin['ema120']) * 100
                    if distance < 1:
                        signals.append(f"⚠️ BTC勉强站上EMA120，仅高出{distance:.2f}%，极度脆弱")
                    else:
                        signals.append(f"✅ BTC站上EMA120，高出{distance:.2f}%，多头支撑有效")
                        
            if coin['symbol'] == 'ETH':
                if not coin['above_ema120']:
                    distance = ((coin['ema120'] - coin['price']) / coin['price']) * 100
                    signals.append(f"🔴 ETH未站上EMA120，还差+{distance:.1f}%，中期趋势偏弱")
                    
            if coin['symbol'] == 'SOL':
                if not coin['above_ema60'] and not coin['above_ema120']:
                    signals.append(f"🔴 SOL双线之下，最弱大盘核心币")
        
        # 市场情绪信号
        overview = self.parsed_data.get('overview', {})
        falling_pct = overview.get('falling_24h', {}).get('percentage', 0)
        if falling_pct > 70:
            signals.append(f"🔴 {falling_pct}%币种24h下跌，普跌格局，卖压主导")
            
        return signals
        
    def _generate_recommendations(self):
        """生成操作建议"""
        recommendations = []
        
        sentiment = self.analysis.get('market_sentiment', {})
        score = sentiment.get('score', 5)
        
        if score < 3:
            recommendations.append("🔴 极度偏空：减仓观望，等待更清晰的信号")
        elif score < 5:
            recommendations.append("🟡 偏空观望：不急于抄底，等待BTC企稳")
        elif score < 7:
            recommendations.append("🟡 中性震荡：轻仓操作，严格止损")
        else:
            recommendations.append("🟢 偏多：可逐步建仓，关注强势币种")
            
        # BTC关键位建议
        major_coins = self.parsed_data.get('major_coins', [])
        for coin in major_coins:
            if coin['symbol'] == 'BTC':
                if coin['above_ema120']:
                    recommendations.append(f"📊 BTC关键位: 守住${coin['ema120']:,.0f}则稳定，跌破则减仓")
                    
        # MEME建议
        meme_analysis = self.analysis.get('meme_analysis', {})
        if meme_analysis.get('strong', 0) > 0:
            strong_list = meme_analysis.get('strong_coins', [])
            recommendations.append(f"🐕 MEME机会: {', '.join(strong_list)} 表现强势，可小仓位博弈")
            
        return recommendations
        
    def print_report(self):
        """打印分析报告"""
        print("\n" + "="*60)
        print("📊 币安市场分析报告")
        print("="*60)
        
        # 元数据
        print(f"\n📅 报告时间: {self.parsed_data.get('report_time', 'N/A')}")
        print(f"📊 数据来源: {self.parsed_data.get('data_source', 'N/A')}")
        
        # 市场情绪
        sentiment = self.analysis.get('market_sentiment', {})
        print(f"\n{'='*60}")
        print("🎯 市场情绪")
        print(f"{'='*60}")
        print(f"情绪评分: {sentiment.get('score', 'N/A')}/10")
        print(f"市场状态: {sentiment.get('sentiment', 'N/A')}")
        print(f"24h下跌比例: {sentiment.get('falling_percentage', 'N/A')}%")
        print(f"站上EMA120比例: {sentiment.get('above_ema120_percentage', 'N/A')}%")
        
        # 大盘核心
        print(f"\n{'='*60}")
        print("💰 大盘核心分析")
        print(f"{'='*60}")
        for coin_analysis in self.analysis.get('major_coins_analysis', []):
            print(f"\n{coin_analysis['symbol']}:")
            print(f"  当前价格: ${coin_analysis['price']:,.2f}")
            print(f"  趋势判断: {coin_analysis['trend']}")
            print(f"  风险等级: {coin_analysis['risk_level']}")
            print(f"  {coin_analysis['key_level']}")
            
        # 关键信号
        print(f"\n{'='*60}")
        print("⚡ 关键信号")
        print(f"{'='*60}")
        for signal in self.analysis.get('key_signals', []):
            print(f"  {signal}")
            
        # MEME分析
        meme = self.analysis.get('meme_analysis', {})
        print(f"\n{'='*60}")
        print("🐕 MEME板块分析")
        print(f"{'='*60}")
        print(f"总数: {meme.get('total', 0)}")
        print(f"强势(双线上): {meme.get('strong', 0)}个 - {', '.join(meme.get('strong_coins', []))}")
        print(f"中性(仅EMA60): {meme.get('neutral', 0)}个")
        print(f"弱势(双线下): {meme.get('weak', 0)}个 - {', '.join(meme.get('weak_coins', []))}")
        
        # 操作建议
        print(f"\n{'='*60}")
        print("📋 操作建议")
        print(f"{'='*60}")
        for rec in self.analysis.get('recommendations', []):
            print(f"  {rec}")
            
        print(f"\n{'='*60}")
        print("分析完成!")
        print("="*60)
        
    def export_json(self, output_path=None):
        """导出JSON格式数据"""
        if output_path is None:
            output_path = self.report_path.with_suffix('.json')
            
        export_data = {
            'metadata': {
                'report_time': self.parsed_data.get('report_time'),
                'data_source': self.parsed_data.get('data_source'),
                'filter': self.parsed_data.get('filter')
            },
            'overview': self.parsed_data.get('overview'),
            'major_coins': self.parsed_data.get('major_coins'),
            'meme_coins': self.parsed_data.get('meme_coins'),
            'analysis': self.analysis
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
            
        print(f"📤 数据已导出到: {output_path}")
        return output_path
        
    def run(self):
        """运行完整分析流程"""
        print("🚀 开始分析币安市场报告...\n")
        
        if not self.load_report():
            return False
            
        self.extract_metadata()
        self.extract_overview_stats()
        self.extract_major_coins()
        self.extract_meme_coins()
        self.generate_analysis()
        self.print_report()
        
        return True


def main():
    """主函数"""
    import sys
    
    # 默认报告路径
    default_path = "/root/.openclaw/workspace/agent-151e9582/crypto-market-analyzer/Binance.com数据模板.md"
    
    # 支持命令行参数
    report_path = sys.argv[1] if len(sys.argv) > 1 else default_path
    
    # 创建分析器并运行
    analyzer = CryptoMarketAnalyzer(report_path)
    
    if analyzer.run():
        # 导出JSON
        analyzer.export_json()
        print("\n✅ 分析完成!")
    else:
        print("\n❌ 分析失败!")
        sys.exit(1)


if __name__ == "__main__":
    main()
