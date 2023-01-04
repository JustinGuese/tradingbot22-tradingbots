from datetime import datetime, timedelta

import pandas as pd
from basebot22.basebot import BaseBot

bot = BaseBot("simplesma-v1", backendurl = "http://tradingbot-baseimage-service:8000")

weights = pd.read_csv("smaweights.csv", index_col=0)
weightsTslaFix = pd.read_csv("smaweights-tslareduced.csv", index_col=0)

smavals = pd.read_csv("smabest.csv", index_col=0)

toBuy = []
toSell = []
portfolio = bot.getPortfolio()
for ticker, (money,nrTrades,tradeWinsMedian,smallSMA,bigSMA) in smavals.iterrows():
    data = bot.getData(ticker, start_date = datetime.now() - timedelta(days=int(max([smallSMA,bigSMA])*2)))
    data["smallSMA"] = data["adj_close"].rolling(int(smallSMA)).mean()
    data["bigSMA"] = data["adj_close"].rolling(int(bigSMA)).mean()
    # did we have a cross in the last 3 days?
    crossUp = any(data.iloc[-2:]["smallSMA"] > data.iloc[-2:]["bigSMA"])
    crossDown = any(data.iloc[-2:]["smallSMA"] < data.iloc[-2:]["bigSMA"])
    
    holdingNr = portfolio.get(ticker, 0)
    
    if crossUp and holdingNr == 0:
        print(f"upcross {ticker}")
        toBuy.append(ticker)
    elif crossDown and holdingNr > 0:
        print(f"downcross {ticker}")
        toSell.append(ticker)
    
if len(toSell) > 0:
    # first sell to get cash
    for ticker in toSell:
        print("selling all bc of downcross: ", ticker)
        bot.sell(ticker)
    portfolio = bot.getPortfolio()
if len(toBuy) > 0:
    # then buy
    cash = portfolio.get("USD", 0)
    for ticker in toBuy:
        weight = weights.loc[ticker, "money"] # money is actually weight 0.31 and so on
        if cash * weight > 50:
            print("buying with weight: ", ticker, weight)
            bot.buy(ticker, cash * weight, amountInUSD = True)
        
# do the same for the weighted tsla
if len(toSell) > 0 or len(toBuy) > 0:
    bot = BaseBot("simplesma-tslareduced-v1", backendurl = "http://tradingbot-baseimage-service:8000")
    print("same for tsla reduced bot")
    if len(toSell) > 0:
        # first sell to get cash
        for ticker in toSell:
            print("selling all bc of downcross: ", ticker)
            bot.sell(ticker)
        portfolio = bot.getPortfolio()
    if len(toBuy) > 0:
        # then buy
        cash = portfolio.get("USD", 0)
        for ticker in toBuy:
            weight = weightsTslaFix.loc[ticker, "money"] # money is actually weight 0.31 and so on
            if cash * weight > 50:
                print("buying with weight: ", ticker, weight)
                bot.buy(ticker, cash * weight, amountInUSD = True)