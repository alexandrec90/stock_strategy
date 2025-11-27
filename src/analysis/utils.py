import os

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def load_stock_data(filename):
    """Load stock data from data/ folder."""
    return pd.read_csv(os.path.join("data", filename), parse_dates=["Date"])


def save_csv(df, filename):
    """Save DataFrame to data/ folder as CSV."""
    df.to_csv(os.path.join("data", filename), index=False)


def exp_func(x, a, b):
    return a * np.exp(b * x)


def fit_exponential(window_prices):
    """Fit exponential model to window_prices."""
    window_days = np.arange(0, len(window_prices))
    p0 = [window_prices[0], 0.001]
    params, _ = curve_fit(exp_func, window_days, window_prices, p0=p0, maxfev=10000)
    return params


def normalize_window(window, current_price):
    wmin = min(window.min(), current_price)
    wmax = max(window.max(), current_price)
    if wmax == wmin:
        return 0.5
    norm = (current_price - wmin) / (wmax - wmin)
    return float(np.clip(norm, 0.0, 1.0))


def log_linear_predict(window_prices, x_pred):
    arr = np.asarray(window_prices, dtype=float)
    if np.any(arr <= 0):
        raise ValueError("Non-positive prices in window")
    x = np.arange(0, len(window_prices))
    y = np.log(arr)
    slope, intercept = np.polyfit(x, y, 1)
    ln_pred = intercept + slope * x_pred
    return float(np.exp(ln_pred))
