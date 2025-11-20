from utils import load_stock_data, save_csv, normalize_window, log_linear_predict
from config import WINDOW_SHORT, WINDOW_LONG, PREDICT_DAYS, STOCK_PRICES_CSV, METRICS_CSV
import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def compute_metrics():
    logger.info("Loading stock price data...")
    try:
        df = load_stock_data(STOCK_PRICES_CSV)
    except FileNotFoundError:
        logger.error(f"Stock prices file not found. Run 'fetch' command first.")
        raise
    
    if df.empty:
        logger.error("Stock prices file is empty")
        raise ValueError("No data to process. Run fetch command first.")
    
    required_cols = ['Date', 'Symbol', 'Close']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    logger.info(f"Processing {len(df)} records for {df['Symbol'].nunique()} symbols")
    results = []
    symbols_processed = 0
    total_symbols = df['Symbol'].nunique()
    
    for symbol, group in df.groupby('Symbol'):
        symbols_processed += 1
        logger.info(f"Computing metrics for {symbol} ({symbols_processed}/{total_symbols})...")
        group = group.sort_values('Date').reset_index(drop=True)
        prices = group['Close'].values
        n = len(prices)
        for i in range(n):
            current_price = prices[i]
            row = {
                'Date': group.loc[i, 'Date'],
                'Symbol': symbol,
                'CurrentPrice': current_price,
            }
            # Normalized over last WINDOW_SHORT (or all available if fewer days)
            if i > 0:
                window_size = min(i, WINDOW_SHORT)
                window = prices[i-window_size:i]
                norm20 = normalize_window(window, current_price)
            else:
                # First entry: no prior data, set to neutral 0.5
                norm20 = 0.5
            row['Normalized_20'] = norm20
            # Normalized over last WINDOW_LONG (or all available if fewer days)
            if i > 0:
                window_size = min(i, WINDOW_LONG)
                window = prices[i-window_size:i]
                norm200 = normalize_window(window, current_price)
            else:
                # First entry: no prior data, set to neutral 0.5
                norm200 = 0.5
            row['Normalized_200'] = norm200
            # 200-day projected return based on last WINDOW_SHORT (exp model)
            if i >= WINDOW_SHORT:
                window = prices[i-WINDOW_SHORT:i]
                try:
                    x_pred = WINDOW_SHORT + PREDICT_DAYS
                    pred_price = log_linear_predict(window, x_pred)
                    ret20 = pred_price / current_price if current_price != 0 else np.nan
                except Exception:
                    ret20 = np.nan
            else:
                ret20 = np.nan
            row['PredReturn_20exp'] = ret20
            # 200-day projected return based on last WINDOW_LONG (exp model)
            if i >= WINDOW_LONG:
                window = prices[i-WINDOW_LONG:i]
                try:
                    x_pred = WINDOW_LONG + PREDICT_DAYS
                    pred_price = log_linear_predict(window, x_pred)
                    ret200 = pred_price / current_price if current_price != 0 else np.nan
                except Exception:
                    ret200 = np.nan
            else:
                ret200 = np.nan
            row['PredReturn_200exp'] = ret200
            results.append(row)
    res_df = pd.DataFrame(results)
    save_csv(res_df, METRICS_CSV)
    logger.info(f"Saved metrics to data/{METRICS_CSV} with {len(res_df)} rows")
    logger.info("Metrics computation complete!")

if __name__ == '__main__':
    compute_metrics()
