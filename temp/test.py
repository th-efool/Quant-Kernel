import requests
import requests

url = 'https://api.upstox.com/v3/historical-candle/intraday/NSE_EQ%7CINE848E01016/minutes/5'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer {eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIzR0NYRzIiLCJqdGkiOiI2OTRkNWRkMjZhNjY4YjU1YTdmMWEzMjQiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNQbHVzUGxhbiI6dHJ1ZSwiaWF0IjoxNzY2Njc3OTcwLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3NjY3MDAwMDB9.OfEzQ98hLzM4XJz-exQZba4qbzkPtGAdJX4IoU7Ktqg}'
}

response = requests.get(url, headers=headers)

# Check the response status
if response.status_code == 200:
    # Do something with the response data (e.g., print it)
    print(response.json())
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")
