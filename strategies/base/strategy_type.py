from enum import Enum
from strategies.strategy_ma_crossover import MACrossoverStrategy
from strategies.strategy_mcginley_breakout import McGinleyBreakoutStrategy
from indicators.base.indicator_type import IndicatorType
from strategies.strategy_vwap_crossover import VWAPCrossoverStrategy


class StrategyType(Enum):
    MA_CROSSOVER = {
        "strategy": MACrossoverStrategy,
        "params": {
            "fast": "ma_7",
            "slow": "ma_21",
        },
        "indicators": [
            IndicatorType.MA(period=7),
            IndicatorType.MA(period=21),
        ],
    }

    MCGINLEY_BREAKOUT = {
        "strategy": McGinleyBreakoutStrategy,
        "params": {
            "price_col": "close",
            "mcg_col": "mcginley_14",
        },
        "indicators": [
            IndicatorType.MC_GINLEY(period=14),
        ],
    }
    VWAP_1D_7D = {
        "strategy": VWAPCrossoverStrategy,
        "params": {
            "fast_days": 1,
            "slow_days": 7,
        },
        "indicators": [
            IndicatorType.VWAP(1),
            IndicatorType.VWAP(7),
        ],
    }

