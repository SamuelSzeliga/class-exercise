import logging
from pathlib import Path

import pandas as pd

data_path = Path("data") / "messy_netflix_titles.csv"
df = pd.read_csv(data_path)

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""

    logger.debug(f"{df.shape}")
    print(f"Shape: {df.shape}")
    print(f"First five rows: ")
    print(df.head())
    print(f"Columns {df.columns}")
    print(df.dtypes())



def remove_duplicates(df):
    """Remove exact duplicate rows."""

    before = df.copy()
    df = df.drop_duplicates()
    logger.debug(f"Before: {len(before)}, after: {len(df)}")
    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""

    before = df.copy()
    df = df.dropna()
    logger.debug(f"Before: {len(before)}, after: {len(df)}")
    return df