from datetime import datetime, timedelta
from os import environ

import numpy as np
from basebot22.basebot import BaseBot


class TrendBot(BaseBot):

    def __init__(self, name: str, stock, backendurl: str = "http://127.0.0.1:8000"):
        super().__init__(name, backendurl)
        self.stock = stock
        
    def getCurrentTrend(self, lookback = 200):
        data = self.getData(self.stock, start_date = (datetime.utcnow() - timedelta(lookback)).date())
        signal = self.getTrend(data)
        print(signal[-5:])
        if len(np.unique(signal)) < 2:
            raise ValueError("not enough lookback yet")
        decision = np.median(signal[-5:])
        return decision
    
    def act(self, decision):
        portfolio = self.getPortfolio()
        usd = portfolio["USD"]
        stocks = portfolio.get(self.stock, 0)
        if decision == 1 and stocks == 0:
            # buy
            self.buy(self.stock, amountInUSD = True, amount = usd)
            print("i buy %s" % self.stock)
        elif decision == -1 and stocks > 0:
            # sell  
            self.sell(self.stock, amount = stocks)
            print("i sell %s" % self.stock)
        else:
            print("doing nothing...")
        
if __name__ == "__main__":
    bot = TrendBot("simpletrendbot-" + environ["TICKER"], environ["TICKER"]) # , backendurl = "http://tradingbot-baseimage-service:8000")
    decision = bot.getCurrentTrend()
    bot.act(decision)
