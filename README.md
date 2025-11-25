# Stock Strategy

A Python-based stock analysis tool that fetches historical price data and computes technical metrics for market analysis.

## Features

- **Data Fetching**: Automated fetching of historical stock data from Yahoo Finance
- **Technical Metrics**:
  - 20-day and 200-day normalized price indicators
  - Exponential growth predictions for 200-day returns
  - Multiple lookback windows (20-day and 200-day) for trend analysis
- **Flexible Configuration**: YAML-based configuration for easy parameter tuning
- **CLI Interface**: Simple command-line tool for running analysis

## Project Structure

```
stock_strategy/
├── config.yaml           # Configuration (windows, lookback days, file paths)
├── data/                 # Data directory (git-ignored except symbols.csv)
│   ├── symbols.csv       # Stock symbols to analyze
│   ├── stock_prices.csv  # Fetched historical data
│   └── metrics.csv       # Computed technical metrics
├── src/
│   ├── __init__.py       # Package initialization
│   ├── cli.py            # Command-line interface
│   ├── core/             # Core configuration and shared utilities
│   │   └── config.py     # Centralized config values (use `from src.core.config import ...`)
│   ├── data/             # Data ingestion helpers
│   │   └── fetch_stocks.py # Yahoo Finance data fetcher (use `from src.data.fetch_stocks import main`)
│   ├── analysis/         # Analysis and metrics implementations
│   │   ├── metrics.py    # Technical indicators calculator (use `from src.analysis.metrics import compute_metrics`)
│   │   └── utils.py      # Shared utility functions (use `from src.analysis.utils import ...`)
│   └── trading/          # Trading integrations
│       └── ibkr.py       # Interactive Brokers integration (use `from src.trading.ibkr import demo_trade`)
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_utils.py
│   └── test_ibkr.py
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alexandrec90/stock_strategy.git
cd stock_strategy
```

2. Create and activate a Python virtual environment:
```bash
# Windows:
python -m venv .venv
.venv\Scripts\activate

# Unix/MacOS:
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.yaml` to customize:
- Window sizes for technical indicators
- Lookback period for historical data
- Data directory and file names

```yaml
metrics:
  window_short: 20      # Short-term window (days)
  window_long: 200      # Long-term window (days)
  predict_days: 200     # Prediction horizon (days)

fetch:
  lookback_days: 500    # Historical data to fetch (days)
```

## Usage

### CLI (Recommended)

```bash
# Fetch stock data
python src/cli.py fetch

# Compute metrics
python src/cli.py metrics

# Run full pipeline (fetch + metrics)
python src/cli.py all
```

### Trading demo (IBKR)

This project includes a safe trading demo that can be used to test order placement logic.

- By default the demo runs in dry-run mode and will not connect to Interactive Brokers nor place orders:

  ```bash
  python src/cli.py trade-demo
  ```

- To attempt a live order you must run TWS or IB Gateway in paper mode and explicitly request a live run. For safety the CLI requires both `--live` and `--confirm` to send a live order:

  ```bash
  python src/cli.py trade-demo --symbol AAPL --qty 1 --live --confirm
  ```

Ensure you understand the risks before sending live orders. Use `--live` only when your IB environment is configured and you intend to trade in your paper account.

### Managing Symbols

Edit `data/symbols.csv` to specify stocks to analyze:
```csv
Symbol,Name
AAPL,Apple Inc.
MSFT,Microsoft Corporation
TSLA,Tesla Inc.
```

## Output Files

### stock_prices.csv
Raw historical price data including:
- Date, Open, High, Low, Close, Volume
- Dividends and Stock Splits
- Symbol identifier

### metrics.csv
Technical analysis metrics:
- **Normalized_20**: Current price position in 20-day range [0-1]
- **Normalized_200**: Current price position in 200-day range [0-1]
- **PredReturn_20exp**: Predicted 200-day return using 20-day exponential fit
- **PredReturn_200exp**: Predicted 200-day return using 200-day exponential fit

## Testing

Run the test suite:
```bash
pytest tests/
```

Run tests with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Dependencies

- Python ≥ 3.11
- pandas
- numpy
- scipy
- yfinance
- pyyaml

Development:
- pytest

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.
