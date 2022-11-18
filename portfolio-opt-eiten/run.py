# needs to have train run first

import json
from os import environ

from basebot import BaseBot

with open("persistent/winners.json", "r") as f:
    winners = json.load(f)
    
priceCache = dict()

for testtype in winners.keys():

    bot = BaseBot(f"eiten_longonly_daily_weeklyRebalance_testtype-{testtype}", backendurl = environ.get("BACKENDURL", "http://localhost:8000"))
    portfolio = bot.getPortfolio()
    usd = portfolio["USD"]
    
    print("using stategy %s for testtype %s" % (winners[testtype]["name"], testtype))
    
    # first get worth of portfolio
    totalDollar = 0
    for ticker in portfolio.keys():
        if ticker == "USD":
            totalDollar += usd
            priceCache["USD"] = 1
        else:
            if ticker in priceCache:
                crntPrice = priceCache[ticker]
            else:
                priceCache[ticker] = bot.getCurrentPrice(ticker)
            totalDollar += portfolio[ticker] * priceCache[ticker]
    # then calculate weights
    crntWeights = dict()
    for ticker in portfolio.keys():
        crntWeights[ticker] = portfolio[ticker] * priceCache[ticker] / totalDollar
    print("current weights are: %s" % str(crntWeights))
    
    toBuy = dict()
    
    for ticker in winners[testtype]["weights"]:
        # compare
        if ticker in portfolio:
            # if we bought it already
            if crntWeights[ticker] < winners[testtype]["weights"][ticker]:
                # we need to buy more
                diff = winners[testtype]["weights"][ticker] - crntWeights[ticker] # only weight pct remember!
                usdAmountToBuy = diff * totalDollar / priceCache[ticker]
                # remember this until we have enough cash
                toBuy[ticker] = usdAmountToBuy
            elif crntWeights[ticker] > winners[testtype]["weights"][ticker]:
                # we need to sell
                diff = crntWeights[ticker] - winners[testtype]["weights"][ticker]
                usdAmountToSell = diff * totalDollar / priceCache[ticker]
                bot.sell(ticker, usdAmountToSell, amountInUSD=True)
        else:
            # ticker not yet bought
            priceCache[ticker] = bot.getCurrentPrice(ticker)
            usdAmountToBuy = winners[testtype]["weights"][ticker] * totalDollar / priceCache[ticker]
            toBuy[ticker] = usdAmountToBuy
            
    # now we have a list of what to buy
    portfolio = bot.getPortfolio()
    usd = portfolio["USD"]
    ## little sanity check
    if sum(toBuy.values()) > usd:
        print("not enough usd to buy all the stuff you want.")
        print("usd: %s" % str(round(usd,2)))
        print("you want to buy: ", str(toBuy))
        # adapt the sum of toBuy to usd
        divident = sum(toBuy.values()) / usd
        for ticker in toBuy:
            toBuy[ticker] /= divident
        assert sum(toBuy.values()) <= usd
    # now we can buy
    for ticker, usdAmount in toBuy.items():
        bot.buy(ticker, usdAmount, amountInUSD=True)