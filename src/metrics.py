from utils import load_stock_data, save_csv, normalize_window, log_linear_predict
from config import WINDOW_SHORT, WINDOW_LONG, PREDICT_DAYS, STOCK_PRICES_CSV, METRICS_CSV
import pandas as pd
import numpy as np

def compute_metrics():
    df = load_stock_data(STOCK_PRICES_CSV)
    results = []
    for symbol, group in df.groupby('Symbol'):
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
    print(f"Saved metrics to data/{METRICS_CSV} with {len(res_df)} rows")

if __name__ == '__main__':
    compute_metrics()
