from os import environ

import pandas as pd
from basebot22.basebot import BaseBot
from requests import get

bot = BaseBot("simple-analyst-rating-v1", backendurl = environ.get("BACKENDURL", "http://localhost:8000"))

# TODO: integrate this query 2 BaseBot
res = get(f"{bot.backendurl}/data/earnings/ratings/all")
if res.status_code != 200:
    raise Exception(f"Could not get ratings from backend: {res.text}")

res = res.json()
df = pd.DataFrame(res)
df = df.sort_values(by = "analyst_rating", ascending = True)
analyst_ratings = df["analyst_rating"]
mn, mx = analyst_ratings.min(), analyst_ratings.max()
x_scaled = (analyst_ratings - mx) / (mn - mx)
df["analyst_scaled"] = x_scaled.values / 2
df["analyst_scaled"] = df["analyst_scaled"] / df["analyst_scaled"].sum()

# onyl keep ticker and analyst_scaled
df = df[["ticker", "analyst_scaled"]]
print(df.head())

portfolio = bot.getPortfolio()
usd = portfolio["USD"]
# get total holding
PRICESTORE = dict()
def getPrice(ticker):
    if ticker in PRICESTORE:
        return PRICESTORE[ticker]
    else:
        PRICESTORE[ticker] = bot.getCurrentPrice(ticker)
        return PRICESTORE[ticker]

totalWorth = 0
for ticker, amount in portfolio.items():
    if ticker != "USD":
        totalWorth += amount * getPrice(ticker)
    else:
        totalWorth += amount

for i in range(len(df)):
    ticker = df.iloc[i]["ticker"]
    weight = df.iloc[i]["analyst_scaled"]
    currentHoldings = portfolio.get(ticker, 0)
    currentHoldings = currentHoldings * getPrice(ticker)
    targetHoldings = totalWorth * weight
    diffUsd = targetHoldings - currentHoldings
    if abs(diffUsd) > 30:
        
        if diffUsd > 0:
            print("buying %.2f$ of %s" % (diffUsd, ticker))
            bot.buy(ticker, diffUsd, amountInUSD = True)
        elif diffUsd < 0:
            print("selling %.2f$ of %s" % (-diffUsd, ticker))
            bot.sell(ticker, -diffUsd, amountInUSD = True)
    else:
        print("difference too small to act for %s. is: %.2f$" % (ticker, diffUsd))
