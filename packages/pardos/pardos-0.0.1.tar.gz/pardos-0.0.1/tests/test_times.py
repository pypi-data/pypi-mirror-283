from datetime import datetime, timedelta

import pandas as pd
import pytest
from pardos.times import InvalidTimeStringError, parse_human_time


def test_parse_human_time():
    assert parse_human_time("1d") == timedelta(days=1)
    assert parse_human_time("2h30m") == timedelta(hours=2, minutes=30)
    assert parse_human_time("1d12h30m45s") == timedelta(
        days=1, hours=12, minutes=30, seconds=45
    )

    with pytest.raises(InvalidTimeStringError):
        parse_human_time("invalid")

    with pytest.raises(InvalidTimeStringError):
        parse_human_time("1d2d")

    with pytest.raises(InvalidTimeStringError):
        parse_human_time("")


def test_datetime_accessor_initialization():
    df = pd.DataFrame({"date": [datetime.now()]})
    assert hasattr(df["date"], "hdt")

    with pytest.raises(AttributeError):
        pd.DataFrame({"not_date": [1, 2, 3]})["not_date"].hdt


def test_within():
    now = datetime.now()
    df = pd.DataFrame(
        {
            "date": [
                now - timedelta(hours=1),
                now - timedelta(hours=3),
                now - timedelta(days=1),
                now - timedelta(days=2),
            ]
        }
    )

    result = df["date"].hdt.within("2h")
    assert result.tolist() == [True, False, False, False]

    result = df["date"].hdt.within("1d12h")
    assert result.tolist() == [True, True, True, False]


def test_before():
    now = datetime.now()
    df = pd.DataFrame(
        {
            "date": [
                now - timedelta(hours=1),
                now - timedelta(hours=3),
                now - timedelta(days=1),
                now - timedelta(days=2),
            ]
        }
    )

    result = df["date"].hdt.before("2h")
    assert result.tolist() == [False, True, True, True]

    result = df["date"].hdt.before("1d12h")
    assert result.tolist() == [False, False, False, True]


# Add more tests as needed
