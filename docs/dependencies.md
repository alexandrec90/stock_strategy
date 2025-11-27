# Dependencies

Detailed documentation of all project dependencies with justifications.

---

## Core Dependencies

### numpy (>=1.24.0)
**PyPI**: https://pypi.org/project/numpy/  
**Purpose**: Numerical computing and array operations

**Used In**:
- `src/analysis/utils.py`: Array operations, mathematical functions
- `src/analysis/metrics.py`: NaN handling, data type conversions

**Key Functions**:
- `np.array()`: Convert lists to arrays for efficient computation
- `np.log()`, `np.exp()`: Logarithmic transformations for price modeling
- `np.polyfit()`: Linear regression for log-linear predictions
- `np.clip()`: Ensure normalized values stay in [0, 1] range
- `np.nan`: Represent missing/invalid metric values

**Version Rationale**: 
- `>=1.24.0`: Requires NumPy 2.0 compatibility improvements
- Provides better type hints for modern Python

**Alternative Considered**: None (industry standard for numerical Python)

---

### pandas (>=2.0.0)
**PyPI**: https://pypi.org/project/pandas/  
**Purpose**: DataFrame operations for tabular stock data

**Used In**:
- All modules: Primary data structure for stock prices and metrics
- `src/data/fetch_stocks.py`: Combine data from multiple symbols
- `src/analysis/metrics.py`: Group by symbol, process time series

**Key Functions**:
- `pd.read_csv()`: Load stock data from CSV files
- `pd.DataFrame()`: Structure for storing prices and metrics
- `df.groupby('Symbol')`: Process each stock independently
- `df.to_csv()`: Save computed metrics
- `pd.concat()`: Combine data from multiple symbols

**Version Rationale**:
- `>=2.0.0`: Major performance improvements for groupby operations
- Better datetime handling (critical for stock data)
- PyArrow backend support for faster CSV I/O

**Alternative Considered**: Raw CSV + NumPy (rejected: too low-level, error-prone)

---

### yfinance (>=0.2.0)
**PyPI**: https://pypi.org/project/yfinance/  
**Purpose**: Download historical stock prices from Yahoo Finance

**Used In**:
- `src/data/fetch_stocks.py`: Primary data source

**Key Functions**:
- `yf.Ticker(symbol)`: Create ticker object
- `ticker.history(start, end)`: Download OHLCV data for date range

**Why Yahoo Finance?**:
- Free, no API key required
- Reliable historical data
- Wide coverage (US and international stocks)

**Version Rationale**:
- `>=0.2.0`: Improved error handling for missing data
- Better support for datetime ranges

**Alternatives Considered**:
- Alpha Vantage: Requires API key, rate limits
- Quandl: Deprecated free tier
- IEX Cloud: Paid only

**Limitations**:
- Rate limiting (yfinance has informal limits)
- Delayed data (15-20 minutes for free tier)
- Occasional API changes (Yahoo doesn't officially support it)

---

### scipy (>=1.10.0)
**PyPI**: https://pypi.org/project/scipy/  
**Purpose**: Statistical functions and curve fitting

**Used In**:
- `src/analysis/utils.py`: Exponential curve fitting

**Key Functions**:
- `scipy.optimize.curve_fit()`: Fit exponential model to price data

**Why Needed?**:
- `fit_exponential()` uses non-linear curve fitting
- NumPy's `polyfit()` only handles linear/polynomial, not exponential

**Version Rationale**:
- `>=1.10.0`: Improved optimization algorithms
- Better convergence for curve_fit with financial data

**Usage Note**: 
- Currently used in `fit_exponential()` (experimental feature)
- Main predictions use `log_linear_predict()` with NumPy (more stable)

**Alternative Considered**: 
- Pure NumPy with log transform (used for main predictions)
- statsmodels (rejected: overkill for simple curve fitting)

---

### pyyaml (>=6.0)
**PyPI**: https://pypi.org/project/PyYAML/  
**Purpose**: Parse configuration from config.yaml

**Used In**:
- `src/core/config.py`: Load user configuration

**Key Functions**:
- `yaml.safe_load()`: Parse YAML file into Python dict

**Why YAML over JSON/TOML?**:
- Human-friendly (comments, multi-line strings)
- Widely supported
- Good for config files (vs JSON which lacks comments)

**Version Rationale**:
- `>=6.0`: Full Python 3.11+ support
- Security improvements (safe_load is default)

**Alternative Considered**: 
- JSON: No comments, less readable
- TOML: Good option, but YAML more familiar to users
- .env files: Too simplistic for nested config

---

### scikit-learn (>=1.3.0)
**PyPI**: https://pypi.org/project/scikit-learn/  
**Purpose**: Machine learning algorithms for trading models

**Used In**:
- `src/models/trading_model.py`: Random Forest classifier for buy/sell signals

**Key Functions**:
- `RandomForestClassifier()`: Ensemble model for classification
- `train_test_split()`: Split data for training/validation
- `GridSearchCV()`: Hyperparameter tuning
- `classification_report()`: Model evaluation metrics

**Why Scikit-learn?**:
- Industry standard for traditional ML
- Comprehensive algorithm library
- Excellent documentation and community support
- Integrates well with pandas/numpy ecosystem

**Version Rationale**:
- `>=1.3.0`: Improved performance for tree-based models
- Better support for pandas DataFrames
- Enhanced cross-validation tools

**Alternatives Considered**:
- XGBoost: More powerful for tabular data, but scikit-learn provides good baseline
- TensorFlow/PyTorch: Overkill for traditional ML, steeper learning curve

---

## Development Dependencies

### pytest (>=7.0.0)
**PyPI**: https://pypi.org/project/pytest/  
**Purpose**: Testing framework

**Used In**:
- `tests/` directory: All unit tests

**Key Features**:
- Simple test discovery (test_*.py files)
- Fixtures for reusable test data
- Detailed failure reporting

**Version Rationale**:
- `>=7.0.0`: Python 3.11 compatibility
- Better type hint support

---

### pytest-cov (>=4.0.0)
**PyPI**: https://pypi.org/project/pytest-cov/  
**Purpose**: Test coverage reporting

**Usage**:
```bash
pytest --cov=src --cov-report=html
```

**Why Needed?**: Identify untested code paths

---

### black (>=23.0.0)
**PyPI**: https://pypi.org/project/black/  
**Purpose**: Automatic code formatting

**Configuration**: See `[tool.black]` in `pyproject.toml`
- Line length: 100 characters
- Target: Python 3.11

**Why Black?**:
- Opinionated (no debates about formatting)
- Consistent output (deterministic)
- Widely adopted in Python community

**Usage**:
```bash
black src/ tests/
```

---

### ruff (>=0.1.0)
**PyPI**: https://pypi.org/project/ruff/  
**Purpose**: Fast linting and import sorting

**Configuration**: See `[tool.ruff]` in `pyproject.toml`
- Checks: errors (E), pyflakes (F), imports (I), naming (N), docstrings (D)
- Style: Google docstring convention

**Why Ruff?**:
- 10-100x faster than pylint/flake8
- Replaces multiple tools (flake8, isort, pydocstyle)
- Written in Rust for speed

**Usage**:
```bash
ruff check src/ tests/
ruff check --fix src/  # Auto-fix issues
```

---

## Dependency Graph

```
yfinance ─┐
          ├─→ pandas ──→ numpy
scipy ────┘

pyyaml (standalone)

pytest ──→ pytest-cov
black (standalone)
ruff (standalone)
```

**Key Insight**: Main computational stack is numpy → pandas → {yfinance, scipy}

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

Installs: Production + pytest, pytest-cov, black, ruff

---

## Version Pinning Strategy

**Current Approach**: Minimum version requirements (`>=X.Y.Z`)

**Rationale**:
- Allow users to use newer versions (forward compatibility)
- Pin minimum for features we depend on
- No upper bounds (avoid dependency conflicts)

**When to Update**:
- Security vulnerabilities: Bump minimum version
- New features needed: Bump minimum version
- Breaking changes: Test with new version, update code if needed

**Lock File**: Consider adding `requirements.txt` with exact versions for reproducibility:
```bash
pip freeze > requirements.txt
```

---

## Future Dependencies (Planned)

### ib_insync (for IBKR integration)
**Purpose**: Interact with Interactive Brokers API  
**Status**: Planned for src/trading/ibkr.py  
**Why**: Best Python wrapper for IBKR (async, well-maintained)

### plotly or matplotlib (for visualization)
**Purpose**: Chart stock prices and metrics  
**Status**: Under consideration  
**Decision**: Wait until visualization features requested

### SQLAlchemy (for database)
**Purpose**: Store data in SQLite/PostgreSQL instead of CSV  
**Status**: Future (when scaling beyond 100 symbols)  
**Why**: Better performance for large datasets, relationships

---

<!-- AI: When adding new dependencies:
1. Add to pyproject.toml [project.dependencies] with version and comment
2. Add new section above with:
   - Purpose
   - Used In
   - Key Functions
   - Version Rationale
   - Alternatives Considered
3. Update dependency graph if relationships change
4. Update README.md installation section
-->

*Last updated by AI: 2025-11-26*  
*Auto-maintained using `.github/copilot-instructions.md` standards*
