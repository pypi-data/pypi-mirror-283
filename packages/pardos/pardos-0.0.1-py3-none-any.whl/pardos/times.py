import re
from datetime import datetime, timedelta
from typing import Union

import pandas as pd
from pandas.api.extensions import register_dataframe_accessor, register_series_accessor


class InvalidTimeStringError(ValueError):
    """Raised when an invalid time string is provided."""

    pass


def parse_human_time(time_string: str) -> timedelta:
    """
    Parse a human-readable time string into a timedelta object.

    Args:
        time_string: A string representing a duration (e.g., '1d2h30m')

    Returns:
        A timedelta object representing the parsed duration

    Raises:
        InvalidTimeStringError: If the time string is invalid
    """
    if not isinstance(time_string, str):
        raise InvalidTimeStringError("Input must be a string")

    time_string = time_string.lower().strip()
    if not time_string:
        raise InvalidTimeStringError("Time string cannot be empty")

    pattern = r"^(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$"
    match = re.match(pattern, time_string)

    if not match:
        raise InvalidTimeStringError(
            "Invalid time string format or incorrect order of units"
        )

    days, hours, minutes, seconds = match.groups()

    if all(unit is None for unit in (days, hours, minutes, seconds)):
        raise InvalidTimeStringError("At least one time unit must be specified")

    total_seconds = 0
    if days:
        total_seconds += int(days) * 86400
    if hours:
        total_seconds += int(hours) * 3600
    if minutes:
        total_seconds += int(minutes) * 60
    if seconds:
        total_seconds += int(seconds)

    if total_seconds == 0:
        raise InvalidTimeStringError("Total duration must be greater than zero")

    return timedelta(seconds=total_seconds)


class DateTimeAccessor:
    """Custom accessor for datetime-like pandas objects."""

    def __init__(self, pandas_obj: Union[pd.Series, pd.DataFrame]):
        self._obj = pandas_obj
        if not pd.api.types.is_datetime64_any_dtype(self._obj):
            raise AttributeError("Can only use .hdt accessor with datetime-like values")

    def within(self, time_string: str) -> Union[pd.Series, pd.DataFrame]:
        """
        Check if datetime values are within the specified time from now.

        Args:
            time_string: A string representing a duration (e.g., '1d2h30m')

        Returns:
            A boolean Series or DataFrame
        """
        delta = parse_human_time(time_string)
        now = datetime.now()
        return (now - delta) <= self._obj

    def before(self, time_string: str) -> Union[pd.Series, pd.DataFrame]:
        """
        Check if datetime values are before the specified time from now.

        Args:
            time_string: A string representing a duration (e.g., '1d2h30m')

        Returns:
            A boolean Series or DataFrame
        """
        delta = parse_human_time(time_string)
        now = datetime.now()
        return self._obj < (now - delta)


# Register the custom accessor
register_dataframe_accessor("hdt")(DateTimeAccessor)
register_series_accessor("hdt")(DateTimeAccessor)
