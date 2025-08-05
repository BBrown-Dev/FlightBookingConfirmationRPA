import pandas as pd
import random
from faker import Faker

fake = Faker()
airport_codes = ['LAX', 'JFK', 'ORD', 'ATL', 'DFW', 'DEN', 'SFO', 'SEA', 'MIA', 'PHX']
statuses = ['Confirmed', 'Cancelled', 'Pending']
invalid_airports = ['XXX', 'ZZZ', '123']

def generate_reservation(index):
    return {
        'PNR': f"PNR{1000 + index}",
        'Passenger': fake.name(),
        'Origin': random.choice(airport_codes + invalid_airports if index % 20 == 0 else airport_codes),
        'Destination': random.choice(airport_codes),
        'Fare': random.choice([round(random.uniform(100, 1000), 2), 'N/A'] if index % 15 == 0 else [round(random.uniform(100, 1000), 2)]),
        'Status': random.choice(statuses),
    }

# Generate 200 records
data = [generate_reservation(i) for i in range(200)]

# Introduce duplicates
data += [data[5], data[42]]

# Introduce missing values
data[10]['Fare'] = None
data[25]['Passenger'] = None

df = pd.DataFrame(data)
df.to_csv('reservations.csv', index=False)
