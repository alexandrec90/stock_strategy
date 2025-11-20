import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from config import LOOKBACK_DAYS, SYMBOLS_CSV, DATA_DIR, STOCK_PRICES_CSV

def main():
    # Read symbols from CSV
    symbols = pd.read_csv(SYMBOLS_CSV)['Symbol'].dropna().astype(str).str.strip().tolist()

    # Calculate the date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=LOOKBACK_DAYS)

    # Create an empty DataFrame to store all data
    all_data = pd.DataFrame()

    # Fetch data for each symbol
    for symbol in symbols:
        # Download the data
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start_date, end=end_date)
        
        # Add symbol column
        data['Symbol'] = symbol
        
        # Append to main DataFrame
        all_data = pd.concat([all_data, data])

    # Reset index to make Date a column
    all_data = all_data.reset_index()

    # Save to CSV
    output_file = os.path.join(DATA_DIR, STOCK_PRICES_CSV)
    all_data.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
    print(f"Total records: {len(all_data)}")

if __name__ == '__main__':
    main()