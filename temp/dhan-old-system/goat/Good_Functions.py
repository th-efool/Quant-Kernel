import yfinance as yf
import pandas as pd
def fetch_data(ticker, start_date, end_date):
    data=yf.download(ticker, start=start_date, end=end_date, progress=True)
    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

from dhanhq import dhanhq
from dhanhq import marketfeed
client_id = " "
access_token = " "
dhan = dhanhq(client_id,access_token)

#you can change it for daily data also
def dhan_intraday_minute_data(id_security):
    wanna_convert_date_time =  False
    # Fetch data using dhan API
    data = dhan.intraday_minute_data(
        security_id=id_security,
        exchange_segment='NSE_EQ',
        instrument_type='EQUITY',
        from_date='2024-01-21',
        to_date='2024-01-21'
    )

    # Validate response
    if not data or 'data' not in data:
        print(f"Invalid or empty response for security ID: {id_security}")
        return pd.DataFrame()  # Return an empty DataFrame if response is invalid

    # Ensure 'data' key contains iterable data suitable for DataFrame
    try:
        df = pd.DataFrame(data['data'])
    except Exception as e:
        return pd.DataFrame()  # Return an empty DataFrame on failure

    if wanna_convert_date_time:
        temp_list = []
        for i in df['start_Time']:
            temp = dhan.convert_to_date_time(i)
            temp_list.append(temp)
        df['Date'] = temp_list
    df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low','close': 'Adj Close','volume': 'Volume'}, inplace=True)
    return df


def backtest(df):
    pos = False
    num = 0
    percentchange = []
    for i in df.index:
        if (df['What to do?'].iloc[i]):
            if(pos == False):
                pos = True
                bp = df['Adjusted Close'].iloc[i]
        elif (df['What to do?'].iloc[i]):
            if pos == True:
                percentchange.append(round((df['Adjusted Close'].iloc[i] - bp) / bp * 100, 2))
                pos = False
        num += 1
        if (num == df['Adjusted Close'].count() - 1 and pos == True):
            percentchange.append(round((df['Adjusted Close'].iloc[i] - bp) / bp * 100, 2))
            pos = False
    print(percentchange)

