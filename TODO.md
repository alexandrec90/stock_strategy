# Project TODO

This file contains the project backlog and next actionable steps.

- [x] Create `TODO.md` file
- [x] Populate `TODO.md` with initial tasks (development, tests, CI, docs)

- [ ] Fetch data from Yahoo Finance
	- Implement data ingestion (e.g. `yfinance` or `pandas-datareader`).
	- Save raw OHLCV history to `data/` for reproducibility.

- [ ] Calculate basic metrics on prices
	- Compute 20-day and 200-day growth rates.
	- Compute 20-day and 200-day range score (volatility/normalized range).
	- Add implementations in `price_normalized.py` or `metrics.py`.

- [ ] Find investing models for those metrics
	- Research rule-based signals and simple ML models (logistic regression, random forest).
	- Prioritize interpretable models for initial experiments.

- [ ] Divide data into training/predict sets to evaluate models
	- Create time-aware splits (rolling window / expanding window).
	- Save splits and preprocessing pipeline to reproduce results.

- [ ] Evaluate models
	- Backtest strategies and compute performance metrics (return, drawdown, Sharpe).
	- Produce summary reports and visualizations in `reports/`.

- [ ] Figure out how to place paper orders on IBRK
	- Research Interactive Brokers API (IB API / IBKR Python / ib_insync) for paper trading.
	- Document auth and sandbox steps.

- [ ] Implement model on IBRK
	- Add order placement, position sizing, and safety checks.
	- Run in paper environment and log results.

- [ ] Add basic unit tests
	- Tests for `fetch_stocks.py` and `metrics.py`.

- [ ] Add CI workflow
	- Create GitHub Actions to run tests and lint on push.

- [ ] Format and lint
	- Add `black`, `isort`, and `flake8` with pre-commit hooks.

Notes:
- Keep this file updated as tasks progress. Use the internal tracker for automated status.
- I can update or split these tasks into smaller subtasks if you want.
