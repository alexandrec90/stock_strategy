import pandas as pd
import numpy as np

# Constants
WINDOW_DAYS = 20

# Files
input_csv = 'stock_prices.csv'
output_csv = 'price_normalized.csv'

# Load data
df = pd.read_csv(input_csv, parse_dates=['Date'])

results = []
for symbol, group in df.groupby('Symbol'):
    group = group.sort_values('Date').reset_index(drop=True)
    prices = group['Close'].values
    n = len(prices)

    for i in range(WINDOW_DAYS, n):
        window = prices[i-WINDOW_DAYS:i]
        current_price = prices[i]
        # normalized score: (current - min) / (max - min) over the window
        # include the current price in min/max so Normalized is always in [0,1]
        wmin = min(window.min(), current_price)
        wmax = max(window.max(), current_price)
        if wmax == wmin:
            # if all values equal (including current), choose neutral 0.5
            norm = 0.5
        else:
            norm = (current_price - wmin) / (wmax - wmin)
        # clamp to [0,1] to guard against rounding/noise
        norm = float(np.clip(norm, 0.0, 1.0))

        results.append({
            'Date': group.loc[i, 'Date'],
            'Symbol': symbol,
            'CurrentPrice': current_price,
            'Normalized': norm
        })

res_df = pd.DataFrame(results)
res_df.to_csv(output_csv, index=False)
print(f"Saved normalized scores to {output_csv} with {len(res_df)} rows")