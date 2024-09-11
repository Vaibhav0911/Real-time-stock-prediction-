import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period='2y', interval='1d'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    data.reset_index(inplace=True)
    return data

def create_features(df):
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['RSI'] = compute_rsi(df['Close'])
    df.dropna(inplace=True)  # Remove rows with NaN values after rolling operations
    return df

def compute_rsi(series, period=14):
    delta = series.diff(1)
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

if __name__ == "__main__":
    df = fetch_stock_data('AAPL')
    df = create_features(df)
    df.to_csv('data/AAPL.csv', index=False)

