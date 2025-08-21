import datetime

import numpy as np
import pandas as pd
import pytest
import src
from src.krakowbike.analyze_data import (
    calculate_basic_statistics,
    calculate_seasonal_trends,
    calculate_weather_correlations,
    weather_summary,
)

MOCK_STREET_NAMES = ["street_a", "street_b", "street_c"]
MOCK_AIR_COLUMN = "Air_quality_column"
MOCK_MONTH_TO_SEASON = {"January": "Winter"}


#########################################
# TODO complete functions' documentation
#########################################


@pytest.fixture
def sample_dataframe():
    dates = [
        "2023-01-01",
        "2023-01-02",
        "2023-01-03",
        "2023-01-04",
        "2023-01-05",
    ]
    data = {
        "street_a": [10.0, 20.0, 30.0, 40.0, 50.0],
        "street_b": [100.0, 200.0, 300.0, 400.0, 500.0],
        "street_c": [50.0, 50.0, 50.0, 50.0, 50.0],
        "Średnia temperatura dobowa [°C]": [-10, 0, 10, 20, 30],
        "Suma dobowa opadów [mm]": [0, 0.5, 1, 3, 10],
        "Air_quality_column": [0, 25, 60, 90, 200],
        "total_daily_traffic": [160.0, 270.0, 380.0, 490.0, 600.0],
    }
    df = pd.DataFrame(data, index=dates)
    df.index = pd.to_datetime(df.index)
    return df


#########################################


# tests for calculate_basic_statistics function
def test_calculate_basic_statistics(sample_dataframe):
    result = calculate_basic_statistics(sample_dataframe, for_html=False)
    expected_stats = ["mean", "std", "min", "max"]

    assert isinstance(result, pd.DataFrame)
    assert list(result.index) == expected_stats
    assert list(result.columns) == list(sample_dataframe.columns)

    for col in sample_dataframe.columns:
        assert np.isclose(result.loc["mean", col], sample_dataframe[col].mean())
        assert np.isclose(result.loc["std", col], sample_dataframe[col].std())
        assert np.isclose(result.loc["min", col], sample_dataframe[col].min())
        assert np.isclose(result.loc["max", col], sample_dataframe[col].max())


def test_calculate_basic_statistics_for_html(sample_dataframe):
    result = calculate_basic_statistics(sample_dataframe, for_html=True)

    assert isinstance(result, str)
    assert "<table" in result
    assert "<tr>" in result
    assert "<th>" in result


#########################################


# tests for weather_summary function
def test_weather_summary(monkeypatch, sample_dataframe):
    monkeypatch.setattr(src.krakowbike.analyze_data, "AIR_COLUMN", MOCK_AIR_COLUMN)
    result = weather_summary(sample_dataframe, for_html=False)
    expected_keys = ["temperature_impact", "precipitation_impact", "air_quality_impact"]
    expected_cols = ["mean", "std", "count"]
    temp_vals = {"Cold (<0°C)", "Cool (0-10°C)", "Mild (10-20°C)", "Warm (>20°C)"}
    precip_vals = {"No rain", "Light rain", "Moderate rain", "Heavy rain"}
    air_vals = {"Very good", "Good", "Moderate", "Sufficient", "Bad", "Vary bad"}

    assert isinstance(result, dict)
    assert list(result.keys()) == expected_keys

    for val in result.values():
        assert isinstance(val, pd.DataFrame)
        assert list(val.columns) == expected_cols

    assert set(result.get("temperature_impact").index).issubset(temp_vals)
    assert set(result.get("precipitation_impact").index).issubset(precip_vals)
    assert set(result.get("air_quality_impact").index).issubset(air_vals)


def test_weather_summary_for_html(monkeypatch, sample_dataframe):
    monkeypatch.setattr(src.krakowbike.analyze_data, "AIR_COLUMN", MOCK_AIR_COLUMN)
    result = weather_summary(sample_dataframe, for_html=True)
    expected_keys = ["temperature_impact", "precipitation_impact", "air_quality_impact"]

    assert isinstance(result, dict)
    assert list(result.keys()) == expected_keys
    for val in result.values():
        assert isinstance(val, str)
        assert "<table" in val
        assert "<tr>" in val
        assert "<th>" in val


#########################################


# tests for calculate_seasonal_trends function
def test_calculate_seasonal_trends(monkeypatch, sample_dataframe):
    monkeypatch.setattr(
        src.krakowbike.analyze_data, "MONTH_TO_SEASON", MOCK_MONTH_TO_SEASON
    )
    result = calculate_seasonal_trends(sample_dataframe, for_html=False)
    expected_keys = [
        "yearly_trends",
        "monthly_patterns",
        "seasonal_patterns",
        "weekly_patterns",
    ]
    expected_cols = ["mean", "sum", "std"]
    year_vals = {datetime.datetime(2023, 1, 1).year}
    month_vals = {"January"}
    week_days_vals = {
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    }
    seasons_vals = {"Winter"}

    assert isinstance(result, dict)
    assert list(result.keys()) == expected_keys

    for val in result.values():
        assert isinstance(val, pd.DataFrame)
        assert list(val.columns) == expected_cols

    assert set(result.get("yearly_trends").index).issubset(year_vals)
    assert set(result.get("monthly_patterns").index).issubset(month_vals)
    assert set(result.get("weekly_patterns").index).issubset(week_days_vals)
    assert set(result.get("seasonal_patterns").index).issubset(seasons_vals)


def test_calculate_seasonal_trends_for_html(monkeypatch, sample_dataframe):
    monkeypatch.setattr(
        src.krakowbike.analyze_data, "MONTH_TO_SEASON", MOCK_MONTH_TO_SEASON
    )
    result = calculate_seasonal_trends(sample_dataframe, for_html=True)
    expected_keys = [
        "yearly_trends",
        "monthly_patterns",
        "seasonal_patterns",
        "weekly_patterns",
    ]

    assert isinstance(result, dict)
    assert list(result.keys()) == expected_keys
    for val in result.values():
        assert isinstance(val, str)
        assert "<table" in val
        assert "<tr>" in val
        assert "<th>" in val


#########################################


# tests for calculate_weather_correlations function
def test_calculate_weather_correlations(monkeypatch, sample_dataframe):
    monkeypatch.setattr(src.krakowbike.analyze_data, "STREET_NAMES", MOCK_STREET_NAMES)
    result = calculate_weather_correlations(sample_dataframe)
    weather_cols = [
        col
        for col in sample_dataframe.columns
        if not (col in MOCK_STREET_NAMES or col == "total_daily_traffic")
    ]

    assert isinstance(result, dict)
    assert set(result.keys()) == set(weather_cols)
    for val in result.values():
        assert isinstance(val, (float, np.float64))
        assert -1 <= val <= 1


def test_sorting_calculate_weather_correlations(monkeypatch, sample_dataframe):
    monkeypatch.setattr(src.krakowbike.analyze_data, "STREET_NAMES", MOCK_STREET_NAMES)
    result = calculate_weather_correlations(sample_dataframe)

    correlations_values = list(result.values())
    abs_correlations = [abs(val) for val in correlations_values]

    assert abs_correlations == sorted(abs_correlations, reverse=True)
