import glob

import pandas as pd
import pytest
from src.krakowbike.load_data import load_data


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({"street_a": [100, 150]}, index=["2023-01-01", "2023-01-02"])


def test_load_data(monkeypatch, sample_dataframe):
    def mock_glob(path: str):
        return ["file1.csv", "file2.csv"]

    def mock_read_csv(file_path: str, sep: str, index_col: str):
        return sample_dataframe

    monkeypatch.setattr(glob, "glob", mock_glob)
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    df = load_data("some/path", "file")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["street_a"]
    assert list(df.index) == ["2023-01-01", "2023-01-02", "2023-01-01", "2023-01-02"]
