# pip install git+https://github.com/JustinGuese/tradingbot22-basebot/
from datetime import date, timedelta
from os import environ
from time import sleep

import numpy as np
import pandas as pd
from basebot22.basebot import BaseBot

bot = BaseBot("testbot", backendurl = environ.get("BACKEND_URL", "http://tradingbot-baseimage-service:8000")) # backendurl = "https://trading:%s@tradingbot.datafortress.cloud" % environ["PW"]

def __calculateExpectedMove(earningsFinanceData: dict):
    all_changes_list = earningsFinanceData["all_changes_list"] # from the previous#
    assert len(all_changes_list) > 0
    assert isinstance(all_changes_list, list)
    # assert all numeric
    # print("all_changes_list: ", all_changes_list)
    assert all([isinstance(x, (int, float)) for x in all_changes_list])
    # now seperate positive and negative changes
    positive = [x for x in all_changes_list if x > 0]
    negative = [x for x in all_changes_list if x <= 0]
    # calculate the median
    positive = np.median(positive)
    negative = np.median(negative)
    # creatae a dict
    res = {
        "positive" : positive,
        "negative" : negative
    }
    return res

def checkExpectedMove(ticker: str, earningsFinanceData: dict):
    global bot
    # load the effect from backend
    earningsEffectObj = bot.getEarningsEffect(ticker)
    assert earningsEffectObj is not None
    assert len(earningsEffectObj) > 0
    # {
    # "ticker": "DG",
    # "medchange": -0.05,
    # "medvariance": 0.13,
    # "all_changes_list": [0.1567644054519073, -0.07509504108000069, -0.0492703679293522],
    # "best": {
    #     "Selling General Administrative": 1,
    #     "Interest Expense": 0.96,
    #     "Net Income Applicable To Common Shares": -0.25,
    #     "win": -0.64
    #   }
    # }
    print("earnings objs: ", earningsEffectObj)
    expectedChanges = __calculateExpectedMove(earningsEffectObj)
    # contains a dict with positive and negative median changes
    
    # we need to calculate the pct change 
    earningsFinanceData = pd.DataFrame(earningsFinanceData) # need 2 swag
    earningsFinanceData = earningsFinanceData.set_index("timestamp")
    earningsFinanceData = earningsFinanceData.dropna(how="all", axis=1)
    earningsFinanceData = earningsFinanceData.drop(["ticker"], axis=1)
    # print("earningsFinanceData: ", earningsFinanceData)
    earningsFinanceData = earningsFinanceData.pct_change()
    
    biggestCorr = earningsEffectObj["best"]
    biggestCorrKeys = list(biggestCorr.keys())
    
    def colNameFix(name):
        return name.replace(" ", "_").lower()
    
    # TODO: we do not have "win" yet, but I don't want to calculate it again
    if "win" in biggestCorrKeys:
        print("warning: win is in biggestcorrkeys. skip it for now.")
        earningsFinanceData["win"] = 0
    currentPositive1 = earningsFinanceData.iloc[-1][colNameFix(biggestCorrKeys[0])] # from the newest entry, the first (most positive ) correlations
    currentPositive2 = earningsFinanceData.iloc[-1][colNameFix(biggestCorrKeys[1])] # from the newest entry, the second (most positive ) correlations
    currentNegative1 = earningsFinanceData.iloc[-1][colNameFix(biggestCorrKeys[2])] # from the newest entry, the first (most negative ) correlations
    currentNegative2 = earningsFinanceData.iloc[-1][colNameFix(biggestCorrKeys[3])] # from the newest entry, the second (most negative ) correlations
    
    posVsNegCount = 0
    if currentPositive1 > 0:
        posVsNegCount += 1
    if currentPositive2 > 0:
        posVsNegCount += 1
    if currentNegative1 < 0:
        posVsNegCount -= 1
    if currentNegative2 < 0:
        posVsNegCount -= 1
    
    selector = "positive" if posVsNegCount > 0 else "negative"
    expectedChange = expectedChanges[selector]
    return {
        "expectedChange" : expectedChange,
        "posVsNegCount" : posVsNegCount
    }

def tradeOnDecision(ticker: str, expected: dict, howManyWaiting: int):
    global bot
    portfolio = bot.getPortfolio()
    usd = portfolio["usd"]
    usdThisTrade  = usd / howManyWaiting
    # expected structure is:
    # {
    #     "expectedChange" : expectedChange,
    #     "posVsNegCount" : posVsNegCount
    # }
    # act on that deicison
    crntPrice = bot.getTickerPrice(ticker)
    maximumdate = date.today() + timedelta(days=15)
    if expected["posVsNegCount"] > 0:
        # buy with stop loss
        # TODO: somehow make this, that it waits for selling off take profit until it circles back. meaning that if it exceeds the take profit, wait until reversal to sell
        takeProfitPrice = crntPrice * (1 + expected["expectedChange"]) * 0.99 # some safety net idk, need to test
        stopLossPrice = crntPrice * 0.98 # what the fuck do i know
        print("buying %s with take profit %s and stop loss %s" % (ticker, takeProfitPrice, stopLossPrice))
        bot.buy(ticker, usdThisTrade, amountInUSD=True, close_if_above = takeProfitPrice, close_if_below = stopLossPrice, maximum_date = maximumdate)
    else:
        # short with stop loss
        takeProfitPrice = crntPrice * (1 - expected["expectedChange"]) * 1.01 # some safety net idk, need to test
        stopLossPrice = crntPrice * 1.02 # what
        print("shorting %s with take profit %s and stop loss %s" % (ticker, takeProfitPrice, stopLossPrice))
        bot.buy(ticker, usdThisTrade, amountInUSD=True, short=True, close_if_below = takeProfitPrice, close_if_above = stopLossPrice, maximum_date = maximumdate)

# TODO: i dont trust the yf.calendar, i think it's maybe only the yearly earnings?
# upcomingEarnings = bot.getEarningsCalendar(only_now = True) # y does it fail now?
# # [{'timestamp': '2022-11-30T00:00:00', 'ticker': 'DG', 'earnings_avg': 2.53, 'earnings_low': 2.37, 'earnings_high': 2.66, 'revenue_avg': 9419, 'revenue_low': 9282, 'revenue_high': 9475}]
# # list of upcoming earnings
NOTHING = True
# if len(upcomingEarnings) < 0:
#     # also query previous earning publishings with  getEarningsCalendarPrevious
previousEarningDates = bot.getEarningsCalendarPrevious()  # returns a list of tiemstamp + ticker for today, if something was published today in the previous 3 years
if len(previousEarningDates) > 0:
    NOTHING = False
    upcomingEarnings = previousEarningDates # it's not completely the same, but we just need ticker and timestamp, which both have
        
    # remove duplicates of the same ticker
    clean = []
    for x in upcomingEarnings:
        if x["ticker"] not in [y["ticker"] for y in clean]:
            clean.append(x)
    upcomingEarnings = clean

if NOTHING:
    print("No upcoming earnings")
else:
    print("upcomingEarnings: ", upcomingEarnings)
    AllDone = [False] * len(upcomingEarnings)
    runNo = 0
    while not all(AllDone):
        for i, earningsObj in enumerate(upcomingEarnings):
            # query yfinance for earnings every half an hour
            bot.updateEarnings(earningsObj["ticker"])
            earningsFinanceData = bot.getEarningsFinancials(earningsObj["ticker"], only_now = False)
            currentEarningsFinanceData = earningsFinanceData[0] # the newest will be at the top
            # check if timestamp today or tomorrow
            # if we have the financial data, check if it's today's date already
            if currentEarningsFinanceData["timestamp"] == date.today() or currentEarningsFinanceData["timestamp"] == date.today() + timedelta(days = 1):
                # if it is, then we can start trading
                # print("we have an earnings update!!", currentEarningsFinanceData)
                expected = checkExpectedMove(earningsObj["ticker"], earningsFinanceData)
                
                tradeOnDecision(earningsObj["ticker"], expected, len(AllDone))
                print("%s update arrived. expected move: " % earningsObj["ticker"], expected)
                AllDone[i] = True
            else:
                print("dont have an earnings update yet for ", earningsObj["ticker"], ". re-query in half an hour. current latest earnings update is: ", currentEarningsFinanceData["timestamp"])
        runNo += 1
        print("run %d: %d/%d done. sleep 30 minutes" % (runNo, sum(AllDone), len(AllDone)))
        sleep(30 * 60) # sleep 30 minutes