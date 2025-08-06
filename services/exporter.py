# This module provides functionality to export cleaned data to a CSV file.

import logging
import os

# get a module-specific logger
logger = logging.getLogger(__name__)

def export_cleaned(df, output_path):
    # Write DataFrame to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Exported cleaned data to %s", output_path)