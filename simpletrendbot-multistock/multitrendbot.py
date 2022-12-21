from datetime import datetime, timedelta
from os import environ

import numpy as np
from basebot22.basebot import BaseBot
from tqdm import tqdm


class TrendBot(BaseBot):

    def __init__(self, name: str, backendurl: str = "http://127.0.0.1:8000"):
        super().__init__(name, backendurl)
        
    def getCurrentTrend(self, stock, lookback = 200):
        data = self.getData(stock, start_date = (datetime.utcnow() - timedelta(lookback)).date())
        signal = self.getTrend(data)
        signal = signal.drop(["ticker"], axis=1)
        if len(np.unique(signal)) < 2:
            raise ValueError("not enough lookback yet")
        decision = np.median(signal[-5:])
        return decision
    
        
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
        
if __name__ == "__main__":
    bot = TrendBot("simpletrendbot-multistock-v1", backendurl= environ.get("BACKENDURL", "http://10.43.226.131:8000")) # debug http://10.43.226.131:8000
    portfolio = bot.getPortfolio()
    usd = portfolio["USD"] 
    buy = []
    sell = []
    for ticker in tqdm(ALL_TRADEABLE):
        decision = bot.getCurrentTrend(ticker)
        holding = portfolio.get(ticker, 0)
        if decision == 1 and holding == 0:
            buy.append(ticker)
        elif decision == -1 and holding > 0:
            sell.append(ticker)
            
    for ticker in sell:
        print("i sell %s" % ticker)
        bot.sell(ticker) # sell all
    if len(sell) > 0:
        # refresh
        portfolio = bot.getPortfolio()
        usd = portfolio["USD"] 
    for ticker in buy:
        print("i buy %s" % ticker)
        bot.buy(ticker, amountInUSD = True, amount = usd / len(buy))