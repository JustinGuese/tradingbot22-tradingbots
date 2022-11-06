import json
from datetime import date
from os import path
from pathlib import Path

import numpy as np
from sklearn.tree import DecisionTreeClassifier, _tree
from tqdm import tqdm

from basebot import BaseBot

startMoney = 10000
COMMISSION = 0.00025
code = ""

# use decision tree
def oneRun(model, X, lookbackarray = [1]):
    preds = model.predict(X)
    # print("the predictions are: ", np.unique(preds, return_counts=True))
    bestLookback = -1
    bestLookbackWin = -9999
    bestLookbackPortfolio = []
    for lookback in lookbackarray: # range(0, 5):
        money = startMoney
        nrStocks = 0
        portfolio = []
        for i in range(lookback, len(X)):
            if lookback > 0:
                prednow = np.median(preds[i-lookback:i+1])
            else:
                prednow = preds[i]
            # "translate" 0 to -1 like we did it before
            if prednow == 0:
                prednow = -1
            # print("prednow is, " , prednow)
            # prednow = preds[i]
            if prednow == 1 and nrStocks == 0 and money > 10:
                # buy
                howmany = money / X.iloc[i]["adj_close"] * .99
                cost = howmany * X.iloc[i]["adj_close"] * (1 + COMMISSION)
                money -= cost
                nrStocks += howmany
            elif prednow == -1 and nrStocks > 0:
                money += nrStocks * X.iloc[i]["adj_close"] * (1 - COMMISSION)
                nrStocks = 0
            portfolio.append(money + nrStocks * X.iloc[i]["adj_close"])
        # last day sell
        money += nrStocks * X.iloc[-1]["adj_close"] * (1 - COMMISSION)
        win = money - startMoney
        if win > bestLookbackWin:
            bestLookback = lookback
            bestLookbackWin = win
            bestLookbackPortfolio = portfolio
    return bestLookbackWin, bestLookback, bestLookbackPortfolio


def tree_to_code(tree, feature_names):
    global code
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    feature_names = [f.replace(" ", "_")[:-5] for f in feature_names]
    code += "def getDecision(dfrow):\n"

    def recurse(node, depth):
        global code
        indent = "    " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            code += "{}if dfrow['{}'] <= {}:\n".format(indent, name, np.round(threshold,2))
            recurse(tree_.children_left[node], depth + 1)
            code += "{}else:  # if dfrow['{}'] > {}\n".format(indent, name, np.round(threshold,2))
            recurse(tree_.children_right[node], depth + 1)
        else:
            code += "{}return {}\n".format(indent, np.argmax(tree_.value[node][0]))

    recurse(0, 1)
# tree_to_code(clf, x_train.columns)

def getBestTree(ticker):
    global code
    bot = BaseBot("testbot")
    data = bot.getData(ticker, date(2015,1,1), date.today(), technical_indicators = ["all"])
    data = bot.getTrend(data)

    # get baseline
    startMoney = 10000
    COMMISSION = 0.00025 # interactive brokers commission
    howmany = startMoney / data.iloc[0]["adj_close"]
    win = howmany * data.iloc[-1]["adj_close"] - startMoney

    days = (data.index[-1] - data.index[0]).days

    print("with just holding you would have made %.2f$" % win)
    winPerMonth = win / (days / 30)
    winPctPerYear = winPerMonth * 12 / startMoney * 100
    print("or %.2f%% per year" % winPctPerYear)
    print("or %.2f$ per month" % winPerMonth)
    X, Y = data.drop(["signal", "ticker"], axis=1), data["signal"]


    bestDepth = -1
    bestLeafes = -1
    bestLookback = -1
    bestDepthWin = -9999
    collection = []
    # explicitly force a max of 20 to prevent overfitting
    for depth in [50,40,30,20,15,10,5]:
        for leafes in [50,40,30,20,15,10,5]:
            clf = DecisionTreeClassifier(max_depth=depth, max_leaf_nodes = leafes)
            # train with bigdf, test with df (all world)
            clf.fit(X,Y)
            # scr = clf.score(X, Y)
            # print("score is: ", scr)
            bestLookbackWin, lookback, bestLookbackPortfolio = oneRun(clf, X, lookbackarray = [0,1,3,5,10])
            collection.append([depth,leafes,lookback,bestLookbackWin])
            if bestLookbackWin >= (bestDepthWin*.95): # equal to prefer smaller trees, 95% to accept a bit worse for smaller trees
                bestDepthWin = bestLookbackWin
                bestDepth = depth
                bestLeafes = leafes
                bestLookback = lookback
    print("the best depth is %d, best leave %d, best lookback %d. with a win of %.2f$" % (bestDepth, bestLeafes, bestLookback, bestDepthWin))
    code = ""
    tree_to_code(clf, X.columns)
    # make sure bestSettings folder exists
    Path("bestSettings").mkdir(parents=True, exist_ok=True)
    
    with open("bestSettings/%s.py" % ticker, "w") as f:
        f.write(code)
    code = ""
    if path.exists("bestSettings/all.json"):
        with open("bestSettings/all.json", "r") as f:
            settings = json.load(f)
    else:
        settings = {}
    settings[ticker] = {"win" : bestDepthWin, "depth": bestDepth, "leafes": bestLeafes, "lookback": bestLookback}
    with open("bestSettings/all.json", "w") as f:
        json.dump(settings, f, indent = 4)

ALLOWED_STOCKS = [
    "AAPL", "MSFT", "GOOG", "TSLA", 'AMD', 'AMZN', 'DG', 'KDP', 'LLY', 'NOC', 'NVDA', 'PGR', 'TEAM', 'UNH', 'WM',  # stocks
    "CWEG.L", "IWDA.AS", "EEM", # etfs
    "BTC-USD", "ETH-USD", "AVAX-USD" # crypto
]

# only do this on the first of the month or if the file does not exist
today = date.today()
if today.day == 1 or not path.exists("bestSettings/all.json"):
    print("running getBestTree for all stocks")
    for ticker in tqdm(ALLOWED_STOCKS):
        getBestTree(ticker)
