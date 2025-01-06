import pandas as pd
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

# Load clients_data_with_id.csv
clients_data = pd.read_csv("clients_table.csv")

unique_account_ids = set()

def generate_unique_account_id():
    while True:
        # Generate a random account ID (one letter + six digits)
        account_id = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100000, 999999)}"
        if account_id not in unique_account_ids:
            unique_account_ids.add(account_id)
            return account_id
        
# Generate accounts data
accounts = []
for _, client in clients_data.iterrows():
    client_id = client['client_id']
    date_of_birth = pd.to_datetime(client['date_of_birth'])

    # Ensure the client is at least 18 years old before account creation
    min_creation_date = date_of_birth + timedelta(days=18 * 365)
    for _ in range(random.randint(1, 3)):  # Each client can have 1-3 accounts
        accounts.append({
            "account_id": generate_unique_account_id(),  
            "client_id": client_id,
            "account_type": random.choice(["savings", "checking", "brokerage"]),
            "balance": round(random.uniform(1000, 100000), 2),
            "creation_date": fake.date_between(start_date=min_creation_date, end_date="today"),
            "currency": "CHF"
        })

# Save to CSV
accounts_df = pd.DataFrame(accounts)
accounts_df.to_csv("accounts_data.csv", index=False, encoding="utf-8")
print("accounts_data.csv saved successfully.")
