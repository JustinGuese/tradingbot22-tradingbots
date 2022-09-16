from basebot import BaseBot
from datetime import date
import pandas as pd
from tqdm import tqdm
import numpy as np
import json
from os import environ
import lightgbm as lgb
from sklearn.model_selection import train_test_split


class LGBBot(BaseBot):
    def __init__(self, name: str, stock: str, backendurl: str = "http://127.0.0.1:8000"):
        super().__init__(name, backendurl)
        self.stock = stock

    def prepareData(self, df):
        df["pctChange"] = df["SMA_3"].pct_change()
        df["signal"] = np.sign(df["pctChange"])
        df["signal"] = df["signal"].shift(-1)
        df = df.fillna(0)
        y = df["signal"]
        df = df.drop(["signal", "ticker"], axis = 1)
        # del df
        x_train, x_test, y_train, y_test = train_test_split(
            df, y, test_size=0.2)
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

    
    def backtest(self):
        # df = self.getData(self.stock, start_date = date(2019, 1, 1), end_date = date.today(), technical_indicators = ["all"])
        # print(df.head())
        # df.to_parquet("tmpaapldata.parquet")
        df = pd.read_parquet("tmpaapldata.parquet")
        df, train_data, validation_data, x_test, y_test = self.prepareData(df)
        # training
        bst, y_pred, y_pred_soft = self.train(train_data, validation_data, x_test, y_test)
        # now simulate
        startMoney = 10000
        money = startMoney
        shares = 0
        baselineStocks = money / df.iloc[0]["close"]
        baselineWin = baselineStocks * df.iloc[-1]["close"]
        for i in range(len(df)):
            datasnippet = df.iloc[i]
            pred = bst.predict([datasnippet])[0]
            pred = self.getDecision(pred)
            pred_raw = self.getRawDecision(pred)
            
            if pred == 1 and money > 0 and shares == 0:
                shares = money / datasnippet["close"]
                money = 0
            elif pred == -1 and shares > 0:
                money = shares * datasnippet["close"]
                shares = 0
            
        # at the end sell all shares
        if shares > 0:
            money += shares * datasnippet["close"]
        print("money: ", money)
        print("money per month", money / len(df) / 30)
        print("baseline money: ", baselineWin)
        # pred
        # accuracy:  0.0
        # money:  67480.58600966299
        # money per month 2.4083007141207347
        # baseline money:  38594.22413472413


        
        




    def run(self):
        df = self.getData(self.stock, technical_indicators = ["all"])
        # df = pd.read_parquet("tmpaapldata.parquet")
        df, train_data, validation_data, x_test, y_test = self.prepareData(df)
        # training
        bst, y_pred, y_pred_soft = self.train(train_data, validation_data, x_test, y_test, num_rounds = 100)
        # get last data and preds
        datasnippet = df.iloc[-3:]
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
    bot = LGBBot("lgb-bot-" + environ["TICKER"], environ["TICKER"], backendurl="http://tradingbot-baseimage-service:8000") # , backendurl="http://tradingbot-baseimage-service:8000"
    # winOverHolding = bot.backtest()
    bot.run()