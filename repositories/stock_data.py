import yfinance as yf

class Stock_Data:
    def __init__(self, ticker, price):
        self.ticker = ticker
        self.price = price

    def get_stock_data(tickers, start_date, end_date):
        stock_data_frame = yf.download(tickers, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        stock_closing_price_history = stock_data_frame['Close']
        cleaned_stock_data = stock_closing_price_history.dropna()
        return cleaned_stock_data