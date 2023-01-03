# weights
# 15% eff core
# 25% vol hedge
# 25% sector momentum
# 15% large cap val
# 20% commodity momentum

# effcore
# 15% NTSX

# volatility hedge
# 25%, inverse volatility 30d weight, GLD, UUP, DBMF

# sector momentum
# 25%, top 2 of 200d cum return of: VDE, VNQ, VHT, VFH, VOX, VPU, VAW, VGT, VIS, VDC, VCR

# large cap val
# 15%, inverse volatility 21d, VLUE, FNDX, VTV, RWL

# comodity momentum
# 20%, equal weights of
# agriculture, if 42d cum ret of DBA is greater than 42d cum ret of SHV, then DBA, else SHV
# base metals, if 42d cum ret of DBB is greater than 42d cum ret of SHV, then DBB, else SHV
# oil, if 42d cum ret of DBO is greater than 42d cum ret of SHV, then DBO, else SHV
# uranium, if 42d cum ret of URA is greater than 42d cum ret of SHV, then URA, else SHV
# timber, if 42d cum ret of WOOD is greater than 42d cum ret of SHV, then WOOD, else SHV
# gold, if 42d cum ret of GLD is greater than 42d cum ret of SHV, then GLD, else SHV
# energy, if 42d cum ret of DBE is greater than 42d cum ret of SHV, then DBE, else SHV
# list all the symbols mentioned above
# symbols = ['NTSX', 'GLD', 'UUP', 'DBMF', 'VDE', 'VNQ', 'VHT', 'VFH', 'VOX', 'VPU', 
#         'VAW', 'VGT', 'VIS', 'VDC', 'VCR', 'VLUE', 'FNDX', 'VTV', 'RWL', 'DBA', 'SHV', 
#         'DBB', 'DBO', 'URA', 'WOOD', 'DBE']

from datetime import datetime, timedelta
from os import environ

import pandas as pd
from basebot22.basebot import BaseBot

MODE = environ.get("MODE", "opus")
MODES = ["opus", "effcore", "volhedge", "sectormom", "largecapval", "commodmom"]
if MODE not in MODES:
    raise ValueError(f"MODE must be one of {MODES}")
bot = BaseBot("composer-oppy-" + MODE + "-v1", backendurl = "http://tradingbot-baseimage-service:8000")

def effcore(budget: float):
    return {"NTSX": 1. * budget} # bc we want to return this 

def calculateCurrentVolatility(df: pd.DataFrame, range: int = 45):
    df["daily_returns"] = df["adj_close"].pct_change()
    # 45 bc we need 45 d volatility
    df["daily_volatility"] = df["daily_returns"].rolling(range).std()
    return df["daily_volatility"][-1]

def inverseVolatilityWeights(bot, tickers: list, range: int = 45):
    crntVolatilities = dict()
    for ticker in tickers:
        df = bot.getData(ticker, start_date = datetime.now() - timedelta(days=100))
        crntVolatilities[ticker] = calculateCurrentVolatility(df, range)
    # create weights according to inverse volatilities (lower volatilities get higher weights)
    print("volatilities: " + str(crntVolatilities))
    for ticker, volatility in crntVolatilities.items():
        crntVolatilities[ticker] = 1 / volatility
    weights = dict()
    for ticker, volatility in crntVolatilities.items():
        weights[ticker] = crntVolatilities[ticker] / sum(crntVolatilities.values())
    print("weights: " + str(weights))
    return weights

def volhedge(budget: float):
    global bot
    weights = inverseVolatilityWeights(bot, ["GLD", "UUP", "DBMF"], 30)
    return {k: v * budget for k, v in weights.items()}

def sectormom(budget: float, range: int = 200):
    global bot
    tickers = ["VDE", "VNQ", "VHT", "VFH", "VOX", "VPU", "VAW", "VGT", "VIS", "VDC", "VCR"]
    cumret = dict()
    for ticker in tickers:
        df = bot.getData(ticker, start_date = datetime.now() - timedelta(days=int(range*1.5)))
        df["cumulative_return"] = (df["close"] / df["close"].shift(range)) - 1
        cumret[ticker] = df["cumulative_return"].iloc[-1]
        assert cumret[ticker] is not None, f"cumret is None for {ticker}"
    cumret = {k: v for k, v in sorted(cumret.items(), key=lambda item: item[1], reverse=True)}
    print("sectormom cumret: ", cumret)
    biggestTwo = list(cumret.keys())[:2]
    return {biggestTwo[0]: 0.5 * budget, biggestTwo[1]: 0.5 * budget}

def largecapval(budget: float):
    global bot
    weights = inverseVolatilityWeights(bot, ["VLUE", "FNDX", "VTV", "RWL"], 21)
    return {k: v * budget for k, v in weights.items()}

def __buyHelper(tobuy: dict, cumret: dict, ticker: str):
    if cumret[ticker] > cumret["SHV"]:
        if ticker not in tobuy:
            tobuy[ticker] = 0
        tobuy[ticker] +=  1
    else:
        if "SHV" not in tobuy:
            tobuy["SHV"] = 0
        tobuy["SHV"] += 1
    return tobuy, cumret

def commodmom(budget: float, range: int = 42):
    global bot
    symbols = ['DBA', 'SHV', 'DBB', 'DBO', 'URA', 'WOOD', 'DBE', 'GLD']
    tobuy = dict()
    cumret = dict()
    # get several cum returns
    for ticker in symbols:
        df = bot.getData(ticker, start_date = datetime.now() - timedelta(days=int(range*1.2)))
        df["cumulative_return"] = (df["close"] / df["close"].shift(range)) - 1
        cumret[ticker] = df["cumulative_return"].iloc[-1]
    ## logics
    # agriculture 
    tobuy, cumret = __buyHelper(tobuy, cumret, "DBA")
    # base metals
    tobuy, cumret = __buyHelper(tobuy, cumret, "DBB")
    # oil
    tobuy, cumret = __buyHelper(tobuy, cumret, "DBO")
    # uranium
    tobuy, cumret = __buyHelper(tobuy, cumret, "URA")
    # timber
    tobuy, cumret = __buyHelper(tobuy, cumret, "WOOD")
    # gold
    tobuy, cumret = __buyHelper(tobuy, cumret, "GLD")
    # energy
    tobuy, cumret = __buyHelper(tobuy, cumret, "DBE")
    
    # convert the counts to weights
    tobuy = {k: v / sum(tobuy.values()) for k, v in tobuy.items()}
    print("commodmom tobuy: ", tobuy)
    return {k: v * budget for k, v in tobuy.items()}


### the final trade logic
# MODES = ["opus", "effcore", "volhedge", "sectormom", "largecapval", "commodmom"]
portfolio = bot.getPortfolio()
usd = portfolio["USD"]
portfolioWorth = bot.getPortfolioWorth()
if MODE == "opus":
    # weights
    # 15% eff core
    # 25% vol hedge
    # 25% sector momentum
    # 15% large cap val
    # 20% commodity momentum
    effcoreweights = effcore(0.15 * portfolioWorth)
    volhedgeweights = volhedge(0.25 * portfolioWorth)
    sectormomweights = sectormom(0.25 * portfolioWorth)
    largecapvalweights = largecapval(0.15 * portfolioWorth)
    commodmomweights = commodmom(0.20 * portfolioWorth)
    # merge
    allWeights = {**effcoreweights, **volhedgeweights, **sectormomweights, **largecapvalweights, **commodmomweights}
    
elif MODE == "effcore":
    allWeights = effcore(portfolioWorth)
elif MODE == "volhedge":
    allWeights = volhedge(portfolioWorth)
elif MODE == "sectormom":
    allWeights = sectormom(portfolioWorth)
elif MODE == "largecapval":
    allWeights = largecapval(portfolioWorth)
elif MODE == "commodmom":
    allWeights = commodmom(portfolioWorth)
else:
    raise ValueError(f"MODE must be one of {MODES}")

assert allWeights
print("all Weights in mode %s: " % MODE, allWeights)

## calculate current holdings
toSell = []
portfolioHoldings = dict()
for ticker, amount in portfolio.items():
    if ticker == "USD":
        worth = amount
    else:
        crntPrice = bot.getCurrentPrice(ticker)
        worth = amount * crntPrice
        if ticker not in allWeights.values():
            toSell.append(ticker)
    portfolioHoldings[ticker] = worth
    
## calculate the difference
for ticker in toSell:
    print("selling off all %s" % ticker)
    bot.sell(ticker)
portfolio = bot.getPortfolio()
portfolioWorth = bot.getPortfolioWorth()


for ticker, weight in allWeights.items():
    if ticker not in portfolio:
        difference = weight
    else:
        difference = weight - portfolio[ticker]
    if abs(difference) > 100: # only act if difference bigger 100$
        if difference > 0:
            print("buying %.2f$ of %s" % (difference, ticker))
            bot.buy(ticker, amount = difference, amountInUSD= True)
        elif difference < 0:
            print("selling %.1f$ of %s" % (difference, ticker))
            bot.sell(ticker, amount = abs(difference), amountInUSD= True)