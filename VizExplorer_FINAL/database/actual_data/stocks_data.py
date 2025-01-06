import requests
import csv
import datetime

# StockData.org API Token
API_TOKEN = "WQcniszLe8G08PI4cjIzAT8gofiLnCahdrKoKxyR"  # Replace with your actual API token

# Base URL for the historical data endpoint
BASE_URL = "https://api.stockdata.org/v1/data/eod"

# List of stock tickers to fetch data for
stock_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]

# Output CSV file
output_file = "historical_stock_data.csv"

# Define start and end dates
end_date = datetime.datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.datetime.now() - datetime.timedelta(days=3*365)).strftime("%Y-%m-%d")  # Approx. 3 years

# Fetch data for a single ticker, handling pagination
def fetch_data_with_pagination(ticker, start_date, end_date):
    all_data = []
    current_start_date = start_date

    while current_start_date <= end_date:
        # Set the chunk end date (180 days per request as per documentation)
        current_end_date = (datetime.datetime.strptime(current_start_date, "%Y-%m-%d") + datetime.timedelta(days=180)).strftime("%Y-%m-%d")
        if current_end_date > end_date:
            current_end_date = end_date

        # API parameters
        params = {
            "symbols": ticker,
            "api_token": API_TOKEN,
            "date_from": current_start_date,
            "date_to": current_end_date,
            "format": "json",
            "interval": "day",  # Daily interval
            "sort": "asc",  # Sort by ascending date
        }

        # Fetch data
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json().get("data", [])
            all_data.extend(data)
            print(f"Fetched {len(data)} records for {ticker} from {current_start_date} to {current_end_date}.")
        else:
            print(f"Error fetching data for {ticker} from {current_start_date} to {current_end_date}: {response.status_code}")
            break

        # Update start date for the next chunk
        current_start_date = (datetime.datetime.strptime(current_end_date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    return all_data

# Save data to a CSV file
def save_to_csv(data, file_name):
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["ticker", "date", "open", "high", "low", "close", "volume"])
        # Write the data rows
        for record in data:
            writer.writerow([
                record.get("ticker"),
                record.get("date"),
                record.get("open"),
                record.get("high"),
                record.get("low"),
                record.get("close"),
                record.get("volume"),
            ])

# Main function to fetch and save data for multiple tickers
def main():
    all_data = []
    for ticker in stock_tickers:
        print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
        ticker_data = fetch_data_with_pagination(ticker, start_date, end_date)
        # Add ticker info to each record
        for record in ticker_data:
            record["ticker"] = ticker
        all_data.extend(ticker_data)

    # Save all data to CSV if available
    if all_data:
        save_to_csv(all_data, output_file)
        print(f"Data saved to {output_file}")
    else:
        print("No data fetched.")

# Run the script
if __name__ == "__main__":
    main()
