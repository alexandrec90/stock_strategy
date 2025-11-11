import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Configuration constants
DAYS = 500  # lookback / how far back to fetch
SYMBOLS_CSV = 'symbols.csv'  # CSV file containing tickers under a 'Symbol' column

# Read symbols from CSV
symbols = pd.read_csv(SYMBOLS_CSV)['Symbol'].dropna().astype(str).str.strip().tolist()

# Calculate the date range
end_date = datetime.now()
start_date = end_date - timedelta(days=DAYS)

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
output_file = 'stock_prices.csv'
all_data.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")
print(f"Total records: {len(all_data)}")