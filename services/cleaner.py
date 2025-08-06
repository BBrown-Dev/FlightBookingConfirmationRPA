# This module provides functions to clean and preprocess data in the DataFrame.

import logging
import psutil
import time
from services.profiler import profile

# Get a module-specific logger
logger = logging.getLogger(__name__)

@profile
def drop_duplicates(df):
    """
    Removes duplicate rows based on PNR and logs metrics:
      - rows before/after
      - execution time
      - memory delta
    """
    proc = psutil.Process()
    mem_before = proc.memory_info().rss
    t0 = time.perf_counter()

    before = len(df)
    df = df.drop_duplicates(subset=["PNR"])
    removed = before - len(df)
    if removed:
        logger.info("Removed %d duplicate PNR records", removed)

    t1 = time.perf_counter()
    mem_after = proc.memory_info().rss

    logger.info(
        "drop_duplicates metrics — rows_before: %d, rows_after: %d, time: %.3fs, Δmem: %.2f MB",
        before,len(df),t1 - t0,(mem_after - mem_before) / (1024**2))

    return df