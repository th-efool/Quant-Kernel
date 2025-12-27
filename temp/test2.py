import requests

ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIzR0NYRzIiLCJqdGkiOiI2OTRkNWRkMjZhNjY4YjU1YTdmMWEzMjQiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNQbHVzUGxhbiI6dHJ1ZSwiaWF0IjoxNzY2Njc3OTcwLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3NjY3MDAwMDB9.OfEzQ98hLzM4XJz-exQZba4qbzkPtGAdJX4IoU7Ktqg"

url = "https://api.upstox.com/v3/historical-candle/NSE_EQ|INE918Z01012/day/2025-12-25/2024-01-01"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

r = requests.get(url, headers=headers)
print(r.status_code)
print(r.text)
