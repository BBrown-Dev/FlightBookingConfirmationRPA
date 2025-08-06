# This module reads a CSV file into a DataFrame.

import pandas as pd
import logging
import psutil
import time
import gc
from typing import Any

logger = logging.getLogger(__name__)

def load_reservations(
    filepath: str,
    fill_value: str = "Unknown Passenger",
    **read_csv_kwargs: Any
) -> pd.DataFrame:
    """
    Load a flight reservations CSV, fill missing Passenger names,
    and log performance metrics (runtime, memory usage, row count).

    Parameters:
        filepath: Path to the CSV file.
        fill_value: Replacement for missing Passenger entries.
        **read_csv_kwargs: Additional arguments for pandas.read_csv.

    Returns:
        A pandas DataFrame with missing Passenger values filled.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        pd.errors.ParserError: If pandas fails to parse the file.
        KeyError: If the 'Passenger' column is missing.
    """
    # Capture start metrics
    proc = psutil.Process()
    mem_before = proc.memory_info().rss
    t0 = time.perf_counter()

    try:
        df = pd.read_csv(filepath, **read_csv_kwargs)
    except FileNotFoundError:
        logger.error("File not found: %s", filepath)
        raise
    except Exception as e:
        logger.exception("Failed to read %s: %s", filepath, e)
        raise

    if "Passenger" not in df.columns:
        logger.error("Required column 'Passenger' missing in %s", filepath)
        raise KeyError("Passenger column is required")

    # Vectorized fill
    missing_count = df["Passenger"].isna().sum()
    if missing_count:
        df["Passenger"] = df["Passenger"].fillna(fill_value)
        logger.info("Filled %d missing Passenger names", missing_count)

    # Final sanity check
    non_str = (df["Passenger"].map(type) != str).sum()
    if non_str:
        logger.warning("%d Passenger entries are not strings after fill", non_str)

    # Capture end metrics
    t1 = time.perf_counter()
    mem_after = proc.memory_info().rss
    runtime_s = t1 - t0
    mem_delta_mb = (mem_after - mem_before) / (1024 * 1024)

    logger.info(
        "load_reservations metrics — rows: %d | time: %.3fs | Δmem: %.2f MB",
        len(df), runtime_s, mem_delta_mb
    )

    # Clean up large temporary objects
    del proc, mem_before, mem_after, t0, t1
    gc.collect()

    return df