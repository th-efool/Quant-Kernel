import goat
from goat import *
start_date = '2024-01-21'
end_date = (datetime.now() + timedelta(days=1))

day_trading=False
if day_trading:
    frequency = 5 # Number of minute/day BASIS
    goat_tickers = goat.symbol_security_pairs
else:
    goat_tickers = goat.tickers
    frequency = 1

short=7*frequency
long=21*frequency
sma_short="Sma"+str(short/frequency)
sma_long="Sma"+str(long/frequency)


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

    if 'Adj Close' not in df.columns:
        df['Adj Close'] = df['Close']
    # Calculate Indicators/Markers for Our Strategy
    df[sma_short] = df['Adj Close'].rolling(window=short).mean()
    df[sma_long] = df['Adj Close'].rolling(window=long).mean()
    # Additional Buying Or Selling Conditions Set
    latest_row = df.iloc[-1]  # Get the latest row
    if not df.empty:
        latest_row = df.iloc[-1]  # Safely fetch the last row
        Short_Strong = (latest_row[sma_short].item()>latest_row[sma_long].item())  # Extract scalar
        previous_row = df.iloc[-2]
        Previous_Short_Strong = (previous_row[sma_short].item()>previous_row[sma_long].item())
        close_above = latest_row['Adj Close'].item() > latest_row[sma_short].item()
        if (Short_Strong and Previous_Short_Strong==0 and close_above):
            if day_trading:
                print(f"Buy signal for {ticker[0]}:")
                print(latest_row[['Adj Close', 'High', sma_short, sma_long]])
            elif not day_trading:
                print(f"Buy signal for {ticker}:")
                print(latest_row[['Date', 'Adj Close', 'High', sma_short, sma_long]])
