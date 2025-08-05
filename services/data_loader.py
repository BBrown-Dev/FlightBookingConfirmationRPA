# This module reads a CSV file into a DataFrame.

import pandas as pd

def load_reservations(filepath):

    return pd.read_csv(filepath)
