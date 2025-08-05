# This script is the main point of entry and processes flight reservation data.

from services.data_loader import load_reservations
from services.transformer import convert_fares, add_total
from services.validator import validate_airports
from services.cleaner import drop_duplicates
from services.exporter import export_cleaned

def main():
    # Load the synthetic data
    df = load_reservations("data/generated_reservations.csv")

    # Transform fares
    df = convert_fares(df)

    # Add computed columns
    df = add_total(df, tax_rate=0.075)

    # Filter out invalid airports
    df = validate_airports(df)

    # Remove duplicate reservations
    df = drop_duplicates(df)

    # Export results
    export_cleaned(df, "output/cleaned_reservations.csv")

if __name__ == "__main__":
    main()
