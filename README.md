# Stock Strategy

A Python-based stock analysis tool that fetches historical price data and computes various technical metrics for market analysis.

## Features

- **Data Fetching**: Automated fetching of historical stock data from Yahoo Finance
- **Technical Metrics**:
  - 20-day and 200-day normalized price indicators
  - Exponential growth predictions for 200-day returns
  - Multiple lookback windows (20-day and 200-day) for trend analysis
- **Flexible Configuration**: Symbol list maintained in CSV for easy updates

## Project Structure

```
├── src/hello/
│   ├── fetch_stocks.py    # Yahoo Finance data fetcher
│   ├── metrics.py         # Technical indicators calculator
│   ├── predict_returns.py # Exponential growth predictions
│   └── price_normalized.py # Price normalization
├── symbols.csv           # Configure stock symbols here
├── pyproject.toml       # Project dependencies and metadata
└── requirements.txt     # Direct dependencies list
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alexandrec90/stock_strategy.git
cd stock_strategy
```

2. Create and activate a Python virtual environment:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Unix/MacOS:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Configure stock symbols:
   - Edit `symbols.csv` to specify the stocks you want to analyze
   - One symbol per row under the 'Symbol' column

2. Fetch historical data:
```bash
python src/hello/fetch_stocks.py
```

3. Generate technical metrics:
```bash
python src/hello/metrics.py
```

## Output Files

- `stock_prices.csv`: Raw historical price data including:
  - Date, Open, High, Low, Close, Volume
  - Dividends and Stock Splits
  - Symbol identifier

- `metrics.csv`: Technical analysis metrics including:
  - Normalized_20: Current price position in 20-day range [0-1]
  - Normalized_200: Current price position in 200-day range [0-1]
  - PredReturn_20exp: Predicted 200-day return using 20-day exp. fit
  - PredReturn_200exp: Predicted 200-day return using 200-day exp. fit

## Dependencies

- Python ≥ 3.11
- numpy ≥ 1.24.0
- pandas ≥ 2.0.0
- yfinance ≥ 0.2.0
- scipy ≥ 1.10.0

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Testing

To run the tests, you can use the following command:

```
pytest tests/test_main.py
```

Make sure you have `pytest` installed in your environment.

## Dependencies

This project does not have any external dependencies. However, you can manage your dependencies in the `requirements.txt` file if needed.

## License

This project is open source and available under the MIT License.