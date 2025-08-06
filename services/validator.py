# This module validates flight data records based on airport codes.
import logging

# get a module-specific logger
logger = logging.getLogger(__name__)

VALID_AIRPORTS = {"LAX", "JFK", "ORD", "ATL", "DFW", "DEN", "SFO", "SEA", "MIA", "PHX"}

def validate_airports(df):
    # Drops records with invalid airports
    invalid_origins = set(df["Origin"]) - VALID_AIRPORTS
    invalid_destinations = set(df["Destination"]) - VALID_AIRPORTS

    if invalid_origins or invalid_destinations:
        logger.error("Invalid Origins: %s, Destinations: %s", invalid_origins, invalid_destinations)

    return df[
        df["Origin"].isin(VALID_AIRPORTS) &
        df["Destination"].isin(VALID_AIRPORTS)
        ].copy()