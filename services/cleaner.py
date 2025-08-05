# This module provides functions to clean and preprocess data in the DataFrame.

def drop_duplicates(df):
    # Removes duplicate rows across all columns.
    return df.drop_duplicates()
