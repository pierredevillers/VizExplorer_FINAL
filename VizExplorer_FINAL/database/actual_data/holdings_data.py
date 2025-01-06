import pandas as pd
import random

# Load existing portfolio and stock/ETF data
portfolios_df = pd.read_csv("portfolios_data.csv")  # Ensure this file contains portfolio_id
stocks_df = pd.read_csv("historical_stock_data.csv")  # Contains tickers for stocks
etfs_df = pd.read_csv("etfs_historical_data.csv")  # Contains tickers for ETFs

# Combine tickers from stocks and ETFs
all_tickers = pd.concat([stocks_df["ticker"], etfs_df["ticker"]]).tolist()

# Generate holdings for each portfolio
holdings = []
holding_id_counter = 1  # Start ID counter
for _, portfolio in portfolios_df.iterrows():
    num_holdings = random.randint(3, 10)  # Each portfolio has 3-10 holdings
    for _ in range(num_holdings):
        ticker = random.choice(all_tickers)
        quantity = round(random.uniform(10, 1000), 2)  # Random quantity of shares
        purchase_price = round(random.uniform(50, 500), 2)  # Purchase price per unit
        current_value = round(quantity * random.uniform(50, 500), 2)  # Current value

        holdings.append({
            "holding_id": f"H{holding_id_counter:06d}",  # Generate unique ID, e.g., "H000001"
            "portfolio_id": portfolio["portfolio_id"],
            "ticker": ticker,
            "quantity": quantity,
            "purchase_price": purchase_price,
            "current_value": current_value
        })
        holding_id_counter += 1  # Increment the counter

# Convert to DataFrame and save as CSV
holdings_df = pd.DataFrame(holdings)
holdings_df.to_csv("holdings_data.csv", index=False, encoding="utf-8")
print("Holdings data saved to 'holdings_data.csv'")
