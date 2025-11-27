# Stock Strategy

A Python-based stock analysis tool that fetches historical price data and computes technical metrics for market analysis.

---

## Features

<!-- AI: Update feature list when adding new capabilities -->
- ✅ **Data Fetching**: Automated fetching of historical stock data from Yahoo Finance
- ✅ **Technical Metrics**:
  - 20-day and 200-day normalized price indicators
  - Exponential growth predictions for 200-day returns
  - Multiple lookback windows (20-day and 200-day) for trend analysis
- ✅ **Flexible Configuration**: YAML-based configuration for easy parameter tuning
- ✅ **CLI Interface**: Simple command-line tool for running analysis
- 🚧 **IBKR Integration**: Interactive Brokers trading (under development)

---

## Quick Start

```bash
# Clone repository
git clone https://github.com/alexandrec90/stock_strategy.git
cd stock_strategy

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Unix/MacOS

# Install package
pip install -e ".[dev]"

# Fetch stock data
python src/cli.py fetch

# Compute metrics
python src/cli.py metrics
```

---

## Installation

### Production (Minimal)
```bash
pip install -e .
```

Installs: numpy, pandas, yfinance, scipy, pyyaml

### Development (Full)
```bash
pip install -e ".[dev]"
```

Installs: Production dependencies + pytest, pytest-cov, black, ruff

**Dependencies**: See [docs/dependencies.md](docs/dependencies.md) for detailed justifications.

<!-- AI: When adding dependencies, update docs/dependencies.md first -->

---

## Configuration

Edit `config.yaml` to customize behavior. See [docs/configuration.md](docs/configuration.md) for complete options.

**Key Settings**:
```yaml
metrics:
  window_short: 20      # Short-term window (days)
  window_long: 200      # Long-term window (days)
  predict_days: 200     # Prediction horizon (days)

fetch:
  lookback_days: 500    # Historical data to fetch (days)
```

---

## Usage

### Command Line Interface

```bash
# Fetch stock data
python src/cli.py fetch

# Compute metrics
python src/cli.py metrics

# Run full pipeline (fetch + metrics)
python src/cli.py all

# Trading demo (dry-run, safe)
python src/cli.py trade-demo

# Trading demo (live - requires TWS/Gateway in paper mode)
python src/cli.py trade-demo --symbol AAPL --qty 1 --live --confirm
```

### Managing Symbols

Edit `data/symbols.csv` to specify stocks to analyze:
```csv
Symbol
AAPL
MSFT
TSLA
```

### Programmatic Usage

```python
# Fetch data
from src.data.fetch_stocks import main as fetch_stocks
fetch_stocks()

# Compute metrics
from src.analysis.metrics import compute_metrics
compute_metrics()

# Load results
import pandas as pd
metrics = pd.read_csv('data/metrics.csv')
```

---

## Output Files

### `data/stock_prices.csv`
Raw historical price data from Yahoo Finance:
- Columns: Date, Symbol, Open, High, Low, Close, Volume, Dividends, Stock Splits

### `data/metrics.csv`
Computed technical metrics:
- **Normalized_20**: Price position in 20-day range [0,1] (0=min, 1=max)
- **Normalized_200**: Price position in 200-day range [0,1]
- **PredReturn_20exp**: Predicted 200-day return using 20-day exponential model
- **PredReturn_200exp**: Predicted 200-day return using 200-day exponential model

**Interpretation**:
- Normalized close to 0 → Stock near historical lows (potential buy)
- Normalized close to 1 → Stock near historical highs (potential sell)
- PredReturn > 1.0 → Model predicts price increase
- PredReturn < 1.0 → Model predicts price decrease

---

## Documentation

<!-- AI: Add new doc files to this list -->
- **[API Reference](docs/api-reference.md)** - All functions and classes
- **[Architecture](docs/architecture.md)** - System design and data flow
- **[Configuration](docs/configuration.md)** - All config options explained
- **[Dependencies](docs/dependencies.md)** - Why each dependency is needed
- **[File Summaries](docs/file-summaries.md)** - AI context summaries (auto-generated)
- **[AI Changelog](docs/ai-changelog.md)** - AI-assisted changes log

---

## Project Structure

├── .github/
│   └── copilot-instructions.md  # AI coding standards (auto-loaded)
├── .vscode/
│   ├── settings.json            # VS Code configuration
│   └── tasks.json               # Build and utility tasks
├── src/
│   ├── analysis/                # Metrics computation
│   │   ├── metrics.py          # Main computation logic
│   │   └── utils.py            # Helper functions
│   ├── core/                    # Config, constants
│   │   └── config.py           # Load config.yaml
│   ├── data/                    # Data fetching
│   │   └── fetch_stocks.py     # Download from Yahoo Finance
│   ├── trading/                 # Trading integration
│   │   └── ibkr.py             # Interactive Brokers API
│   ├── utils/                   # Utility scripts
│   │   └── docstring_summarizer.py # Generate AI file summaries
│   └── cli.py                   # Command-line interface
├── data/                        # Generated data files
│   ├── symbols.csv              # Stock symbols (user-created)
│   ├── stock_prices.csv         # Historical prices (generated)
│   └── metrics.csv              # Computed metrics (generated)
├── docs/                        # Documentation
│   ├── api-reference.md
│   ├── architecture.md
│   ├── configuration.md
│   ├── dependencies.md
│   ├── file-summaries.md        # AI context summaries (auto-generated)
│   └── ai-changelog.md
├── tests/                       # Unit tests
├── config.yaml                  # Configuration file
├── pyproject.toml              # Package metadata
└── README.md                    # This file

<!-- AI: Update structure when adding new directories -->

---

## Development

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Auto-fix linting issues
ruff check --fix src/

# Type checking (via Pylance in VS Code)
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_utils.py

# Run tests matching pattern
pytest -k "test_normalize"
```

### Adding New Features

When adding code, AI will automatically:
1. Add type hints and docstrings (via `.github/copilot-instructions.md`)
2. Update `docs/api-reference.md`
3. Update `docs/ai-changelog.md`
4. Create unit tests
5. Follow project coding standards

**VS Code Tasks** (Ctrl+Shift+P → "Tasks: Run Task"):
- `Generate File Summaries` - Update AI context summaries
- `Format Code` - Run Black formatter
- `Lint Code` - Run Ruff linter
- `Run Tests` - Execute test suite

See `.github/copilot-instructions.md` for coding standards.

---

## Requirements

- **Python**: ≥ 3.11
- **Core**: numpy, pandas, yfinance, scipy, pyyaml
- **Dev**: pytest, pytest-cov, black, ruff

See [docs/dependencies.md](docs/dependencies.md) for version requirements and justifications.

---

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Make changes (AI will auto-apply coding standards)
4. Run tests (`pytest`)
5. Format code (`black src/ tests/`)
6. Commit changes (`git commit -m 'Add AmazingFeature'`)
7. Push to branch (`git push origin feature/AmazingFeature`)
8. Open Pull Request

**Code Standards**: All code follows patterns in `.github/copilot-instructions.md`

---

## License

This project is open source and available under the MIT License.

---

*Documentation maintained with AI assistance - See [docs/ai-changelog.md](docs/ai-changelog.md)*  
*Last updated: 2025-11-26*

