import goat
from goat import *
start_date = '2024-01-21'
end_date = (datetime.now() + timedelta(days=1))

day_trading=True
if day_trading:
    frequency = 5 # Number of minute/day BASIS
    goat_tickers = goat.symbol_security_pairs
else:
    goat_tickers = goat.tickers
    frequency = 1

short=7*frequency
long=21*frequency


for ticker in goat_tickers:
    if day_trading:
        df = dhan_intraday_minute_data(ticker[1])
    else:
        df = goat.fetch_data(ticker, start_date, end_date)
    if df.empty:
        if day_trading:
            print(f"Data for {ticker[0]} is empty or failed to download. Skipping...")
        elif not day_trading:
            print(f"Data for {ticker} is empty or failed to download. Skipping...")
        continue
   # Calculate Indicators/Markers for Our Strategy


    # Implementing Strategy on Dataset

    # Additional Buying Or Selling Conditions Set
    latest_row = df.iloc[-1]  # Get the latest row
    if not df.empty:
        latest_row = df.iloc[-1]  # Safely fetch the last row
        what_to_do = latest_row['What to do?'].item()  # Extract scalar
        previous_row = df.iloc[-2]
        previous_what_to_do = previous_row['What to do?'].item()
        if (what_to_do == 1 and previous_what_to_do==0):
            if day_trading:
                print(f"Sell signal for {ticker[0]}:")
                print(latest_row[['Adj Close', 'High', 'What to do?']])
            elif not day_trading:
                print(f"Sell signal for {ticker}:")
                print(latest_row[['Date', 'Adj Close', 'High', 'What to do?']])

