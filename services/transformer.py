# This module contains functions to transform the DataFrame.
from venv import logger
import pandas as pd


def convert_fares(df):
    # Converts Fare column to float.
    df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce")
    invalid_number = df["Fare"].isna().sum()

    if invalid_number:
        logger.warning(f"{invalid_number} invalid fares coerced to NaN")
    df["Fare"].fillna(df["Fare"].median(), inplace=True)
    return df

def add_total(df, tax_rate):
    # Adds a Total column as Fare + tax.
    df["Total"] = df["Fare"] * (1 + tax_rate)
    return df
