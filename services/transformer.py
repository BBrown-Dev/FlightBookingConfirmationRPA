# This module contains functions to transform the DataFrame.

import pandas as pd
import logging
import psutil
import time
import gc
from services.profiler import profile

# Get a module-specific logger
logger = logging.getLogger(__name__)

@profile
def convert_fares(df):
    # Start metrics
    proc = psutil.Process()
    mem_before = proc.memory_info().rss
    t0 = time.perf_counter()

    # Converts Fare column to float.
    df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce")
    invalid_number = df["Fare"].isna().sum()

    if invalid_number:
        logger.warning("%d invalid fares coerced to NaN", invalid_number)
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())

    # End metrics
    t1 = time.perf_counter()
    mem_after = proc.memory_info().rss
    logger.info("convert_fares — rows: %d, time: %.3fs, Δmem: %.2fMB",len(df),
                t1 - t0,(mem_after - mem_before) / (1024 ** 2))

    # Release temp objects
    del proc, mem_before, mem_after, t0, t1
    gc.collect()

    return df

@profile
def add_total(df, tax_rate):
    # Start metrics
    proc = psutil.Process()
    mem_before = proc.memory_info().rss
    t0 = time.perf_counter()

    # Adds a Total column as Fare + tax.
    df["Total"] = df["Fare"] * (1 + tax_rate)

    # End metrics
    t1 = time.perf_counter()
    mem_after = proc.memory_info().rss
    logger.info("add_total — rows: %d, time: %.3fs, Δmem: %.2fMB",len(df),
                t1 - t0,(mem_after - mem_before) / (1024 ** 2))

    # Release temp objects
    del proc, mem_before, mem_after, t0, t1
    gc.collect()

    return df
