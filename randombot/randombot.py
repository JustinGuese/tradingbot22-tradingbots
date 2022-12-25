from os import environ
from random import random

from basebot22.basebot import BaseBot

ALL_TRADEABLE = [
"AAPL",
"MSFT",
"GOOG",
"TSLA",
"AMD",
"AMZN",
"DG",
"KDP",
"LLY",
"NOC",
"NVDA",
"PGR",
"TEAM",
"UNH",
"WM",
"URTH",
"IWDA.AS",
"EEM",
"XAIX.DE",
"BTEC.L",
"L0CK.DE",
"2B76.DE",
"W1TA.DE",
"RENW.DE",
"BNXG.DE",
"BTC-USD",
"ETH-USD",
"AVAX-USD"
]

bot = BaseBot("randombot-v1", backendurl= environ.get("BACKENDURL", "http://10.43.226.131:8000")) # debug http://10.43.226.131:8000
portfolio = bot.getPortfolio()
usd = portfolio["USD"] 
for ticker in ALL_TRADEABLE:
    if random() > 0.95:
        print("i buy %s" % ticker)
        bot.buy(ticker, amount = usd * random(), amountInUSD = True)
    elif random() < 0.05:
        if ticker in portfolio:
            print("i sell %s" % ticker)
            bot.sell(ticker) # sell all