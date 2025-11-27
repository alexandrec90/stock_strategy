"""Command-line interface for stock strategy analysis."""

import argparse

from src.analysis.metrics import compute_metrics

# Import implementations from subpackages directly
from src.data.fetch_stocks import main as fetch_main

# Trading demo import (optional - only used for the demo trade command)
try:
    from src.trading.ibkr import demo_trade
except Exception:
    demo_trade = None


def main():
    parser = argparse.ArgumentParser(
        description="Stock strategy analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # fetch
    subparsers.add_parser("fetch", help="Fetch stock data from Yahoo Finance")

    # metrics
    subparsers.add_parser("metrics", help="Compute technical metrics")

    # all
    subparsers.add_parser("all", help="Run fetch then metrics")

    # trade-demo
    trade_parser = subparsers.add_parser(
        "trade-demo", help="Run a trading demo (dry-run by default)"
    )
    trade_parser.add_argument("--symbol", "-s", default="AAPL", help="Ticker symbol to trade")
    trade_parser.add_argument("--qty", "-q", type=float, default=1.0, help="Quantity to trade")
    trade_parser.add_argument(
        "--order-type", choices=["market", "limit"], default="market", help="Order type"
    )
    trade_parser.add_argument(
        "--limit", type=float, default=None, help="Limit price (required for limit orders)"
    )
    trade_parser.add_argument(
        "--live",
        action="store_true",
        help="If provided, attempt to send a live order (requires --confirm)",
    )
    trade_parser.add_argument(
        "--confirm", action="store_true", help="Confirmation flag required to send live orders"
    )

    args = parser.parse_args()

    if args.command == "fetch":
        print("Fetching stock data...")
        fetch_main()
    elif args.command == "metrics":
        print("Computing metrics...")
        compute_metrics()
    elif args.command == "all":
        print("Running full pipeline...")
        print("\n1. Fetching stock data...")
        fetch_main()
        print("\n2. Computing metrics...")
        compute_metrics()
        print("\nPipeline complete!")
    elif args.command == "trade-demo":
        if demo_trade is None:
            print(
                "Trading demo is not available. Ensure src/trading/ibkr.py is present and dependencies are installed."
            )
            return

        # Safety: require explicit confirm to send live orders
        if args.live and not args.confirm:
            print(
                "To send a live order you must pass --live --confirm. By default this runs as a dry-run."
            )
            return

        is_dry = not args.live
        print(
            f"Running trading demo: symbol={args.symbol} qty={args.qty} order_type={args.order_type} dry_run={is_dry}"
        )

        # If limit order, ensure limit provided
        if args.order_type == "limit" and args.limit is None:
            print("Limit order requested but --limit was not provided.")
            return

        demo_trade(
            args.symbol,
            args.qty,
            dry_run=is_dry,
            order_type=args.order_type,
            limit_price=args.limit,
        )


if __name__ == "__main__":
    main()
