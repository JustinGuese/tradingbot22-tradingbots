# see: tradingbot22-tradingbots/jupyternotebooks/composer.ipynb
from datetime import datetime, timedelta

from basebot22.basebot import BaseBot

# basic setup
bot = BaseBot("composer-buydipsqqq-original", backendurl = "http://tradingbot-baseimage-service:8000") # backendurl = "http://tradingbot-baseimage-service:8000"

def switchPair(tickerWanted):
    portfolio = bot.getPortfolio()
    if tickerWanted == "TQQQ":
        TOSELL = "BSV"
        TOBUY = "TQQQ"
    elif tickerWanted == "BSV":
        TOSELL = "TQQQ"
        TOBUY = "BSV"
    else:
        raise ValueError("tickerWanted must be either TQQQ or BSV")
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


# calculate 5 day cumulative return of qqq
qqq = bot.getData("QQQ", start_date = datetime.now() - timedelta(days=15))
# 5 day cumulative return of qqq
qqq["cumulative_return"] = qqq["adj_close"].pct_change(5).cumsum()
qqqCrnt5DCumRet = qqq["cumulative_return"][-1]
print("qqq now: ", qqqCrnt5DCumRet)
if qqqCrnt5DCumRet < -0.05: # if less than -5%
    # if 1d cumret of tqqq greater than 5%
    tqqq = bot.getData("TQQQ", start_date = datetime.now() - timedelta(days=5))
    tqqq["cumulative_return"] = tqqq["adj_close"].pct_change(1).cumsum()
    tqqqCrnt5DCumRet = tqqq["cumulative_return"][-1]
    print("tqqq now: ", tqqqCrnt5DCumRet)
    if tqqqCrnt5DCumRet > 0.05:
        # buy bsv, why?
        switchPair("BSV")
    else:
        # buy tqqq
        switchPair("TQQQ")
else:
    # sell all tqqq, buy bsv
    switchPair("BSV")