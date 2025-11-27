"""
Module: src.models.trading_model
Purpose: Machine learning models for predicting buy/sell signals from stock metrics.
Dependencies: scikit-learn, pandas, numpy
Output: Trained classifiers for trading decisions

Key Concepts:
- Label creation: Buy/Sell/Hold based on future price movements
- Feature engineering: Use technical metrics as predictors
- Model evaluation: Classification metrics and backtesting
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class TradingModel(ABC):
    """Abstract base class for trading models that predict buy/sell signals.

    This class defines the interface for training and using ML models
    to generate trading signals from technical indicators.
    """

    @abstractmethod
    def train(self, data: pd.DataFrame, **kwargs) -> None:
        """Train the model on historical data.

        Args:
            data: DataFrame with features and target labels
            **kwargs: Additional training parameters
        """
        pass

    @abstractmethod
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Generate predictions for new data.

        Args:
            data: DataFrame with features (no target column)

        Returns:
            Array of predictions (0=Hold, 1=Buy, 2=Sell)
        """
        pass

    @abstractmethod
    def evaluate(self, data: pd.DataFrame) -> Dict[str, Union[float, str]]:
        """Evaluate model performance on test data.

        Args:
            data: DataFrame with features and true labels

        Returns:
            Dictionary with evaluation metrics
        """
        pass


class RandomForestTradingModel(TradingModel):
    """Random Forest classifier for trading signal prediction.

    Uses technical indicators to predict buy/sell/hold signals based on
    future price movements. Designed for time series data with proper
    temporal splitting to avoid lookahead bias.
    """

    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: Optional[int] = None,
        random_state: int = 42,
        feature_cols: Optional[List[str]] = None,
        target_col: str = "signal",
    ):
        """Initialize Random Forest trading model.

        Args:
            n_estimators: Number of trees in the forest
            max_depth: Maximum depth of trees (None for unlimited)
            random_state: Random seed for reproducibility
            feature_cols: List of column names to use as features
            target_col: Name of target column (0=Hold, 1=Buy, 2=Sell)
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.feature_cols = feature_cols
        self.target_col = target_col

        self.model: Optional[RandomForestClassifier] = None
        self.scaler: Optional[StandardScaler] = None
        self.is_trained = False

        logger.info(
            f"Initialized RandomForestTradingModel with {n_estimators} estimators, "
            f"max_depth={max_depth}"
        )

    def create_labels(
        self,
        data: pd.DataFrame,
        price_col: str = "CurrentPrice",
        forward_days: int = 5,
        buy_threshold: float = 0.02,
        sell_threshold: float = -0.02,
    ) -> pd.DataFrame:
        """Create buy/sell/hold labels based on future price movements.

        Args:
            data: DataFrame with price data
            price_col: Column name for current price
            forward_days: Days to look ahead for price movement
            buy_threshold: Minimum % increase for Buy signal
            sell_threshold: Maximum % decrease for Sell signal

        Returns:
            DataFrame with added 'signal' column (0=Hold, 1=Buy, 2=Sell)
        """
        df = data.copy().sort_values(["Symbol", "Date"])

        # Calculate future price after forward_days
        df["future_price"] = df.groupby("Symbol")[price_col].shift(-forward_days)

        # Calculate return
        df["future_return"] = (df["future_price"] - df[price_col]) / df[price_col]

        # Create signals
        conditions = [
            (df["future_return"] > buy_threshold),  # Buy
            (df["future_return"] < sell_threshold),  # Sell
        ]
        choices = [1, 2]  # 1=Buy, 2=Sell
        df[self.target_col] = np.select(conditions, choices, default=0)  # 0=Hold

        # Remove rows where future_price is NaN (insufficient future data)
        df = df.dropna(subset=["future_price"])

        logger.info(
            f"Created labels: {len(df)} samples, "
            f"Buy: {(df[self.target_col] == 1).sum()}, "
            f"Sell: {(df[self.target_col] == 2).sum()}, "
            f"Hold: {(df[self.target_col] == 0).sum()}"
        )

        return df

    def prepare_features(
        self, data: pd.DataFrame, has_target: bool = True
    ) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        """Prepare features and target for training.

        Args:
            data: DataFrame with features and optionally target column
            has_target: Whether the data includes the target column

        Returns:
            Tuple of (features DataFrame, target Series or None)
        """
        if self.feature_cols is None:
            # Use all numeric columns except target and metadata
            exclude_cols = [self.target_col, "Date", "Symbol", "future_price", "future_return"]
            if not has_target:
                exclude_cols = ["Date", "Symbol", "future_price", "future_return"]
            self.feature_cols = [
                col
                for col in data.select_dtypes(include=[np.number]).columns
                if col not in exclude_cols
            ]

        X = data[self.feature_cols].copy()

        if has_target:
            y = data[self.target_col]
        else:
            y = None

        # Handle any remaining NaN values
        X = X.fillna(X.mean())

        logger.info(f"Prepared features: {X.shape[1]} features, {len(X)} samples")

        return X, y

    def train(
        self, data: pd.DataFrame, tune_hyperparams: bool = False, cv_folds: int = 5, **kwargs
    ) -> None:
        """Train the Random Forest model.

        Args:
            data: DataFrame with features and target labels
            tune_hyperparams: Whether to perform hyperparameter tuning
            cv_folds: Number of cross-validation folds
            **kwargs: Additional parameters for training
        """
        # Prepare data
        X, y = self.prepare_features(data, has_target=True)
        assert y is not None, "Target column required for training"

        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        if tune_hyperparams:
            # Hyperparameter tuning with time series cross-validation
            param_grid = {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
            }

            tscv = TimeSeriesSplit(n_splits=cv_folds)
            grid_search = GridSearchCV(
                RandomForestClassifier(random_state=self.random_state),
                param_grid,
                cv=tscv,
                scoring="f1_macro",
                n_jobs=-1,
            )

            logger.info("Starting hyperparameter tuning...")
            grid_search.fit(X_scaled, y)

            self.model = grid_search.best_estimator_
            logger.info(f"Best parameters: {grid_search.best_params_}")
        else:
            # Simple training
            self.model = RandomForestClassifier(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                random_state=self.random_state,
                **kwargs,
            )
            self.model.fit(X_scaled, y)

        self.is_trained = True
        logger.info("Model training completed")

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Generate predictions for new data.

        Args:
            data: DataFrame with features (no target column)

        Returns:
            Array of predictions (0=Hold, 1=Buy, 2=Sell)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")

        X, _ = self.prepare_features(data, has_target=False)
        assert self.scaler is not None, "Scaler not initialized"
        assert self.model is not None, "Model not trained"

        X_scaled = self.scaler.transform(X)

        predictions = self.model.predict(X_scaled)
        return predictions

    def predict_proba(self, data: pd.DataFrame) -> np.ndarray:
        """Generate prediction probabilities for new data.

        Args:
            data: DataFrame with features

        Returns:
            Array of prediction probabilities for each class
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")

        X, _ = self.prepare_features(data, has_target=False)
        assert self.scaler is not None, "Scaler not initialized"
        assert self.model is not None, "Model not trained"

        X_scaled = self.scaler.transform(X)

        probabilities = self.model.predict_proba(X_scaled)
        return probabilities

    def evaluate(self, data: pd.DataFrame) -> Dict[str, Union[float, str]]:
        """Evaluate model performance on test data.

        Args:
            data: DataFrame with features and true labels

        Returns:
            Dictionary with evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")

        X, y_true = self.prepare_features(data, has_target=True)
        assert y_true is not None, "Target column required for evaluation"
        assert self.scaler is not None, "Scaler not initialized"
        assert self.model is not None, "Model not trained"

        X_scaled = self.scaler.transform(X)

        y_pred = self.model.predict(X_scaled)

        # Generate classification report
        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        assert isinstance(report, dict), "Report should be a dictionary"

        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)

        results = {
            "accuracy": report.get("accuracy", 0.0),
            "precision_hold": report.get("0", {}).get("precision", 0.0),
            "precision_buy": report.get("1", {}).get("precision", 0.0),
            "precision_sell": report.get("2", {}).get("precision", 0.0),
            "recall_hold": report.get("0", {}).get("recall", 0.0),
            "recall_buy": report.get("1", {}).get("recall", 0.0),
            "recall_sell": report.get("2", {}).get("recall", 0.0),
            "f1_hold": report.get("0", {}).get("f1-score", 0.0),
            "f1_buy": report.get("1", {}).get("f1-score", 0.0),
            "f1_sell": report.get("2", {}).get("f1-score", 0.0),
            "confusion_matrix": cm.tolist(),
        }

        logger.info(f"Model evaluation - Accuracy: {results['accuracy']:.3f}")
        return results

    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores from the trained model.

        Returns:
            Dictionary mapping feature names to importance scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained to get feature importance")

        assert self.model is not None, "Model not trained"
        assert self.feature_cols is not None, "Features not prepared"

        importance_scores = self.model.feature_importances_
        return dict(zip(self.feature_cols, importance_scores))
