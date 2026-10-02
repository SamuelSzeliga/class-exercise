import logging
from pathlib import Path
import re
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


def clean_text(value):
    """Normalize one text value."""

    value = value.strip()
    value = value.lower()
    value = re.sub(r"\s+", " ", value)
    return value


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""

    if column not in df.columns():
        logger.error(f"Column {column} not found")
        raise ValueError(f"Column {column} not found")

    before = len(df)

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - threshold * iqr
    upper = q3 + threshold * iqr
    df = df[(df["column"] >= lower) & (df["column"] <= upper)]
    rows_removed = before - len(df)

    logger.debug(f"Thresholf: {threshold}; {rows_removed} removed")
    return df