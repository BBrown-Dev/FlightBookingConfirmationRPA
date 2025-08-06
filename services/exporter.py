# This module provides functionality to export cleaned data to a CSV file.

import logging
import os
import time
import psutil
import gc
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
def export_cleaned(df, output_path):
    """
    Writes the cleaned DataFrame to CSV and logs metrics:
      - row count
      - execution time
      - memory before/after (MB)
    Releases memory after export.
    """
    proc = psutil.Process()
    mem_before = proc.memory_info().rss
    t0 = time.perf_counter()

    # Ensure directory exists and write CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Exported cleaned data to %s", output_path)

    t1 = time.perf_counter()
    mem_after = proc.memory_info().rss

    # Log performance metrics
    logger.info(
        "export_cleaned metrics — rows: %d, time: %.3fs, Δmem: %.2f MB",
        len(df),t1 - t0,(mem_after - mem_before) / 1024**2)

    # Release memory held by DataFrame
    del df
    gc.collect()