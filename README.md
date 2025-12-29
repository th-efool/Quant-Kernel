# Quant Kernel
An GUI python-based, algo trading & indicator signal scanning & capturing application
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Pandas](https://img.shields.io/badge/pandas-required-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active%20development-yellow.svg)
![Architecture](https://img.shields.io/badge/architecture-modular-informational.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

A **modular quantitative research kernel** focused on **clarity, composability, and correctness**.
![Quant Kernel Screenshot](https://raw.githubusercontent.com/th-efool/Quant-Kernel/main/docs/screenshot20251229195242.png)

#### To run the application:
1. Clone the repository
2. Install the dependencies
3. run app/app.py
**clean execution graph**:
```
Market Data → Indicators → Strategies → Signals → (Renderer / Backtests / Execution)
```
Each layer is isolated, deterministic, and replaceable.

---

## Design Philosophy

* **Separation of concerns**
  Data fetching, indicator computation, strategy logic, and rendering never bleed into each other.
* **Deterministic pipelines**
  Every stage consumes a DataFrame and returns a DataFrame or Series — no hidden state.
* **Configuration through composition, not flags**
  You add indicators and strategies explicitly; duplicates are deduplicated structurally.
* **Mechanics > magic**
  No “black box” frameworks. Everything is inspectable and override-friendly.


---

## High-Level Architecture

```
data/
 ├─ QKHistoricalData        # Data orchestration (API + tickers)
 ├─ fetchers/               # Yahoo / Upstox / Dhan implementations

indicators/
 ├─ IndicatorBase           # Pure feature generators
 ├─ IndicatorManager        # Deduplicates & runs indicators

strategies/
 ├─ StrategyBase            # Signal contracts
 ├─ StrategyManager         # Orchestrates strategies

gui/
 ├─ QKRenderer              # (planned) presentation-only layer

engine.py                   # Glue: data → strategies → renderer
```

---

## Core Concepts

### 1. Data Layer (`QKHistoricalData`)

Handles:

* API selection (`yfinance`, `upstox`, `dhan`)
* Date ranges
* Time units (days, minutes, etc.)
* Ticker resolution

```python
data = QKHistoricalData(api=QKApi.yfinance)
df = data.fetch_historical("RELIANCE")
```

This layer **never** knows about indicators or strategies.

---

### 2. Indicators

Indicators are **pure feature generators**.

Rules:

* Input: full DataFrame
* Output: `dict[str, pd.Series]`
* Series **must align with input index**

```python
class MovingAverage(IndicatorBase):
    def compute(self, df):
        return {
            f"ma_{self.period}": df["close"].rolling(self.period).mean()
        }
```

Indicators do **not** know:

* which strategy uses them
* how they are plotted
* how signals are generated

---

### 3. IndicatorManager

Responsible for:

* Deduplicating indicators by configuration
* Running them exactly once
* Injecting outputs into the DataFrame

```python
manager.add(MovingAverage(21))
manager.add(MovingAverage(21))  # deduped
```

---

### 4. Strategies

Strategies:

* Declare **what indicators they need**
* Convert indicators → signals
* Never compute indicators directly

```python
class MACrossoverStrategy(StrategyBase):
    signal_column = "ma_cross"

    def indicators(self):
        return [MovingAverage(7), MovingAverage(21)]

    def compute(self, df):
        ...
```

Each strategy instance gets a unique `signal_column_id`:

```
ma_cross_1
ma_cross_2
```

This allows **multiple parameterized instances** safely.

---

### 5. StrategyManager

Responsibilities:

* Register strategies
* Collect required indicators
* Execute indicators first
* Execute strategies second

```python
strategy_mgr = StrategyManager()
strategy_mgr.add(MACrossoverStrategy(7, 21))
strategy_mgr.add(DayRangeBreakoutStrategy(0.05))

df = strategy_mgr.run(df)
```

No plotting. No execution. Just signals.

---

## Renderer
Quant-Kernel includes a **modular, component-driven Tkinter renderer** designed to visualize strategy outputs without polluting the execution pipeline.

The GUI layer is **presentation-only**: it never fetches data, computes indicators, or generates signals.

### Key Properties
* **Component-based UI**
  Every visible element (inputs, selectors, charts) is an isolated `UIComponent` with a strict build/value contract.
* **Declarative configuration**
  Indicators, strategies, and fetch parameters are configured via composable UI blocks — no hardcoded forms.
* **Multi-ticker rendering**
  Each ticker renders into its own chart component, stacked vertically inside a scrollable view.
* **Incremental, non-blocking execution**
  Data fetching and strategy execution run in background threads; charts are appended progressively to avoid UI freezes.
* **Strict separation**
  ```
  UI → Controller → Data/Strategies → DataFrame → Renderer
  ```
  The renderer only consumes final DataFrames.

---
### GUI Architecture (Simplified)
```
gui/
 ├─ components/
 │   ├─ base_ui_component.py     # UI contract
 │   ├─ param_input.py           # Typed input forms
 │   ├─ select_and_configure.py  # Class + params selection
 │   ├─ add_to_list.py           # Multi-instance aggregation
 │   ├─ stock_chart.py           # Single-ticker chart
 │   └─ market_chart_view.py     # Scrollable multi-chart container
 │
 ├─ layout/
 │   ├─ row.py / column.py       # Layout composition
 │   └─ panel.py                 # Size-constrained containers
 │
 ├─ views/
 │   └─ main_view.py             # Pure UI composition
 │
 └─ QKRenderer.py                # Tk bootstrap + layout build
```

---

### Renderer Responsibilities
The renderer **does not**:
* decide what to fetch
* decide what to compute
* interpret signals

It **only**:
* lays out UI components
* renders charts from DataFrames
* manages scrolling, redraws, and lifecycle

Each ticker → one chart → one figure
No shared state, no multiplexed axes.

---

### Execution Flow (GUI Mode)
```
User Input
   ↓
Controller.run_pipeline(ticker)
   ↓
DataFrame (OHLC + indicators + signals)
   ↓
MarketChartView.append_data()
   ↓
StockChartComponent.render()
```

Charts are **filtered, skipped, or appended** before rendering when signal filters are enabled, conserving resources.

---

This keeps the GUI **predictable, debuggable, and replaceable**, while remaining lightweight enough to evolve into backtesting, batch scanning, or headless modes later.

This prevents renderer bloat and keeps visuals modular.

---

## engine.py (Execution Glue)

```python
from data.QK_data_manager import QKHistoricalData
from strategies.QK_strategy_manager import StrategyManager
from gui.QKRenderer import QKRenderer

TheDataManager = QKHistoricalData()
TheStrategyManager = StrategyManager()
Renderer = QKRenderer()
```


## Philosophy Summary

> Indicators describe **markets**
> Strategies describe **beliefs**
> Managers describe **execution**
> Renderers describe **perception**

Quant-Kernel keeps those ideas separate — on purpose.


