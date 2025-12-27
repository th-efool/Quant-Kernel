# Quant Kernel
An GUI python-based, algo trading & indicator signal scanning & capturing application

# Quant-Kernel

**Quant-Kernel** is a modular Python-based market data acquisition framework designed for quantitative trading and research. It provides a unified interface to fetch historical and intraday market data from multiple Indian stock market APIs, including **Upstox**, **Dhan**, and **Yahoo Finance**.

The project is structured to allow seamless switching between different data providers while maintaining a consistent data format (Pandas DataFrames or Typed Candles).

---

## 🏗️ Project Architecture

The system follows a provider-consumer pattern where specific API fetchers inherit from a base class to ensure a standard contract.

### Key Components:

* **`QKHistoricalData` (DataManager)**: The high-level entry point. It manages API switching and coordinates between ticker management and data fetching.
* **`DataFetcherBase`**: An abstract base class defining the required methods (`_fetch_historical`, `_fetch_intraday`) for any new data provider.
* **`TickerManager`**: Handles the loading and filtering of security symbols/IDs from local configurations (`india.yaml`).
* **`CommonTypes`**: Enforces type safety using Python Enums and Data Classes for candles, dates, and units.

---

## 🚀 Features

* **Unified API**: Fetch data from different brokers using the same method calls.
* **Multi-Provider Support**:
* **Upstox**: Supports historical and intraday via REST API.
* **Dhan**: Supports daily historical and minute-based intraday data.
* **Yahoo Finance**: General market data.


* **Normalization**: Automatically converts varying API response formats (JSON, column-wise arrays, etc.) into normalized `QKCandle` objects and Pandas DataFrames.
* **Ticker Mapping**: Managed via YAML to handle the differences in symbol naming conventions across providers.

---

## 📂 Project Structure

```text
quant-kernel/
├── core/
│   ├── CommonTypes.py      # Enums (Unit, QKApi) and Data Classes (QKCandle)
│   ├── env.py              # Environment variable loader
│   └── SecretKeys.env      # API credentials (git-ignored)
├── data/
│   ├── APIs/
│   │   ├── historical_data/
│   │   │   ├── data_fetcher_base.py  # Abstract Base Class
│   │   │   ├── dhan_fetcher.py       # Dhan Implementation
│   │   │   └── upstox_fetcher.py     # Upstox Implementation
│   │   └── ticker_symbols/
│   │       ├── loader.py             # YAML loader for symbols
│   │       ├── ticker_manager.py     # Symbol management logic
│   │       └── india.yaml            # Symbol & Security ID database
│   └── data_manager.py     # Main Public API
└── requirements.txt

```

---

## 🛠️ Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/quant-kernel.git
cd quant-kernel

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Configure Environment Variables:**
Create a `core/SecretKeys.env` file and add your API credentials:
```env
DHAN_CLIENT_ID=your_id
DHAN_SECRET_KEY=your_token
UPSTOX_ACCESS_TOKEN=your_token

```



---

## 💻 Usage

### Basic Data Fetching

```python
from data.data_manager import QKHistoricalData
from core.CommonTypes import QKApi

# Initialize with Upstox
qk = QKHistoricalData(api=QKApi.upstox)

# Get top tickers from the manager
tickers = qk.tickers.first(5)

# Fetch historical data
data = qk.getHistoricalData(tickers)

```

### Switching APIs on the fly

```python
# Switch from Upstox to Dhan
qk.switch_api(QKApi.dhan)

# Fetch intraday data using Dhan
intraday_data = qk.getIntradayData(tickers)

```

---

