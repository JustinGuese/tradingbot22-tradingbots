# needs to have train run first

import json
from os import environ

from basebot import BaseBot

with open("persistent/winners.json", "r") as f:
    winners = json.load(f)
    
priceCache = dict()

for testtype in winners.keys():

    bot = BaseBot(f"eiten_longshort_daily_monthlyRebalance_testtype-{testtype}", backendurl = environ.get("BACKENDURL", "http://localhost:8000"))
    portfolio = bot.getPortfolio()
    usd = portfolio["USD"]
    
    print("using stategy %s for testtype %s" % (winners[testtype]["name"], testtype))
    
    
    
    # now we need to pay attention to shorts...
    # sell everything first
    for ticker, amount in portfolio.items():
        if ticker != "USD":
            bot.sell(ticker, -1, short = amount < 0)
        
    # then get worth of portfolio
    worth = bot.getPortfolioWorth()
    
    for ticker, targetWeight in winners[testtype]["weights"].items():
        amount = worth * targetWeight
        bot.buy(ticker, abs(amount), amountInUSD = True, short = targetWeight < 0)