import sys
import types
import builtins
import pytest


def make_fake_ib_insync():
    """Create a fake ib_insync module with minimal behavior for testing."""
    mod = types.SimpleNamespace()

    class IB:
        def __init__(self):
            self.connected = False

        def connect(self, host, port, clientId=None):
            self.connected = True
            return True

        def qualifyContracts(self, contract):
            # pretend to qualify
            return [contract]

        def placeOrder(self, contract, order):
            return {"contract": contract, "order": order}

        def sleep(self, t):
            pass

        def disconnect(self):
            self.connected = False

    class Stock:
        def __init__(self, symbol, exchange, currency):
            self.symbol = symbol

    class MarketOrder:
        def __init__(self, action, quantity, account=None):
            self.action = action
            self.quantity = quantity
            self.account = account

    class LimitOrder:
        def __init__(self, action, quantity, limit_price, account=None):
            self.action = action
            self.quantity = quantity
            self.limit_price = limit_price
            self.account = account

    mod.IB = IB
    mod.Stock = Stock
    mod.MarketOrder = MarketOrder
    mod.LimitOrder = LimitOrder
    return mod


def test_demo_dry_run(capsys):
    # Import the demo function
    from src.trading.ibkr import demo_trade

    res = demo_trade('AAPL', 1, dry_run=True)
    captured = capsys.readouterr()
    assert res is None
    assert 'DRY-RUN' in captured.out


def test_demo_live_calls_ib(monkeypatch):
    fake = make_fake_ib_insync()
    monkeypatch.setitem(sys.modules, 'ib_insync', fake)

    # Now import the module under test (it will import ib_insync from sys.modules)
    from src.trading import ibkr

    # Call demo_trade with dry_run=False which should use the fake IB
    trade = ibkr.demo_trade('AAPL', 2, dry_run=False, order_type='market')
    # Expect a trade-like dict from fake placeOrder
    assert isinstance(trade, dict)
    assert trade['order'].quantity == 2
