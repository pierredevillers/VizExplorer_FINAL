import pandas as pd
import random
from faker import Faker

fake = Faker()

# Load accounts.csv and clients_data_with_id.csv
accounts_data = pd.read_csv("accounts_data.csv")
clients_data = pd.read_csv("clients_table.csv")
unique_transaction_ids = set()


def generate_unique_transaction_id():
    while True:
        # Generate an 8-digit transaction ID
        transaction_id = f"{random.randint(10000000, 99999999)}"
        if transaction_id not in unique_transaction_ids:
            unique_transaction_ids.add(transaction_id)
            return transaction_id
        
# Generate transactions data
transactions = []
for _, account in accounts_data.iterrows():
    account_id = account["account_id"]
    client_id = account["client_id"]
    currency = account["currency"]  # Get currency from the account

    for _ in range(random.randint(5, 20)):  # Each account can have 5-20 transactions
        transaction_type = random.choice(["deposit", "withdrawal", "buy", "sell"])
        stock_ticker = random.choice(["AAPL", "MSFT", "GOOGL", "TSLA", None]) if transaction_type in ["buy", "sell"] else None
        
        transactions.append({
            "transaction_id": generate_unique_transaction_id(),  # Auto-increment in PostgreSQL
            "client_id": client_id,  # Link to client
            "account_id": account_id,  # Link to account
            "transaction_date": fake.date_time_between(start_date="-2y", end_date="now"),
            "transaction_type": transaction_type,
            "amount": round(random.uniform(10, 5000), 2),
            "stock_ticker": stock_ticker,
            "currency": currency  # Include currency
        })

# Save to CSV
transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv("transactions_data.csv", index=False, encoding="utf-8")

print("transactions_data.csv saved successfully.")
