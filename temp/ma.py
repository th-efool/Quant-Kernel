import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# ======================
# CONFIG
# ======================
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIzR0NYRzIiLCJqdGkiOiI2OTRkNWRkMjZhNjY4YjU1YTdmMWEzMjQiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNQbHVzUGxhbiI6dHJ1ZSwiaWF0IjoxNzY2Njc3OTcwLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3NjY3MDAwMDB9.OfEzQ98hLzM4XJz-exQZba4qbzkPtGAdJX4IoU7Ktqg"
INSTRUMENT_KEY = "NSE_EQ|INE918Z01012"

FROM_DATE = "2024-01-01"
TO_DATE = date.today().strftime("%Y-%m-%d")

url = f"https://api.upstox.com/v3/historical-candle/{INSTRUMENT_KEY}/day/{FROM_DATE}/{TO_DATE}"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}


# ======================
# FETCH DATA
# ======================
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("API Error:", response.text)
    exit()

candles = response.json()["data"]["candles"]

# ✅ 7 columns (important)
df = pd.DataFrame(
    candles,
    columns=["date", "open", "high", "low", "close", "volume", "oi"]
)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# ======================
# MA CALCULATION
# ======================
df["MA7"] = df["close"].rolling(7).mean()
df["MA21"] = df["close"].rolling(21).mean()

# ======================
# CROSSOVER LOGIC
# ======================
df["Signal"] = 0
df.loc[(df["MA7"] > df["MA21"]) & (df["MA7"].shift(1) <= df["MA21"].shift(1)), "Signal"] = 1
df.loc[(df["MA7"] < df["MA21"]) & (df["MA7"].shift(1) >= df["MA21"].shift(1)), "Signal"] = -1

# ======================
# PLOT
# ======================
plt.figure(figsize=(14, 7))

plt.plot(df["date"], df["close"], label="Close")
plt.plot(df["date"], df["MA7"], label="MA 7")
plt.plot(df["date"], df["MA21"], label="MA 21")

plt.scatter(df[df["Signal"] == 1]["date"], df[df["Signal"] == 1]["close"], marker="^", s=100)
plt.scatter(df[df["Signal"] == -1]["date"], df[df["Signal"] == -1]["close"], marker="v", s=100)

plt.title("MA(7,21) Crossover – NSE_EQ|INE918Z01012")
plt.legend()
plt.grid(True)
plt.show()
