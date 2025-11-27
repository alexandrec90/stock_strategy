# Architecture

System design and data flow for the stock_strategy project.

---

## Overview

Stock Strategy is a Python-based tool for analyzing stock data using technical indicators and predictive models. The system follows a pipeline architecture:

```
[Symbols List] → [Fetch] → [Stock Prices] → [Compute] → [Metrics] → [Analysis/Trading]
```

---

## Directory Structure

```
stock_strategy/
├── src/
│   ├── analysis/          # Metrics computation and analysis
│   │   ├── metrics.py     # Main metrics computation logic
│   │   └── utils.py       # Helper functions (normalize, predict)
│   ├── core/              # Configuration and shared utilities
│   │   └── config.py      # Load config.yaml and provide constants
│   ├── data/              # Data fetching and management
│   │   └── fetch_stocks.py # Download stock prices via yfinance
│   ├── trading/           # Trading integration (IBKR)
│   │   └── ibkr.py        # Interactive Brokers API wrapper
│   └── cli.py             # Command-line interface
├── data/                  # Generated data files (gitignored)
│   ├── symbols.csv        # List of stock symbols to track
│   ├── stock_prices.csv   # Historical OHLCV data
│   └── metrics.csv        # Computed technical metrics
├── tests/                 # Unit tests
├── docs/                  # Documentation
└── config.yaml            # Configuration file
```

---

## Data Flow

### 1. Symbol Definition
**File**: `data/symbols.csv`  
**Format**: CSV with `Symbol` column  
**Purpose**: Define which stocks to analyze

```csv
Symbol
AAPL
MSFT
GOOGL
```

### 2. Data Fetching
**Module**: `src.data.fetch_stocks`  
**Command**: `stock-strategy fetch` (or run directly)  
**Process**:
1. Read symbols from `data/symbols.csv`
2. Calculate date range (LOOKBACK_DAYS from config)
3. Download historical data using yfinance
4. Combine all data into single DataFrame
5. Save to `data/stock_prices.csv`

**Output**: `data/stock_prices.csv`
```csv
Date,Symbol,Open,High,Low,Close,Volume
2024-01-01,AAPL,150.0,152.0,149.5,151.5,1000000
```

### 3. Metrics Computation
**Module**: `src.analysis.metrics`  
**Command**: `stock-strategy compute` (or run directly)  
**Process**:
1. Load stock prices from `data/stock_prices.csv`
2. Group by symbol
3. For each symbol, process chronologically:
   - Calculate normalized positions (20-day and 200-day windows)
   - Predict future returns using log-linear regression
4. Save all metrics to `data/metrics.csv`

**Output**: `data/metrics.csv`
```csv
Date,Symbol,CurrentPrice,Normalized_20,Normalized_200,PredReturn_20exp,PredReturn_200exp
2024-01-01,AAPL,151.5,0.75,0.68,1.15,1.22
```

### 4. Analysis & Trading
**Status**: Under development  
**Planned**: Use metrics to rank stocks, generate signals, execute trades via IBKR

---

## Key Algorithms

### Normalization (`normalize_window`)

Maps current price to position within historical range.

**Formula**:
```
normalized = (current_price - min_price) / (max_price - min_price)
```

**Range**: [0, 1]
- 0 = at historical minimum (oversold)
- 1 = at historical maximum (overbought)
- 0.5 = neutral (or when min == max)

**Use Case**: Identify if stock is trading at relative highs/lows compared to recent history.

### Log-Linear Prediction (`log_linear_predict`)

Predicts future price assuming exponential growth.

**Why Exponential?** Stock prices tend to grow exponentially due to compounding returns. A stock growing 10% per year doubles in ~7 years (exponential), not linearly.

**Algorithm**:
1. Take log of historical prices: `y = log(price)`
2. Fit linear regression: `y = mx + b`
3. Extrapolate to future point: `y_pred = m * x_pred + b`
4. Convert back: `price_pred = exp(y_pred)`

**Example**:
```python
# Prices: [100, 110, 121, 133]  (growing ~10% per period)
# Log prices: [4.605, 4.700, 4.796, 4.890]  (linear growth)
# Fit line, predict at x=10
# Result: exp(predicted_log) ≈ 259
```

**Use Case**: Estimate where price might be in PREDICT_DAYS (200 days) based on recent trend.

---

## Configuration System

### File: `config.yaml`

Central configuration for all parameters. Never hardcode values in code.

**Structure**:
```yaml
data:
  dir: "data"
  symbols_file: "symbols.csv"
  stock_prices_file: "stock_prices.csv"
  metrics_file: "metrics.csv"

fetch:
  lookback_days: 730  # 2 years

metrics:
  window_short: 20    # 20-day window
  window_long: 200    # 200-day window
  predict_days: 200   # Forecast 200 days ahead
```

### Loading: `src.core.config`

Reads `config.yaml` and exposes constants:

```python
from src.core.config import WINDOW_SHORT, PREDICT_DAYS

# Use constants instead of hardcoding
window = prices[-WINDOW_SHORT:]
```

**Benefits**:
- Single source of truth
- Easy experimentation (change one value)
- AI-friendly (clear what values are configurable)

---

## Performance Characteristics

### `fetch_stocks.main()`
- **Complexity**: O(n) where n = number of symbols
- **Bottleneck**: Network I/O (yfinance API calls)
- **Time**: ~1-2 seconds per symbol
- **Optimization**: Could parallelize API calls

### `compute_metrics()`
- **Complexity**: O(n * m * w) where:
  - n = number of symbols
  - m = days of history per symbol
  - w = window size for calculations
- **Bottleneck**: Row-by-row iteration in metrics.py
- **Time**: ~2 seconds per symbol (1000 days of data)
- **Optimization Potential**: 
  - Vectorize using pandas.rolling()
  - Current: ~2 minutes for 50 symbols
  - Optimized: ~10 seconds estimated

### Memory Usage
- **Stock Prices**: ~1 KB per row → ~5 MB for 50 symbols, 2 years daily data
- **Metrics**: Similar to stock prices (same row count)
- **Peak Memory**: <50 MB for typical workloads

---

## Module Dependencies

```
src.cli
  └─ src.data.fetch_stocks
  └─ src.analysis.metrics

src.data.fetch_stocks
  ├─ yfinance (external)
  ├─ pandas (external)
  └─ src.core.config

src.analysis.metrics
  ├─ src.analysis.utils
  └─ src.core.config

src.analysis.utils
  ├─ pandas (external)
  ├─ numpy (external)
  └─ scipy (external)

src.trading.ibkr
  └─ src.core.config
```

**External Dependencies**: See `docs/dependencies.md` for detailed justifications.

---

## Extension Points

### Adding New Metrics

1. Add calculation function to `src/analysis/utils.py`
2. Call from `compute_metrics()` in `src/analysis/metrics.py`
3. Add column to output DataFrame
4. Document in `docs/api-reference.md`

**Example**: Adding RSI (Relative Strength Index)

```python
# In src/analysis/utils.py
def calculate_rsi(prices: np.ndarray, window: int = 14) -> float:
    """Calculate RSI indicator."""
    # Implementation...
    pass

# In src/analysis/metrics.py, inside the loop:
if i >= 14:
    row['RSI'] = calculate_rsi(prices[i-14:i])
else:
    row['RSI'] = np.nan
```

### Adding New Data Sources

1. Create new module in `src/data/`
2. Follow pattern: read config, fetch data, save to CSV
3. Add to CLI commands in `src/cli.py`
4. Document data format in this file

---

## Error Handling Strategy

### Fetch Phase
- Missing symbols.csv → FileNotFoundError with helpful message
- Network errors → Log warning, continue with other symbols
- No data retrieved → ValueError at end (fail fast)

### Compute Phase
- Missing stock_prices.csv → FileNotFoundError with instruction to run fetch
- Empty file → ValueError
- Calculation errors (e.g., negative prices) → Log warning, set to NaN, continue

### Philosophy
- **Fail fast** on configuration errors (missing files, wrong format)
- **Fail soft** on calculation errors (NaN, log, continue)
- **Always log** important events for debugging

---

## Future Architecture Considerations

### Planned Features
- [ ] Portfolio optimization module
- [ ] Backtesting framework
- [ ] Real-time data streaming
- [ ] Interactive Brokers live trading

### Scalability
- Current: ~100 symbols, daily data
- Future: 1000+ symbols → Need database (SQLite/PostgreSQL)
- Future: Intraday data → Need time-series optimizations

---

<!-- AI: Update this file when:
- Adding new modules
- Changing data flow
- Modifying core algorithms
- Adding external integrations
-->

*Last updated by AI: 2025-11-26*  
*Auto-maintained using `.github/copilot-instructions.md` standards*
