import os
import pandas as pd

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
OUTPUT_FILE = "returns.csv"

def calculate_daily_returns(file_path, ticker):
    """
    Loads a CSV and calculates daily return from the 'Close' price.
    """
    df = pd.read_csv(file_path, parse_dates=['Date'])
    df.sort_values('Date', inplace=True)

    # Force 'Close' column to numeric (if not already), coerce errors
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # Drop rows where Close is NaN
    df.dropna(subset=['Close'], inplace=True)

    # Calculate daily returns
    df['Daily Return'] = df['Close'].pct_change()

    # Drop NaNs from first row (after pct_change)
    df.dropna(subset=['Daily Return'], inplace=True)

    return df[['Date', 'Daily Return']].rename(columns={'Daily Return': ticker})


def build_returns_dataset():
    """
    Loops through all raw CSVs and builds a master returns DataFrame.
    """
    all_returns = []

    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv"):
            ticker = file.replace(".csv", "")
            file_path = os.path.join(RAW_DIR, file)
            print(f"Processing {ticker}...")

            try:
                returns = calculate_daily_returns(file_path, ticker)
                all_returns.append(returns)
            except Exception as e:
                print(f"Skipping {ticker} due to error: {e}")

    # Merge all on Date
    df_merged = all_returns[0]
    for df in all_returns[1:]:
        df_merged = pd.merge(df_merged, df, on='Date', how='outer')

    df_merged.sort_values("Date", inplace=True)
    df_merged.set_index("Date", inplace=True)

    # Save to CSV
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    output_path = os.path.join(PROCESSED_DIR, OUTPUT_FILE)
    df_merged.to_csv(output_path)

    print(f"\n Saved combined returns data to {output_path}")

if __name__ == "__main__":
    build_returns_dataset()
