import glob
from functools import partial

import pandas as pd


def load_data(dir_path: str, dataset: str) -> pd.DataFrame:
    """
    Load and concatenate CSV files matching a dataset pattern from a directory.

    Searches for CSV files containing the specified dataset name in the filename,
    loads them with 'Data' column as index, and concatenates them into a single
    DataFrame.

    :param dir_path: str, path to the directory containing CSV files to load.
    :param dataset: str, pattern to match in filenames.
    :return: pd.DataFrame, concatenated DataFrame from all matching CSV files,
             with 'Data' column as index.
    """
    fpaths = glob.glob(f"{dir_path}/*{dataset}*")
    returned_df = pd.concat(
        [pd.read_csv(file_path, sep=",", index_col="Data") for file_path in fpaths],
        axis=0,
    )
    return returned_df


load_bike_data = partial(load_data, dataset="rowery")
load_weather_data = partial(load_data, dataset="pogoda")
load_air_data = partial(load_data, dataset="powietrze")
