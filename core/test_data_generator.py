import pandas as pd
import numpy as np

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.expand_frame_repr", False)


def make_test_df(
    rows: int = 100,
    start="2025-01-01 09:15",
    freq="5min",
    tz="Asia/Kolkata",
):
    timestamps = pd.date_range(
        start=start,
        periods=rows,
        freq=freq,
        tz=tz
    )

    base = 100
    noise = np.random.normal(0, 0.8, size=rows).cumsum()

    close = base + noise
    open_ = close + np.random.normal(0, 0.4, size=rows)
    high = np.maximum(open_, close) + np.random.uniform(0.2, 1.0, size=rows)
    low = np.minimum(open_, close) - np.random.uniform(0.2, 1.0, size=rows)
    volume = np.random.randint(100_000, 900_000, size=rows)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "adjclose": close,
        "volume": volume,
    })

    return df
