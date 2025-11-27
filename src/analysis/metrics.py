import logging

import numpy as np
import pandas as pd

from src.analysis.utils import load_stock_data, log_linear_predict, normalize_window, save_csv
from src.core.config import METRICS_CSV, PREDICT_DAYS, STOCK_PRICES_CSV, WINDOW_LONG, WINDOW_SHORT

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def compute_metrics() -> None:
    """Compute stock metrics for all symbols in stock_prices.csv.

    Only computes metrics when at least 200 past data points are available
    to ensure all indicators (Normalized_20/200, PredReturn_20exp/200exp)
    are fully calculable. Skips the first 199 rows per symbol.

    Args:
        None (reads from STOCK_PRICES_CSV via config)

    Returns:
        None (saves results to METRICS_CSV)

    Raises:
        FileNotFoundError: If stock_prices.csv is missing
        ValueError: If data is empty or missing required columns

    Examples:
        >>> compute_metrics()  # Computes and saves metrics
        # Output: Metrics saved to data/metrics.csv with X rows
    """
    logger.info("Loading stock price data...")
    try:
        df = load_stock_data(STOCK_PRICES_CSV)
    except FileNotFoundError:
        logger.error("Stock prices file not found. Run 'fetch' command first.")
        raise

    if df.empty:
        logger.error("Stock prices file is empty")
        raise ValueError("No data to process. Run fetch command first.")

    required_cols = ["Date", "Symbol", "Close"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    logger.info(f"Processing {len(df)} records for {df['Symbol'].nunique()} symbols")
    results = []
    symbols_processed = 0
    total_symbols = df["Symbol"].nunique()

    for symbol, group in df.groupby("Symbol"):
        symbols_processed += 1
        logger.info(f"Computing metrics for {symbol} ({symbols_processed}/{total_symbols})...")
        group = group.sort_values("Date").reset_index(drop=True)
        prices = group["Close"].values
        n = len(prices)

        # Only start computing when we have at least WINDOW_LONG (200) past data points
        # This ensures all metrics can be fully calculated without NaN or partial values
        start_idx = WINDOW_LONG
        if n <= start_idx:
            logger.warning(
                f"Skipping {symbol}: Only {n} data points, need at least "
                f"{start_idx + 1} for full metrics"
            )
            continue

        for i in range(start_idx, n):
            current_price = prices[i]
            row = {
                "Date": group.loc[i, "Date"],
                "Symbol": symbol,
                "CurrentPrice": current_price,
            }

            # Normalized over last WINDOW_SHORT (always available since
            # i >= WINDOW_LONG > WINDOW_SHORT)
            window_size = WINDOW_SHORT
            window = prices[i - window_size : i]
            norm20 = normalize_window(window, current_price)
            row["Normalized_20"] = norm20

            # Normalized over last WINDOW_LONG (always available since i >= WINDOW_LONG)
            window_size = WINDOW_LONG
            window = prices[i - window_size : i]
            norm200 = normalize_window(window, current_price)
            row["Normalized_200"] = norm200

            # 200-day projected return based on last WINDOW_SHORT (exp model)
            window = prices[i - WINDOW_SHORT : i]
            x_pred = WINDOW_SHORT + PREDICT_DAYS
            pred_price = log_linear_predict(window, x_pred)
            ret20 = pred_price / current_price if current_price != 0 else np.nan
            row["PredReturn_20exp"] = ret20

            # 200-day projected return based on last WINDOW_LONG (exp model)
            window = prices[i - WINDOW_LONG : i]
            x_pred = WINDOW_LONG + PREDICT_DAYS
            pred_price = log_linear_predict(window, x_pred)
            ret200 = pred_price / current_price if current_price != 0 else np.nan
            row["PredReturn_200exp"] = ret200

            results.append(row)

        logger.info(
            f"Processed {n - start_idx} rows for {symbol} (skipped first "
            f"{start_idx} due to insufficient history)"
        )

    res_df = pd.DataFrame(results)
    save_csv(res_df, METRICS_CSV)
    logger.info(f"Saved metrics to data/{METRICS_CSV} with {len(res_df)} rows")
    logger.info("Metrics computation complete!")


if __name__ == "__main__":
    compute_metrics()
