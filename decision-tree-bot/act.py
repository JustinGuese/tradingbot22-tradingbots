import json
from datetime import datetime, timedelta

import pandas as pd

from basebot import BaseBot

with open("bestSettings/all.json", "r") as f:
    settings = json.load(f)
    
df = pd.DataFrame(settings).T
df = df.sort_values(by="win", ascending=False)
# kick out all wins below 11000
df = df[df["win"] > 11000]
totalWin = df["win"].sum()
df["winPct"] = df["win"] / totalWin
print(df)

bot = BaseBot("decision-tree-bot-v1")

portfolio = bot.getPortfolio()
usd = portfolio["USD"]
print("portfolio", portfolio)

for ticker in df.index:
    # import the matching decision
    with open(f"bestSettings/{ticker}.py", "r") as f:
        code = f.read()
    with open("tmpcode.py" , "w") as f:
        f.write(code)
    from tmpcode import getDecision

    # get latest data
    tickerdata = bot.getData(ticker, (datetime.utcnow() - timedelta(2)).date(), 
        datetime.utcnow().date(), technical_indicators = ["all"])
    
    decision = getDecision(tickerdata.iloc[-1])
    # 0 is sell, 1 is buy
    print(f"for {ticker} decision is {decision}")
    
    if portfolio.get(ticker, 0) > 0:
        if decision == 0:
            print(f"selling {ticker}")
            bot.sell(ticker, portfolio[ticker])
    elif portfolio.get(ticker, 0) == 0:
        if decision == 1:
            print(f"buying {ticker}")
            buyWeight = df.loc[ticker, "winPct"]
            bot.buy(ticker, usd * buyWeight, amountInUSD=True)