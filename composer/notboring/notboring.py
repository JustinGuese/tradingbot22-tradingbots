# see: tradingbot22-tradingbots/jupyternotebooks/composer.ipynb
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from basebot22.basebot import BaseBot

# basic setup
bot = BaseBot("composer-boring-v1", backendurl = "http://tradingbot-baseimage-service:8000")

# check if currentMode.txt exists, if not create it
Path("persistent/currentMode.txt").touch()
with open("persistent/currentMode.txt", "r") as f:
    currentMode = f.read()
    if currentMode == "":
        currentMode = "none"
# end basic setup

# helper functions
def switchMode(mode):
    with open("persistent/currentMode.txt", "w+") as f:
        f.write(mode)
    return mode

def get10DayMaxDrawdown(ticker):
    qqq = bot.getData(ticker, start_date = datetime.now() - timedelta(days=100))
    # calculate the max percentage drawdown of the last 45 days
    rollMax = qqq['adj_close'].rolling(10, min_periods=1).max()
    dailyDrawdown = qqq['adj_close'] / rollMax - 1.0

    maxDailyDrawdown = dailyDrawdown.rolling(10, min_periods=1).min()

    crntMaxDailyDrawdown = maxDailyDrawdown[-1]

    # print("crnt max daily drawdown qqq: " + str(crntMaxDailyDrawdown))
    return crntMaxDailyDrawdown

def calculateCurrent45dVolatility(df: pd.DataFrame):
    df["daily_returns"] = df["adj_close"].pct_change()
    # 45 bc we need 45 d volatility
    df["daily_volatility"] = df["daily_returns"].rolling(45).std()
    return df["daily_volatility"][-1]

def inverseVolatilityWeights(tickers: list):
    crntVolatilities = dict()
    for ticker in tickers:
        df = bot.getData(ticker, start_date = datetime.now() - timedelta(days=100))
        crntVolatilities[ticker] = calculateCurrent45dVolatility(df)
    # create weights according to inverse volatilities (lower volatilities get higher weights)
    print("volatilities: " + str(crntVolatilities))
    for ticker, volatility in crntVolatilities.items():
        crntVolatilities[ticker] = 1 / volatility
    weights = dict()
    for ticker, volatility in crntVolatilities.items():
        weights[ticker] = crntVolatilities[ticker] / sum(crntVolatilities.values())
    print("weights: " + str(weights))
    return weights

def buyAccordingToWeights(weights: dict):
    portfolio = bot.getPortfolio()
    usd = portfolio["USD"]
    print("portfolio: ", portfolio)
    if len(portfolio) > 1:
        # sell all stocks
        print("selling all open stocks")
        for ticker, amount in portfolio.items():
            if ticker != "USD":
                bot.sell(ticker) # all
        # reset
        portfolio = bot.getPortfolio()
        usd = portfolio["USD"]
    # buy according to weights
    if usd > 50:
        for ticker, weight in weights.items():
            print(f'buying {weight*usd}$ of {ticker}')
            bot.buy(ticker, amount = weight*usd, amountInUSD=True)
    else:
        print("not enough usd to buy u poor f#k")
    
#### trade logic
qqqCrntMaxDailyDrawdown = get10DayMaxDrawdown("QQQ")
if qqqCrntMaxDailyDrawdown < -0.06: # question: how is the "grater than" meant? 
    print("risk off mode")
    if currentMode != "risk off":
        currentMode = switchMode("risk off")
        print("switching mode to risk off")
        # get 45d inverse volatility weights
        weights = inverseVolatilityWeights(["GLD", "TMF", "FAS", "TQQQ", "UUP"])
        print(weights)
        buyAccordingToWeights(weights)
else:
    # if 10d max drawdown of TMF is greather than 7%
    # "risk off mode"
    tmfCrntMaxDailyDrawdown = get10DayMaxDrawdown("TMF")
    if tmfCrntMaxDailyDrawdown < -0.07:
        print("risk off mode")
        if currentMode != "risk off":
            currentMode = switchMode("risk off")
            print("switching mode to risk off")
            # get 45d inverse volatility weights
            weights = inverseVolatilityWeights(["GLD", "TMF", "FAS", "TQQQ", "UUP"])
            print(weights)
            buyAccordingToWeights(weights)
    else:
        # "risk on mode"
        # inverse volatility weight 45d = Assets that are more volatile receive lower weights
        # TMF, FAS, TQQQ (treasury bull 3x, financial bull 3x, 3x qqq)
        print("risk off on")
        if currentMode != "risk on":
            currentMode = switchMode("risk on")
            print("switching mode to risk on")
            # get 45d inverse volatility weights
            weights = inverseVolatilityWeights(["TMF", "FAS", "TQQQ"])
            print(weights)
            buyAccordingToWeights(weights)
    