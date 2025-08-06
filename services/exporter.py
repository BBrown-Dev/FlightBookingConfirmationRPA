# This module provides functionality to export cleaned data to a CSV file.

import logging
import os
import time
import psutil
import gc
from services.profiler import profile

# Get a module-specific logger
logger = logging.getLogger(__name__)

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