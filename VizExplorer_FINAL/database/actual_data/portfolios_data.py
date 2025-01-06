import pandas as pd
import random
from faker import Faker

# Load existing client IDs
clients_df = pd.read_csv("clients_table.csv")  # Ensure this file contains client_id
client_ids = clients_df["client_id"].tolist()

fake = Faker()

# Predefined portfolio types for more realistic naming
portfolio_types = [
    "Balanced Growth", 
    "High-Yield Income", 
    "Conservative Wealth Plan", 
    "Global Diversification", 
    "Dynamic Opportunities", 
    "Sustainable Investment"
]

# Function to generate random portfolio IDs
def generate_portfolio_id():
    return f"P{random.randint(100000, 999999)}"

# Generate portfolios for clients
portfolios = []
used_ids = set() 
for client_id in client_ids:
    num_portfolios = random.randint(1, 3)  # Each client can have 1-3 portfolios
    for _ in range(num_portfolios):
        portfolio_id = generate_portfolio_id()
        while portfolio_id in used_ids:  # Ensure the ID is unique
            portfolio_id = generate_portfolio_id()
        used_ids.add(portfolio_id)
        
        portfolio_type = random.choice(portfolio_types)
        portfolios.append({
            "portfolio_id": portfolio_id,
            "client_id": client_id,
            "portfolio_name": f"{portfolio_type} Portfolio",
            "total_value": round(random.uniform(50000, 1000000), 2),
            "currency": random.choice(["USD", "CHF", "EUR"]),
            "creation_date": fake.date_between(start_date="-10y", end_date="today")
        })

# Convert to DataFrame and save as CSV
portfolios_df = pd.DataFrame(portfolios)
portfolios_df.to_csv("portfolios_data.csv", index=False, encoding="utf-8")
print("Portfolio data saved to 'portfolios_data.csv'")
