import yfinance as yf
import pandas as pd
import os
from datetime import datetime 

# List of tickers to download 
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META",
           "TSLA", "NVDA", "JPM", "UNH", "HD"]

# Set the start and end dates for historical data
START_DATE = "2018-01-01"
END_DATE = "2024-12-31"

# Directory to save raw CSVs
SAVE_DIR = "data/raw"

def download_and_save_data(ticker : str):
    """
    Downloads historical data for a single ticker and saves it as CSV.
    """

    try:
        print("Downloading the data for ticker:", ticker)
        df = yf.download(ticker , start=START_DATE, end=END_DATE)

        if not df.empty:
            df.reset_index(inplace = True)
            filename = os.path.join(SAVE_DIR, f"{ticker}.csv")
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        else:
            print(f"No data found for {ticker}")
    except Exception as e:
        print(f"Error in downloading {ticker} : {e}")

def download_all_tickers(tickers: list):
    """
    Loop through all tickers and download data.
    """
    os.makedirs(SAVE_DIR, exist_ok=True)

    for ticker in tickers:
        download_and_save_data(ticker)

if __name__ == "__main__":
    download_all_tickers(TICKERS)
 