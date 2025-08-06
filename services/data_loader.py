# This module reads a CSV file into a DataFrame.

import pandas as pd
import logging

# get a module-specific logger
logger = logging.getLogger(__name__)

def load_reservations(filepath):
    df = pd.read_csv(filepath)
    missing_number = df["Passenger"].isna().sum()

    if missing_number:
        logger.info("Filling %d missing Passenger names", missing_number)
    df["Passenger"].fillna("Unknown Passenger", inplace=True)
    return df
