import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "8fe61d1ab09c4b558b0d78bef77a68f6"  
tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
languages = ["en", "de", "fr"]

end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=3*365)).strftime("%Y-%m-%d")

news_data = []

for ticker in tickers:
    for language in languages:
        page = 1
        while True:
            url = f"https://newsapi.org/v2/everything?q={ticker}&language={language}&from={start_date}&to={end_date}&page={page}&apiKey={API_KEY}"
            response = requests.get(url)
            
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                if not articles:  # Stop if no more articles
                    break
                
                for article in articles:
                    news_data.append({
                        "ticker": ticker,
                        "headline": article["title"],
                        "source": article["source"]["name"],
                        "publish_date": article["publishedAt"],
                        "url": article["url"],
                        "language": language
                    })
                page += 1  # Go to the next page
            else:
                print(f"Error fetching news for {ticker} in {language}: {response.status_code}")
                break

# Save news data to CSV
news_df = pd.DataFrame(news_data)
news_df.to_csv("market_news_data.csv", index=False)

print("Historical Market news data saved to CSV.")
