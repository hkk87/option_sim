import yfinance as yf

def get_price(ticker, period, interval, start = None, end = None):
    ticker = yf.Ticker(ticker)
    df = ticker.history(period, interval,start,end)
    df['pct_change'] = df['Close'].pct_change()
    df.dropna(inplace=True)
    df.drop(labels=['Dividends','Stock Splits'], axis=1, inplace=True)
    
    return df

def change_float(x):
    try:
        return float(x)
    except:
        return x