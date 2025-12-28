# indicators/indicator_type.py
from enum import Enum

from indicators.indicator_day_range_percentage import DayRangePct
from indicators.indicator_mcginley import McGinleyDynamic
from indicators.indicator_moving_average import MovingAverage
from indicators.indicator_vwap import VWAP


class IndicatorType(Enum):
    MC_GINLEY = McGinleyDynamic
    MA = MovingAverage
    DAY_RANGE_PCT = DayRangePct
    VWAP = VWAP


    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)
