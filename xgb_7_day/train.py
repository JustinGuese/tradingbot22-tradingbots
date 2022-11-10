import json
from datetime import date, timedelta
from os import environ
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from basebot import BaseBot


def prepareData(ticker: str, train: bool = True) -> pd.DataFrame:
    if train:
        lookback = date(2015,1,1)
    else:
        lookback = date.today() - timedelta(days=30)
    bot = BaseBot("testbot", backendurl=environ.get("BACKENDURL", "http://tradingbot-baseimage-service:8000"))
    data = bot.getData(ticker, lookback, date.today(), technical_indicators = ["all"])
    data["adj_close_pct_change"] = data["adj_close"].pct_change() # get daily returns
    # make signal -1 or 1 depending on if the adj_close will be higher or lower in 7 days
    data["signal"] = data["adj_close"].shift(-7) > data["adj_close"]
    data["signal"] = data["signal"].astype(int)
    # data["signal"] = data["signal"].replace(0, -1)
    data["signal"] = data["signal"].fillna(1) # positive market outlook

    # data["signal"].value_counts()
    # X, Y = data.drop(["ticker", "signal"], axis=1), data["signal"]
    return data

def findBestLookback(ticker: str, x_train: pd.DataFrame, model: XGBClassifier) -> int:

    startMoney = 10000
    bestWin = -9999999
    bestSettings = dict()

    for lookback in [1,5,7,10,13,15,20]:
        money = startMoney
        stocks = 0
        portfolio = []
        baseline = []
        baselineHowmany = money / x_train.iloc[0]["adj_close"]
        for i in range(lookback, len(x_train)):
            crntPrice = x_train.iloc[i]["adj_close"]
            preds = model.predict(x_train.iloc[i-lookback:i])
            # print("preds: ", preds)
            pred = np.median(preds)
            if pred == 1 and money > 10 and stocks == 0:
                # buy
                howMany = money / crntPrice * 0.98
                cost = howMany * crntPrice
                money -= cost
                stocks = howMany
            elif pred == 0 and stocks > 0:
                # sell
                money += stocks * crntPrice
                stocks = 0
            portfolio.append(money + stocks * crntPrice)
            baseline.append(baselineHowmany * crntPrice)
        if portfolio[-1] > bestWin:
            bestWin = portfolio[-1]
            bestSettings = dict(lookback = lookback, win=portfolio[-1], baselineWin = baselineHowmany) #  portfolio = portfolio, baseline = baseline
    # print("best win: ", bestWin, lookback)
    with open(f"persistent/{ticker}_best_settings.json", "w") as f:
        json.dump(bestSettings, f, indent=4)
    return lookback

def train(ticker: str, data: pd.DataFrame) -> Tuple[pd.DataFrame, XGBClassifier]:
    X, Y = data.drop(["ticker", "signal"], axis=1), data["signal"]
    # x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, shuffle=False)
    # use the last one for pred only as we fake it
    x_train_shuffled, _, y_train_shuffled, _ = train_test_split(X.iloc[:-1], Y.iloc[:-1], test_size=0.001, shuffle=True)
    model = XGBClassifier(n_jobs = -1)
    model.fit(x_train_shuffled, y_train_shuffled)
    joblib.dump(model, f"persistent/{ticker}_model.pkl")
    # find best lookback
    lookback = findBestLookback(ticker, X.iloc[:-1], model)
    lastX = X.iloc[-lookback:]
    return lastX, model # the row we are going to predict

def loadLatest(ticker: str) -> Tuple[pd.DataFrame, XGBClassifier]:
    model = joblib.load(f"persistent/{ticker}_model.pkl")
    with open(f"persistent/{ticker}_best_settings.json", "r") as f:
        bestSettings = json.load(f)
    lookback = bestSettings["lookback"]
    data = prepareData(ticker, train=False)
    X, Y = data.drop(["ticker", "signal"], axis=1), data["signal"]
    lastX = X.iloc[-lookback:]
    return lastX, model