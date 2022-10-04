from datetime import date, datetime, timedelta
from math import sqrt
from random import randint
from typing import List
from urllib.parse import quote_plus

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from requests import get, post, put
from scipy.signal import argrelextrema


class BaseBot:

    def __init__(self, name: str, stocks: List[str], backendurl: str = "http://127.0.0.1:8000"):
        self.backendurl: str = backendurl
        self.headers: dict = { 'accept': 'application/json', 'Content-Type': 'application/json'}
        self.name: str = self.checkOrCreate(name)
        self.stocks: List[str] = stocks
    
    def checkOrCreate(self, name: str) -> str:
        response = get(self.backendurl + '/bot/' + quote_plus(name), headers=self.headers)
        if response.status_code != 200:
            # create
            json_data = {
                'name': name,
                'description': 'created in basebot',
            }
            response = put(self.backendurl + "/bot", json=json_data, headers=self.headers)
        return name

    def getPortfolio(self) -> dict:
        response = get(self.backendurl + '/bot/' + quote_plus(self.name), headers=self.headers)
        if response.status_code != 200:
            raise Exception("Error getting portfolio: ", response.text)
        return response.json()["portfolio"]

    def getPortfolioWorth(self) -> float:
        response = get(self.backendurl + '/bot/%s/portfolioworth' % quote_plus(self.name), headers=self.headers)
        if response.status_code != 200:
            raise Exception("Error getting portfolio worth: ", response.text)
        return response.json()["worth"]

    def buy(self, ticker: str, amount: float = -1, amountInUSD: bool = False):
        params = {
            "botname": self.name,
            'ticker': ticker,
            'amount': amount,
            "amountInUSD": amountInUSD,
        }
        response = put(self.backendurl + '/buy/', params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Error buying: ", response.text)

    def sell(self, ticker: str, amount: float = -1, amountInUSD: bool = False):
        params = {
            "botname": self.name,
            'ticker': ticker,
            'amount': amount,
            "amountInUSD": amountInUSD,
        }
        response = put(self.backendurl + '/sell/', params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Error selling: ", response.text)

    def getData(self, ticker: str, start_date: date = (datetime.utcnow() - timedelta(7)).date(), 
        end_date: date = datetime.utcnow().date(), technical_indicators: list = []):
        json_data = {
            'ticker': ticker,
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d"),
            'technical_analysis_columns': technical_indicators,
        }
        response = post(self.backendurl + '/data/', json=json_data, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Error getting data: ", response.text)
        df = pd.DataFrame(response.json())
        df.set_index("timestamp", inplace=True)
        df.sort_index(inplace=True)
        # df = df[::-1]
        return df
    
    def getCurrentPrice(self, ticker: str):
        response = get(self.backendurl + '/data/current_price/' + quote_plus(ticker), headers=self.headers)
        if response.status_code != 200:
            raise Exception("Error getting current price data: ", response.text)
        return float(response.text)
    
    def getTrend(self, df: pd.DataFrame) -> pd.DataFrame:
        if "adj_close" not in df:
            raise ValueError("adj_close not in dataframe: " + str(df.columns))
        price = df["adj_close"]
        # moving average
        price = price.rolling(window=20).mean()
        price = price.fillna(method='bfill')
        # for local maxima
        maxima = argrelextrema(price.values, np.greater)

        # for local minima
        minima = argrelextrema(price.values, np.less)
        # convert that to a target variable
        signal = np.zeros(len(price))
        lastSignal  = 0
        for i in range(len(price)):
            if i in maxima[0]:
                lastSignal = -1
            elif i in minima[0]:
                lastSignal = 1
            signal[i] = lastSignal
        return signal
        
    ## basic backtest functionality
    def getDecision(self, row: pd.Series, ticker: str = "") -> int:
        # raise NotImplementedError("getDecision not implemented")
        return randint(-1, 1)
    
    # def __oneBacktest(self, ticker: str, startdate: date, enddate: date, technical_indicators: list = []) -> int:
    #     startMoney = 10000
    #     money = startMoney
    #     nrStocks = 0
    #     data = self.getData(ticker, startdate, enddate, technical_indicators = technical_indicators)
    #     for i in range(len(data)):
    #         row = data.iloc[i]
    #         decision = self.getDecision(row)
    #         if decision == 1 and money > 0 and nrStocks == 0:
    #             amount = money / row["adj_close"] * .99
    #             cost = amount * row["adj_close"] * (1 + 0.00025) # commission
    #             money -= cost
    #             nrStocks += amount
    #         elif decision == -1 and nrStocks > 0:
    #             money += nrStocks * row["adj_close"] * (1 - 0.00025) # commission
    #             nrStocks = 0
    #     # last day sell nrStocks
    #     money += nrStocks * data.iloc[-1]["adj_close"] * (1 - 0.00025) # commission
    #     return money - startMoney
        
    
    # def backtest(self, technical_indicators: list = []) -> int:
    #     totalWins = 0
    #     # start at several points in time
    #     startdate = date(2010, 1, 1)
    #     enddate = date(2015, 12, 31)
    #     days = (enddate - startdate).days
    #     wins = 0
    #     for ticker in self.stocks:
    #         win = self.__oneBacktest(ticker, startdate, enddate, technical_indicators=technical_indicators)
    #         winPerMonth = win / days * 30
    #     wins += winPerMonth
    #     # next a shorter range
    #     startdate = date(2017, 1, 1)
    #     enddate = date(2020, 12, 31)
    #     days = (enddate - startdate).days

if __name__ == "__main__":
    bot = BaseBot("testbot")
    print(bot.getPortfolio())
    bot.buy("AAPL", 2000, amountInUSD=True)
    print("portfolio after buy")
    print(bot.getPortfolio())
    print("portfolio after sell")
    bot.sell("AAPL", 1500, amountInUSD=True)
    print(bot.getPortfolio())
    print("portfolio worth is: %.2f dollars" % bot.getPortfolioWorth())
