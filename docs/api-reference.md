# API Reference

Comprehensive documentation of all public functions and classes in the stock_strategy project.

---

## Module: `src.analysis.metrics`

**Purpose**: Calculate technical indicators and metrics for stock analysis  
**Output**: Generates `data/metrics.csv` with normalized prices and predictions

### Functions

#### `compute_metrics()`

**Signature**: `compute_metrics() -> None`

**Description**: Process all stock symbols and compute technical metrics for each date/symbol combination. Only computes metrics when at least 200 past data points are available to ensure all indicators are fully calculable. Skips the first 199 rows per symbol.

**Workflow**:
1. Load historical stock prices from `data/stock_prices.csv`
2. For each symbol with ≥200 data points, compute metrics starting from the 200th day:
   - `Normalized_20`: Price position within 20-day range [0,1]
   - `Normalized_200`: Price position within 200-day range [0,1]
   - `PredReturn_20exp`: 200-day predicted return using 20-day exponential model
   - `PredReturn_200exp`: 200-day predicted return using 200-day exponential model
3. Save results to `data/metrics.csv`

**Returns**: None (writes to file)

**Raises**:
- `FileNotFoundError`: If `stock_prices.csv` is missing
- `ValueError`: If stock prices file is empty or missing required columns

**Performance**: Approximately 2 seconds per symbol on average hardware

**Example Usage**:
```python
from src.analysis.metrics import compute_metrics

compute_metrics()
# Output: data/metrics.csv with complete metrics (no partial/NaN values)
```

---

## Module: `src.analysis.utils`

**Purpose**: Utility functions for data loading, saving, and calculations  
**Dependencies**: pandas, numpy, scipy

### Functions

#### `load_stock_data(filename: str) -> pd.DataFrame`

**Description**: Load stock data from the data directory.

**Args**:
- `filename`: Name of CSV file in data/ directory

**Returns**: DataFrame with stock data (Date column parsed as datetime)

**Example**:
```python
df = load_stock_data('stock_prices.csv')
```

---

#### `save_csv(df: pd.DataFrame, filename: str) -> None`

**Description**: Save DataFrame to data directory as CSV.

**Args**:
- `df`: DataFrame to save
- `filename`: Name of output CSV file

**Returns**: None

---

#### `normalize_window(window: np.ndarray, current_price: float) -> float`

**Description**: Calculate normalized position of current price within historical range.

**Algorithm**: Maps current price to [0,1] where:
- 0 = at or below historical minimum
- 1 = at or above historical maximum
- 0.5 = neutral (returned when min == max)

**Args**:
- `window`: Array of historical prices
- `current_price`: Current price to normalize

**Returns**: Normalized value in range [0, 1]

**Example**:
```python
window = np.array([100, 110, 105, 115])
current = 112
normalized = normalize_window(window, current)  # Returns ~0.80 (80% of range)
```

---

#### `log_linear_predict(window_prices: np.ndarray, x_pred: float) -> float`

**Description**: Predict future price using log-linear regression (exponential growth model).

**Algorithm**: 
1. Perform linear regression on log(prices)
2. Extrapolate to x_pred time point
3. Return exp(predicted_log_price)

**Why Log-Linear**: Stock prices tend to grow exponentially over time. Linear regression on log(price) captures this pattern better than raw price regression.

**Args**:
- `window_prices`: Array of historical prices for regression
- `x_pred`: Future time point to predict (days from start of window)

**Returns**: Predicted price at x_pred

**Raises**:
- `ValueError`: If window contains non-positive prices

**Example**:
```python
prices = np.array([100, 102, 105, 108, 110])
# Predict 10 days after the 5-day window ends
predicted = log_linear_predict(prices, x_pred=15)
```

---

#### `fit_exponential(window_prices: np.ndarray) -> tuple`

**Description**: Fit exponential model to price window using curve fitting.

**Args**:
- `window_prices`: Array of historical prices

**Returns**: Tuple of (a, b) parameters where price = a * exp(b * x)

---

## Module: `src.data.fetch_stocks`

**Purpose**: Download historical stock prices from Yahoo Finance  
**Output**: Saves to `data/stock_prices.csv`

### Functions

#### `main() -> None`

**Description**: Fetch historical stock data for all symbols in `data/symbols.csv`.

**Workflow**:
1. Read symbols from `data/symbols.csv`
2. Calculate date range (LOOKBACK_DAYS from config)
3. Download data using yfinance for each symbol
4. Combine all data and save to `data/stock_prices.csv`

**Returns**: None (writes to file)

**Raises**:
- `FileNotFoundError`: If `symbols.csv` not found
- `ValueError`: If no symbols in file or no data retrieved

**Example Usage**:
```python
from src.data.fetch_stocks import main

main()
# Output: data/stock_prices.csv with Date, Symbol, Open, High, Low, Close, Volume
```

---

## Module: `src.core.config`

**Purpose**: Load and provide configuration constants from `config.yaml`  
**Pattern**: Import constants directly (never hardcode values in code)

### Constants

#### Data Paths
- `DATA_DIR`: Directory for data files
- `SYMBOLS_CSV`: Path to symbols list file
- `STOCK_PRICES_CSV`: Filename for stock prices
- `METRICS_CSV`: Filename for computed metrics

#### Fetch Settings
- `LOOKBACK_DAYS`: Number of days of historical data to fetch

#### Metrics Settings
- `WINDOW_SHORT`: Short-term window size (default: 20 days)
- `WINDOW_LONG`: Long-term window size (default: 200 days)
- `PREDICT_DAYS`: Forecast horizon (default: 200 days)

#### IBKR Settings
- `IBKR_HOST`: Interactive Brokers TWS/Gateway host
- `IBKR_PORT`: Connection port
- `IBKR_CLIENT_ID`: Client identifier
- `IBKR_ACCOUNT`: Account type (LIVE/PAPER)

**Example Usage**:
```python
from src.core.config import WINDOW_SHORT, PREDICT_DAYS

# Use config constants instead of hardcoding
window = prices[-WINDOW_SHORT:]
```

---

## Module: `src.cli`

**Purpose**: Command-line interface for stock_strategy  
**Entry Point**: `stock-strategy` command (defined in pyproject.toml)

<!-- AI: Document CLI commands here when implemented -->

---

## Module: `src.trading.ibkr`

**Purpose**: Interactive Brokers integration for trading  
**Status**: Under development

<!-- AI: Document IBKR functions here when implemented -->

---

## Module: `src.models`

**Purpose**: Machine learning models for trading strategy development  
**Output**: Trained classifiers for buy/sell signal prediction

### Classes

#### `TradingModel` (Abstract Base Class)

**Description**: Abstract interface for trading models that predict buy/sell signals.

**Methods**:
- `train(data: pd.DataFrame, **kwargs) -> None`: Train model on historical data
- `predict(data: pd.DataFrame) -> np.ndarray`: Generate predictions (0=Hold, 1=Buy, 2=Sell)
- `evaluate(data: pd.DataFrame) -> Dict`: Evaluate model performance

---

#### `RandomForestTradingModel(TradingModel)`

**Description**: Random Forest classifier for trading signal prediction using technical indicators.

**Initialization**:
```python
model = RandomForestTradingModel(
    n_estimators=100,
    max_depth=None,
    feature_cols=["Normalized_20", "Normalized_200", "PredReturn_20exp", "PredReturn_200exp"]
)
```

**Key Methods**:

##### `create_labels(data: pd.DataFrame, ...) -> pd.DataFrame`

**Description**: Create buy/sell/hold labels based on future price movements.

**Args**:
- `data`: DataFrame with price data
- `price_col`: Column name for current price (default: "CurrentPrice")
- `forward_days`: Days to look ahead (default: 5)
- `buy_threshold`: Minimum % increase for Buy (default: 0.02)
- `sell_threshold`: Maximum % decrease for Sell (default: -0.02)

**Returns**: DataFrame with added 'signal' column (0=Hold, 1=Buy, 2=Sell)

**Example**:
```python
labeled_data = model.create_labels(metrics_df)
```

##### `train(data: pd.DataFrame, tune_hyperparams=False) -> None`

**Description**: Train the Random Forest model with optional hyperparameter tuning.

**Args**:
- `data`: DataFrame with features and target labels
- `tune_hyperparams`: Whether to perform grid search (default: False)

**Example**:
```python
model.train(labeled_data, tune_hyperparams=True)
```

##### `predict(data: pd.DataFrame) -> np.ndarray`

**Description**: Generate buy/sell/hold predictions for new data.

**Args**:
- `data`: DataFrame with features (no target column)

**Returns**: Array of predictions (0=Hold, 1=Buy, 2=Sell)

##### `evaluate(data: pd.DataFrame) -> Dict`

**Description**: Evaluate model performance with classification metrics.

**Returns**: Dictionary with accuracy, precision, recall, F1-score for each class

##### `get_feature_importance() -> Dict`

**Description**: Get feature importance scores from trained model.

**Returns**: Dictionary mapping feature names to importance scores

**Example Usage**:
```python
from src.models import RandomForestTradingModel
import pandas as pd

# Load metrics data
metrics = pd.read_csv("data/metrics.csv")

# Create model
model = RandomForestTradingModel()

# Create labels based on 5-day future returns
labeled_data = model.create_labels(metrics)

# Train model
model.train(labeled_data)

# Make predictions
predictions = model.predict(metrics)

# Evaluate performance
results = model.evaluate(labeled_data)
print(f"Accuracy: {results['accuracy']:.3f}")

# Check feature importance
importance = model.get_feature_importance()
print("Top features:", sorted(importance.items(), key=lambda x: x[1], reverse=True)[:3])
```

---

---

## Module: `src.utils.docstring_summarizer`

**Purpose**: Generate concise AI-friendly summaries of Python files  
**Output**: Updates `docs/file-summaries.md`

### Functions

#### `summarize_file(file_path: Path) -> str`

**Description**: Generate AI-friendly summary of a single Python file.

**Args**:
- `file_path`: Path to .py file to summarize

**Returns**: Markdown summary string

**Raises**:
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If file is not valid Python

---

#### `summarize_project(root_path: Path, output_file: Path) -> None`

**Description**: Generate summaries for all .py files in project and save to file.

**Args**:
- `root_path`: Project root directory
- `output_file`: Where to save the combined summary

**Returns**: None (writes to file)

**Example Usage**:
```python
from src.utils.docstring_summarizer import summarize_project
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
output = project_root / "docs" / "file-summaries.md"
summarize_project(project_root, output)
```

---

<!-- AI: When adding new functions, add them to the appropriate module section above.
     Follow this template:

#### `function_name(param: Type) -> ReturnType`

**Description**: Brief description

**Args**:
- `param`: Description

**Returns**: Description

**Example**:
```python
result = function_name(value)
```
-->

---

*Last updated by AI: 2025-11-26*  
*Auto-maintained using `.github/copilot-instructions.md` standards*

