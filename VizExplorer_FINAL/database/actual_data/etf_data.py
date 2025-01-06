import requests
import pandas as pd
from datetime import datetime, timedelta

# Replace with your FMP API key
API_KEY = "LKU2cJAL44h5tsPdhkmQp7lg5gMijmnj"

# List of ETF symbols to fetch data for
etf_metadata = {
    "CHSPI": "UBS ETF (Swiss Performance Index)",
    "CSNDX": "Credit Suisse Bond Index Fund",
    "EUNL": "iShares Core MSCI Europe ETF",
    "SPY": "SPDR S&P 500 ETF Trust",
    "IVV": "iShares Core S&P 500 ETF",
    "VTI": "Vanguard Total Stock Market ETF"
}

# Set the start date for fetching data (3 years back)
end_date = datetime.now()
start_date = end_date - timedelta(days=3*365)

# Data storage
etf_data = []

# Fetch data for each ETF
for symbol, name in etf_metadata.items():
    print(f"Fetching data for {symbol}...")
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        historical_data = data.get("historical", [])
        
        for record in historical_data:
            record_date = datetime.strptime(record["date"], "%Y-%m-%d")
            
            # Only include data within the last 3 years
            if start_date <= record_date <= end_date:
                etf_data.append({
                    "ticker": symbol,
                    "name": name, 
                    "date": record["date"],
                    "open": record["open"],
                    "high": record["high"],
                    "low": record["low"],
                    "close": record["close"],
                    "volume": record["volume"]
                })
    else:
        print(f"Failed to fetch data for {symbol}: {response.status_code}")

# Convert to DataFrame
etf_df = pd.DataFrame(etf_data)

# Save to CSV
etf_df.to_csv("etfs_historical_data.csv", index=False, encoding="utf-8")
print("ETF historical data saved to 'etfs_data.csv'")
