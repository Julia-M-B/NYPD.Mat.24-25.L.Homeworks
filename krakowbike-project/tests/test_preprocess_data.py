import numpy as np
import pandas as pd
import pytest
import src.krakowbike.preprocess_data
from src.krakowbike.preprocess_data import (
    calculate_daily_traffic,
    fill_nan_values_with_mean,
    get_proper_time_period,
    merge_datasets,
    preprocess_dataset,
    remove_empty_columns,
    set_proper_values_types,
)

MOCK_STREET_NAMES = ["street_a", "street_b", "street_c"]

#########################################
# TODO complete functions' documentation
#########################################


# tests for merge_datasets function
def test_merge_multiple_dataframes():
    df1 = pd.DataFrame({"A": [1, 2, 3]}, index=[2, 1, 0])
    df2 = pd.DataFrame({"B": [4, 5, 6]}, index=[2, 1, 0])
    df3 = pd.DataFrame({"C": [7, 8, 9]}, index=[2, 1, 0])

    result = merge_datasets((df1, df2, df3))
    expected = pd.DataFrame(
        {"A": [3, 2, 1], "B": [6, 5, 4], "C": [9, 8, 7]}, index=[0, 1, 2]
    )

    assert result.equals(expected)


def test_index_order():
    df1 = pd.DataFrame({"A": [1, 2, 3]}, index=[2, 1, 0])
    df2 = pd.DataFrame({"B": [4, 5, 6]}, index=[3, 4, 5])
    result = merge_datasets((df1, df2))
    expected = pd.DataFrame(
        {
            "A": [3, 2, 1, np.nan, np.nan, np.nan],
            "B": [np.nan, np.nan, np.nan, 4, 5, 6],
        },
        index=[0, 1, 2, 3, 4, 5],
    )
    assert result.equals(expected)


#########################################


# tests for set_proper_values_types function
def test_set_proper_values_types():
    df = pd.DataFrame(
        {
            "A": ["1", "2", "-"],
            "B": ["3", " ", "5"],
        }
    )
    result = set_proper_values_types(df)

    assert result.dtypes["A"] == "float64"
    assert result.dtypes["B"] == "float64"
    assert np.isnan(result.loc[2, "A"])
    assert np.isnan(result.loc[1, "B"])


def test_already_numeric_columns():
    df = pd.DataFrame({"A": [1.0, 2.0, 3.0], "B": [4, 5, 6]})
    result = set_proper_values_types(df)

    assert result.dtypes["A"] == "float64"
    assert result.dtypes["B"] == "float64"


#########################################


# tests for remove_empty_columns function
def test_remove_columns_with_many_nulls():
    # threshold = 50%
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": [1, np.nan, np.nan, np.nan, np.nan],  # 80% null
            "C": [np.nan, np.nan, np.nan, np.nan, np.nan],  # empty column
        }
    )
    result = remove_empty_columns(df)

    assert "A" in result.columns
    assert "B" not in result.columns
    assert "D" not in result.columns
    assert result.shape == (5, 1)


def test_remove_columns_with_not_enough_nulls():
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4, 5],
            "B": [1, 2, 3, np.nan, 5],  # 20% null
        }
    )
    result = remove_empty_columns(df)

    assert result.equals(df)


def test_remove_empty_columns_edge_case():
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": [1, 2, np.nan, np.nan],  # 50% null
        }
    )
    result = remove_empty_columns(df)

    assert result.equals(df)


#########################################


# test for fill_nan_values_with_mean function
def test_fill_nan_with_mean():
    df = pd.DataFrame(
        {
            "A": [1.0, 2.0, np.nan, 4.0],
            "B": [np.nan, 2.0, 3.0, 4.0],
            "C": [1.0, 2.0, 3.0, 4.0],
        }
    )
    result = fill_nan_values_with_mean(df)

    assert result.isna().sum().sum() == 0
    assert result.loc[2, "A"] == (1.0 + 2.0 + 4.0) / 3.0
    assert result.loc[0, "B"] == (2.0 + 3.0 + 4.0) / 3.0


#########################################


# tests for get_proper_time_period function
def test_get_proper_time_period():
    start_date = "2020-01-02"
    end_date = "2020-01-03"
    df = pd.DataFrame(
        {"A": [1, 2, 3, 4]},
        index=["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04"],
    )
    expected_df = pd.DataFrame({"A": [2, 3]}, index=["2020-01-02", "2020-01-03"])
    result = get_proper_time_period(df, start_date, end_date)

    assert result.equals(expected_df)


def test_start_date_too_early():
    start_date = "2016-01-01"
    end_date = "2020-01-01"
    df = pd.DataFrame(
        {"A": [1, 2, 3]}, index=["2020-01-01", "2020-01-02", "2020-01-03"]
    )
    with pytest.raises(ValueError) as err:
        get_proper_time_period(df, start_date, end_date)

    assert "Invalid start_date/end_date argument." in str(err.value)


def test_end_date_too_late():
    start_date = "2020-01-01"
    end_date = "2025-01-01"
    df = pd.DataFrame(
        {"A": [1, 2, 3]}, index=["2020-01-01", "2020-01-02", "2020-01-03"]
    )
    with pytest.raises(ValueError) as err:
        get_proper_time_period(df, start_date, end_date)

    assert "Invalid start_date/end_date argument." in str(err.value)


def test_start_date_after_end_date():
    start_date = "2020-01-03"
    end_date = "2020-01-01"
    df = pd.DataFrame(
        {"A": [1, 2, 3]}, index=["2020-01-01", "2020-01-02", "2020-01-03"]
    )
    with pytest.raises(ValueError) as err:
        get_proper_time_period(df, start_date, end_date)

    assert "Invalid start_date/end_date argument." in str(err.value)


#########################################


def test_calculate_daily_traffic(monkeypatch):
    monkeypatch.setattr(
        src.krakowbike.preprocess_data, "STREET_NAMES", MOCK_STREET_NAMES
    )
    df = pd.DataFrame(
        {
            "street_a": [10, 20, 30],
            "street_b": [5, 15, 25],
            "street_c": [2, 8, 12],
            "other_col": [100, 200, 300],
        }
    )

    calculate_daily_traffic(df)

    expected_sums = [17, 43, 67]  # row-wise sum of street columns only

    assert "total_daily_traffic" in df.columns
    assert np.all(df["total_daily_traffic"].values == expected_sums)


#########################################


# tests for preprocess_dataset function
def test_preprocess_dataset(monkeypatch):
    monkeypatch.setattr(
        src.krakowbike.preprocess_data, "STREET_NAMES", MOCK_STREET_NAMES
    )
    df1 = pd.DataFrame(
        {
            "street_a": ["10", "20", "-", "-", "30", "40"],
            "other1": ["1", "2", "3", "4.", "5.", "6"],
        },
        index=[
            "2018-01-03",
            "2018-01-04",
            "2018-01-05",
            "2018-01-06",
            "2018-01-01",
            "2018-01-02",
        ],
    )

    df2 = pd.DataFrame(
        {
            "street_b": ["5", " ", "15", "23", "7", "20"],
            "street_c": ["4", "2", "8", "12", "67", "134"],
            "other2": [2.0, np.nan, np.nan, np.nan, np.nan, 30.0],
        },
        index=[
            "2018-01-01",
            "2018-01-02",
            "2018-01-03",
            "2018-01-04",
            "2018-01-05",
            "2018-01-06",
        ],
    )
    result = preprocess_dataset(
        df1, df2, start_date="2018-01-01", end_date="2018-01-06"
    )

    assert "total_daily_traffic" in result.columns
    assert "other2" not in result.columns
    assert result.dtypes.apply(lambda x: x == "float64").all()
    assert result.isna().sum().sum() == 0


def test_preprocessing_with_invalid_dates(monkeypatch):
    monkeypatch.setattr(
        src.krakowbike.preprocess_data, "STREET_NAMES", MOCK_STREET_NAMES
    )
    df1 = pd.DataFrame(
        {
            "street_a": ["10", "20", "-", "-", "30", "40"],
            "other1": ["1", "2", "3", "4.", "5.", "6"],
        },
        index=[
            "2018-01-03",
            "2018-01-04",
            "2018-01-05",
            "2018-01-06",
            "2018-01-01",
            "2018-01-02",
        ],
    )

    df2 = pd.DataFrame(
        {
            "street_b": ["5", " ", "15", "23", "7", "20"],
            "street_c": ["4", "2", "8", "12", "67", "134"],
            "other2": [2.0, np.nan, np.nan, np.nan, np.nan, 30.0],
        },
        index=[
            "2018-01-01",
            "2018-01-02",
            "2018-01-03",
            "2018-01-04",
            "2018-01-05",
            "2018-01-06",
        ],
    )
    with pytest.raises(ValueError):
        preprocess_dataset(df1, df2, start_date="2020-01-01", end_date="2018-01-01")
