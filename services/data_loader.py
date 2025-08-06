# This module reads a CSV file into a DataFrame.

import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_reservations(filepath):
    df = pd.read_csv(filepath)
    missing_number = df["Passenger"].isna().sum()

    if missing_number:
        logger.info(f"Filling {missing_number} missing passenger names")
    df["Passenger"].fillna("Unknown Passenger", inplace=True)
    return df
