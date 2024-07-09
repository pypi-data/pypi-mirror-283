import pandas as pd
import pardos
import pytest


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "A": [1, 2, 3, 2, 1],
            "B": [4, 5, 6, 5, 4],
            "C": ["x", "y", "z", "y", "x"],
            "D": [10, 10, 10, 10, 10],
            "E": [1.1, 2.2, 3.3, 4.4, 5.5],
        }
    )


def test_select(sample_df):
    result = sample_df.select(A=2)
    assert len(result) == 2
    assert all(result["A"] == 2)

    result = sample_df.select(A=[1, 3])
    assert len(result) == 3
    assert all(result["A"].isin([1, 3]))


def test_augment(sample_df):
    def E(A, B):
        return A + B

    sample_df.augment(E)
    assert "E" in sample_df.columns
    assert all(sample_df["E"] == sample_df["A"] + sample_df["B"])

    def F(A, B):
        return A * B

    result = sample_df.augment(F, name="Product", inplace=False)
    assert "Product" not in sample_df.columns
    assert all(result == sample_df["A"] * sample_df["B"])


def test_is_constant(sample_df):
    assert sample_df["D"].is_constant()
    assert not sample_df["A"].is_constant()


def test_drop_constant(sample_df):
    result = sample_df.drop_constant()
    assert "D" not in result.columns
    assert len(result.columns) == 4

    result = sample_df.drop_constant(ignore=["D"])
    assert "D" in result.columns
    assert len(result.columns) == 5


def test_constants(sample_df):
    result = sample_df.constants()
    assert isinstance(result, pd.DataFrame)
    assert "D" in result.index
    assert result.loc["D", "Unique"] == 10

    result_series = sample_df.constants(as_series=True)
    assert isinstance(result_series, pd.Series)
    assert "D" in result_series.index
    assert result_series["D"] == 10


def test_broadcast(sample_df):
    result = sample_df.broadcast("A", to=4)
    assert 4 in result["A"].unique()
    assert len(result) > len(sample_df)

    result = sample_df.broadcast("C", to=["w"], when={"A": 1})
    assert "w" in result["C"].unique()
    assert len(result) > len(sample_df)


def test_smooth(sample_df):
    result = sample_df.smooth("A", group_by=("C",), alpha=0.5)
    assert len(result) == len(sample_df)
    assert not result.equals(sample_df["A"])

    result = sample_df.smooth("B", group_by=("C",), window=3)
    assert len(result) == len(sample_df)
    assert not result.equals(sample_df["B"])

    with pytest.raises(ValueError):
        sample_df.smooth("A", group_by=("C",))


def test_groupby_robust(sample_df):
    result = sample_df.groupby_robust(["A"], "mean")
    assert len(result) == 3  # 3 unique values in column C
    assert "B" in result.columns
    assert "D" in result.columns
    assert "C" in result.columns

    with pytest.raises(ValueError):
        sample_df["C"] = ["x", "y", "z", "x", "y"]
        sample_df.groupby_robust(["A"], "mean")


def test_groupby_and_take_best(sample_df):
    result = sample_df.groupby_and_take_best(["C"], "E", 1)
    assert len(result) == 3  # 3 unique values in column C
    assert all(result.groupby("C")["E"].transform("max") == result["E"])


def test_as_hashable(sample_df):
    sample_df["F"] = [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}, {"e": 5}]
    result = sample_df.as_hashable()
    assert all(result["F"].map(lambda x: isinstance(x, str)))


def test_set_collection(sample_df):
    result = sample_df.set_collection("G", [1, 2, 3])
    assert "G" in result.columns
    assert all(result["G"].map(lambda x: x == [1, 2, 3]))

    result = sample_df.set_collection("H", {"x": 1, "y": 2})
    assert "H" in result.columns
    assert all(result["H"].map(lambda x: x == {"x": 1, "y": 2}))


def test_fillNA(sample_df):
    from pardos.methods import NA_VALUE

    sample_df["I"] = [1, None, 3, NA_VALUE, 5]
    result = sample_df["I"].fillNA(0)
    assert result.tolist() == [1, None, 3, 0, 5]

    # cat_s = pd.Series(["a", "b", NA_VALUE, "c"], dtype="category")
    # result = cat_s.fillNA("d")
    # assert "d" in result.cat.categories
    # assert result.tolist() == ["a", "b", "d", "c"]


def test_isNA(sample_df):
    from pardos.methods import NA_VALUE

    sample_df["J"] = [1, None, 3, NA_VALUE, 5]
    result = sample_df["J"].isNA()
    assert result.tolist() == [False, False, False, True, False]


def test_notNA(sample_df):
    from pardos.methods import NA_VALUE

    sample_df["K"] = [1, None, 3, NA_VALUE, 5]
    result = sample_df["K"].notNA()
    assert result.tolist() == [True, True, True, False, True]


def test_to_categories(sample_df):
    sample_df["F"] = ["p", "q", "r", "p", "q"]
    result = sample_df.to_categories(threshold=0.7)
    assert isinstance(result["C"].dtype, pd.CategoricalDtype)
    assert isinstance(result["F"].dtype, pd.CategoricalDtype)
    assert not isinstance(result["A"].dtype, pd.CategoricalDtype)


def test_unique_per_col(sample_df):
    sample_df["F"] = ["p", "q", "r", "p", "q"]
    result = sample_df.unique_per_col(threshold=0.5, constant=True, display=False)
    assert len(result) == 1  # D column
    assert all(isinstance(r, pd.Series) for r in result)


# Add more test functions for other methods as needed
