import numpy as np
from sklearn.neighbors import KernelDensity
import pandas as pd
from datetime import timedelta



def generate_kde(df,n_rolling=40):
    std = df['pct_change'].rolling(n_rolling).std().iloc[-1]
    q25, q75 = np.percentile(df['pct_change'], [25,75])
    iqr = q75 - q25

    # best bandwidth estimator from Density Estimator for Statistics and Data Analysis pag 47
    A = min(std, iqr / 1.34)
    h = 0.9 * A * len(df)**(-1/5)

    kde = KernelDensity(kernel='tophat',bandwidth=h).fit(df['pct_change'].values.reshape(-1,1))
    last_price = df.Close.iloc[-1]
    return kde, last_price

def generate_path(df, n_days, n_rolling=40):
    
    forecast_date = pd.bdate_range(df['Date'].iloc[-1], df['Date'].iloc[-1] + timedelta(days = n_days))[1:]

    kde, last_price = generate_kde(df, n_rolling = 40)
    path = 1 + kde.sample(len(forecast_date)-1)
    
    forecast = np.hstack((np.array(last_price), path.cumprod() * last_price))

    return pd.DataFrame( forecast, columns=['Close']).set_index(forecast_date)

def generate_path_date(df, expiration_date, n_rolling=40):
    
    forecast_date = pd.bdate_range(df['Date'].iloc[-1], expiration_date)

    kde, last_price = generate_kde(df, n_rolling = 40)
    path = 1 + kde.sample(len(forecast_date)-1)
    
    forecast = np.hstack((np.array(last_price), path.cumprod() * last_price))

    return pd.DataFrame( forecast, columns=['Close']).set_index(forecast_date)


