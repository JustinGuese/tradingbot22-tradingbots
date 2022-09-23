import pandas as pd
import yfinance as yf

# the biggest 10 stocks by market cap in 2000
# 1	Microsoft	United States	Software industry	Increase586,197
# 2	General Electric	United States	Conglomerate	Increase474,956
# 3	NTT Docomo	Japan	Telecommunications	Increase366,204
# 4	Cisco Systems	United States	Networking hardware	Increase348,965
# 5	Walmart	United States	Retail	Increase286,153
# 6	Intel	United States	Computer hardware	Increase277,096
# 7	Nippon Telegraph & Telephone	Japan	Telecommunications	Increase274,905
# 8	ExxonMobil	United States	Oil and gas	Increase265,894
# 9	Lucent	United States	Telecommunications	Increase237,668
# 10	Deutsche Telekom	Germany	Telecommunications	Increase209,628
STOCKS = ["MSFT", "GE", "CSCO", "WMT", "INTC", "NTTYY", "XOM", "DTEGY"]

data = yf.download(STOCKS, start="2000-01-01", end="2000-12-31")
data.head()

closes = data["Adj Close"]
closes.head()

# pyportfolio opt
import pandas as pd
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier

# Calculate expected returns and sample covariance

def getWeights(closes: pd.DataFrame):
    mu = expected_returns.mean_historical_return(closes)
    S = risk_models.sample_cov(closes)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    try:
        weights = ef.max_sharpe()
    except Exception:
        weights = ef.min_volatility()
    return weights
# ef.portfolio_performance(verbose=True)

# optimize every year
for year in range(2000, 2022):
    start = f"{year}-01-01"
    end = f"{year}-12-31"
    subcloses = closes.loc[start:end]
    subcloses = subcloses.fillna(method="bfill")
    mu = expected_returns.mean_historical_return(subcloses)
    S = risk_models.sample_cov(subcloses)

    # Optimize for maximal Sharpe ratio
    
    try:
        ef = EfficientFrontier(mu, S)
        weights = ef.max_sharpe()
    except Exception as e:
        ef = EfficientFrontier(mu, S)
        weights = ef.min_volatility()
    print(year, weights)
