from enum import Enum


class StrEnumMixin(Enum):
    def __str__(self):
        return self.value


class Interval(StrEnumMixin):
    SECOND = "1s"
    MINUTE = "1m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    THIRTY_MINUTE = "30m"
    HOUR = "1h"
    FOUR_HOUR = "4h"
    DAY = "1d"
    WEEK = "1w"
    MONTH = "1M"
