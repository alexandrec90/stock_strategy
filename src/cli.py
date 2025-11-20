"""Command-line interface for stock strategy analysis."""
import argparse
import sys
from pathlib import Path

# Add src to path if running as script
sys.path.insert(0, str(Path(__file__).parent))

from fetch_stocks import main as fetch_main
from metrics import compute_metrics


def main():
    parser = argparse.ArgumentParser(
        description="Stock strategy analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s fetch          # Fetch stock data from Yahoo Finance
  %(prog)s metrics        # Compute technical metrics
  %(prog)s all            # Run fetch then metrics
        """
    )
    
    parser.add_argument(
        'command',
        choices=['fetch', 'metrics', 'all'],
        help='Command to run'
    )
    
    args = parser.parse_args()
    
    if args.command == 'fetch':
        print("Fetching stock data...")
        fetch_main()
    elif args.command == 'metrics':
        print("Computing metrics...")
        compute_metrics()
    elif args.command == 'all':
        print("Running full pipeline...")
        print("\n1. Fetching stock data...")
        fetch_main()
        print("\n2. Computing metrics...")
        compute_metrics()
        print("\nPipeline complete!")


if __name__ == '__main__':
    main()
