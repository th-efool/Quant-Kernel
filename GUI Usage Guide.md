# Quant Kernel GUI — Usage Guide

This GUI is a **configuration-driven market scanner and renderer**.
You **declare** what to fetch, **compose** indicators & strategies, and the system **executes + renders incrementally**.

The UI is divided into **four logical regions**:

```
[ API Selection ]   [ Fetch Config ]   [ Run ]
[ Indicators ]      [ Strategies ]     [ Charts ]
```
![Quant Kernel Screenshot](https://raw.githubusercontent.com/th-efool/Quant-Kernel/main/docs/screenshot20251229195242.png)

---

## 1. API Selection Panel

This section defines **where tickers come from** and **how many are processed**.

### Fields

| Field           | Meaning                                      |
| --------------- | -------------------------------------------- |
| `api (QKApi)`   | Data provider (`yfinance`, `upstox`, `dhan`) |
| `exchange`      | Exchange namespace (e.g. `NSE`)              |
| `start_index`   | Starting index into ticker list              |
| `end_index`     | Ending index (exclusive)                     |
| `enable_filter` | Enable signal-based filtering                |
| `filter_last_n` | Lookback window (last N candles)             |

### How ticker ranges work

Tickers are loaded from your YAML source **once**, then sliced:

```text
tickers[start_index : end_index]
```

Examples:

* `0 → 10` → first 10 tickers
* `10 → 20` → next batch
* Enables **batch scanning without restarting the app**

---

### Signal Filter (Optional)

When `enable_filter` is checked:

* For each ticker:

  * Look at **last N candles**
  * If **any strategy emits BUY or SELL** → chart is rendered
  * If **only HOLD or no signals** → ticker is skipped

This:

* avoids rendering noise
* conserves memory
* scales to large ticker sets

---

## 2. Fetch Config Panel

Controls **how market data is fetched**.

### Fields

| Field               | Meaning                          |
| ------------------- | -------------------------------- |
| `mode`              | `historical` or `intraday`       |
| `interval`          | Candle interval (days / minutes) |
| `intraday_interval` | Required only for intraday       |
| `from_date`         | Start date (YYYY-MM-DD)          |
| `to_date`           | End date                         |
| `unit`              | Time unit (`days`, etc.)         |

### Notes

* Dates are **validated but not auto-corrected**
* Changing fetch config **invalidates all downstream computation**
* GUI does not cache results — every run is explicit

---

## 3. Indicators Panel

Indicators are **pure feature generators**.

### How to use

1. Select an indicator from **Indicator Config**
2. Fill in parameters
3. Click **Add**
4. Repeat to add multiple indicators

### Key behavior

* Multiple instances allowed
* Same indicator + same params → deduplicated internally
* Indicators **do not generate signals**
* Indicators are computed **once per run**

---

## 4. Strategies Panel

Strategies convert indicators → signals.

### How to use

1. Select a strategy
2. Configure parameters
3. Click **Add**
4. Multiple strategies can coexist

### Behavior

* Each strategy instance gets a unique signal column
* BUY / SELL / HOLD values are written into the DataFrame
* Strategies **declare which indicators they need**
* Strategy execution happens **after all indicators**

---

## 5. Run Pipeline Button

When you press **RUN PIPELINE**:

### Execution flow

```
UI State
  ↓
Ticker Resolution (range-based)
  ↓
For each ticker:
  → Fetch Data
  → Run Indicators
  → Run Strategies
  → Apply Signal Filter (optional)
  → Append Chart
```

### Important details

* Execution runs in a **background thread**
* UI remains responsive
* Charts appear **incrementally**
* Failed tickers do not block others

---

## 6. Market Charts View (Right Panel)

This is a **scrollable multi-chart renderer**.

### Behavior

* One ticker → one chart → one Matplotlib figure
* Charts are stacked vertically
* Scrollbar appears automatically
* No shared axes between tickers

### What is rendered

* Candlesticks (OHLC)
* Indicator overlays (MA, VWAP, etc.)
* Strategy signals:

  * ▲ BUY
  * ▼ SELL
* Secondary Y-axis for percentage-based indicators

### Clearing behavior

* Each run **clears previous charts**
* Charts are destroyed, not hidden
* Prevents figure leaks and memory growth

---

## 7. Typical Usage Patterns

### Scan in batches

```
Run 1: start=0, end=25
Run 2: start=25, end=50
Run 3: start=50, end=75
```

### Signal-only scan

* Enable filter
* Set `filter_last_n = 3`
* Render only actionable tickers

### Strategy comparison

* Add multiple strategies
* Compare signals visually per ticker

---

## What the GUI Does NOT Do

* ❌ No automatic trading
* ❌ No hidden state
* ❌ No auto-refresh
* ❌ No implicit caching

Every run is **explicit and reproducible**.

---

## Mental Model (Important)

* **UI = configuration**
* **Controller = orchestration**
* **DataFrame = truth**
* **Renderer = visualization only**

Once you understand that, everything else clicks.

