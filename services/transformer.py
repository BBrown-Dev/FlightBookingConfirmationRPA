# This module contains functions to transform the DataFrame.

def convert_fares(df):
    # Converts Fare column to float.
    df["Fare"] = df["Fare"].astype(float)
    return df

def add_total(df, tax_rate):
    # Adds a Total column as Fare + tax.
    df["Total"] = df["Fare"] * (1 + tax_rate)
    return df
