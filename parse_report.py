#!/usr/bin/env python3
"""
币安市场分析报告解析器
用于解析Markdown格式的币安市场分析报告
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime

class BinanceReportParser:
    """币安市场分析报告解析器"""
    
    def __init__(self, report_path):
        self.report_path = Path(report_path)
        self.raw_content = ""
        self.parsed_data = {}
        
    def load_report(self):
        """加载报告文件"""
        with open(self.report_path, 'r', encoding='utf-8') as f:
            self.raw_content = f.read()
        return self
    
    def parse_metadata(self):
        """解析报告元数据"""
        metadata = {}
        
        # 提取数据时间
        time_match = re.search(r'\*\*数据时间\*\*:\s*(.+)', self.raw_content)
        if time_match:
            metadata['data_time'] = time_match.group(1).strip()
        
        # 提取数据来源
        source_match = re.search(r'\*\*数据来源\*\*:\s*(.+)', self.raw_content)
        if source_match:
            metadata['data_sources'] = source_match.group(1).strip()
        
        # 提取筛选条件
        filter_match = re.search(r'\*\*筛选条件\*\*:\s*(.+)', self.raw_content)
        if filter_match:
            metadata['filter'] = filter_match.group(1).strip()
            
        return metadata
    
    def parse_overview(self):
        """解析总览统计"""
        overview = {}
        
        # 提取关键指标
        patterns = {
            'total_coins': r'主板币种总数\s*\|\s*\*\*(\d+)\*\*',
            'total_volume': r'总24h成交量\s*\|\s*\*\*(\$[\d,]+M)\*\*',
            'above_ema60': r'站上EMA60\s*\|\s*(\d+/\d+\s*\([\d.]+%)\)',
            'above_ema120': r'站上EMA120\s*\|\s*(\d+/\d+\s*\([\d.]+%)\)',
            'rising_24h': r'24h上涨\s*\|\s*(\d+/\d+\s*\([\d.]+%)\)',
            'falling_24h': r'24h下跌\s*\|\s*(\d+/\d+\s*\([\d.]+%)\)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, self.raw_content)
            if match:
                overview[key] = match.group(1)
        
        return overview
    
    def parse_major_coins(self):
        """解析大盘核心币种"""
        coins = []
        
        # 查找大盘核心表格
        section_match = re.search(
            r'# 二、大盘核心.*?(?=# 三、|$)',
            self.raw_content,
            re.DOTALL
        )
        
        if section_match:
            section = section_match.group(0)
            # 提取表格行
            rows = re.findall(
                r'\|\s*(\d+)\s*\|\s*\*\*(\w+)\*\*\s*\|\s*([\d,.]+)\s*\|\s*([+-]?[\d.]+%)\s*\|\s*([\d.]+)\s*\|\s*\$?([\d,.]+)\s*\|\s*\$?([\d,.]+)\s*\|\s*\$?([\d,.]+)\s*\|\s*([+-]?[\d.]+%)\s*\|\s*([\d,.]+)\s*\|\s*([\d,.]+)\s*\|\s*([✅❌])\s*\|\s*([✅❌])\s*\|',
                section
            )
            
            for row in rows:
                coins.append({
                    'rank': int(row[0]),
                    'symbol': row[1],
                    'price': float(row[2].replace(',', '')),
                    'change_24h': row[3],
                    'volume_24h': float(row[4]),
                    'market_cap': row[5],
                    'fdv': row[6],
                    'ath': float(row[7].replace(',', '')),
                    'from_ath': row[8],
                    'ema60': float(row[9].replace(',', '')),
                    'ema120': float(row[10].replace(',', '')),
                    'above_ema60': row[11] == '✅',
                    'above_ema120': row[12] == '✅'
                })
        
        return coins
    
    def parse_mainboard_others(self):
        """解析主板其他币种"""
        coins = []
        
        section_match = re.search(
            r'# 三、主板其他.*?(?=# 四、|$)',
            self.raw_content,
            re.DOTALL
        )
        
        if section_match:
            section = section_match.group(0)
            rows = re.findall(
                r'\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*([\d,.]+)\s*\|\s*([+-]?[\d.]+%)\s*\|\s*([\d.]+)\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*([+-]?[\d.]+%)\s*\|\s*([\d,.]+)\s*\|\s*([\d,.]+)\s*\|\s*([✅❌?])\s*\|\s*([✅❌?])\s*\|',
                section
            )
            
            for row in rows:
                coins.append({
                    'rank': int(row[0]),
                    'symbol': row[1],
                    'price': float(row[2].replace(',', '')),
                    'change_24h': row[3],
                    'volume_24h': float(row[4]),
                    'market_cap': int(row[5].replace(',', '')),
                    'fdv': int(row[6].replace(',', '')),
                    'from_ath': row[7],
                    'ema60': float(row[8].replace(',', '')),
                    'ema120': float(row[9].replace(',', '')),
                    'above_ema60': row[10] == '✅',
                    'above_ema120': row[11] == '✅'
                })
        
        return coins
    
    def parse_meme_coins(self):
        """解析MEME板块"""
        coins = []
        
        section_match = re.search(
            r'# 四、MEME板块.*?(?=# 五、|$)',
            self.raw_content,
            re.DOTALL
        )
        
        if section_match:
            section = section_match.group(0)
            rows = re.findall(
                r'\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*([\d,.]+)\s*\|\s*([+-]?[\d.]+%)\s*\|\s*([\d.]+)\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*([\d,.]+)\s*\|\s*([+-]?[\d.]+%)\s*\|\s*([\d,.]+)\s*\|\s*([\d,.]+)\s*\|\s*([✅❌])\s*\|\s*([✅❌])\s*\|\s*(\w+)\s*\|',
                section
            )
            
            for row in rows:
                coins.append({
                    'rank': int(row[0]),
                    'symbol': row[1],
                    'price': float(row[2].replace(',', '')),
                    'change_24h': row[3],
                    'volume_24h': float(row[4]),
                    'market_cap': int(row[5].replace(',', '')),
                    'fdv': int(row[6].replace(',', '')),
                    'ath': float(row[7].replace(',', '')),
                    'from_ath': row[8],
                    'ema60': float(row[9].replace(',', '')),
                    'ema120': float(row[10].replace(',', '')),
                    'above_ema60': row[11] == '✅',
                    'above_ema120': row[12] == '✅',
                    'zone': row[13]
                })
        
        return coins
    
    def parse_eth_ecosystem(self):
        """解析ETH生态"""
        coins = []
        
        section_match = re.search(
            r'# 五、ETH生态.*?(?=# 六、|$)',
            self.raw_content,
            re.DOTALL
        )
        
        if section_match:
            section = section_match.group(0)
            rows = re.findall(
                r'\|\s*(\w+)\s*\|\s*([\d,.]+)\s*\|\s*([+-]?[\d.]+%)\s*\|\s*([\d.]+)\s*\|\s*([\d,.]+)\s*\|\s*([\d,.]+)\s*\|\s*([✅❌])\s*\|\s*([✅❌])\s*\|\s*([+-]?[\d.]+%)\s*\|\s*([+-]?[\d.]+%)\s*\|',
                section
            )
            
            for row in rows:
                coins.append({
                    'symbol': row[0],
                    'price': float(row[1].replace(',', '')),
                    'change_24h': row[2],
                    'volume_24h': float(row[3]),
                    'ema60': float(row[4].replace(',', '')),
                    'ema120': float(row[5].replace(',', '')),
                    'above_ema60': row[6] == '✅',
                    'above_ema120': row[7] == '✅',
                    'distance_ema60': row[8],
                    'distance_ema120': row[9]
                })
        
        return coins
    
    def parse_market_sentiment(self):
        """解析市场情绪"""
        sentiment = {}
        
        section_match = re.search(
            r'# 六、市场情绪总结.*?(?=# 七、|$)',
            self.raw_content,
            re.DOTALL
        )
        
        if section_match:
            section = section_match.group(0)
            
            # 提取综合情绪评分
            score_match = re.search(r'综合情绪.*?\*\*🔴\s*([\d.]+)/10\*\*', section)
            if score_match:
                sentiment['score'] = float(score_match.group(1))
            
            # 提取市场状态
            status_match = re.search(r'市场状态:\s*(.+)', section)
            if status_match:
                sentiment['status'] = status_match.group(1).strip()
        
        return sentiment
    
    def parse_all(self):
        """解析所有数据"""
        self.load_report()
        
        self.parsed_data = {
            'metadata': self.parse_metadata(),
            'overview': self.parse_overview(),
            'major_coins': self.parse_major_coins(),
            'mainboard_others': self.parse_mainboard_others(),
            'meme_coins': self.parse_meme_coins(),
            'eth_ecosystem': self.parse_eth_ecosystem(),
            'market_sentiment': self.parse_market_sentiment()
        }
        
        return self.parsed_data
    
    def export_json(self, output_path):
        """导出为JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.parsed_data, f, ensure_ascii=False, indent=2)
        return output_path
    
    def generate_summary(self):
        """生成摘要"""
        data = self.parsed_data
        
        summary = f"""
📊 币安市场分析报告摘要
========================

📅 数据时间: {data['metadata'].get('data_time', 'N/A')}
📊 数据来源: {data['metadata'].get('data_sources', 'N/A')}

🎯 市场情绪: {data['market_sentiment'].get('score', 'N/A')}/10
📈 市场状态: {data['market_sentiment'].get('status', 'N/A')}

💰 大盘核心 ({len(data['major_coins'])}个):
"""
        
        for coin in data['major_coins']:
            summary += f"  - {coin['symbol']}: ${coin['price']:,.2f} ({coin['change_24h']})\n"
        
        summary += f"""
🐕 MEME板块 ({len(data['meme_coins'])}个):
"""
        
        for coin in data['meme_coins'][:5]:
            summary += f"  - {coin['symbol']}: ${coin['price']} ({coin['change_24h']})\n"
        
        summary += f"""
📊 主板其他 ({len(data['mainboard_others'])}个)
🔷 ETH生态 ({len(data['eth_ecosystem'])}个)

========================
"""
        
        return summary


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python parse_report.py <报告文件路径>")
        sys.exit(1)
    
    report_path = sys.argv[1]
    
    print(f"📊 正在解析报告: {report_path}")
    
    parser = BinanceReportParser(report_path)
    data = parser.parse_all()
    
    # 生成摘要
    summary = parser.generate_summary()
    print(summary)
    
    # 导出JSON
    output_path = Path(report_path).parent / 'parsed_report.json'
    parser.export_json(str(output_path))
    print(f"✅ 数据已导出到: {output_path}")
    
    # 打印统计
    print(f"\n📈 数据统计:")
    print(f"  - 大盘核心: {len(data['major_coins'])}个")
    print(f"  - 主板其他: {len(data['mainboard_others'])}个")
    print(f"  - MEME板块: {len(data['meme_coins'])}个")
    print(f"  - ETH生态: {len(data['eth_ecosystem'])}个")


if __name__ == '__main__':
    main()
