

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

short=9*frequency
long=26*frequency
sma_short="Sma"+str(short)
sma_long="Sma"+str(long)



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
    # Implementing Strategy on Dataset
    df['HIGH']=df['High']
    df['What to do?'] = np.where(df['HIGH'] < df[sma_short], 1, 0)  # 1 = BUY, 0 = SELL
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

