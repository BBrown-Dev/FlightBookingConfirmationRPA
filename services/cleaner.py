# This module provides functions to clean and preprocess data in the DataFrame.

import logging

logger = logging.getLogger(__name__)

def drop_duplicates(df):
    # Removes duplicate rows across all columns.
    before = len(df)
    df = df.drop_duplicates(subset=["PNR"])
    removed = before - len(df)

    if removed:
        logger.info(f"Removed {removed} duplicate PNR records")

    return df