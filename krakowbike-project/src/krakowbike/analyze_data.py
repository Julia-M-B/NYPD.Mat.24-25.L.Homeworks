import pandas as pd

from src.krakowbike.utils import AIR_COLUMN, MONTH_TO_SEASON, STREET_NAMES

#########################################
# TODO complete functions' documentation
#########################################


def calculate_basic_statistics(
    df: pd.DataFrame, for_html: bool = False
) -> pd.DataFrame | str:
    """
    Return data frame with basic statistics (mean, std, min, max)
    for each column in given dataframe.
    :param df: dataframe for which the statistics are calculated
    :param for_html:
    :return: dataframe
    """
    means = df.mean().values
    stds = df.std().values
    mins = df.min().values
    maxs = df.max().values
    stats = {"mean": means, "std": stds, "min": mins, "max": maxs}
    df = pd.DataFrame(stats, index=df.columns)
    df = round(df, 2)
    if for_html:
        return df.to_html()
    return df


def weather_summary(df: pd.DataFrame, for_html: bool = False) -> dict:
    """
    Create summaries for weather factors:
    - average daily temperature
    - total daily rainfall
    - air quality
    :param df: dataframe containing weather data
    :return: dictionary with summary for different weather factors
    """
    df_copy = df.copy()
    temp_col = "Średnia temperatura dobowa [°C]"
    df_copy["temp_category"] = pd.cut(
        df_copy[temp_col],
        bins=[-float("inf"), 0, 10, 20, float("inf")],
        labels=["Cold (<0°C)", "Cool (0-10°C)", "Mild (10-20°C)", "Warm (>20°C)"],
    )

    precip_col = "Suma dobowa opadów [mm]"
    df_copy["rain_category"] = pd.cut(
        df_copy[precip_col],
        bins=[-float("inf"), 0, 1, 5, float("inf")],
        labels=["No rain", "Light rain", "Moderate rain", "Heavy rain"],
    )

    df_copy["air_category"] = pd.cut(
        df_copy[AIR_COLUMN],
        bins=[-float("inf"), 20, 50, 80, 110, 150, float("inf")],
        labels=["Very good", "Good", "Moderate", "Sufficient", "Bad", "Vary bad"],
    )
    summary = {
        "temperature_impact": df_copy.groupby("temp_category", observed=True)[
            "total_daily_traffic"
        ].agg(["mean", "std", "count"]),
        "precipitation_impact": df_copy.groupby("rain_category", observed=True)[
            "total_daily_traffic"
        ].agg(["mean", "std", "count"]),
        "air_quality_impact": df_copy.groupby("air_category", observed=True)[
            "total_daily_traffic"
        ].agg(["mean", "std", "count"]),
    }
    for k, v in summary.items():
        summary[k] = round(v,2)
    if for_html:
        summary = dict([(k, v.to_html()) for k, v in summary.items()])

    return summary


def calculate_seasonal_trends(df: pd.DataFrame, for_html: bool = False) -> dict:
    """
    Analyze daily cycling traffic depending on the day of the week,
    month, season and year.
    :param df: dataframe containing traffic data
    :return: dictionary with seasonal summaries
    """
    df_copy = df.copy()
    df_copy["year"] = df_copy.index.year
    df_copy["month"] = df_copy.index.month_name()
    df_copy["day_of_week"] = df_copy.index.day_name()
    df_copy["season"] = df_copy["month"].map(MONTH_TO_SEASON)

    analysis_results = {
        "yearly_trends": df_copy.groupby("year")["total_daily_traffic"].agg(
            ["mean", "sum", "std"]
        ),
        "monthly_patterns": df_copy.groupby("month")["total_daily_traffic"].agg(
            ["mean", "sum", "std"]
        ),
        "seasonal_patterns": df_copy.groupby("season")["total_daily_traffic"].agg(
            ["mean", "sum", "std"]
        ),
        "weekly_patterns": df_copy.groupby("day_of_week")["total_daily_traffic"].agg(
            ["mean", "sum", "std"]
        ),
    }
    for k, v in analysis_results.items():
        analysis_results[k] = round(v,2)
    if for_html:
        analysis_results = dict([(k, v.to_html()) for k, v in analysis_results.items()])

    return analysis_results


def calculate_weather_correlations(df: pd.DataFrame) -> dict:
    """
    Calculate correlations between different weather factors
    and total daily bicycle traffic.
    :param df: dataframe for which the correlations are calculated
    :return: dictionary containing correlations coefficients
    """
    df_copy = df.copy()
    weather_columns = [
        col
        for col in df_copy.columns
        if not (col in STREET_NAMES or col == "total_daily_traffic")
    ]

    correlations = {}
    for weather_col in weather_columns:
        correlations[weather_col] = df_copy["total_daily_traffic"].corr(
            df_copy[weather_col]
        )

    return dict(sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True))
