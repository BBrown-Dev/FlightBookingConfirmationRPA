### Data Assumptions

- Synthetic dataset simulates flight reservations with realistic fields.
- Airport codes are randomly selected from a valid list, with occasional invalid entries.
- Passenger names are generated using the Faker library.
- Fare values range from $100 to $1000, with some entries containing invalid types or missing values.
- Status values include Confirmed, Cancelled, and Pending.

### Edge Cases Introduced

- Missing `Fare` and `Passenger` fields to simulate incomplete data.
- Duplicate records to test deduplication logic.
- Invalid airport codes to test validation routines.
- Incorrect data types in `Fare` to test type-checking and conversion logic.
