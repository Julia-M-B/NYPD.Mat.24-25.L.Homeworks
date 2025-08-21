import glob
from functools import partial

import pandas as pd


def load_data(dir_path: str, dataset: str) -> pd.DataFrame:
    """
    Loading dataset
    :param dir_path:
    :param dataset:
    :return:
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
