"""
Module: src.models
Purpose: Machine learning models for trading strategy development.
Dependencies: scikit-learn, pandas, numpy
Output: Trained models for buy/sell signal prediction

Key Concepts:
- TradingModel: Abstract base class for ML trading models
- RandomForestTradingModel: Random Forest implementation for classification
- Model training and evaluation utilities
"""

from .trading_model import RandomForestTradingModel, TradingModel

__all__ = ["TradingModel", "RandomForestTradingModel"]
