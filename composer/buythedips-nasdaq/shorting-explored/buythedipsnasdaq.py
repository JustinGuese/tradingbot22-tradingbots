from datetime import datetime, timedelta

# further adapted, see notebook jupyternotebooks/composer-buythedrip.ipynb
from basebot22.basebot import BaseBot

# basic setup
bot = BaseBot("composer-buydipsqqq-shorting-explored", backendurl = "http://tradingbot-baseimage-service:8000") # backendurl = "http://tradingbot-baseimage-service:8000"

def switchPair(tickerWanted):
    portfolio = bot.getPortfolio()
    if tickerWanted == "TQQQ":
        TOSELL = "SQQQ"
        TOBUY = "TQQQ"
    elif tickerWanted == "SQQQ":
        TOSELL = "TQQQ"
        TOBUY = "SQQQ"
    else:
        raise ValueError("tickerWanted must be either TQQQ or sqqq")
    tosell = portfolio.get(TOSELL, 0)
    if tosell > 0:
        print("selling all ", TOSELL)
        bot.sell(TOSELL)
        portfolio = bot.getPortfolio() # refresh
    usd = portfolio.get("USD", 0)
    if usd > 50:
        print("buying %s with USD: " % TOBUY, usd)
        bot.buy(TOBUY, amount = usd, amountInUSD=True)
    else:
        print("not enough cash or already holding %s" % TOBUY)


# 
qqq = bot.getData("QQQ", start_date = datetime.now() - timedelta(days=100))

# explored in notebook: use cum sum return with lookback 1, and threshold
lookback = 1
threshold = 0.7842105263157895

qqq["cumulative_5d_return"] = qqq["adj_close"].pct_change(lookback).cumsum()
crntThreshold = qqq["cumulative_5d_return"].iloc[-1]

if crntThreshold > threshold:
    # buy tqqq
    switchPair("TQQQ")
else:
    # buy sqqq
    switchPair("SQQQ")