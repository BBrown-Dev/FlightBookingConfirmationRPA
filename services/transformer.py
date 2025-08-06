# This module contains functions to transform the DataFrame.

import pandas as pd
import logging

# get a module-specific logger
logger = logging.getLogger(__name__)

def convert_fares(df):
    # Converts Fare column to float.
    df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce")
    invalid_number = df["Fare"].isna().sum()

    if invalid_number:
        logger.warning("%d invalid fares coerced to NaN", invalid_number)
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    return df

def add_total(df, tax_rate):
    # Adds a Total column as Fare + tax.
    df["Total"] = df["Fare"] * (1 + tax_rate)
    return df
