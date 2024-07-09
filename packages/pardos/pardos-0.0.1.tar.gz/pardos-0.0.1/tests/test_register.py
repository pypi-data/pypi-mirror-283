import pandas as pd
from pardos.register import register_dataframe_method, register_series_method


def test_register_dataframe_method():
    @register_dataframe_method
    def test_method(df, value):
        return df + value

    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    result = df.test_method(1)

    assert hasattr(
        pd.DataFrame, "test_method"
    ), "Method should be registered to DataFrame"
    assert result.equals(
        pd.DataFrame({"A": [2, 3, 4], "B": [5, 6, 7]})
    ), "Method should add value to all elements"


def test_register_series_method():
    @register_series_method
    def test_method(series, value):
        return series + value

    s = pd.Series([1, 2, 3])
    result = s.test_method(1)

    assert hasattr(pd.Series, "test_method"), "Method should be registered to Series"
    assert result.equals(
        pd.Series([2, 3, 4])
    ), "Method should add value to all elements"


def test_method_chaining():
    @register_dataframe_method
    def method1(df):
        return df * 2

    @register_dataframe_method
    def method2(df):
        return df + 1

    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    result = df.method1().method2()

    expected = pd.DataFrame({"A": [3, 5, 7], "B": [9, 11, 13]})
    assert result.equals(expected), "Methods should be chainable"


# Add more tests as needed
