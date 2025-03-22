import yfinance as yf
import pandas as pd

class Stock_Data:
    def __init__(self, ticker, price):
        self.ticker = ticker
        self.price = price

    def get_stock_data(tickers, start_date, end_date):
        stock_data_frame = yf.download(tickers, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        stock_closing_price_history = stock_data_frame['Close']
        cleaned_stock_data = stock_closing_price_history.dropna()
        return cleaned_stock_data

    def time_period_filter(cleaned_stock_data, rebal_period):
    # rebal_period should be handled in the front end with the following options:
    # Monthly - '1ME'
    # Quarterly - '3ME'
    # Semiannual - '6ME'
    # Annual - '12ME'
    df=cleaned_stock_data
    df['date_column'] = pd.to_datetime(df.index)
    df = df.set_index('date_column')
    df_last_day = df.resample(rebal_period).apply(lambda x: x.iloc[-1])
    df_last_day = df_last_day.reset_index()
    return df_last_day
