import pandas as pd

from src.krakowbike.utils import STREET_NAMES

#########################################
# TODO complete functions' documentation
#########################################


def merge_datasets(*dataframes: tuple[pd.DataFrame]) -> pd.DataFrame:
    """

    :param dataframes:
    :return:
    """
    merged_df = pd.concat(list(*dataframes), axis=1)
    return merged_df.sort_index()


def set_proper_values_types(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
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

    :param df:
    :return:
    """
    means = df.mean()
    return df.fillna(means, axis=0)


def get_proper_time_period(
    df: pd.DataFrame, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Get the right period of time for data analysis.
    :param df: dataframe to be preprocessed
    :param start_date: string containing start date in format YYYY-MM-DD
    :param end_date: string containing end date in format YYYY-MM-DD
    :return:
    """
    if any((start_date < "2017-01-01", end_date > "2021-12-31", start_date > end_date)):
        raise ValueError(
            f"Invalid start_date/end_date argument. Dates have to fall in between 2017-01-01 and 2021-12-31. Instead got {start_date} and {end_date}."
        )
    return df.loc[start_date:end_date, :]


def convert_index_to_datetime(df: pd.DataFrame) -> None:
    df.index = pd.to_datetime(df.index)


def remove_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """
    threshold = int(df.shape[0] * 0.5)
    return df.dropna(axis=1, thresh=threshold)


def calculate_daily_traffic(df: pd.DataFrame) -> None:
    """

    :param df:
    :return:
    """
    df["total_daily_traffic"] = df[STREET_NAMES].sum(axis=1)


def preprocess_dataset(
    *dataframes: tuple[pd.DataFrame],
    start_date: str = "2017-01-01",
    end_date: str = "2021-12-31",
) -> pd.DataFrame:
    """

    :param dataframes:
    :param start_date:
    :param end_date:
    :return:
    """
    df = merge_datasets(dataframes)
    df = set_proper_values_types(df)
    df = remove_empty_columns(df)
    df = fill_nan_values_with_mean(df)
    df = get_proper_time_period(df, start_date, end_date)
    convert_index_to_datetime(df)
    calculate_daily_traffic(df)
    return df
