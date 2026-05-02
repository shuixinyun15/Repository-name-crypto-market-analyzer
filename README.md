# Crypto Market Analyzer

A comprehensive cryptocurrency market analysis tool that provides detailed daily reports for all sectors and individual coins, inspired by Binance spot market analysis.

## Features

- **Comprehensive Market Overview**: Total market statistics with detailed breakdowns
- **Major Coins Analysis**: BTC, ETH, SOL, BNB with key signals
- **Sector-by-Sector Breakdown**:
  - Main Board (42 coins sorted by volume)
  - MEME Sector (22 coins with tier analysis)
  - ETH Ecosystem (17 DeFi/L2 tokens)
- **Technical Indicators**: EMA60/120, RSI, Volume Ratio, ATH distance
- **Market Sentiment Dashboard**: Multi-dimensional scoring system
- **Trading Recommendations**: Actionable insights with conditions

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Data Sources

- Binance API (real-time ticker & klines)
- CoinGecko API (market cap & FDV)

## Output

Generates comprehensive Markdown reports with:
- All coins in each sector with full metrics
- Technical analysis signals
- Market sentiment scoring
- Trading recommendations

## License

MIT