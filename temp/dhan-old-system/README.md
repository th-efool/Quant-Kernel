# Stock Signal Screener

GOAT Stock Screener is a Python-based project designed to analyze stocks using technical indicators and automated trading strategies. It leverages data from multiple sources, including [yfinance](https://pypi.org/project/yfinance/) for historical data and the Dhan HQ API for intraday data. With a modular structure, the project makes it easy to extend or customize strategies and indicators.

## Features

- **Multiple Technical Strategies**: Implementation of Moving Average Crossover and McGinley Dynamic indicator strategies.
- **Dual Market Data Sources**: Support for Yahoo Finance (global markets) and Dhan brokerage API (Indian markets).
- **Flexible Trading Timeframes**: Configure for daily or intraday (minute-based) analysis.
- **Customizable Parameters**: Adjust indicator periods and calculation frequencies.
- **Clear Signal Generation**: Distinct buy and sell signal identification.
- **Modular Architecture**:Clear separation of functions, indicators, and strategy scripts for easy maintenance and expansion.

## Project Structure

```
goat/
├── Good_Functions.py        # Data fetching (yfinance & Dhan HQ API) and backtesting functions.
├── Indicators.py            # Calculation of technical indicators (e.g., McGinley indicator).
├── Initialization.py        # Configuration and initialization (ticker arrays for different data sources).
└── __init__.py

├── MA Cross Buy.py          # Strategy for moving average crossover buy signals.
├── MA Cross Sell.py         # Strategy for moving average crossover sell signals.
├── McG Buy.py               # Strategy for McGinley-based buy signals.
├── McG Sell.py              # Strategy for McGinley-based sell signals.
├── Template.py              # Template for developing new strategies.
└── __init__.py
```

## Getting Started

### Configuration

- **Dhan HQ API Credentials:**\
  In `Good_Functions.py`, replace the placeholder values for `client_id` and `access_token` with your own credentials.

- **Ticker Initialization:**\
  Update the ticker arrays in `Initialization.py` to match your preferred list of stocks for both yfinance and Dhan HQ.

### Customizing Strategies

You can modify the following parameters in each strategy file:
- `day_trading`: Set to `True` for intraday analysis, `False` for daily analysis
- `frequency`: Adjusts the time interval multiplication factor
- `short`/`long`/`period`: Strategy-specific indicator periods

### Creating New Strategies

1. Use `Template.py` as a starting point
2. Implement your indicator calculations in the designated section
3. Define your strategy logic for buying and selling.
4. Run and test your new strategy

## Usage

- **Running a Strategy:**

  For example, to run the McGinley Sell strategy, execute:

  ```bash
  python "McG Sell.py"
  ```

  This script will:

  - Fetch stock data (using yfinance or the Dhan HQ API based on your settings).
  - Calculate the McGinley indicator.
  - Generate and print sell signals by comparing stock highs with the indicator.

- **Developing Custom Strategies:**

  Use `Template.py` as a starting point for your own strategy implementations. Add or modify indicator functions in `Indicators.py` as needed.

- **Backtesting:**

  The `backtest` function in `Good_Functions.py` can be used to evaluate the performance of your strategies over historical data.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a branch for your feature or bug fix.
3. Commit your changes and submit a pull request.
4. Ensure your code follows the project’s style guidelines and includes documentation where necessary.

### Installation
### Prerequisites
- Python 3.7 or higher
- Required Python libraries:
  - pandas
  - numpy
  - yfinance
  - dhanhq

Install dependencies using pip:

```bash
pip install pandas numpy yfinance dhanhq
```
1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/goat-stock-screener.git
   cd goat-stock-screener
   ```

2. **(Optional) Create and activate a virtual environment:**

   ```bash
   python -m venv env
   source env/bin/activate  # For Windows: env\Scripts\activate
   ```


## Disclaimer

This project is provided for educational and informational purposes only. Use it at your own risk. The author is not responsible for any financial losses incurred through its use.

