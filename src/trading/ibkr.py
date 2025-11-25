"""Interactive Brokers (IBKR) trading helpers.

This module provides a small, safe wrapper around ib_insync for placing
paper/dry-run orders. It intentionally avoids executing any trades by
default and requires an explicit call with dry_run=False to place real orders.

Note: ib_insync is an optional dependency. If it's not installed, the demo
functions will still exist but will raise an informative error when executed.
"""
from typing import Optional
import logging

from src.core.config import IBKR_HOST, IBKR_PORT, IBKR_CLIENT_ID, IBKR_ACCOUNT


logger = logging.getLogger(__name__)


def _ensure_ib_insync():
    try:
        from ib_insync import IB, Stock, MarketOrder, LimitOrder

        return IB, Stock, MarketOrder, LimitOrder
    except Exception as exc:  # pragma: no cover - informative
        raise ImportError(
            "ib_insync is required for IBKR trading. Add it to requirements and install it (pip install ib_insync)."
        ) from exc


def connect_ibkr(host: str = IBKR_HOST, port: int = IBKR_PORT, client_id: int = IBKR_CLIENT_ID):
    """Create and return a connected IB() instance.

    Caller is responsible for calling ib.disconnect() when done.
    """
    IB, *_ = _ensure_ib_insync()
    ib = IB()
    logger.info("Connecting to IBKR at %s:%s (clientId=%s)", host, port, client_id)
    connected = ib.connect(host, port, clientId=client_id)
    if not connected:
        raise ConnectionError(f"Failed to connect to IB at {host}:{port} (clientId={client_id})")
    logger.info("Connected to IBKR")
    return ib


def place_market_order(ib, symbol: str, quantity: float, action: str = 'BUY', account: Optional[str] = IBKR_ACCOUNT):
    """Place a simple market order for a US-listed stock.

    Returns the Trade object from ib_insync.
    """
    IB, Stock, MarketOrder, _ = _ensure_ib_insync()
    if quantity <= 0:
        raise ValueError("quantity must be positive")

    contract = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(contract)
    order = MarketOrder(action, quantity, account=account)
    logger.info("Placing %s market order for %s qty=%s on account=%s", action, symbol, quantity, account)
    trade = ib.placeOrder(contract, order)
    return trade


def place_limit_order(ib, symbol: str, quantity: float, limit_price: float, action: str = 'BUY', account: Optional[str] = IBKR_ACCOUNT):
    """Place a simple limit order.
    """
    IB, Stock, _, LimitOrder = _ensure_ib_insync()
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    if limit_price <= 0:
        raise ValueError("limit_price must be positive")

    contract = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(contract)
    order = LimitOrder(action, quantity, limit_price, account=account)
    logger.info("Placing %s limit order for %s qty=%s limit=%s account=%s", action, symbol, quantity, limit_price, account)
    trade = ib.placeOrder(contract, order)
    return trade


def demo_trade(symbol: str, quantity: float, dry_run: bool = True, order_type: str = 'market', limit_price: Optional[float] = None):
    """Demo helper that shows how to place an order.

    By default this performs a dry-run: it will print/log what it would do
    without connecting to IB. To actually send an order set dry_run=False.
    """
    if dry_run:
        logger.info("DRY-RUN: would place %s order: symbol=%s qty=%s limit=%s account=%s", order_type, symbol, quantity, limit_price, IBKR_ACCOUNT)
        print(f"DRY-RUN: would place {order_type} order - symbol={symbol} qty={quantity} limit={limit_price} account={IBKR_ACCOUNT}")
        return None

    # Real execution path
    IB, *_ = _ensure_ib_insync()
    ib = connect_ibkr()
    try:
        if order_type == 'market':
            trade = place_market_order(ib, symbol, quantity)
        elif order_type == 'limit':
            if limit_price is None:
                raise ValueError("limit_price must be provided for limit orders")
            trade = place_limit_order(ib, symbol, quantity, limit_price)
        else:
            raise ValueError(f"Unsupported order_type: {order_type}")

        # Optionally wait briefly for status updates (non-blocking)
        ib.sleep(1)
        logger.info("Trade placed: %s", trade)
        return trade
    finally:
        try:
            ib.disconnect()
        except Exception:
            pass
