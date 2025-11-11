import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from datetime import timedelta

# Exponential function for curve fitting
def exp_func(x, a, b):
    return a * np.exp(b * x)

# Read data
input_csv = 'stock_prices.csv'
output_csv = 'predicted_returns.csv'

# Constants
WINDOW_DAYS = 20
PREDICT_DAYS = 200

# Load CSV
df = pd.read_csv(input_csv, parse_dates=['Date'])

# We'll work per symbol
results = []

for symbol, group in df.groupby('Symbol'):
    group = group.sort_values('Date').reset_index(drop=True)
    # Use Close price for modeling
    prices = group['Close'].values
    dates = group['Date'].values

    n = len(prices)
    # For each date starting from index WINDOW_DAYS (i.e., at least WINDOW_DAYS prior days available)
    for i in range(WINDOW_DAYS, n):
        # Use previous WINDOW_DAYS: indices i-WINDOW_DAYS .. i-1
        window_prices = prices[i-WINDOW_DAYS:i]
        window_days = np.arange(0, WINDOW_DAYS)  # day 0 .. WINDOW_DAYS-1

        # Fit exponential model to the window
        try:
            # Provide initial guesses to help convergence
            p0 = [window_prices[0], 0.001]
            params, _ = curve_fit(exp_func, window_days, window_prices, p0=p0, maxfev=10000)
            a, b = params

            # Predict price PREDICT_DAYS from the current date.
            # Our x for window start is 0 at oldest of window (i-WINDOW_DAYS).
            # The current date corresponds to x = WINDOW_DAYS (since window covers 0..WINDOW_DAYS-1 and next day is index WINDOW_DAYS).
            x_pred = WINDOW_DAYS + PREDICT_DAYS
            pred_price = exp_func(x_pred, a, b)

            current_price = prices[i]
            ret = pred_price / current_price if current_price != 0 else np.nan

            results.append({
                'Date': group.loc[i, 'Date'],
                'Symbol': symbol,
                'CurrentPrice': current_price,
                'PredictedPrice200d': pred_price,
                'Return': ret
            })
        except Exception as e:
            # If fit fails, skip
            # Optionally, could log the error
            continue

# Save results
res_df = pd.DataFrame(results)
res_df.to_csv(output_csv, index=False)
print(f"Saved predictions to {output_csv} with {len(res_df)} rows")
