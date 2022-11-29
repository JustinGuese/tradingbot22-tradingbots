# pip install git+https://github.com/JustinGuese/tradingbot22-basebot/
from datetime import date, timedelta
from os import environ

from basebot22.basebot import BaseBot
from tqdm import tqdm

bot = BaseBot("testbot", backendurl = "https://trading:%s@tradingbot.datafortress.cloud" % environ["PW"])

upcomingEarnings = bot.getEarningsCalendar(only_now = True) # y does it fail now?
# [{'timestamp': '2022-11-30T00:00:00', 'ticker': 'DG', 'earnings_avg': 2.53, 'earnings_low': 2.37, 'earnings_high': 2.66, 'revenue_avg': 9419, 'revenue_low': 9282, 'revenue_high': 9475}]
# list of upcoming earnings
if len(upcomingEarnings) < 0:
    print("No upcoming earnings")
else:
    AllDone = [False] * len(upcomingEarnings)
    for i, earningsObj in enumerate(upcomingEarnings):
        # query yfinance for earnings every half an hour
        bot.updateEarnings(earningsObj["ticker"])
        earningsFinanceData = bot.getEarningsFinancials(earningsObj["ticker"], only_now = True)
        earningsFinanceData = earningsFinanceData[0]
        # check if timestamp today or tomorrow
        earningsFinanceData["timestamp"] = earningsFinanceData["timestamp"].date()
        # if we have the financial data, check if it's today's date already
        if earningsFinanceData["timestamp"] == date.today() or earningsFinanceData["timestamp"] == date.today() + timedelta(days = 1):
            # if it is, then we can start trading
            print("we have an earnings update!!", earningsFinanceData)
            AllDone[i] = True
        else:
            print("dont have an earnings update yet for ", earningsFinanceData["ticker"], ". re-query in half an hour. current latest earnings update is: ", earningsFinanceData["timestamp"])
print("\nupcoming earnings: ")
for earningsObj in upcomingEarnings:
    print(earningsObj)