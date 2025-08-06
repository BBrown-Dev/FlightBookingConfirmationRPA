# This module validates flight data records based on airport codes.

import logging
import time
import psutil
import gc
import cProfile
import pstats
import io
from datetime import datetime

# Get a module-specific logger
logger = logging.getLogger(__name__)

VALID_AIRPORTS = {"LAX", "JFK", "ORD", "ATL", "DFW", "DEN", "SFO", "SEA", "MIA", "PHX"}

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
def validate_airports(df):
    """
    Drops records with invalid airports, logs errors and performance metrics:
      - invalid origin/destination sets
      - rows before/after
      - execution time
      - memory delta
    Releases memory held by the original DataFrame.
    """
    proc = psutil.Process()
    mem_before = proc.memory_info().rss
    t0 = time.perf_counter()
    rows_before = len(df)

    invalid_origins = set(df["Origin"]) - VALID_AIRPORTS
    invalid_destinations = set(df["Destination"]) - VALID_AIRPORTS

    if invalid_origins or invalid_destinations:
        logger.error("Invalid Origins: %s, Destinations: %s",invalid_origins, invalid_destinations)

    valid_df = df[
        df["Origin"].isin(VALID_AIRPORTS) &
        df["Destination"].isin(VALID_AIRPORTS)
    ].copy()
    rows_after = len(valid_df)
    removed = rows_before - rows_after

    t1 = time.perf_counter()
    mem_after = proc.memory_info().rss

    logger.info("validate_airports metrics — rows_before: %d, rows_after: %d, "
                "removed: %d, time: %.3fs, Δmem: %.2f MB",rows_before,rows_after,removed,
                t1 - t0,(mem_after - mem_before) / 1024**2)

    # Release memory held by the original DataFrame
    del df
    gc.collect()

    return valid_df