# The granddaddy of internet-famous investing strategies. In 2019, Hedgefundie, a member of the Bogleheads investing forum, proposed a simple strategy to replicate an aggressive risk parity portfolio. Two uncorrelated, leveraged assets -- equities and bonds -- are combined with the goal of achieving higher risk adjusted returns than an equivalent unleveraged portfolio. 
# This strategy was developed by Hedgefundie 
# it is a one time setup.

from datetime import datetime, timedelta

from basebot22.basebot import BaseBot

# get 20d cumulative return
bot = BaseBot("composer-hedgefundies-excellent-static-v1")
portfolio = bot.getPortfolio()
usd = portfolio["USD"]
bot.buy("UPRO", amount = usd * 0.55, amountInUSD= True)
bot.buy("TMF", amount = usd * 0.45, amountInUSD= True)