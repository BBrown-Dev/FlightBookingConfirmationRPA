# This module validates flight data records based on airport codes.

VALID_AIRPORTS = {"LAX", "JFK", "ORD", "ATL", "DFW", "DEN", "SFO", "SEA", "MIA", "PHX"}

def validate_airports(df):
    # Drops records with invalid airports
    return df[
        df["Origin"].isin(VALID_AIRPORTS) &
        df["Destination"].isin(VALID_AIRPORTS)
    ]
