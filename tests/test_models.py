"""Tests for trading models in src.models."""

import numpy as np
import pandas as pd
import pytest

from src.models import RandomForestTradingModel


@pytest.fixture
def sample_metrics_data():
    """Create sample metrics data for testing."""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=100, freq="D")
    symbols = ["AAPL"] * 50 + ["GOOG"] * 50

    data = {
        "Date": dates,
        "Symbol": symbols,
        "CurrentPrice": np.random.uniform(100, 200, 100),
        "Normalized_20": np.random.uniform(0, 1, 100),
        "Normalized_200": np.random.uniform(0, 1, 100),
        "PredReturn_20exp": np.random.uniform(0.8, 1.2, 100),
        "PredReturn_200exp": np.random.uniform(0.8, 1.2, 100),
    }

    return pd.DataFrame(data)


def test_random_forest_model_initialization():
    """Test RandomForestTradingModel initialization."""
    model = RandomForestTradingModel(n_estimators=50, max_depth=10)

    assert model.n_estimators == 50
    assert model.max_depth == 10
    assert not model.is_trained
    assert model.model is None


def test_create_labels(sample_metrics_data):
    """Test label creation from price data."""
    model = RandomForestTradingModel()
    labeled_data = model.create_labels(sample_metrics_data, forward_days=5)

    # Should have signal column
    assert "signal" in labeled_data.columns

    # Should have fewer rows due to forward looking
    assert len(labeled_data) < len(sample_metrics_data)

    # Signals should be 0, 1, or 2
    assert labeled_data["signal"].isin([0, 1, 2]).all()


def test_model_training(sample_metrics_data):
    """Test model training pipeline."""
    model = RandomForestTradingModel(n_estimators=10, random_state=42)

    # Create labels
    labeled_data = model.create_labels(sample_metrics_data)

    # Train model
    model.train(labeled_data)

    assert model.is_trained
    assert model.model is not None
    assert model.scaler is not None


def test_model_prediction(sample_metrics_data):
    """Test model prediction."""
    model = RandomForestTradingModel(n_estimators=10, random_state=42)

    # Create labels and train
    labeled_data = model.create_labels(sample_metrics_data)
    model.train(labeled_data)

    # Make predictions
    predictions = model.predict(sample_metrics_data)

    assert len(predictions) == len(sample_metrics_data)
    assert all(pred in [0, 1, 2] for pred in predictions)


def test_model_evaluation(sample_metrics_data):
    """Test model evaluation."""
    model = RandomForestTradingModel(n_estimators=10, random_state=42)

    # Create labels and train
    labeled_data = model.create_labels(sample_metrics_data)
    model.train(labeled_data)

    # Evaluate
    results = model.evaluate(labeled_data)

    assert "accuracy" in results
    assert isinstance(results["accuracy"], (int, float))
    assert 0 <= results["accuracy"] <= 1


def test_feature_importance(sample_metrics_data):
    """Test feature importance extraction."""
    model = RandomForestTradingModel(n_estimators=10, random_state=42)

    # Create labels and train
    labeled_data = model.create_labels(sample_metrics_data)
    model.train(labeled_data)

    # Get importance
    importance = model.get_feature_importance()

    assert isinstance(importance, dict)
    assert len(importance) > 0
    assert all(isinstance(v, (int, float)) for v in importance.values())


def test_untrained_model_errors(sample_metrics_data):
    """Test that untrained model raises appropriate errors."""
    model = RandomForestTradingModel()

    with pytest.raises(ValueError, match="must be trained"):
        model.predict(sample_metrics_data)

    with pytest.raises(ValueError, match="must be trained"):
        model.evaluate(sample_metrics_data)

    with pytest.raises(ValueError, match="must be trained"):
        model.get_feature_importance()
