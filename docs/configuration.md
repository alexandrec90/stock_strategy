# Configuration

Complete documentation of all configuration options in `config.yaml`.

---

## Overview

Stock Strategy uses a YAML configuration file (`config.yaml`) for all runtime parameters. This allows easy experimentation without changing code.

**Location**: Project root (`config.yaml`)  
**Format**: YAML (supports comments and nested structures)  
**Loading**: Automatically loaded by `src.core.config` on import

---

## Configuration Sections

### Data Settings

Configure data directory and file names.

```yaml
data:
  dir: data                          # Directory for all data files
  symbols_file: symbols.csv          # List of stock symbols to track
  stock_prices_file: stock_prices.csv  # Historical OHLCV data
  metrics_file: metrics.csv          # Computed metrics output
```

#### Options

**`data.dir`** (string)
- **Purpose**: Root directory for all data files
- **Default**: `data`
- **Type**: Relative or absolute path
- **Note**: Directory is auto-created if missing

**`data.symbols_file`** (string)
- **Purpose**: Filename of symbols list (relative to data.dir)
- **Default**: `symbols.csv`
- **Format**: CSV with `Symbol` column
- **Example**:
  ```csv
  Symbol
  AAPL
  MSFT
  ```

**`data.stock_prices_file`** (string)
- **Purpose**: Filename for downloaded stock prices
- **Default**: `stock_prices.csv`
- **Written by**: `src.data.fetch_stocks`
- **Columns**: Date, Symbol, Open, High, Low, Close, Volume

**`data.metrics_file`** (string)
- **Purpose**: Filename for computed metrics
- **Default**: `metrics.csv`
- **Written by**: `src.analysis.metrics`
- **Columns**: Date, Symbol, CurrentPrice, Normalized_20, Normalized_200, PredReturn_20exp, PredReturn_200exp

---

### Fetch Settings

Configure data fetching behavior.

```yaml
fetch:
  lookback_days: 500  # Number of days of historical data to download
```

#### Options

**`fetch.lookback_days`** (integer)
- **Purpose**: How many days of history to download
- **Default**: 500 (~2 years of trading days)
- **Range**: 1 to 10,000+
- **Recommendation**: 
  - Minimum: 250 days (for 200-day window calculations)
  - Typical: 500-730 days (2 years)
  - Maximum: Limited by data availability (varies by symbol)

**Examples**:
```yaml
lookback_days: 250   # 1 year (minimum for metrics)
lookback_days: 730   # 2 years (recommended)
lookback_days: 1825  # 5 years (for long-term analysis)
```

**Note**: Yahoo Finance typically provides 10+ years of daily data for most symbols.

---

### Metrics Settings

Configure technical indicator calculations.

```yaml
metrics:
  window_short: 20    # Short-term window (days)
  window_long: 200    # Long-term window (days)
  predict_days: 200   # Forecast horizon (days)
```

#### Options

**`metrics.window_short`** (integer)
- **Purpose**: Short-term lookback window for calculations
- **Default**: 20 days (~1 month of trading days)
- **Used For**:
  - `Normalized_20`: Price position within 20-day range
  - `PredReturn_20exp`: Prediction based on 20-day trend
- **Typical Values**: 10, 20, 50
- **Financial Context**: 20-day SMA is a common short-term indicator

**`metrics.window_long`** (integer)
- **Purpose**: Long-term lookback window for calculations
- **Default**: 200 days (~10 months of trading days)
- **Used For**:
  - `Normalized_200`: Price position within 200-day range
  - `PredReturn_200exp`: Prediction based on 200-day trend
- **Typical Values**: 50, 100, 200
- **Financial Context**: 200-day SMA is a standard long-term indicator

**`metrics.predict_days`** (integer)
- **Purpose**: How far into the future to predict (forecast horizon)
- **Default**: 200 days (~10 months ahead)
- **Used For**: Both `PredReturn_20exp` and `PredReturn_200exp`
- **Range**: 1 to 365+
- **Note**: Longer horizons = less reliable predictions

**Examples**:

```yaml
# Conservative (shorter windows)
metrics:
  window_short: 10
  window_long: 50
  predict_days: 30

# Standard (default)
metrics:
  window_short: 20
  window_long: 200
  predict_days: 200

# Long-term focus
metrics:
  window_short: 50
  window_long: 200
  predict_days: 365
```

**Important**: Ensure `lookback_days >= window_long` or early data points will have insufficient history.

---

### IBKR Settings

Configure Interactive Brokers TWS/Gateway connection.

```yaml
ibkr:
  host: 127.0.0.1  # TWS/Gateway hostname
  port: 7497       # TWS paper trading port
  client_id: 101   # Unique client identifier
  account: PAPER   # Account type (PAPER or LIVE)
```

#### Options

**`ibkr.host`** (string)
- **Purpose**: Hostname of Interactive Brokers TWS or Gateway
- **Default**: `127.0.0.1` (localhost)
- **Typical**: `127.0.0.1` (local) or IP address (remote)

**`ibkr.port`** (integer)
- **Purpose**: Socket port for TWS/Gateway API
- **Default**: 7497 (TWS paper trading)
- **Standard Ports**:
  - `7497`: TWS paper trading
  - `7496`: TWS live trading
  - `4002`: Gateway paper trading
  - `4001`: Gateway live trading

**`ibkr.client_id`** (integer)
- **Purpose**: Unique identifier for this client connection
- **Default**: 101
- **Range**: 0-32,767
- **Note**: Each connection must have unique client_id

**`ibkr.account`** (string)
- **Purpose**: Account type indicator
- **Default**: `PAPER`
- **Values**: 
  - `PAPER`: Paper trading (simulated)
  - `LIVE`: Live trading (real money)
- **Safety**: Always test with PAPER first!

**Security Note**: This module is under development. Always verify trades in TWS before enabling live trading.

---

## Example Configurations

### Minimal (Fast Testing)
```yaml
data:
  dir: data
  symbols_file: symbols.csv
  stock_prices_file: stock_prices.csv
  metrics_file: metrics.csv

fetch:
  lookback_days: 250  # Just enough for 200-day window

metrics:
  window_short: 10
  window_long: 50
  predict_days: 30

ibkr:
  host: 127.0.0.1
  port: 7497
  client_id: 101
  account: PAPER
```

### Production (Recommended)
```yaml
data:
  dir: data
  symbols_file: symbols.csv
  stock_prices_file: stock_prices.csv
  metrics_file: metrics.csv

fetch:
  lookback_days: 730  # 2 years

metrics:
  window_short: 20    # Industry standard
  window_long: 200    # Industry standard
  predict_days: 200

ibkr:
  host: 127.0.0.1
  port: 7497
  client_id: 101
  account: PAPER  # Change to LIVE only when ready
```

### Research (Maximum History)
```yaml
data:
  dir: data
  symbols_file: symbols.csv
  stock_prices_file: stock_prices.csv
  metrics_file: metrics.csv

fetch:
  lookback_days: 3650  # 10 years

metrics:
  window_short: 50
  window_long: 200
  predict_days: 365

ibkr:
  host: 127.0.0.1
  port: 7497
  client_id: 101
  account: PAPER
```

---

## Accessing Configuration in Code

**Always use `src.core.config` constants**. Never hardcode values.

```python
# GOOD: Use config constants
from src.core.config import WINDOW_SHORT, PREDICT_DAYS

window = prices[-WINDOW_SHORT:]
prediction = model.predict(horizon=PREDICT_DAYS)

# BAD: Hardcoded values (DO NOT DO THIS)
window = prices[-20:]  # What if user changes config?
prediction = model.predict(horizon=200)  # Inflexible
```

**Available Constants**:
```python
from src.core.config import (
    # Data paths
    DATA_DIR,
    SYMBOLS_CSV,
    STOCK_PRICES_CSV,
    METRICS_CSV,
    
    # Fetch settings
    LOOKBACK_DAYS,
    
    # Metrics settings
    WINDOW_SHORT,
    WINDOW_LONG,
    PREDICT_DAYS,
    
    # IBKR settings
    IBKR_HOST,
    IBKR_PORT,
    IBKR_CLIENT_ID,
    IBKR_ACCOUNT,
)
```

---

## Validation

The config system performs basic validation on load (in `src/core/config.py`).

**Automatic Checks**:
- File existence: `config.yaml` must exist
- Valid YAML: Must parse without errors
- Required keys: All sections must be present

**Runtime Validation**:
- File paths: Checked when files are accessed
- Numeric ranges: Checked by individual functions

**Error Messages**: If config is invalid, you'll see clear error on import.

---

## Customization

### Creating a Custom Config

1. Copy `config.yaml` to `config.custom.yaml`
2. Modify values
3. Load custom config:

```python
from src.core.config import load_config

config = load_config('config.custom.yaml')
WINDOW_SHORT = config['metrics']['window_short']
```

### Environment-Specific Configs

```bash
config.dev.yaml     # Development settings
config.prod.yaml    # Production settings
config.test.yaml    # Testing settings
```

Use environment variable to switch:
```python
import os
config_file = os.getenv('CONFIG_FILE', 'config.yaml')
config = load_config(config_file)
```

---

<!-- AI: When adding new config options:
1. Add to config.yaml with sensible default
2. Document in this file with purpose, range, examples
3. Add constant to src/core/config.py
4. Update src/core/config.py docstring
5. Add to "Available Constants" section above
-->

*Last updated by AI: 2025-11-26*  
*Auto-maintained using `.github/copilot-instructions.md` standards*
