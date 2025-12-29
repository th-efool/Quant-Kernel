# Quant Kernel
An GUI python-based, algo trading & indicator signal scanning & capturing application
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Pandas](https://img.shields.io/badge/pandas-required-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active%20development-yellow.svg)
![Architecture](https://img.shields.io/badge/architecture-modular-informational.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

A **modular quantitative research kernel** focused on **clarity, composability, and correctness**.

Quant-Kernel is *not* a monolithic trading bot.
It is a **clean execution graph**:

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

## Renderer (NOTE FOR LATER)

⚠️ **Intentionally deferred**

**Design decision (important):**

> `QKRenderer` will NOT draw everything itself.

Instead:

* Individual visual elements (price chart, MA overlay, signal markers, volume pane, etc.)
  will live in **separate component files**
* `QKRenderer` will only:

  * accept a DataFrame
  * compose components
  * orient/layout them

Think **UI layout engine**, not plotting logic.

Planned structure:

```
gui/
 ├─ components/
 │   ├─ price.py
 │   ├─ moving_average.py
 │   ├─ signals.py
 │   └─ volume.py
 ├─ QKRenderer.py   # orchestrates components only
```

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


