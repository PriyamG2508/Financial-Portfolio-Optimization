import numpy as np
import yfinance as yf
import pandas as pd 
from datetime import datetime
import os 

class FinancialDataCollector:
    def __init__(self, ticker, start_date, end_date=None):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date if end_date else datetime.today().strftime('%Y-%m-%d')
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def collect_stock_data(self, tickers):
        """
        Collect historical data for specified tickers
        """
        print(f"Collecting data for {len(tickers)} assets from {self.start_date} to {self.end_date}")

        # Download data
        data = yf.download(tickers, start=self.start_date, end=self.end_date)

        # Save raw data
        data.to_csv(os.path.join(self.data_dir, 'raw_price_data.csv'))

        # Process and return adjusted close prices
        adj_close = data['Adj Close']
        adj_close.to_csv(os.path.join(self.data_dir, 'adj_close_prices.csv'))
        
        print(f"Data collection complete. Shape: {adj_close.shape}")
        return adj_close
    
    def calculate_returns(self, prices, return_type='simple'):
        """
        Calculate return from price data
        """
        if return_type == 'simple':
            returns = prices.pct_change().dropna()
        elif return_type == 'log':
            returns = np.log(prices / prices.shift(1)).dropna()
        else:
            raise ValueError("Invalid return type. Choose 'simple' or 'log'")
        
        returns.to_csv(os.path.join(self.data_dir, f'{return_type}_returns.csv'))
        print(f"Calculated {return_type} returns. Shape: {returns.shape}")
        return returns
