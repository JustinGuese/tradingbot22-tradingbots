# see: tradingbot22-tradingbots/jupyternotebooks/composer.ipynb
from datetime import datetime, timedelta

# further adapted to use the getTrend function we already have
from basebot22.basebot import BaseBot

# basic setup
bot = BaseBot("composer-buydipsqqq-shorting-gettrend", backendurl = "http://tradingbot-baseimage-service:8000") # backendurl = "http://tradingbot-baseimage-service:8000"

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
qqq = bot.getTrend(qqq)
crntTrend = qqq["signal"][-1] # either 1 or -1 for up or down trend

if crntTrend == 1:
    print("uptrend, buy TQQQ")
    switchPair("TQQQ")
elif crntTrend == -1:
    print("downtrend, buy SQQQ")
    switchPair("SQQQ")
else:
    raise ValueError("crntTrend must be either 1 or -1. is: ", str(crntTrend))