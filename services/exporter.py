# This module provides functionality to export cleaned data to a CSV file.

def export_cleaned(df, output_path):
    # Write DataFrame to CSV
    df.to_csv(output_path, index=False)
