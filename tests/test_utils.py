"""Tests for utility functions."""
import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.analysis.utils import normalize_window, log_linear_predict, exp_func


def test_normalize_window_normal_range():
    """Test normalization with typical price range."""
    window = np.array([100, 105, 110, 95, 100])
    current_price = 107
    result = normalize_window(window, current_price)
    assert 0.0 <= result <= 1.0
    assert result > 0.5  # Current price is above middle


def test_normalize_window_at_max():
    """Test normalization when current price is at max."""
    window = np.array([100, 105, 110, 95, 100])
    current_price = 110
    result = normalize_window(window, current_price)
    assert result == 1.0


def test_normalize_window_at_min():
    """Test normalization when current price is at min."""
    window = np.array([100, 105, 110, 95, 100])
    current_price = 95
    result = normalize_window(window, current_price)
    assert result == 0.0


def test_normalize_window_all_equal():
    """Test normalization when all prices are equal."""
    window = np.array([100, 100, 100, 100])
    current_price = 100
    result = normalize_window(window, current_price)
    assert result == 0.5


def test_exp_func():
    """Test exponential function."""
    result = exp_func(0, 100, 0.01)
    assert result == pytest.approx(100)
    result = exp_func(10, 100, 0.01)
    assert result > 100


def test_log_linear_predict_positive_growth():
    """Test prediction with positive growth trend."""
    window = np.array([100, 102, 104, 106, 108])
    x_pred = 10
    result = log_linear_predict(window, x_pred)
    assert result > 108  # Should predict higher


def test_log_linear_predict_negative_prices_raises():
    """Test that negative prices raise error."""
    window = np.array([100, -50, 104])
    with pytest.raises(ValueError):
        log_linear_predict(window, 5)
