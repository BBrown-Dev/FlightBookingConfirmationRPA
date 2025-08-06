# This module provides functions to clean and preprocess data in the DataFrame.

import logging
import psutil
import time
import cProfile
import pstats
import io
from datetime import datetime

# Get a module-specific logger
logger = logging.getLogger(__name__)

# Profiling decorator to capture performance metrics
def profile(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()

        # Dump raw stats
        prof_file = f"profile_{func.__name__}_{datetime.now():%Y%m%d_%H%M%S}.prof"
        pr.dump_stats(prof_file)

        # Write top 20 to txt
        s = io.StringIO()
        stats = pstats.Stats(pr, stream=s).sort_stats("cumtime")
        stats.print_stats(20)
        txt_file = f"{func.__name__}_stats_{datetime.now():%Y%m%d_%H%M%S}.txt"

        with open(txt_file, "w") as f:
            f.write(s.getvalue())
            return result

    return wrapper

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