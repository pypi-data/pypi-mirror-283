import inspect
import itertools
import json
from typing import Any, Callable, Optional, Sequence, Union

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from pandas.api.types import  union_categoricals

from .register import register_dataframe_method, register_series_method

NA_VALUE = "N/A"


@register_dataframe_method
def select(df: DataFrame, **kwargs) -> DataFrame:
    """
    Select rows from DataFrame based on column values.

    Args:
        df: Input DataFrame
        **kwargs: Column names and values to select

    Returns:
        DataFrame with selected rows

    Examples:
        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        >>> select(df, A=2)
           A  B
        1  2  5
    """
    attrs = df.attrs
    for k, vs in kwargs.items():
        if vs is None:
            df = df[df[k].isna()]
        elif isinstance(vs, list):
            df = df[df[k].isin(vs)]
        else:
            df = df[df[k] == vs]
    df.attrs = attrs
    return df


@register_dataframe_method
def augment(
    df: DataFrame, fn: Callable, name: Optional[str] = None, inplace: bool = True
) -> Optional[Series]:
    """
    Apply a function to create a new column in the DataFrame.

    Args:
        df: Input DataFrame
        fn: Function to apply
        name: Name of the new column (default: function name)
        inplace: If True, modify DataFrame in place

    Returns:
        New Series if not inplace, None otherwise
    Examples:
        >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        >>> def C(A, B):
        ...     return A+B if A > 1 else B
        >>> augment(df, C)
           A  B  C
        0  1  4  4
        1  2  5  7
        2  3  6  9
    """
    name = name if name else fn.__name__
    params = list(inspect.signature(fn).parameters.keys())
    for param in params:
        assert (
            param in df.columns
        ), f"Function argument '{param}' not in dataframe columns"

    def wrapper(row):
        kwargs = {k: row.get(k) for k in params}
        return fn(**kwargs)

    ser = df.apply(wrapper, axis=1)
    if not inplace:
        return ser
    df[name] = ser


@register_series_method
def is_constant(ser: Series) -> bool:
    """
    Check if all values in a Series are the same.

    Args:
        ser: Input Series

    Returns:
        True if all values are the same, False otherwise
    """
    return ser.nunique(dropna=False) == 1


@register_dataframe_method
def drop_constant(
    df: DataFrame, inplace: bool = False, ignore: Optional[Sequence[str]] = None
) -> Optional[DataFrame]:
    """
    Drop columns with constant values from a DataFrame.

    Args:
        df: Input DataFrame
        inplace: If True, do operation inplace and return None
        ignore: List of column names to ignore

    Returns:
        DataFrame with constant columns dropped
    """
    _ignore = ignore or []
    columns_to_drop = [
        c for c in df.columns if df[c].is_constant() and c not in _ignore
    ]
    return df.drop(columns=columns_to_drop, inplace=inplace)


@register_dataframe_method
def constants(df: DataFrame, as_series: bool = False) -> Union[Series, DataFrame]:
    """
    Returns constant columns and their unique values.

    Args:
        df: Input DataFrame
        as_series: If True, return as Series instead of DataFrame

    Returns:
        Series or DataFrame with constant columns and their unique values
    """
    constant_cols = [c for c in df.columns if df[c].is_constant()]
    constant_vals = [df[c].iloc[0] for c in constant_cols]
    ser = pd.Series(data=constant_vals, index=constant_cols)
    if as_series:
        return ser
    return pd.DataFrame(ser, columns=["Unique"])


@register_dataframe_method
def broadcast(
    df: DataFrame,
    col: str,
    when: Optional[dict[str, Any]] = None,
    to: Optional[Union[str, list]] = None,
    concat: bool = True,
) -> DataFrame:
    """
    Broadcast an attribute by copying rows and changing the values of a given column.

    Args:
        df: Input DataFrame
        col: Column to broadcast
        to: Values to broadcast to (default: all other unique values in the column)
        concat: If True, concatenate result with original DataFrame
        **when: Conditions for selecting rows to broadcast

    Returns:
        DataFrame with broadcasted values
    """
    tmp = df.select(**(when or {}))
    from_vals = tmp[col].unique()
    if to is None:
        to = [x for x in df[col].unique() if x not in from_vals]
    if not isinstance(to, (tuple, list)):
        to = [to]

    join = np.array([[old, new] for old in from_vals for new in to])
    col_old = col + "_old"
    join = pd.DataFrame(data=join, columns=[col_old, col])
    tmp = tmp.rename(columns={col: col_old})
    tmp = pd.merge(tmp, join, on=col_old)
    tmp.drop(columns=[col_old], inplace=True)
    if concat:
        merged = pd.concat([df, tmp])
        return merged
    return tmp


@register_dataframe_method
def constants_subset(df: DataFrame, **selector) -> DataFrame:
    """
    Returns variables that are constant in the selected subset while leaving out
    aspects that are constant for the entire dataset.

    Args:
        df: Input DataFrame
        **selector: Conditions for selecting the subset

    Returns:
        DataFrame with constants in the subset that are not constant in the full dataset
    """
    sub_df = df.select(**selector)
    sub_constants = sub_df.constants()
    return sub_constants[~sub_constants.index.isin(set(df.constants().index))]


@register_dataframe_method
def smooth(
    df: DataFrame,
    column: str,
    *,
    group_by: tuple,
    alpha: Optional[float] = None,
    window: Optional[int] = None,
) -> Series:
    """
    Smooth a column in the DataFrame using exponential weighted mean or rolling mean.

    Args:
        df: Input DataFrame
        column: Column to smooth
        group_by: Columns to group by before smoothing
        alpha: Smoothing factor for exponential weighted mean
        window: Window size for rolling mean

    Returns:
        Smoothed Series

    Raises:
        ValueError: If neither alpha nor window is specified
    """
    if alpha is not None:
        return df.groupby(list(group_by))[column].transform(
            lambda x: x.ewm(alpha=alpha).mean()
        )
    elif window is not None:
        return df.groupby(list(group_by))[column].transform(
            lambda x: x.rolling(window, center=True).mean()
        )
    raise ValueError("Either alpha or window must be specified")


@register_dataframe_method
def broadcast_attrs(df: DataFrame, prefix: str = "") -> DataFrame:
    """
    Add DataFrame attributes as new columns.

    Args:
        df: Input DataFrame
        prefix: Prefix for new column names

    Returns:
        DataFrame with new columns added from attributes
    """
    for col, val in df.attrs.items():
        if isinstance(val, (tuple, list, dict)):
            df[prefix + col] = np.array(list(itertools.repeat(val, len(df))))
        else:
            df[prefix + col] = val
    return df


@register_dataframe_method
def groupby_robust(
    df: pd.DataFrame,
    groupby: Sequence[str],
    number_agg: Union[str, Callable],
    enforce_unique_str: bool = True,
    multiple_token: Any = "MULTIPLE",
    **groupby_kws,
) -> pd.DataFrame:
    """
    Group by and aggregate, preserving string columns

    Args:
        df: Input DataFrame
        groupby: Columns to group by
        number_agg: Aggregation function for numeric columns
        enforce_unique_str: If True, raise error for non-unique string values
        multiple_token: Token to use for multiple string values
        **groupby_kws: Additional keyword arguments for groupby

    Returns:
        Grouped and aggregated DataFrame
    """

    def str_agg(col: pd.Series) -> Any:
        if col.nunique(dropna=False) == 1:
            return col.mode().iloc[0]
        if enforce_unique_str:
            raise ValueError(f"Multiple values for col {col.name}: {col.unique()}")
        return multiple_token

    agg_by_type = {
        "number": number_agg,
        "object": str_agg,
        "category": str_agg,
    }

    cols_by_type = {
        type_: df.select_dtypes(type_).columns.difference(groupby)
        for type_ in agg_by_type
    }

    agg_by_col = {
        col: (col, agg_by_type[type_])
        for type_, cols in cols_by_type.items()
        for col in cols
    }

    return df.groupby(groupby, **groupby_kws).agg(**agg_by_col)


@register_dataframe_method
def groupby_and_take_best(
    df: pd.DataFrame, groupby: Sequence[str], metric: str, n: int
) -> pd.DataFrame:
    """
    Group by and for each subgroup keep 'n' rows with the largest value of the metric.

    Args:
        df: Input DataFrame
        groupby: Columns to group by
        metric: Column name to use for selecting the best rows
        n: Number of rows to keep per group

    Returns:
        DataFrame with the best 'n' rows per group
    """

    def keep_best(df_group: pd.DataFrame) -> pd.DataFrame:
        return df_group.sort_values(metric, ascending=False).head(n)

    return df.groupby(groupby, as_index=False).apply(keep_best).reset_index(drop=True)

@register_dataframe_method
def as_hashable(df: pd.DataFrame, inplace: bool = False) -> pd.DataFrame:
    """
    Ensure all values in the DataFrame are hashable.

    Args:
        df: Input DataFrame
        inplace: If True, modify DataFrame in place

    Returns:
        DataFrame with all values converted to hashable types
    """
    if not inplace:
        df = df.copy()
    for col in df.columns:
        if not df[col].map(pd.api.types.is_hashable).all():
            df[col] = df[col].map(
                lambda x: json.dumps(x) if not pd.api.types.is_hashable(x) else x
            )
    return df


@register_dataframe_method
def set_collection(df: pd.DataFrame, col: str, val: Any) -> pd.DataFrame:
    """
    Set a value to a column in the DataFrame. Works well with collection types.

    Args:
        df: Input DataFrame
        col: Column name to set the value
        val: Value to set (can be a scalar, list, tuple, or dict)

    Returns:
        DataFrame with the new column added or updated
    """
    if isinstance(val, (tuple, list, dict)):
        df[col] = np.array(itertools.repeat(val, len(df)))
    else:
        df[col] = val
    return df


#### NA RELATED FUNCTIONS ####

# The goal of NA_VALUE is to avoid quirks with NaN and None values in pandas.
# In many cases we explicitly care about missing values


@register_series_method
def fillNA(ser: Series, value: Any, inplace: bool = False) -> Series:
    """
    Fill NA values in a Series with a specified value.

    Args:
        ser: Input Series
        value: Value to use for filling NA
        inplace: If True, do operation inplace and return None

    Returns:
        Series with NA values filled
    """
    if not inplace:
        ser = ser.copy()
    if ser.dtype.name == "category":
        ser.cat.add_categories(value)
    ser[ser == NA_VALUE] = value
    return ser


@register_series_method
def isNA(ser: Series) -> Series:
    """
    Check if values in a Series are NA.

    Args:
        ser: Input Series

    Returns:
        Boolean Series indicating NA values
    """
    return ser == NA_VALUE


@register_series_method
def notNA(ser: Series) -> Series:
    """
    Check if values in a Series are not NA.

    Args:
        ser: Input Series

    Returns:
        Boolean Series indicating non-NA values
    """
    return ser != NA_VALUE


#### CATEGORY RELATED FUNCTIONS ####


def broadcast_categories(dfs: list[DataFrame]) -> list[DataFrame]:
    """
    Ensure categorical columns have the same categories across all DataFrames.

    Args:
        dfs: list of DataFrames

    Returns:
        list of DataFrames with broadcasted categories
    """
    for col in set.intersection(*[set(df.columns) for df in dfs]):
        if all(isinstance(df[col].dtype, pd.CategoricalDtype) for df in dfs):
            all_cats = union_categoricals([df[col] for df in dfs]).categories
            for df in dfs:
                df[col] = pd.Categorical(df[col], categories=all_cats)
    return dfs


@register_dataframe_method
def to_categories(
    df: DataFrame, threshold: float = 0.1, inplace: bool = False
) -> DataFrame:
    """
    Convert object columns to category type if they have few unique values.

    Args:
        df: Input DataFrame
        threshold: Maximum ratio of unique values to total values for conversion
        inplace: If True, do operation inplace and return None

    Returns:
        DataFrame with applicable columns converted to category type
    """
    if not inplace:
        df = df.copy()
    for c in df.select_dtypes(object):
        if df[c].nunique(dropna=False) < threshold * len(df):
            df[c] = df[c].astype("category")
            if df[c].isna().sum() > 0:
                df[c] = df[c].cat.add_categories(NA_VALUE).fillna(NA_VALUE)
    return df


#### NOTEBOOK RELATED FUNCTIONS ####


@register_dataframe_method
def unique_per_col(
    df: DataFrame, threshold: float = 0.5, constant: bool = False, display: bool = True
) -> Optional[list]:
    """
    Display or return unique values for columns with few unique values.

    Args:
        df: Input DataFrame
        threshold: Maximum ratio of unique values to total values for display
        constant: If True, include constant columns
        display: If True, display results; if False, return as list

    Returns:
        List of Series with unique values per column if display is False, None otherwise
    """
    low = 0 if constant else 1
    uniqs = []
    with pd.option_context("display.max_colwidth", 400):
        for col in df:
            if low < df[col].nunique(dropna=False) < threshold * len(df):
                ser = df[col]
                if ser.isna().any():
                    ser = ser.fillna(NA_VALUE)
                ser = ser.value_counts()
                uniqs.append(ser)
                if display:
                    from IPython.display import display as notebook_display

                    notebook_display(DataFrame(ser).T)
    if not display:
        return uniqs
