from basebot import BaseBot
from datetime import date
import pandas as pd
from tqdm import tqdm
import numpy as np
import json
from os import environ

class RSIExampleBot(BaseBot):
    def __init__(self, name: str, stock: str, backendurl: str = "http://127.0.0.1:8000"):
        super().__init__(name, backendurl)
        self.stock = stock
        self.rsi_threshold = 30

    def getDecision(self, datarow):
        if datarow["momentum_rsi"] < self.rsi_threshold:
            return "buy"
        elif 100 - datarow["momentum_rsi"] > self.rsi_threshold:
            return "sell"
        return "hold"
    
    def backtest(self):
        df = self.getData(self.stock, start_date = date(2019, 1, 1), end_date = date.today(), technical_indicators = ["momentum_rsi"])
        bestWins = dict()
        commission = 0.0005
        startMoney = 10000
        nrStocks = 0

        baselineNrStocks = startMoney / df.iloc[0]["close"] * (1 - commission)
        baselineWin = baselineNrStocks * df.iloc[-1]["close"] * (1 - commission) - startMoney

        money = startMoney
        nrStocks = 0
        trades = []

        for i in range(len(df)):
            row = df.iloc[i]
            decision = self.getDecision(row)
            crntPrice = row["close"]
            if decision == "buy" and nrStocks == 0:
                howmany = money * (1 - commission) / crntPrice
                money -= (howmany * crntPrice) * (1 + commission)
                nrStocks += howmany
            elif decision == "sell" and nrStocks > 0:
                win = (nrStocks * crntPrice) * (1 - commission)
                money += win
                nrStocks = 0
                trades.append(win)
        # at the end liquidate all stocks
        money += nrStocks * crntPrice
        print("win is: ", money - startMoney)
        print("baseline win is: ", baselineWin)
        print("win over just holding: ", money - startMoney - baselineWin)
        print("nr trades: ", len(trades))
        return money - baselineWin

    def run(self):
        df = self.getData(self.stock, technical_indicators = ["momentum_rsi"])
        decision = self.getDecision(df.iloc[-1])
        print("decision is: ", decision)
        if decision != "hold":
            portfolio = self.getPortfolio()
            if decision == "buy" and self.stock not in portfolio:
                print("buying ", self.stock)
                self.buy(self.stock)
            elif decision == "sell" and self.stock in portfolio:
                print("selling ", self.stock)
                self.sell(self.stock)
        else:
            print("not doing/holding ", self.stock)

if __name__ == "__main__":
    bot = RSIExampleBot("rsi-bot-" + environ["TICKER"], environ["TICKER"], backendurl="http://tradingbot-baseimage-service:8000")
    # winOverHolding = bot.backtest()
    bot.run()