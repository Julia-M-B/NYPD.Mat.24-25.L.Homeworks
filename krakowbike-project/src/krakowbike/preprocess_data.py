import pandas as pd

from src.krakowbike.utils import STREET_NAMES


def merge_datasets(*dataframes: tuple[pd.DataFrame]) -> pd.DataFrame:
    """
    Merge multiple dataframes horizontally and sort by index.

    :param dataframes: Tuple of dataframe to merge
    :return: Merged and sorted dataframe
    """
    merged_df = pd.concat(list(*dataframes), axis=1)
    return merged_df.sort_index()


def set_proper_values_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all columns to float64, replacing missing value indicators with NaN.

    :param df: pd.Dataframe, dataframe with mixed data types
    :return: pd.Dataframe, dataframe with all columns as float64
    """
    non_numerical_cols = [
        col for col in df.columns if df[col].dtypes in ["object", "category", "string"]
    ]
    for col in non_numerical_cols:
        df[col] = df[col].str.replace("-", "nan")
        df[col] = df[col].str.replace(" ", "nan")
    return df.astype("float64")


def fill_nan_values_with_mean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values with column means.

    :param df: pd.Dataframe, dataframe with missing values
    :return: pd.Dataframe, dataframe with NaN values filled with column means
    """
    means = df.mean()
    return df.fillna(means, axis=0)


def get_proper_time_period(
    df: pd.DataFrame, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Filter DataFrame to specified date range (minimum 2017-01-01,
    maximum 2021-12-31).

    :param df: pd.Dataframe, dataframe to be filtered
    :param start_date: str, start date in format YYYY-MM-DD
    :param end_date: str, end date in format YYYY-MM-DD
    :return: Filtered dataframe for the specified period
    """
    if any((start_date < "2017-01-01", end_date > "2021-12-31", start_date > end_date)):
        raise ValueError(
            f"Invalid start_date/end_date argument. Dates have to fall in between 2017-01-01 and 2021-12-31. Instead got {start_date} and {end_date}."
        )
    return df.loc[start_date:end_date, :]


def convert_index_to_datetime(df: pd.DataFrame) -> None:
    """
    Convert dataframe index to datetime format in-place.

    :param df: pd.Dataframe, dataframe with string index to convert
    :return: None (modifies dataframe in-place)
    """
    df.index = pd.to_datetime(df.index)


def remove_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove columns with more than 50% missing values.

    :param df: pd.Dataframe, dataframe to clean
    :return: dataframe with sparse columns removed
    """
    threshold = int(df.shape[0] * 0.5)
    return df.dropna(axis=1, thresh=threshold)


def calculate_daily_traffic(df: pd.DataFrame) -> None:
    """
    Add total daily traffic column by summing all street traffic columns.

    :param df: pd.Dataframe, dataframe containing individual street traffic data
    :return: None (adds 'total_daily_traffic' column in-place)
    """
    df["total_daily_traffic"] = df[STREET_NAMES].sum(axis=1)


def preprocess_dataset(
    *dataframes: tuple[pd.DataFrame],
    start_date: str = "2017-01-01",
    end_date: str = "2021-12-31",
) -> pd.DataFrame:
    """
    Complete preprocessing pipeline for bike traffic datasets.

    :param dataframes: Tuple of dataframes to merge and preprocess
    :param start_date: str, start date for filtering (default: 2017-01-01)
    :param end_date: str, end date for filtering (default: 2021-12-31)
    :return: Fully preprocessed DataFrame ready for analysis
    """
    df = merge_datasets(dataframes)
    df = set_proper_values_types(df)
    df = remove_empty_columns(df)
    df = fill_nan_values_with_mean(df)
    df = get_proper_time_period(df, start_date, end_date)
    convert_index_to_datetime(df)
    calculate_daily_traffic(df)
    return df
