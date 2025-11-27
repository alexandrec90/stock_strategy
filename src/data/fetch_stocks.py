import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.core.config import DATA_DIR, LOOKBACK_DAYS, STOCK_PRICES_CSV, SYMBOLS_CSV

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    # Validate symbols file exists
    if not Path(SYMBOLS_CSV).exists():
        logger.error(f"Symbols file not found: {SYMBOLS_CSV}")
        raise FileNotFoundError(f"Please create {SYMBOLS_CSV} with stock symbols")

    # Read and validate symbols from CSV
    try:
        df = pd.read_csv(SYMBOLS_CSV)
        if "Symbol" not in df.columns:
            raise ValueError("symbols.csv must have a 'Symbol' column")
        symbols = df["Symbol"].dropna().astype(str).str.strip().tolist()
        if not symbols:
            raise ValueError("No symbols found in symbols.csv")
        logger.info(f"Loading data for {len(symbols)} symbols: {', '.join(symbols)}")
    except Exception as e:
        logger.error(f"Error reading symbols file: {e}")
        raise

    # Calculate the date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=LOOKBACK_DAYS)

    # Create an empty DataFrame to store all data
    all_data = pd.DataFrame()

    # Ensure data directory exists
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    # Fetch data for each symbol
    for symbol in symbols:
        try:
            logger.info(f"Fetching data for {symbol}...")
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)

            if data.empty:
                logger.warning(f"No data returned for {symbol}")
                continue

            # Add symbol column
            data["Symbol"] = symbol

            # Append to main DataFrame
            all_data = pd.concat([all_data, data])
            logger.info(f"Retrieved {len(data)} records for {symbol}")
        except Exception as e:
            logger.error(f"Failed to fetch data for {symbol}: {e}")
            continue

    # Reset index to make Date a column
    all_data = all_data.reset_index()

    # Validate we have data before saving
    if all_data.empty:
        logger.error("No data was fetched for any symbols")
        raise ValueError("No data retrieved. Check symbols and network connection.")

    # Save to CSV
    output_file = os.path.join(DATA_DIR, STOCK_PRICES_CSV)
    all_data.to_csv(output_file, index=False)
    logger.info(f"Data saved to {output_file}")
    logger.info(f"Total records: {len(all_data)}")


if __name__ == "__main__":
    main()
