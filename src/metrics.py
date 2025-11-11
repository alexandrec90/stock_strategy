import pandas as pd
import numpy as np

# Constants
WINDOW_SHORT = 20
WINDOW_LONG = 200
PREDICT_DAYS = 200

# Files
INPUT_CSV = 'stock_prices.csv'
OUTPUT_CSV = 'metrics.csv'

def log_linear_predict(window_prices, x_pred, window_len):
    """Fit log(price) = ln(a) + b*x by linear regression and predict price at x_pred.
    window_prices: array-like of length window_len (ordered oldest->newest)
    x_pred: scalar x where oldest of window is x=0 and current date is x=window_len
    Returns predicted_price (float) or raises if fit fails.
    """
    arr = np.asarray(window_prices, dtype=float)
    if np.any(arr <= 0):
        raise ValueError('Non-positive prices in window')
    x = np.arange(0, window_len)
    y = np.log(arr)
    # linear fit y = intercept + slope * x
    slope, intercept = np.polyfit(x, y, 1)
    ln_a = intercept
    b = slope
    ln_pred = ln_a + b * x_pred
    return float(np.exp(ln_pred))

def compute_metrics():
    df = pd.read_csv(INPUT_CSV, parse_dates=['Date'])
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

            # Normalized over last WINDOW_SHORT
            if i >= WINDOW_SHORT:
                window = prices[i-WINDOW_SHORT:i]
                wmin = min(window.min(), current_price)
                wmax = max(window.max(), current_price)
                if wmax == wmin:
                    norm20 = 0.5
                else:
                    norm20 = (current_price - wmin) / (wmax - wmin)
                norm20 = float(np.clip(norm20, 0.0, 1.0))
            else:
                norm20 = np.nan
            row['Normalized_20'] = norm20

            # Normalized over last WINDOW_LONG
            if i >= WINDOW_LONG:
                window = prices[i-WINDOW_LONG:i]
                wmin = min(window.min(), current_price)
                wmax = max(window.max(), current_price)
                if wmax == wmin:
                    norm200 = 0.5
                else:
                    norm200 = (current_price - wmin) / (wmax - wmin)
                norm200 = float(np.clip(norm200, 0.0, 1.0))
            else:
                norm200 = np.nan
            row['Normalized_200'] = norm200

            # 200-day projected return based on last WINDOW_SHORT (exp model)
            if i >= WINDOW_SHORT:
                window = prices[i-WINDOW_SHORT:i]
                try:
                    x_pred = WINDOW_SHORT + PREDICT_DAYS
                    pred_price = log_linear_predict(window, x_pred, WINDOW_SHORT)
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
                    pred_price = log_linear_predict(window, x_pred, WINDOW_LONG)
                    ret200 = pred_price / current_price if current_price != 0 else np.nan
                except Exception:
                    ret200 = np.nan
            else:
                ret200 = np.nan
            row['PredReturn_200exp'] = ret200

            results.append(row)

    res_df = pd.DataFrame(results)
    res_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved metrics to {OUTPUT_CSV} with {len(res_df)} rows")

if __name__ == '__main__':
    compute_metrics()
