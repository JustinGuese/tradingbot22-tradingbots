import json
from datetime import date
from os import environ

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from basebot import BaseBot


class LGBBot(BaseBot):
    def __init__(self, name: str, stock: str, backendurl: str = "http://127.0.0.1:8000"):
        super().__init__(name, backendurl)
        self.stock = stock

    def prepareData(self, df):
        df["pctChange"] = df["SMA_3"].pct_change()
        df["signal"] = np.sign(df["pctChange"])
        df["signal"] = self.getTrend(df)
        df = df.fillna(0)
        y = df["signal"]
        df = df.drop(["signal", "ticker"], axis = 1)
        # del df
        x_train, x_test, y_train, y_test = train_test_split(
            df, y, test_size=0.05, shuffle = True)
        train_data = lgb.Dataset(x_train, label = y_train)
        validation_data = lgb.Dataset(x_test, label=y_test, reference=train_data)
        return df, train_data, validation_data, x_test, y_test

    def getDecision(self, pred):
        if pred < -.25:
            return -1
        elif pred > .25:
            return 1
        else:
            return 0

    def getRawDecision(self, pred):
        return np.sign(pred)

    def train(self, train_data, validation_data, x_test, y_test, num_rounds = 10):
        param = dict()
        param['metric'] = ['auc', 'binary_logloss']
        bst = lgb.train(param, train_data, num_rounds, valid_sets=[validation_data])
        bst.save_model('model.txt')
        # get score
        y_pred = bst.predict(x_test)
        print("accuracy: ", np.sum(y_pred == y_test) / len(y_test))
        y_pred_soft = [self.getDecision(x) for x in y_pred]
        return bst, y_pred, y_pred_soft

    
    def backtest(self, iterations = 100, ):
        df = self.getData(self.stock, start_date = date(2020, 1, 1), end_date = date.today(), technical_indicators = ["all"])
        print(df.head())
        df.to_parquet("tmpaapldata.parquet")
        # df = pd.read_parquet("tmpaapldata.parquet")
        df, train_data, validation_data, x_test, y_test = self.prepareData(df)
        # training
        bst, y_pred, y_pred_soft = self.train(train_data, validation_data, x_test, y_test, num_rounds = iterations)
        # now simulate
        startMoney = 10000
        
        baselineStocks = startMoney / df.iloc[0]["adj_close"]
        baselineWin = baselineStocks * df.iloc[-1]["adj_close"]
        
        bestLookback = -1
        bestWin = -99999999
        for lookback in [1, 3, 5, 10, 50]:
            money = startMoney
            shares = 0
            for i in range(lookback, len(df)):
                datasnippet = df.iloc[i-lookback:i]
                pred = np.median(bst.predict(datasnippet))
                pred = self.getDecision(pred)
                pred_raw = self.getRawDecision(pred)
                lastPrice = df.iloc[i]["adj_close"]
                if pred == 1 and money > 0 and shares == 0:
                    shares = money / lastPrice * (1.00025)
                    money = 0
                elif pred == -1 and shares > 0:
                    money = shares * lastPrice * (1-0.00025)
                    shares = 0
            # at the end sell all shares
            if shares > 0:
                money += shares * lastPrice
            if money > bestWin:
                bestWin = money
                bestLookback = lookback
        print("money with lookback %d is %.2f$" % (bestLookback, bestWin))
        print("money per month", bestWin / len(df) / 30)
        print("baseline money: ", baselineWin)
        # pred
        # accuracy:  0.0
        # money:  67480.58600966299
        # money per month 2.4083007141207347
        # baseline money:  38594.22413472413

    def run(self, lookback = 3):
        df = self.getData(self.stock, technical_indicators = ["all"])
        # df = pd.read_parquet("tmpaapldata.parquet")
        df, train_data, validation_data, x_test, y_test = self.prepareData(df)
        # training
        bst, y_pred, y_pred_soft = self.train(train_data, validation_data, x_test, y_test, num_rounds = 100)
        # get last data and preds
        datasnippet = df.iloc[-lookback:]
        pred = bst.predict(datasnippet)
        pred = np.sign(np.median(pred))
        # print("i predict. ", pred)
        if pred != 0:
            portfolio = self.getPortfolio()
            if pred == 1 and portfolio["USD"] > 10 and portfolio.get(environ["TICKER"], 0) == 0:
                self.buy(environ["TICKER"])
                print("bought ", environ["TICKER"])
            elif pred == -1 and portfolio.get(environ["TICKER"], 0) > 0:
                self.sell(environ["TICKER"])
                print("sold ", environ["TICKER"])
            else:
                print("nothing to do")

if __name__ == "__main__":
    environ["TICKER"] = "AAPL"
    
    bot = LGBBot("lgb-trend-bot-" + environ["TICKER"], environ["TICKER"]) # , backendurl="http://tradingbot-baseimage-service:8000"
    bot.backtest()
    # bot.run()
