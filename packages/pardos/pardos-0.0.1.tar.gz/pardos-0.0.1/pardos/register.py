# Vendored from https://github.com/Zsailer/pandas_flavor
from functools import wraps
from typing import Any, Callable

from pandas.api.extensions import register_dataframe_accessor, register_series_accessor


def register_dataframe_method(method: Callable[..., Any]) -> Callable[..., Any]:
    """
    Register a function as a method attached to the Pandas DataFrame.

    This decorator allows you to add custom methods to Pandas DataFrames,
    making them accessible as if they were built-in Pandas methods.

    Args:
        method: The function to be registered as a DataFrame method.

    Returns:
        The decorated function.

    Example:
        @register_dataframe_method
        def print_column(df, col):
            '''Print the dataframe column given'''
            print(df[col])

        # Usage:
        df.print_column('column_name')
    """

    @wraps(method)
    def inner(*args: Any, **kwargs: Any) -> Any:
        class AccessorMethod:
            def __init__(self, pandas_obj: Any):
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args: Any, **kwargs: Any) -> Any:
                return method(self._obj, *args, **kwargs)

        register_dataframe_accessor(method.__name__)(AccessorMethod)
        return method

    return inner()


def register_series_method(method: Callable[..., Any]) -> Callable[..., Any]:
    """
    Register a function as a method attached to the Pandas Series.

    This decorator allows you to add custom methods to Pandas Series,
    making them accessible as if they were built-in Pandas methods.

    Args:
        method: The function to be registered as a Series method.

    Returns:
        The decorated function.

    Example:
        @register_series_method
        def custom_mean(ser):
            '''Calculate a custom mean'''
            return ser.mean() * 2

        # Usage:
        series.custom_mean()
    """

    @wraps(method)
    def inner(*args: Any, **kwargs: Any) -> Any:
        class AccessorMethod:
            def __init__(self, pandas_obj: Any):
                self._obj = pandas_obj

            @wraps(method)
            def __call__(self, *args: Any, **kwargs: Any) -> Any:
                return method(self._obj, *args, **kwargs)

        register_series_accessor(method.__name__)(AccessorMethod)
        return method

    return inner()
